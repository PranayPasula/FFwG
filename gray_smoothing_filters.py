# For this part of the assignment, You can use inbuilt functions to compute the fourier transform
# You are welcome to use fft that are available in numpy and opencv
import math
import numpy as np
import cv2


class Filtering:
    image = None
    filter = None
    cutoff = None
    order = None

    def __init__(self, image, filter_name, cutoff, order=0):
        """initializes the variables frequency filtering on an input image
        takes as input:
        image: the input image
        filter_name: the name of the mask to use
        cutoff: the cutoff frequency of the filter
        order: the order of the filter (only for butterworth
        returns"""
        self.image = image
        if filter_name == 'ideal_l':
            self.filter = self.get_ideal_low_pass_filter
        elif filter_name == 'butterworth_l':
            self.filter = self.get_butterworth_low_pass_filter
        elif filter_name == 'gaussian_l':
            self.filter = self.get_gaussian_low_pass_filter

        self.cutoff = cutoff
        self.order = order

    def get_ideal_low_pass_filter(self, shape, cutoff):
        """Computes a Ideal low pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the ideal filter
        returns a ideal low pass mask"""
        h, w = shape
        mask = np.zeros((h, w), dtype=np.int8)
        for y in range(h):
            for x in range(w):
                dist = (((y - h * 0.5) ** 2) + ((x - w * 0.5) ** 2)) ** 0.5
                mask[y, x] = int(dist <= cutoff)
        return mask

    def get_butterworth_low_pass_filter(self, shape, cutoff, order):
        """Computes a butterworth low pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the butterworth filter
        order: the order of the butterworth filter
        returns a butterworth low pass mask"""
        h, w = shape
        n = order * 2
        mask = np.zeros((h, w))
        for y in range(h):
            for x in range(w):
                dist = (((y - h * 0.5) ** 2) + ((x - w * 0.5) ** 2)) ** 0.5
                mask[y, x] = 1 / (1 + ((dist / cutoff) ** n))
        return mask

    def get_gaussian_low_pass_filter(self, shape, cutoff):
        """Computes a gaussian low pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the gaussian filter (sigma)
        returns a gaussian low pass mask"""
        # TA said that I am missing a negative on the gaussian low pass
        h, w = shape
        mask = np.zeros((h, w))
        for y in range(h):
            for x in range(w):
                dist = (((y - h * 0.5) ** 2) + ((x - w * 0.5) ** 2)) ** 0.5
                mask[y, x] = (math.exp(-dist ** 2 / (2 * (cutoff ** 2))))
        return mask


    def post_process_image(self, image):
        """Post process the image to create a full contrast stretch of the image
        takes as input:
        image: the image obtained from the inverse fourier transform
        return an image with full contrast stretch
        -----------------------------------------------------
        1. Full contrast stretch (fsimage)
        2. take negative (255 - fsimage)
        """

        h, w = image.shape
        new_image = np.zeros((h, w))

        lo = np.min(image)
        hi = np.max(image)
        p = (255 - 1) / (hi - lo)

        for y in range(h):
            for x in range(w):
                new_image[y, x] = p * (image[y, x] - lo)

        return new_image

    def filtering(self):
        """Performs frequency filtering on an input image
        returns a filtered image, magnitude of DFT, magnitude of filtered DFT
        ----------------------------------------------------------
        You are allowed to used inbuilt functions to compute fft
        There are packages available in numpy as well as in opencv
        Steps:
        1. Compute the fft of the image
        2. shift the fft to center the low frequencies
        3. get the mask (write your code in functions provided above) the functions can be called by self.filter(shape, cutoff, order)
        4. filter the image frequency based on the mask (Convolution theorem)
        5. compute the inverse shift
        6. compute the inverse fourier transform
        7. compute the magnitude
        8. You will need to do a full contrast stretch on the magnitude and depending on the algorithm you may also need to
        take negative of the image to be able to view it (use post_process_image to write this code)
        Note: You do not have to do zero padding as discussed in class, the inbuilt functions takes care of that
        filtered image, magnitude of DFT, magnitude of filtered DFT: Make sure all images being returned have grey scale full contrast stretch and dtype=uint8
        """

        # Compute the fft of the image
        fft = np.fft.fft2(self.image)

        # shift the fft to center the low frequencies
        fft_shift = np.fft.fftshift(fft)
        magnitude_dft = np.abs(fft_shift)
        magnitude_dft[magnitude_dft == 0] = 1
        magnitude_dft = np.log(magnitude_dft).astype('uint8')
        magnitude_dft = self.post_process_image(magnitude_dft)

        # get the mask (write your code in functions provided above) the functions can be called by self.filter(shape, cutoff, order)
        if self.order != 0:
            mask = self.filter(self.image.shape, self.cutoff, self.order)
        else:
            mask = self.filter(self.image.shape, self.cutoff)
        mask = np.round(mask)

        # filter the image frequency based on the mask (Convolution theorem)
        product = mask * fft_shift
        magnitude_idft = np.abs(product)
        magnitude_idft[magnitude_idft == 0] = 1
        magnitude_idft = np.log(magnitude_idft).astype('uint8')
        magnitude_idft = self.post_process_image(magnitude_idft)

        # compute the inverse shift
        new_image = np.fft.ifftshift(product)

        # compute the inverse fourier transform
        ifft = np.fft.ifft2(new_image)

        # compute the magnitude
        magnitude_ifft = np.abs(ifft)

        # You will need to do a full contrast stretch on the magnitude
        new_image = self.post_process_image(magnitude_ifft)
        return new_image
