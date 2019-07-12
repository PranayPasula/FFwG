#define NO_IMPORT_ARRAY
#define PY_ARRAY_UNIQUE_SYMBOL FOURIER_ARRAY_API
#include "fourier.h"

void dft_simple(int size_N, float* dptr, std::complex<float>* fft_ptr)
{
	float W = 2 * PI / size_N;

	int arr_size = size_N * size_N;

	float* cos_arr = new float[arr_size];
	float* sin_arr = new float[arr_size];

	int offset_dst = 0;

	for (int u = 0; u < size_N; u++)
	{
		for (int v = 0; v < size_N; v++)
		{

			std::complex<float> mycomplex(0, 0);

			int offset = 0;
			for (int i = 0; i < size_N; i++) {
				int ui = u * i;

				for (int j = 0; j < size_N; j++) {
					float phase = (i * u + v * j) * W;
					std::complex<float> local(cosf(phase), -sinf(phase));
					mycomplex += dptr[offset] * local;
					offset++;
				}
			}

			fft_ptr[offset_dst] = mycomplex;
			offset_dst++;
		}
	}
}

void ditfft2_simple(int size_N, double* dptr, std::complex<double>* fft_ptr, int stride)
{
	int arr_size = size_N * size_N;
	std::complex<double> W(0, -2 * PI / size_N);
	std::complex<double> W2(0, -4 * PI / size_N);

	std::complex<double> * twiddle_01 = new std::complex<double>[size_N];
	std::complex<double> * twiddle_11 = new std::complex<double>[arr_size / 2];

	for (int v = 0; v < size_N; v++)
	{
		twiddle_01[v] = std::exp((double)v * W);
	}

	for (int u = 0; u < arr_size / 2; u++) {
		twiddle_11[u] = std::exp((double)(u)* W);
	}

	int offset_dst = 0;

	for (int u = 0; u < size_N; u++)
	{
		std::complex<double> twiddle_10 = std::exp((double)u * W);

		for (int v = 0; v < size_N; v++)
		{

			std::complex<double> sum00(0, 0);
			std::complex<double> sum01(0, 0);
			std::complex<double> sum10(0, 0);
			std::complex<double> sum11(0, 0);

			int uivj = 0;
			int offset00 = 0;

			for (int i = 0; i < size_N / (2 * stride); i++) {
				for (int j = 0; j < size_N / (2 * stride); j++) {

					int offset01 = offset00 + stride;
					int offset10 = offset00 + size_N * stride;
					int offset11 = offset10 + stride;

					std::complex<double> local = std::exp((double)(uivj)* W2);
					sum00 += dptr[offset00] * local;
					sum01 += dptr[offset01] * local;
					sum10 += dptr[offset10] * local;
					sum11 += dptr[offset11] * local;
					uivj += v * stride;
					offset00 += 2 * stride;
				}
				offset00 += size_N * stride;
				uivj += u * stride;
			}

			fft_ptr[offset_dst] = sum00 + twiddle_01[v] * sum01 + twiddle_10 * sum10 + twiddle_11[u + v] * sum11;
			offset_dst++;
		}
	}
}
