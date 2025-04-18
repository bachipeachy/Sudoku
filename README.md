# Sudoku by Bachi

A clean, lightweight Sudoku game for macOS — built with [Toga](https://beeware.org/) in Python. No timers, just pure logic and relaxation.

## Sudoku Game Rules
Fill a 9×9 grid so each row, column, and mutually exclusive 3×3 sub-grids contains digits 1–9 exactly once.

## Features

- Easy, Medium, Hard difficulty modes
- Auto-loads an Easy puzzle at startup
- "New Game" read-only digits shown in RED
- "User Inputs" shown in BLACK
- “Check Solution” highlights incorrect entries in PURPLE
- “Show Solution” reveals final answers in GREEN
- Clean grid with bold lines between 3x3 subgrids
- Native macOS feel using the Toga framework
- Built and bundled as a standalone mac `Sudoku by Bachi.dmg` (no Python required)

## How to Run
Download and double click "Sudoku by Bachi.dmg" package for Mac and drop it in the application folder. It has no dependencies.
Or, run python script on command line "python sudoku.py" after "pip install toga"-- the python library for GUI.

## Developer

Made with by [Bachi Peachy](https://github.com/bachipeachy)

## Build Instructions (Optional)

To convert into a Mac app using `py2app`:

```bash
pip install toga toga-cocoa py2app
python setup.py py2app
```

This will create a standalone "Sudoku by Bachi.app" in the `dist/` folder.


## License

MIT — use, modify, and share freely!
