/**
 * HAZARDX AI — Centralized Axios API Client
 * Interfaces with FastAPI endpoints at /api/v1
 */

import axios, { AxiosError } from 'axios';
import type {
  HealthResponse,
  ModelCatalogResponse,
  ModelPerformanceSummary,
  HazardExplanationResponse,
  DashboardSummaryResponse,
  FloodFeatures,
  FloodPredictionResponse,
  LandslideFeatures,
  LandslidePredictionResponse,
  EarthquakeFeatures,
  EarthquakePredictionResponse,
  CycloneFeatures,
  CyclonePredictionResponse,
  WildfireFeatures,
  WildfirePredictionResponse,
  MultiHazardPredictionRequest,
  MultiHazardPredictionResponse,
  ForecastSummaryCard,
  HazardForecastTimeline,
  MultiHazardLocationForecastResponse,
  ForecastEvaluationReport,
  IntelligenceSource,
  DataFreshnessReport,
  IngestionStatusResponse,
} from '../types/hazard';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

export interface ApiErrorDetail {
  field?: string;
  error?: string;
}

export interface ApiErrorResponse {
  status: string;
  error_code: string;
  message: string;
  details?: ApiErrorDetail[] | string;
}

export const formatApiError = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    const axiosErr = error as AxiosError<ApiErrorResponse>;
    if (axiosErr.response?.data) {
      const data = axiosErr.response.data;
      if (Array.isArray(data.details)) {
        return `${data.message}: ` + data.details.map(d => `${d.field}: ${d.error}`).join(' | ');
      }
      return data.message || `Server error (${axiosErr.response.status})`;
    }
    if (axiosErr.code === 'ERR_NETWORK') {
      return 'Cannot connect to HAZARDX AI backend. Please verify FastAPI is running at http://127.0.0.1:8000.';
    }
    return axiosErr.message;
  }
  return error instanceof Error ? error.message : 'An unexpected error occurred.';
};

