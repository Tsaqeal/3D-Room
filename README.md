# 🏠 3D Room Visualization Tool (Python + Matplotlib)

A fully interactive 3D room visualization built in Python using Matplotlib.  
This tool allows users to generate a custom 3D room with:

- Multiple **doors**
- Multiple **windows**
- Optional **fireplace**
- Optional **skirting boards**
- Auto-calculated **paintable wall area**, **ceiling area**, **door & window area**, etc.
- A clean 2-panel layout showing the **3D view** and a **full data summary**

This started as a small learning experiment — and grew into a complete geometry + validation tool powered by Python.

---

## 📸 Screenshot

<img width="1503" height="773" alt="image" src="https://github.com/user-attachments/assets/14f98519-b3a0-4431-80d7-33084c199b4e" />



---

## ✨ Features

### 🧱 Room Structure
- Custom room dimensions (length × width × height)
- Dynamic 3D rendering using Matplotlib
- Wall, floor, and ceiling faces
- Light-blue painted ceiling

### 🚪 Doors
- Multiple doors per room
- Custom size, location, and wall assignment
- Automatic overlap prevention
- Correct subtraction from wall paint area
- Labels (“Door 1”, “Door 2”, ...)

### 🪟 Windows
- Multiple windows per room
- Custom height, width, wall, offset, and bottom height
- Light purple color
- Automatic overlap prevention
- Correct subtraction from wall area
- Labels (“Window 1”, “Window 2”, ...)

### 🔥 Fireplace
- Optional
- Placed on user-selected wall
- Inward facing depth
- No top area counted (sits against ceiling)
- Adds fireplace wall area back into wall calculations

### 🪵 Skirting Boards
- Optional
- Custom height
- Automatically cuts out door spans
- Visualized in dim gray color

### 📐 Area Calculation Panel (Right Side)
Automatically calculates:

- Total gross wall area  
- Net wall area (minus doors, minus windows, plus fireplace)  
- Ceiling area  
- Skirting board area  
- Total door area  
- Total window area  
- Fireplace additional wall area  

All displayed in a clean monospace info panel.

---

## 🧮 Technical Highlights
- Fully parametric geometry  
- Validation for:
  - wall bounds  
  - overlapping features  
  - height & width constraints  
  - fireplace inward depth  
- Dynamic Matplotlib object creation  
- 3D coordinate calculations  
- Clean subplot layout  
- Labels positioned automatically based on geometry  

---

## 🚀 Installation

### Requirements
- Python 3.8+
- Matplotlib
- NumPy

### Install dependencies
```bash
pip install matplotlib numpy

```


▶️ Usage

Run the script:

```bash
python 3d_room.py
```


Then follow the prompts:

Room size

Number of doors

Door dimensions + wall + offset

Number of windows

Window dimensions + wall + offset + bottom height

Optional fireplace

Optional skirting

The 3D visualization + info panel will appear when complete.

🧠 Project Evolution

This project grew step-by-step through continuous learning and prompt engineering.

v1 — Initial Version

Hardcoded room

One door

One window

One fireplace

No input validation

No labels

No area calculations

(Code included below in “Previous Version”)

v2 — User Input for Room Size

v3 — Multiple Doors

v4 — Multiple Windows

v5 — Fireplace on any wall

v6 — Skirting Boards

v7 — Wall, Door, Window Labels

v8 — Two-panel layout (3D + info panel)

v9 — Full area calculations

v10 — Final Polished Version (current)

🏛 Previous Version (Before Major Updates)

This was the first version of the project — simple and static.
Included here to show project evolution and learning progress.

<details <summary>Click to expand</summary>

