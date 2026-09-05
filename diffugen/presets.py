import numpy as np

from diffugen.simulation import reaction_diffusion


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
