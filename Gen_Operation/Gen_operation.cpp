
#include "pch.h" // use stdafx.h in Visual Studio 2017 and earlier
#include <utility>
#include <limits.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "Gen_Operation.h"
#pragma warning (disable:4996)

typedef struct logInfo {
    char name[6];
    int stockPrice;
    int isReasonable;
} log_info;

// DLL internal state variables:
static log_info log_list[496163];
static double data[496163][13];

void init_data() {
    FILE* fp;
    fp = fopen("data_for_GA.csv", "r");
    for (int i = 0;i < 496163; i++) {
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
    for (int i = 0; i < 496163; i++) {
        log_list[i].isReasonable = 1;
        for (int j = 0; j < 13; j++) {
            if (gen_list[j] < data[i][j]) {
                log_list[i].isReasonable = 0;
            }
        }
    }
}

double calcProfitPercent()
{
    int i = 0;
    double profitPercentSum = 0.0;
    int numCompany = 1;
    char * name = log_list[0].name;

    int sellPrice=0, buyPrice=0, numBuy=0;
    for (int i = 0; i < 496163; ++i)
    {
        if (strcmp(name, log_list[i].name) != 0) {
            numCompany += 1;
            if (buyPrice != 0) {
                if (sellPrice == 0) {
                    sellPrice = log_list[i - 1].stockPrice * numBuy;
                }
                profitPercentSum += (double)sellPrice / (double)buyPrice;
            }
            sellPrice = buyPrice = numBuy = 0;
        }
        if (log_list[i].isReasonable == 1) {
            numBuy += 1;
            buyPrice += log_list[i].stockPrice;
        }
        else if (log_list[i].isReasonable == 0) {
            sellPrice += log_list[i].stockPrice * numBuy;
            numBuy = 0;
        }
    }
    return profitPercentSum / numCompany;
}
