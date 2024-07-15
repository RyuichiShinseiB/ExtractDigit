from pathlib import Path
from typing import Literal, NamedTuple

import cv2.typing as cv2t
import numpy as np
from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    left: int = Field(ge=0)
    right: int = Field(ge=0)
    top: int = Field(ge=0)
    bottom: int = Field(ge=0)

    @staticmethod
    def get_bounding_box(img: cv2t.MatLike) -> "BoundingBox":
        nonzero = np.argwhere(img != 0)
        top, left = np.min(nonzero, 0)
        bottom, right = np.max(nonzero, 0)
        return BoundingBox(left=left, right=right, top=top, bottom=bottom)

    def unpack(self) -> tuple[int, int, int, int]:
        """Unpacking position

        Returns:
            tuple[int, int, int, int]: (left, right, top, bottom)
        """
        return self.left, self.right, self.top, self.bottom


class Point(NamedTuple):
    x: int
    y: int

    def to_tuple(self, order: Literal["xy", "yx"] = "xy") -> tuple[int, int]:
        """Converts to tuple

        Args:
            order (Literal["xy", "yx"], optional): the order of x and y. Defaults to "xy".

        Raises:
            KeyError: If an order other than xy or yx is entered, this error is raised.

        Returns:
            tuple[int, int]: order=="xy" -> (x, y). order=="yx" -> (y, x)
        """  # noqa: E501
        if order == "xy":
            return (self.x, self.y)
        elif order == "yx":
            return (self.y, self.x)
        raise KeyError("`Order` is 'xy' or 'yx'")


class QuadrilateralVertices(BaseModel):
    upper_left: Point
    upper_right: Point
    lower_left: Point
    lower_right: Point

    def align_vertices(
        self,
    ) -> tuple[
        tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]
    ]:
        """Align vertices.

        Returns:
            tuple[tuple[int, int] x 4]: Vertex is (x, y). (upper left, upper right, lower right, lower left)
        """  # noqa: E501
        return (
            self.upper_left.to_tuple(),
            self.upper_right.to_tuple(),
            self.lower_right.to_tuple(),
            self.lower_left.to_tuple(),
        )


class RangeTuple(NamedTuple):
    minimum: float
    maximum: float

    def to_tuple(self) -> tuple[float, float]:
        return self.minimum, self.maximum


class CropTransformParams(BaseModel):
    crop_area_vertices: QuadrilateralVertices
    dst_size: tuple[int, int]
    imshow: bool = False
    close_up_area: BoundingBox = BoundingBox(
        left=1900, right=2450, top=1600, bottom=1950
    )


class BinalizeParams(BaseModel):
    gb_ksize: tuple[int, int]
    gb_sigmaX: float
    epf_sigma_s: float
    epf_sigma_r: float
    adaptive_thresh_blocksize: int
    adaptive_thresh_C: int
    closing_ksize: tuple[int, int]


class FilteringDigitParams(BaseModel):
    bb_filling_ratio: float
    bb_image_ratio: float
    inner_aspect_range: RangeTuple


class EstimationParams(BaseModel):
    aspect_thresh: float
    three_digits_aspect: float
    filling_area_ratio_thresh: float


class Configurations(BaseModel):
    crop_transform: CropTransformParams
    binalize: BinalizeParams
    filtering_digit: FilteringDigitParams

    @staticmethod
    def load_json(path: str | Path) -> "Configurations":
        with open(path, "r") as f:
            json_txt = f.read()
        return Configurations.model_validate_json(json_txt)
