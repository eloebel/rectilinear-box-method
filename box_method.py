#!/usr/bin/python -u
#
# Purpose: Rectilinear box method to quantify glacier terminus position change
# Author: Erik Loebel
# Last change: 2022-09-05
#
#
# ------------------------------------------
### loading necessary modules ###
import os
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib
import shapefile # Requires the pyshp package
import shapely
from shapely.ops import split
from functools import partial
import pyproj
from datetime import datetime
from tifffile import TiffFile
from osgeo import gdal
import cartopy.crs as ccrs
from matplotlib import cm
### ------------------------------------------
### define glacier ###
glacier = 'harald_moltke_brae'

### define path ###
path = '/home_cl12/loebel/WORK/git'

linewidth=0.5                                  # linewidth of the calving front plot
basemap=path+'/basemap/'+glacier+'.tif'        # location of the background image (should be filled in automatically using the defined glacier name)

### ------------------------------------------

print('  - loading glacier box and lines ...')
### loading glacier box ###
box = shapefile.Reader(path+'/box/'+glacier+'.shp')
feature = box.shapeRecords()[0]
box = feature.shape.__geo_interface__  
box_geom = shapely.geometry.shape(box)

### generating list of lines ###
lines = next(os.walk(path+'/lines/'+glacier))[1]
lines.sort()                                # dates (which are also folder- and filenames of calving front lines)

### transforming lines to decimal year ###
def dt_to_dec(dt):                                          # defining function to do that
    year_start = datetime(dt.year, 1, 1)
    year_end = year_start.replace(year=dt.year+1)
    return dt.year + ((dt - year_start).total_seconds() /   # seconds so far
        float((year_end - year_start).total_seconds()))     # seconds in year

dates = next(os.walk(path+'/lines/'+glacier))[1]
dates.sort()
dates_dec = np.zeros(len(dates))
format = '%Y%m%d'
for i in range(len(dates)):
    input=str(dates[i])
    dates_dec[i] = dt_to_dec(datetime.strptime(input, format))     # dates_dec are the decimal year times to corresponding lines

### starting the plot ###
fig = plt.figure(figsize=(10,10),dpi=300)   # size, dpi
fig.suptitle(glacier + ' | ' + str(len(lines)) + ' calving front positions', fontsize=16)          # title
gs = fig.add_gridspec(3, 20)                # defining grid of the plots
fig.tight_layout()                          # using tight layout

### set up colorbar ###
ax0 = fig.add_subplot(gs[0:2, 19])          # position of colorbar in defined grid space
cmap = cm.get_cmap('viridis', 128)          # using viridis colorbar
norm = plt.Normalize(vmin=np.min(dates_dec), vmax=np.max(dates_dec))
cb1 = matplotlib.colorbar.ColorbarBase(ax0,cmap=cmap, norm=norm, orientation='vertical',ticklocation='right',label='Year')
 
### set up projection transform ###
wgs84 = pyproj.CRS('EPSG:4326')
epsg_3413 = pyproj.CRS('EPSG:3413')
project = pyproj.Transformer.from_crs(epsg_3413, wgs84, always_xy=True).transform

box_wgs84 = shapely.ops.transform(project, box_geom)        # transform box from epsg:3413 to epsg:4326

### basemap (background image) ###
print('  - loading basemap ...')
with TiffFile(basemap) as tif:                  # load .tif
    basemap_raster = tif.asarray()

basemap = gdal.Open(basemap)
prj=basemap.GetProjection()
UTM_zone=(prj.split("UTM zone ",1)[1])[ 0 : 2 ] # getting UTM zone
            
width_basemap = basemap.RasterXSize             # getting width
height_basemap = basemap.RasterYSize            # getting height
gt_basemap = basemap.GetGeoTransform()
minx_basemap = gt_basemap[0]                                                                # getting min x coordinate
miny_basemap = gt_basemap[3] + width_basemap*gt_basemap[4] + height_basemap*gt_basemap[5]   # getting min y coordinate
maxx_basemap = gt_basemap[0] + width_basemap*gt_basemap[1] + height_basemap*gt_basemap[2]   # getting max x coordinate
maxy_basemap = gt_basemap[3]                                                                # getting max y coordinate
img_extent_basemap = (minx_basemap, maxx_basemap, miny_basemap, maxy_basemap)

