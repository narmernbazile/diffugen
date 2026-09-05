from pathlib import Path

from diffugen.presets import big_eggs, circles, eggs, standard, texture
from diffugen.rendering import contrast_img, save_tile, tile_img


def main() -> None:
  WHITE = (255, 255, 255)
  BLACK = (0, 0, 0)
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
