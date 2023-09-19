"""
6.101 Lab 1: Katie Chen
Image Processing
"""

#!/usr/bin/env python3

import math

from PIL import Image

# NO ADDITIONAL IMPORTS ALLOWED!


def get_pixel(image, row, col):
    pixel_index = row * image["width"] + col 
    return image["pixels"][pixel_index]


def set_pixel(image, row, col, color):
    pixel_index = row * image["width"] + col 
    image["pixels"][pixel_index] = color

def apply_per_pixel(image, func):
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"][:],
    }
    for i in range(image["height"]): 
        # row 
        for j in range(image["width"]): 
            # col
            color = get_pixel(image, i, j)
            new_color = func(color)
            set_pixel(result, i, j, new_color)

    return result


def inverted(image):
    return apply_per_pixel(image, lambda color: 255-color)


# HELPER FUNCTIONS

def get_pixel_zero(image, row, col): 
    new_row = row
    new_col = col
    if row < 0:
        return 0
    if row > image["height"] - 1: 
        return 0

    if col < 0 or col > image["width"]-1: 
        return 0
    
    else: 
        return get_pixel(image, row, col)
    
def get_pixel_extend(image, row, col): 
    new_row = row
    new_col = col
    if row < 0:
        new_row = 0
    if row > image["height"] - 1: 
        new_row = image["height"] - 1

    if col < 0:  
        new_col = 0
    if col > image["width"] - 1:
        new_col = image["width"] - 1

    return get_pixel(image, new_row, new_col) 


def get_pixel_wrap(image, row, col): 
    new_row = row
    new_col = col

    # if row < 0:
    #     new_row = image["height"] - 1 - (row % image["height"])
    # if row > image["height"] - 1: 
    #     new_row = row % image["height"]

    # if col < 0:  
    #     new_col = image["width"] - 1 - (row % image["width"])
    # if col > image["width"] - 1:
    #     new_col = col % image["width"]

    new_row = row % image["height"]
    new_col = col % image["width"]

    return get_pixel(image, new_row, new_col) 


def correlate(image, kernel, boundary_behavior):
    """
    Compute the result of correlating the given image with the given kernel.
    `boundary_behavior` will one of the strings "zero", "extend", or "wrap",
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    if boundary_behavior is not one of "zero", "extend", or "wrap", return
    None.

    Otherwise, the output of this function should have the same form as a 6.101
    image (a dictionary with "height", "width", and "pixels" keys), but its
    pixel values do not necessarily need to be in the range [0,255], nor do
    they need to be integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE

    # kernel = {
    #     'size': 3,
    #     'pixles': [1, 1, 1, 1, 1, 1, 1, 1, 1]
    # }

    """

    

    if boundary_behavior not in ["zero", "extend", "wrap"]: 
        return None 
    
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"][:],
    } 
    
    kernel_length = len(kernel["pixels"])
    k = kernel["size"] // 2
    for row in range(image["height"]): 
        for col in range(image["width"]): 
                currently_under_kernel = []
                # getting what's currently under the kernel
                for r in range(row - k, row + k + 1):
                    for c in range(col - k, col + k + 1):
                        if boundary_behavior == "zero":
                            currently_under_kernel.append(get_pixel_zero(image, r, c))
                        if boundary_behavior == "extend":
                            currently_under_kernel.append(get_pixel_extend(image, r, c))
                        if boundary_behavior == "wrap": 
                            currently_under_kernel.append(get_pixel_wrap(image, r, c))
                new_color = sum([currently_under_kernel[i] * kernel["pixels"][i] for i in range(kernel_length)])
                set_pixel(result, row, col, new_color)

    return result
                
        

def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the "pixels" list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    result = {
        "height": image["height"], 
        "width": image["width"], 
        "pixels": image["pixels"][:]
    }

    for i, pixel in enumerate(image["pixels"]): 
        
        if pixel <= 0: 
            result["pixels"][i] = 0

        if pixel >= 255: 
            result["pixels"][i] = 255

        result["pixels"][i] = round(pixel)
    
    return result


def blur_kernel(n): 
    """
    takes a number n

    returns a n x n kernel
    """

    kernel = {
        "size": n,
        "pixels": []
    }

    kernel_length = len(range(n**2))
    value = 1 / kernel_length
    kernel["pixels"] = [value] * kernel_length

    return kernel

# FILTERS

def blurred(image, kernel_size, boundry_behavior="extend"):
    """
    Return a new image representing the result of applying a box blur (with the
    given kernel size) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)

    # then compute the correlation of the input image with that kernel

    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    
    kernel = blur_kernel(kernel_size)
    result = correlate(image, kernel, boundary_behavior = boundry_behavior)

    return round_and_clip_image(result)


def sharpened(image, n): 
    """
    creates a blurred image B with n x n sized kernel 
    sharpens the image by S = 2 * image - B

    returns an sharpened image
    """
    result = {
        "height": image["height"], 
        "width": image["width"], 
        "pixels": image["pixels"][:]
    }
    blurred_img = blurred(image, n)
    for i in range(len(image["pixels"])): 
        result["pixels"][i] = 2 * image["pixels"][i] - blurred_img["pixels"][i]
    
    return round_and_clip_image(result)

def edges(image): 
    """
    correlate K1, K2 kernel on image to obtain O1, O2 resulting image
    the final result is the square root of (sum of each pixel squared in O1 and O2)

    return an image

    """

    result = {
        "height": image["height"], 
        "width": image["width"], 
        "pixels": image["pixels"][:]
    }

    k1 = {
        "size": 3,
        "pixels": [
            -1, -2 ,-1,
            0, 0,  0,
            1,  2,  1
        ]
    }

    k2 = {
        "size": 3,
        "pixels": [
            -1, 0, 1,
            -2, 0, 2,
            -1, 0, 1
        ]
    }

    O1 = correlate(image, k1, "extend")
    O2 = correlate(image, k2, "extend")

    for i in range(len(image["pixels"])): 
        result["pixels"][i] = math.sqrt(O1["pixels"][i] ** 2 + O2["pixels"][i] ** 2)
    
    return round_and_clip_image(result)


# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image("test_images/cat.png")
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError(f"Unsupported image mode: {img.mode}")
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_greyscale_image(image, filename, mode="PNG"):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the "mode" parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    pass

