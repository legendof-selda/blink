import sys
import os
import pathlib
import json
module_path = os.path.abspath(os.path.join(__file__, "../.."))
if module_path not in sys.path:
    sys.path.append(module_path)
from blink import Config

sample = "./tests/sample.json"
config = Config(sample)

print(config._config)
print(config["key1"])
print(config.keys())

with open(sample, "r") as json_file:
    original = json_file.read()

change = config._config.copy()
change["key15"] = "NewKey"
with open(sample, "w") as json_file:
    json.dump(change, json_file)

print(config._config)
print(config["key1"])
print(config["key15"])
print(config.keys())

with open(sample, "w") as json_file:
    json_file.write(original)

print(config._config)
print(config["key1"])
print(config["key15"])
print(config.keys())