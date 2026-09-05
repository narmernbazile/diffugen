# Diffugen

Diffugen is a small creative-coding project that turns Gray–Scott
reaction–diffusion simulations into seamless, black-and-white tiled images.

## Requirements

- Python 3.14
- [Pipenv](https://pipenv.pypa.io/)

## Run

Install the locked dependencies and generate all five built-in patterns:

```bash
pipenv install
pipenv run python main.py
```

The script creates `.rd/` automatically. Each preset produces an intermediate
tile, a thresholded tile, and a final 9 by 9 wallpaper image. Generated files
are ignored by Git.

Runs are deterministic by default. The simulation functions also accept
`seed=None` when fresh random initialization is wanted.

## Test

```bash
pipenv run python -m unittest discover -s tests
```

The tests use small simulations and temporary image files, so they complete
quickly and do not write generated artwork into the repository.

## License

Diffugen is available under the GNU General Public License v3.0. See `LICENSE`.
