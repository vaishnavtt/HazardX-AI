import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppLayout } from './components/layout/AppLayout';
import { DashboardPage } from './pages/DashboardPage';
import { MapPage } from './pages/MapPage';
import { FloodPage } from './pages/FloodPage';
import { LandslidePage } from './pages/LandslidePage';
import { EarthquakePage } from './pages/EarthquakePage';
import { CyclonePage } from './pages/CyclonePage';
import { WildfirePage } from './pages/WildfirePage';
import { MultiHazardPage } from './pages/MultiHazardPage';
import { ModelsPage } from './pages/ModelsPage';
import { LocationAssessmentPage } from './pages/LocationAssessmentPage';
import { AlertManagementPage } from './pages/AlertManagementPage';
import { ForecastPage } from './pages/ForecastPage';
import { AboutPage } from './pages/AboutPage';
import { PastEventsPage } from './pages/PastEventsPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="map" element={<MapPage />} />
          <Route path="forecasts" element={<ForecastPage />} />
          <Route path="check-location" element={<LocationAssessmentPage />} />
          <Route path="location-assessment" element={<LocationAssessmentPage />} />
          <Route path="alerts" element={<AlertManagementPage />} />
          <Route path="past-events" element={<PastEventsPage />} />
          <Route path="about" element={<AboutPage />} />

          {/* Advanced Model Consoles */}
          <Route path="hazards/floods" element={<FloodPage />} />
          <Route path="hazards/landslides" element={<LandslidePage />} />
          <Route path="hazards/earthquakes" element={<EarthquakePage />} />
          <Route path="hazards/cyclones" element={<CyclonePage />} />
          <Route path="hazards/wildfires" element={<WildfirePage />} />
          <Route path="multi-hazard" element={<MultiHazardPage />} />
          <Route path="models" element={<ModelsPage />} />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
