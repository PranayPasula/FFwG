from PIL import Image
import cv2
import sys
# from DFT import DFT
from numpy.random import rand
import numpy as np
from datetime import datetime
import bispy.qfft
import matplotlib.pyplot as plt
from qft import QFTclass
import  threading


def applyFullContrastStretch( image):
    input = np.reshape(image, image.size)
    a = min(input)
    b = max(input)
    BminA = b - a
    Kmin1 = 255
    p = Kmin1 / BminA
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            image[i, j] = p * (image[i, j] - a)
    return image


def convolve( image, mask):
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            image[i, j] = image[i, j] * mask[i, j]
    return image


def display_image(window_name, image):
    """A function to display image"""
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)


def filtermethod(image):
    cutoff = 7

    p = image.shape[0]
    q = image.shape[1]
    for u in range(p):
        for v in range(q):
            distance = np.sqrt(np.square(u - p / 2) + np.square(v - q / 2))
            if distance <= cutoff:
                image[u, v] = 1
            else:
                image[u, v] = 0
    return image

def main():
    matrix = np.array(Image.open('output/car.png').convert('RGB'))
    QFTclass.imagematrix = matrix


    #b, g, r = cv2.split(matrix)

    #b = np.dot(np.quaternion(0, 1, 0, 0), b)
    #g = np.dot(np.quaternion(0, 0, 1, 0), g)
    #r = np.dot(np.quaternion(0, 0, 0, 1), r)
    #matrix = b + g + r

    #fft_matrix = bispy.qfft.Qfft(bispy.qfft.Qfft(matrix))
    QFTclass.QFTmatrix = np.zeros((matrix.shape[0], matrix.shape[1]), dtype=np.quaternion)
    QFTclass.IQFTMatrix = np.zeros((matrix.shape[0], matrix.shape[1]), dtype=np.quaternion)
    # QFTclass.IQFTMatrix = np.zeros((QFTclass.QFTmatrix.shape[0], QFTclass.QFTmatrix.shape[1]), dtype=np.quaternion)

    fft_matrix = QFTclass.QFTmatrix
    #qft_inst = QFTclass()
    print(matrix.shape)
    QFTclass.h, QFTclass.w, QFTclass.c = matrix.shape

    for u in range(matrix.shape[0]):
        for v in range(matrix.shape[1]):
            # Q_fourier_transform(u,v)
            #threading.Thread(target=QFTclass.computeQFT, args=(u, v)).start()
            QFTclass.computeQFT(u, v)

    fft_matrix = QFTclass.QFTmatrix

    QFTclass.IQFTMatrix = np.zeros((fft_matrix.shape[0], fft_matrix.shape[1]), dtype=np.quaternion)
    #final_qft = bispy.qfft.iQfft(bispy.qfft.iQfft(filtered_mat))
    for u in range(fft_matrix.shape[0]):
        for v in range(fft_matrix.shape[1]):
            QFTclass.computeIQFT(u, v)

    final_qft = QFTclass.IQFTMatrix
    final_image = np.float_(rand(matrix.shape[0], matrix.shape[1], 3)*0)
    for x in range(final_qft.shape[0]):
            for y in range(final_qft.shape[1]):
                quat = final_qft[x, y]
                quat.real = 0
                final_image[x, y, 0] =round((quat * np.quaternion(0,1,0,0)).real * -1)
                final_image[x, y, 1] = round((quat * np.quaternion(0,0,1,0)).real * -1)
                final_image[x, y, 2] =round((quat * np.quaternion(0,0,0,1)).real * -1)
    plt.imshow(final_image)
    display_image("test", final_image)
    fb,fg,fr = cv2.split(final_image)
    fb = applyFullContrastStretch(fb) * 10
    fg = applyFullContrastStretch(fg) * 10
    fr = applyFullContrastStretch(fr) * 10
    final_image = cv2.merge([fb,fg,fr])
    plt.imshow(final_image)
    display_image("test", final_image)

if __name__ == "__main__":
    main()