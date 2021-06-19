import json
import yaml
import toml
import pathlib
from configparser import ConfigParser
import xmltodict


class InitDict(ConfigParser):
    def to_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop("__name__", None)
        return d


def load_config(path: pathlib.Path, ext: str = None, **kwargs):
    config: dict = None
    ext = path.suffix if ext is None else ext
    with path.open(mode="r") as config_file:
        if ext == ".json":
            config = json.load(config_file)
        elif ext in [".yml", ".yaml"]:
            config = yaml.load(config_file, Loader=yaml.loader.SafeLoader)
        elif ext == ".xml":
            config = xmltodict.parse(config_file, **kwargs)
        elif ext == ".ini":
            ini_config = InitDict()
            ini_config.read_file(config_file)
            config = ini_config.to_dict()
        elif ext == ".toml":
            config = toml.load(config_file)
        else:
            print("Currently supports ini, josn, toml, yaml, xml config files only")
            raise Exception("File type not supported!")
    return config
