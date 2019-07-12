import numpy as np
import cv2


class PeriodicNoise:

    image = None

    def __init__(self, image, method, same):
        self.image = image
        if method == 'periodic_point':
            self.method = self.random_periodic_point
        elif method == 'periodic_circle':
            self.method = self.random_periodic_circle
        elif method == 'periodic_ring':
            self.method = self.random_periodic_ring
        if same is True:
            self.same = True
        else:
            self.same = False

    def random_periodic_point(self, scalar = 0.1):
        """
        Function to create two symmetric points of periodic noise
        :param scalar: Amount to modify the current 'max noise' in system by
        :return: image as np array
        """
        import random
        if self.image.ndim == 2:
            row, col = self.image.shape

            image_dft = np.fft.fft2(self.image)
            image_dft_shift = np.fft.fftshift(image_dft)

            center = (int(row / 2), int(col / 2))

            rand_point = (random.randint(1, row / 4), random.randint(1, col / 4))

            current_max = image_dft_shift[center]

            image_dft_shift[tuple(np.subtract(center, rand_point))] = current_max * scalar
            image_dft_shift[tuple(np.add(center, rand_point))] = current_max * scalar

            image_idft_shift = np.fft.ifftshift(image_dft_shift)
            image_idft = np.fft.ifft2(image_idft_shift)

            return abs(image_idft).astype('uint8')

        if self.image.ndim == 3:
            row, col, dim = self.image.shape
            image_append = np.empty(self.image.shape).astype('complex64')
            b = self.image[:, :, 0]
            g = self.image[:, :, 1]
            r = self.image[:, :, 2]
            counter = 0

            center = (int(row / 2), int(col / 2))


            if self.same is True:
                rand_point = (random.randint(1, row / 4), random.randint(1, col / 4))

            for i in [b, g, r]:

                image_dft = np.fft.fft2(i)
                image_dft_shift = np.fft.fftshift(image_dft)

                current_max = image_dft_shift[center]

                if self.same is False:
                    rand_point = (random.randint(1, row / 4), random.randint(1, col / 4))

                image_dft_shift[tuple(np.subtract(center, rand_point))] = current_max * scalar
                image_dft_shift[tuple(np.add(center, rand_point))] = current_max * scalar

                image_idft_shift = np.fft.ifftshift(image_dft_shift)
                if counter == 0:
                    image_append[:, :, 0] = np.fft.ifft2(image_idft_shift)
                    counter += 1
                if counter == 1:
                    image_append[:, :, 1] = np.fft.ifft2(image_idft_shift)
                    counter += 1
                if counter == 2:
                    image_append[:, :, 2] = np.fft.ifft2(image_idft_shift)

            return abs(image_append).astype('uint8')

    def random_periodic_circle(self, scalar = 0.01, r = 3):
        import random
        if self.image.ndim == 2:
            row, col = self.image.shape

            image_dft = np.fft.fft2(self.image)
            image_dft_shift = np.fft.fftshift(image_dft)

            center = (int(row / 2), int(col / 2))

            rand_point = (random.randint(1, row), random.randint(1, col))

            current_max = image_dft_shift[center]

            mask = self.create_circle_mask(center = rand_point, radius = r)

            image_dft_shift[mask] = current_max * scalar

            image_idft_shift = np.fft.ifftshift(image_dft_shift)
            image_idft = np.fft.ifft2(image_idft_shift)

            return abs(image_idft).astype('uint8')

        if self.image.ndim == 3:
            row, col, dim = self.image.shape
            image_append = np.empty(self.image.shape).astype('complex64')
            b = self.image[:, :, 0]
            g = self.image[:, :, 1]
            r = self.image[:, :, 2]
            counter = 0

            center = (int(row / 2), int(col / 2))

            if self.same is True:
                rand_point = (random.randint(1, row), random.randint(1, col))

            for i in [b, g, r]:

                image_dft = np.fft.fft2(i)
                image_dft_shift = np.fft.fftshift(image_dft)

                current_max = image_dft_shift[center]

                if self.same is False:
                    rand_point = (random.randint(1, row), random.randint(1, col))

                mask = self.create_circle_mask(center=rand_point, radius=r)

                image_dft_shift[mask] = current_max * scalar

                image_idft_shift = np.fft.ifftshift(image_dft_shift)

                if counter == 0:
                    image_append[:, :, 0] = np.fft.ifft2(image_idft_shift)
                    counter += 1
                if counter == 1:
                    image_append[:, :, 1] = np.fft.ifft2(image_idft_shift)
                    counter += 1
                if counter == 2:
                    image_append[:, :, 2] = np.fft.ifft2(image_idft_shift)

            return abs(image_append).astype('uint8')

    def random_periodic_ring(self, scalar = 0.01, small_rad = 25, large_rad = 27):
        import random
        if self.image.ndim == 2:
            row, col = self.image.shape

            image_dft = np.fft.fft2(self.image)
            image_dft_shift = np.fft.fftshift(image_dft)

            center = (int(row / 2), int(col / 2))

            current_max = image_dft_shift[center]

            # create circle
            x = np.arange(0, row)
            y = np.arange(0, col)

            mask = self.create_ring_mask(inner_r = small_rad, outer_r = large_rad)

            image_dft_shift[mask] = current_max * scalar

            image_idft_shift = np.fft.ifftshift(image_dft_shift)
            image_idft = np.fft.ifft2(image_idft_shift)

            return abs(image_idft).astype('uint8')

        if self.image.ndim == 3:
            row, col, dim = self.image.shape
            image_append = np.empty(self.image.shape).astype('complex64')
            b = self.image[:, :, 0]
            g = self.image[:, :, 1]
            r = self.image[:, :, 2]
            counter = 0

            center = (int(row / 2), int(col / 2))

            # rand_point = (random.randint(1, row), random.randint(1, col))

            for i in [b, g, r]:

                image_dft = np.fft.fft2(i)
                image_dft_shift = np.fft.fftshift(image_dft)

                current_max = image_dft_shift[center]

                # create circle
                x = np.arange(0, row)
                y = np.arange(0, col)

                mask = self.create_ring_mask(inner_r=small_rad, outer_r=large_rad)

                image_dft_shift[mask] = current_max * scalar

                image_idft_shift = np.fft.ifftshift(image_dft_shift)

                if counter == 0:
                    image_append[:, :, 0] = np.fft.ifft2(image_idft_shift)
                    counter += 1
                if counter == 1:
                    image_append[:, :, 1] = np.fft.ifft2(image_idft_shift)
                    counter += 1
                if counter == 2:
                    image_append[:, :, 2] = np.fft.ifft2(image_idft_shift)

            return abs(image_append).astype('uint8')

    def add_noise(self):
        output = self.method()
        return output

    def create_circle_mask(self, center=None, radius=None):
        """
        Function to create a circular mask
        :param center: center of circle
        :param radius: radius of circle
        :return: circular mask as np array
        """

        row, col = self.image.shape[:2]

        if center is None:
            center = [int(row / 2), int(col / 2)]
        if radius is None:
            radius = min(center[0], center[1], row - center[0], col - center[1])

        Y, X = np.ogrid[:row, :col]
        dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

        mask = dist_from_center <= radius

        return mask

    def create_ring_mask(self, center=None, inner_r=None, outer_r=None):
        """
        Function to create a ring-shaped masked
        :param center: center of ring
        :param inner_r: radius of inner circle
        :param outer_r: radius of outer circle
        :return: ring mask as np array
        """

        row, col = self.image.shape[:2]

        if center is None:  # use the middle of the image
            center = [int(row / 2), int(col / 2)]

        Y, X = np.ogrid[:row, :col]
        dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

        mask = (inner_r <= dist_from_center) & \
               (dist_from_center <= outer_r)

        return mask

