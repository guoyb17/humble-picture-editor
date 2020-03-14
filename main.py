import os, argparse, math
from PIL import Image as image
import numpy as np


def projective(bitmap, width, height, background, x_limit, y_limit):
    '''
    Input: source bitmap and its size, background for target (directly cover) and its size for range limit.

    Runtime: input three points from (..., ...) to (..., ...).

    Return: filled background (finished picture).
    '''
    print("[NOTE] You need 4 points to clarify projective parameters.")
    As = [0.0, 0.0]
    Ad = [0.0, 0.0]
    Bs = [0.0, 0.0]
    Bd = [0.0, 0.0]
    Cs = [0.0, 0.0]
    Cd = [0.0, 0.0]
    Ds = [0.0, 0.0]
    Dd = [0.0, 0.0]
    print("Point A: from...")
    As[0] = int(input(">> Input point A from x: "))
    As[1] = int(input(">> Input point A from y: "))
    print("Point A: to...")
    Ad[0] = int(input(">> Input point A to x: "))
    Ad[1] = int(input(">> Input point A to y: "))
    print("Point B: from...")
    Bs[0] = int(input(">> Input point B from x: "))
    Bs[1] = int(input(">> Input point B from y: "))
    print("Point B: to...")
    Bd[0] = int(input(">> Input point B to x: "))
    Bd[1] = int(input(">> Input point B to y: "))
    print("Point C: from...")
    Cs[0] = int(input(">> Input point C from x: "))
    Cs[1] = int(input(">> Input point C from y: "))
    print("Point C: to...")
    Cd[0] = int(input(">> Input point C to x: "))
    Cd[1] = int(input(">> Input point C to y: "))
    print("Point D: from...")
    Ds[0] = int(input(">> Input point D from x: "))
    Ds[1] = int(input(">> Input point D from y: "))
    print("Point D: to...")
    Dd[0] = int(input(">> Input point D to x: "))
    Dd[1] = int(input(">> Input point D to y: "))
    tr_mat = np.eye(3)
    _A = np.array([[As[0], As[1], 1, 0, 0, 0, -As[0] * Ad[0], -As[1] * Ad[0]],
                   [0, 0, 0, As[0], As[1], 1, -As[0] * Ad[1], -As[1] * Ad[1]],
                   [Bs[0], Bs[1], 1, 0, 0, 0, -Bs[0] * Bd[0], -Bs[1] * Bd[0]],
                   [0, 0, 0, Bs[0], Bs[1], 1, -Bs[0] * Bd[1], -Bs[1] * Bd[1]],
                   [Cs[0], Cs[1], 1, 0, 0, 0, -Cs[0] * Cd[0], -Cs[1] * Cd[0]],
                   [0, 0, 0, Cs[0], Cs[1], 1, -Cs[0] * Cd[1], -Cs[1] * Cd[1]],
                   [Ds[0], Ds[1], 1, 0, 0, 0, -Ds[0] * Dd[0], -Ds[1] * Dd[0]],
                   [0, 0, 0, Ds[0], Ds[1], 1, -Ds[0] * Dd[1], -Ds[1] * Dd[1]]])
    _b = np.array([[Ad[0]], [Ad[1]], [Bd[0]], [Bd[1]], [Cd[0]], [Cd[1]], [Dd[0]], [Dd[1]]])
    _x = np.linalg.solve(_A, _b)
    tr_mat[0][0] = _x[0][0]
    tr_mat[0][1] = _x[1][0]
    tr_mat[0][2] = _x[2][0]
    tr_mat[1][0] = _x[3][0]
    tr_mat[1][1] = _x[4][0]
    tr_mat[1][2] = _x[5][0]
    tr_mat[2][0] = _x[6][0]
    tr_mat[2][1] = _x[7][0]
    for iter_x in range(height):
        for iter_y in range(width):
            src = np.array([[iter_y], [iter_x], [1]])
            dst = np.matmul(tr_mat, src)
            t_y = int(round(dst[0][0] / dst[2][0]))
            t_x = int(round(dst[1][0] / dst[2][0]))
            if 0 <= t_x and t_x < x_limit and 0 <= t_y and t_y < y_limit:
                background[t_x][t_y] = bitmap[iter_x][iter_y]
    return background

def main(ipt_img, opt_img, mode, background):
    src = image.open(ipt_img)
    width, height = src.size
    bitmap = np.array(src)
    if mode == "subimg":
        if background == None:
            print("[ERROR] background is necessary for subimg mode!")
            return
        bg_pic = image.open(background)
        x_limit, y_limit = bg_pic.size
        bg_bitmap = np.array(bg_pic)
        ans = projective(bitmap, width, height, bg_bitmap, x_limit, y_limit)
    elif mode == "sphere":
        pass
    elif mode == "new": # TODO: change new
        pass
    else:
        print("[ERROR] Illegal mode! Only accept: subimg, sphere, new") # TODO: change new
        return
    dst = image.fromarray(ans)
    dst.save(opt_img)

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
                        default=None,
                        help="output file",
                        required=True
                        )
    parser.add_argument("-m", "--mode", type=str,
                        help="mode: subimg, sphere, new",
                        required=True
                        )
    parser.add_argument("-b", "--background", type=str,
                        default=None, 
                        help="background picture, None for black background; essential for subimg!",
                        required=False
                        )

    args = parser.parse_args()
    main(args.input, args.output, args.mode, args.background)
