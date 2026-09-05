# Diffugen

Diffugen is a small creative-coding project that turns Gray–Scott
reaction–diffusion simulations into seamless, black-and-white tiled images.

## Requirements

- Python 3.14
- [Pipenv](https://pipenv.pypa.io/)

## Run

Install the locked dependencies:

```bash
pipenv install
```

List the built-in presets:

```bash
pipenv run python -m diffugen --list-presets
```

Generate one reproducible wallpaper:

```bash
pipenv run python -m diffugen \
  --preset standard --seed 42 --output wallpaper.png
```

Size, simulation steps, and tile repetition can also be selected:

```bash
pipenv run python -m diffugen \
  --preset texture --size 64 --steps 20000 --scale 9 --seed 42 \
  --output wallpaper.png
```

Running without options preserves the original behavior and generates all five
presets under `.rd/`:

```bash
pipenv run python -m diffugen
```

The original `pipenv run python main.py` entry point remains available.

Use `--all-presets --output-dir PATH` to choose a directory for a multi-preset
run. Output directories are created automatically, and generated `.rd/` files
are ignored by Git.

Runs are deterministic by default. The simulation functions also accept
`seed=None` when fresh random initialization is wanted.

## Test

```bash
pipenv run pytest
```

The tests use small simulations and temporary image files, so they complete
quickly and do not write generated artwork into the repository.

## License

Diffugen is available under the GNU General Public License v3.0. See `LICENSE`.
