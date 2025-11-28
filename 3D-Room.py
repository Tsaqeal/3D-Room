import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

# =========================================================
# VALIDATION & UTILITY HELPERS
# =========================================================


def validate_linear_feature(name, offset, width, wall_length):
    if offset < 0:
        raise ValueError(f"{name} offset cannot be negative.")
    if width <= 0:
        raise ValueError(f"{name} width must be > 0.")
    if offset + width > wall_length:
        raise ValueError(
            f"{name} exceeds wall length: offset({offset}) + width({width}) > wall({wall_length})"
        )


def validate_height(name, bottom, height, ceiling):
    if bottom < 0:
        raise ValueError(f"{name} bottom height cannot be below 0 m.")
    if height <= 0:
        raise ValueError(f"{name} height must be > 0.")
    if bottom + height > ceiling:
        raise ValueError(
            f"{name} exceeds ceiling: bottom({bottom}) + height({height}) > ceiling({ceiling})"
        )


def subtract_interval(segments, a, b):
    """Used to carve out door openings from skirting boards."""
    new_segments = []
    for s, e in segments:
        if b <= s or a >= e:
            new_segments.append([s, e])
        else:
            if a > s:
                new_segments.append([s, a])
            if b < e:
                new_segments.append([b, e])
    return new_segments


def intervals_overlap(a_start, a_end, b_start, b_end):
    """Return True if two [start, end) intervals overlap."""
    return max(a_start, b_start) < min(a_end, b_end)


def ensure_no_overlap(name, wall, offset, width, others):
    """
    Ensure [offset, offset+width) on a given wall does not overlap
    any feature in 'others' that shares that wall.
    Each element in 'others' must have keys: 'wall', 'offset', 'width', 'type'.
    """
    a_start, a_end = offset, offset + width
    for o in others:
        if o["wall"] != wall:
            continue
        b_start = o["offset"]
        b_end = o["offset"] + o["width"]
        if intervals_overlap(a_start, a_end, b_start, b_end):
            raise ValueError(
                f"{name} overlaps with existing {o['type']} on wall {wall} "
                f"([{a_start}, {a_end}) vs {o['type']} [{b_start}, {b_end}))."
            )


# =========================================================
# ROOM INPUT
# =========================================================
wall1 = float(input("Enter the length of Wall 1 (X direction, meters): "))
wall2 = float(input("Enter the length of Wall 2 (Y direction, meters): "))
height = float(input("Enter the room height (meters): "))

# =========================================================
# ROOM GEOMETRY
# =========================================================
vertices = [
    [0, 0, 0], [wall1, 0, 0], [wall1, wall2, 0], [0, wall2, 0],
    [0, 0, height], [wall1, 0, height], [
        wall1, wall2, height], [0, wall2, height]
]

# faces index mapping:
# 0: Wall 1 (front), 1: Wall 2 (right), 2: Wall 3 (back),
# 3: Wall 4 (left), 4: Ceiling, 5: Floor
faces = [
    [vertices[0], vertices[1], vertices[5], vertices[4]],  # 0 - Wall 1 front
    [vertices[1], vertices[2], vertices[6], vertices[5]],  # 1 - Wall 2 right
    [vertices[2], vertices[3], vertices[7], vertices[6]],  # 2 - Wall 3 back
    [vertices[3], vertices[0], vertices[4], vertices[7]],  # 3 - Wall 4 left
    [vertices[4], vertices[5], vertices[6], vertices[7]],  # 4 - Ceiling
    [vertices[0], vertices[1], vertices[2], vertices[3]]   # 5 - Floor
]

# =========================================================
# DOORS
# =========================================================
doors = []
door_area_total = 0.0

num_doors = int(input("\nHow many doors? (0–10): "))

