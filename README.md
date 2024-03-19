# camels_meteo
Repository to process meteorological data for CAMELS-DE


## HYRAS
Run HYRAS in parallel, change `N_THREADS` in `scripts/papermill_execute_parallel.py` to controll number of parallel threads.  

Run:
`docker run -v ./input_data:/input_data -v ./output_data:/output_data -v ./scripts:/scripts -v /path/to/camelsp/output_data:/camelsp/output_data -it --rm hyras`