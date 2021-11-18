# Crane Game
A classic arcade game for a special person!

## Dev Setup

Make sure you have Anaconda3 installed.

Create a new environment with PyBox2D:
```
$ conda create -n crane -c conda-forge python=3.8 pybox2d
$ conda activate crane
```

Clone this repository to your favorite place and install it as an editable package:

```
$ (crane) git clone https://github.com/mtmk-ee/crane-game.git
$ (crane) pip install -e crane-game
```

## Building

Building this game requires PyInstaller, grab it if you don't have it already
```
$ (crane) pip install pyinstaller
```

To build the game, run the following:

```
$ (crane) cd crane-game
$ (crane) pyinstaller crane.spec --windowed
```

If successful, the game should build to `crane-game/dist`!