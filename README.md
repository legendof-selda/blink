# :eye:blink

A hot-reload configuration dictionary

## Introduction

`blink` allows you to create configuration dictionary to your python program which autoupdates when your file changes. Usually when you load a config file, the loaded dictionary is stored in memory and when the actual config file changes, those changes are not reflected in memory. `blink` can help you with that problem by updating your config dictionary based on file changes safely.

You can access configuration exactly how you access your dictionary in python.

## How to use

Just import

```python
from blink import Config

config = Config("config.json")
```

and use it like a normal dictionary!

```python
val = config["key1"]["subkey1"]
print(config["number"])
```
