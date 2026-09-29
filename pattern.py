
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi

# Input values (same as your original code)
numCells = 100
numOuter = 10
numInner = 10
width = 500

total = numCells + numOuter + numInner
outerRadius = width / 2

# Generate points using your exact formula
points = []

for i in range(total):
    f = i / total
    a = i * 1.6180339887

    distance = f * outerRadius

    x = -np.cos(a * 2 * np.pi) * distance
    y = np.sin(a * 2 * np.pi) * distance

    points.append([x, y])

points = np.array(points)

# Create Voronoi diagram
vor = Voronoi(points)

# Convert infinite Voronoi regions into finite polygons
def voronoi_finite_polygons_2d(vor, radius=None):
    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)

    if radius is None:
        radius = vor.points.ptp().max() * 2

    # Map ridges to their corresponding points
    all_ridges = {}

    for (p1, p2), (v1, v2) in zip(
        vor.ridge_points, vor.ridge_vertices
    ):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    for p1, region_index in enumerate(vor.point_region):
        vertices = vor.regions[region_index]

        if all(v >= 0 for v in vertices):
            new_regions.append(vertices)
            continue

        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v1 >= 0 and v2 >= 0:
                continue

            # Find the missing endpoint
            v = v1 if v1 >= 0 else v2

            tangent = vor.points[p2] - vor.points[p1]
            tangent /= np.linalg.norm(tangent)

            normal = np.array([-tangent[1], tangent[0]])

            midpoint = (vor.points[p1] + vor.points[p2]) / 2
            direction = np.sign(np.dot(midpoint - center, normal)) * normal

            far_point = vor.vertices[v] + direction * radius

            new_vertices.append(far_point.tolist())
            new_region.append(len(new_vertices) - 1)

        # Sort polygon vertices counterclockwise
        polygon = np.asarray([new_vertices[v] for v in new_region])
        c = polygon.mean(axis=0)

        angles = np.arctan2(
            polygon[:, 1] - c[1],
            polygon[:, 0] - c[0]
        )

        new_region = np.array(new_region)[np.argsort(angles)]

        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)


# Generate finite polygons
regions, vertices = voronoi_finite_polygons_2d(
    vor, radius=outerRadius * 5
)

# Plot the pattern
fig, ax = plt.subplots(figsize=(8, 8))

fig.patch.set_facecolor("black")
ax.set_facecolor("black")

# Draw each Voronoi cell
for region in regions:
    polygon = vertices[region]

    ax.fill(
        polygon[:, 0],
        polygon[:, 1],
        facecolor="black",
        edgecolor="#555555",
        linewidth=0.9
    )

# Color dots by their angular position
for x, y in points:
    angle = np.arctan2(y, x)

    if -np.pi / 4 <= angle < np.pi / 4:
        color = "#00ff55"      # Right: green
    elif np.pi / 4 <= angle < 3 * np.pi / 4:
        color = "#2929ff"      # Top: blue
    elif angle >= 3 * np.pi / 4 or angle < -3 * np.pi / 4:
        color = "#00ffff"      # Left: cyan
    else:
        color = "#ff2020"      # Bottom: red

    ax.scatter(x, y, color=color, s=12, zorder=3)

# Set the viewing area
ax.set_xlim(-outerRadius * 1.1, outerRadius * 1.1)
ax.set_ylim(-outerRadius * 1.1, outerRadius * 1.1)

ax.set_aspect("equal")
ax.axis("off")

plt.tight_layout(pad=0)

# Display the pattern
plt.show()
