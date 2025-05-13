import numpy as np
import ctypes

npz=np.load("tz.npz")

compute_check = npz["compute_check"]
reg_check = npz["reg_check"]
flag_check = npz["flag_check"]
compute_hash = npz["compute_hash"]
reg_hash = npz["reg_hash"]
flag_hash = npz["flag_hash"]
reg_scrable = npz["reg_scrable"]

for i in range(1, 12):
    for j in range(compute_check.shape[1]):
        # print(f"{i} {j} {compute_check[i][j]} {reg_check[i][j]} {flag_check[i][j]}")
        if reg_check[i][j]:
            if reg_hash[i, j][:2].tolist() != [i, j]: # unprobable to be real, skip
                continue
            print(f"reg_check[{i}][{j}] = {reg_hash[i, j]}")
        if flag_check[i][j]:
            flagh = flag_hash[i, j]
            # to bits, unsigned
            flagh = ctypes.c_uint64(flagh).value
            if flagh > 2**20: # unprobable to be real, skip
                continue
            flagh = bin(flagh)[2:].zfill(16)[::-1]
            print(f"flag_check[{i}][{j}] = {flagh}")
        if compute_check[i][j]:
            print(f"compute_check[{i}][{j}] = {compute_hash[i, j]}")
            print(f"reg_scrable -> ({reg_scrable[i][0]}, {reg_scrable[i][1]})")
            break

# masks = npz["masks"]
# flag = np.load("flag.npz")["flag"]

# from PIL import Image

# flag_png = Image.fromarray(flag * 255)
# flag_png.show()

# def mask(mask, offset, flag):
#     flag = flag ^ np.roll(mask, offset, axis=1)
#     return flag

# flag = mask(masks[0], 1, flag)
# flag_cols = [flag[:, i] for i in range(flag.shape[1])]
# print(flag_cols)