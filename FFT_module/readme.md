This module provides C++ implementations of the 2D Discrete Fourier Transform and a 2D Fast Fourier Transform.
Expected input is a square NumPy array, where size N is a power of 2 (e.g., 64x64) and an empty complex128 array
of equal size to hold the output.

Available functions are complex_dft() and complex_fft()

NumPy and Python 3 are required.

To build the module, run "Python setup.py install" to build module for your system and install it in the current
Python environment.

A prebuild x64 module for Windows is included.