for i in range(num_doors):
    print(f"\nDoor {i+1}:")
    wall = int(input("  Wall (1–4): "))
    offset = float(input("  Offset from wall corner (m): "))
    width = float(input("  Door total width (m): "))
    d_height = float(input("  Door total height (m): "))

    validate_linear_feature("Door", offset, width,
                            wall1 if wall in (1, 3) else wall2)
    validate_height("Door", 0, d_height, height)

    # Prevent overlap with existing doors
    ensure_no_overlap("Door", wall, offset, width, doors)

    if wall == 1:
        verts = [[offset, 0, 0], [offset+width, 0, 0],
                 [offset+width, 0, d_height], [offset, 0, d_height]]
    elif wall == 2:
        verts = [[wall1, offset, 0], [wall1, offset+width, 0],
                 [wall1, offset+width, d_height], [wall1, offset, d_height]]
    elif wall == 3:
        verts = [[offset, wall2, 0], [offset+width, wall2, 0],
                 [offset+width, wall2, d_height], [offset, wall2, d_height]]
    elif wall == 4:
        verts = [[0, offset, 0], [0, offset+width, 0],
                 [0, offset+width, d_height], [0, offset, d_height]]

    doors.append({
        "type": "door",
        "wall": wall,
        "offset": offset,
        "width": width,
        "height": d_height,
        "verts": verts
    })
    door_area_total += width * d_height

# =========================================================
# WINDOWS
# =========================================================
windows = []
window_area_total = 0.0

num_windows = int(input("\nHow many windows? (0–10): "))

for i in range(num_windows):
    print(f"\nWindow {i+1}:")
    wall = int(input("  Wall (1–4): "))
    offset = float(input("  Offset from wall corner (m): "))
    w_width = float(input("  Window width (m): "))
    w_height = float(input("  Window height (m): "))
    bottom = float(input("  Window bottom height above floor (m): "))

    validate_linear_feature("Window", offset, w_width,
                            wall1 if wall in (1, 3) else wall2)
    validate_height("Window", bottom, w_height, height)

    # Prevent overlap with doors and previous windows
    ensure_no_overlap("Window", wall, offset, w_width, doors + windows)

    top = bottom + w_height

    if wall == 1:
        verts = [[offset, 0, bottom], [offset+w_width, 0, bottom],
                 [offset+w_width, 0, top], [offset, 0, top]]
    elif wall == 2:
        verts = [[wall1, offset, bottom], [wall1, offset+w_width,
                                           bottom], [wall1, offset+w_width, top], [wall1, offset, top]]
    elif wall == 3:
        verts = [[offset, wall2, bottom], [offset+w_width, wall2,
                                           bottom], [offset+w_width, wall2, top], [offset, wall2, top]]
    elif wall == 4:
        verts = [[0, offset, bottom], [0, offset+w_width, bottom],
                 [0, offset+w_width, top], [0, offset, top]]

    windows.append({
        "type": "window",
        "wall": wall,
        "offset": offset,
        "width": w_width,
        "height": w_height,
        "bottom": bottom,
        "verts": verts
    })
    window_area_total += w_width * w_height

# =========================================================
# FIREPLACE (NO TOP FACE COUNTED OR DRAWN)
# =========================================================
fireplace_faces = []
fireplace_extra_wall_area = 0.0
has_fire = input("\nIs there a fireplace? (y/n): ").strip().lower()

if has_fire == "y":
    print("\nFireplace:")
    f_wall = int(input("  Wall (1–4): "))
    f_offset = float(input("  Offset from wall corner (m): "))
    f_width = float(input("  Fireplace width (m): "))
    f_depth = float(input("  Fireplace depth inward (m): "))
    f_height = height

    validate_linear_feature("Fireplace", f_offset, f_width,
                            wall1 if f_wall in (1, 3) else wall2)
    ensure_no_overlap("Fireplace", f_wall, f_offset, f_width, doors + windows)

    if f_depth <= 0:
        raise ValueError("Fireplace depth must be > 0.")
    if f_wall in (1, 3) and f_depth > wall2:
        raise ValueError("Fireplace depth exceeds room width.")
    if f_wall in (2, 4) and f_depth > wall1:
        raise ValueError("Fireplace depth exceeds room length.")

    # Build 8 vertices of fireplace prism
    if f_wall == 1:
        x0, x1 = f_offset, f_offset+f_width
        fireplace = [[x0, 0, 0], [x1, 0, 0], [x1, f_depth, 0], [x0, f_depth, 0],
                     [x0, 0, f_height], [x1, 0, f_height], [x1, f_depth, f_height], [x0, f_depth, f_height]]
    elif f_wall == 2:
        y0, y1 = f_offset, f_offset+f_width
        fireplace = [[wall1, y0, 0], [wall1, y1, 0], [wall1-f_depth, y1, 0], [wall1-f_depth, y0, 0],
                     [wall1, y0, f_height], [wall1, y1, f_height], [wall1-f_depth, y1, f_height], [wall1-f_depth, y0, f_height]]
    elif f_wall == 3:
        x0, x1 = f_offset, f_offset+f_width
        fireplace = [[x0, wall2, 0], [x1, wall2, 0], [x1, wall2-f_depth, 0], [x0, wall2-f_depth, 0],
                     [x0, wall2, f_height], [x1, wall2, f_height], [x1, wall2-f_depth, f_height], [x0, wall2-f_depth, f_height]]
    elif f_wall == 4:
        y0, y1 = f_offset, f_offset+f_width
        fireplace = [[0, y0, 0], [0, y1, 0], [f_depth, y1, 0], [f_depth, y0, 0],
                     [0, y0, f_height], [0, y1, f_height], [f_depth, y1, f_height], [f_depth, y0, f_height]]

    f = fireplace
    # No top face – only bottom + 4 vertical faces
    fireplace_faces = [
        [f[0], f[1], f[2], f[3]],  # Bottom
        [f[0], f[1], f[5], f[4]],  # Front
        [f[1], f[2], f[6], f[5]],  # Right
        [f[2], f[3], f[7], f[6]],  # Back (inward)
        [f[3], f[0], f[4], f[7]]   # Left
    ]

    # Extra vertical wall area added by fireplace (2 sides + back)
    fireplace_extra_wall_area = (2 * f_depth + f_width) * f_height