export const api = {
  // System Health & Monitoring
  getHealth: async (): Promise<HealthResponse> => {
    const res = await apiClient.get<HealthResponse>('/health');
    return res.data;
  },

  // Model Governance & Performance
  getModels: async (): Promise<ModelCatalogResponse> => {
    const res = await apiClient.get<ModelCatalogResponse>('/models');
    return res.data;
  },

  getModelPerformance: async (): Promise<ModelPerformanceSummary[]> => {
    const res = await apiClient.get<ModelPerformanceSummary[]>('/models/performance');
    return res.data;
  },

  getPhase13Validation: async (): Promise<any> => {
    const res = await apiClient.get<any>('/models/phase13-validation');
    return res.data;
  },

  getDashboardSummary: async (): Promise<DashboardSummaryResponse> => {
    const res = await apiClient.get<DashboardSummaryResponse>('/dashboard/summary');
    return res.data;
  },

  // TreeSHAP Explainability
  getExplanation: async (hazard: string, task?: string): Promise<HazardExplanationResponse> => {
    const res = await apiClient.get<HazardExplanationResponse>(`/explanations/${hazard}`, {
      params: task ? { task } : undefined,
    });
    return res.data;
  },

  // Hazard Predictions
  predictFlood: async (features: FloodFeatures): Promise<FloodPredictionResponse> => {
    const res = await apiClient.post<FloodPredictionResponse>('/predict/flood', features);
    return res.data;
  },

  predictLandslide: async (features: LandslideFeatures): Promise<LandslidePredictionResponse> => {
    const res = await apiClient.post<LandslidePredictionResponse>('/predict/landslide', features);
    return res.data;
  },

  predictEarthquake: async (features: EarthquakeFeatures): Promise<EarthquakePredictionResponse> => {
    const res = await apiClient.post<EarthquakePredictionResponse>('/predict/earthquake', features);
    return res.data;
  },

  predictCyclone: async (features: CycloneFeatures): Promise<CyclonePredictionResponse> => {
    const res = await apiClient.post<CyclonePredictionResponse>('/predict/cyclone', features);
    return res.data;
  },

  predictWildfire: async (features: WildfireFeatures): Promise<WildfirePredictionResponse> => {
    const res = await apiClient.post<WildfirePredictionResponse>('/predict/wildfire', features);
    return res.data;
  },

  predictAll: async (request: MultiHazardPredictionRequest): Promise<MultiHazardPredictionResponse> => {
    const res = await apiClient.post<MultiHazardPredictionResponse>('/predict/all', request);
    return res.data;
  },

  // Real-Time Scientific Data (Phase 6)
  getLiveStatus: async () => {
    const res = await apiClient.get('/live/status');
    return res.data;
  },

  getLiveEarthquakes: async (minMag = 2.5, limit = 100) => {
    const res = await apiClient.get('/live/earthquakes', { params: { min_magnitude: minMag, limit } });
    return res.data;
  },

  getLiveWildfires: async (minConf = 'nominal', limit = 100) => {
    const res = await apiClient.get('/live/wildfires', { params: { min_confidence: minConf, limit } });
    return res.data;
  },

  getLiveCyclones: async (limit = 50) => {
    const res = await apiClient.get('/live/cyclones', { params: { limit } });
    return res.data;
  },

  getLiveFloods: async (lat: number, lon: number, locationName?: string) => {
    const res = await apiClient.get('/live/floods', { params: { lat, lon, location_name: locationName } });
    return res.data;
  },

  getLiveLandslides: async (limit = 20) => {
    const res = await apiClient.get('/live/landslides', { params: { limit } });
    return res.data;
  },

  getLiveWeather: async (lat: number, lon: number) => {
    const res = await apiClient.get('/live/weather', { params: { lat, lon } });
    return res.data;
  },

  getLiveEvents: async (params?: { hazard_type?: string; min_lat?: number; max_lat?: number; min_lon?: number; max_lon?: number; limit?: number }) => {
    const res = await apiClient.get('/live/events', { params });
    return res.data;
  },

  // Geospatial Risk Assessment (Phase 7)
  geocodeLocation: async (query: string, limit = 8) => {
    const res = await apiClient.get('/geospatial/geocode', { params: { q: query, limit } });
    return res.data;
  },

  assessLocationRisk: async (request: any) => {
    const res = await apiClient.post('/geospatial/assess', request);
    return res.data;
  },

  getLocationProfile: async (lat: number, lon: number) => {
    const res = await apiClient.get(`/geospatial/location/${lat}/${lon}`);
    return res.data;
  },

  getHazardZones: async (params?: { hazard_type?: string; layer_type?: string; horizon?: string }) => {
    const res = await apiClient.get('/geospatial/hazard-zones', { params });
    return res.data;
  },

  // Intelligent Alert Management (Phase 8)
  getAlerts: async (params?: {
    hazard_type?: string;
    severity?: string;
    status?: string;
    min_lat?: number;
    max_lat?: number;
    min_lon?: number;
    max_lon?: number;
    start_date?: string;
    end_date?: string;
    page?: number;
    page_size?: number;
  }) => {
    const res = await apiClient.get('/alerts', { params });
    return res.data;
  },

  getAlert: async (alertId: string) => {
    const res = await apiClient.get(`/alerts/${alertId}`);
    return res.data;
  },

  getAlertSummary: async () => {
    const res = await apiClient.get('/alerts/summary');
    return res.data;
  },

  getAlertHistory: async (alertId?: string, limit = 50) => {
    const res = await apiClient.get('/alerts/history', { params: { alert_id: alertId, limit } });
    return res.data;
  },

  acknowledgeAlert: async (alertId: string, acknowledgedBy = 'Duty Disaster Analyst', notes?: string) => {
    const res = await apiClient.post(`/alerts/${alertId}/acknowledge`, { acknowledged_by: acknowledgedBy, notes });
    return res.data;
  },

  resolveAlert: async (alertId: string, resolvedBy = 'Operations Supervisor', resolutionNotes = 'Hazard conditions normalized') => {
    const res = await apiClient.post(`/alerts/${alertId}/resolve`, { resolved_by: resolvedBy, resolution_notes: resolutionNotes });
    return res.data;
  },

  getAlertMonitorStatus: async () => {
    const res = await apiClient.get('/alerts/monitor/status');
    return res.data;
  },

  triggerAlertMonitor: async () => {
    const res = await apiClient.post('/alerts/monitor/trigger');
    return res.data;
  },

  // Phase 10: Multi-Hazard Forecasting & Intelligence
  getForecastSummary: async (): Promise<ForecastSummaryCard[]> => {
    const res = await apiClient.get<ForecastSummaryCard[]>('/forecasts/summary');
    return res.data;
  },

  getForecastTimeline: async (params: {
    hazard: string;
    lat: number;
    lon: number;
    location_name?: string;
  }): Promise<HazardForecastTimeline> => {
    const res = await apiClient.get<HazardForecastTimeline>('/forecasts/timeline', { params });
    return res.data;
  },

  assessLocationForecast: async (request: {
    location_name?: string;
    latitude: number;
    longitude: number;
    forecast_horizons?: string[];
    hazards?: string[];
  }): Promise<MultiHazardLocationForecastResponse> => {
    const res = await apiClient.post<MultiHazardLocationForecastResponse>('/forecasts/assess-location', request);
    return res.data;
  },

  getForecastEvaluations: async (): Promise<ForecastEvaluationReport> => {
    const res = await apiClient.get<ForecastEvaluationReport>('/forecasts/evaluations');
    return res.data;
  },

  getIntelligenceSources: async (): Promise<IntelligenceSource[]> => {
    const res = await apiClient.get<IntelligenceSource[]>('/intelligence/sources');
    return res.data;
  },

  getIntelligenceHealth: async () => {
    const res = await apiClient.get('/intelligence/health');
    return res.data;
  },

  getIntelligenceFreshness: async (): Promise<DataFreshnessReport> => {
    const res = await apiClient.get<DataFreshnessReport>('/intelligence/freshness');
    return res.data;
  },

  getIngestionStatus: async (): Promise<IngestionStatusResponse> => {
    const res = await apiClient.get<IngestionStatusResponse>('/intelligence/ingestion/status');
    return res.data;
  },

  triggerIngestionCycle: async () => {
    const res = await apiClient.post('/intelligence/ingestion/trigger');
    return res.data;
  },
};

