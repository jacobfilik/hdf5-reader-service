import multiprocessing as mp
from typing import Any, Mapping

import h5py

from hdf5_reader_service.utils import h5_tree_map

from .metadata import metadata


def fetch_tree(path: str, subpath: str, swmr: bool, queue: mp.Queue) -> None:
    path = "/" + path

    def get_metadata(name: str, obj: h5py.HLObject) -> Mapping[str, Any]:
        return metadata(obj)

    with h5py.File(path, "r", swmr=swmr, libver="latest") as f:
        tree = h5_tree_map(get_metadata, f, map_name="metadata")

    queue.put(tree)