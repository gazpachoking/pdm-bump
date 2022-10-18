from dataclasses import dataclass
from pathlib import Path
import re

from .config import Config

DEFAULT_REGEX = re.compile(
    r"^__version__\s*=\s*[\"'](?P<version>.+?)[\"']\s*(?:#.*)?$", re.M
)


@dataclass
class DynamicVersionConfig:
    file: Path
    regex: re.Pattern


def find_dynamic_config(
    root_path: Path, project_config: Config
) -> DynamicVersionConfig | None:
    if (
        project_config.get_pyproject_value("build-system", "build-backend")
        == "pdm.pep517.api"
        and project_config.get_pyproject_value(
            "tool", "pdm", "version", "source"
        )
        == "file"
    ):
        file_path = project_config.get_pyproject_value(
            "tool", "pdm", "version", "path"
        )
        return DynamicVersionConfig(
            file=root_path / file_path,
            regex=DEFAULT_REGEX,
        )


def get_dynamic_version(config: DynamicVersionConfig) -> str | None:
    with config.file.open("r") as fp:
        match = config.regex.search(fp.read())
    return match and match.group("version")


def replace_dynamic_version(config: DynamicVersionConfig, new_version: str):
    with config.file.open("r") as fp:
        version_file = fp.read()
        match = config.regex.search(version_file)
        old_version_line = match.group(0)
        old_version = match.group("version")
        new_version_line = old_version_line.replace(old_version, new_version)
        new_version_file = config.regex.sub(new_version_line, version_file)
    with config.file.open("w") as fp:
        fp.write(new_version_file)