# =========================================================
# SKIRTING BOARDS
# =========================================================
skirting_faces = []
skirting_area = 0.0
has_skirting = input("\nAre there skirting boards? (y/n): ").strip().lower()

if has_skirting == "y":
    skirt_h = float(input("  Skirting height (m): "))

    wall1_segs = [[0, wall1]]
    wall2_segs = [[0, wall2]]
    wall3_segs = [[0, wall1]]
    wall4_segs = [[0, wall2]]

    for d in doors:
        off, w = d["offset"], d["width"]
        if d["wall"] == 1:
            wall1_segs = subtract_interval(wall1_segs, off, off+w)
        elif d["wall"] == 2:
            wall2_segs = subtract_interval(wall2_segs, off, off+w)
        elif d["wall"] == 3:
            wall3_segs = subtract_interval(wall3_segs, off, off+w)
        elif d["wall"] == 4:
            wall4_segs = subtract_interval(wall4_segs, off, off+w)

    for s, e in wall1_segs:
        length = e - s
        skirting_area += length * skirt_h
        skirting_faces.append(
            [[s, 0, 0], [e, 0, 0], [e, 0, skirt_h], [s, 0, skirt_h]])
    for s, e in wall2_segs:
        length = e - s
        skirting_area += length * skirt_h
        skirting_faces.append([[wall1, s, 0], [wall1, e, 0], [
                              wall1, e, skirt_h], [wall1, s, skirt_h]])
    for s, e in wall3_segs:
        length = e - s
        skirting_area += length * skirt_h
        skirting_faces.append([[s, wall2, 0], [e, wall2, 0], [
                              e, wall2, skirt_h], [s, wall2, skirt_h]])
    for s, e in wall4_segs:
        length = e - s
        skirting_area += length * skirt_h
        skirting_faces.append(
            [[0, s, 0], [0, e, 0], [0, e, skirt_h], [0, s, skirt_h]])

# =========================================================
# AREA CALCULATIONS
# =========================================================
wall_gross_area = 2 * (wall1 + wall2) * height
wall_net_area = wall_gross_area - door_area_total - \
    window_area_total + fireplace_extra_wall_area
ceiling_area = wall1 * wall2

# =========================================================
# PLOTTING
# =========================================================
fig = plt.figure(figsize=(15, 7))

# --------- LEFT: 3D VIEW ----------
ax = fig.add_subplot(1, 2, 1, projection="3d")

# Draw room faces with light blue ceiling
for i, face in enumerate(faces):
    if i == 4:  # ceiling
        color = "lightblue"
        alpha = 0.6
    else:
        color = "lightgrey"
        alpha = 0.5
    ax.add_collection3d(
        Poly3DCollection([face], facecolors=color,
                         alpha=alpha, edgecolor="black")
    )

# Doors
for d in doors:
    ax.add_collection3d(
        Poly3DCollection(
            [d["verts"]], facecolors="saddlebrown", edgecolor="black")
    )

