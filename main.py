import os, argparse, math
from PIL import Image as image
import numpy as np


def main(ipt_img, opt_img, mode, param):
    src = image.open(ipt_img)
    width, height = src.size
    bitmap = np.array(src)
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script to modify 24-bit RGB pictures."
        )
    parser.add_argument("-i", "--input", type=str,
                        default=None,
                        help="input file",
                        required=True
                        )
    parser.add_argument("-o", "--output", type=str,
                        default="out",
                        help="output file"
                        )
    parser.add_argument("-m", "--mode", type=str,
                        help="mode: brightness, contrast, gamma, equalization",
                        required=True
                        )
    parser.add_argument("-p", "--param", type=float,
                        default=None, 
                        help="modify parameter (any value for equalization)",
                        required=True
                        )

    args = parser.parse_args()
    main(args.input, args.output, args.mode, args.param)
