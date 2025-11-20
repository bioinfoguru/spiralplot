import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from spiralplot import spiralplot

def main():
    # Create sample data
    col1 = list(range(4, 10))
    col2 = list(range(4, 10))

    # Third column: squares of the numbers
    squares = [x**2 for x in col1]

    # Build the DataFrame
    df = pd.DataFrame({
        "X": col1,
        "Y": col2,
        "spiral": squares,
        "spiral2": [x*2 for x in col1]
    })
    
    plt.figure(figsize=(10, 10))
    spiralplot(
        data=df,
        x='X',
        y='Y',
#        spiral='spiral',
#        color='blue',
        spiral=['spiral', 'spiral2'], # Two columns
        spiral_colors=['green', 'orange'],
        scale=0.1, # Adjusted scale for this data range
        dpt=30 # Dots per turn
    )
    
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Spiral Glyph Plot (size by spiral + spiral2)")
    
    plt.savefig('spiral_demo_dual.png')
    print("Spiral glyph plot saved to spiral_demo_dual.png")

if __name__ == "__main__":
    main()
