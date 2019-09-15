#ifndef VCLIB
#define VCLIB

#ifdef VCLIB_COMPILE
#define VCLIB_IMEXPORT __declspec(dllexport)
#else
#define VCLIB_IMEXPORT __declspec(dllimport)
#endif

//extern "C" {
//VCLIB_IMEXPORT void func (int a, int b=0);
//VCLIB_IMEXPORT void func (int a, int b, int c);
	VCLIB_IMEXPORT void afunc3 (int a, int b, int c=0);
	VCLIB_IMEXPORT void func (int a, int b);
//}
#endif