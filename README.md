# Connect-Four with a Minimax AI

A terminal Connect-Four game where you play against an AI opponent driven by the
[minimax](https://en.wikipedia.org/wiki/Minimax) algorithm. Written for CSC 242
(Introduction to AI) at the University of Rochester.

## Play

```bash
python3 connect_four.py
```

You'll be asked to pick a board size:

- **3×3** — the search is small enough that minimax plays the full game tree, so
  the AI is unbeatable.
- **6×7** (standard Connect-Four) — the tree is too large to search exhaustively,
  so the AI searches to a fixed depth and then falls back to a heuristic
  evaluation of the position (`predict`).

Enter a column number on your turn; the AI responds automatically.

## How it works

- The board is a 2-D grid; the AI explores possible future states by recursively
  applying `minimax`, scoring a win for the AI as `+1`, a loss as `-1`, and a draw
  as `0`.
- On the larger board, a depth cutoff keeps the search tractable and `predict`
  supplies a heuristic score for non-terminal positions at the cutoff.
- Win detection checks all four line orientations (horizontal, vertical, and both
  diagonals).

## Notes

- This is the "history of learning" version: it was my first AI assignment, and
  the heuristic for the 6×7 board is deliberately simple. Alpha-beta pruning was
  left as a stretch goal and is not implemented.
- Fixed since the original submission: the anti-diagonal win checks
  (`check_l_slope` and one branch of `predict`) used unguarded negative row
  indices that could wrap around in Python and report a false win; the loops now
  start at a safe offset. The game entry point is also guarded behind
  `if __name__ == '__main__'` so the module can be imported and unit-tested.
