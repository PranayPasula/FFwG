__author__      = "Charles Livermore"
__email__       = "cmliverm@central.uh.edu"
__version__     = "0.0.1"

import cv2
import sys
from Statistical.StatNoise import StatNoise
from Periodic.PeriodicNoise import PeriodicNoise

def main():
    """
    Main noise function.
    Loads image, calls noise functions from other files
    :return:
    """
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument("-i", "--image", dest="image",
                        help="Specify the image filename", metavar="IMAGE")
    parser.add_argument("-d", "--dim", dest="dimension",
                        help="Specify how to load the image: grey for greyscale, rgb for color", metavar="DIM")
    parser.add_argument("-m", "--method", dest="method",
                        help="Specify the type of noise ", metavar="METHOD")
    parser.add_argument("-s", "--same", dest="same",
                        help="Specify if the RGB random points should be the same for all channels", metavar="SAME")
    parser.add_argument("-c", "--copy", dest="copy",
                        help="Specify if the modified image should be saved in the local directory with appended filename", metavar="copy")


    # parse arguments
    args = parser.parse_args()

    # Load image
    if args.image is None:
        print("Please specify the name of image")
        print("use the -h option to see usage information")
        sys.exit(2)
    else:
        if args.dimension is None:
            print("Please specify how to load the image: grey for greyscale, rgb for color.")
        if args.dimension in ['grey', 'GREY']:
            input_image = cv2.imread(args.image, 0)
        if args.dimension in ['rgb', 'RGB']:
            input_image = cv2.imread(args.image, 1)

    # Handle method
    if args.method is None:
        print("Noise method not specified using default (gauss)")
        print("use the -h option to see usage information")
        method = 'gauss'
    elif args.method not in ['gauss', 'impulse', 'poisson', 'rayleigh', 'gamma', 'exponential', 'periodic_point',
                             'periodic_circle', 'periodic_ring']:
        print("Unknown method, using default (gauss)")
        print("use the -h option to see usage information")
        method = 'gauss'
    else:
        method = args.method

    # Handle same
    if args.same in ['yes', 'YES', '1']:
        same = True
    elif args.same in ['no', 'NO', '0']:
        same = False
    else:
        same = True

    if method in ['gauss', 'impulse', 'poisson', 'rayleigh', 'gamma', 'exponential']:
        Noise_obj = StatNoise(input_image, method)
        output = Noise_obj.add_noise()

    if method in ['periodic_point', 'periodic_circle', 'periodic_ring']:
        Noise_obj = PeriodicNoise(input_image, method, same)
        output = Noise_obj.add_noise()

    # Handle copy
    if args.copy in ['yes', 'YES', '1']:
        cv2.imwrite(args.image + '_' + method + '.png',output)

    cv2.imshow('image', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    main()

