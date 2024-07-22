# HYRAS

## Description

Dockerized tool to extract and process data from the HYRAS netCDF files for CAMELS-DE.  
Running the tool is computationally very expensive, as loading the netCDF data for all CAMELS-DE stations takes a lot of time.  
The tool uses the Python library `papermill` to execute jupyter notebooks and also save the executed notebook to the output directory, which makes the workflow very transparent and comprehensible.  
Each notebook processes **one** HYRAS variable for **one** CAMELS-DE station. The docker container then runs these notebooks in parallel, the number of parallel threads can be set in `01_papermill_execute_parallel` via the parameter `N_THREADS`. Unfortuanally, Kernel crashes are quite common, this of course depends on your hardware and on `N_THREADS`, decrease the number of parallel threads if kernel crashes happen often.  
The tool is designed in a way, that you can just restart the container when a crash happens, the tool will continue where the crash happened and won't processes variables twice.  

A folder is created in the `output_data` folder for the results of each catchment, we save three sub-folders:
- `data`: contains the extracted and aggregated HYRAS .csv data as well as the clipped-to-the-catchment .nc files
- `plots`: contains a raster plot of the clipped data and a timeseries plot of the aggregated data
- `notebooks`: contains the notebooks executed by papermill which produced the outputs

Extracted variables are copied to the camelsp `output_data` directory of each station, where other tools process the data further and organize it for the final CAMELS-DE release.

## Container

### Build the container

```bash
docker build -t hyras .
```

### Run the container

Follow the instructions in `input_data/README.md` to add the necessary input data to run the tool. 

To run the container, the local `input_data`, `output_data` and `camelsp/output_data` directories have to be mounted inside the container:

```bash
docker run -v ./input_data:/input_data -v ./output_data:/output_data -v /path/to/local/camelsp/output_data:/camelsp/output_data -it --rm hyras
```

## Output variables

All variables represent the extracted and aggregated data for each catchment.  

**Humidity**:
- humidity_mean [%]
- humidity_min [%]
- humidity_median [%]
- humidity_max [%]
- humidity_stdev [%]

**TemperatureMin**:
- temperature_min_mean [°C]
- temperature_min_min [°C]
- temperature_min_median [°C]
- temperature_min_max [°C]
- temperature_min_stdev [°C]

**TemperatureMean**:
- temperature_mean_mean [°C]
- temperature_mean_min [°C]
- temperature_mean_median [°C]
- temperature_mean_max [°C]
- temperature_mean_stdev [°C]

**TemperatureMax**:
- temperature_max_mean [°C]
- temperature_max_min [°C]
- temperature_max_median [°C]
- temperature_max_max [°C]
- temperature_max_stdev [°C]

**RadiationGlobal**:
- radiation_global_mean [W/m²]
- radiation_global_min [W/m²]
- radiation_global_median [W/m²]
- radiation_global_max [W/m²]
- radiation_global_stdev [W/m²]

**Precipitation**:
- precipitation_mean [mm]
- precipitation_min [mm]
- precipitation_median [mm]
- precipitation_max [mm]
- precipitation_stdev [mm]
