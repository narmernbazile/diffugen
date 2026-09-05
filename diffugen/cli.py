import argparse
import tempfile
from collections.abc import Sequence
from pathlib import Path

import numpy as np

from diffugen.presets import PRESETS, Preset, get_preset
from diffugen.simulation import DEFAULT_SEED, DEFAULT_SIZE, DEFAULT_STEPS


DEFAULT_SCALE = 9
DEFAULT_OUTPUT_DIR = Path('.rd')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def positive_int(value: str) -> int:
  parsed = int(value)
  if parsed < 1:
    raise argparse.ArgumentTypeError('must be at least 1')
  return parsed


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    prog='diffugen',
    description='Generate tiled Gray-Scott reaction-diffusion art.',
  )
  selection = parser.add_mutually_exclusive_group()
  selection.add_argument('--preset', choices=PRESETS)
  selection.add_argument(
    '--all-presets', action='store_true',
    help='generate every preset (the default when no preset is selected)',
  )
  selection.add_argument(
    '--list-presets', action='store_true',
    help='print available preset names and exit',
  )
  parser.add_argument('--size', type=positive_int, default=DEFAULT_SIZE)
  parser.add_argument('--steps', type=positive_int, default=DEFAULT_STEPS)
  parser.add_argument('--scale', type=positive_int, default=DEFAULT_SCALE)
  parser.add_argument('--seed', type=int, default=DEFAULT_SEED)
  parser.add_argument('--output', type=Path, help='final image path for one preset')
  parser.add_argument(
    '--output-dir', type=Path, default=DEFAULT_OUTPUT_DIR,
    help='output directory (default: .rd)',
  )
  return parser


def generate_wallpaper(preset: Preset, output_path: Path, *, size: int,
                       steps: int, scale: int, seed: int | None) -> None:
  from diffugen.rendering import contrast_img, save_tile, tile_img

  rng = np.random.default_rng(seed)
  A, B = preset.simulate(n=size, nt=steps, rng=rng)
  with tempfile.TemporaryDirectory() as directory:
    temporary_dir = Path(directory)
    tile_path = temporary_dir / 'tile.png'
    processed_path = temporary_dir / 'processed_tile.png'
    save_tile(A, tile_path, 'binary')
    contrast_img(tile_path, processed_path, BLACK, WHITE)
    tile_img(processed_path, output_path, scale)


def generate_all(output_dir: Path, *, size: int, steps: int,
                 scale: int, seed: int | None) -> None:
  from diffugen.rendering import contrast_img, save_tile, tile_img

  output_dir.mkdir(parents=True, exist_ok=True)
  for idx, preset in enumerate(PRESETS.values()):
    rng = np.random.default_rng(seed)
    A, B = preset.simulate(n=size, nt=steps, rng=rng)
    tile_path = output_dir / f'_tile{idx}.png'
    processed_path = output_dir / f'_processed_tile{idx}.png'
    save_tile(A, tile_path, 'binary')
    contrast_img(tile_path, processed_path, BLACK, WHITE)
    tile_img(processed_path, output_dir / f'wallpaper{idx}.png', scale)


def main(argv: Sequence[str] | None = None) -> int:
  parser = build_parser()
  args = parser.parse_args(argv)

  if args.list_presets:
    print('\n'.join(PRESETS))
    return 0

  if args.preset:
    output_path = args.output or args.output_dir / f'{args.preset}.png'
    generate_wallpaper(
      get_preset(args.preset), output_path,
      size=args.size, steps=args.steps, scale=args.scale, seed=args.seed,
    )
    return 0

  if args.output:
    parser.error('--output requires --preset')

  generate_all(
    args.output_dir,
    size=args.size, steps=args.steps, scale=args.scale, seed=args.seed,
  )
  return 0
