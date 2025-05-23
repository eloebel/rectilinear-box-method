# Rectilinear box method: tracking glacier terminus change

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/531123105.svg)](https://zenodo.org/badge/latestdoi/531123105)

The rectilinear box method is a well-established tool for tracking glacier terminus change. Rather than using a single profile to measure advance or retreat, this method uses a rectilinear box that accounts for uneven changes along the calving front. This technique was first described by [Moon and Joughin, 2008](https://doi.org/10.1029/2007JF000927). Here, we provide a customisable and easy to use implementation of the method. 
![jakobshavn_git](https://user-images.githubusercontent.com/68990782/188456837-30c44202-971b-4d4c-9ac8-3d3e011543b3.png)

## Installation
To run this tool, clone the repository and install all required python packages. You can use the `requirements.txt` with `conda`:
```
conda create --name <env_name> --file requirements.txt
```

## Usage
This repository already includes example data for the Glacier *Harald Moltke Bræ* (Greenland). For this dataset, the script works out-of-the-box by running `python box_method.py`. For analyzing other glaciers, three inputs are needed:

1. Glacier box (Polygon Shapefile format)
2. Calving front locations (LineSting Shapefile format)
3. Basemap or image which is used as a background for the figure (geoTIF format)

The box should be arranged so that it can be divided into two parts by each calving front line. The coordinate reference system of the inputs can be defined in `box_method.py`. The file names of the basemap and glacier box must correspond to the label of the glacier. In addition, the folder structure must be considered (see example).

Calculated terminus changes are saved to a text file. In addition, an overview image is generated.

Without additional information, the tool does not know whether the glacier is retreating or advancing. In its current state, it assumes that the calving front is retreating. If this is not the case and the resulting time series is mirrored, the `>` must be replaced by a `<` in line 177 of `box_method.py`.

## Citation
If you find our software helpful and use it in your research, please use the following BibTeX entry.
````
@Article{loebel2024,
AUTHOR = {Loebel, E. and Scheinert, M. and Horwath, M. and Humbert, A. and Sohn, J. and Heidler, K. and Liebezeit, C. and Zhu, X. X.},
TITLE = {Calving front monitoring at a subseasonal resolution: a deep learning application for Greenland glaciers},
JOURNAL = {The Cryosphere},
VOLUME = {18},
YEAR = {2024},
NUMBER = {7},
PAGES = {3315--3332},
URL = {https://tc.copernicus.org/articles/18/3315/2024/},
DOI = {10.5194/tc-18-3315-2024}
}
````

## Contact
**Erik Loebel**  
TU Dresden | Geodetic Earth System Research   
[tu-dresden.de/geo/ipg/gef](https://tu-dresden.de/bu/umwelt/geo/ipg/gef)  
[erik.loebel@tu-dresden.de](mailto:erik.Loebel@tu-dresden.de)
