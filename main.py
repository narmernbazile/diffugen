#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

# source: https://github.com/wigging/gray-scott
def lap5(f: np.ndarray, h2: float) -> np.ndarray:
  """
  Use a five-point stencil with periodic boundary conditions to approximate
  the Laplacian. The corresponding array slices for each component of the
  stencil are noted.
  """
  f = np.pad(f, 1, mode='wrap')

  left   = f[1:-1, :-2]   # shift left for f(x - h, y)
  right  = f[1:-1, 2:]    # shift right for f(x + h, y)
  down   = f[2:, 1:-1]    # shift down for f(x, y - h)
  up     = f[:-2, 1:-1]   # shift up for f(x, y + h)
  center = f[1:-1, 1:-1]  # center for f(x, y)

  fxy = (left + right + down + up - 4 * center) / h2

  return fxy

# source: https://github.com/wigging/gray-scott
def reaction_diffusion(da: float, # diffusion rate for A
                       db: float, # diffusion rale for B
                        F: float, # feed rate
                        k: float, # kill rate
                        n: int   = 64,    # number of cells; nxn
                        h: int   = 2,     # approximation interval
                       nt: int   = 20000, # number of timesteps to simulate
                       dt: float = 1,     # magnitude of each timestep
                       seed: int | None = 0,
                        ) -> tuple[np.ndarray, np.ndarray]:
  
  # initalized concentrations of chemicals A and B represented as nxn matrices
  A = np.ones((n, n), dtype='float64')
  B = np.zeros((n, n), dtype='float64')

  # initial concentrations at center 3x3 grid
  low = (n // 2) - 1
  high = (n // 2) + 2
  rng = np.random.default_rng(seed)
  A[low:high, low:high] = 0.50 + rng.uniform(0, 0.1, (3, 3))
  B[low:high, low:high] = 0.25 + rng.uniform(0, 0.1, (3, 3))

  # iterate nt timesteps.
  for _ in range(nt):
    ABB = A * B * B
    A += (da * lap5(A, h*h) - ABB + F * (1 - A)) * dt
    B += (db * lap5(B, h*h) + ABB - B * (F + k)) * dt

  return A, B


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


def eggs(seed: int | None = 0) -> tuple[np.ndarray, np.ndarray]:
  return reaction_diffusion(0.30, 0.10, 0.027, 0.040, seed=seed)

def standard(seed: int | None = 0) -> tuple[np.ndarray, np.ndarray]:
  return reaction_diffusion(0.20, 0.10, 0.025, 0.056, seed=seed)

def circles(seed: int | None = 0) -> tuple[np.ndarray, np.ndarray]:
  return reaction_diffusion(0.10, 0.20, 0.025, 0.056, seed=seed)

def texture(seed: int | None = 0) -> tuple[np.ndarray, np.ndarray]:
  return reaction_diffusion(0.55, 0.08, 0.027, 0.040, seed=seed)
  
def big_eggs(seed: int | None = 0) -> tuple[np.ndarray, np.ndarray]:
  return reaction_diffusion(0.10, 0.20, 0.025, 0.040, seed=seed)

def main() -> None:
  WHITE  = (255, 255, 255)
  BLACK  = (0, 0, 0)
  output_dir = Path('.rd')
  output_dir.mkdir(parents=True, exist_ok=True)
  patterns = [standard, texture, circles, eggs, big_eggs]
  for idx, pattern in enumerate(patterns):
    A, B = pattern()
    tile_path = output_dir / f'_tile{idx}.png'
    processed_path = output_dir / f'_processed_tile{idx}.png'
    save_tile(A, tile_path, 'binary')
    contrast_img(tile_path, processed_path, BLACK, WHITE)
    tile_img(processed_path, output_dir / f'wallpaper{idx}.png', 9)
  


if __name__ == "__main__": main()
