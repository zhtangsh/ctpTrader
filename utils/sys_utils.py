import logging
from pathlib import Path


def _get_project_folder(project_name: str) -> Path:
    """
    Generate Project Folder
    :param project_name: 项目名称
    :return:
    """
    home_path: Path = Path.home()
    project_path: Path = home_path.joinpath(project_name)

    if not project_path.exists():
        project_path.mkdir()

    return project_path


PROJECT_DIR = _get_project_folder(".ctpTrader")


def get_file_path(filename: str) -> Path:
    """
    Get path for temp file with filename.
    """
    return PROJECT_DIR.joinpath(filename)


def get_folder_path(folder_name: str) -> Path:
    """
    Get path for temp folder with folder name.
    """
    folder_path: Path = PROJECT_DIR.joinpath(folder_name)
    if not folder_path.exists():
        folder_path.mkdir()
    return folder_path


def logging_config(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format='%(asctime)s %(name)s %(levelname)-8s %(message)s'
    )
