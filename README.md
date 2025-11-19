# Spiral Plot

A Python package to create scatter plots where each point is represented by a spiral glyph. This is useful for visualizing a third dimension of data (magnitude, duration, etc.) as the complexity or size of a spiral at a specific 2D location. It also supports visualizing two values simultaneously using a dual-colored spiral.

## Installation

You can install this package locally using pip:

```bash
pip install .
```

Or directly from GitHub:

```bash
pip install git+https://github.com/bioinfoguru/spiralplot.git
```

## Usage

### Single Spiral Value

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from spiralplot import spiralplot

# Create sample data
n = 20
df = pd.DataFrame({
    'x_pos': np.random.rand(n) * 100,
    'y_pos': np.random.rand(n) * 100,
    'magnitude': np.random.rand(n) * 50 + 10 
})

plt.figure(figsize=(10, 10))
spiralplot(
    data=df,
    x='x_pos',
    y='y_pos',
    spiral='magnitude',
    cmap='magma',
    scale=0.5
)
plt.show()
```

### Dual Spiral Values

You can visualize two values at once. The total length of the spiral represents the sum of the values, and the spiral is split into two colors proportional to each value.

```python
df['magnitude2'] = np.random.rand(n) * 50 + 10

plt.figure(figsize=(10, 10))
spiralplot(
    data=df,
    x='x_pos',
    y='y_pos',
    spiral=['magnitude', 'magnitude2'], # Pass list of two columns
    spiral_colors=['blue', 'red'],      # Colors for each part
    scale=0.5
)
plt.show()
```

## API

### `spiralplot(data, x, y, spiral, ax=None, cmap='viridis', color=None, scale=1.0, spiral_scale=0.1, spiral_colors=None, **kwargs)`

- `data`: Input pandas DataFrame.
- `x`: Column name for x-axis position.
- `y`: Column name for y-axis position.
- `spiral`: Column name (str) or list of two column names (list of str).
    - If single string: Maps value to spiral length.
    - If list of two strings: Maps sum of values to length, splits spiral into two colors.
- `ax`: Optional matplotlib Axes.
- `cmap`: Colormap for the spirals. Ignored if `color` is provided or if `spiral` is a list.
- `color`: Single color to use for all spirals. Overrides `cmap`. Ignored if `spiral` is a list.
- `scale`: Global scaling factor for the size of the spirals relative to data coordinates.
- `spiral_scale`: Factor to control the size of individual dots within the spiral.
- `spiral_colors`: List of two colors (e.g. `['green', 'orange']`) to use when `spiral` is a list of two columns.
- `**kwargs`: Additional arguments passed to `plt.scatter`.
