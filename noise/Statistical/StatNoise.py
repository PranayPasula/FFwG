import numpy as np


class StatNoise:

    image = None
    mean = None
    sigma = None
    sp_ratio = None
    percent = None
    method = None

    def __init__(self, image, method):
        self.image = image
        if method == 'gauss':
            self.method = self.gaussian_noise
        elif method == 'impulse':
            self.method = self.impulse_noise
        elif method == 'poisson':
            self.method = self.poisson_noise
        elif method == 'rayleigh':
            self.method = self.rayleigh_noise
        elif method == 'gamma':
            self.method = self.gamma_noise
        elif method == 'exponential':
            self.method = self.exponential_noise

    def gaussian_noise(self, mean=0, sigma=20):
        """
        Function to add gaussian noise (normal dist) to an image
        :param mean: mean value of distribution
        :param sigma: standard deviation
        :return: image plus noise
        """
        if self.image.ndim == 3:
            row, col, ch = self.image.shape
            '''
            Parameters:
                mean (mu): a.k.a. the expectation of the dist.
                sigma (standard deviation): square this for the variance (if needed)
            '''
            gauss_noise = np.random.normal(mean, sigma, (row, col, ch))
            gauss_noise = gauss_noise.reshape(row, col, ch)
            image_noise = self.image + gauss_noise

        elif self.image.ndim == 2:
            row, col  = self.image.shape
            '''
            Parameters:
                mean (mu): a.k.a. the expectation of the dist.
                sigma (standard deviation): square this for the variance (if needed)
            '''
            gauss_noise = np.random.normal(mean, sigma, (row, col))
            gauss_noise = gauss_noise.reshape(row, col)
            image_noise = self.image + gauss_noise

        return image_noise.astype('uint8')

    def impulse_noise(self, sp_ratio=0.5, percent=0.1):
        """
        Function to add impulse (salt & pepper) noise to an image
        :param sp_ratio: value between 0 and 1; 1 = all salt, 0 = all pepper
        :param percent: What percent of the image to affect
        :return:
        """

        # make local copy to edit
        image_copy = np.copy(self.image)

        # Add "Salt"

        salt_num = np.ceil(percent * self.image.size * sp_ratio)
        coords = [np.random.randint(0, i - 1, int(salt_num))
                  for i in self.image.shape]
        image_copy[tuple(coords)] = 255

        # Add "Pepper"
        pepper_num = np.ceil(percent * self.image.size * (1. - sp_ratio))
        coords = [np.random.randint(0, i - 1, int(pepper_num))
                  for i in self.image.shape]
        image_copy[tuple(coords)] = 0

        return image_copy.astype('uint8')

    def poisson_noise(self):

        image_noise = np.random.poisson(self.image, self.image.shape)
        return image_noise.astype('uint8')

    def rayleigh_noise(self, scale=25):

        image_noise = self.image + np.random.rayleigh(scale, self.image.shape)
        return image_noise.astype('uint8')

    def gamma_noise(self, shape=5, scale=10):

        image_noise = self.image + np.random.gamma(shape, scale, self.image.shape)
        return image_noise.astype('uint8')

    def exponential_noise(self, scale=15):

        image_noise = self.image + np.random.exponential(scale, self.image.shape)
        return image_noise.astype('uint8')

    def add_noise(self):
        output = self.method()
        return output

