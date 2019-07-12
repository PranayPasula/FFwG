#pragma once
#include <complex>

#define PI 3.14159265358979323846264338327950288419716939937510

extern void dft_simple(int size_N, float* dptr, std::complex<float>* fft_ptr);
extern void ditfft2_recursive(int size_N, double* dptr, std::complex<double>* fft_ptr);
extern void ditfft2(int size_N, std::complex<double>* dptr, std::complex<double>* fft_ptr, int stride);
