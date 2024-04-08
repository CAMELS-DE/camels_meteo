# HYRAS

Download the HYRAS netCDFs from the DWD opendata server: https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/hyras_de/

Use the netCDFs files covering the entire temporal range (e.g. `tasmin_hyras_5_1951_2020_v5-0_de.nc`), except for RadiationGlobal, where a merged netCDFs file does not exist. Here you have to download the yearly netCDF files.




# HYRAS - Hydrometeorological Gridded Data

## Description

*from: https://www.dwd.de/DE/leistungen/hyras/hyras.html*

HYRAS provides daily data on a 1x1 km² / 5x5 km² grid for **precipitation**, **temperature (mean, minimum, and maximum)**, **humidity**, and **global radiation** from 1951 to 2020. The data are generated using adapted and improved regionalization methods used at the German Weather Service. For instance, the well-established REGNIE method was used for precipitation regionalization. Similar methods to those used in creating Test Reference Years (TRY) were applied to other parameters. Prior to regionalization, input data underwent quality control checks. Extensive error analyses were conducted on the regionalized data to ensure their reliability (see Supplementary Information). Subsequently, statistical-climatological evaluations were carried out in various projects. HYRAS not only analyzes past climate but is also utilized for bias adjustment of regionalized climate projection data. Furthermore, it serves as input data for hydrological modeling and finds widespread applications in climate modeling and impact research.

## Data retrieval for this repository
- Download the HYRAS netCDFs from the DWD opendata server: https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/hyras_de/
    - Use the netCDFs files covering the entire temporal range (e.g. `tasmin_hyras_5_1951_2020_v5-0_de.nc`), except for RadiationGlobal, where a merged netCDFs file does not exist. Here you have to download the yearly netCDF files.
- Save the data in the `input_data` folder of this repository with the following folder structure:

```
/
|- input_data/
|  |- hyras/
|  |  |- Humidity/
|  |  |  |- humidity_hyras_5_1951_2020_v5-0_de.nc
|  |  |- TemperatureMean/
|  |  |  |- tasmean_hyras_5_1951_2020_v5-0_de.nc
|  |  |- RadiationGlobal/
|  |  |  |- rsds_hyras_5_1951_v3-0_de
|  |  |  |- rsds_hyras_5_1952_v3-0_de
|  |  |  |- ...
|  |  |- ...
```

## Citation
Source: Deutscher Wetterdienst