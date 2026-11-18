import React, { useState } from 'react';
import { 
  History, 
  Search, 
  MapPin, 
  Calendar, 
  Filter, 
  Droplets, 
  Mountain, 
  Activity, 
  Wind, 
  Flame,
  ExternalLink,
  ShieldCheck
} from 'lucide-react';
import { GlassCard } from '../components/glass/GlassCard';
import { GlassPanel } from '../components/glass/GlassPanel';
import { LiquidButton } from '../components/ui/LiquidButton';
import { LiquidSegmentedControl } from '../components/ui/LiquidSegmentedControl';
import { Link } from 'react-router-dom';

interface HistoricalEvent {
  id: string;
  name: string;
  hazard_type: 'floods' | 'landslides' | 'earthquakes' | 'cyclones' | 'wildfires';
  location: string;
  country: string;
  date: string;
  severity: 'EXTREME' | 'VERY HIGH' | 'HIGH';
  impactSummary: string;
  keyMetricLabel: string;
  keyMetricValue: string;
  verifiedSource: string;
  coordinates: [number, number];
}

const HISTORICAL_BENCHMARKS: HistoricalEvent[] = [
  {
    id: 'hist-fl-1',
    name: 'Henan Extreme Pluvial Deluge',
    hazard_type: 'floods',
    location: 'Zhengzhou, Henan',
    country: 'China',
    date: 'July 2021',
    severity: 'EXTREME',
    impactSummary: 'Record-shattering hourly precipitation exceeding 201.9 mm/hr resulting in catastrophic urban basin inundation.',
    keyMetricLabel: 'Max 24h Precipitation',
    keyMetricValue: '624.1 mm (1-in-1000 yr)',
    verifiedSource: 'China Meteorological Administration & GloFAS Benchmark',
    coordinates: [34.7466, 113.6253]
  },
  {
    id: 'hist-fl-2',
    name: 'Hurricane Katrina Gulf Coast Surge',
    hazard_type: 'floods',
    location: 'Lower Mississippi / New Orleans',
    country: 'United States',
    date: 'August 2005',
    severity: 'EXTREME',
    impactSummary: 'Catastrophic storm surge levee breaches flooding over 80% of New Orleans.',
    keyMetricLabel: 'Peak Surge Height',
    keyMetricValue: '8.5 m (28 ft)',
    verifiedSource: 'US Army Corps of Engineers & NOAA Coastal Inundation',
    coordinates: [29.9511, -90.0715]
  },
  {
    id: 'hist-ls-1',
    name: 'Wayanad Hillslope Debris Flow',
    hazard_type: 'landslides',
    location: 'Meppadi / Chooralmala, Kerala',
    country: 'India',
    date: 'July 2024',
    severity: 'EXTREME',
    impactSummary: 'Excessive 48h cloudburst rainfall triggering massive translational debris slides on steep weathered Precambrian gneiss slopes.',
    keyMetricLabel: 'Antecedent 48h Rainfall',
    keyMetricValue: '572.0 mm',
    verifiedSource: 'Geological Survey of India (GSI) & NASA GLC',
    coordinates: [11.5500, 76.1300]
  },
  {
    id: 'hist-ls-2',
    name: 'Oso Hillside Terrane Collapse',
    hazard_type: 'landslides',
    location: 'Snohomish County, Washington',
    country: 'United States',
    date: 'March 2014',
    severity: 'VERY HIGH',
    impactSummary: 'Deep-seated rotational mudflow damming the North Fork Stillaguamish River following intense saturated antecedent rain.',
    keyMetricLabel: 'Displaced Volume',
    keyMetricValue: '18 Million Tons',
    verifiedSource: 'USGS Landslide Hazards Program Benchmark',
    coordinates: [48.2831, -121.9161]
  },
  {
    id: 'hist-eq-1',
    name: 'Gorkha Mainshock & Aftershock Sequence',
    hazard_type: 'earthquakes',
    location: 'Gorkha / Kathmandu Valley',
    country: 'Nepal',
    date: 'April–May 2015',
    severity: 'EXTREME',
    impactSummary: 'Mw 7.8 mainshock along the Main Himalayan Thrust followed by strong Mw 7.3 Kodari aftershock and hundreds of M4+ tremors.',
    keyMetricLabel: 'Mainshock Magnitude',
    keyMetricValue: 'Mw 7.8 (Focal Depth: 8.2 km)',
    verifiedSource: 'USGS Comprehensive Seismicity Catalog (ANSS)',
    coordinates: [28.2300, 84.7310]
  },
  {
    id: 'hist-eq-2',
    name: 'Kumamoto Doublet Fault Ruptures',
    hazard_type: 'earthquakes',
    location: 'Kyushu',
    country: 'Japan',
    date: 'April 2016',
    severity: 'EXTREME',
    impactSummary: 'Mw 6.2 foreshock followed 28 hours later by Mw 7.0 mainshock along the Futagawa and Hinagu strike-slip fault zones.',
    keyMetricLabel: 'Max Acceleration (PGA)',
    keyMetricValue: '1.38 g',
    verifiedSource: 'JMA & USGS Seismological Research',
    coordinates: [32.7550, 130.7630]
  },
  {
    id: 'hist-cy-1',
    name: 'Super Typhoon Haiyan (Yolanda)',
    hazard_type: 'cyclones',
    location: 'Leyte / Samar Islands',
    country: 'Philippines',
    date: 'November 2013',
    severity: 'EXTREME',
    impactSummary: 'One of the most intense tropical cyclones in recorded human history, making landfall with 1-minute sustained winds of 195 mph.',
    keyMetricLabel: 'Peak 1-min Sustained Wind',
    keyMetricValue: '170 kts (315 km/h)',
    verifiedSource: 'JTWC & JMA IBTrACS Ground-Truth Registry',
    coordinates: [11.2444, 125.0039]
  },
  {
    id: 'hist-cy-2',
    name: 'Super Cyclonic Storm Amphan',
    hazard_type: 'cyclones',
    location: 'Bay of Bengal / West Bengal & Sundarbans',
    country: 'India & Bangladesh',
    date: 'May 2020',
    severity: 'EXTREME',
    impactSummary: 'Category 5 equivalent super cyclone undergoing explosive rapid intensification in warm ocean waters of 31°C.',
    keyMetricLabel: 'Rapid Intensification Rate',
    keyMetricValue: '+60 kts in 24 hours',
    verifiedSource: 'IMD RSMC New Delhi Official Cyclone Archive',
    coordinates: [21.8000, 88.3000]
  },
  {
    id: 'hist-wf-1',
    name: 'Camp Fire Catastrophe',
    hazard_type: 'wildfires',
    location: 'Paradise, Butte County, California',
    country: 'United States',
    date: 'November 2018',
    severity: 'EXTREME',
    impactSummary: 'High-velocity Diablo winds driving extreme ignition susceptibility across drought-desiccated timber fuels.',
    keyMetricLabel: 'Rate of Fire Spread',
    keyMetricValue: '80 Acres / minute',
    verifiedSource: 'CAL FIRE & NASA FIRMS Thermal Telemetry',
    coordinates: [39.7596, -121.6219]
  },
  {
    id: 'hist-wf-2',
    name: 'Black Summer Megafires',
    hazard_type: 'wildfires',
    location: 'New South Wales & Victoria',
    country: 'Australia',
    date: '2019–2020',
    severity: 'EXTREME',
    impactSummary: 'Unprecedented continental pyrocumulonimbus firestorms generated by prolonged record heatwaves and extreme fuel desiccation.',
    keyMetricLabel: 'Total Area Burned',
    keyMetricValue: '24 Million Hectares',
    verifiedSource: 'Australian Bureau of Meteorology & NASA FIRMS VIIRS',
    coordinates: [-35.3075, 149.1244]
  }
];

