import numpy as np
#import cv2 as cv

class Sharpen:

    def post_process_image(self, image):
        """Post process the image to create a full contrast stretch of the image
        takes as input:
        image: the image obtained from the inverse fourier transform
        return an image with full contrast stretch

        Post processing is different for homomorphic and lapacian transforms. therefore the variable L tells
        which one to use ( L=0 -> homomorphic and L=1 -> Laplacian).
        -----------------------------------------------------
        Full contrast stretch (fsimage)
        """

        a = np.min(image)
        b = np.max(image)
        m = np.uint8((255 / (b - a)) * (image - a)+0.5)

        return m

    def homomorphic_mask(self, size, gamaH, gamaL, d0, c):
        m = np.ones(size)

        for u in range(size[0]):
            for v in range(size[1]):
                d = np.sqrt((u-size[0]/2)**2 + (v-size[1]/2)**2)
                m[u, v] = (gamaH - gamaL)*(1-np.exp(-c*(d**2 / d0**2)))+gamaL

        return m

    def laplacian_mask(self, size, c):
        m = np.ones(size)
        alpha = np.sqrt(size[0]**2 + size[1]**2)
        for u in range(size[0]):
            for v in range(size[1]):
                d = np.sqrt((u-(size[0]/2))**2 + (v-(size[1]/2))**2)/alpha
                m[u, v] = 1+c*4*(np.pi*d)**2
        return m


    def homomorphic(self, image, gamaL, gamaH, d0, c):
        """performs a homomorphic transformation on a gray level image. takes as input the image, gamaL and gamaH. where
        gamaH is for high freq. i.e. shadows or reflectance. And gamaL is for low freq. i.e. light areas/illumination
        normally gamaL < 1 and gamaH > 1
        d0 is cutoff and c is sharpness of the slope of filter function"""

        size = np.shape(image)
        s_image = image + 1.0
        logimg = np.log(s_image)  # taking log of the original image to separate illumination and reflectance

        fimg = np.fft.fft2(logimg)  # taking Fourier transform of the image
        cfimg = np.fft.fftshift(fimg)  # shifting the low frequencies to the center
        m = self.homomorphic_mask(size, gamaH, gamaL, d0, c)  # computing the filter mask
        cfimg = cfimg*m
        icfs = np.fft.ifftshift(cfimg)  # removing center-shift in masked fft.
        image_filtered = np.abs(np.fft.ifft2(icfs))  # taking inverse Fourier transform
        image_final = np.exp(image_filtered) # exponentiating the filtered image to get the final image
        image_final = self.post_process_image(image_final)  # going back to spatial domain
        #cv.imshow('final image', image_final)
        #cv.waitKey(0)
        return image_final


    def laplacian(self, image, c):
        size = np.shape(image)

        fimg = np.fft.fft2(image)  # taking Fourier transform of the image
        cfimg = np.fft.fftshift(fimg)  # shifting the low frequencies to the center

        m = self.laplacian_mask(size, c)

        cfimg = cfimg * m

        icfs = np.fft.ifftshift(cfimg)  # removing center-shift in masked fft.
        image_filtered = np.abs(np.fft.ifft2(icfs))  # taking inverse Fourier transform
        m = self.post_process_image(image_filtered)  # going back to spatial domain

        ##################################
        'this new portion is for balancing the intensity distribution by removing the top super bright pixels'
        'Afterwards full contrast stretch is performed.'

        intensity = 255
        hist = np.zeros(256)  #forming histogram
        size = np.shape(m)
        for k in range(size[1]):
            for j in range(size[0]):
                hist[m[j, k]] = hist[m[j, k]] + 1
        for x in range(255):
            if np.sum(hist[0:x]) >= (0.999 * size[0] * size[1]):
                intensity = x
                break
        for x in range(size[0]):
            for y in range(size[1]):
                if m[x, y] > np.uint8(intensity):
                    m[x, y] = np.uint8(intensity)
        a = np.min(m)
        b = np.max(m)
        image_final = np.uint8((255 / (b - a)) * (m - a) + 0.5)
       # cv.imshow('final image', image_final)
       # cv.waitKey(0)
        return image_final
