# Diffugen

Diffugen is a small creative-coding project that turns Gray–Scott
reaction–diffusion simulations into seamless, black-and-white tiled images.

## Examples

| Standard | Texture | Eggs |
| --- | --- | --- |
| ![Standard preset: maze-like bands](examples/standard-seed-42.png) | ![Texture preset: dense textile-like pattern](examples/texture-seed-42.png) | ![Eggs preset: alternating circles and diamonds](examples/eggs-seed-42.png) |
| Big eggs | Capsules | Lattice |
| ![Big eggs preset: rings and dots](examples/big-eggs-seed-42.png) | ![Custom parameters: rounded capsules](examples/capsules-seed-1002.png) | ![Custom parameters: symmetric glyph lattice](examples/lattice-seed-1009.png) |
| Mosaic | Contours | Fingerprint |
| ![Custom parameters: cellular mosaic](examples/mosaic-seed-1014.png) | ![Custom parameters: nested contours](examples/contours-seed-1031.png) | ![Custom parameters: fingerprint-like arcs](examples/fingerprint-seed-1041.png) |

Each image is reproducible from documented parameters and commands in
[the examples gallery](examples/README.md).

## Install

- Python 3.11 or newer

Create a virtual environment and install Diffugen with its test dependency:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Run

List the built-in presets:

```bash
python -m diffugen --list-presets
```

Generate one reproducible wallpaper:

```bash
python -m diffugen \
  --preset standard --seed 42 --output wallpaper.png
```

Size, simulation steps, and tile repetition can also be selected:

```bash
python -m diffugen \
  --preset texture --size 64 --steps 20000 --scale 9 --seed 42 \
  --output wallpaper.png
```

Running without options preserves the original behavior and generates all five
presets under `.rd/`:

```bash
python -m diffugen
```

The installed `diffugen` command and the original `python main.py` entry point
remain available.

Use `--all-presets --output-dir PATH` to choose a directory for a multi-preset
run. Output directories are created automatically, and generated `.rd/` files
are ignored by Git.

Runs are deterministic by default. The simulation functions also accept
`seed=None` when fresh random initialization is wanted.

## Test

```bash
pytest
```

The tests use small simulations and temporary image files, so they complete
quickly and do not write generated artwork into the repository.

## License

Diffugen is available under the GNU General Public License v3.0. See `LICENSE`.
