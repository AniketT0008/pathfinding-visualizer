# Pathfinding Visualization Robot

Solve a maze with **A\***, **BFS**, or **DFS**, watch the search animate, then optionally drive a differential-drive robot along the path.

Hardware target:
- **ESP32-S3**
- **L298N** motor driver
- **2× gearbox motors** (left/right) + caster or skid

---

## Repo layout

```
main.py                          # CLI entry: generate → solve → visualize → drive?
maze_generator.py                # DFS maze + loops
Astar.py / BFS_*.py / DFS_*.py   # pathfinding + animation frames
visualizer.py                    # pygame animation
path_to_commands.py              # grid path → FORWARD/LEFT/RIGHT timed cmds
robot_client.py                  # WiFi TCP client → ESP32
config.py                        # cell/turn timing + maze defaults
firmware/esp32_s3_l298n/
  esp32_s3_l298n.ino             # ESP32-S3 + L298N firmware
```

---

## 1. Python setup

```bash
cd pathfinding-visualization-robot
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Flow:
1. Enter maze size (default 21)
2. Pick algorithm
3. Watch the search + green path
4. Choose `y` / `d` / `n` to drive the robot (or dry-run)

Tune `CELL_MS` and `TURN_MS` in `config.py` so one step ≈ one cell and a turn ≈ 90°.

---

## 2. Electronics (ESP32-S3 + L298N)

| L298N pin | ESP32-S3 GPIO (default sketch) |
|-----------|--------------------------------|
| IN1       | 10 |
| IN2       | 11 |
| IN3       | 12 |
| IN4       | 13 |
| ENA       | 14 (PWM left) |
| ENB       | 21 (PWM right) |
| GND       | GND (must share ground with ESP) |

- Motor battery / supply goes to L298N **12V** (or motor rated supply) — **not** the ESP 3.3V pin.
- Jump ENA/ENB headers **removed** if you want PWM speed control (sketch drives them).
- If motors spin the wrong way, swap that motor’s two wires or swap IN1/IN2 (or IN3/IN4).

Edit pins at the top of `firmware/esp32_s3_l298n/esp32_s3_l298n.ino` if your wiring differs.

---

## 3. Flash firmware

1. Arduino IDE → Board: **ESP32S3 Dev Module**
2. Set `ssid` / `password` in the `.ino`
3. Upload, open Serial Monitor @ 115200
4. Copy the printed IP into `robot_client.py` → `ESP32_IP`

Quick test:

```bash
python robot_client.py
```

Should print a successful PING/PONG. Then:

```bash
python -c "from robot_client import execute_commands; execute_commands(['FORWARD:400','LEFT:320','FORWARD:400','STOP'], dry_run=False)"
```

---

## 4. How path → motors works

1. Solver returns a list of cells `(row, col)` from start → goal  
2. `path_to_commands` assumes the robot starts facing **EAST** and emits timed commands:
   - `LEFT:320` / `RIGHT:320` for 90° pivots  
   - `FORWARD:450` for one cell  
3. ESP32 runs each timed move, then stops  

If the robot overshoots, lower `CELL_MS`. If turns are short of 90°, raise `TURN_MS`.

---

## Commands the ESP understands

| Command | Meaning |
|---------|---------|
| `FORWARD` / `BACKWARD` / `LEFT` / `RIGHT` / `STOP` | Continuous until next command |
| `FORWARD:400` | Forward 400 ms then auto-STOP |
| `LEFT:350` / `RIGHT:350` | Pivot for N ms |
| `PING` | Reply `PONG` |

---

## Safety

- First runs: use **dry-run** (`d`) and lift the drive wheels off the ground.
- Keep a way to cut motor power (switch on the battery).
- Don’t power motors from the ESP USB port.

---

## Pushing to GitHub

This folder is ready to become its own repo (or replace `pathfinding-visualizer`):

```bash
git init
git add .
git commit -m "Complete pathfinding visualizer with ESP32-S3 + L298N drive"
gh repo create pathfinding-visualization-robot --public --source=. --push
```
