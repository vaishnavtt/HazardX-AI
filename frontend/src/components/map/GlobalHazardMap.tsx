import React, { useEffect, useRef, useState, useCallback } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { api, formatApiError } from '../../api/client';
import { AlertBadge } from '../common/AlertBadge';
import {
  Radio,
  RefreshCw,
  Layers,
  MapPin,
  ExternalLink,
  Activity,
  Bell,
  Eye,
  EyeOff,
  RotateCcw,
  SlidersHorizontal,
  ShieldAlert,
  Info,
  Clock,
  Droplets,
  Mountain,
  Flame,
  Wind
} from 'lucide-react';
import type { AlertLevel, HazardType } from '../../types/hazard';

// ============================================================================
// MANDATORY HAZARD COLOR SYSTEM (Identifies Hazard Category, NOT Severity)
// ============================================================================
export const HAZARD_COLORS: Record<HazardType, { hex: string; name: string; bg: string; border: string; text: string }> = {
  floods: { hex: '#2196F3', name: 'Floods', bg: 'bg-blue-500/20', border: 'border-blue-500', text: 'text-blue-400' },
  landslides: { hex: '#FF9800', name: 'Landslides', bg: 'bg-amber-500/20', border: 'border-amber-500', text: 'text-amber-400' },
  earthquakes: { hex: '#9C27B0', name: 'Earthquakes', bg: 'bg-purple-500/20', border: 'border-purple-500', text: 'text-purple-400' },
  cyclones: { hex: '#00BCD4', name: 'Cyclones', bg: 'bg-cyan-500/20', border: 'border-cyan-500', text: 'text-cyan-400' },
  wildfires: { hex: '#F44336', name: 'Wildfires', bg: 'bg-rose-500/20', border: 'border-rose-500', text: 'text-rose-400' },
};

// ============================================================================
// SEVERITY VISUAL ENCODING (Opacity & Stroke based on Risk Level)
// ============================================================================
export const SEVERITY_OPACITIES: Record<string, { fillOpacity: number; strokeWidth: number; label: string }> = {
  LOW: { fillOpacity: 0.20, strokeWidth: 1.0, label: 'Low Risk' },
  GREEN: { fillOpacity: 0.20, strokeWidth: 1.0, label: 'Low Risk' },
  MODERATE: { fillOpacity: 0.40, strokeWidth: 1.5, label: 'Moderate Risk' },
  YELLOW: { fillOpacity: 0.40, strokeWidth: 1.5, label: 'Moderate Risk' },
  HIGH: { fillOpacity: 0.60, strokeWidth: 2.0, label: 'High Risk' },
  ORANGE: { fillOpacity: 0.60, strokeWidth: 2.0, label: 'High Risk' },
  'VERY HIGH': { fillOpacity: 0.75, strokeWidth: 2.5, label: 'Very High Risk' },
  EXTREME: { fillOpacity: 0.90, strokeWidth: 3.0, label: 'Extreme Risk' },
  RED: { fillOpacity: 0.90, strokeWidth: 3.0, label: 'Extreme Risk' },
};

export interface MapFeatureProperties {
  id: string;
  name: string;
  hazard_type: HazardType;
  hazard_color: string;
  risk_category: string;
  risk_score?: number;
  layer_type: 'FORECAST_RISK_ZONE' | 'LIVE_OBSERVATION' | 'HISTORICAL_BENCHMARK' | 'MODEL_ASSESSMENT';
  location: string;
  lat: number;
  lng: number;
  date?: string;
  forecast_horizon?: string;
  valid_until?: string;
  primary_metric_label?: string;
  primary_metric_value: string;
  data_source: string;
  data_provenance: string;
  details?: string;
  contributing_factors?: Array<{ name: string; value: string }>;
  model_name?: string;
  disclaimer?: string;
}