plot_extent=[box_wgs84.bounds[0], box_wgs84.bounds[2], box_wgs84.bounds[1], box_wgs84.bounds[3]]    # defining extent of box

### plotting basemap (background image) ###
print('  - plotting the basemap ...')
ax1 = fig.add_subplot(gs[0:2, 0:19],projection=ccrs.NorthPolarStereo()) 
ax1.set_extent(plot_extent)
ax1.imshow(basemap_raster,extent=img_extent_basemap,transform=ccrs.UTM(UTM_zone),cmap='gray') 
gl = ax1.gridlines(draw_labels=True, x_inline=False, y_inline=False,color='k',alpha=0.3, linestyle='--')
gl.top_labels = True
gl.right_labels = True
gl.bottom_labels = True
gl.left_labels = True

### plotting box in transparent white ###
xs, ys = box_geom.exterior.xy
ax1.fill(xs, ys,transform=ccrs.epsg(3413), alpha=0.3, fc='white')

### looping through all lines (.shp files) and (1.) calculating area change and (2.) plotting them on the map (with color according to decimal year date) ###
print('  - calculating area change ...')
area = np.zeros(len(lines))
for i, line in tqdm(enumerate(lines), total=len(lines)):
    ### load line ###
    line = shapefile.Reader(path+'/lines/'+glacier+'/'+line+'/calving_front_'+line+'_3413.shp')
    feature = line.shapeRecords()[0]
    line = feature.shape.__geo_interface__  
    line_geom = shapely.geometry.shape(line)
    ### split polygon by line ###
    out = split(box_geom, line_geom)
    ### transform output polygon(s) to EPSG 4326 ###
    out_wgs84 = shapely.ops.transform(project, out)
    box_1 = out_wgs84.geoms[0]
    box_2 = out_wgs84.geoms[1]
    
    ### calculate the area of box 1 in m^2 ###
    geom=box_1
    geom_area = shapely.ops.transform(
        partial(
            pyproj.transform,
            pyproj.Proj("+proj=latlon"),
            pyproj.Proj(
                proj='aea',
                lat_1=geom.bounds[1],
                lat_2=geom.bounds[3]
            )
        ),
        geom)
    area_box_1=geom_area.area
    area[i]=area_box_1
    ### plotting line on map ###
    ax1.plot(*out.geoms[0].exterior.xy,transform=ccrs.epsg(3413),linewidth=linewidth, color=cmap(norm(float(dates_dec[i]))))

### plot box exterior in black ###
ax1.plot(*box_geom.exterior.xy,transform=ccrs.epsg(3413),linewidth=linewidth+0.5,color="black")

print('  - plotting time series ...')
### final area in km2 -> assumption that glacier is retrating ###
if area[0] >= area[len(area)-1]:
    area_final=(area-area[0])/1000000
else:
    area_final=(area[0]-area)/1000000

### plotting the series ###
ax2 = fig.add_subplot(gs[2, :])
ax2.scatter(dates_dec,area_final,s=5,color="black")
ax2.set_xlabel("Year")
ax2.set_ylabel("Area (km²)")

### group dates by year (connecting all values of each year in plot) ###
min_year=int((np.ceil(dates_dec[0]))-1)
max_year=int((np.ceil(dates_dec[len(dates_dec)-1]))-1)
for i in range(min_year, max_year+1, 1):
    idx = (dates_dec>i)*(dates_dec<(i+1))
    output = np.where(idx)[0]
    dates_dec_=dates_dec[output]
    area_final_=area_final[output]
    ax2.plot(dates_dec_,area_final_,color="gray",linewidth=1)
fig.subplots_adjust(hspace=0.2)
#plt.show()
plt.savefig(path+'/OVERVIEW_' + glacier +'.png')
plt.close()

