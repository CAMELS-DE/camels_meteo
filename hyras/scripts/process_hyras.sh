#!/bin/bash
# make directories to store the output data if they do not exist
mkdir -p /output_data/scripts

# logging
exec > >(tee -a /output_data/scripts/processing.log) 2>&1

# Start processing
echo "[$(date +%F\ %T)] Starting processing of HYRAS meteorological data for the CAMELS-DE dataset..."

# Start parallel extraction and processing of HYRAS data
echo "[$(date +%T)] Extracting and processing HYRAS data..."
python /scripts/01_papermill_execute_parallel.py
cp /scripts/01_papermill_execute_parallel.R /output_data/scripts/01_papermill_execute_parallel.R
echo "[$(date +%T)] Saved extracted and processed HYRAS data for all CAMELS-DE stations with 02_papermill_execute_parallel.R"

# Create metadata file for hyras run and copy hyras data to CAMELS-DE station folders
echo "[$(date +%T)] Creating metadata file for hyras run and copying hyras data to CAMELS-DE station folders..."
python /scripts/02_add_hyras_to_stations_and_create_metadata.py
cp /scripts/02_add_hyras_to_stations_and_create_metadata.py /output_data/scripts/02_add_hyras_to_stations_and_create_metadata.py
echo "[$(date +%T)] Saved metadata file for hyras run and copied hyras data to CAMELS-DE station folders with 02_add_hyras_to_stations_and_create_metadata.py"

# Copy scripts to /camelsp/output_data/scripts/soils/isric/
mkdir -p /camelsp/output_data/scripts/meteo/hyras/
cp /output_data/scripts/* /camelsp/output_data/scripts/meteo/hyras/

# Change permissions of the output data
chmod -R 777 /camelsp/output_data/
chmod -R 777 /output_data/