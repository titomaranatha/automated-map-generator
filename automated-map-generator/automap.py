import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib_scalebar.scalebar import ScaleBar
import os

def generate_map(
    layers,
    output_file='output_map.pdf',
    title='Automated Map',
    styles=None,
    figsize=(11, 8.5),
    dpi=300,
    legend_cols=1,
    scale_units='m',
    north_arrow=True
):
    """
    Generate a styled map with multiple layers, legend, and scale bar
    
    Parameters:
    layers (dict): Dictionary of GeoDataFrames with layer names as keys
    output_file (str): Output filename (PDF or PNG)
    title (str): Map title
    styles (dict): Dictionary of style parameters for each layer
    figsize (tuple): Figure dimensions in inches
    dpi (int): Output resolution
    legend_cols (int): Number of columns in legend
    scale_units (str): Units for scale bar ('m', 'km', 'ft')
    north_arrow (bool): Add north arrow
    """
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    # Default styles
    default_styles = {
        'landuse': {'color': '#c0d6c0', 'edgecolor': 'none', 'label': 'Land Use'},
        'rivers': {'color': '#66b3ff', 'linewidth': 1.5, 'label': 'Rivers'},
        'roads': {'color': '#808080', 'linewidth': 0.8, 'label': 'Roads'}
    }
    styles = styles or default_styles
    
    # Plot layers in reverse order (last layer on top)
    for layer_name, gdf in reversed(layers.items()):
        style = styles.get(layer_name, {})
        if gdf.geometry.type.iloc[0] == 'Polygon':
            gdf.plot(ax=ax, **style)
        else:
            gdf.plot(ax=ax, **style)
    
    # Add scale bar
    ax.add_artist(ScaleBar(
        dx=1,  # 1 unit in data coordinates = 1 meter
        units=scale_units,
        location='lower left',
        length_fraction=0.2,
        scale_formats=['{units}']
    ))
    
    # Add north arrow
    if north_arrow:
        ax.annotate('N', xy=(0.95, 0.92), xycoords='axes fraction',
                    fontsize=20, ha='center', va='center',
                    arrowprops=dict(arrowstyle='->', lw=2))
    
    # Create legend
    legend_elements = []
    for layer_name, style in styles.items():
        if 'label' in style:
            if 'color' in style and 'linewidth' in style:
                legend_elements.append(Line2D(
                    [0], [0], 
                    color=style['color'], 
                    lw=style['linewidth'],
                    label=style['label']
                ))
            elif 'color' in style:
                legend_elements.append(plt.Rectangle(
                    (0,0), 1, 1, 
                    fc=style['color'], 
                    ec=style.get('edgecolor', 'none'),
                    label=style['label']
                ))
    
    if legend_elements:
        ax.legend(
            handles=legend_elements,
            loc='upper right',
            ncol=legend_cols,
            frameon=True,
            title='Legend'
        )
    
    # Set title and adjust layout
    ax.set_title(title, fontsize=16, pad=20)
    ax.axis('off')
    plt.tight_layout()
    
    # Save output
    output_ext = os.path.splitext(output_file)[1].lower()
    plt.savefig(output_file, bbox_inches='tight')
    print(f"Map saved to {output_file}")
    plt.close()