from typing import Sequence, overload

import cv2
import cv2.typing as cv2t
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Polygon
from pydantic import BaseModel


class BoundingBox(BaseModel):
    left: int
    right: int
    top: int
    bottom: int

    @staticmethod
    def _get_bounding_box(img: cv2t.MatLike) -> "BoundingBox":
        nonzero = np.argwhere(img != 0)
        top, left = np.min(nonzero, 0)
        bottom, right = np.max(nonzero, 0)
        return BoundingBox(left=left, right=right, top=top, bottom=bottom)


def crop_transform_show_digits(
    src: cv2t.MatLike,
    pnts: tuple[tuple[int, int], ...],
    dstsize: tuple[int, int],
    *,
    imshow: bool = False,
    roi: tuple[int, int, int, int] | None = None,
    close_up_area: tuple[tuple[int, int], tuple[int, int]] | None = None,
) -> cv2t.MatLike:
    """Crops and rectifies a target area of an image to a rectangle

    Args:
        src (cv2t.MatLike): A source image.
        pnts (tuple[tuple[int, int], ...]): Each vertex of the area to be cropped. The order is clockwise.
        dstsize (tuple[int, int]): Image size after rectangle correction.
        imshow (bool, optional): Whether to compare images before and after conversion.  Defaults to False.
        roi (tuple[int, int, int, int] | None, optional): _description_. Defaults to None.
        close_up_area (tuple[tuple[int, int], tuple[int, int]] | None, optional): _description_. Defaults to None.

    Returns:
        cv2t.MatLike: Cropped and corrected image.
    """  # noqa: E501
    pts1 = np.array(pnts, np.float32)
    height, width = dstsize
    pts2 = np.array(
        [[0, 0], [width, 0], [width, height], [0, height]], np.float32
    )

    trans_mat = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(src, trans_mat, (width, height))

    if imshow:
        fig, ax = plt.subplots(1, 2, figsize=(16, 6))
        fig = plt.figure(figsize=(16, 6))
        if roi is None:
            xmin, ymin = 0, 0
            ymax, xmax = src.shape
        else:
            xmin, xmax, ymin, ymax = roi
        ax = fig.add_subplot(1, 2, 1)
        ax.imshow(
            # src[ymin : ymax + 1, xmin : xmax + 1],
            src,
            cmap=plt.get_cmap("Greys_r"),
            extent=(xmin - 0.5, xmax + 0.5, ymax + 0.5, ymin - 0.5),
        )
        ax.add_patch(Polygon(pnts, fc="None", ec="red", alpha=0.5))
        if close_up_area is not None:
            ax.set_xlim(close_up_area[0])
            ax.set_ylim(close_up_area[1][::-1])
            ax.set_xticks(
                np.arange(close_up_area[0][0], close_up_area[0][1], 50),
                minor=True,
            )
            ax.set_yticks(
                np.arange(close_up_area[1][0], close_up_area[1][1], 50),
                minor=True,
            )
        ax = fig.add_subplot(1, 2, 1)
        ax.imshow(dst, cmap=plt.get_cmap("Greys_r"))

    return dst


def binalize_image(
    img: cv2t.MatLike,
    gb_ksize: cv2t.Size = (15, 15),
    gb_sigmaX: float = 2,
    epf_sigma_s: float = 110,
    epf_sigma_r: float = 0.01,
    adaptive_thresh_blocksize: int = 301,
    adaptive_thresh_C: int = 1,
    closing_ksize: cv2t.Size = (3, 3),
) -> cv2t.MatLike:
    blured = cv2.GaussianBlur(img, ksize=gb_ksize, sigmaX=gb_sigmaX)
    blured = cv2.edgePreservingFilter(
        blured, sigma_s=epf_sigma_s, sigma_r=epf_sigma_r
    )
    binary = cv2.adaptiveThreshold(
        blured,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        adaptive_thresh_blocksize,
        adaptive_thresh_C,
    )
    kernel = np.ones(closing_ksize, np.uint8)
    close = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    return close


