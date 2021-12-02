
#include "pch.h" // use stdafx.h in Visual Studio 2017 and earlier
#include <utility>
#include <limits.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "Gen_Operation.h"
#pragma warning (disable:4996)
//#define LOG_SIZE 496163
//#define LOG_SIZE 54799
#define LOG_SIZE 404946
//#define LOG_SIZE 146017

typedef struct logInfo {
    char name[6];
    int stockPrice;
    int isReasonable;
} log_info;

// DLL internal state variables:
static log_info log_list[LOG_SIZE];
static double data[LOG_SIZE][13];

void init_data() {
    FILE* fp;
    fp = fopen("data_for_GA.csv", "r");
    for (int i = 0;i < LOG_SIZE; i++) {
        char a[400];
        fgets(a, sizeof(a), fp);

        char* ptr = strtok(a, ",'");
        double x;
        int j = 0;

        while (ptr != NULL) {
            if (j == 13) {
                log_list[i].stockPrice = atoi(ptr);
                ptr = strtok(NULL, ",'");
                j++;
                continue;
            }
            if (j == 14) {
                for (int l = 0;l < 6;l++) {
                    log_list[i].name[l] = ptr[l];
                }
                ptr = strtok(NULL, ",'");
                j++;
                continue;
            }
            x = atof(ptr);
            data[i][j] = x;
            ptr = strtok(NULL, ",'");
            j++;
        }
    }
    fclose(fp);
}

void eval_gen(const double* gen_list) {
    for (int i = 0; i < LOG_SIZE; i++) {
        log_list[i].isReasonable = 1;
        double b = gen_list[13];
        int std = (int)gen_list[14];
        int cnt = 0;
        for (int j = 0; j < 13; j++) {
            if (gen_list[j] + b > data[i][j] ) {
                log_list[i].isReasonable = 2;
            }
            else if (gen_list[j] > data[i][j]) {
                log_list[i].isReasonable = 0;
                ++cnt;
            }
        }
        if (log_list[i].isReasonable != 1) {
            if (cnt > std) log_list[i].isReasonable = 0;
            else log_list[i].isReasonable = 2;
        }
    }
}

double calcProfitPercent()
{
    int i = 0;
    double profitPercentSum = 0.0;
    int numCompany = 0;
    char * name = log_list[0].name;
    int sellPrice=0, buyPrice=0, numBuy=0;
    for (int i = 0; i < LOG_SIZE; ++i)
    {
        if (strcmp(name, log_list[i].name) != 0) {
            if (buyPrice != 0) {
                numCompany += 1;
                if (sellPrice == 0) {
                    sellPrice = log_list[i - 1].stockPrice * numBuy;
                }
                profitPercentSum += double(sellPrice - buyPrice) / double(buyPrice) * 100.0;
            }
            name = log_list[i].name;
            sellPrice = buyPrice = numBuy = 0;
        }
        if (log_list[i].isReasonable == 1) {
            numBuy += 1;
            buyPrice += log_list[i].stockPrice;
        }
        else if (log_list[i].isReasonable == 0) {
            sellPrice += log_list[i].stockPrice * numBuy;
            if (numBuy!= 0 && sellPrice == 0) return float(i);
            numBuy = 0;
        }
    }
    if (numCompany < 50) return 0.0;
    return profitPercentSum / numCompany;
}

int check_log(const double* gen_list) {
    int numBuy = 0;
    for (int i = 0; i < LOG_SIZE; ++i) {
        if (log_list[i].isReasonable == 1) ++numBuy;
    }
    return numBuy;
}

int check_read() {
    int stockPrice = log_list[0].stockPrice;
    for (int i = 0; i < LOG_SIZE; ++i) {
        if (stockPrice != log_list[i].stockPrice) return stockPrice;
    }
}