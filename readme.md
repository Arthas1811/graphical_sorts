# library for Searching Algorithms with GUI for IT-Classes
by [Arthas1811](https://github.com/Arthas1811)

## Installation

```bash
pip install graphical-sort-lib
```

## Usage

```python
import graphicalSortLib

graphicalSortLib.run()
```

## Troubleshooting

- **_tkinter.TclError: Can't find a usable init.tcl**  
  Python 3.13 virtual environments sometimes lose the Tcl/Tk search path.  
  Version 1.0+ of this library automatically locates the base installation, but if the
  error persists please reinstall Python with the optional *tcl/tk and IDLE* feature
  so that the runtime is available.
