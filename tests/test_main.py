from pathlib import Path

import numpy as np
from PIL import Image

from diffugen.rendering import contrast_img, save_tile, tile_img
from diffugen.simulation import lap5, reaction_diffusion


def test_lap5_on_known_matrix():
  field = np.arange(9, dtype=np.float64).reshape(3, 3)
  expected = np.array([
    [12, 9, 6],
    [3, 0, -3],
    [-6, -9, -12],
  ], dtype=np.float64)

  np.testing.assert_array_equal(lap5(field, 1), expected)


def test_lap5_wraps_across_boundaries():
  field = np.zeros((3, 3))
  field[0, 0] = 1
  expected = np.array([
    [-4, 1, 1],
    [1, 0, 0],
    [1, 0, 0],
  ])

  np.testing.assert_array_equal(lap5(field, 1), expected)


def test_reaction_diffusion_small_simulation():
  rng = np.random.default_rng(42)
  A, B = reaction_diffusion(
    0.2, 0.1, 0.025, 0.056, n=8, nt=5, rng=rng
  )

  assert A.shape == (8, 8)
  assert B.shape == (8, 8)
  assert np.issubdtype(A.dtype, np.floating)
  assert np.issubdtype(B.dtype, np.floating)
  assert np.isfinite(A).all()
  assert np.isfinite(B).all()
  assert np.all((0 <= A) & (A <= 1))
  assert np.all((0 <= B) & (B <= 1))


def test_reaction_diffusion_is_deterministic_with_seeded_generators():
  kwargs = {'n': 8, 'nt': 5}
  first = reaction_diffusion(
    0.2, 0.1, 0.025, 0.056, rng=np.random.default_rng(42), **kwargs
  )
  second = reaction_diffusion(
    0.2, 0.1, 0.025, 0.056, rng=np.random.default_rng(42), **kwargs
  )

  np.testing.assert_array_equal(first[0], second[0])
  np.testing.assert_array_equal(first[1], second[1])


def test_contrast_img_applies_expected_colors(tmp_path: Path):
  source_path = tmp_path / 'source.png'
  output_path = tmp_path / 'nested' / 'contrasted.png'
  source = np.array([
    [[127, 127, 127, 64], [128, 128, 128, 192]],
  ], dtype=np.uint8)
  Image.fromarray(source).save(source_path)

  contrast_img(
    source_path,
    output_path,
    light_color=(10, 20, 30),
    dark_color=(200, 210, 220),
  )

  with Image.open(output_path) as output_image:
    actual = np.array(output_image)
  expected = np.array([
    [[200, 210, 220, 64], [10, 20, 30, 192]],
  ], dtype=np.uint8)
  assert actual.dtype == np.uint8
  np.testing.assert_array_equal(actual, expected)


def test_tile_img_repeats_source_pixels(tmp_path: Path):
  source_path = tmp_path / 'source.png'
  output_path = tmp_path / 'nested' / 'tiled.png'
  source = np.array([
    [[255, 0, 0, 255], [0, 255, 0, 255]],
    [[0, 0, 255, 255], [255, 255, 0, 255]],
  ], dtype=np.uint8)
  Image.fromarray(source).save(source_path)

  tile_img(source_path, output_path, scale_factor=3)

  with Image.open(output_path) as output_image:
    actual = np.array(output_image)
  expected = np.tile(source, (3, 3, 1))
  assert actual.shape == (6, 6, 4)
  assert actual.dtype == np.uint8
  np.testing.assert_array_equal(actual, expected)


def test_save_tile_renders_tiny_matrix(tmp_path: Path):
  output_path = tmp_path / 'rendered.png'
  matrix = np.array([
    [0.0, 0.25],
    [0.75, 1.0],
  ], dtype=np.float64)

  save_tile(matrix, output_path, 'binary')

  with Image.open(output_path) as output_image:
    actual = np.array(output_image)
    assert output_image.mode == 'RGBA'
    assert output_image.width > matrix.shape[1]
    assert output_image.height > matrix.shape[0]
  assert actual.dtype == np.uint8
