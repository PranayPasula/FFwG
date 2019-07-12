# This is for RGB high-pass filtering and unsharp masking/high-boost filtering.
# The filters are (1) ideal, (2) Butterworth, and (3) Gaussian high-pass.
# Unsharp masking/highboost filtering uses the Gaussian high-pass.
#
#   Usage:  Read code and comments in main(). Parameter names added to function
#           calls for clarity.
#
#   Input:  1. 3-channel color image, cutoff frequency
#           2. Image filename
#           3. Filter type/method
#           4. Filter order (for Butterworth) or high-boost coefficient
#              (for unsharp masking)
#
#   Output: 3-channel filtered color image


import numpy as np
import math
import cv2
from numpy import ma


class HighpassFiltering:

  shape = None
  bgr_split_img = None
  cutoff = None
  filter_name = None
  order = None
  filter = None

  # Assigns class variables based on input image and filter arguments.
  # Converts color image in 3-dim (B,G,R) numpy array format to 3-dim
  # numpy array in which axis 0 is separated by B,G,R channels.
  def __init__(self, img, cutoff, filter_name, order=None):
    self.shape = (len(img), len(img[0]))
    self.bgr_split_img = self.split_bgr(img)
    self.cutoff = cutoff
    self.filter_name = filter_name
    self.order = order
    filters = {
      'ideal_h':    self.ideal_h,
      'butter_h':   self.butter_h,
      'gaussian_h': self.gaussian_h,
      'unsharp_m':  self.unsharp_mask
    }
    self.filter = filters[filter_name]

  # Separates BGR channels and returns 3-d array with axis 0 split on channel
  def split_bgr(self, img):
    return np.array([img[:,:,0], img[:,:,1], img[:,:,2]])

  # Restores split BGR channel DFT into desired color image
  def merge_bgr(self, channel_stk):
    return np.dstack((channel_stk[0], channel_stk[1], channel_stk[2]))

  # Ideal high-pass filter
  def ideal_h(self, shape, cutoff):
    mask = np.zeros(shape, dtype=np.uint8)
    mask_rows = shape[0]
    mask_cols = shape[1]
    center_row = math.floor(mask_rows / 2)
    center_col = math.floor(mask_cols / 2)

    for row in range(mask_rows):
      for col in range(mask_cols):
        distance = ((row - center_row) ** 2 + (col - center_col) ** 2) ** (1 / 2)
        if distance >= cutoff:
          mask[row][col] = 1

    return mask

  # Ideal Butterworth high-pass filter
  def butter_h(self, shape, cutoff, order):
    mask = np.zeros(shape, dtype=np.float64)
    mask_rows = shape[0]
    mask_cols = shape[1]
    center_row = math.floor(mask_rows / 2)
    center_col = math.floor(mask_cols / 2)

    for row in range(mask_rows):
      for col in range(mask_cols):
        distance = ((row - center_row) ** 2 + (col - center_col) ** 2) ** (1 / 2)
        mask[row][col] = 1 - (1 / (1 + (distance / cutoff) ** (2 * order)))

    return mask

  # Ideal Gaussian high-pass filter
  def gaussian_h(self, shape, cutoff):
    mask = np.zeros(shape, dtype=np.float64)
    mask_rows = shape[0]
    mask_cols = shape[1]
    center_row = math.floor(mask_rows / 2)
    center_col = math.floor(mask_cols / 2)

    for row in range(mask_rows):
      for col in range(mask_cols):
        distance = ((row - center_row) ** 2 + (col - center_col) ** 2) ** (1 / 2)
        mask[row][col] = 1 - math.exp(-(distance ** 2) / (2 * (cutoff ** 2)))

    return mask

  # Creates mask for unsharp masking. Accessed through 'unsharp_m' argument when
  # calling filtering(). The argument 'order' equals the high-boost coefficient.
  # Uses Gaussian high-pass filtering.
  def unsharp_mask(self):
    highboost_coeff = self.order
    mask = (1 + highboost_coeff * self.gaussian_h(self.shape, self.cutoff))
    return mask

  # Apply full-contrast stretch
  def post_process_image(self, image):
    min = np.min(image)
    max = np.max(image)
    lower_limit = 0
    upper_limit = 255
    image = (image - min) * ((upper_limit - lower_limit) / (max - min)) + lower_limit
    image = np.floor(image + 0.5)

    return image

  # Creates a filtered color image from the input color image and arguments
  #   Input:  Color image as 3-dim (B,G,R) numpy array
  #   Output: Filtered image as 3-dim (B,G,R) numpy array
  def filtering(self):
    # Find DFT for each channel
    dft = np.fft.fftn(self.bgr_split_img, axes=(1,2))

    # Shift DFT to center 0-freq for each channel
    shift_dft = np.fft.fftshift(dft, axes=(1,2))

    # Create mask that will be applied to DFT
    if (self.filter_name != 'unsharp_m'):
      if (self.filter_name == 'butter_h'):
        mask_single = self.filter(self.shape, self.cutoff, self.order)
      else:
        mask_single = self.filter(self.shape, self.cutoff)
      mask_triple = np.array([mask_single, mask_single, mask_single])

      # Apply mask to DFT
      shift_filt_dft = shift_dft * mask_triple

    # Create unsharp mask and apply to DFT
    else:
      shift_filt_dft = shift_dft * self.unsharp_mask()

    # Reverse shift filtered DFT
    filt_dft = np.fft.ifftshift(shift_filt_dft, axes=(1,2))

    # Perform inverse Fourier transform on each channel's DFT
    idft = np.fft.ifftn(filt_dft, axes=(1,2))
    idft_mag = np.abs(idft)

    # Apply full constrast stretch to each channel of filtered image
    stretch_idft_mag = np.array([self.post_process_image(idft_mag[0]),
                                 self.post_process_image(idft_mag[1]),
                                 self.post_process_image(idft_mag[2])])

    # Manipulate array axes to get final filtered image
    final_filt_img = self.merge_bgr(stretch_idft_mag.real.astype(np.uint8))
    return final_filt_img


def main():
  # Change string argument below to name of image (3-channel) you want to filter
  img = cv2.imread('lena_big.png', 1)

  # # Change arguments in line below to control filtering
  # obj = HighpassFiltering(img=img, cutoff=20, filter_name='gaussian_h')  # For high-pass filtering

  # Change arguments in line below to control cutoff frequency and strength of
  # unsharp masking/high-boost filtering
  obj = HighpassFiltering(img=img, cutoff=100, filter_name='unsharp_m', order=2)  # For unsharp masking
  cv2.imshow('filtered img', obj.filtering())
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  cv2.imwrite('lena_big_unsharp_100_2_rgb.png', obj.filtering())

  # Greyscale test
  img_grey = cv2.imread("lena_big.png", 0)
  img_grey_prep = np.broadcast_to(np.atleast_3d(img_grey), (img_grey.shape[0], img_grey.shape[1], 3))
  obj_grey = HighpassFiltering(img=img_grey_prep, cutoff=100, filter_name='unsharp_m', order=2)
  img_grey_final = obj_grey.filtering()[:,:,0]
  cv2.imshow('grey filtered img', img_grey_final)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  cv2.imwrite('lena_big_unsharp_100_2_grey.png', img_grey_final)


if __name__ == '__main__':
  main()