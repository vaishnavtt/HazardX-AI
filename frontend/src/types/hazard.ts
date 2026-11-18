/**
 * HAZARDX AI — TypeScript Definitions matching Backend Pydantic Schemas
 */

export type AlertLevel = 'GREEN' | 'YELLOW' | 'ORANGE' | 'RED';

export type OperationalStatus = 'OPERATIONAL' | 'EXPERIMENTAL' | 'UNAVAILABLE_FOR_OPERATIONAL_USE';

export type HazardType = 'floods' | 'landslides' | 'earthquakes' | 'cyclones' | 'wildfires';

export interface FeatureAttribution {
  feature: string;
  importance_score: number;
  direction: 'RISK_INCREASING' | 'RISK_DECREASING';
  description: string;
}

export interface HealthResponse {
  status: string;
  version: string;
  service: string;
  models_loaded: number;
  operational_models: string[];
  experimental_models: string[];
  timestamp: string;
}

export interface ModelCatalogItem {
  hazard: string;
  task_name: string;
  task_type: string;
  target_column: string;
  operational_status: OperationalStatus;
  primary_metric_name: string;
  primary_test_score: number;
  model_version: string;
  artifact_path: string;
  description: string;
}

export interface ModelCatalogResponse {
  total_models: number;
  operational_models_count: number;
  experimental_models_count: number;
  models: ModelCatalogItem[];
}

export interface ModelPerformanceSummary {
  hazard: string;
  task_name: string;
  task_type: string;
  target_column: string;
  algorithm: string;
  operational_status: OperationalStatus;
  primary_metric_name: string;
  primary_test_score: number;
  secondary_metric_name: string;
  secondary_test_score: number;
  top_important_features: string;
  version: string;
}

export interface HazardExplanationResponse {
  hazard_name: string;
  task_name: string;
  method: string;
  top_global_features: Array<{
    feature: string;
    mean_abs_shap: number;
    physical_role?: string;
  }>;
  physical_interpretation: string;
  shap_summary_plot_url?: string;
  shap_bar_plot_url?: string;
}

export interface DashboardSummaryResponse {
  system_name: string;
  status: string;
  total_hazards_supported: number;
  total_models_available: number;
  operational_models_count: number;
  experimental_models_count: number;
  hazard_overview: Record<string, {
    supported_tasks: string[];
    primary_task: string;
    primary_metric: string;
    operational_status: string;
    key_drivers: string[];
    disclaimer?: string;
  }>;
}

/* Feature Inputs */
export interface FloodFeatures {
  precip_1d_mm: number;
  precip_3d_sum_mm: number;
  precip_7d_sum_mm: number;
  precip_14d_sum_mm: number;
  api_14d_index: number;
  temp_2m_celsius: number;
  soil_temp_celsius: number;
  river_discharge_m3s: number;
  river_discharge_7d_mean_m3s: number;
  river_discharge_ratio_7d: number;
  elevation_m: number;
  slope_degrees: number;
  topographic_wetness_index: number;
  distance_to_river_km: number;
}

export interface LandslideFeatures {
  precip_1d_mm: number;
  precip_3d_sum_mm: number;
  precip_7d_sum_mm: number;
  precip_30d_sum_mm: number;
  api_30d_index: number;
  temp_2m_celsius: number;
  soil_temp_celsius: number;
  slope_degrees: number;
  elevation_m: number;
  aspect_degrees: number;
  plan_curvature: number;
  soil_clay_fraction_pct: number;
  distance_to_road_km: number;
  distance_to_stream_km: number;
}

export interface EarthquakeFeatures {
  mainshock_mag: number;
  focal_depth_km: number;
  dist_to_active_fault_km: number;
  nearest_fault_slip_type: string;
  prior_count_7d_100km: number;
  prior_count_30d_100km: number;
  prior_count_365d_100km: number;
  prior_max_mag_30d: number;
  cumulative_energy_log_joules: number;
  seismic_rate_accel_ratio: number;
  regional_b_value: number;
}

