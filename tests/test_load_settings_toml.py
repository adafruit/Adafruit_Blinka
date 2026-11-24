# SPDX-FileCopyrightText: 2025 Justin Myers
#
# SPDX-License-Identifier: MIT
import os
from unittest import mock
import pytest
import adafruit_blinka
from adafruit_blinka import get_setting, load_settings_toml

try:
    import tomllib
except ImportError:
    import tomli as tomllib

# pylint: disable=no-self-use,unused-argument

CONVERTED_TOML = {
    "123": 123,
    "test": "test",
    "test-hyphen": "test-hyphen",
    "test_bool": True,
    "test_number": 123,
    "test_space": "test space",
    "test_underscore": "test_underscore",
    "true": False,
}


INVALID_TOML = b"""
# strings
test=test
"""


VALID_TOML = b"""
# strings
test="test"
test_space="test space"
test_underscore="test_underscore"
test-hyphen="test-hyphen"
# number
test_number=123
# bool
test_bool=true
# other
123=123
true=false
"""

VALID_TOML_WITH_UNSUPPORTED_DATA_DICT = b"""
# dict
data = { key_1 = "value", key_2 = "value" }
"""

VALID_TOML_WITH_UNSUPPORTED_DATA_LIST = b"""
# list
numbers = [ 1, 2, 3 ]
"""

VALID_TOML_WITH_UNSUPPORTED_DATA_MANY = b"""
# dict
data = { key_1 = "value", key_2 = "value" }

# list
numbers = [ 1, 2, 3 ]

[nested]
test="test"
"""

VALID_TOML_WITH_UNSUPPORTED_DATA_NESTED = b"""
[nested]
test="test"
"""


@pytest.fixture(autouse=True)
def _reset_settings(monkeypatch):
    monkeypatch.setattr(adafruit_blinka, "_settings", None)
    monkeypatch.delenv("BLINKA_TEST_SETTING", raising=False)


class TestLoadSettingsToml:
    @mock.patch("adafruit_blinka.os.path.isfile", mock.Mock(return_value=False))
    def test_raises_with_no_file(self):
        with pytest.raises(
            FileNotFoundError, match="settings.toml not found in current directory."
        ):
            load_settings_toml()

    @mock.patch("adafruit_blinka.os.path.isfile", mock.Mock(return_value=True))
    @mock.patch("builtins.open", mock.mock_open(read_data=INVALID_TOML))
    def test_raises_with_invalid_file(self):
        with pytest.raises(
            tomllib.TOMLDecodeError, match=r"Error with settings\.toml file\."
        ) as raised:
            load_settings_toml()
        assert isinstance(raised.value.__cause__, tomllib.TOMLDecodeError)

    @mock.patch("adafruit_blinka.os.path.isfile", mock.Mock(return_value=True))
    @mock.patch(
        "builtins.open", mock.mock_open(read_data=VALID_TOML_WITH_UNSUPPORTED_DATA_DICT)
    )
    def test_raises_with_invalid_file_dict(self):
        with pytest.raises(
            ValueError, match="The types: 'dict' are not supported in settings.toml."
        ):
            load_settings_toml()

    @mock.patch("adafruit_blinka.os.path.isfile", mock.Mock(return_value=True))
    @mock.patch(
        "builtins.open", mock.mock_open(read_data=VALID_TOML_WITH_UNSUPPORTED_DATA_LIST)
    )
    def test_raises_with_invalid_file_list(self):
        with pytest.raises(
            ValueError, match="The types: 'list' are not supported in settings.toml."
        ):
            load_settings_toml()

    @mock.patch("adafruit_blinka.os.path.isfile", mock.Mock(return_value=True))
    @mock.patch(
        "builtins.open", mock.mock_open(read_data=VALID_TOML_WITH_UNSUPPORTED_DATA_MANY)
    )
    def test_raises_with_invalid_file_many(self):
        with pytest.raises(
            ValueError,
            match="The types: 'dict, list' are not supported in settings.toml.",
        ):
            load_settings_toml()

    @mock.patch("adafruit_blinka.os.path.isfile", mock.Mock(return_value=True))
    @mock.patch(
        "builtins.open",
        mock.mock_open(read_data=VALID_TOML_WITH_UNSUPPORTED_DATA_NESTED),
    )
    def test_raises_with_invalid_file_nested(self):
        with pytest.raises(
            ValueError, match="The types: 'dict' are not supported in settings.toml."
        ):
            load_settings_toml()

    @mock.patch("adafruit_blinka.os.path.isfile", mock.Mock(return_value=True))
    @mock.patch("builtins.open", mock.mock_open(read_data=VALID_TOML))
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_returns_data(self):
        for key in CONVERTED_TOML:
            assert os.getenv(key) is None

        assert load_settings_toml() == CONVERTED_TOML

        for key, value in CONVERTED_TOML.items():
            assert os.getenv(key) == str(value)


def test_get_setting_raises_for_missing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(KeyError, match="BLINKA_TEST_SETTING"):
        get_setting("BLINKA_TEST_SETTING")


def test_get_setting_reads_the_file_once(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "settings.toml"
    path.write_text(
        "BLINKA_TEST_SETTING = 2\n[app]\noptions = [1, true]\n", encoding="utf-8"
    )
    assert get_setting("BLINKA_TEST_SETTING") == 2
    path.unlink()
    assert get_setting("app") == {"options": [1, True]}
    assert "BLINKA_TEST_SETTING" not in os.environ
    with pytest.raises(KeyError, match="BLINKA_TEST_MISSING"):
        get_setting("BLINKA_TEST_MISSING")


def test_get_setting_prefers_environment(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "settings.toml").write_text("invalid TOML]", encoding="utf-8")
    monkeypatch.setenv("BLINKA_TEST_SETTING", "4")
    assert get_setting("BLINKA_TEST_SETTING") == "4"
    monkeypatch.delenv("BLINKA_TEST_SETTING")
    with pytest.raises(tomllib.TOMLDecodeError):
        get_setting("BLINKA_TEST_SETTING")


def test_explicit_load_refreshes_get_setting(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "settings.toml"
    path.write_text("BLINKA_TEST_SETTING = 2\n", encoding="utf-8")
    assert get_setting("BLINKA_TEST_SETTING") == 2
    path.write_text("BLINKA_TEST_SETTING = 3\n", encoding="utf-8")
    assert load_settings_toml() == {"BLINKA_TEST_SETTING": 3}
    assert os.environ["BLINKA_TEST_SETTING"] == "3"
    monkeypatch.delenv("BLINKA_TEST_SETTING")
    assert get_setting("BLINKA_TEST_SETTING") == 3
