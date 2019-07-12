import numpy as np
import main

class FilteringColor:

    @staticmethod
    def get_ideal_low_pass_filter(shape, cutoff, order):
        """Computes a Ideal low pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the ideal filter
        returns a ideal low pass mask"""

        filter = np.zeros(shape, np.float32)

        width, height = shape[:2]

        for x in range(-int(cutoff),int(cutoff)):
            x_pos = int(x + width/2 - 1)
            y_range = cutoff*np.sin(np.arccos(x/cutoff))
            for y in range(-int(y_range), int(y_range)):
                y_pos = int(y + height/2 - 1)
                filter[x_pos, y_pos] = 1.0;

        return filter

    @staticmethod
    def get_ideal_high_pass_filter(shape, cutoff, order):
        """Computes a Ideal high pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the ideal filter
        returns a ideal high pass mask"""

        filter = np.ones(shape, np.float32)
        filter = filter - FilteringColor.get_ideal_low_pass_filter(shape, cutoff, order)
        
        return filter

    @staticmethod
    def get_butterworth_low_pass_filter(shape, cutoff, order):
        """Computes a butterworth low pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the butterworth filter
        order: the order of the butterworth filter
        returns a butterworth low pass mask"""
      
        filter = np.zeros(shape, np.float32)

        width, height = shape[:2]

        for x in range(width):
            for y in range(height):
                filter[x, y] = 1/(1+(np.sqrt((x - width/2)**2+(y - height/2)**2)/cutoff)**(2*order));

        return filter

    @staticmethod
    def get_butterworth_high_pass_filter(shape, cutoff, order):
        """Computes a butterworth high pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the butterworth filter
        order: the order of the butterworth filter
        returns a butterworth high pass mask"""

        #Hint: May be one can use the low pass filter function to get a high pass mask

        filter = np.ones(shape, np.float32)
        filter = filter - FilteringColor.get_butterworth_low_pass_filter(shape, cutoff, order)
        
        return filter

    @staticmethod
    def get_gaussian_low_pass_filter(shape, cutoff, order):
        """Computes a gaussian low pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the gaussian filter (sigma)
        returns a gaussian low pass mask"""

        filter = np.zeros(shape, np.float32)

        width, height = shape[:2]

        for x in range(width):
            for y in range(height):
                filter[x, y] = np.exp(-((x - width/2)**2+(y - height/2)**2)/(2*cutoff**2));

        return filter

    @staticmethod
    def get_gaussian_high_pass_filter(shape, cutoff, order):
        """Computes a gaussian high pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the gaussian filter (sigma)
        returns a gaussian high pass mask"""

        filter = np.ones(shape, np.float32)
        filter = filter - FilteringColor.get_gaussian_low_pass_filter(shape, cutoff, order)
        
        return filter


    @staticmethod
    def post_process_image(image):
        """Post process the image to create a full contrast stretch of the image
        takes as input:
        image: the image obtained from the inverse fourier transform
        return an image with full contrast stretch
        -----------------------------------------------------
        1. Full contrast stretch (fsimage)
        2. take negative (255 - fsimage)
        """

        output = np.log(1 + np.abs(image))

        min = output.min()
        max = output.max()

        P = 255/(max - min)
        L = -(P*min)

        output = output*P + L

        return np.uint8(output)

    @staticmethod
    def GetMask(image, lowPassParams, highPassParams, isBandPass):
        """Get the combined mask for high pass/lowpass/bandpass/band reject"""
        shape = np.shape(image)

        lowPassFilter = None
        highPassFilter = None

        if lowPassParams != None:
            filter_name = lowPassParams[0]
            if filter_name == 'ideal_l':
                lowPassFilter = FilteringColor.get_ideal_low_pass_filter(shape, lowPassParams[1],lowPassParams[2])
            elif filter_name == 'butterworth_l':
                lowPassFilter = FilteringColor.get_butterworth_low_pass_filter(shape, lowPassParams[1],lowPassParams[2])
            elif filter_name == 'gaussian_l':
                lowPassFilter = FilteringColor.get_gaussian_low_pass_filter(shape, lowPassParams[1],lowPassParams[2])

        if highPassParams != None:
            filter_name = highPassParams[0]
            if filter_name == 'ideal_h':
                highPassFilter = FilteringColor.get_ideal_high_pass_filter(shape, highPassParams[1],highPassParams[2])
            elif filter_name == 'butterworth_h':
                highPassFilter = FilteringColor.get_butterworth_high_pass_filter(shape, highPassParams[1],highPassParams[2])
            elif filter_name == 'gaussian_h':
                highPassFilter = FilteringColor.get_gaussian_high_pass_filter(shape, highPassParams[1],highPassParams[2])
       
        if lowPassParams != None and highPassParams != None:
            mask = lowPassFilter + highPassFilter
            if isBandPass:
                mask = 1 - mask
        elif lowPassParams != None and highPassParams == None:
            mask = lowPassFilter
        elif lowPassParams == None and highPassParams != None:
            mask = highPassFilter
        else:
            mask = np.ones(shape, np.uint8)
        return mask

    @staticmethod
    def ApplyFiltering(image, mask):
        """Performs frequency filtering on an input image
        returns a filtered image, magnitude of DFT, magnitude of filtered DFT        
        """
        dft = main.fourier_transform(image)
        #dft = np.fft.fft2(image)

        shifted_dft = np.fft.fftshift(dft)

        filtered_dft = shifted_dft * mask
        #shifted_ift = np.fft.ifft2(filtered_dft)
        #shifted_ift = np.fft.ifft2(filtered_dft)

        #filtered_image = np.abs(shifted_ift)
        filtered_image = main.inverse_fourier_transform(filtered_dft)

        return FilteringColor.post_process_image(filtered_image), FilteringColor.post_process_image(np.abs(shifted_dft)), FilteringColor.post_process_image(filtered_dft)
