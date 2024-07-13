from typing import Sequence, TypeAlias

import cv2
import matplotlib.pyplot as plt
import numpy as np

SegmentOnOff: TypeAlias = Sequence[int]


class SegmentStates:
    def __init__(self, initial_vals: SegmentOnOff | None = None) -> None:
        if initial_vals is not None and len(initial_vals) != 7:
            raise ValueError(
                "The Number of segment state is 7,"
                f"but {len(initial_vals)} were entered."
            )
        self.states = [0] * 7 if initial_vals is None else list(initial_vals)

    def turn_on(self, idx: int) -> "SegmentStates":
        self.states[idx] = 1
        return self

    def all_turn_off(self) -> "SegmentStates":
        self.states = [0] * 7
        return self

    def cvt_digit(self) -> int | None:
        try:
            digit = SEGMENT_DIGITS[tuple(self.states)]
        except KeyError as e:
            print(e)
            print("Instead, returned None.")
            digit = None
        return digit


SEGMENT_DIGITS: dict[SegmentOnOff, int] = {
    (1, 1, 1, 1, 1, 1, 0): 0,
    (0, 1, 1, 0, 0, 0, 0): 1,
    (1, 1, 0, 1, 1, 0, 1): 2,
    (1, 1, 1, 1, 0, 0, 1): 3,
    (0, 1, 1, 0, 0, 1, 1): 4,
    (1, 0, 1, 1, 0, 1, 1): 5,
    (1, 0, 1, 1, 1, 1, 1): 6,
    (1, 1, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9,
}


SEGMENT_LOCATIONS = {
    0: (0, 1),
    1: (1, 2),
    2: (3, 2),
    3: (4, 1),
    4: (3, 0),
    5: (1, 0),
    6: (2, 1),
}


def show_grid_img(digit_img: np.ndarray, num_col: int, num_row: int) -> None:
    height, width = digit_img.shape[:2]
    img = digit_img[0 : height - 1, 0 : width - 1]
    grid_splited_imgs = grid_split_array(img, num_col, num_row)

    fig = plt.figure(figsize=(3, 5))
    seg_locs = set(SEGMENT_LOCATIONS.values())
    print(seg_locs)
    axes = fig.subplots(5, 5)
    for h_step, v_imgs in enumerate(grid_splited_imgs):
        for v_step, _img in enumerate(v_imgs):
            if (h_step, v_step) in seg_locs:
                print(h_step, v_step)
                if len(_img.shape) != 2:
                    _img = _img[:, :, 0]
                axes[h_step, v_step].imshow(_img)  # type: ignore
            axes[h_step, v_step].set_title(  # type: ignore
                f"({h_step}, {v_step})"
            )
            axes[h_step, v_step].set_axis_off()  # type: ignore
    fig.tight_layout()


def grid_split_array(
    arr: np.ndarray, num_col: int, num_row: int
) -> list[list[np.ndarray]]:
    """Split array into a grid

    Args:
        arr (np.ndarray): A source array.
        num_col (int): Number of horizontal divisions.
        num_row (int): Number of vertical divisions.

    Returns:
        list[list[np.ndarray]]: Outer list is collection of horizontal split
    """
    row_arrays = np.array_split(arr, num_row, axis=0)
    col_row_arrays = [
        np.array_split(row_array, num_col, axis=1) for row_array in row_arrays
    ]
    return col_row_arrays


def estimate_digit(digit_img: np.ndarray) -> int | None:
    num_horizontal_split = 5
    num_vertical_split = 3
    grid_splited_imgs = grid_split_array(
        digit_img, num_horizontal_split, num_vertical_split
    )
    segment_states = SegmentStates()
    area_threshold = 0.2
    for segment_idx, (i, j) in SEGMENT_LOCATIONS.items():
        _img = grid_splited_imgs[i][j]
        if _img.ndim != 2:
            _img = _img[:, :, 0]
        nonzero_area = np.count_nonzero(_img)
        img_area = _img.size
        filling_ratio = nonzero_area / img_area
        if filling_ratio >= area_threshold:
            segment_states.turn_on(segment_idx)
    return segment_states.cvt_digit()


def main() -> None:
    img = cv2.imread("./data/processed_images/processed_sample_pad.png")
    h_img, w_img = img.shape[:2]
    print(h_img, w_img)
    num_digit = 3
    num_horizontal_split = 3
    num_vertical_split = 5

    imgs = np.array_split(img, num_digit, axis=1)
    img = imgs[2]
    grid_splited_imgs = grid_split_array(
        img, num_horizontal_split, num_vertical_split
    )
    plt.imshow(img, "gray")
    plt.show()

    segment_states = SegmentStates()
    area_threshold = 0.2
    for segment_idx, (i, j) in SEGMENT_LOCATIONS.items():
        _img = grid_splited_imgs[i][j]
        if _img.ndim != 2:
            _img = _img[:, :, 0]
        nonzero_area = np.count_nonzero(_img)
        img_area = _img.size
        filling_ratio = nonzero_area / img_area
        if filling_ratio >= area_threshold:
            segment_states.turn_on(segment_idx)

    print("Estimated digit: ", segment_states.cvt_digit())


if __name__ == "__main__":
    main()