export const PastEventsPage: React.FC = () => {
  const [selectedHazard, setSelectedHazard] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const hazardColors: Record<string, string> = {
    floods: '#2196F3',
    landslides: '#FF9800',
    earthquakes: '#9C27B0',
    cyclones: '#00BCD4',
    wildfires: '#F44336'
  };

  const filteredEvents = HISTORICAL_BENCHMARKS.filter((ev) => {
    const matchesHazard = selectedHazard === 'all' || ev.hazard_type === selectedHazard;
    const matchesQuery = 
      ev.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ev.location.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ev.country.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesHazard && matchesQuery;
  });

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-16">
      {/* Header */}
      <div className="relative rounded-3xl glass-panel p-8 md:p-10 overflow-hidden border border-slate-200/80 shadow-sm bg-white/80">
        <span className="glass-specular-sheen" />
        <div className="max-w-3xl space-y-3 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold">
            <History className="w-3.5 h-3.5" />
            Verified Scientific Benchmarks
          </div>

          <h1 className="text-3xl md:text-4xl font-black text-slate-900 tracking-tight">
            Past Natural Hazard <span className="text-sky-600">Events</span>
          </h1>

          <p className="text-slate-600 text-sm md:text-base leading-relaxed">
            Explore authentic ground-truth benchmark disasters used to train and validate 
            the HAZARDX AI predictive models against actual historical outcomes.
          </p>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Segmented Filter */}
        <LiquidSegmentedControl
          value={selectedHazard}
          onChange={setSelectedHazard}
          options={[
            { value: 'all', label: 'All Hazards' },
            { value: 'floods', label: 'Floods' },
            { value: 'landslides', label: 'Landslides' },
            { value: 'earthquakes', label: 'Earthquakes' },
            { value: 'cyclones', label: 'Cyclones' },
            { value: 'wildfires', label: 'Wildfires' }
          ]}
        />

        {/* Search */}
        <div className="relative w-full md:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search event or country..."
            className="w-full pl-10 pr-4 py-2 rounded-full bg-white border border-slate-300 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-sky-500 shadow-sm"
          />
        </div>
      </div>

      {/* Events Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filteredEvents.map((ev) => {
          const hColor = hazardColors[ev.hazard_type];
          return (
            <GlassCard 
              key={ev.id}
              glowColor={hColor}
              className="hover:scale-[1.01] transition-transform flex flex-col justify-between bg-white/85 border border-slate-200/80 shadow-sm"
              style={{ borderLeft: `4px solid ${hColor}` }}
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span 
                    className="text-[11px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full"
                    style={{ background: `${hColor}18`, color: hColor }}
                  >
                    {ev.hazard_type}
                  </span>

                  <span className="flex items-center gap-1 text-xs text-slate-500">
                    <Calendar className="w-3.5 h-3.5" />
                    {ev.date}
                  </span>
                </div>

                <div>
                  <h3 className="text-lg font-bold text-slate-900 tracking-tight">{ev.name}</h3>
                  <p className="text-xs text-slate-500 flex items-center gap-1 mt-0.5">
                    <MapPin className="w-3.5 h-3.5 text-sky-600" />
                    {ev.location}, {ev.country}
                  </p>
                </div>

                <p className="text-xs text-slate-600 leading-relaxed">
                  {ev.impactSummary}
                </p>

                <div className="p-3 rounded-2xl bg-slate-50/80 border border-slate-200/70 space-y-1">
                  <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">
                    {ev.keyMetricLabel}
                  </span>
                  <p className="text-sm font-bold text-slate-900 font-mono">
                    {ev.keyMetricValue}
                  </p>
                </div>
              </div>

              <div className="pt-4 border-t border-slate-200/60 mt-4 flex items-center justify-between text-xs">
                <span className="text-slate-500 text-[11px] flex items-center gap-1">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                  {ev.verifiedSource.split('&')[0]}
                </span>

                <Link to={`/map?lat=${ev.coordinates[0]}&lon=${ev.coordinates[1]}&zoom=7`}>
                  <LiquidButton variant="secondary" size="sm">
                    View on Map
                  </LiquidButton>
                </Link>
              </div>
            </GlassCard>
          );
        })}
      </div>
    </div>
  );
};

export default PastEventsPage;
