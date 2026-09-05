import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from main import contrast_img, lap5, reaction_diffusion, save_tile, tile_img


class LaplacianTests(unittest.TestCase):
  def test_constant_field_has_zero_laplacian(self):
    field = np.ones((4, 4))
    np.testing.assert_array_equal(lap5(field, 1), np.zeros((4, 4)))

  def test_stencil_wraps_across_boundaries(self):
    field = np.zeros((3, 3))
    field[0, 0] = 1

    expected = np.array([
      [-4, 1, 1],
      [1, 0, 0],
      [1, 0, 0],
    ])
    np.testing.assert_array_equal(lap5(field, 1), expected)


class SimulationTests(unittest.TestCase):
  def test_seed_reproduces_simulation(self):
    args = (0.2, 0.1, 0.025, 0.056)
    first_a, first_b = reaction_diffusion(*args, n=8, nt=3, seed=42)
    second_a, second_b = reaction_diffusion(*args, n=8, nt=3, seed=42)

    np.testing.assert_array_equal(first_a, second_a)
    np.testing.assert_array_equal(first_b, second_b)


class ImagePipelineTests(unittest.TestCase):
  def test_threshold_and_tile(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      source_path = root / 'source.png'
      threshold_path = root / 'threshold.png'
      wallpaper_path = root / 'nested' / 'wallpaper.png'
      source = np.array([
        [[0, 0, 0, 255], [255, 255, 255, 255]],
        [[127, 127, 127, 255], [128, 128, 128, 255]],
      ], dtype=np.uint8)
      Image.fromarray(source, 'RGBA').save(source_path)

      contrast_img(source_path, threshold_path, (0, 0, 0), (255, 255, 255))
      tile_img(threshold_path, wallpaper_path, 2)

      with Image.open(threshold_path) as threshold_image:
        threshold = np.array(threshold_image)
      with Image.open(wallpaper_path) as wallpaper_image:
        wallpaper = np.array(wallpaper_image)

      np.testing.assert_array_equal(threshold[0, 0, :3], [255, 255, 255])
      np.testing.assert_array_equal(threshold[0, 1, :3], [0, 0, 0])
      self.assertEqual(wallpaper.shape, (4, 4, 4))
      np.testing.assert_array_equal(wallpaper[:2, :2], threshold)
      np.testing.assert_array_equal(wallpaper[2:, 2:], threshold)

  def test_small_end_to_end_generation(self):
    with tempfile.TemporaryDirectory() as directory:
      root = Path(directory)
      tile_path = root / 'intermediate' / 'tile.png'
      processed_path = root / 'processed.png'
      wallpaper_path = root / 'wallpaper.png'
      concentrations, _ = reaction_diffusion(
        0.2, 0.1, 0.025, 0.056, n=8, nt=2, seed=7
      )

      save_tile(concentrations, tile_path, 'binary')
      contrast_img(tile_path, processed_path, (0, 0, 0), (255, 255, 255))
      tile_img(processed_path, wallpaper_path, 2)

      self.assertTrue(tile_path.is_file())
      self.assertTrue(processed_path.is_file())
      self.assertTrue(wallpaper_path.is_file())


if __name__ == '__main__':
  unittest.main()
