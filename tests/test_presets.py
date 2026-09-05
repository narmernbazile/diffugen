import pytest

from diffugen.presets import PRESETS, get_preset


def test_preset_lookup_exposes_named_parameters():
  standard = get_preset('standard')

  assert standard.name == 'standard'
  assert standard.da == pytest.approx(0.20)
  assert standard.db == pytest.approx(0.10)
  assert standard.feed == pytest.approx(0.025)
  assert standard.kill == pytest.approx(0.056)
  assert tuple(PRESETS) == (
    'standard', 'texture', 'circles', 'eggs', 'big_eggs'
  )
