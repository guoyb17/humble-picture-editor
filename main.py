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

def sphere(bitmap, width, height, background, x_limit, y_limit):
    '''
    Input: source bitmap and its size,
           background for target (directly cover) and its size for range limit.
           Especially, if background == None, x_limit and y_limit == any,
           then use black background.

    Runtime: input radius of target sphere (0 for min(width, height) / 2),
             (if use picture background) sphere center's coordinate

    Return: filled background (finished picture).
    '''
    legal_r = False
    while not legal_r:
        radius = int(input(">> Input sphere radius (pixel; 0 for min(width, height) / 2; must <= min(width, height) / 2): "))
        if radius > int(round(min(width, height) / 2)):
            print("[ERROR] radius must <= min(width, height) / 2!")
        else:
            legal_r = True
        if radius == 0:
            radius = int(round(min(width, height) / 2))
    x_c = radius
    y_c = radius
    if background == None:
        x_limit = 2 * radius
        y_limit = 2 * radius
        background = np.zeros((x_limit, y_limit, bitmap.shape[2]))
    else:
        print("[NOTE] You need to input the sphere center's coordinate.")
        x_c = int(input(">> Input center point x: "))
        y_c = int(input(">> Input center point y: "))
    for iter_x in range(max(x_c - radius, 0), min(x_c + radius, x_limit)):
        for iter_y in range(max(y_c - radius, 0), min(y_c + radius, y_limit)):
            dx = iter_x - x_c
            dy = iter_y - y_c
            rho = int(round(math.sqrt(dx ** 2 + dy ** 2)))
            if rho <= radius:
                phi = math.asin(rho / radius)
                rho_0 = radius * phi
                if rho == 0:
                    src_dx = 0
                    src_dy = 0
                else:
                    src_dx = dx * rho_0 / rho
                    src_dy = dy * rho_0 / rho
                src_x = int(round(height / 2 + src_dx))
                src_y = int(round(width / 2 + src_dy))
                if 0 <= src_x and src_x < height and 0 <= src_y and src_y < width:
                    background[iter_x][iter_y] = bitmap[src_x][src_y]
                else:
                    background[iter_x][iter_y] = [128, 128, 128] # gray padding
    return background

def cylinder(bitmap, width, height, is_r):
    '''
    Input: source bitmap and its size,
           whether row direction (x direction) is the shaft.

    Return: finished picture.
    '''
    if is_r:
        radius = int(round(height / math.pi))
        ans = np.zeros((radius * 2, width, bitmap.shape[2]))
        for iter_x in range(height):
            for iter_y in range(width):
                phi = (iter_x - height / 2) / radius
                tar_x = int(round(radius + radius * math.sin(phi)))
                if 0 <= tar_x and tar_x < radius * 2:
                    ans[tar_x][iter_y] = bitmap[iter_x][iter_y]
    else:
        radius = int(round(width / math.pi))
        ans = np.zeros((height, radius * 2, bitmap.shape[2]))
        for iter_x in range(height):
            for iter_y in range(width):
                phi = (iter_y - width / 2) / radius
                tar_y = int(round(radius + radius * math.sin(phi)))
                if 0 <= tar_y and tar_y < radius * 2:
                    ans[iter_x][tar_y] = bitmap[iter_x][iter_y]
    return ans

def main(ipt_img, opt_img, mode, background):
    src = image.open(ipt_img).convert("RGB")
    width, height = src.size
    bitmap = np.array(src)
    if mode == "subimg":
        if background == None:
            print("[ERROR] background is necessary for subimg mode!")
            return
        bg_pic = image.open(background).convert("RGB")
        x_limit, y_limit = bg_pic.size
        bg_bitmap = np.array(bg_pic)
        ans = projective(bitmap, width, height, bg_bitmap, x_limit, y_limit)
    elif mode == "sphere":
        bg_bitmap = None
        x_limit = 0
        y_limit = 0
        if background != None:
            bg_pic = image.open(background).convert("RGB")
            x_limit, y_limit = bg_pic.size
            bg_bitmap = np.array(bg_pic)
        ans = sphere(bitmap, width, height, bg_bitmap, x_limit, y_limit)
    elif mode == "cylinder":
        print("[NOTE] Which direction do you want to use as the shaft of the cylinder?")
        legal_selection = False
        while not legal_selection:
            _selection = input(">> Input shaft direction (r / c): ")
            if _selection == "r":
                legal_selection = True
                ans = cylinder(bitmap, width, height, True)
            elif _selection == "c":
                legal_selection = True
                ans = cylinder(bitmap, width, height, False)
            else:
                print("[ERROR] You must input \"r\" or \"c\"!")
    else:
        print("[ERROR] Illegal mode! Only accept: subimg, sphere, cylinder")
        return
    dst = image.fromarray(np.uint8(ans))
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
                        help="mode: subimg, sphere, cylinder",
                        required=True
                        )
    parser.add_argument("-b", "--background", type=str,
                        default=None, 
                        help="background picture, None for black background; ignored by cylinder; essential for subimg!",
                        required=False
                        )

    args = parser.parse_args()
    main(args.input, args.output, args.mode, args.background)
