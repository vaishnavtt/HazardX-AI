"""
HAZARDX AI — Machine Learning Pipeline Configuration
Defines dataset schemas, feature subsets, task targets, loss weightings, and model paths.
"""

import os

RANDOM_STATE = 42

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'model_ready')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports', 'model_evaluation')
SHAP_DIR = os.path.join(REPORTS_DIR, 'shap')
FIGURES_DIR = os.path.join(REPORTS_DIR, 'figures')

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(SHAP_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# Configuration for all 5 hazards and 12 distinct prediction tasks
HAZARD_CONFIGS = {
    'floods': {
        'name': 'Floods',
        'dataset_path': os.path.join(DATA_DIR, 'floods', 'flood_model_ready.csv'),
        'model_dir': os.path.join(MODELS_DIR, 'floods'),
        'features': [
            'precip_1d_mm', 'precip_3d_sum_mm', 'precip_7d_sum_mm', 'precip_14d_sum_mm',
            'api_14d_index', 'temp_2m_celsius', 'soil_temp_celsius', 'river_discharge_m3s',
            'river_discharge_7d_mean_m3s', 'river_discharge_ratio_7d', 'elevation_m',
            'slope_degrees', 'topographic_wetness_index', 'distance_to_river_km'
        ],
        'categorical_features': [],
        'tasks': {
            'flood_occurrence': {
                'target': 'flood_occurred',
                'type': 'binary_classification',
                'description': 'Binary Flood Occurrence Classification (1 = Flood Event, 0 = Non-Flood Control)',
                'pos_weight': 1.0,
                'metric_primary': 'pr_auc'
            },
            'flood_severity': {
                'target': 'severity_class',
                'type': 'multiclass_classification',
                'description': 'Flood Severity Class (0 = None, 1 = Large, 2 = Extreme/Decadal)',
                'num_class': 3,
                'metric_primary': 'f1_macro'
            }
        }
    },
    'landslides': {
        'name': 'Landslides',
        'dataset_path': os.path.join(DATA_DIR, 'landslides', 'landslide_model_ready.csv'),
        'model_dir': os.path.join(MODELS_DIR, 'landslides'),
        'features': [
            'precip_1d_mm', 'precip_3d_sum_mm', 'precip_7d_sum_mm', 'precip_30d_sum_mm',
            'api_30d_index', 'temp_2m_celsius', 'soil_temp_celsius', 'slope_degrees',
            'elevation_m', 'aspect_degrees', 'plan_curvature', 'soil_clay_fraction_pct',
            'distance_to_road_km', 'distance_to_stream_km'
        ],
        'categorical_features': [],
        'tasks': {
            'landslide_occurrence': {
                'target': 'landslide_occurred',
                'type': 'binary_classification',
                'description': 'Binary Landslide Occurrence Classification (1 = Landslide Event, 0 = Stable Slope)',
                'pos_weight': 1.0,
                'metric_primary': 'pr_auc'
            },
            'landslide_magnitude': {
                'target': 'hazard_magnitude_class',
                'type': 'multiclass_classification',
                'description': 'Landslide Magnitude Class (0 = None, 1 = Small/Medium, 2 = Large/Catastrophic)',
                'num_class': 3,
                'metric_primary': 'f1_macro'
            }
        }
    },
    'earthquakes': {
        'name': 'Earthquakes',
        'dataset_path': os.path.join(DATA_DIR, 'earthquakes', 'earthquake_model_ready.csv'),
        'model_dir': os.path.join(MODELS_DIR, 'earthquakes'),
        'features': [
            'mainshock_mag', 'focal_depth_km', 'dist_to_active_fault_km', 'nearest_fault_slip_type',
            'prior_count_7d_100km', 'prior_count_30d_100km', 'prior_count_365d_100km',
            'prior_max_mag_30d', 'cumulative_energy_log_joules', 'seismic_rate_accel_ratio',
            'regional_b_value'
        ],
        'categorical_features': ['nearest_fault_slip_type'],
        'tasks': {
            'aftershock_hazard': {
                'target': 'elevated_aftershock_hazard',
                'type': 'binary_classification',
                'description': 'Regional Elevated Aftershock Hazard Assessment (>=5 aftershocks or secondary M>=5.0 within 30d/100km)',
                'pos_weight': 4.05,
                'metric_primary': 'pr_auc'
            },
            'aftershock_count': {
                'target': 'aftershock_count_30d',
                'type': 'regression',
                'description': '30-Day Aftershock Count Regression within 100km radius',
                'metric_primary': 'rmse'
            },
            'max_aftershock_mag': {
                'target': 'max_aftershock_mag_30d',
                'type': 'regression',
                'description': '30-Day Maximum Aftershock Magnitude Regression (Mw)',
                'metric_primary': 'rmse'
            }
        }
    },
    'cyclones': {
        'name': 'Cyclones',
        'dataset_path': os.path.join(DATA_DIR, 'cyclones', 'cyclone_model_ready.csv'),
        'model_dir': os.path.join(MODELS_DIR, 'cyclones'),
        'features': [
            'current_wind_kt', 'current_pres_hpa', 'dist_to_land_km', 'landfall_flag',
            'past_delta_wind_6h', 'past_delta_wind_12h', 'past_delta_pres_6h',
            'translational_speed_kt', 'heading_degrees', 'coriolis_param', 'pot_intensity_headroom'
        ],
        'categorical_features': [],
        'tasks': {
            'rapid_intensification': {
                'target': 'rapid_intensification',
                'type': 'binary_classification',
                'description': 'Tropical Cyclone Rapid Intensification Classification (Delta V >= 30 kt in 24 hours)',
                'pos_weight': 17.25,
                'metric_primary': 'pr_auc'
            },
            'intensity_change_24h': {
                'target': 'delta_wind_24h',
                'type': 'regression',
                'description': '24-Hour Continuous Wind Intensity Change Regression (knots)',
                'metric_primary': 'rmse'
            }
        }
    },
    'wildfires': {
        'name': 'Wildfires',
        'dataset_path': os.path.join(DATA_DIR, 'wildfires', 'wildfire_model_ready.csv'),
        'model_dir': os.path.join(MODELS_DIR, 'wildfires'),
        'features': [
            'temp_2m_celsius', 'relative_humidity_pct', 'wind_speed_10m_ms', 'precip_7d_sum_mm',
            'precip_30d_sum_mm', 'soil_temp_celsius', 'fwi_fire_weather_index', 'slope_degrees',
            'elevation_m', 'distance_to_road_km'
        ],
        'categorical_features': [],
        'tasks': {
            'wildfire_occurrence': {
                'target': 'wildfire_occurred',
                'type': 'binary_classification',
                'description': 'Wildfire Ignition / Occurrence Susceptibility Classification',
                'pos_weight': 1.0,
                'metric_primary': 'pr_auc'
            },
            'frp_intensity': {
                'target': 'log_total_frp_mw',
                'type': 'regression',
                'description': 'Log10 Fire Radiative Power (MW) Intensity Regression',
                'metric_primary': 'rmse'
            },
            'fire_duration': {
                'target': 'fire_duration_days',
                'type': 'regression',
                'description': 'Fire Episode Duration Regression (days)',
                'metric_primary': 'rmse'
            }
        }
    }
}