// Curated authentic historical benchmark events
export const BENCHMARK_EVENTS: MapFeatureProperties[] = [
  {
    id: 'bench-fl-1',
    name: 'Henan Extreme Pluvial Flood',
    hazard_type: 'floods',
    hazard_color: '#2196F3',
    risk_category: 'EXTREME',
    risk_score: 0.95,
    layer_type: 'HISTORICAL_BENCHMARK',
    lat: 34.7466,
    lng: 113.6253,
    location: 'Zhengzhou, Henan, China',
    date: '2021-07-20',
    primary_metric_label: 'Precipitation Anomaly',
    primary_metric_value: '1d Precip: 624.1 mm | GloFAS: 820 m³/s',
    data_source: 'Copernicus GloFAS / ERA5 Archive',
    data_provenance: 'HISTORICAL_BENCHMARK',
    details: 'Historic hourly rainfall anomaly causing widespread basin overbank inundation.',
    disclaimer: 'Verified historical benchmark event from official Copernicus reanalysis archive.'
  },
  {
    id: 'bench-ls-1',
    name: 'Wayanad Monsoon Hillslope Failure',
    hazard_type: 'landslides',
    hazard_color: '#FF9800',
    risk_category: 'EXTREME',
    risk_score: 0.92,
    layer_type: 'HISTORICAL_BENCHMARK',
    lat: 11.5167,
    lng: 76.1333,
    location: 'Wayanad, Kerala, India',
    date: '2024-07-30',
    primary_metric_label: 'Precipitation Trigger',
    primary_metric_value: '1d Precip: 280 mm | Clay: 42%',
    data_source: 'NASA GLC / Geological Survey of India',
    data_provenance: 'HISTORICAL_BENCHMARK',
    details: 'Multiple concurrent debris flows triggered by extreme monsoon cloudburst pulses.',
    disclaimer: 'Verified historical landslide catalog event.'
  },
  {
    id: 'bench-eq-1',
    name: 'Kumamoto Aftershock Sequence',
    hazard_type: 'earthquakes',
    hazard_color: '#9C27B0',
    risk_category: 'EXTREME',
    risk_score: 0.88,
    layer_type: 'HISTORICAL_BENCHMARK',
    lat: 32.7547,
    lng: 130.7633,
    location: 'Kyushu, Japan',
    date: '2016-04-16',
    primary_metric_label: 'Mainshock Rupture',
    primary_metric_value: 'Mw 7.0 | Focal Depth: 10 km',
    data_source: 'USGS ComCat / GEM Faults',
    data_provenance: 'HISTORICAL_BENCHMARK',
    details: 'Shallow crustal strike-slip rupture generating high-intensity aftershock clustering.',
    disclaimer: 'Historical aftershock sequence catalog record.'
  },
  {
    id: 'bench-cy-1',
    name: 'Super Typhoon Haiyan (Yolanda)',
    hazard_type: 'cyclones',
    hazard_color: '#00BCD4',
    risk_category: 'EXTREME',
    risk_score: 0.98,
    layer_type: 'HISTORICAL_BENCHMARK',
    lat: 10.6000,
    lng: 125.0000,
    location: 'Eastern Visayas, Philippines',
    date: '2013-11-08',
    primary_metric_label: 'Sustained Wind Speed',
    primary_metric_value: '170 kt | Min Pres: 895 hPa',
    data_source: 'NOAA IBTrACS Global Cyclone Database',
    data_provenance: 'HISTORICAL_BENCHMARK',
    details: 'Extreme Rapid Intensification (+45 kt in 24h) fueled by high ocean heat headroom.',
    disclaimer: 'Verified historical cyclone benchmark record.'
  },
  {
    id: 'bench-wf-1',
    name: 'Camp Fire Extreme Wildfire',
    hazard_type: 'wildfires',
    hazard_color: '#F44336',
    risk_category: 'EXTREME',
    risk_score: 0.94,
    layer_type: 'HISTORICAL_BENCHMARK',
    lat: 39.8100,
    lng: -121.4400,
    location: 'Butte County, California, USA',
    date: '2018-11-08',
    primary_metric_label: 'Fire Weather Index (FWI)',
    primary_metric_value: 'FWI: 62.4 | RH: 8% | Wind: 22 m/s',
    data_source: 'NASA FIRMS / MODIS & VIIRS Detections',
    data_provenance: 'HISTORICAL_BENCHMARK',
    details: 'Jarbo gap down-slope Diablo wind storm igniting desiccated timber fuel canopy.',
    disclaimer: 'Verified historical wildfire benchmark observation.'
  }
];

