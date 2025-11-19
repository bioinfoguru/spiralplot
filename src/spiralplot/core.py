import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def spiralplot(data, x, y, spiral, ax=None, cmap='viridis', color=None, scale=1.0, spiral_scale=0.1, spiral_colors=None, **kwargs):
    """
    Create a scatter plot where each point is represented by a spiral glyph.
    
    Parameters
    ----------
    data : pd.DataFrame
        Input data structure.
    x : str
        Column name for the x-axis position.
    y : str
        Column name for the y-axis position.
    spiral : str or list of str
        Column name(s) for the variable(s) that determine the spiral properties.
        If a single string, behaves as before.
        If a list of two strings, the total number of dots is the sum of values in both columns.
        The dots corresponding to the first column will have one color, and the second another.
    ax : matplotlib.axes.Axes, optional
        Axes object to draw the plot onto, otherwise uses the current Axes.
    cmap : str, optional
        Colormap for the spirals if color mapping is used (currently uniform per spiral).
        Ignored if `color` is provided or if `spiral` is a list of two columns.
    color : str or tuple, optional
        Single color to use for all spirals. Overrides `cmap`.
        Ignored if `spiral` is a list of two columns.
    scale : float, optional
        Global scaling factor for the size of the spirals.
    spiral_scale : float, optional
        Factor to control the spacing of dots within the spiral.
    spiral_colors : list of str/tuple, optional
        List of two colors to use when `spiral` contains two columns. 
        Defaults to ['blue', 'red'] if not provided.
    **kwargs
        Other keyword arguments passed to matplotlib.pyplot.scatter.
        
    Returns
    -------
    ax : matplotlib.axes.Axes
        The Axes object with the plot drawn onto it.
    """
    if ax is None:
        ax = plt.gca()
        
    # Extract data
    x_vals = data[x].values
    y_vals = data[y].values
    
    # Handle single vs dual spiral columns
    if isinstance(spiral, list) and len(spiral) == 2:
        s_col1, s_col2 = spiral
        s_vals1 = data[s_col1].values
        s_vals2 = data[s_col2].values
        
        # Ensure numeric
        if not np.issubdtype(s_vals1.dtype, np.number):
             s_vals1 = pd.factorize(s_vals1)[0] + 1
        if not np.issubdtype(s_vals2.dtype, np.number):
             s_vals2 = pd.factorize(s_vals2)[0] + 1
             
        # Total value for normalization
        s_vals_total = s_vals1 + s_vals2
        is_dual = True
        
        if spiral_colors is None:
            spiral_colors = ['blue', 'red']
    else:
        if isinstance(spiral, list):
            spiral = spiral[0] # Fallback if list of 1
            
        s_vals = data[spiral].values
        # Normalize spiral values to determine number of points or length
        if not np.issubdtype(s_vals.dtype, np.number):
             s_vals = pd.factorize(s_vals)[0] + 1
        s_vals_total = s_vals
        is_dual = False

    # Normalize s_vals_total to a reasonable range of points
    s_min, s_max = s_vals_total.min(), s_vals_total.max()
    if s_max > s_min:
        # Map to range [10, 100]
        n_points_total = 10 + (s_vals_total - s_min) / (s_max - s_min) * 90
    else:
        n_points_total = np.full_like(s_vals_total, 50)
        
    n_points_total = n_points_total.astype(int)
    
    all_x = []
    all_y = []
    all_c = [] 
    
    for i in range(len(data)):
        cx, cy = x_vals[i], y_vals[i]
        n = n_points_total[i]
        
        # Generate spiral
        theta = np.linspace(0, n * 0.2, n)
        r = scale * 0.1 * theta 
        
        sx = cx + r * np.cos(theta)
        sy = cy + r * np.sin(theta)
        
        all_x.extend(sx)
        all_y.extend(sy)
        
        # Color logic
        if is_dual:
            # Calculate proportion of points for first column
            v1 = s_vals1[i]
            v2 = s_vals2[i]
            total = v1 + v2
            if total > 0:
                n1 = int(n * (v1 / total))
            else:
                n1 = 0
            n2 = n - n1
            
            all_c.extend([spiral_colors[0]] * n1)
            all_c.extend([spiral_colors[1]] * n2)
        else:
            val = s_vals_total[i]
            if color is not None:
                all_c.extend([color] * n)
            else:
                all_c.extend([val] * n)
        
    # Plot
    if is_dual or color is not None:
        # When using explicit colors (dual or single override), we pass the list of colors directly
        scatter = ax.scatter(all_x, all_y, c=all_c, s=5*spiral_scale, **kwargs)
    else:
        # When using cmap
        scatter = ax.scatter(all_x, all_y, c=all_c, cmap=cmap, s=5*spiral_scale, **kwargs)
        if np.issubdtype(s_vals_total.dtype, np.number):
            plt.colorbar(scatter, ax=ax, label=spiral)
        
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    title_label = f"{spiral[0]} + {spiral[1]}" if isinstance(spiral, list) else spiral
    ax.set_title(f"Spiral Glyph Plot (size by {title_label})")
    
    return ax

