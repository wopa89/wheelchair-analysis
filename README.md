
# Analysis of OSM Data Quality with ohsome API

This project is part of the Masterthesis

'Analyse des Potentials von OSM-Daten für eine barrierefreie
Auskunft für Rollstuhlfahrende im ÖPNV anhand
Datenqualitäts-Analysen und einer Routing-Anwendung - am Beispiel
Karlsruhe und Magdeburg'

The python scripts make use of the ohsome API and the possibility to access 
OSM history.

![alt text](https://github.com/wopa89/wheelchair-analysis/blob/main/python-scripts-overview.png?raw=true)

With the scripts it is possible to do a completeness analysis of OSM station objects 
with tag wheelchair and a contribution analysis with counting numbers of contributions 
by type.
## Requirements

Following depencencies are in requirements.yml
```
name: analysis
dependencies:
    - python=3.10.0
    - numpy=1.22.0
    - matplotlib=3.5.1
    - geopandas=0.10.2
    - requests=2.25.1
```

### Installation with conda

To install the requirements its easiest to create a conda environment
```
conda env create -f environment.yml
conda activate analysis
pip install ohsome --no-deps
```

## Input

The ohsome-input.ini file needs a 

- start and endtime for analysis timeperiod
- geojson with administrative boundary
- filter parameters
- csv output file
- additional csv output file for completeness

Example of parameters are in ohsome-input.ini

## Usage
```
python script.py ohsome-input.ini
```