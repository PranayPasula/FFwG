"""starter file to run homomorphic and or laplacian filtering"""

# Example Usage: ./runme.py -i image -f homomorphic -c cutoff -o order -gl gammaL -gh gammaH
# Example Usage: python runme.py -i image -f homomorphic -c cutoff -o order -gl gammaL -gh gammaH
# Example Usage: ./runme.py -i image -f laplacian -o cofficient/order
# Example Usage: python runme.py -i image -f laplacian -o cofficient/order

import cv2
import sys
from Sharpen import Sharpen
from datetime import datetime


def display_image(window_name, image):
    """A function to display image"""
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)


def main():
    """ The main funtion that parses input arguments, calls the approrpiate
     fitlering method and writes the output image"""

    #Parse input arguments
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument("-i", "--image", dest="image",
                        help="specify the name of the image", metavar="IMAGE")
    parser.add_argument("-f", "--filter", dest="filter",
                        help="specify name of the filter (homomorphic, laplacian)", metavar="FILTER")
    parser.add_argument("-c", "--cutoff_f", dest="cutoff_f",
                        help="specify the cutoff frequency", metavar="CUTOFF FREQUENCY")
    parser.add_argument("-o", "--order", dest="order",
                        help="specify the order/cofficient for homomorphic/laplacian filter", metavar="ORDER")
    parser.add_argument("-gl", "--gamma_l", dest="gamma_l",
                        help="specify the gamma L for homomorphic filter", metavar="GAMMAL")
    parser.add_argument("-gh", "--gamma_h", dest="gamma_h",
                        help="specify the gamma H for homomorphic filter", metavar="GAMMAH")

    args = parser.parse_args()

    #Load image
    if args.image is None:
        print("Please specify the name of image")
        print("use the -h option to see usage information")
        sys.exit(2)
    else:
        image_name = args.image.split(".")[0]
        input_image = cv2.imread(args.image, 0)
        rows, cols = input_image.shape

    #Check resize scale parametes
    if args.filter is None:
        print("Filter not specified using default (Homomorphic)")
        print("use the -h option to see usage information")
        filter = 'homomorphic'
    elif args.filter not in ['homomorphic', 'laplacian']:
        print("Unknown filter, using default (homomorphic)")
        print("use the -h option to see usage information")
        filter = 'homomorphic'
    else:
        filter = args.filter


    if filter in ['laplacian']:
        if args.order is None:
            print("Cutoff not specified. using default 0.00001")
            print("use the -h option to see usage information")
            order = 0.00001
        else:
            order = float(args.order)
        dummy = Sharpen()
        output = dummy.laplacian(input_image, order)
    elif filter in ['homomorphic']:
        if args.order is None:
            print("order of filter not specified, using default 1")
            print("use the -h option to see usage information")
            order = 1
        else:
            order = float(args.order)
        if args.gamma_l is None:
            print("gamma L not specified, using default 0.3")
            gamma_l = 0.3
        else:
            gamma_l = float(args.gamma_l)
        if args.gamma_h is None:
            print("gamma H not specified using default 0.3")
            gamma_h = 0.3
        else:
            gamma_h = float(args.gamma_h)
        if args.cutoff_f is None:
            print("cutoff freq not specified, using default 35")
            cutoff_f = 35
        else:
            cutoff_f = float(args.cutoff_f)
        dummy = Sharpen()
        output = dummy.homomorphic(input_image, gamma_l, gamma_h, cutoff_f, order)
    else:
        output = None


    #Write output file
    output_dir = 'output/'
    if filter == 'homomorphic':
        output_image_name = output_dir+image_name+"_"+filter+" gamma L "+str(gamma_l)+" gamma H "+str(gamma_h)+".png"
    elif filter == 'laplacian':
        output_image_name = output_dir+image_name+"_"+filter+" cofficient "+str(order)+".png"
    cv2.imwrite(output_image_name, output)


if __name__ == "__main__":
    main()