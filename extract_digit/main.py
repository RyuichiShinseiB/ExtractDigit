import cv2
import matplotlib.pyplot as plt

from extract_digit.estimate_digit import estimate_digit
from extract_digit.param_config import Configurations
from extract_digit.processing import (
    binalize_image,
    crop_transform_show_digits,
    draw_contours,
    fill_contours,
    filtering_digit_contours,
    find_contours,
    pad_image,
    remove_image_margins,
    sort_digit_contours,
)


def main() -> None:
    config_path = "extract_digit/configs/config.json"
    cfg = Configurations.load_json(config_path)
    img_path = "data/src_images/IMG_20240708_132157_011.jpg"
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    cropped_img = crop_transform_show_digits(
        src=img,
        crop_area_vertices=cfg.crop_transform.crop_area_vertices,
        dst_size=cfg.crop_transform.dst_size,
        imshow=cfg.crop_transform.imshow,
        close_up_area=cfg.crop_transform.close_up_area,
    )
    plt.show()

    binalized_img = binalize_image(
        img=cropped_img,
        gb_ksize=cfg.binalize.gb_ksize,
        gb_sigmaX=cfg.binalize.gb_sigmaX,
        epf_sigma_s=cfg.binalize.epf_sigma_s,
        epf_sigma_r=cfg.binalize.epf_sigma_r,
        adaptive_thresh_blocksize=cfg.binalize.adaptive_thresh_blocksize,
        adaptive_thresh_C=cfg.binalize.adaptive_thresh_C,
    )
    plt.imshow(binalized_img, "gray")
    plt.show()

    contours, _ = find_contours(binalized_img, cropped_img)
    plt.show()

    contours = filtering_digit_contours(
        contours,
        cropped_img,
        bb_filling_ratio=cfg.filtering_digit.bb_filling_ratio,
        bb_image_ratio=cfg.filtering_digit.bb_image_ratio,
        inner_aspect_range=cfg.filtering_digit.inner_aspect_range,
    )
    drawing_contours = draw_contours(cropped_img, contours)
    digits_area = fill_contours(cropped_img, contours)
    plt.imshow(digits_area)
    plt.show()

    removed_margins = remove_image_margins(digits_area)
    plt.imshow(removed_margins)
    plt.show()

    pad_digits = pad_image(removed_margins)
    plt.imshow(pad_digits)
    plt.show()


if __name__ == "__main__":
    main()
