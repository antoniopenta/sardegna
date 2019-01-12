## SArDeGnA (SpAtial Data Grid frAmework)
- SArDeGnA is a lightweight framework to manage spatial data in Python using a grid approach.
- This framework can help you to manage Point of Interests (i.e. pubs, restaurant) or points related to trajectories.
- An example of a grid created with SArDeGnA and imported in Google Maps as KML file :


![Example of SArDeGnA Grid](https://imgur.com/a/cAs9515)


- [Full Google map](https://drive.google.com/open?id=1nrIEkZOveyefdghtYO-fclhb6LbQpB2b&usp=sharing)


## The Design: ( a spatial grid in one line of python code)

- The framework has a set of classes and related functions useful to create a grid to organize your spatial data.

- **You can create a grid in just one line of code!** :
```python
 Grid().create_grid([lng_center, lat_center, radius_center], radius_cell)
 ```
- lng_center is the center of the grid specified in longitude
- lat_center is the center of the grid specified in latitude
- radius_center is the radius of the grid
- radius_cell is the radius of the cell within the grid

- Then, you have a set of primitives that will help you to manage the POI within the grid.

## Dependencies

- [GDAL](https://www.gdal.org/) - Geospatial Data Abstraction Library (GDAL2).
- Python Binding for GDAL

- In Mac, it will prefer to use brew as follow :
```bash
 brew install gdal2 --HEAD
```
-  "--HEAD" to install the header
- For Linux and Microsoft, you can google : ) : install GDAL2
- Some good links for installing GDAL in Windows  are :
    - https://www.gis.usu.edu/~chrisg/python/2009/docs/gdal_win.pdf
    - https://stackoverflow.com/questions/33574902/install-gdal-using-conda ( based on Conda )
- For MAC, I found useful to run:

```bash
brew update && brew upgrade
```
- Note that in order to install the python binding, first check the version of installed GDAL:
```bash
(spatial-data-analysis) AMAC02RF28MG8WN:spatial-data-framework antonio.penta$ ogr2ogr --version
GDAL 2.4.0, released 2018/12/14
```
- Then, you can run the following pip install (be sure the virtual env is activated, and you are using the pip of your virtual env):
```bash
pip install pygdal=="`gdal-config --version`.*"
```
- The above line  has been  suggested (here)[https://github.com/nextgis/pygdal/tree/master/2.2.4]

- If the installation of GDAL is ok, you should be able to run successfully  the following import in your python console:
```bash
from osgeo import gdal
```
- In my case, I have:
```bash
(spatial-data-analysis) AMAC02RF28MG8WN:spatial-data-framework antonio.penta$ python
Python 3.6.3 (default, Oct  4 2017, 06:09:05)
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.42.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from osgeo import gdal
>>> exit
```

## Virtualenv

- SArDeGnA  uses the  virtual env descrebed  in requirements.txt file, so you need to incorporate it in your env:
```bash
pip install -r requirements.txt
```

## Jupyter with Ipyleaflet extension to visualize the maps

- The attached Jupyter Notebook is using extension [ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet) to visualize the map.
-  My suggestion is to install ipyleaflet downloading the latest development from GitHub (requires npm installed):
```bash
$ git clone https://github.com/jupyter-widgets/ipyleaflet.git
$ cd ipyleaflet
$ pip install -ee .
$ jupyter nbextension install --py --symlink --sys-prefix ipyleaflet
$ jupyter nbextension enable --py --sys-prefix ipyleaflet
```
- The, you need to be sure to enable the extension from the Jupyter notebook installed in your virtual env.
- In my case, I followed the instructions detailed [here](https://github.com/jupyter-widgets/ipyleaflet) under the Installation session, ensuring to lunch 'jupyter labextension .. ' as '/path_your_env/jupyter labextension .. '

## Tutorial

- - The tutorial is a Jupyter notebook (TutorialFramework.ipynb) saved in the main folder

- Be sure to have Jupyter installed in the virtual env that contains the GDAL binding,
- Be sure to lunch the notebook with the virtual env that contains the GDAL binding, a good explanation of how to have
a Jupyter notebook on the top of predefined virtual env can be found (here)[https://anbasile.github.io/programming/2017/06/25/jupyter-venv/]
- Be sure to have the Ipyleaflet extension, please read the session above.

- To check if Jupyter notebook is using the right env, you can print the sys.path and check the path:
```python
import sys
print(sys.path)
```


## Authors

Antonio Penta
