# Sudoku
[![CI Sudoku workflow](https://github.com/MaxOfLondon/sudoku/actions/workflows/deploy-pygame.yml/badge.svg)](https://github.com/MaxOfLondon/sudoku/actions/workflows/deploy-pygame.yml)
 
## Description

An OO implementation of Sudoku game in Python Pygame with Pygbag wasm. The game can be run as stand alone app or as a browser game.

Play [Sudoku](https://maxoflondon.github.io/sudoku/index.html) now on Github.

> **_NOTE:_** It will take some time to load for the first time in the browser because all dependencies are being downloaded and game assembled but subsequent run should be much faster, please be patient.

### Installing

Run below commands to download project, setup virtualenv and install dependencies:

```
git clone https://github.com/MaxOfLondon/sudoku
cd sudoku
chmod +x install-and-test-run.sh
# for development:
source install-and-test-run.sh dev
# for production (default if no argument given):
source install-and-test-run.sh prod
```

If you prefer to intall manually, run:

```
python3 -m pip install --user virtualenv
virtualenv -q -p /usr/bin/python3 .venv
source .venv/bin/activate
# for development:
pip install -r requirements/dev.txt
# for production:
pip install -r requirements/prod.txt
```

### Executing program

You can test run the game using `install-and-test-run.sh` script. It will offer to launch game with python and then in the web browser via local test server.

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

Select an empty cell then using keyboard enter a number or click on a number button at the bottom.

To restart the game with difficulty adjusted, slide the slider at the top to desired position then press <kbd>R</kbd> key or click R button in the top-right corner. Game is easier with slider closer to the left edge and harder when slider is to the right. The default position is 50%.

To display hints (incorrectly entered numbers will be highlited), press <kbd>H</kbd> key or click lightbulb button in the bottom-right corner. Hit <kbd>H</kbd> again to toggle hints off.

To pause the game, press <kbd>SPACEBAR</kbd> key or click the pause button in the top-left corner.

## Screenshot

![Screenshot](src/img/screenshot1.png?raw=true "Screenshot")

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
