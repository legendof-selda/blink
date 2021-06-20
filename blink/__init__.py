import pathlib
from .utils import load_config, dumps, export
from typing import Union
import traceback


class Config(object):
    def __init__(self, config_path: Union[pathlib.Path, str], **kwargs):
        self.config_path = pathlib.Path(config_path)
        if not self.config_path.is_file():
            if "create_file_if_not_exists" in kwargs and kwargs["create_file_if_not_exists"] is True:
                self.config_path.touch()
                self._config = {}
            else:
                raise FileNotFoundError("File does not exist!")
        else:
            self._config = load_config(self.config_path, **kwargs)
        self._update()
    
    def dumps(self, type:str, **kwargs) -> str:
        return dumps(self._config, type, **kwargs)

    def export(self, path:Union[pathlib.Path, str], ext:str = None, **kwargs) -> str:
        export(pathlib.Path(path), self._config, ext, **kwargs)
    
    def _check(self):
        if self.config_path.stat().st_mtime != self._modified:
            self._reload()

    def _reload(self):
        print(f"Reloading {self.config_path.name}")
        try:
            self._config = load_config(self.config_path)
        except Exception as err:
            print("Error Reloading config!")
            traceback.print_tb(err.__traceback__)
        finally:
            self._update()

    def _update(self):
        self._modified = self.config_path.stat().st_mtime

    def __getitem__(self, key):
        self._check()
        return self._config[key]
    
    def keys(self):
        self._check()
        return self._config.keys()

    def has_key(self, key):
        return key in self.keys()
    
    def __contains__(self, key):
        return self.has_key(key)
    
    def __iter__(self):
        return self._config.__iter__()
    
    def iterkeys(self):
        return self.__iter__()
    
    def items(self):
        return self._config.items()
    
    def __str__(self) -> str:
        self._check()
        return str(self._config)
