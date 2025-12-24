## screenshot-sum

Sums up the numbers found in the latest screenshot taken.

## Instructions

0. Install helper software

   ```
   brew install tesseract python-tk
   ```

1. Install dependencies

   ```
   uv sync
   ```

2. Edit SCREENSHOTS_PATH to point to wherever your screenshots land
3. Launch (watches for new screenshots in SCREENSHOTS_PATH defined in main.py)
   ```
   uv run main.py
   ```
4. Take a screenshot of a list of numbers. A small region will work best (Cmd+Shift+4)
5. A dialog box should appear with the screenshot name, list of numbers detected, and the total sum.

Note: You must have Tkinter via python-tk (brew install python-tk) in addition to regular python 3.14.2 or higher!