# Door labels at center
for i, d in enumerate(doors, 1):
    vx = d["verts"][0][0]
    vy = d["verts"][0][1]
    vz = d["height"] * 0.5
    ax.text(
        vx, vy, vz,
        f"Door {i}",
        color="brown",
        fontsize=9,
        ha="center",
        va="center"
    )

# Windows (light purple)
for w in windows:
    ax.add_collection3d(
        Poly3DCollection([w["verts"]], facecolors="plum",
                         alpha=0.7, edgecolor="black")
    )

# Window labels at center
for i, w in enumerate(windows, 1):
    vx = w["verts"][0][0]
    vy = w["verts"][0][1]
    vz = w["bottom"] + (w["height"] * 0.5)
    ax.text(
        vx, vy, vz,
        f"Window {i}",
        color="purple",
        fontsize=9,
        ha="center",
        va="center"
    )

# Fireplace (no top face)
for f in fireplace_faces:
    ax.add_collection3d(
        Poly3DCollection([f], facecolors="darkred", edgecolor="black")
    )

# Skirting
for s in skirting_faces:
    ax.add_collection3d(
        Poly3DCollection([s], facecolors="dimgray", edgecolor="black")
    )

# Wall labels
ax.text(wall1/2, 0,      height/2, "WALL 1",
        color='black', fontsize=12, ha='center')
ax.text(wall1,   wall2/2, height/2, "WALL 2",
        color='black', fontsize=12, ha='center')
ax.text(wall1/2, wall2,  height/2, "WALL 3",
        color='black', fontsize=12, ha='center')
ax.text(0,       wall2/2, height/2, "WALL 4",
        color='black', fontsize=12, ha='center')
ax.text(wall1/2, wall2/2, 0,        "FLOOR",
        color='black', fontsize=10, ha='center')
ax.text(wall1/2, wall2/2, height,   "CEILING",
        color='black', fontsize=10, ha='center')

ax.set_xlim(0, wall1)
ax.set_ylim(0, wall2)
ax.set_zlim(0, height)
ax.set_box_aspect([wall1, wall2, height])

ax.set_xlabel("Length (m)")
ax.set_ylabel("Width (m)")
ax.set_zlabel("Height (m)")
ax.set_title("3D Room Visualization with Labels")

# --------- RIGHT: INFO PANEL ----------
ax2 = fig.add_subplot(1, 2, 2)
ax2.axis("off")

info = []

info.append("ROOM SIZE:")
info.append(f"  {wall1:.2f} × {wall2:.2f} × {height:.2f} m\n")

info.append("AREAS:")
info.append(f"  Walls gross: {wall_gross_area:.2f} m²")
info.append(
    f"  Walls net (– doors – windows + fireplace): {wall_net_area:.2f} m²")
info.append(f"  Ceiling: {ceiling_area:.2f} m²")
info.append(f"  Skirting: {skirting_area:.2f} m²")
info.append(f"  Doors total: {door_area_total:.2f} m²")
info.append(f"  Windows total: {window_area_total:.2f} m²")
if has_fire == "y":
    info.append(
        f"  Fireplace added wall area: {fireplace_extra_wall_area:.2f} m²")
info.append("")  # blank line

info.append("DOORS:")
if doors:
    for i, d in enumerate(doors, 1):
        info.append(
            f"  {i}. Wall {d['wall']} | offset {d['offset']} m | {d['width']}×{d['height']} m")
else:
    info.append("  None")

info.append("\nWINDOWS:")
if windows:
    for i, w in enumerate(windows, 1):
        info.append(
            f"  {i}. Wall {w['wall']} | offset {w['offset']} m | "
            f"{w['width']}×{w['height']} m | bottom {w['bottom']} m"
        )
else:
    info.append("  None")

info.append("\nFIREPLACE:")
if has_fire == "y":
    info.append(
        f"  Wall {f_wall} | offset {f_offset} m | width {f_width} m | depth {f_depth} m")
else:
    info.append("  None")

info.append("\nSKIRTING:")
if has_skirting == "y":
    info.append(f"  Height: {skirt_h} m")
else:
    info.append("  None")

ax2.text(0.01, 0.99, "\n".join(info), va="top",
         ha="left", fontsize=11, family="monospace")

plt.tight_layout()
plt.show()