export interface CycloneFeatures {
  current_wind_kt: number;
  current_pres_hpa: number;
  dist_to_land_km: number;
  landfall_flag: number;
  past_delta_wind_6h: number;
  past_delta_wind_12h: number;
  past_delta_pres_6h: number;
  translational_speed_kt: number;
  heading_degrees: number;
  coriolis_param: number;
  pot_intensity_headroom: number;
}

export interface WildfireFeatures {
  temp_2m_celsius: number;
  relative_humidity_pct: number;
  wind_speed_10m_ms: number;
  precip_7d_sum_mm: number;
  precip_30d_sum_mm: number;
  soil_temp_celsius: number;
  fwi_fire_weather_index: number;
  slope_degrees: number;
  elevation_m: number;
  distance_to_road_km: number;
}

/* Prediction Responses */
export interface FloodPredictionResponse {
  hazard_name: string;
  flood_occurrence_predicted: boolean;
  raw_model_score: number;
  calibrated_susceptibility_score: number;
  risk_category: string;
  alert_level: AlertLevel;
  severity_class: number;
  severity_label: string;
  action_guidance: string;
  important_contributing_features: FeatureAttribution[];
  model_version: string;
  input_validation_status: string;
  limitations_and_warnings: string[];
}

export interface LandslidePredictionResponse {
  hazard_name: string;
  landslide_occurrence_predicted: boolean;
  raw_model_score: number;
  calibrated_susceptibility_score: number;
  risk_category: string;
  alert_level: AlertLevel;
  hazard_magnitude_class: number;
  hazard_magnitude_label: string;
  action_guidance: string;
  important_contributing_features: FeatureAttribution[];
  model_version: string;
  input_validation_status: string;
  limitations_and_warnings: string[];
}

export interface EarthquakePredictionResponse {
  hazard_name: string;
  assessment_type: string;
  disclaimer: string;
  elevated_aftershock_hazard_predicted: boolean;
  hazard_probability: number;
  risk_category: string;
  alert_level: AlertLevel;
  action_guidance: string;
  estimated_max_aftershock_magnitude: number | null;
  estimated_aftershock_count: number | null;
  important_contributing_features: FeatureAttribution[];
  model_version: string;
  input_validation_status: string;
  limitations_and_warnings: string[];
}

export interface CyclonePredictionResponse {
  hazard_name: string;
  rapid_intensification_predicted: boolean;
  rapid_intensification_probability: number;
  predicted_24h_intensity_change_kt: number;
  projected_wind_24h_kt: number;
  risk_category: string;
  alert_level: AlertLevel;
  action_guidance: string;
  important_contributing_features: FeatureAttribution[];
  model_version: string;
  input_validation_status: string;
  limitations_and_warnings: string[];
}

export interface WildfirePredictionResponse {
  hazard_name: string;
  wildfire_susceptibility_predicted: boolean;
  raw_model_score: number;
  calibrated_susceptibility_score: number;
  risk_category: string;
  alert_level: AlertLevel;
  action_guidance: string;
  estimated_log_frp_mw: number | null;
  estimated_duration_days: number | null;
  important_contributing_features: FeatureAttribution[];
  model_version: string;
  input_validation_status: string;
  limitations_and_warnings: string[];
}

export interface MultiHazardPredictionRequest {
  flood?: FloodFeatures;
  landslide?: LandslideFeatures;
  earthquake?: EarthquakeFeatures;
  cyclone?: CycloneFeatures;
  wildfire?: WildfireFeatures;
}

export interface MultiHazardPredictionResponse {
  timestamp: string;
  hazards_evaluated: string[];
  composite_highest_alert_level: AlertLevel;
  results: {
    flood?: FloodPredictionResponse;
    landslide?: LandslidePredictionResponse;
    earthquake?: EarthquakePredictionResponse;
    cyclone?: CyclonePredictionResponse;
    wildfire?: WildfirePredictionResponse;
  };
}

/* Phase 6 & Phase 7 Real-Time Data and Geospatial Intelligence Types */