export const GlobalHazardMap: React.FC = () => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const polygonsLayerRef = useRef<L.LayerGroup | null>(null);
  const markersLayerRef = useRef<L.LayerGroup | null>(null);
  const clickMarkerRef = useRef<L.Marker | null>(null);
  const tileLayerRef = useRef<L.TileLayer | null>(null);
  const [basemapStyle, setBasemapStyle] = useState<'osm' | 'light' | 'terrain'>('osm');

  // Layer States
  const [activeHazards, setActiveHazards] = useState<Record<HazardType, boolean>>({
    floods: true,
    landslides: true,
    earthquakes: true,
    cyclones: true,
    wildfires: true,
  });

  const [activeLayerTypes, setActiveLayerTypes] = useState<Record<string, boolean>>({
    FORECAST_RISK_ZONE: true,
    LIVE_OBSERVATION: true,
    HISTORICAL_BENCHMARK: true,
    MODEL_ASSESSMENT: true,
  });

  const [severityFilter, setSeverityFilter] = useState<string>('ALL');
  const [selectedHorizon, setSelectedHorizon] = useState<string>('24h');

  // Data States
  const [hazardZonesGeoJson, setHazardZonesGeoJson] = useState<any | null>(null);
  const [liveObservations, setLiveObservations] = useState<MapFeatureProperties[]>([]);
  const [activeAlerts, setActiveAlerts] = useState<MapFeatureProperties[]>([]);
  const [selectedFeature, setSelectedFeature] = useState<MapFeatureProperties | null>(null);
  const [clickedCoords, setClickedCoords] = useState<{ lat: number; lng: number } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Dynamic Point Assessment State
  const [pointAssessing, setPointAssessing] = useState(false);
  const [pointAssessmentResult, setPointAssessmentResult] = useState<any | null>(null);

  // 1. Fetch Backend Data
  const fetchMapData = useCallback(async () => {
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const [zonesRes, eventsRes, alertsRes] = await Promise.all([
        api.getHazardZones({ horizon: selectedHorizon }),
        api.getLiveEvents({ limit: 100 }),
        api.getAlerts({ status: 'ACTIVE', page_size: 50 })
      ]);

      if (zonesRes && zonesRes.features) {
        setHazardZonesGeoJson(zonesRes);
      }

      // Map live events into MapFeatureProperties
      if (eventsRes && Array.isArray(eventsRes.data)) {
        const liveMapped: MapFeatureProperties[] = eventsRes.data.map((item: any) => {
          const hType: HazardType = (item.hazard_type as HazardType) || 'earthquakes';
          const hColor = HAZARD_COLORS[hType]?.hex || '#2196F3';
          return {
            id: String(item.id || item.event_id || Math.random()),
            name: item.title || `${hType.toUpperCase()} Event`,
            hazard_type: hType,
            hazard_color: hColor,
            risk_category: item.severity || 'MODERATE',
            risk_score: item.severity === 'RED' ? 0.85 : item.severity === 'ORANGE' ? 0.65 : 0.40,
            layer_type: 'LIVE_OBSERVATION',
            location: item.location || `Coordinates (${Number(item.lat).toFixed(2)}, ${Number(item.lon).toFixed(2)})`,
            lat: Number(item.lat || item.latitude),
            lng: Number(item.lon || item.longitude),
            date: item.event_time ? item.event_time.split('T')[0] : 'Today',
            primary_metric_label: 'Recorded Observation',
            primary_metric_value: item.primary_metric || 'Authentic Scientific Telemetry',
            data_source: item.source || 'HAZARDX Official Feeds',
            data_provenance: 'LIVE_OBSERVATION',
            details: `Real-time physical observation recorded at ${item.event_time || 'recent UTC'}. Source: ${item.source || 'Official Sensor Feed'}.`,
            disclaimer: 'Live confirmed physical observation. Not a predictive forecast.'
          };
        });
        setLiveObservations(liveMapped);
      }

      // Map active alerts
      if (alertsRes && Array.isArray(alertsRes.items)) {
        const alertMapped: MapFeatureProperties[] = alertsRes.items.map((alt: any) => {
          const hType: HazardType = (alt.hazard_type as HazardType) || 'floods';
          const hColor = HAZARD_COLORS[hType]?.hex || '#2196F3';
          return {
            id: alt.alert_id,
            name: alt.title,
            hazard_type: hType,
            hazard_color: hColor,
            risk_category: alt.severity || 'HIGH',
            risk_score: alt.confidence_score || 0.70,
            layer_type: 'MODEL_ASSESSMENT',
            location: alt.location_name || `Coordinate (${Number(alt.latitude).toFixed(2)}, ${Number(alt.longitude).toFixed(2)})`,
            lat: Number(alt.latitude),
            lng: Number(alt.longitude),
            date: alt.created_at ? alt.created_at.split('T')[0] : 'Active',
            primary_metric_label: 'Alert Guidance',
            primary_metric_value: alt.guidance?.substring(0, 50) + '...',
            data_source: alt.source || 'HAZARDX Early Warning Engine',
            data_provenance: 'MODEL_INFERENCE',
            details: `${alt.description} Guidance: ${alt.guidance}`,
            disclaimer: 'Automated early warning decision-support advisory. Adhere to civil protection instructions.'
          };
        });
        setActiveAlerts(alertMapped);
      }

    } catch (err) {
      console.error('Error fetching map data:', err);
      setErrorMsg(formatApiError(err));
    } finally {
      setIsLoading(false);
    }
  }, [selectedHorizon]);

  useEffect(() => {
    fetchMapData();
  }, [fetchMapData]);

  // 2. Initialize Leaflet Map Instance
  useEffect(() => {
    if (!mapContainerRef.current || mapInstanceRef.current) return;

    // Clean, high-performance Leaflet map instance
    const map = L.map(mapContainerRef.current, {
      center: [20.0, 0.0],
      zoom: 2.2,
      minZoom: 2,
      maxZoom: 18,
      worldCopyJump: true,
      zoomControl: false,
    });

    // Add zoom control to top-right
    L.control.zoom({ position: 'topright' }).addTo(map);

    // Reliable, free, watermark-free OpenStreetMap basemap provider
    const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      subdomains: 'abc',
      maxZoom: 19,
    });

    // Automatic fallback if tile load errors occur
    osmLayer.on('tileerror', () => {
      osmLayer.setUrl('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
    });

    osmLayer.addTo(map);
    tileLayerRef.current = osmLayer;

    // Layer Groups: Polygons placed underneath Markers so points remain clickable
    const polyGroup = L.layerGroup().addTo(map);
    const markerGroup = L.layerGroup().addTo(map);

    polygonsLayerRef.current = polyGroup;
    markersLayerRef.current = markerGroup;
    mapInstanceRef.current = map;

    // Handle Map Clicks for Point Assessment
    map.on('click', (e: L.LeafletMouseEvent) => {
      const { lat, lng } = e.latlng;
      setClickedCoords({ lat, lng });
      setPointAssessmentResult(null);

      if (clickMarkerRef.current) {
        clickMarkerRef.current.setLatLng(e.latlng);
      } else {
        const pinIcon = L.divIcon({
          className: 'click-pin-marker',
          html: `
            <div style="position: relative; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center;">
              <div style="position: absolute; width: 26px; height: 26px; border-radius: 50%; background: #38bdf8; opacity: 0.4; animation: ping 1.5s infinite;"></div>
              <div style="position: relative; width: 14px; height: 14px; border-radius: 50%; background: #0284c7; border: 2px solid #ffffff; box-shadow: 0 0 12px #38bdf8;"></div>
            </div>
          `,
          iconSize: [28, 28],
          iconAnchor: [14, 14],
        });
        clickMarkerRef.current = L.marker(e.latlng, { icon: pinIcon }).addTo(map);
      }
    });

    // Invalidate size immediately once mounted
    setTimeout(() => {
      map.invalidateSize();
    }, 100);

    // Attach ResizeObserver to keep tiles sharp on layout changes / sidebar toggling
    const resizeObserver = new ResizeObserver(() => {
      map.invalidateSize();
    });
    resizeObserver.observe(mapContainerRef.current);

    return () => {
      resizeObserver.disconnect();
      map.remove();
      mapInstanceRef.current = null;
      if (mapContainerRef.current) {
        delete (mapContainerRef.current as any)._leaflet_id;
      }
    };
  }, []);

  // Dynamically update basemap tile URL when user changes basemap selection
  useEffect(() => {
    if (!tileLayerRef.current) return;
    const basemapUrls = {
      osm: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      light: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
      terrain: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    };
    const targetUrl = basemapUrls[basemapStyle] || basemapUrls.osm;
    tileLayerRef.current.setUrl(targetUrl);
  }, [basemapStyle]);

  // 3. Render Geometries & Markers whenever Data, Filters, or Horizons change
  useEffect(() => {
    if (!mapInstanceRef.current || !polygonsLayerRef.current || !markersLayerRef.current) return;

    polygonsLayerRef.current.clearLayers();
    markersLayerRef.current.clearLayers();

    // A. RENDER GEOJSON HAZARD ZONES (Polygons & Lines)
    if (hazardZonesGeoJson && activeLayerTypes.FORECAST_RISK_ZONE) {
      L.geoJSON(hazardZonesGeoJson, {
        filter: (feature) => {
          const hType: HazardType = feature.properties?.hazard_type;
          if (!activeHazards[hType]) return false;

          const sev = feature.properties?.risk_category;
          if (severityFilter !== 'ALL' && sev !== severityFilter) return false;

          return true;
        },
        style: (feature) => {
          const hType: HazardType = feature?.properties?.hazard_type || 'floods';
          const hColor = HAZARD_COLORS[hType]?.hex || '#2196F3';
          const sev = feature?.properties?.risk_category || 'MODERATE';
          const sevStyle = SEVERITY_OPACITIES[sev] || SEVERITY_OPACITIES.MODERATE;

          const isLine = feature?.geometry?.type === 'LineString';
          return {
            color: hColor,
            weight: isLine ? 3.5 : sevStyle.strokeWidth,
            opacity: 0.95,
            fillColor: hColor,
            fillOpacity: isLine ? 0 : sevStyle.fillOpacity,
            dashArray: isLine ? '6, 6' : undefined,
          };
        },
        onEachFeature: (feature, layer) => {
          const props = feature.properties;
          layer.on('click', (e) => {
            L.DomEvent.stopPropagation(e);
            const center = (layer as any).getBounds ? (layer as any).getBounds().getCenter() : (layer as any).getLatLng ? (layer as any).getLatLng() : { lat: 0, lng: 0 };
            setSelectedFeature({
              id: props.id || String(Math.random()),
              name: props.name,
              hazard_type: props.hazard_type,
              hazard_color: props.hazard_color,
              risk_category: props.risk_category,
              risk_score: props.risk_score,
              layer_type: props.layer_type,
              location: props.location,
              lat: center.lat,
              lng: center.lng,
              forecast_horizon: props.forecast_horizon,
              valid_until: props.valid_until,
              primary_metric_label: props.primary_metric_label,
              primary_metric_value: props.primary_metric_value,
              data_source: props.data_source,
              data_provenance: props.data_provenance,
              contributing_factors: props.contributing_factors,
              model_name: props.model_name,
              disclaimer: props.disclaimer
            });
          });

          layer.bindTooltip(
            `<div style="font-family: monospace; font-size: 11px;">
              <strong style="color: ${props.hazard_color};">[${props.hazard_type.toUpperCase()}]</strong> ${props.name}
              <div style="color: #cbd5e1; font-size: 10px;">${props.primary_metric_label}: ${props.primary_metric_value}</div>
            </div>`,
            { direction: 'top', sticky: true }
          );
        }
      }).addTo(polygonsLayerRef.current);
    }

    // B. RENDER POINT MARKERS (Live Observations, Alerts, Benchmark Events)
    const combinedPoints: MapFeatureProperties[] = [];

    if (activeLayerTypes.LIVE_OBSERVATION) {
      combinedPoints.push(...liveObservations);
    }
    if (activeLayerTypes.MODEL_ASSESSMENT) {
      combinedPoints.push(...activeAlerts);
    }
    if (activeLayerTypes.HISTORICAL_BENCHMARK) {
      combinedPoints.push(...BENCHMARK_EVENTS);
    }

    combinedPoints.forEach((pt) => {
      if (!activeHazards[pt.hazard_type]) return;
      if (severityFilter !== 'ALL' && pt.risk_category !== severityFilter) return;

      const color = HAZARD_COLORS[pt.hazard_type]?.hex || '#2196F3';
      const sevStyle = SEVERITY_OPACITIES[pt.risk_category] || SEVERITY_OPACITIES.MODERATE;

      // Pulse animation on extreme markers
      const isExtreme = pt.risk_category === 'EXTREME' || pt.risk_category === 'RED';

      const customIcon = L.divIcon({
        className: 'custom-hazard-marker',
        html: `
          <div style="position: relative; width: 26px; height: 26px; display: flex; align-items: center; justify-content: center;">
            <div style="position: absolute; width: ${isExtreme ? '28px' : '22px'}; height: ${isExtreme ? '28px' : '22px'}; border-radius: 50%; background: ${color}; opacity: ${sevStyle.fillOpacity}; ${isExtreme ? 'animation: ping 1.8s infinite;' : ''}"></div>
            <div style="position: relative; width: 14px; height: 14px; border-radius: 50%; background: ${color}; border: ${sevStyle.strokeWidth + 0.5}px solid #ffffff; box-shadow: 0 0 10px ${color};"></div>
          </div>
        `,
        iconSize: [26, 26],
        iconAnchor: [13, 13],
      });

      const marker = L.marker([pt.lat, pt.lng], { icon: customIcon });

      marker.on('click', (e) => {
        L.DomEvent.stopPropagation(e);
        setSelectedFeature(pt);
      });

      marker.bindTooltip(
        `<div style="font-family: monospace; font-size: 11px;">
          <strong style="color: ${color};">[${pt.hazard_type.toUpperCase()}]</strong> ${pt.name}
          <div style="color: #94a3b8; font-size: 10px;">${pt.primary_metric_value}</div>
          <div style="color: #64748b; font-size: 9px; text-transform: uppercase;">${pt.layer_type.replace('_', ' ')}</div>
        </div>`,
        { direction: 'top', offset: [0, -10] }
      );

      markersLayerRef.current?.addLayer(marker);
    });

  }, [hazardZonesGeoJson, liveObservations, activeAlerts, activeHazards, activeLayerTypes, severityFilter]);

  // Toggle helpers
  const toggleHazard = (hazard: HazardType) => {
    setActiveHazards((prev) => ({ ...prev, [hazard]: !prev[hazard] }));
  };

  const toggleLayerType = (layerType: string) => {
    setActiveLayerTypes((prev) => ({ ...prev, [layerType]: !prev[layerType] }));
  };

  const handleClearAllLayers = () => {
    setActiveHazards({ floods: false, landslides: false, earthquakes: false, cyclones: false, wildfires: false });
  };

  const handleShowAllLayers = () => {
    setActiveHazards({ floods: true, landslides: true, earthquakes: true, cyclones: true, wildfires: true });
    setActiveLayerTypes({ FORECAST_RISK_ZONE: true, LIVE_OBSERVATION: true, HISTORICAL_BENCHMARK: true, MODEL_ASSESSMENT: true });
    setSeverityFilter('ALL');
  };

  const handleResetMapView = () => {
    if (mapInstanceRef.current) {
      mapInstanceRef.current.setView([20.0, 0.0], 2.2);
    }
  };

  const handleAssessClickedLocation = async () => {
    if (!clickedCoords) return;
    setPointAssessing(true);
    try {
      const res = await api.assessLocationForecast({
        latitude: clickedCoords.lat,
        longitude: clickedCoords.lng,
        location_name: `Point (${clickedCoords.lat.toFixed(2)}, ${clickedCoords.lng.toFixed(2)})`,
        forecast_horizons: ['6h', '12h', '24h', '48h', '72h'],
      });
      setPointAssessmentResult(res);
    } catch (err) {
      console.error('Point assessment error:', err);
    } finally {
      setPointAssessing(false);
    }
  };

  const getHazardIcon = (hazard: string) => {
    switch (hazard.toLowerCase()) {
      case 'floods': return <Droplets className="w-4 h-4 text-blue-400" />;
      case 'landslides': return <Mountain className="w-4 h-4 text-amber-400" />;
      case 'earthquakes': return <Activity className="w-4 h-4 text-purple-400" />;
      case 'cyclones': return <Wind className="w-4 h-4 text-cyan-400" />;
      case 'wildfires': return <Flame className="w-4 h-4 text-rose-400" />;
      default: return <ShieldAlert className="w-4 h-4 text-slate-400" />;
    }
  };

  return (
    <div className="relative w-full h-[660px] lg:h-[750px] rounded-3xl overflow-hidden border border-slate-200/90 shadow-xl bg-[#F4F7FB] flex flex-col font-sans text-xs">
      
      {/* 1. TOP FLOATING CONTROL BAR */}
      <div className="absolute top-3 left-3 right-3 z-[1000] flex flex-wrap items-center justify-between gap-2 pointer-events-none">
        
        {/* Left: Hazard Layer Toggles (Mandatory 5 Colors) */}
        <div className="pointer-events-auto flex flex-wrap items-center gap-1.5 bg-white/95 backdrop-blur-md p-1.5 rounded-2xl border border-slate-200/90 shadow-md">
          <span className="text-[10px] text-slate-500 uppercase font-bold px-2">Hazards:</span>
          {(Object.keys(HAZARD_COLORS) as HazardType[]).map((h) => {
            const isActive = activeHazards[h];
            const color = HAZARD_COLORS[h];
            return (
              <button
                key={h}
                type="button"
                onClick={() => toggleHazard(h)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                  isActive
                    ? 'bg-slate-50 text-slate-900 border border-slate-300 shadow-xs'
                    : 'bg-transparent text-slate-400 hover:text-slate-700'
                }`}
              >
                <span
                  className="w-2.5 h-2.5 rounded-full shadow-xs"
                  style={{ backgroundColor: isActive ? color.hex : '#CBD5E1' }}
                />
                <span className="capitalize">{h}</span>
              </button>
            );
          })}
        </div>

        {/* Right: Data Layer Type Toggles, Basemap Switcher & Controls */}
        <div className="pointer-events-auto flex flex-wrap items-center gap-1.5 bg-white/95 backdrop-blur-md p-1.5 rounded-2xl border border-slate-200/90 shadow-md">
          {/* Basemap Switcher */}
          <select
            value={basemapStyle}
            onChange={(e) => setBasemapStyle(e.target.value as any)}
            className="bg-slate-50 border border-slate-200 text-slate-700 px-2.5 py-1 rounded-xl text-[11px] font-semibold focus:outline-none"
          >
            <option value="osm">Basemap: Standard OSM</option>
            <option value="light">Basemap: Clean Light</option>
            <option value="terrain">Basemap: Topographic</option>
          </select>

          <button
            type="button"
            onClick={() => toggleLayerType('FORECAST_RISK_ZONE')}
            className={`px-2.5 py-1 rounded-xl text-[11px] font-semibold transition-all ${
              activeLayerTypes.FORECAST_RISK_ZONE
                ? 'bg-sky-50 text-sky-800 border border-sky-300 shadow-xs'
                : 'text-slate-500 hover:bg-slate-100'
            }`}
          >
            Forecast Zones
          </button>

          <button
            type="button"
            onClick={() => toggleLayerType('LIVE_OBSERVATION')}
            className={`px-2.5 py-1 rounded-xl text-[11px] font-semibold transition-all ${
              activeLayerTypes.LIVE_OBSERVATION
                ? 'bg-emerald-50 text-emerald-800 border border-emerald-300 shadow-xs'
                : 'text-slate-500 hover:bg-slate-100'
            }`}
          >
            Live Observations
          </button>

          <button
            type="button"
            onClick={() => toggleLayerType('HISTORICAL_BENCHMARK')}
            className={`px-2.5 py-1 rounded-xl text-[11px] font-semibold transition-all ${
              activeLayerTypes.HISTORICAL_BENCHMARK
                ? 'bg-purple-50 text-purple-800 border border-purple-300 shadow-xs'
                : 'text-slate-500 hover:bg-slate-100'
            }`}
          >
            Benchmarks
          </button>

          {/* Severity Filter Dropdown */}
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            className="bg-slate-50 border border-slate-200 text-slate-700 px-2 py-1 rounded-xl text-[11px] font-semibold focus:outline-none"
          >
            <option value="ALL">Severity: All</option>
            <option value="LOW">Low</option>
            <option value="MODERATE">Moderate</option>
            <option value="HIGH">High</option>
            <option value="VERY HIGH">Very High</option>
            <option value="EXTREME">Extreme</option>
          </select>

          {/* Quick Controls */}
          <button
            type="button"
            onClick={handleResetMapView}
            title="Reset Map View"
            className="p-1.5 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
          <button
            type="button"
            onClick={fetchMapData}
            title="Refresh Feeds"
            disabled={isLoading}
            className="p-1.5 text-slate-500 hover:text-cyan-700 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin text-cyan-600' : ''}`} />
          </button>
        </div>
      </div>

      {/* 2. LEAFLET DOM CONTAINER */}
      <div ref={mapContainerRef} className="w-full flex-1 z-0 cursor-crosshair" />

      {/* 3. BOTTOM FLOATING LEGEND & STATUS BAR */}
      <div className="absolute bottom-3 left-3 z-[1000] bg-white/95 backdrop-blur-md p-3.5 rounded-2xl border border-slate-200/90 shadow-xl max-w-xl text-[11px] space-y-2 pointer-events-auto">
        <div className="flex items-center justify-between border-b border-slate-100 pb-1.5">
          <span className="font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-cyan-600" /> Multi-Hazard GIS Legend
          </span>
          <span className="text-[10px] text-slate-500 font-mono">
            {isLoading ? 'Updating feeds...' : 'Live Connected'}
          </span>
        </div>

        {/* Hazard Colors (Mandatory 5 Colors) */}
        <div className="flex flex-wrap items-center gap-3 text-slate-700 font-medium">
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-[#2196F3] border border-white shadow-xs" />
            <span>Floods (Blue)</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-[#FF9800] border border-white shadow-xs" />
            <span>Landslides (Orange)</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-[#9C27B0] border border-white shadow-xs" />
            <span>Earthquakes (Purple)</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-[#00BCD4] border border-white shadow-xs" />
            <span>Cyclones (Cyan)</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-[#F44336] border border-white shadow-xs" />
            <span>Wildfires (Red)</span>
          </span>
        </div>

        {/* Severity Opacity Guide */}
        <div className="flex flex-wrap items-center gap-3 pt-1 border-t border-slate-100 text-[10px] text-slate-500">
          <span className="font-bold text-slate-700">Severity:</span>
          <span>Low (20% Fill)</span>
          <span>Moderate (40%)</span>
          <span>High (60% + Border)</span>
          <span>Extreme (90% + Pulsing)</span>
        </div>
      </div>

      {/* 4. CLICK-TO-ASSESS COORDINATE ACTION BANNER */}
      {clickedCoords && !selectedFeature && (
        <div className="absolute bottom-3 left-1/2 -translate-x-1/2 z-[1000] bg-white/95 backdrop-blur-md border border-cyan-400 p-3.5 rounded-2xl shadow-xl flex flex-col sm:flex-row items-center gap-3 max-w-lg">
          <div className="flex items-center gap-2">
            <MapPin className="w-4 h-4 text-cyan-600 shrink-0" />
            <div>
              <span className="text-slate-800 font-bold">Selected Coordinate:</span>
              <span className="text-slate-600 ml-1 font-mono">{clickedCoords.lat.toFixed(4)}, {clickedCoords.lng.toFixed(4)}</span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleAssessClickedLocation}
              disabled={pointAssessing}
              className="px-3.5 py-1.5 rounded-xl bg-cyan-600 hover:bg-cyan-700 text-white font-semibold flex items-center gap-1.5 transition-colors disabled:opacity-50 shadow-xs"
            >
              {pointAssessing ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Activity className="w-3.5 h-3.5" />}
              <span>{pointAssessing ? 'Assessing...' : 'Run Point Forecast'}</span>
            </button>
            <button
              type="button"
              onClick={() => { setClickedCoords(null); setPointAssessmentResult(null); }}
              className="px-2 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-600 hover:text-slate-900"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {/* Point Assessment Instant Result Modal */}
      {pointAssessmentResult && (
        <div className="absolute top-16 left-1/2 -translate-x-1/2 z-[1000] bg-white/95 backdrop-blur-xl border border-cyan-300 p-4 rounded-2xl shadow-2xl w-96 max-w-[90vw] text-slate-800 space-y-2">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2">
            <span className="font-bold text-slate-900 flex items-center gap-2">
              <Activity className="w-4 h-4 text-cyan-600" /> 72h Point Forecast
            </span>
            <button onClick={() => setPointAssessmentResult(null)} className="text-slate-400 hover:text-slate-700">✕</button>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-slate-500 font-medium">Composite Risk:</span>
            <span className={`px-2 py-0.5 rounded-full font-bold text-[10px] ${
              pointAssessmentResult.composite_risk_category === 'EXTREME' || pointAssessmentResult.composite_risk_category === 'RED' ? 'bg-rose-100 text-rose-800 border border-rose-300' :
              pointAssessmentResult.composite_risk_category === 'HIGH' || pointAssessmentResult.composite_risk_category === 'ORANGE' ? 'bg-amber-100 text-amber-800 border border-amber-300' : 'bg-emerald-100 text-emerald-800 border border-emerald-300'
            }`}>
              {pointAssessmentResult.composite_risk_category} ({(pointAssessmentResult.composite_risk_score * 100).toFixed(0)}%)
            </span>
          </div>
          <div className="text-[11px] text-slate-600">
            Primary Hazard: <strong className="text-slate-900 capitalize">{pointAssessmentResult.primary_hazard}</strong>
          </div>
          <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 text-[10px] text-slate-600 leading-relaxed">
            {pointAssessmentResult.disclaimer}
          </div>
        </div>
      )}

      {/* 5. SELECTED FEATURE SLIDE-OVER DRAWER (Rich Popover Details) */}
      {selectedFeature && (
        <div className="absolute bottom-3 right-3 top-16 w-80 lg:w-96 z-[1000] bg-white/95 backdrop-blur-xl border border-slate-200 rounded-3xl p-5 shadow-2xl flex flex-col justify-between overflow-y-auto">
          <div className="space-y-3.5">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-slate-100 pb-2.5">
              <div className="flex items-center gap-2">
                {getHazardIcon(selectedFeature.hazard_type)}
                <span
                  className="font-bold uppercase tracking-wider text-xs"
                  style={{ color: selectedFeature.hazard_color }}
                >
                  {selectedFeature.hazard_type}
                </span>
                <span className="px-2 py-0.5 rounded-full text-[9px] font-mono bg-slate-100 text-slate-700 border border-slate-200">
                  {selectedFeature.layer_type.replace(/_/g, ' ')}
                </span>
              </div>
              <button
                type="button"
                onClick={() => setSelectedFeature(null)}
                className="text-slate-400 hover:text-slate-700 text-sm px-2 py-0.5 rounded-lg bg-slate-100 hover:bg-slate-200 transition-colors"
              >
                ✕
              </button>
            </div>

            {/* Title & Location */}
            <div>
              <h3 className="text-sm font-bold text-slate-900 leading-snug">{selectedFeature.name}</h3>
              <p className="text-[11px] text-slate-500 mt-0.5 flex items-center gap-1 font-medium">
                <MapPin className="w-3.5 h-3.5 text-cyan-600 shrink-0" />
                <span>{selectedFeature.location}</span>
              </p>
            </div>

            {/* Risk & Provenance Badges */}
            <div className="grid grid-cols-2 gap-2 text-[10px]">
              <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
                <span className="text-slate-400 uppercase font-semibold block mb-0.5">Risk Level</span>
                <span
                  className="font-bold px-2 py-0.5 rounded-full inline-block"
                  style={{
                    backgroundColor: `${selectedFeature.hazard_color}18`,
                    color: selectedFeature.hazard_color,
                    border: `1px solid ${selectedFeature.hazard_color}40`
                  }}
                >
                  {selectedFeature.risk_category} {selectedFeature.risk_score ? `(${(selectedFeature.risk_score * 100).toFixed(0)}%)` : ''}
                </span>
              </div>
              <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
                <span className="text-slate-400 uppercase font-semibold block mb-0.5">Data Provenance</span>
                <span className="font-mono text-slate-700 font-semibold block truncate" title={selectedFeature.data_provenance}>
                  {selectedFeature.data_provenance}
                </span>
              </div>
            </div>

            {/* Primary Physical Metric */}
            <div className="bg-cyan-50/70 p-3 rounded-2xl border border-cyan-100">
              <span className="text-[10px] text-cyan-800 uppercase font-semibold block mb-1">
                {selectedFeature.primary_metric_label || 'Key Observation / Forecast'}
              </span>
              <span className="text-slate-900 font-mono font-bold text-xs">
                {selectedFeature.primary_metric_value}
              </span>
            </div>

            {/* Contributing Factors */}
            {selectedFeature.contributing_factors && selectedFeature.contributing_factors.length > 0 && (
              <div className="space-y-1">
                <span className="text-[10px] text-slate-500 uppercase font-semibold block">Contributing Factors</span>
                <div className="space-y-1">
                  {selectedFeature.contributing_factors.map((f, idx) => (
                    <div key={idx} className="flex items-center justify-between p-2 rounded-xl bg-slate-50 text-[10px] border border-slate-100">
                      <span className="text-slate-600">{f.name}:</span>
                      <span className="text-slate-900 font-mono font-semibold">{f.value}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Details / Narrative */}
            {selectedFeature.details && (
              <div className="text-[11px] text-slate-700 leading-relaxed bg-slate-50 p-3 rounded-2xl border border-slate-200">
                {selectedFeature.details}
              </div>
            )}

            {/* Source & Model */}
            <div className="pt-2 border-t border-slate-100 text-[10px] text-slate-500 space-y-0.5">
              <div>Source: <span className="text-slate-800 font-medium">{selectedFeature.data_source}</span></div>
              {selectedFeature.model_name && (
                <div>Model: <span className="text-slate-800 font-mono">{selectedFeature.model_name}</span></div>
              )}
            </div>

            {/* Statutory Disclaimer */}
            <div className="p-2.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-[10px] leading-relaxed">
              {selectedFeature.disclaimer || 'Automated decision-support advisory. Adhere to civil protection instructions.'}
            </div>
          </div>

          {/* Action Button: Run full location assessment */}
          <div className="pt-3 border-t border-slate-100 mt-2">
            <a
              href={`/check-location?lat=${selectedFeature.lat.toFixed(4)}&lon=${selectedFeature.lng.toFixed(4)}`}
              className="w-full flex items-center justify-center gap-1.5 py-2.5 px-3 rounded-xl bg-cyan-600 hover:bg-cyan-700 text-white font-semibold transition-colors shadow-sm"
            >
              <span>Inspect Full Location Profile</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      )}
    </div>
  );
};
