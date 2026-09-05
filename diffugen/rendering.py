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
    image_array = np.array(input_image.convert('RGBA'))

  for i in range(len(image_array)):
    for j in range(len(image_array[i])):
      r = image_array[i][j][0]
      g = image_array[i][j][1]
      b = image_array[i][j][2]
      a = image_array[i][j][3]

      r = light_color[0] if r > 255//2 else dark_color[0]
      g = light_color[1] if g > 255//2 else dark_color[1]
      b = light_color[2] if b > 255//2 else dark_color[2]

      image_array[i][j][0] = r
      image_array[i][j][1] = g
      image_array[i][j][2] = b
      image_array[i][j][3] = a

  output_image = Image.fromarray(image_array)
  out_img_path = Path(out_img_path)
  out_img_path.parent.mkdir(parents=True, exist_ok=True)
  output_image.save(out_img_path)
  output_image.close()


def merge_and_contrast_img(in_imgA_path: str | Path,
                           in_imgB_path: str | Path,
                           out_img_path: str | Path) -> None:
  with Image.open(in_imgA_path) as input_imageA:
    imageA_array = np.array(input_imageA.convert('RGBA'))
  with Image.open(in_imgB_path) as input_imageB:
    imageB_array = np.array(input_imageB.convert('RGBA'))
  if imageA_array.shape != imageB_array.shape:
    raise ValueError("image A and image B are different dimensions")
  height, width, _ = imageA_array.shape
  output_array = np.zeros((height, width, 4), dtype=np.uint8)
  for i in range(height):
    for j in range(width):
      output_array[i][j][0] = int(imageA_array[i][j][0])  # adopt the 'reds' from image A
      output_array[i][j][1] = 0 # don't use the green channel
      output_array[i][j][2] = int(imageB_array[i][j][2])
      output_array[i][j][3] = 255 # we want this pixel to be fully opaque 

  output_image = Image.fromarray(output_array, 'RGBA')
  out_img_path = Path(out_img_path)
  out_img_path.parent.mkdir(parents=True, exist_ok=True)
  output_image.save(out_img_path)
  output_image.close()


def tile_img(in_img_path: str | Path, out_img_path: str | Path,
             scale_factor: int) -> None:
  with Image.open(in_img_path) as input_image:
    input_array = np.array(input_image.convert('RGBA'))
  height, width, channels = input_array.shape
  output_height = scale_factor * height
  output_width = scale_factor * width
  output_array = np.zeros((output_height, output_width, channels), dtype=np.uint8)

  for i in range(output_height):
    for j in range(output_width):
      pixel = input_array[i % height][j % width]
      output_array[i][j] = pixel

  output_image = Image.fromarray(output_array)
  out_img_path = Path(out_img_path)
  out_img_path.parent.mkdir(parents=True, exist_ok=True)
  output_image.save(out_img_path)
  output_image.close()
