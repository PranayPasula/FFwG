import cv2 as cv
import numpy as np

class Sharpen:

    @staticmethod
    def post_process_image(image):
        """Post process the image to create a full contrast stretch of the image
        takes as input:
        image: the image obtained from the inverse fourier transform
        return an image with full contrast stretch
        -----------------------------------------------------
        Full contrast stretch (fsimage)
        """
        a = np.min(image)
        b = np.max(image)

        size = np.shape(image)
        m = np.zeros(size, np.uint8)

        m = np.uint8((255 / (b - a)) * (image - a)+0.5)

        #for x in range(size[0]):
        #    for y in range(size[1]):
        #        mask[x, y] = np.uint8((255 / (b - a)) * (image[x, y] - a)+0.5)

        n = np.ones(size, np.uint8) * 255 - m  # this is for computing the negative but I don't know why
        return m

    @staticmethod
    def homomorphic_mask(size, gamaH, gamaL, d0, c):
        m = np.ones(size)

        for u in range(size[0]):
            for v in range(size[1]):
                d = np.sqrt((u-size[0]/2)**2 + (v-size[1]/2)**2)
                m[u, v] = (gamaH - gamaL)*(1-np.exp(-c*(d**2 / d0**2)))+gamaL

        return m

    @staticmethod
    def laplacian_mask(size,c):
        m = np.ones(size)
        #print('mid x', size[0]/2, 'mid y', size[1]/2)
        alpha = np.sqrt(size[0]**2 + size[1]**2)
        #alpha = 1
        for u in range(size[0]):
            for v in range(size[1]):
                d = np.sqrt((u-(size[0]/2))**2 + (v-(size[1]/2))**2)/alpha
                m[u, v] = 1+c*4*(np.pi*d)**2
                #print('x', u, 'y', v, 'd', d, 'm', m[u, v])
        return mask

    @staticmethod
    def homomorphic(image, gamaL, gamaH, d0, c):
        """performs a homomorphic transformation on a gray level image. takes as input the image, gamaL and gamaH. where
        gamaH is for high freq. i.e. shadows or reflectance. And gamaL is for low freq. i.e. light areas/illumination
        normally gamaL < 1 and gamaH > 1
        d0 is cutoff and c is sharpness of the slope of filter function"""

        size = np.shape(image)
        s_image = image + 1.0
        logimg = np.log(s_image)  # taking log of the original image to separate illumination and reflectance

        fimg = np.fft.fft2(logimg)  # taking Fourier transform of the image
        cfimg = np.fft.fftshift(fimg)  # shifting the low frequencies to the center
        image_fft = np.log(np.abs(cfimg))  # computing and displaying fourier transform's log plot.

        m = Sharpen.homomorphic_mask(size, gamaH, gamaL, d0, c)  # computing the filter mask

        cfimg = cfimg*m
        #for u in range(size[0]):  # applying filter mask to centered fouier transform
        #    for v in range(size[1]):
        #        cfimg[u, v] = cfimg[u, v]*m[u, v]

        icfs = np.fft.ifftshift(cfimg)  # removing center-shift in masked fft.
        image_filtered = np.abs(np.fft.ifft2(icfs))  # taking inverse Fourier transform
        image_final = np.exp(image_filtered) # exponentiating the filtered image to get the final image

        image_final = Sharpen.post_process_image(image_final)  # going back to spatial domain
        stacked_img = np.hstack((Sharpen.post_process_image(image), image_final))

        return image_final, cfimg


    @staticmethod
    def laplacian(image, c):
        size = np.shape(image)

        fimg = np.fft.fft2(image)  # taking Fourier transform of the image
        cfimg = np.fft.fftshift(fimg)  # shifting the low frequencies to the center

        m = Sharpen.laplacian_mask(size, c)

        cfimg = cfimg * m
        #for u in range(size[0]):  # applying filter mask to centered fouier transform
        #    for v in range(size[1]):
        #        cfimg[u, v] = cfimg[u, v] * m[u, v]

        icfs = np.fft.ifftshift(cfimg)  # removing center-shift in masked fft.
        image_filtered = np.abs(np.fft.ifft2(icfs))  # taking inverse Fourier transform
        image_final = Sharpen.post_process_image(image_filtered)  # going back to spatial domain
        stacked_img = np.hstack((Sharpen.post_process_image(image), image_final))
        return image_final, stacked_img
