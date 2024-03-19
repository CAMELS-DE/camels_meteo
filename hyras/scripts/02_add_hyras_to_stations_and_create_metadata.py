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


def add_hyras_to_station_folder():
    """
    Add extracted HYRAS data to the CAMELS-DE data folder of 
    each station.
    
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
        station_output_path = s.output_path()

        # get hyras output path
        hyras_output_path = f"/output_data/{camels_id}"

        # check if hyras_output_path exists
        if not os.path.exists(hyras_output_path):
            continue
        
        # copy contents of hyras data to station
        shutil.copytree(hyras_output_path, station_output_path)

        # rename hyras data folder to hyras
        os.rename(f"{station_output_path}/{camels_id}", f"{station_output_path}/hyras")
        
    return None


if __name__ == "__main__":
    merge_hyras_metadata()
    add_hyras_to_station_folder()