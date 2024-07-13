import cv2
import cv2.typing as cv2t
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon


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
        _type_: _description_
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
