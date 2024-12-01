import kaggle

from constants import Paths
from os.path import isdir
from typing import AnyStr, Iterable

def download_if_missing(dataset_names: Iterable[AnyStr], dataset_root_path: AnyStr = Paths.DATASET_ROOT) -> None:
    def download_if_missing(dataset_name: AnyStr, dataset_root_path: AnyStr) -> None:
        directory = f'{dataset_root_path}/{dataset_name}'
        if isdir(directory):
            return
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(dataset_name, directory, unzip=True)
    for dataset_name in dataset_names:
        download_if_missing(dataset_name, dataset_root_path)
