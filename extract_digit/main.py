import re
from pathlib import Path

import cv2
import matplotlib.pyplot as plt

from extract_digit.estimate_digit import estimate_digits_from_image
from extract_digit.param_config import Configurations
from extract_digit.processing import (
    binalize_image,
    crop_transform_show_digits,
    fill_contours,
    filtering_digit_contours,
    find_contours,
    pad_image,
    remove_image_margins,
)
from extract_digit.utils import (
    select_directory_with_window,
    select_img_with_window,
)


def run_one_file(img_path: str | Path, is_imshow: bool = False) -> list[str]:
    config_path = "extract_digit/configs/config.json"
    cfg = Configurations.load_json(config_path)
    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)

    cropped_img = crop_transform_show_digits(
        src=img,
        crop_area_vertices=cfg.crop_transform.crop_area_vertices,
        dst_size=cfg.crop_transform.dst_size,
        imshow=cfg.crop_transform.imshow,
        close_up_area=cfg.crop_transform.close_up_area,
    )

    binalized_img = binalize_image(
        img=cropped_img,
        gb_ksize=cfg.binalize.gb_ksize,
        gb_sigmaX=cfg.binalize.gb_sigmaX,
        epf_sigma_s=cfg.binalize.epf_sigma_s,
        epf_sigma_r=cfg.binalize.epf_sigma_r,
        adaptive_thresh_blocksize=cfg.binalize.adaptive_thresh_blocksize,
        adaptive_thresh_C=cfg.binalize.adaptive_thresh_C,
    )

    contours = find_contours(binalized_img)

    contours = filtering_digit_contours(
        contours,
        cropped_img,
        bb_filling_ratio=cfg.filtering_digit.bb_filling_ratio,
        bb_image_ratio=cfg.filtering_digit.bb_image_ratio,
        inner_aspect_range=cfg.filtering_digit.inner_aspect_range,
    )
    digits_area = fill_contours(cropped_img, contours)

    removed_margins = remove_image_margins(digits_area)
    added_pad_img = pad_image(removed_margins)
    digits = estimate_digits_from_image(
        added_pad_img, cfg.estimation, is_imshow
    )
    print(digits)

    if is_imshow:
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.imshow(removed_margins)
        plt.show()

    return digits


def run_on_directory(src_dir: str | Path, dst_dir: str | Path) -> None:
    src_dir = Path(src_dir)
    # Select image file paths and sort
    img_paths = sorted(
        [
            p
            for p in src_dir.iterdir()
            if re.search(r"^.*\.(jpg|png|JPEG)$", p.name)
        ]
    )
    # Extract digits from each image
    digits_eash_image = [[p.stem] + run_one_file(p) for p in img_paths]

    dst_dir = Path(dst_dir)
    with open(dst_dir / "measured_lux_progress.csv", "x") as f:
        f.write("img_name,4th-digit,3rd-digit,2nd-digit,1st-digit\n")
        f.writelines([",".join(digits) + "\n" for digits in digits_eash_image])


if __name__ == "__main__":
    while True:
        all_or_one = input(
            "For a single file? [0], for a directory? [1] or exit? [-1]: "
        )
        if all_or_one == "0":
            src_path = select_img_with_window()
            run_one_file(src_path, is_imshow=True)
        elif all_or_one == "1":
            src_dir = select_directory_with_window()
            dst_dir = select_directory_with_window()
            run_on_directory(src_dir, dst_dir)
        elif all_or_one == "-1":
            print("Exit")
            break
        else:
            print(
                f"Expected '0', '1' or '-1', but '{all_or_one}' was entered. ",
                "Please enter again.",
            )
            continue
