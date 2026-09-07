# Mahabali Run

A fast-paced endless runner built with **pygame-ce**, putting a twist on the legend of Mahabali and Vamana.

## The Story

In the traditional telling, Mahabali offers his head so that Vamana's third step can be completed, descending willingly into the underworld. *Mahabali Run* flips the script: you play as Mahabali, sprinting and dodging to outrun Vamana's ever-growing foot before it comes down.

## Features

- Endless runner gameplay with escalating difficulty
- Swipe-based touch controls (left / right dodging, sliding)
- Custom SVG-based sprite rendering
- Sounds form [pixabag](https://pixabay.com/)

## Controls

| Action | Desktop |
|---|---|
| Move left | A or Left Key |
| Move right | D or Right Key |
| Slide | S or Down Key |
| Start / Restart | Click Play Button |
| Quit | `Esc` |

## Running from Source

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone <repo-url>
cd mahabali-run
uv venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
uv pip install -r pyproject.toml
python src/mahabali_run/main.py
```

## Building

### Windows Executable

Built with [PyInstaller](https://pyinstaller.org/):

```powershell
pyinstaller --onefile --windowed --name "MahabaliRun" --icon="mahabalirun.ico" `
  --add-data "src\graphics;graphics" `
  --add-data "src\sounds;sounds" `
  --paths "src\mahabali_run" `
  .\src\mahabali_run\main.py
```

The resulting `.exe` is placed in `dist/`.

## Tech Stack

- [pygame-ce](https://pyga.me/) — game engine
- [PyInstaller](https://pyinstaller.org/) — Windows packaging
- [uv](https://docs.astral.sh/uv/) — Python package management

## License

See [LICENSE](LICENSE).
