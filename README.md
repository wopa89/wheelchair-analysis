# wheelchair-analysis

# Requirements

Installing with Conda

conda env create -f environment.yml

conda activate analysis

pip install ohsome --no-deps

# input
input is managed through ohsome-input.ini
it needs a start and endtime for analysis timeperiod
a boundary geojson
filter arguments
output file for csv
script-completeness.py needs two outputs csv for object and attributes
other scrips need on output file