"""
HAZARDX AI — External Scientific API Integration Clients
Modular connectors for authentic real-time data ingestion:
- USGS Earthquake Hazards Program (FDSNWS)
- NASA FIRMS (MODIS / VIIRS Active Fire Detections)
- Open-Meteo Global Numerical Weather Prediction (ECMWF, GFS, ICON)
- Copernicus GloFAS River Discharge Forecasts
- NOAA NHC Active Storms & IBTrACS
- NASA Global Landslide Catalog & ERA5 Rainfall Triggers
"""

from .usgs_client import usgs_client, USGSClient
from .nasa_firms_client import firms_client, NASAFIRMSClient
from .weather_client import weather_client, WeatherClient
from .glofas_client import glofas_client, GloFASClient
from .cyclone_client import cyclone_client, CycloneClient
from .landslide_client import landslide_client, LandslideClient
from .base_client import BaseResilientClient
from .imd_client import imd_client, IMDClient

__all__ = [
    "usgs_client", "USGSClient",
    "firms_client", "NASAFIRMSClient",
    "weather_client", "WeatherClient",
    "glofas_client", "GloFASClient",
    "cyclone_client", "CycloneClient",
    "landslide_client", "LandslideClient",
    "base_client", "BaseResilientClient",
    "imd_client", "IMDClient"
]

