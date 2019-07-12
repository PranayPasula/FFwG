from distutils.core import setup, Extension, DEBUG
import numpy as np

sfc_module = Extension('fourier_extension',
                       sources = ['dft_simple.cpp','ditfft2.cpp','module.cpp'],
                       include_dirs=[np.get_include()],
                       extra_compile_args=['-O2']
                       )

setup(name = 'fourier_extension', version = '1.0',
    description = 'Python Package with DFT and FFT C++ extension',
    ext_modules = [sfc_module]
    )