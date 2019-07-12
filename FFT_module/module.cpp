#define PY_ARRAY_UNIQUE_SYMBOL FOURIER_ARRAY_API
#include <Python.h>
#include <numpy/arrayobject.h>
#include "fourier.h"

static PyObject* complex_dft(PyObject* dummy, PyObject* args)
{
	bool success = false;

	PyObject* arg1 = NULL, * out = NULL;
	PyObject* arr1 = NULL, * oarr = NULL;

	if (!PyArg_ParseTuple(args, "OO!", &arg1, &PyArray_Type, &out)) return NULL;

	arr1 = PyArray_FROM_OTF(arg1, NPY_FLOAT, NPY_ARRAY_IN_ARRAY);

	if (arr1 == NULL)
	{
		return NULL;
	}

	oarr = PyArray_FROM_OTF(out, NPY_CFLOAT, NPY_ARRAY_INOUT_ARRAY);
	success = (oarr != NULL);

	if (success)
	{
		int nd = PyArray_NDIM(arr1);
		npy_intp* dims = PyArray_DIMS(arr1);
		float* dptr = (float*)PyArray_DATA(arr1);
		std::complex<float>* fft_ptr = (std::complex<float>*)PyArray_DATA(oarr);

		dft_simple(dims[0], dptr, fft_ptr);

		Py_DECREF(arr1);
		Py_DECREF(oarr);
		Py_INCREF(Py_None);
		return Py_None;
	}
	else
	{
		Py_XDECREF(arr1);
		Py_XDECREF(oarr);
		return NULL;
	}
}

static PyObject* complex_fft128(PyObject* dummy, PyObject* args)
{
	bool success = false;

	PyObject* arg1 = NULL, * out = NULL;
	PyObject* arr1 = NULL, * oarr = NULL;

	if (!PyArg_ParseTuple(args, "OO!", &arg1, &PyArray_Type, &out)) return NULL;

	arr1 = PyArray_FROM_OTF(arg1, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

	if (arr1 == NULL)
	{
		return NULL;
	}

	oarr = PyArray_FROM_OTF(out, NPY_COMPLEX128, NPY_ARRAY_INOUT_ARRAY);
	success = (oarr != NULL);

	if (success)
	{
		int nd = PyArray_NDIM(arr1);
		npy_intp* dims = PyArray_DIMS(arr1);
		double* dptr = (double*)PyArray_DATA(arr1);
		std::complex<double>* fft_ptr = (std::complex<double>*)PyArray_DATA(oarr);

		ditfft2_recursive(dims[0], dptr, fft_ptr);

		Py_DECREF(arr1);
		Py_DECREF(oarr);
		Py_INCREF(Py_None);
		return Py_None;
	}
	else
	{
		Py_XDECREF(arr1);
		Py_XDECREF(oarr);
		return NULL;
	}
}

static PyMethodDef fourier_extension_methods[] = {
	{ "complex_dft", (PyCFunction)complex_dft, METH_VARARGS, NULL },
	{ "complex_fft", (PyCFunction)complex_fft128, METH_VARARGS, NULL },

	{ NULL, NULL, 0, NULL}
};

static PyModuleDef fourier_module = {
	PyModuleDef_HEAD_INIT,
	"fourier_extension",
	"Provides C implemenations of Discrete Fourier Transform and Fast Fourier Transform",
	0,
	fourier_extension_methods
};

PyMODINIT_FUNC PyInit_fourier_extension() {
	PyObject* module = PyModule_Create(&fourier_module);
	import_array();

	return module;
}