export interface LiveEarthquakeEvent {
  id: string;
  title: string;
  magnitude: number;
  depth_km: number;
  latitude: number;
  longitude: number;
  event_time: string;
  location: string;
  significance?: number;
  url?: string;
  data_freshness: string;
  source: string;
}

export interface LiveWildfireEvent {
  id: string;
  latitude: number;
  longitude: number;
  brightness_kelvin: number;
  frp_mw: number;
  confidence: string;
  acq_time: string;
  satellite: string;
  daynight: string;
  data_freshness: string;
  source: string;
}

export interface LiveCycloneEvent {
  id: string;
  name: string;
  basin: string;
  latitude: number;
  longitude: number;
  intensity_kt: number;
  min_pressure_hpa?: number;
  speed_kt?: number;
  heading_deg?: number;
  observation_time: string;
  classification: string;
  data_freshness: string;
  source: string;
}

export interface LiveFloodObservation {
  id: string;
  location_name: string;
  latitude: number;
  longitude: number;
  current_discharge_m3s: number;
  mean_discharge_7d_m3s: number;
  max_forecast_discharge_m3s: number;
  discharge_anomaly_ratio: number;
  flood_threshold_exceeded: boolean;
  observation_time: string;
  data_freshness: string;
  source: string;
}

export interface LiveLandslideObservation {
  id: string;
  location_name: string;
  latitude: number;
  longitude: number;
  precip_1d_mm: number;
  precip_30d_mm: number;
  slope_degrees: number;
  elevated_moisture_hazard: boolean;
  observation_time: string;
  data_freshness: string;
  source: string;
}

export interface CurrentWeatherObservation {
  latitude: number;
  longitude: number;
  elevation_m: number;
  temperature_2m_c: number;
  relative_humidity_pct: number;
  precipitation_mm: number;
  surface_pressure_hpa: number;
  wind_speed_10m_ms: number;
  wind_direction_10m_deg: number;
  weather_code: number;
  weather_description: string;
  observation_time: string;
  data_freshness: string;
  source: string;
}

export interface SourceHealthStatus {
  source_id: string;
  name: string;
  status: string;
  endpoint: string;
  requires_api_key: boolean;
  api_key_configured: boolean;
  last_checked: string;
  last_success?: string;
  response_time_ms?: number;
  update_frequency: string;
}

export interface LiveStatusResponse {
  system_status: string;
  timestamp: string;
  sources: SourceHealthStatus[];
  cache_entries_active: number;
  data_policy: string;
}

export interface GenericLiveFeedResponse {
  hazard_type: string;
  total_records: number;
  records_returned: number;
  data_freshness: string;
  retrieval_timestamp: string;
  source_attribution: string;
  data: any[];
}

export interface EnvironmentalContext {
  elevation_m: number;
  slope_degrees: number;
  aspect_degrees: number;
  plan_curvature: number;
  topographic_wetness_index: number;
  dist_to_active_fault_km: number;
  nearest_fault_slip_type: string;
  temp_2m_celsius: number;
  relative_humidity_pct: number;
  wind_speed_10m_ms: number;
  surface_pressure_hpa: number;
  precip_1d_mm: number;
  precip_30d_sum_mm: number;
  river_discharge_m3s: number;
  fwi_fire_weather_index: number;
  weather_description: string;
  data_freshness: string;
  source_attribution: string;
}

export interface HazardAssessmentResult {
  hazard: string;
  model_name: string;
  predicted: boolean;
  probability: number;
  calibrated_probability?: number;
  risk_category: string;
  alert_level: AlertLevel;
  guidance: string;
  operational_status: string;
  secondary_prediction?: Record<string, any>;
  top_features: Array<{
    feature_name?: string;
    feature?: string;
    attribution_value?: number;
    importance_score?: number;
    direction?: string;
    feature_value?: any;
    description?: string;
  }>;
}

export interface GeospatialAssessmentRequest {
  latitude: number;
  longitude: number;
  hazards?: string[];
  scenario_params?: Record<string, any>;
}

