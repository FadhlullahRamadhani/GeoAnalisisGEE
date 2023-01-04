import os
import sys
import time
import argparse
import geopandas as gpd
import fiona
import rasterio as rio
from rasterstats import zonal_stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mgwr.gwr import MGWR
from mgwr.sel_bw import Sel_BW
from mgwr.utils import shift_colormap, truncate_colormap
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--raster', '-tif', default='data/raster/vars_2020.tif', help='Input raster data')
    parser.add_argument('--vector', '-shp', default='data/vector/batas_kab_kec_int.shp', help='Input vektor data')
    parser.add_argument('--filepath', '-fp', default='D:/BRIN/Keris_DSLG/2210_MGWR/', help='Path to base directory')
    parser.add_argument('--exp_name', '-exp', default='mgwr', help='Experiment name')
    parser.add_argument('--log', help='Log to file in save folder; use - for stdout (default is log.txt)', metavar='file', default='log.txt')

    args = parser.parse_args()

    BASE_DIR = args.filepath

    folder_results = os.path.join(BASE_DIR, f'result_{args.exp_name}/')
    if not os.path.exists(folder_results):
        os.makedirs(folder_results)
    
    if args.log != '-':
        sys.stdout = open(os.path.join(folder_results, args.log), 'w')
    
    print(args)

    # Path to data
    fp_raster = os.path.join(BASE_DIR, args.raster)
    fp_zones = os.path.join(BASE_DIR, args.vector)

    # Load vector data
    gdf = gpd.read_file(fp_zones)
    crs = gdf.crs
    gdf['x_utm'] = gdf.centroid.x
    gdf['y_utm'] = gdf.centroid.y

    # Load raster data
    with rio.open(fp_raster, "r") as src:
        profile = src.profile
        transform = profile['transform']
        nodata = src.nodata
        band_index = src.indexes
        # Zonal statistics
        vars = []
        zstats_merged = []
        for i in band_index:
            img = src.read(i)
            img[img==nodata] = np.nan # change nodata to nan to avoid inf when computing zonal statistic mean
            zstats = zonal_stats(gdf, img, affine=transform, prefix=f'b{i}_', stats='mean')
            zstats_merged.append(zstats) # zstats_merged is now a 2D list of lists [bands, shapes]
            vars.append(f'b{i}_mean')

    # Flip the dimensions using zip
    zstats_merged_list = list(zip(*zstats_merged))
    # Aggregate into a single list (dimension: shapes) containing bands
    final_zstats = [{k: v for d in s for k, v in d.items()} for s in zstats_merged_list]
    # Convert zonal statistic results to pandas dataframe
    df_zstats = pd.DataFrame(final_zstats)

    # Merge zones and zonal statistics data frame
    gdf = gdf.join(df_zstats)

    # Clean the data
    gdf = gdf.dropna()
    print('Final input data shape: {}'.format(gdf.shape))

    # Prepare datasets input
    y = gdf[vars[0]].values.reshape((-1,1))
    X = gdf[list(vars[1:])].values
    coords = list(zip(gdf['x_utm'],gdf['y_utm']))

    print('Independent variables: {}'.format(X.shape))
    print('Dependent variable: {}'.format(y.shape))

    X = (X - X.mean(axis=0)) / X.std(axis=0)
    y = (y - y.mean(axis=0)) / y.std(axis=0)

    # Calibrate MGWR model
    print('Start MGWR ....')
    start_time = time.time()
    mgwr_selector = Sel_BW(coords, y, X, multi=True)
    mgwr_bw = mgwr_selector.search(multi_bw_min=[2])
    print('MGWR bandwidth: {}'.format(mgwr_bw))
    mgwr_results = MGWR(coords, y, X, mgwr_selector).fit()
    mgwr_results.summary()
    elapsed_time = (time.time() - start_time)/60
    print('MGWR complete. Elapsed time (minutes): '+str(elapsed_time))

    print('Prepare MGWR results for mapping ...')
    # Obtain t-vals filtered based on multiple testing correction
    mgwr_filtered_t = mgwr_results.filter_tvals()

    # Plot MGWR parameters
    for i in band_index:
        if i-1==0:
            param = 'mgwr_intercept'
        else:
            param = f'mgwr_b{i}'
        
        # Add MGWR parameters to GeoDataframe
        gdf[param] = mgwr_results.params[:,i-1]
        
        # Set color map
        vmin = gdf[param].min()
        vmax = gdf[param].max()
        cmap = plt.cm.seismic
        if (vmin < 0) & (vmax < 0): # If all values are negative use the negative half of the colormap
            cmap = truncate_colormap(cmap, 0.0, 0.5)
        elif (vmin > 0) & (vmax > 0): # If all values are positive use the positive half of the colormap
            cmap = truncate_colormap(cmap, 0.5, 1.0)
        else: # Otherwise, there are positive and negative values so the colormap so zero is the midpoint
            cmap = shift_colormap(cmap, start=0.0, midpoint=1 - vmax/(vmax + abs(vmin)), stop=1.)

        # Create scalar mappable for colorbar and stretch colormap across range of data values
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))

        # Plot
        fig, ax = plt.subplots(nrows=1, ncols=1)
        fig.set_size_inches(8, 6)
        ax.set_title(param, fontsize=10)
        gdf.plot(column=param,
            ax=ax,
            legend=True,
            cmap=sm.cmap, vmin=vmin, vmax=vmax, **{'edgecolor':'black', 'alpha':.65})
        if (mgwr_filtered_t[:,0] == 0).any(): #If there are insignificant parameters plot gray polygons over them
            gdf[mgwr_filtered_t[:,0] == 0].plot(color='lightgrey', ax=ax, **{'edgecolor':'black'})
        plt.savefig(folder_results+param+'.png', dpi=100)
        plt.close()
    
    print('Save output as vector shapefile ....')
    with fiona.Env(OSR_WKT_FORMAT='WKT2_2018'):
        gdf.to_file(folder_results+args.exp_name+'.shp')

    print('{}-Done!'.format(datetime.now()))
    sys.stdout.flush()


if __name__ == "__main__":
    main()