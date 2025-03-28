import numpy as np


def conv_nested(image, kernel):
    Hi, Wi = image.shape
    Hk, Wk = kernel.shape
    out = np.zeros((Hi, Wi))
    kernel = np.flip(kernel)
    for i in range(int(Hk // 2), Hi - int(Hk // 2)):
        for j in range(int(Wk // 2), Wi - int(Wk // 2)):
            for n in range(Hk):
                for m in range(Wk):
                    out[i,j] += np.abs(image[i - int(Hk // 2) + n,j - int(Wk // 2) + m]) * kernel[n,m]
    return out


def zero_pad(image, pad_height, pad_width):
    H, W = image.shape
    out = np.zeros((H + 2 * pad_height, W + 2 * pad_width))
    out[pad_height:H + pad_height, pad_width:W + pad_width] = image
    return out


def conv_fast(image, kernel):
    Hi, Wi = image.shape
    Hk, Wk = kernel.shape
    out = np.zeros((Hi, Wi))
    kernel = np.flip(kernel)
    image = zero_pad(image, int(Hk // 2), int(Wk // 2))
    for i in range(Hi):
        for j in range(Wi):
            out[i,j] = np.sum(np.multiply(kernel, image[i:(i+Hk),j:(j + Wk)])) / 255 / 255

    return out


def cross_correlation(f, g):
    g = np.flip(g)
    out = conv_fast(f, g)

    return out


def zero_mean_cross_correlation(f, g):
    mean_g = np.mean(g)
    g_new = np.zeros_like(g).astype(float)
    g_new[:] = g[:] - mean_g
    print(np.mean(g_new))
    g_new = np.flip(g_new)
    out = conv_fast(f, g_new)

    return out


def normalized_cross_correlation(f, g):
    Hi, Wi = f.shape
    Hk, Wk = g.shape
    out = np.zeros((Hi, Wi))
    g = (g - np.mean(g)) / np.std(g) 
    f = zero_pad(f, int(Hk // 2), int(Wk // 2))
    f_norm = np.zeros_like(g)
    for i in range(Hi):
        for j in range(Wi):
            f_norm = f[i:(i+Hk),j:(j + Wk)]
            out[i,j] = np.sum(np.multiply(g, (f_norm - np.mean(f_norm))) / np.std(f_norm))

    return out