export interface GeospatialAssessmentResponse {
  latitude: number;
  longitude: number;
  location_name: string;
  timestamp: string;
  environmental_context: EnvironmentalContext;
  assessments: Record<string, HazardAssessmentResult>;
  overall_composite_risk: AlertLevel;
  overall_summary: string;
  feature_completeness_pct: number;
  disclaimer: string;
}

export interface LocationProfileResponse {
  latitude: number;
  longitude: number;
  timestamp: string;
  environmental_context: EnvironmentalContext;
  nearest_fault: Record<string, any>;
  terrain: Record<string, any>;
  weather: Record<string, any>;
  hydrology: Record<string, any>;
}

export interface LocationSearchResult {
  id: string;
  name: string;
  state?: string;
  country: string;
  display_name: string;
  latitude: number;
  longitude: number;
  place_type: string;
  importance: number;
}

export interface LocationSearchResponse {
  query: string;
  count: number;
  results: LocationSearchResult[];
}

/* Phase 8 Intelligent Early Warning & Alert Management Types */

export type AlertSeverity = AlertLevel;
export type AlertStatus = 'ACTIVE' | 'ACKNOWLEDGED' | 'RESOLVED' | 'EXPIRED';

export interface AlertItem {
  alert_id: string;
  hazard_type: HazardType;
  severity: AlertLevel;
  title: string;
  description: string;
  latitude: number;
  longitude: number;
  location_name?: string;
  source: string;
  confidence_score: number;
  status: AlertStatus;
  model_prediction: Record<string, any>;
  guidance: string;
  created_at: string;
  updated_at: string;
  acknowledged_at?: string;
  acknowledged_by?: string;
  resolved_at?: string;
  resolved_by?: string;
  resolution_notes?: string;
  dedup_key: string;
  notification_sent: boolean;
  disclaimer: string;
}

export interface AlertListResponse {
  total: number;
  page: number;
  page_size: number;
  items: AlertItem[];
}

export interface AlertSummaryResponse {
  total_active: number;
  total_severe_red: number;
  total_high_orange: number;
  total_moderate_yellow: number;
  by_hazard: Record<string, number>;
  recent_alerts: AlertItem[];
  monitor_status: Record<string, any>;
  data_policy: string;
}

export interface AlertAuditLogItem {
  id: number;
  alert_id: string;
  previous_status?: string;
  new_status: string;
  action_type: string;
  performed_by: string;
  notes?: string;
  timestamp: string;
}

export interface MonitorStatusResponse {
  is_running: boolean;
  interval_seconds: number;
  last_run_timestamp?: string;
  next_run_timestamp?: string;
  total_cycles_completed: number;
  total_alerts_generated: number;
  total_alerts_updated: number;
  last_cycle_duration_ms?: number;
  last_error?: string;
}

// ==========================================
// Phase 10: Multi-Hazard Forecasting Schemas
// ==========================================

export type ForecastHorizon = '6h' | '12h' | '24h' | '48h' | '72h';

export type ForecastRiskCategory = 'LOW' | 'MODERATE' | 'HIGH' | 'VERY HIGH' | 'EXTREME';

export type DataProvenanceType =
  | 'LIVE_OBSERVATION'
  | 'LIVE_FORECAST'
  | 'CACHED_OBSERVATION'
  | 'CACHED_FORECAST'
  | 'HISTORICAL_BENCHMARK'
  | 'MODEL_INFERENCE'
  | 'SIMULATED';

export interface ContributingFactor {
  name: string;
  value: string | number;
  direction?: 'INCREASING' | 'DECREASING' | 'NEUTRAL';
}

export interface HorizonForecastItem {
  horizon: ForecastHorizon;
  valid_from: string;
  valid_until: string;
  risk_score: number;
  risk_category: ForecastRiskCategory;
  primary_metric_label: string;
  primary_metric_value: number;
  primary_metric_unit: string;
  contributing_factors: ContributingFactor[];
  confidence_level: 'HIGH' | 'MODERATE' | 'LOW';
  data_sources: string[];
  data_provenance: DataProvenanceType;
}

