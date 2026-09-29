
# Golden Ratio Voronoi Pattern

A Python project that generates a sunflower-like pattern using the golden ratio and Voronoi diagrams.

The project generates points using the golden ratio and connects them into polygonal cells to create a Voronoi pattern.

## Preview

The output consists of:

- Golden-ratio-based point distribution.
- Voronoi cells with polygon boundaries.
- Black background with gray cell borders.
- Colored points representing the center of each cell.

## How It Works

### 1. Golden Ratio Point Generation

The points are generated using the golden ratio:

\[
\phi = \frac{1+\sqrt{5}}{2}
\]

For each point \(i\):

\[
r_i = \frac{i}{N}\cdot R
\]

\[
\theta_i = 2\pi\phi i
\]

The coordinates are:

\[
x_i=-r_i\cos(\theta_i)
\]

\[
y_i=r_i\sin(\theta_i)
\]

Where:

- `N` is the total number of points.
- `R` is the outer radius.
- `i` is the point index.

### 2. Voronoi Diagram

SciPy's Voronoi implementation is used to divide the space into polygonal cells.

Each cell contains one generated point, and every location inside that cell is closer to its corresponding point than to any other point.

## Requirements

- Python 3
- NumPy
- SciPy
- Matplotlib

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/golden-ratio-voronoi.git
cd golden-ratio-voronoi
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python3 pattern.py
```

A graphical window will open displaying the Voronoi pattern.

## Configuration

You can change the following variables at the top of `pattern.py`:

```python
numCells = 100
numOuter = 10
numInner = 10
width = 500
```

- `numCells`: Number of main points.
- `numOuter`: Additional outer points.
- `numInner`: Additional inner points.
- `width`: Controls the overall pattern radius.

## Technologies Used

- Python
- NumPy
- SciPy
- Matplotlib

## License

This project is open source and available under the MIT License.
