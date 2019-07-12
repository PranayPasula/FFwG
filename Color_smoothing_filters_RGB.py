import numpy as np
import math
import cv2


class LowpassFiltering:
    shape = None
    bgr_split_img = None
    cutoff = None
    filter_name = None
    order = None

    # Assigns class variables based on input image and filter arguments.
    # Converts color image in 3-dim (B,G,R) numpy array format to 3-dim
    # # numpy array in which axis 0 is separated by B,G,R channels.
    def __init__(self, img, cutoff, filter_name, order=None):
        self.shape = (len(img), len(img[0]))
        self.bgr_split_img = self.split_bgr(img)
        self.cutoff = cutoff
        self.filter_name = filter_name
        self.order = order
        filters = {
            'ideal_l': self.ideal_l,
            'butter_l': self.butter_l,
            'gaussian_l': self.gaussian_l,

        }
        self.filter = filters[filter_name]

        # Separates BGR channels and returns 3-d array with axis 0 split on channel

    def split_bgr(self, img):
        return np.array([img[:, :, 0], img[:, :, 1], img[:, :, 2]])

        # Restores split BGR channel DFT into desired color image

    def merge_bgr(self, channel_stk):
        return np.dstack((channel_stk[0], channel_stk[1], channel_stk[2]))

        # Ideal low-pass filter

    def ideal_l(self, shape, cutoff, order):
        mask = np.zeros(shape, dtype=np.uint8)
        mask_rows = shape[0]
        mask_cols = shape[1]
        center_row = math.floor(mask_rows / 2)
        center_col = math.floor(mask_cols / 2)
        for row in range(mask_rows):
            for col in range(mask_cols):
                distance = ((row - center_row) ** 2 + (col - center_col) ** 2) ** (1 / 2)
                mask[row][col] = int(distance <= cutoff)
        return mask

        # Butterworth low-pass filter

    def butter_l(self, shape, cutoff, order):
        mask = np.zeros(shape, dtype=np.float64)
        mask_rows = shape[0]
        mask_cols = shape[1]
        center_row = math.floor(mask_rows / 2)
        center_col = math.floor(mask_cols / 2)
        n = order * 2
        for row in range(mask_rows):
            for col in range(mask_cols):
                distance = ((row - center_row) ** 2 + (col - center_col) ** 2) ** (1 / 2)
                mask[row][col] = 1 / (1 + ((distance / cutoff) ** n))

        return mask

        # Gaussian low-pass filter
    def gaussian_l(self, shape, cutoff, order):
        mask = np.zeros(shape, dtype=np.float64)
        mask_rows = shape[0]
        mask_cols = shape[1]
        center_row = math.floor(mask_rows / 2)
        center_col = math.floor(mask_cols / 2)

        for row in range(mask_rows):
            for col in range(mask_cols):
                distance = ((row - center_row) ** 2 + (col - center_col) ** 2) ** (1 / 2)
                mask[row][col] =  (math.exp(-(distance ** 2) / (2 * (cutoff ** 2))))

        return mask

        # post process the image to create a full contrast stretch of the image as
        # input
    def post_process_image(self, image):
        min = np.min(image)
        max = np.max(image)
        lower_limit = 0
        upper_limit = 255
        image = (image - min) * ((upper_limit - lower_limit) / (max - min)) + lower_limit
        image = np.floor(image + 0.5)

        return image

        # Creates a filtered color image from the input color image and arguments
        #   Input: Color image as 3-dim (B,G,R) numpy array
        #   Output: Filtered image as 3-dim (B,G,R) numpy array
    def filtering(self):
        # Find DFT for each channel
        dft = np.fft.fftn(self.bgr_split_img, axes=(1, 2))

        # Shift DFT to center 0-freq for each channel
        shift_dft = np.fft.fftshift(dft, axes=(1, 2))

        # Create mask that will be applied to DFT
        if self.order != 0:
            mask_single = self.filter(self.shape, self.cutoff, self.order)
        else:
            mask_single = self.filter(self.shape, self.cutoff)
        mask_triple = np.array([mask_single, mask_single, mask_single])
        # Apply mask to DFT
        shift_filt_dft = shift_dft * mask_triple

        # Reverse shift filtered DFT
        filt_dft = np.fft.ifftshift(shift_filt_dft, axes=(1, 2))

        # Perform inverse Fourier transform on each channel's DFT
        idft = np.fft.ifftn(filt_dft, axes=(1, 2))
        idft_mag = np.abs(idft)

        # Apply full constrast stretch to each channel of filtered image
        stretch_idft_mag = np.array([self.post_process_image(idft_mag[0]),
                                     self.post_process_image(idft_mag[1]),
                                     self.post_process_image(idft_mag[2])])

        # Manipulate array axes to get final filtered image
        final_filt_img = self.merge_bgr(stretch_idft_mag.real.astype(np.uint8))
        return final_filt_img


def main():
    # Change string argument below to name of image (3-channel) you want to
    # filter
    img = cv2.imread('lena_big.png', 1)

    # # Change arguments in line below to control filtering
    # obj = HighpassFiltering(img=img, cutoff=20, filter_name='gaussian_h') #
    # For high-pass filtering

    # Change arguments in line below to control cutoff frequency and strength of
    # unsharp masking/high-boost filtering
    obj = LowpassFiltering(img=img, cutoff=20, filter_name='ideal_l', order=2)  # For ideal low pass
    cv2.imshow('filtered img', obj.filtering())
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('lena_big_unsharp_20_2.png', obj.filtering())


if __name__ == '__main__':
    main()
