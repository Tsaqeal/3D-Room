# 3D Room with Door, Window, and Fireplace
# This code creates a 3D representation of a room with a door, window, and fireplace using Matplotlib.
# The user is prompted to input the dimensions of the room, and the code generates a 3D plot of the room with the specified features.
# Import necessary libraries

import numpy as np


from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

# Get user input for wall measurements and ceiling height
# X-direction
wall1 = float(input("Enter the length of the first wall (in meters): "))
# Y-direction
wall2 = float(input("Enter the length of the second wall (in meters): "))
# Z-direction
height = float(input("Enter the height of the ceiling (in meters): "))

# Define the vertices of the room
vertices = [
    [0, 0, 0],               # 0
    [wall1, 0, 0],           # 1
    [wall1, wall2, 0],       # 2
    [0, wall2, 0],           # 3
    [0, 0, height],          # 4
    [wall1, 0, height],      # 5
    [wall1, wall2, height],  # 6
    [0, wall2, height],      # 7
]

# Define the 6 faces of the room (walls, ceiling, floor)   vertices are  like dot in a 3D space, by drawing lines between them we create the walls, ceiling and floor
faces = [
    [vertices[0], vertices[1], vertices[5],
        vertices[4]],  # Wall 1 (front wall)
    [vertices[1], vertices[2], vertices[6],
        vertices[5]],  # Wall 2 (right wall)
    [vertices[2], vertices[3], vertices[7], vertices[6]],  # Wall 3 (back wall)
    [vertices[3], vertices[0], vertices[4], vertices[7]],  # Wall 4 (left)
    [vertices[4], vertices[5], vertices[6], vertices[7]],  # Ceiling
    [vertices[0], vertices[1], vertices[2], vertices[3]],  # Floor
]

# Define a door on Wall 1 (front wall)
door_width = 1.0
door_height = 2.0
door_offset = 0.5  # meters from the left side of Wall 1

door = [
    [door_offset, 0, 0],
    [door_offset + door_width, 0, 0],
    [door_offset + door_width, 0, door_height],
    [door_offset, 0, door_height]
]

# Define a window on Wall 3 (back wall)
window_width = 1.5
window_height = 0.8
window_offset_x = 0.25     # meters from left side of back wall
window_offset_z = 1.5      # meters above the floor

window = [
    [window_offset_x + window_width, wall2, window_offset_z + window_height],
    [window_offset_x, wall2, window_offset_z + window_height],
    [window_offset_x, wall2, window_offset_z],
    [window_offset_x + window_width, wall2, window_offset_z]
]
# Define a fireplace on Wall 2 (right wall)
# The fireplace will be a rectangular prism with a depth towards Wall 4
# and will be positioned at a certain offset from the bottom of Wall 2.
fireplace_depth = 0.50  # Depth of the fireplace towards Wall 4
fireplace_offset = 1  # Distance from the bottom of Wall 2
fireplace_width = 1.70  # Width of the fireplace
fireplace_height = height  # Height of the fireplace

fireplace = [
    [wall1, fireplace_offset, 0],  # Bottom-front-left
    [wall1, fireplace_offset + fireplace_width, 0],  # Bottom-front-right
    [wall1 - fireplace_depth, fireplace_offset +
        fireplace_width, 0],  # Bottom-back-right
    [wall1 - fireplace_depth, fireplace_offset, 0],  # Bottom-back-left
    [wall1, fireplace_offset, fireplace_height],  # Top-front-left
    [wall1, fireplace_offset + fireplace_width,
        fireplace_height],  # Top-front-right
    [wall1 - fireplace_depth, fireplace_offset +
        fireplace_width, fireplace_height],  # Top-back-right
    [wall1 - fireplace_depth, fireplace_offset, fireplace_height],  # Top-back-left
]

# Draw the updated fireplace
fireplace_faces = [
    [fireplace[0], fireplace[1], fireplace[5], fireplace[4]],  # Front face
    [fireplace[1], fireplace[2], fireplace[6], fireplace[5]],  # Right face
    [fireplace[2], fireplace[3], fireplace[7], fireplace[6]],  # Back face
    [fireplace[3], fireplace[0], fireplace[4], fireplace[7]],  # Left face
    [fireplace[4], fireplace[5], fireplace[6], fireplace[7]],  # Top face
    [fireplace[0], fireplace[1], fireplace[2], fireplace[3]],  # Bottom face
]
# Calculate the area of the room in square meters
area = wall1 * wall2
floor_area = area  # Area of the floor (length * width)

# Create a 3D plot
fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

# Draw room faces
for face in faces:
    poly3d = [[tuple(point) for point in face]]
    ax.add_collection3d(Poly3DCollection(
        poly3d, facecolors='lightgrey', alpha=0.5, edgecolor='black'))

# Draw the door
ax.add_collection3d(Poly3DCollection(
    [door], facecolors='saddlebrown', edgecolor='black', alpha=1.0))


# Draw the window
ax.add_collection3d(Poly3DCollection(
    [window], facecolors='skyblue', edgecolor='black', alpha=0.6))

# Draw the fireplace
for face in fireplace_faces:
    poly3d = [[tuple(point) for point in face]]
    ax.add_collection3d(Poly3DCollection(
        poly3d, facecolors='darkred', edgecolor='black', alpha=1.0))


# Draw the square meters of the room
ax.text2D(0.1, 0.95, f"Room Area: {wall1 * wall2:.2f} m²",
          transform=ax.transAxes, fontsize=12, color='black')


# Set plot limits
ax.set_xlim([0, wall1])  # X-axis limits (length of Wall 1)
ax.set_ylim([0, wall2])  # Y-axis limits (length of Wall 2)
ax.set_zlim([0, height])  # Z-axis limits (height of the room)
ax.set_box_aspect([wall1, wall2, height])  # Equal aspect ratio

# Label the axes
ax.set_xlabel('Length (m)')  # X-axis for Wall 1
ax.set_ylabel('Width (m)')  # Y-axis for Wall 2
ax.set_zlabel('Height (m)')  # Z-axis for Ceiling Height
# ax.view_init(elev=210, azim=30)   Optional Set the viewing angle for better visualization
ax.set_title('3D Room with Door  Window and fireplace')  # Title of the plot

# ax.grid(False)    Optional  Disable the grid for better visibility
# ax.set_axis_off() Optional  Hide the axes for a cleaner look
plt.show()
# The code above creates a 3D representation of a room with a door, window, and fireplace using Matplotlib.
