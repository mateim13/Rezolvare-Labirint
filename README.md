# 3D Maze Pathfinding

A Python program that generates a random 3D maze and finds paths between two cells using **BFS** (shortest paths) and **recursive backtracking** (path enumeration). Results are visualized in 3D with Matplotlib and exported as an image, a GIF animation, a CSV file and an HTML report.

Academic project, Year 1 (2024–2025).

## Features

- Random 3D maze generation (`N x N x N` grid, each cell is a wall or free).
- **BFS-based search** that finds all shortest paths between the start and end cells.
- **Recursive backtracking** that enumerates paths between the two cells (capped at 1000 paths, since the number of paths grows exponentially with maze size).
- 3D visualization with Matplotlib: walls, start, end, and the shortest paths highlighted.
- GIF animation of the shortest path being traced step by step (`imageio`).
- Results exported to CSV and appended to an HTML report.

## Requirements

- Python 3
- `matplotlib`
- `imageio`

```bash
pip install matplotlib imageio
```

## Usage

```bash
python main.py
```

The program asks for:

1. The maze size (for example `5`). Start with a maze size of 3. Larger mazes may require significantly more time and memory.
2. The start coordinates, as `x y z` (for example `0 0 0`).
3. The end coordinates, as `x y z`.

Start and end must be free cells. The program prints the list of free positions to help you choose.

The maze is random, so a path between the two cells may not exist. In that case the program reports it and stops; run it again to get a new maze.

## How it works

1. **Maze generation:** each cell is randomly set to `0` (free) or `1` (wall).
2. **Shortest paths (BFS):** the search expands from the start cell level by level using a queue, moving in the 6 directions (±x, ±y, ±z), and keeps every path of minimum length that reaches the end.
3. **Path enumeration (backtracking):** a recursive search tries all unvisited free neighbors, backtracks when a branch fails, and stores each path that reaches the end. The search stops after 1000 paths.
4. **Output:** the shortest paths are drawn in 3D and saved, and the results are exported.

## Output files

All files are saved next to the script:

| File | Content |
| --- | --- |
| `labirint_<start>_to_<end>_<timestamp>.png` | 3D image of the maze with the shortest paths |
| `animatie_labirint.gif` | Animation of one shortest path |
| `Solutii_Labirint.csv` | Paths found, with date and time of each run |
| `raport_labirint_scurt.html` | HTML report with the image, the animation and the first solutions |

The GIF is overwritten on each run, while CSV and HTML reports are appended.

## Project structure

| Function | Purpose |
| --- | --- |
| `generare_labirint` | Generates the random 3D maze |
| `validare` | Checks that a cell is inside the maze and free |
| `drum_minim` | BFS search for the shortest paths |
| `drumuri` | Backtracking enumeration of paths |
| `imagine` | Draws and saves the 3D image |
| `generare_gif` | Builds the GIF animation |
| `salvare_csv`, `html` | Export results |

Function and variable names are in Romanian.

## Author

Matei Mândrescu — [GitHub](https://github.com/mateim13)
