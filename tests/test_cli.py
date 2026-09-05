import pytest

from diffugen.cli import main


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
