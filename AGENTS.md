# AGENTS.md

## Project
Cờ Caro (Omok) game written in **Python 3.14 + pygame-ce** (imported as `pygame`).
`README.md` is in Vietnamese and is the **authoritative spec** — its constraints are grading
requirements, not suggestions. Read it before implementing anything.

## Run
- `python main.py` from the repo root. No build/codegen step — runs the script directly.
- Dependencies: `pip install -r requirements.txt` (`pygame-ce` only). Try install `pygame-ce` first —
  it is a fork of pygame, so install it explicitly instead of assuming stock `pygame`.
- Headless end-to-end check (no display needed): `python smoke_test.py`. Run it after touching screens,
  board logic or transitions — the repo has no CI, so this is the regression safety net.

## Architecture rules (from README — do not violate)
- OOP, SOLID, **composition over inheritance**, low coupling / high cohesion, KISS, and other basic
  programming principles.
- **Max 2 inheritance levels, excluding inheritance from pygame base types.** Today: `Button` and
  `Board` inherit `pygame.sprite.Sprite`; `StartScreen`/`SettingScreen`/`GameScreen` inherit `Screen`.
  Never grow these chains deeper.
- **Scene switching uses the `ScreenState` enum + screen objects — never boolean flags.** README
  discourages boolean state variables for the start/settings/game states; use an object / state-machine
  or screen-manager pattern or enum pattern (this codebase uses the enum). Buttons call
  `App.navigate(state)`; `App` picks the current `Screen` for the frame.
- Render through `pygame.sprite`. **Textures are built manually in code as single-color per-pixel RGBA**
  via `textures.solid_texture()` — there are no image assets; don't add asset/file loading unless asked.

## File map (flat modules, run everything from repo root)
- `main.py` — process bootstrap only (`pygame.init` + `pygame.font.init` → `App().run()`). No game logic.
- `app.py` — `App`: owns the window, main loop (`run()`/`step()`), event dispatch and transitions.
- `states.py` — the `ScreenState` enum used for scene switching.
- `screen.py` — `Screen` base: sprite group, event fan-out, update, render, and `layout()`/`arrange()`
  for size-aware positioning.
- `startScreen.py`, `settingScreen.py`, `gameScreen.py` — the three screens.
  `SettingScreen(navigate, source_state)` shows "Back to Game" only when reached from GAME;
  `GameScreen.reset()` restores the board.
- `board.py` — `Board(pygame.sprite.Sprite)`: grid rendering, `place()`, win detection.
- `Button.py` — `Button(pygame.sprite.Sprite)`; screens duck-type `handle_event`/`update` on sprites.
- `settings.py` — all tunables (display, UI, game). No hardcoded literals elsewhere.
- `textures.py` — `solid_texture(size, color)`, the only texture factory.
- `smoke_test.py` — headless regression check (see Run).
- Naming is inconsistent/camelCase (`Button.py`, `startScreen.py`); match it when adding files.

## Verified behavior (see smoke_test.py)
- Start screen is the initial scene; buttons: Start → GAME, Settings → SETTINGS.
- Game screen: 15×15 board (cell 32px) + Home (→ START) and Settings (→ SETTINGS) buttons below it.
- Stones alternate X/O, occupied cells refuse moves, and `WIN_LENGTH` in a row sets `board.winner`
  and locks the board.
- Settings buttons depend on the source state: from START only "Back to Start"; from GAME also
  "Back to Game". Leaving the game for good (Home or "Back to Start") calls
  `GameScreen.reset()` → `Board.reset()` (empty grid, Player X turn, winner cleared). The same
  `GameScreen` instance persists, so "Back to Game" keeps the moves and the win lock.
- **F11** toggles fullscreen (mutates `settings.FULLSCREEN`, recreates the window). After a transition,
  the incoming screen is positioned on its first frame — clicks computed before that use stale rects.
- The window is `RESIZABLE`; `Screen.layout()` repositions sprites only when the surface size changes.

## Gotchas
- Board geometry lives in `settings.py` (`BOARD_ROWS`/`BOARD_COLS = 15`, `BOARD_CELL_SIZE = 32` → 481px
  board). The old tentative constants (`BOARD_SIZE`, `BOARD_CELL_WIDTH/HEIGHT`) were removed — don't
  reintroduce them.
- Only `main.py`, `settings.py` and `__pycache__/settings.cpython-314.pyc` are git-tracked; every other
  file is untracked and there is **no `.gitignore`**. Don't commit new `.pyc` files by accident; running
  `smoke_test.py` regenerates them.