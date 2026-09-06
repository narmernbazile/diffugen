from dataclasses import dataclass

import numpy as np

from diffugen.simulation import reaction_diffusion


@dataclass(frozen=True)
class Preset:
  name: str
  da: float
  db: float
  feed: float
  kill: float

  def simulate(self, **kwargs) -> tuple[np.ndarray, np.ndarray]:
    return reaction_diffusion(
      self.da, self.db, self.feed, self.kill, **kwargs
    )


PRESETS = {
  'standard': Preset('standard', da=0.20, db=0.10, feed=0.025, kill=0.056),
  'texture': Preset('texture', da=0.55, db=0.08, feed=0.027, kill=0.040),
  'circles': Preset('circles', da=0.10, db=0.20, feed=0.025, kill=0.056),
  'eggs': Preset('eggs', da=0.30, db=0.10, feed=0.027, kill=0.040),
  'big_eggs': Preset('big_eggs', da=0.10, db=0.20, feed=0.025, kill=0.040),
}


def get_preset(name: str) -> Preset:
  return PRESETS[name]


def eggs(seed: int | None = 0) -> tuple[np.ndarray, np.ndarray]:
  return get_preset('eggs').simulate(seed=seed)


def standard(seed: int | None = 0) -> tuple[np.ndarray, np.ndarray]:
  return get_preset('standard').simulate(seed=seed)


def circles(seed: int | None = 0) -> tuple[np.ndarray, np.ndarray]:
  return get_preset('circles').simulate(seed=seed)


def texture(seed: int | None = 0) -> tuple[np.ndarray, np.ndarray]:
  return get_preset('texture').simulate(seed=seed)


def big_eggs(seed: int | None = 0) -> tuple[np.ndarray, np.ndarray]:
  return get_preset('big_eggs').simulate(seed=seed)
