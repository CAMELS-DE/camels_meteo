import geopandas as gpd
from concurrent.futures import ThreadPoolExecutor, as_completed
import papermill as pm
from tqdm import tqdm
import os
import json

from camelsp import get_metadata


VARIABLES = ["Humidity", "RadiationGlobal", "TemperatureMax", "TemperatureMin", "TemperatureMean", "Precipitation"]
CAMELS_IDS = get_metadata().camels_id.values
RESULT_PATH = "/output_data"
N_THREADS = os.cpu_count() - 2


def create_parameter_list():
    """
    Create a list of parameters for the papermill execution.
    
    """
    all_parameters_list = []

    for variable in VARIABLES:
        for camels_id in CAMELS_IDS:
            all_parameters_list.append({"CAMELS_ID": camels_id, 
                                        "HYRAS_VARIABLE": variable, 
                                        "SAVE_NETCDF": True, 
                                        "RESULT_PATH": RESULT_PATH,
                                        "WEIGHTED_STATISTICS": True})

    return all_parameters_list


def execute_notebook(parameters: dict, if_exists: str) -> None:
    """
    Execute the notebook clip_hyras_to_catchment.ipynb with the given parameters.
    You can restart a papermill run with the if_exists parameter. If if_exists is set to "replace", 
    the notebook will be executed no matter if the variable and catchment were already processed. 
    If if_exists is set to "skip", the notebook will not be executed again with the same parameters. 
    If if_exists is set to "raise", a ValueError will be raised if the variable for the catchment 
    was already processed.
    
    
    Parameters
    ----------
    parameters : dict
        The parameters for the notebook.
    if_exists : str
        The if_exists parameter. Can be "replace", "skip", or "raise".

    Returns
    -------
    None    
        
    """
    # check if the metadata file for this station already exists
    if os.path.exists(f"{parameters['RESULT_PATH']}/{parameters['CAMELS_ID']}/metadata.json"):
        if if_exists == "replace":
            # if if_exists is replace, we continue with the execution, no matter if the variable is already in the metadata file
            pass
        elif if_exists == "skip":
            # open the metadata file and check if the variable is already in the file
            with open(f"{parameters['RESULT_PATH']}/{parameters['CAMELS_ID']}/metadata.json", "r") as file:
                metadata = json.load(file)
                if parameters['HYRAS_VARIABLE'] in metadata.get(parameters['CAMELS_ID'], {}):
                    return
        elif if_exists == "raise":
            # open the metadata file and check if the variable is already in the file
            with open(f"{parameters['RESULT_PATH']}/{parameters['CAMELS_ID']}/metadata.json", "r") as file:
                metadata = json.load(file)
                if parameters['HYRAS_VARIABLE'] in metadata.get(parameters['CAMELS_ID'], {}):
                    raise ValueError(f"The variable {parameters['HYRAS_VARIABLE']} for catchment {parameters['CAMELS_ID']} was already processed. Change the if_exists parameter to 'replace' to execute the notebook again or to 'skip' to skip this set of parameters.")
        

    # create folder to save the papermill notebook
    os.makedirs(f"{parameters['RESULT_PATH']}/{parameters['CAMELS_ID']}/notebooks", exist_ok=True)

    # execute the notebook
    pm.execute_notebook(
        input_path="/scripts/clip_hyras_to_catchment.ipynb",
        output_path=f"{parameters['RESULT_PATH']}/{parameters['CAMELS_ID']}/notebooks/{parameters['CAMELS_ID']}_{parameters['HYRAS_VARIABLE']}.ipynb",
        parameters=parameters,
        progress_bar=False
    )


if __name__ == "__main__":
    # set environment variable PYDEVD_DISABLE_FILE_VALIDATION to avoid unnecessary debugger output
    os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"

    # create a list of parameters for the papermill execution
    all_parameters_list = create_parameter_list()

    failed = {}

    with ThreadPoolExecutor(N_THREADS) as executor:
        futures = {executor.submit(execute_notebook, parameters, if_exists="skip"): parameters for parameters in all_parameters_list}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing notebooks"):
            try:
                future.result()  # get the result or raise exception
            except Exception as e:
                params = futures[future]
                print(f"Notebook execution failed for parameters: {params}. Error: {e}")
                failed[params["CAMELS_ID"]] = str(e)

        executor.shutdown(wait=True)
