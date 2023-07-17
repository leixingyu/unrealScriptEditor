
# Unreal Python Editor [![PyPI](https://img.shields.io/pypi/v/unreal-script-editor?color=blue)](https://pypi.org/project/unreal-script-editor/)

A Qt widget that's the Unreal equivalent of the "Maya Script Editor".  
This repo hosts the Python module, for the Unreal plugin, see [this repo](https://github.com/hannesdelbeke/unreal-plugin-python-script-editor).


## About The Project

<img src="https://i.imgur.com/KscixlU.png" alt="ui" height="580px"/>

With the rapid advancement of Unreal Engine and the Python support in Unreal
Engine, more and more people are jumping into Unreal Python scripting. 
Hence the creation of this tool!

## Getting Started

### Prerequisites

The tool needs the following library to be installed:

- Qt for Python: [PySide2](https://pypi.org/project/PySide2/) or [PyQt5](https://pypi.org/project/PyQt5/)
- Python shim for all Qt bindings: [Qt.py](https://pypi.org/project/Qt.py/)


### Add as Menu Button

The tool is meant to be launched from a menu bar button like such:

<img src="https://i.imgur.com/IcQGGu5.png" alt="menu">

You can set up this very easily by adding `startup.py` as a startup script,
under _Project Settings - Plugins - Python_

- download & extract the project zip file
- find the `startup.py` location, and add it to the startup scripts: e.g. `C:\Downloads\unrealScriptEditor\startup.py`


<img src="https://i.imgur.com/wJrkp5b.png" alt="menu">

### Simple Launch Script

**If** you just want to launch the tool in Unreal's python console without adding it to menu,
or if you want to customize the location where the tool is being launched;
refer to the following command:

- the tool has to be in a path that Unreal will search for!

```python
from unrealScriptEditor import main
global editor
editor = main.show()
```

### Install as module
install with pip
```bash
pip install unreal-script-editor
```

Install the module from the repo
```bash
python -m pip install git+https://github.com/hannesdelbeke/unreal-script-editor
```

## Features

- [x] Unreal "native" [stylesheet](https://github.com/leixingyu/unrealStylesheet)
- [x] Save and load python files and temporary scripts
- [x] Code editor short-cut support and Highlighter
- [ ] Auto-completion

## Support

This tool is still in development, if there's any issue please submit your bug
[here](https://github.com/leixingyu/unrealScriptEditor/issues)
or contact [techartlei@gmail.com]()
