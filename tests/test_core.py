import os
import json
import pytest
from pathlib import (
    Path,
)
from py_tasks.core import (
    Register,
    ConfigFile,
)


def cleanup(
    filename,
):
    """Remove generated files from testing"""

    def decorator(
        cls,
    ):
        def teardown_class(
            cls,
        ):
            current_dir = Path(__file__).parent
            file_path = current_dir / filename
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Cleanup: Removed file {filename}")

        cls.__del__ = teardown_class
        return cls

    return decorator


@cleanup(".test.json")
class TestConfigFile:
    CURRENT_DIR = Path(__file__).parent
    FILE_BASENAME = ".test"

    @classmethod
    @pytest.fixture
    def config_file(
        cls,
    ):
        return ConfigFile(
            cls.FILE_BASENAME,
            cls.CURRENT_DIR,
        )

    @pytest.fixture
    def filename(
        self,
    ):
        return self.FILE_BASENAME + ".json"

    def test_filename_is_correct(
        self,
        config_file: ConfigFile,
        filename: str,
    ):
        assert config_file.filename == filename

    @pytest.mark.dependency(name="file_is_created")
    def test_file_is_created(
        self,
        config_file: ConfigFile,
        filename: str,
    ):
        config_file.create_file()

        assert os.path.exists(self.CURRENT_DIR / Path(filename))

    @pytest.mark.dependency(
        name="default_file_template",
        depends=["file_is_created"],
    )
    def test_default_file_template(
        self,
        config_file: ConfigFile,
        filename: str,
    ):
        default_json = {
            "tasks": [],
            "cursor": 0,
            "cumul_count": 0,
        }

        with open(self.CURRENT_DIR / Path(filename)) as target:
            assert target.read() == json.dumps(
                default_json,
                indent=4,
            )

    @pytest.mark.dependency(
        name="read_json",
        depends=["default_file_template"],
    )
    def test_read_json_default(
        self,
        config_file: ConfigFile,
    ):
        content: dict = config_file.read()

        assert isinstance(
            content,
            dict,
        )
        assert content == {
            "tasks": [],
            "cursor": 0,
            "cumul_count": 0,
        }

    @pytest.mark.dependency(depends=["read_json"])
    def test_write_json(
        self,
        config_file: ConfigFile,
        filename: str,
    ):
        test_dict = {
            "tasks": list(range(10)),
            "cursor": 10,
            "cumul_count": 10,
        }

        config_file.write(test_dict)

        assert config_file.read() == test_dict


@cleanup(".test.json")
@pytest.mark.dependency(depends=["TestConfigFile::*"])
class TestRegister:
    FILE_BASENAME = TestConfigFile.FILE_BASENAME

    @classmethod
    @pytest.fixture
    def register(
        cls,
    ):
        return Register(cls.FILE_BASENAME)

    @classmethod
    @pytest.fixture
    def filename(
        cls,
    ):
        return cls.FILE_BASENAME + ".json"

    def test_register_is_created(
        self,
        register: Register,
    ):
        assert isinstance(
            register,
            Register,
        )
