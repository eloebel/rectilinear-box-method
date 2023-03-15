# Rectilinear box method: tracking glacier terminus change
The rectilinear box method is a well-established tool for tracking glacier terminus change. Rather than using a single profile to measure advance or retreat, this method uses a rectilinear box that accounts for uneven changes along the calving front. This technique was first described by [Moon and Joughin, 2008](https://doi.org/10.1029/2007JF000927). Here we provide a complete and easy to use implementation of the method. 
![jakobshavn_git](https://user-images.githubusercontent.com/68990782/188456837-30c44202-971b-4d4c-9ac8-3d3e011543b3.png)

## Installation
To run this tool, clone the repository and install all requirements using:
```
pip install -r requirements.txt
```

## Usage
This repository already includes example data for the Glacier *Harald Moltke Bræ* (Greenland). For this dataset the script works out-of-the-box by running `python box_method.py`. For analyzing other glaciers three things are needed:

1. Glacier box (Polygon Shapefile format)
2. Claving front locations (LineSting Shapefile format)
3. Basemap or image which is used as a background for the figure

The box should be arranged so that it can be divided into two parts by each calving front line. The coordinate reference system must be the same for all three inputs and has to be defined in `box_method.py`. The file names must correspond to the label of the glacier. In addition, the folder structure must be considered (see example).

Without additional information, the tool does not know whether the glacier is retreating or advancing. In its current state, it assumes that the calving front is retreating. If this is not the case and the resulting time series is mirrored, the `>` must be replaced by a `<` in line 156 of `box_method.py`.

## Contact
**Erik Loebel**  
TU Dresden | Geodetic Earth System Research   
[tu-dresden.de/geo/ipg/gef](https://tu-dresden.de/bu/umwelt/geo/ipg/gef)  
[erik.loebel@tu-dresden.de](mailto:erik.Loebel@tu-dresden.de)  
[@ErikLoebel](https://twitter.com/erikloebel)  
