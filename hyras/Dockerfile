# Pull python base image
FROM python:3.10

# Update pip
RUN pip install --upgrade pip

# Install dependencies for camelsp with fixed versions
RUN pip install geopandas==0.14.3
RUN pip install "pandas<2.2.0"
RUN pip install numpy==1.25.2
RUN pip install matplotlib==3.8.3
RUN pip install plotly==5.19.0
RUN pip install pyproj==3.6.1
RUN pip install dateparser==1.2.0
RUN pip install dask==2024.2.0
RUN pip install ydata-profiling==4.6.4
RUN pip install tqdm==4.66.2
RUN pip install openpyxl==3.1.2
RUN pip install papermill==2.5.0
RUN pip install jupyter==1.0.0

# Install camelsp from GitHub
RUN git clone https://github.com/CAMELS-DE/camelsp.git
RUN pip install -e /camelsp 

# Install aditional dependencies for clipping hyras with fixed versions
RUN pip install xarray[complete]==2023.12.0
RUN pip install rioxarray==0.15.0
RUN pip install dask==2023.12.1
RUN pip install contextily==1.5.0

# Install dependencies for exactextract
 RUN apt-get update && apt-get install -y \
      gdal-bin \
      libgdal-dev \
      libgeos-dev 

# # further dependencies for exactextract
RUN pip install "pybind11[global]"

# Clone exactextract from Github
RUN git clone https://github.com/isciences/exactextract
RUN pip install /exactextract

# Change working directory
WORKDIR /scripts

# Run Python script to clip hyras in parallel
CMD ["/bin/bash", "process_hyras.sh"]