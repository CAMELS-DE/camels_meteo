from camelsp import Station, get_metadata
import shutil
import os
import json
from glob import glob
import pandas as pd



def merge_hyras_metadata():
    """
    Merge the HYRAS run metadata (in .json format) into one .csv
    metadata file. This file shows which variables were extracted
    for each station.
    
    """
    # get metadata
    metadata = get_metadata()

    # get camels_ids
    camels_ids = metadata["camels_id"].values

    # create dataframe with camels_id as index to store which variables have been processed
    hyras_metadata = pd.DataFrame(index=camels_ids)

    for variable in ["Humidity", "RadiationGlobal", "TemperatureMin", "TemperatureMax", "TemperatureMean", "Precipitation"]:
        hyras_metadata[f"{variable}_exact_extract_available"] = False

    for camels_id in camels_ids:
        # get metadata file
        metadata_file = f"/output_data/{camels_id}/metadata.json"

        # check if metadata file exists
        if not os.path.exists(metadata_file):
            # if metadata file does not exist, no data was extracted and keep False
            continue
        else:
            with open(metadata_file, "r") as f:
                station_metadata = json.load(f)
                for camels_id, variable_dict in station_metadata.items():
                    for variable, meta_dict in variable_dict.items():
                        # check if the variable was processed succesfully
                        if not "ERROR: Clipped data has dimensionality of 1, cannot calculate weighted statistics" in meta_dict["warnings"]:
                            hyras_metadata.loc[camels_id, f"{variable}_exact_extract_available"] = True

    # save the hyras availability metadata
    hyras_metadata.to_csv("/output_data/scripts/hyras_exact_extract_availability.csv")


def rename_columns():
    """
    Rename the columns of the extracted HYRAS csv dataframe to
    CAMELS-DE variables.
    
    """
    # get metadata
    metadata = get_metadata()

    # get camels_ids
    camels_ids = metadata["camels_id"].values
    
    # iterate over all stations
    for camels_id in camels_ids:
        # get data files for this station
        data_files = glob(f"/output_data/{camels_id}/data/*.csv")

        # iterate over all data files
        for data_file in data_files:
            # load data
            df = pd.read_csv(data_file, index_col=0)

            # get columns
            columns = df.columns

            # rename columns
            if "hurs_" in columns[0]:
                new_colnames = [c.replace("hurs", "humidity") for c in columns]
            elif "rsds_" in columns[0]:
                new_colnames = [c.replace("rsds", "radiation_global") for c in columns]
            elif "tasmin_" in columns[0]:
                new_colnames = [c.replace("tasmin", "temperature_min") for c in columns]
            elif "tasmax_" in columns[0]:
                new_colnames = [c.replace("tasmax", "temperature_max") for c in columns]
            elif "tas_" in columns[0]:
                new_colnames = [c.replace("tas", "temperature_mean") for c in columns]
            elif "pr_" in columns[0]:
                new_colnames = [c.replace("pr", "precipitation") for c in columns]
            else:
                new_colnames = columns

            # rename columns
            df.columns = new_colnames

            # save data
            df.to_csv(data_file)


def add_hyras_to_station_folder():
    """
    Add extracted HYRAS data to the CAMELS-DE data folder of 
    each station.  
    We only copy the extracted csv files to the camelsp folder.
    
    """
    # get metadata
    metadata = get_metadata()

    # get camels_ids
    camels_ids = metadata["camels_id"].values
    
    # iterate over all stations
    for camels_id in camels_ids:
        # initialize Station
        s = Station(camels_id)

        # get Station output path
        station_output_path = s.output_path

        # get extracted hyras csv files
        hyras_files = glob(f"/output_data/{camels_id}/data/*.csv")

        # check if hyras output exists
        if len(hyras_files) == 0:
            continue
        
        # create hyras folder in camelsp directory
        os.makedirs(f"{station_output_path}/hyras", exist_ok=True)

        # copy hyras csv files to station folder
        for hyras_file in hyras_files:
            shutil.copy(hyras_file, f"{station_output_path}/hyras/")


if __name__ == "__main__":
    merge_hyras_metadata()
    rename_columns()
    add_hyras_to_station_folder()