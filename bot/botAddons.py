import cv2
import urllib
from urllib.request import urlopen, Request
import numpy as np


def draw_image(original_image):
    #IMAGE_PATH = "Drawn_images/" + str(original_image)
    request_url = Request(original_image, headers={'User-Agent': 'Mozilla/6.0'})
    req = urlopen(request_url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    image = cv2.imdecode(arr, -1)

    image_shape = image.shape
    canvas = cv2.imread('Drawn_images/pencilsketch_bg.jpg', cv2.CV_8UC1)
    canvas = cv2.resize(canvas, (image_shape[1], image_shape[0]))  # resize background image to the base image size

    img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (21, 21), 0, 0)
    img_blend = cv2.divide(img_gray, img_blur, scale=256)

    img_blend = cv2.multiply(img_blend, canvas, scale=1. / 256)
    final_blend = cv2.cvtColor(img_blend, cv2.COLOR_GRAY2RGB)

    draw_file = 'Drawn_images/drawImage.jpg'
    status = cv2.imwrite(draw_file, final_blend)
    print("Image written to file-system : ", status)
    return draw_file


def cartoon(base_image):
    numDownSamples = 2  # number of downscaling steps
    numBilateralFilters = 7  # number of bilateral filtering steps
    img_rgb = cv2.imread(base_image)
    # -- STEP 1 --
    # downsample image using Gaussian pyramid
    img_color = img_rgb
    for _ in range(numDownSamples):
        img_color = cv2.pyrDown(img_color)

    # repeatedly apply small bilateral filter instead of applying
    # one large filter
    for _ in range(numBilateralFilters):
        img_color = cv2.bilateralFilter(img_color, 9, 9, 7)

    # upsample image to original size
    for _ in range(numDownSamples):
        img_color = cv2.pyrUp(img_color)

    # make sure resulting image has the same dims as original
    img_color = cv2.resize(img_color, img_rgb.shape[:2])

    # -- STEPS 2 and 3 --
    # convert to grayscale and apply median blur
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)

    # -- STEP 4 --
    # detect and enhance edges
    img_edge = cv2.adaptiveThreshold(img_blur, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, 9, 2)

    # -- STEP 5 --
    # convert back to color so that it can be bit-ANDed with color image
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    cv2.imshow('final: ', img_edge)
    cv2.waitKey(0)
    return cv2.bitwise_and(img_color, img_edge)

