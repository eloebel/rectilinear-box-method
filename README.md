# Rectilinear box method: tracking glacier terminus change
The rectilinear box method is a well-established tool for tracking glacier terminus change. Rather than using a single profile to measure advance or retreat, this method uses a rectilinear box that accounts for uneven changes along the calving front. This technique was first described by [Moon and Joughin, 2008](https://doi.org/10.1029/2007JF000927). Here we provide a complete and easy to use implementation of the method. 
![jakobshavn_git](https://user-images.githubusercontent.com/68990782/188456837-30c44202-971b-4d4c-9ac8-3d3e011543b3.png)

## Usage
All processing is done via the script `box_method.py`. Necessary requirements can be installed using:
```
pip install -r requirements.txt
```
This repository already includes a working example for the Glacier Harald Moltke Bræ.
### Calving front dataset for Greenland
Data product for 23 Greenland outlet glacier 2013 to 2021 (manually delineated)  
Data product for 23 Greenland outlet glacier 2013 to 2021 (automatically delineated)  
Implementation of automated calving front extraction using ANN  

## Citation
If you find our code helpful and use it in your research, please use the following BibTeX entry.

```
@article{HEDUNet2021,
  author={Heidler, Konrad and Mou, Lichao and Baumhoer, Celia and Dietz, Andreas and Zhu, Xiao Xiang},
  journal={IEEE Transactions on Geoscience and Remote Sensing}, 
  title={HED-UNet: Combined Segmentation and Edge Detection for Monitoring the Antarctic Coastline}, 
  year={2021},
  volume={},
  number={},
  pages={1-14},
  doi={10.1109/TGRS.2021.3064606}
}
```
## Contact
**Erik Loebel**  
TU Dresden | Geodetic Earth System Research   
[tu-dresden.de/geo/ipg/gef](https://tu-dresden.de/bu/umwelt/geo/ipg/gef)  
[erik.loebel@tu-dresden.de](mailto:erik.Loebel@tu-dresden.de)  
[@ErikLoebel](https://twitter.com/erikloebel)  
