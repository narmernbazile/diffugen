# Diffugen examples

These examples are a small, reproducible cross-section of Diffugen's built-in
presets. All four use a 64-by-64 simulation, seed 42, and a three-by-three tile
layout. The preset-specific step counts were selected to show each pattern at
an interesting stage of its development.

| Image | Preset | Steps | Reproduction command |
| --- | --- | ---: | --- |
| [standard-seed-42.png](standard-seed-42.png) | `standard` | 20,000 | `python -m diffugen --preset standard --size 64 --steps 20000 --scale 3 --seed 42 --output examples/standard-seed-42.png` |
| [texture-seed-42.png](texture-seed-42.png) | `texture` | 12,000 | `python -m diffugen --preset texture --size 64 --steps 12000 --scale 3 --seed 42 --output examples/texture-seed-42.png` |
| [eggs-seed-42.png](eggs-seed-42.png) | `eggs` | 5,000 | `python -m diffugen --preset eggs --size 64 --steps 5000 --scale 3 --seed 42 --output examples/eggs-seed-42.png` |
| [big-eggs-seed-42.png](big-eggs-seed-42.png) | `big_eggs` | 5,000 | `python -m diffugen --preset big_eggs --size 64 --steps 5000 --scale 3 --seed 42 --output examples/big-eggs-seed-42.png` |

Generated scratch output belongs in `generated/`, which is intentionally
ignored by Git. The images in this directory are curated project assets rather
than a general output directory.

## Custom parameter studies

The following five images were selected from a 50-image parameter sweep. Their
names describe the resulting forms; they are not additional built-in presets.
Like the preset gallery, each uses a 64-by-64 simulation and a three-by-three
tile layout.

| Image | `da` | `db` | Feed (`F`) | Kill (`k`) | Steps | Seed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [capsules-seed-1002.png](capsules-seed-1002.png) | 0.12 | 0.06 | 0.022 | 0.051 | 9,000 | 1002 |
| [lattice-seed-1009.png](lattice-seed-1009.png) | 0.16 | 0.08 | 0.038 | 0.061 | 6,000 | 1009 |
| [mosaic-seed-1014.png](mosaic-seed-1014.png) | 0.20 | 0.08 | 0.038 | 0.061 | 9,000 | 1014 |
| [contours-seed-1031.png](contours-seed-1031.png) | 0.36 | 0.12 | 0.018 | 0.047 | 12,000 | 1031 |
| [fingerprint-seed-1041.png](fingerprint-seed-1041.png) | 0.48 | 0.10 | 0.018 | 0.047 | 6,000 | 1041 |

To reproduce the custom studies, run this from the repository root after
installing Diffugen:

```python
from pathlib import Path

from diffugen.cli import generate_wallpaper
from diffugen.presets import Preset

studies = [
    ('capsules', 0.12, 0.06, 0.022, 0.051, 9000, 1002),
    ('lattice', 0.16, 0.08, 0.038, 0.061, 6000, 1009),
    ('mosaic', 0.20, 0.08, 0.038, 0.061, 9000, 1014),
    ('contours', 0.36, 0.12, 0.018, 0.047, 12000, 1031),
    ('fingerprint', 0.48, 0.10, 0.018, 0.047, 6000, 1041),
]

for name, da, db, feed, kill, steps, seed in studies:
    parameters = Preset(name, da=da, db=db, feed=feed, kill=kill)
    generate_wallpaper(
        parameters,
        Path('examples') / f'{name}-seed-{seed}.png',
        size=64,
        steps=steps,
        scale=3,
        seed=seed,
    )
```
