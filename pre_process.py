"""Image Pre-Processing"""
import sys
import cv2
import numpy as np

from config import *
from adjust_photos import adjust


def preprocess_image(image):
    """
    Prepares the image for the next transformation. Applies threshold and canny edge detection.

    :return: Matrices of image after each step.
    """
    if VERBOSE:
        print("Preprocessing image.")
    gray = image.copy()
    _, thresholded = cv2.threshold(gray, THRESHOLD_MIN, THRESHOLD_MAX, cv2.THRESH_BINARY)
    element = np.ones((3, 3))
    thresholded = cv2.erode(thresholded, element)
    edges = cv2.Canny(thresholded, 10, 100, apertureSize=3)
    return edges, thresholded


def detect_lines(hough, image, nlines):
    """
    Detects lines present in the picture and adds ones that are horizontal enough to a list.

    :param hough: result of Hough Transform function.
    :param image: Main image
    :param nlines: How many lines we want to process.
    :return: A list of horizontal lines and an image with lines drawn on it.
    """
    if VERBOSE:
        print("Detecting lines.")
    all_lines = set()
    width, height = image.shape
    # convert to color image so that you can see the lines
    lines_image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    for result_arr in hough[:nlines]:
        rho = result_arr[0][0]
        theta = result_arr[0][1]
        a = np.cos(theta)
        b = np.sin(theta)

        x0 = a * rho
        y0 = b * rho
        shape_sum = width + height
        x1 = int(x0 + shape_sum * (-b))
        y1 = int(y0 + shape_sum * a)
        x2 = int(x0 - shape_sum * (-b))
        y2 = int(y0 - shape_sum * a)

        start = (x1, y1)
        end = (x2, y2)
        diff = y2 - y1
        if abs(diff) < LINES_ENDPOINTS_DIFFERENCE:
            all_lines.add(int((start[1] + end[1]) / 2))
            cv2.line(lines_image_color, start, end, (0, 0, 255), 2)

    if SAVING_IMAGES_STEPS:
        cv2.imwrite("output/5lines.png", lines_image_color)

    return all_lines, lines_image_color


def detect_staffs(all_lines):
    """
    Detects staffs in the image.

    :param all_lines: all lines detected in the image
    :return: list of tuples with beginnings and ends of staffs detected in the image
    """
    if VERBOSE:
        print("Detecting staffs.")
    staffs = []
    lines = []
    all_lines = sorted(all_lines)
    for current_line in all_lines:
        # If current line is far away from last detected line
        if lines and abs(lines[-1] - current_line) > LINES_DISTANCE_THRESHOLD:
            if len(lines) >= 5:
                # Consider it the start of the next staff.
                # If <5 - not enough lines detected. Probably an anomaly - reject.
                staffs.append((lines[0], lines[-1]))
            del lines[:]
        lines.append(current_line)

    # Process the last line
    if len(lines) >= 5:
        if abs(lines[-2] - lines[-1]) <= LINES_DISTANCE_THRESHOLD:
            staffs.append((lines[0], lines[-1]))
    return staffs


def draw_staffs(image, staffs, original):
    """
    Draws staffs on the image.

    :param image: image to write staffs onto
    :param staffs: list of Staff to draw
    """
    width = image.shape[0]
    cropped_staffs = []
    for staff in staffs:
        crop_img = cropped_staffs.append(original[staff[0]-20:staff[1]+20, 0:width])
        # cv2.imwrite("output/cropped.png", crop_img)
        cv2.line(image, (0, staff[0]), (width, staff[0]), ( 0, 0, 0), 5)
        cv2.line(image, (0, staff[1]), (width, staff[1]), ( 0, 0, 0), 5)

    if SAVING_IMAGES_STEPS:
        cv2.imwrite("output/6staffs.png", image)
    return cropped_staffs


def get_staffs(image):
    """
    Returns a list of Staff
    :param image: image to get staffs from
    :return: list of Staff
    """
    processed_image, thresholded = preprocess_image(image)
    hough = cv2.HoughLines(processed_image, 1, np.pi / 150, 200)
    all_lines, lines_image_color = detect_lines(hough, thresholded, 80)
    staffs = detect_staffs(all_lines)
    staves = draw_staffs(lines_image_color, staffs, image)
    return staves

def main():
    # path to the image
    filename = "photos/real1.png"
    image = cv2.imread(filename)
    adjusted_photo = adjust(image)
    staffs = get_staffs(adjusted_photo)
    # save all the staffs onto the staffs folder
    for indx, staff in enumerate(staffs):
        filename = "output/staffs/cropped"+ str(indx)+".png"
        cv2.imwrite(filename, staff)

if __name__ == "__main__":
    main()
