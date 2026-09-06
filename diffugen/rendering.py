from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def save_tile(matrix: np.ndarray, out_img_path: str | Path, cmap: str) -> None:
  out_img_path = Path(out_img_path)
  out_img_path.parent.mkdir(parents=True, exist_ok=True)
  fig, ax = plt.subplots(tight_layout=True)
  ax.axis('off')
  ax.imshow(matrix, interpolation='lanczos', cmap=cmap)
  try:
    fig.savefig(out_img_path, bbox_inches='tight', pad_inches=0)
  finally:
    plt.close(fig)


def contrast_img(in_img_path: str | Path, out_img_path: str | Path,
                 light_color: tuple[int, int, int],
                 dark_color: tuple[int, int, int]) -> None:
  with Image.open(in_img_path) as input_image:
    image_array = np.array(input_image.convert('RGBA'), dtype=np.uint8)

  light = np.asarray(light_color, dtype=np.uint8)
  dark = np.asarray(dark_color, dtype=np.uint8)
  image_array[..., :3] = np.where(image_array[..., :3] > 255//2, light, dark)

  output_image = Image.fromarray(image_array)
  out_img_path = Path(out_img_path)
  out_img_path.parent.mkdir(parents=True, exist_ok=True)
  output_image.save(out_img_path)
  output_image.close()
def tile_img(in_img_path: str | Path, out_img_path: str | Path,
             scale_factor: int) -> None:
  with Image.open(in_img_path) as input_image:
    input_array = np.array(input_image.convert('RGBA'), dtype=np.uint8)
  output_array = np.tile(input_array, (scale_factor, scale_factor, 1))

  output_image = Image.fromarray(output_array)
  out_img_path = Path(out_img_path)
  out_img_path.parent.mkdir(parents=True, exist_ok=True)
  output_image.save(out_img_path)
  output_image.close()
