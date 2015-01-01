Kvartersregeringen
========

### Installation

Kvartersregeringen uses __Flask__ as a backend to parse GeoJSON find the right election districts and __MapBox__ to visualize the results. 

- Install __Virtualenv__: `$ sudo easy_install virtualenv`
- Install [__Brew__](http://brew.sh/)
  - Install GeoDjango libraries [using brew](https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#homebrew)
- Install [__pip__](http://www.pip-installer.org/en/latest/installing.html)
- Init your personal environment with `$ virtualenv env --no-site-packages` and `source env/bin/activate`
- Install requirements: `$ pip install -r requirements.txt`
- Start server: `$ python app.py`

### Update Heroku

- `git subtree push --prefix app heroku master`


### Update with new data

- Load election data and run simulations in R. Write the results of the simulation to the geoJSON file.
  - Methods are stored in `regeringsbildning.R`.
  - The code for loading data and running simulations is stored in `regering tillGeoJSON.R`.
- Modify and run __add-meta-data-and-split.py__ to split the GeoJSON file into provinces.
- Deploy?!
