from typing import Sequence

import cv2.typing as cv2t
from pydantic import BaseModel


class CropTransformParams(BaseModel):
    pnts: Sequence[Sequence[int]]
    dstsize: cv2t.Size
    imshow: bool = False
    roi: Sequence[int] | None = None
    close_up_area: Sequence[Sequence[int]] | None = None


class BinalizeParams(BaseModel):
    gb_ksize: cv2t.Size
    gb_sigmaX: float
    epf_sigma_s: float
    epf_sigma_r: float
    adaptive_thresh_blocksize: int
    adaptive_thresh_C: int
    closing_ksize: cv2t.Size


class FilteringDigitParams(BaseModel):
    bb_filling_ratio: float
    bb_image_ratio: float
    inner_aspect_range: Sequence[float]