@overload
def find_contours(
    src_img: cv2t.MatLike,
) -> Sequence[cv2.typing.MatLike]: ...
@overload
def find_contours(
    src_img: cv2t.MatLike,
    base_img: cv2t.MatLike,
) -> tuple[Sequence[cv2.typing.MatLike], Figure]: ...
def find_contours(
    src_img: cv2t.MatLike,
    base_img: cv2t.MatLike | None = None,
) -> (
    Sequence[cv2.typing.MatLike] | tuple[Sequence[cv2.typing.MatLike], Figure]
):
    contours = cv2.findContours(
        src_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )[0]
    if base_img is not None:
        fig = plt.figure()
        ax = fig.add_subplot()
        drawing = cv2.cvtColor(base_img, cv2.COLOR_GRAY2RGB)
        for i, contour in enumerate(contours):
            x, y, width, height = cv2.boundingRect(contour)
            aspect = _calc_aspect(width, height)
            cv2.rectangle(
                drawing, (x, y), (x + width, y + height), (0, 255, 0)
            )
            cv2.putText(
                drawing,
                f"{aspect:.2f}",
                (x, y),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(0, 255, 0),
            )
            drawing = cv2.drawContours(drawing, contours, i, (255, 0, 0))
        ax.imshow(drawing)
        return contours, fig
    return contours


def _is_over_area(contour: cv2t.MatLike, area: float) -> bool:
    judge = abs(cv2.contourArea(contour, True)) > area
    return judge


def _calc_aspect(width: int, height: int) -> float:
    return max(width, height) / min(width, height)


def _is_inner_aspect(
    contour: cv2t.MatLike, min_aspect: float, max_aspect: float
) -> bool:
    _, _, w, h = cv2.boundingRect(contour)
    aspect = _calc_aspect(w, h)
    return aspect < max_aspect and aspect > min_aspect


def _calc_bb_fill_ratio(contour: cv2t.MatLike) -> float:
    _, _, w, h = cv2.boundingRect(contour)
    contour_area = abs(cv2.contourArea(contour, True))
    return contour_area / (w * h)


def _calc_bb_img_ratio(contour: cv2t.MatLike, img: cv2t.MatLike) -> float:
    h, w = img.shape[:2]
    contour_area = abs(cv2.contourArea(contour, True))
    return contour_area / (h * w)


def _is_longer_than_width(contour: cv2t.MatLike) -> bool:
    _, _, w, h = cv2.boundingRect(contour)
    return h > w


def filtering_digit_contours(
    contours: Sequence[cv2t.MatLike],
    src_img: cv2t.MatLike,
    bb_filling_ratio: float = 0.3,
    bb_image_ratio: float = 3e-3,
    inner_aspect_range: Sequence[float] = (1.3, 6),
) -> Sequence[cv2t.MatLike]:
    extracted_contours = list(
        filter(
            lambda x: _is_longer_than_width(x)
            and _calc_bb_fill_ratio(x) > bb_filling_ratio
            and _calc_bb_img_ratio(x, src_img) > bb_image_ratio
            and _is_inner_aspect(
                x, inner_aspect_range[0], inner_aspect_range[1]
            ),
            contours,
        )
    )
    return extracted_contours


def draw_contours(
    src_img: cv2t.MatLike, contours: Sequence[cv2t.MatLike]
) -> Figure:
    fig = plt.figure()
    ax = fig.add_subplot()
    drawing_canvas = cv2.cvtColor(src_img, cv2.COLOR_GRAY2RGB)
    for i in range(len(contours)):
        drawing_canvas = cv2.drawContours(
            drawing_canvas, contours, i, (255, 0, 0)
        )
    ax.imshow(drawing_canvas)
    return fig


def sort_digit_contours(
    contours: Sequence[cv2t.MatLike],
) -> Sequence[cv2t.MatLike]:
    return sorted(contours, key=lambda x: np.squeeze(x)[:, 0].min())


def remove_image_margins(img: cv2t.MatLike) -> cv2t.MatLike:
    bb = BoundingBox._get_bounding_box(img)
    return img.copy()[bb.top : bb.bottom, bb.left : bb.right]


def pad_image(
    img: cv2t.MatLike, pad_size: Sequence[int] | None = None
) -> cv2t.MatLike:
    if pad_size is None:
        h, w = img.shape[:2]
        pad_size_h = h // 20
        pad_size_w = w // 20
    else:
        pad_size_h = pad_size[0]
        pad_size_w = pad_size[1]

    padding = cv2.copyMakeBorder(
        img,
        pad_size_h,
        pad_size_h,
        pad_size_w,
        pad_size_w,
        cv2.BORDER_CONSTANT,
        value=(0, 0, 0),
    )
    return padding