<div align="center">
<h1 align="center">Unreal Python Editor</h1>

  <p align="center">
    <b>Unreal Engine Python Script Editor</b>
    is an Unreal equivalent of the "Maya Script Editor"
  </p>
</div>


## About The Project

<div align="center">
<img src="https://i.imgur.com/KscixlU.png" alt="ui" height="580px"/>
</div>

With the rapid advancement of Unreal Engine and the Python support in Unreal
Engine, more and more people are jumping into Unreal Python scripting. 
Hence the creation of this tool!

## Getting Started

### Prerequisites

The tool needs the following library to be installed:

- Qt for Python: [PySide2](https://pypi.org/project/PySide2/) or [PyQt5](https://pypi.org/project/PyQt5/)

- Python shim for all Qt bindings: [Qt.py](https://pypi.org/project/Qt5.py/)


### Add as Menu Button

The tool is meant to be launched from a menu bar button like such:

<div align="center">
<img src="https://i.imgur.com/IcQGGu5.png" alt="menu">
</div>

You can set up this very easily by adding `startup.py` as a startup script,
under _Project Settings - Plugins - Python_

- download the project zip file where you can find the `startup.py`, add
that location to the startup scripts: 
e.g. _"C:\Downloads\unrealScriptEditor\startup.py"_


<div align="center">
<img src="https://i.imgur.com/wJrkp5b.png" alt="menu">
</div>

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


## Features

- [x] Unreal "native" [stylesheet](https://github.com/leixingyu/unrealStylesheet)
- [x] Save and load python files and temporary scripts
- [x] Code editor short-cut support and Highlighter
- [ ] Auto-completion

## Support

This tool is still in development, if there's any issue please submit your bug
[here](https://github.com/leixingyu/unrealScriptEditor/issues)
or contact [techartlei@gmail.com]()
