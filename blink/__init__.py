import pathlib
from .utils import load_config
from typing import Union


class Config(object):
    def __init__(self, config_path: Union[pathlib.Path, str], **kwargs):
        self.config_path = pathlib.Path(config_path)
        self._modified = self.config_path.stat().st_mtime
        self._config = load_config(self.config_path)
    
    def _check(self):
        if self.config_path.stat().st_mtime != self._modified:
            self._reload()

    def _reload(self):
        print(f"Reloading {self.config_path.name}")
        self._modified = self.config_path.stat().st_mtime
        self._config = load_config(self.config_path)

    def __getitem__(self, key):
        self._check()
        return self._config[key]
    
    def keys(self):
        self._check()
        return self._config.keys()