export interface SingleHazardForecast {
  hazard_type: HazardType;
  geographic_location: string;
  latitude: number;
  longitude: number;
  forecast_generated_at: string;
  forecast_valid_from: string;
  forecast_valid_until: string;
  forecast_horizon: ForecastHorizon;
  risk_score: number;
  risk_category: ForecastRiskCategory;
  model_name: string;
  model_version: string;
  model_status: string;
  contributing_features: Record<string, any>;
  explanation: string;
  confidence_or_uncertainty: Record<string, any>;
  data_sources: string[];
  data_freshness: string;
  data_provenance: DataProvenanceType;
  warnings: string[];
  limitations: string[];
  secondary_metrics: Record<string, any>;
}

export interface HazardForecastTimeline {
  hazard_type: HazardType;
  geographic_location: string;
  latitude: number;
  longitude: number;
  generated_at: string;
  model_name: string;
  model_status: string;
  horizons: Record<string, HorizonForecastItem>;
  overall_trend: 'INCREASING' | 'DECREASING' | 'STABLE';
  peak_risk_horizon: ForecastHorizon;
  peak_risk_score: number;
  disclaimer: string;
}

export interface ForecastSummaryCard {
  hazard_type: HazardType;
  current_status: string;
  forecast_risk: ForecastRiskCategory;
  forecast_horizon: ForecastHorizon;
  primary_metric_name: string;
  primary_metric_value: number;
  primary_metric_unit: string;
  trend: 'INCREASING' | 'DECREASING' | 'STABLE';
  peak_risk_horizon: ForecastHorizon;
  peak_risk_score: number;
  primary_data_source: string;
  data_provenance: DataProvenanceType;
  data_freshness: string;
  target_location: string;
  updated_at: string;
}

export interface MultiHazardLocationForecastResponse {
  location_name: string;
  latitude: number;
  longitude: number;
  generated_at: string;
  composite_risk_category: ForecastRiskCategory;
  composite_risk_score: number;
  primary_hazard: string;
  hazard_forecasts: Record<string, SingleHazardForecast>;
  timeline_by_hazard: Record<string, HazardForecastTimeline>;
  active_observations_summary: Record<string, any>;
  sources_used: Array<{ name: string; data_type: string }>;
  limitations: string[];
  disclaimer: string;
}

export interface IntelligenceSource {
  source_id: string;
  name: string;
  organization: string;
  data_category: string;
  hazards: string[];
  feed_type: string;
  update_cadence: string;
  endpoint_url: string;
  auth_required: boolean;
  rate_limit: string;
  status: 'CONNECTED' | 'DEGRADED' | 'UNAVAILABLE' | 'CACHED';
  freshness_level: 'FRESH' | 'ACCEPTABLE' | 'STALE' | 'UNAVAILABLE';
  last_updated: string;
  latency_ms: number;
  records_last_ingest: number;
  historical_benchmark_active: boolean;
  scientific_caveat: string;
}

export interface DataFreshnessReport {
  generated_at: string;
  total_sources: number;
  fresh_sources: number;
  acceptable_sources: number;
  stale_sources: number;
  unavailable_sources: number;
  sources: Record<string, {
    status: string;
    age_seconds: number;
    age_human: string;
    threshold_fresh_seconds: number;
    threshold_stale_seconds: number;
    is_live: boolean;
  }>;
}

export interface IngestionStatusResponse {
  is_running: boolean;
  interval_sec: number;
  last_cycle_timestamp?: string;
  last_cycle_duration_ms?: number;
  last_cycle_summary?: Record<string, any>;
}

export interface ForecastEvaluationReport {
  evaluation_date: string;
  overall_verdict: string;
  tasks: Array<{
    hazard: string;
    task: string;
    primary_metric: string;
    operational_test_score: number;
    governance_status: string;
    forecast_horizon: string;
    verified_data_provenance: string;
  }>;
}


