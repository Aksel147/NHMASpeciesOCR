import cv2
from nhma_species_ocr.rotated_rect_crop.rotated_rect_crop import crop_rotated_rectangle
from nhma_species_ocr.util.util import most_frequent


def find_cover_label(img: cv2.Mat) -> tuple[cv2.Mat, bool]:
    """
    
    """
    scale = 1
    extra_border = 100
    img = cv2.resize(src=img, dsize=(0, 0), fx=scale, fy=scale)

    img_bottom_left = img[(img.shape[0]-img.shape[0]/5).__round__():, :(img.shape[1]/2).__round__()]

    canny = cv2.Canny(img_bottom_left, 100, 200)

    rect = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    dilation = cv2.dilate(canny, rect, iterations=1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    parent_contours_with_subchildren = [cnt[3] for cnt in hierarchy[0] if cnt[2] != -1 and cnt[3] != -1]
    label_contour = most_frequent(parent_contours_with_subchildren)

    ((x, y), (width, height), angle) = cv2.minAreaRect(contours[label_contour])
    min_rect = ((x, y), (width + extra_border, height + extra_border), angle)
    label_crop = crop_rotated_rectangle(img_bottom_left, min_rect)
    if label_crop.shape[0] > label_crop.shape[1]:
        label_crop = cv2.rotate(label_crop, cv2.ROTATE_90_CLOCKWISE)

    return label_crop