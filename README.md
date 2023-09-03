# Sudoku

Yet another Sudoku game in python.

## Description

My pgame implementation of popular Sudoku game with setup for pygbag wasm.

### Installing

Run below commands to download project, setup virtualenv and install dependencies:

```
git clone https://github.com/MaxOfLondon/sudoku
cd sudoku
chmod +x install-and-test-run.sh
source install-and-test-run.sh
```

If you prefer to intall manually, run:

```
python3 -m pip install --user virtualenv
virtualenv -q -p /usr/bin/python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Executing program

You can test run the game using `install-and-test-run.sh` script. It will offer to launch game with python and then in the web browser.

Altenatively, to run game manually with Python:

```
cd src
python3 main.py
```

To run game in browser via local test server, ensure you are in project folder and the .venv virtual environment is active then run pygbag:

```
pygbag --ume_block=0 src
```

## How to play

Game rules and how to play instructions can be found on [sudoku.com](https://sudoku.com/how-to-play/sudoku-rules-for-complete-beginners/).

Select an empty cell then using keyboard enter a number or click on number button at the bottom.

To restart the game with difficulty adjusted, slide the slider at the top to desired position then press R key or click R button in the top-right corner. Game is easier with slider closer to the left edge and harder to the right edge. The default position is 50%.

To display hints (incorrectly entered numbers will be highlited), press H key or click lightbulb button in the bottom-right corner.

To pause the game, press SPACEBAR key or click the pause button in the top-left corner.

## Screenshot

![Screenshot](src/img/screenshot1.png?raw=true "Screenshot")

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
