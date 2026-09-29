
import numpy as np
import matplotlib.pyplot as plt

from scipy.spatial import Voronoi
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PolyCollection

# =================================
# Configuration
# =================================

numCells = 100
numOuter = 10
numInner = 10
width = 500

total = numCells + numOuter + numInner
outerRadius = width / 2

# Animation settings
rotation_speed = 3    # Degrees per frame
interval = 30         # Milliseconds between frames

# =================================
# Generate golden ratio points
# =================================

points = []

for i in range(total):
    f = i / total
    a = i * 1.6180339887

    distance = f * outerRadius

    x = -np.cos(a * 2 * np.pi) * distance
    y = np.sin(a * 2 * np.pi) * distance

    points.append([x, y])

points = np.array(points)

# =================================
# Create Voronoi diagram
# =================================

vor = Voronoi(points)


def voronoi_finite_polygons_2d(vor, radius=None):

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)

    if radius is None:
        radius = np.ptp(vor.points, axis=0).max() * 2

    all_ridges = {}

    for (p1, p2), (v1, v2) in zip(
        vor.ridge_points,
        vor.ridge_vertices
    ):
        all_ridges.setdefault(p1, []).append(
            (p2, v1, v2)
        )
        all_ridges.setdefault(p2, []).append(
            (p1, v1, v2)
        )

    for p1, region_index in enumerate(vor.point_region):

        vertices = vor.regions[region_index]

        if all(v >= 0 for v in vertices):
            new_regions.append(vertices)
            continue

        ridges = all_ridges[p1]

        new_region = [
            v for v in vertices if v >= 0
        ]

        for p2, v1, v2 in ridges:

            if v1 >= 0 and v2 >= 0:
                continue

            v = v1 if v1 >= 0 else v2

            tangent = (
                vor.points[p2] - vor.points[p1]
            )

            tangent /= np.linalg.norm(tangent)

            normal = np.array([
                -tangent[1],
                tangent[0]
            ])

            midpoint = (
                vor.points[p1] + vor.points[p2]
            ) / 2

            direction = (
                np.sign(
                    np.dot(midpoint - center, normal)
                ) * normal
            )

            far_point = (
                vor.vertices[v] + direction * radius
            )

            new_vertices.append(
                far_point.tolist()
            )

            new_region.append(
                len(new_vertices) - 1
            )

        # Sort vertices counterclockwise
        polygon = np.asarray([
            new_vertices[v]
            for v in new_region
        ])

        c = polygon.mean(axis=0)

        angles = np.arctan2(
            polygon[:, 1] - c[1],
            polygon[:, 0] - c[0]
        )

        new_region = np.array(new_region)[
            np.argsort(angles)
        ]

        new_regions.append(
            new_region.tolist()
        )

    return new_regions, np.asarray(new_vertices)


regions, vertices = voronoi_finite_polygons_2d(
    vor,
    radius=outerRadius * 5
)

# Create polygons
polygons = [
    vertices[region]
    for region in regions
]

# =================================
# Assign point colors
# =================================

colors = []

for x, y in points:

    angle = np.arctan2(y, x)

    if -np.pi / 4 <= angle < np.pi / 4:
        color = "#00ff55"       # Green

    elif np.pi / 4 <= angle < 3 * np.pi / 4:
        color = "#2929ff"       # Blue

    elif (
        angle >= 3 * np.pi / 4
        or angle < -3 * np.pi / 4
    ):
        color = "#00ffff"       # Cyan

    else:
        color = "#ff2020"       # Red

    colors.append(color)

# =================================
# Setup plot
# =================================

fig, ax = plt.subplots(figsize=(8, 8))

fig.patch.set_facecolor("black")
ax.set_facecolor("black")

ax.set_xlim(
    -outerRadius * 1.1,
    outerRadius * 1.1
)

ax.set_ylim(
    -outerRadius * 1.1,
    outerRadius * 1.1
)

ax.set_aspect("equal")
ax.axis("off")

# Draw Voronoi cells
cells = PolyCollection(
    polygons,
    facecolors="black",
    edgecolors="#555555",
    linewidths=0.9
)

ax.add_collection(cells)

# Draw colored center points
scatter = ax.scatter(
    points[:, 0],
    points[:, 1],
    c=colors,
    s=12,
    zorder=3
)

plt.tight_layout(pad=0)

# =================================
# Ninja star rotation animation
# =================================

def animate(frame):

    # Calculate rotation angle
    angle = np.radians(
        frame * rotation_speed
    )

    # Rotation matrix
    rotation = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle),  np.cos(angle)]
    ])

    # Rotate every polygon
    rotated_polygons = [
        polygon @ rotation.T
        for polygon in polygons
    ]

    cells.set_verts(rotated_polygons)

    # Rotate every point
    rotated_points = points @ rotation.T

    scatter.set_offsets(rotated_points)

    return cells, scatter


ani = FuncAnimation(
    fig,
    animate,
    frames=120,
    interval=interval,
    repeat=True,
    blit=False
)

# =================================
# Display animation
# =================================

plt.show()