```python # 3D Room with Door, Window, and Fireplace
# This code creates a 3D representation of a room with a door, window, and fireplace using Matplotlib.
# The user is prompted to input the dimensions of the room, and the code generates a 3D plot of the room with the specified features.

import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

wall1 = float(input("Enter the length of the first wall (in meters): "))
wall2 = float(input("Enter the length of the second wall (in meters): "))
height = float(input("Enter the height of the ceiling (in meters): "))

vertices = [
    [0, 0, 0],
    [wall1, 0, 0],
    [wall1, wall2, 0],
    [0, wall2, 0],
    [0, 0, height],
    [wall1, 0, height],
    [wall1, wall2, height],
    [0, wall2, height],
]

faces = [
    [vertices[0], vertices[1], vertices[5], vertices[4]],
    [vertices[1], vertices[2], vertices[6], vertices[5]],
    [vertices[2], vertices[3], vertices[7], vertices[6]],
    [vertices[3], vertices[0], vertices[4], vertices[7]],
    [vertices[4], vertices[5], vertices[6], vertices[7]],
    [vertices[0], vertices[1], vertices[2], vertices[3]],
]

door_width = 1.0
door_height = 2.0
door_offset = 0.5

door = [
    [door_offset, 0, 0],
    [door_offset + door_width, 0, 0],
    [door_offset + door_width, 0, door_height],
    [door_offset, 0, door_height]
]

window_width = 1.5
window_height = 0.8
window_offset_x = 0.25
window_offset_z = 1.5

window = [
    [window_offset_x + window_width, wall2, window_offset_z + window_height],
    [window_offset_x, wall2, window_offset_z + window_height],
    [window_offset_x, wall2, window_offset_z],
    [window_offset_x + window_width, wall2, window_offset_z]
]

fireplace_depth = 0.50
fireplace_offset = 1
fireplace_width = 1.70
fireplace_height = height

fireplace = [
    [wall1, fireplace_offset, 0],
    [wall1, fireplace_offset + fireplace_width, 0],
    [wall1 - fireplace_depth, fireplace_offset + fireplace_width, 0],
    [wall1 - fireplace_depth, fireplace_offset, 0],
    [wall1, fireplace_offset, fireplace_height],
    [wall1, fireplace_offset + fireplace_width, fireplace_height],
    [wall1 - fireplace_depth, fireplace_offset + fireplace_width, fireplace_height],
    [wall1 - fireplace_depth, fireplace_offset, fireplace_height],
]

fireplace_faces = [
    [fireplace[0], fireplace[1], fireplace[5], fireplace[4]],
    [fireplace[1], fireplace[2], fireplace[6], fireplace[5]],
    [fireplace[2], fireplace[3], fireplace[7], fireplace[6]],
    [fireplace[3], fireplace[0], fireplace[4], fireplace[7]],
    [fireplace[4], fireplace[5], fireplace[6], fireplace[7]],
    [fireplace[0], fireplace[1], fireplace[2], fireplace[3]],
]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for face in faces:
    poly3d = [[tuple(point) for point in face]]
    ax.add_collection3d(Poly3DCollection(poly3d, facecolors='lightgrey', alpha=0.5))

ax.add_collection3d(Poly3DCollection([door], facecolors='saddlebrown'))
ax.add_collection3d(Poly3DCollection([window], facecolors='skyblue'))

for face in fireplace_faces:
    poly3d = [[tuple(point) for point in face]]
    ax.add_collection3d(Poly3DCollection(poly3d, facecolors='darkred'))

ax.set_xlim(0, wall1)
ax.set_ylim(0, wall2)
ax.set_zlim(0, height)
ax.set_box_aspect([wall1, wall2, height])

ax.set_title('3D Room with Door, Window and Fireplace')
plt.show()

```
</details> <!

🛠 Future Improvements

Planned enhancements:

- Export areas to CSV/JSON

- Add furniture objects (tables, chairs, sofa)

- Add lighting elements

- Add texture mapping (wood floor, painted walls, brick fireplace)

- GUI interface (Tkinter/PyQt)

- Camera orbit animation

- Save high-resolution screenshots automatically

👨‍💻 Author

Vasileios Tsakalos
🔗 GitHub: https://github.com/Tsaqeal

🔗 LinkedIn: https://www.linkedin.com/in/vasileios-tsakalos/

⭐ How to Support

If you like the project, feel free to ⭐ star the repo — it really helps!

