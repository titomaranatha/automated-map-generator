import geopandas as gpd
from shapely.geometry import Polygon, LineString
import numpy as np

def create_sample_data(crs="EPSG:32633"):
    # Create sample land use areas
    landuse_data = {
        'geometry': [
            Polygon([(0, 0), (1000, 0), (1000, 1000), (0, 1000)]),
            Polygon([(1000, 0), (2000, 0), (2000, 1000), (1000, 1000)])
        ],
        'category': ['Residential', 'Commercial']
    }
    landuse = gpd.GeoDataFrame(landuse_data, crs=crs)
    
    # Create sample rivers
    river_data = {
        'geometry': [
            LineString([(500, 500), (1500, 500)]),
            LineString([(200, 800), (1800, 800)])
        ],
        'name': ['Main River', 'North Stream']
    }
    rivers = gpd.GeoDataFrame(river_data, crs=crs)
    
    # Create sample roads
    road_data = {
        'geometry': [
            LineString([(0, 200), (2000, 200)]),
            LineString([(1000, 0), (1000, 1000)])
        ],
        'type': ['Highway', 'Main Street']
    }
    roads = gpd.GeoDataFrame(road_data, crs=crs)
    
    return {'landuse': landuse, 'rivers': rivers, 'roads': roads}

if __name__ == '__main__':
    data = create_sample_data()
    os.makedirs('example_data', exist_ok=True)
    for name, gdf in data.items():
        gdf.to_file(f'example_data/{name}.shp')
    print("Example data created in 'example_data' directory")