#define NO_IMPORT_ARRAY
#define PY_ARRAY_UNIQUE_SYMBOL FOURIER_ARRAY_API
#include "fourier.h"

void ditfft2_recursive(int size_N, double* dptr, std::complex<double>* fft_ptr)
{
	std::complex<double>* complex = new std::complex<double>[size_N*size_N];

	for (int i = 0; i < size_N * size_N; i++) {
		complex[i] = std::complex<double>(dptr[i], 0);
	}

	int stride = 1;

	ditfft2(size_N, complex, fft_ptr, stride);

	delete[] complex;

	return;
}

static std::complex<double> base_W(0, -PI);
static std::complex<double> base_2W(0, -2*PI);
static std::complex<double> twiddle_W = std::exp(base_W);
static std::complex<double> twiddle_2W = std::exp(base_2W);

void ditfft2(int size_N, std::complex<double>* dptr, std::complex<double>* fft_ptr, int stride)
{
	if (size_N == 1)
	{
		fft_ptr[0] = dptr[0];
	}
	else if (size_N == 2)
	{
			fft_ptr[0] = dptr[0] + dptr[1] + dptr[2] + dptr[3];
			fft_ptr[1] = dptr[0] + dptr[2] + twiddle_W * (dptr[1] + dptr[3]);

			fft_ptr[2] = dptr[0] + dptr[1] + twiddle_W * (dptr[2] + dptr[3]);
			fft_ptr[3] = dptr[0] + twiddle_W * (dptr[1] + dptr[2]) + twiddle_2W * dptr[3];
	}
	else
	{
		int arr_size = size_N * size_N;
		int half_arr_size = arr_size / 4;

		std::complex<double> W(0, -2 * PI / size_N);
		std::complex<double> W2(0, -4 * PI / size_N);

		std::complex<double>* dptr00 = new std::complex<double>[half_arr_size];
		std::complex<double>* dptr01 = new std::complex<double>[half_arr_size];
		std::complex<double>* dptr10 = new std::complex<double>[half_arr_size];
		std::complex<double>* dptr11 = new std::complex<double>[half_arr_size];

		{
			int offset00 = 0;
			int offset_dst = 0;
			for (int i = 0; i < size_N / 2; i++) {
				for (int j = 0; j < size_N / 2; j++) {

					int offset01 = offset00 + 1;
					int offset10 = offset00 + size_N;
					int offset11 = offset10 + 1;

					dptr00[offset_dst] = dptr[offset00];
					dptr01[offset_dst] = dptr[offset01];
					dptr10[offset_dst] = dptr[offset10];
					dptr11[offset_dst] = dptr[offset11];

					offset00 += 2;
					offset_dst++;
				}
				offset00 += size_N;
			}
		}

		std::complex<double>* sum00 = new std::complex<double>[half_arr_size];
		std::complex<double>* sum01 = new std::complex<double>[half_arr_size];
		std::complex<double>* sum10 = new std::complex<double>[half_arr_size];
		std::complex<double>* sum11 = new std::complex<double>[half_arr_size];

		ditfft2(size_N / 2, dptr00, sum00, 2 * stride);
		ditfft2(size_N / 2, dptr01, sum01, 2 * stride);
		ditfft2(size_N / 2, dptr10, sum10, 2 * stride);
		ditfft2(size_N / 2, dptr11, sum11, 2 * stride);

		int offset00 = 0;
		int offset_dst00 = 0;
		int offset_dst01 = size_N / 2;
		int offset_dst10 = ((size_N / 2) * size_N);
		int offset_dst11 = ((size_N / 2) * size_N) + (size_N / 2);

		for (int u = 0; u < size_N / 2; u++)
		{
			std::complex<double> twiddle_10 = std::exp((double)u * W);

			for (int v = 0; v < size_N / 2; v++)
			{
				std::complex<double> twiddle_01 = std::exp((double)v * W);
				std::complex<double> twiddle_11 = std::exp((double)(u + v) * W);

				std::complex<double> inter01 = (twiddle_01 * sum01[offset00]);
				std::complex<double> inter10 = (twiddle_10 * sum10[offset00]);
				std::complex<double> inter11 = (twiddle_11 * sum11[offset00]);

				fft_ptr[offset_dst00] = sum00[offset00] + inter01 + inter10 + inter11;
				fft_ptr[offset_dst00+offset_dst01] = sum00[offset00] - inter01 + inter10 - inter11;
				fft_ptr[offset_dst00+offset_dst10] = sum00[offset00] + inter01 - inter10 - inter11;
				fft_ptr[offset_dst00+offset_dst11] = sum00[offset00] - inter01 - inter10 + inter11;

				offset_dst00++;
				offset00++;
			}
			offset_dst00 += size_N/2;
		}

		delete[] dptr00;
		delete[] dptr01;
		delete[] dptr10;
		delete[] dptr11;

		delete[] sum00;
		delete[] sum01;
		delete[] sum10;
		delete[] sum11;
	}
}
