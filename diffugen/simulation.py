import numpy as np


DEFAULT_SIZE = 64
DEFAULT_SPACING = 2
DEFAULT_STEPS = 20000
DEFAULT_TIMESTEP = 1
DEFAULT_SEED = 0


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
                        n: int   = DEFAULT_SIZE,      # number of cells; nxn
                        h: int   = DEFAULT_SPACING,   # approximation interval
                       nt: int   = DEFAULT_STEPS,     # number of timesteps
                       dt: float = DEFAULT_TIMESTEP,  # magnitude of each timestep
                       seed: int | None = DEFAULT_SEED,
                       rng: np.random.Generator | None = None,
                        ) -> tuple[np.ndarray, np.ndarray]:
  
  # initalized concentrations of chemicals A and B represented as nxn matrices
  A = np.ones((n, n), dtype='float64')
  B = np.zeros((n, n), dtype='float64')

  # initial concentrations at center 3x3 grid
  low = (n // 2) - 1
  high = (n // 2) + 2
  if rng is None:
    rng = np.random.default_rng(seed)
  A[low:high, low:high] = 0.50 + rng.uniform(0, 0.1, (3, 3))
  B[low:high, low:high] = 0.25 + rng.uniform(0, 0.1, (3, 3))

  # iterate nt timesteps.
  for _ in range(nt):
    ABB = A * B * B
    A += (da * lap5(A, h*h) - ABB + F * (1 - A)) * dt
    B += (db * lap5(B, h*h) + ABB - B * (F + k)) * dt

  return A, B
