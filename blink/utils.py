import json
import yaml
import toml
import pathlib
from configparser import ConfigParser
import xmltodict
from typing import IO


class ConfigParserExt(ConfigParser):
    def to_dict(self) -> dict:
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop("__name__", None)
        return d
    
    def dumps(self, space_around_delimiters=True) -> str:
        """Return an .ini-format representation of the configuration state.

        If `space_around_delimiters' is True (the default), delimiters
        between keys and values are surrounded by spaces.
        """
        output = ""
        if space_around_delimiters:
            d = " {} ".format(self._delimiters[0])
        else:
            d = self._delimiters[0]
        if self._defaults:
            output += self._dumps_section(self.default_section,
                                    self._defaults.items(), d)
        for section in self._sections:
            output += self._dumps_section(section,
                                self._sections[section].items(), d)
        return output

    def _dumps_section(self, section_name, section_items, delimiter) -> str:
        """Dump string a single section"""
        output = "[{}]\n".format(section_name)
        for key, value in section_items:
            value = self._interpolation.before_write(self, section_name, key,
                                                     value)
            if value is not None or not self._allow_no_value:
                value = delimiter + str(value).replace('\n', '\n\t')
            else:
                value = ""
            output += "{}{}\n".format(key, value)
        output += "\n"
        return output


def load_config(path: pathlib.Path, ext: str = None, **kwargs) -> dict:
    config: dict = None
    ext = path.suffix if ext is None else ext
    with path.open(mode="r") as config_file:
        if ext == ".json":
            config = json.load(config_file, **kwargs)
        elif ext in [".yml", ".yaml"]:
            if "Loader" not in kwargs.keys():
                kwargs["Loader"] = yaml.loader.SafeLoader
            config = yaml.load(config_file, **kwargs)
        elif ext == ".xml":
            xml_input = config_file.read()
            config = xmltodict.parse(xml_input, **kwargs)
        elif ext in [".ini", ".cfg"]:
            ini_config = ConfigParserExt()
            ini_config.read_file(config_file)
            config = ini_config.to_dict()
        elif ext == ".toml":
            config = toml.load(config_file, **kwargs)
        else:
            print("Currently supports ini, json, toml, xml, yaml config files only")
            raise ValueError("File type not supported!")
    return config


def dumps(config: dict, ext: str, **kwargs):
    config_str = ""
    if ext == ".json":
        if "indent" not in kwargs.keys():
            kwargs["indent"] = 2
        config_str = json.dumps(config, **kwargs)
    elif ext in [".yml", ".yaml"]:
        if "indent" not in kwargs.keys():
            kwargs["indent"] = 2
        config_str = yaml.safe_dump(config, **kwargs)
    elif ext == ".xml":
        if "pretty" not in kwargs.keys():
            kwargs["pretty"] = True
        if len(config.keys()) == 1:
            config_str = xmltodict.unparse(config, **kwargs)
        else:
            config_str = xmltodict.unparse({"config": config}, **kwargs)
    elif ext in [".ini", ".cfg"]:
        ini_config = ConfigParserExt()
        ini_config.read_dict(config, **kwargs)
        config_str = ini_config.dumps()
    elif ext == ".toml":
        config_str = toml.dumps(config, **kwargs)
    else:
        print("Currently supports ini, json, toml, xml, yaml config files only")
        raise ValueError("File ext not supported!")
    return config_str


def export(path: pathlib.Path, config: dict, ext: str = None, **kwargs):
    ext = path.suffix if ext is None else ext
    with path.open("w+") as config_file:
        if ext == ".json":
            json.dump(config, config_file, **kwargs)
        elif ext in [".yml", ".yaml"]:
            _ = yaml.safe_dump(config, config_file, **kwargs)
        elif ext == ".xml":
            if len(config.keys()) == 1:
                config_str = xmltodict.unparse(config, **kwargs)
            else:
                config_str = xmltodict.unparse({"config": config}, **kwargs)
            config_file.write(config_str)
        elif ext in [".ini", ".cfg"]:
            ini_config = ConfigParserExt()
            ini_config.read_dict(config, **kwargs)
            ini_config.write(config_file)
        elif ext == ".toml":
            config_str = toml.dump(config, config_file, **kwargs)
        else:
            print("Currently supports ini, json, toml, xml, yaml config files only")
            raise ValueError("File ext not supported!")
