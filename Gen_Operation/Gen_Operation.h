#pragma once
// Gen_Operation.h - Contains genetic evaluate operation
#pragma once

#ifdef GENOPERATION_EXPORTS
#define GENOPERATION_API __declspec(dllexport)
#else
#define GENOPERATION_API __declspec(dllimport)
#endif


extern "C" GENOPERATION_API void init_data();
extern "C" GENOPERATION_API void eval_gen(const double* gen_list);
extern "C" GENOPERATION_API double calcProfitPercent();