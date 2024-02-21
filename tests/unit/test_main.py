# SPDX-FileCopyrightText: 2024 Ohin "Kazani" Taylor <kazani@kazani.dev>
# SPDX-License-Identifier: MIT

"""Test main module of xenops."""

import _pytest.capture

import xenops.__main__


def test_main(capsys: _pytest.capture.CaptureFixture[str]) -> None:
    """Test that main() prints 'Hello world!'."""
    xenops.__main__.main()
    assert capsys.readouterr().out == 'Hello world!\n'
