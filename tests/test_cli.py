from pathlib import Path

import pytest

from diffugen.cli import DEFAULT_OUTPUT_DIR, build_parser, main


def test_no_arguments_print_help(capsys):
  assert main([]) == 0

  output = capsys.readouterr().out
  assert output.startswith('usage: diffugen')
  assert 'Generate tiled Gray-Scott reaction-diffusion art.' in output


def test_default_output_directory_is_generated():
  args = build_parser().parse_args(['--all-presets'])

  assert DEFAULT_OUTPUT_DIR == Path('generated')
  assert args.output_dir == Path('generated')


def test_list_presets(capsys):
  assert main(['--list-presets']) == 0

  assert capsys.readouterr().out.splitlines() == [
    'standard', 'texture', 'circles', 'eggs', 'big_eggs'
  ]


def test_invalid_preset_fails_clearly(capsys):
  with pytest.raises(SystemExit) as error:
    main(['--preset', 'missing'])

  assert error.value.code == 2
  assert "invalid choice: 'missing'" in capsys.readouterr().err
