import React, { useState } from 'react';
import { Search, MapPin, ArrowRight } from 'lucide-react';
import { LiquidButton } from '../ui/LiquidButton';

export interface GlassSearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
  initialValue?: string;
  className?: string;
  quickLocations?: Array<{ name: string; query: string }>;
}

export const GlassSearchBar: React.FC<GlassSearchBarProps> = ({
  onSearch,
  placeholder = "Search any city, region or coordinates (e.g. San Francisco or 37.77, -122.41)...",
  initialValue = "",
  className = "",
  quickLocations = [
    { name: "Tokyo", query: "35.6762, 139.6503" },
    { name: "San Francisco", query: "37.7749, -122.4194" },
    { name: "New Orleans", query: "29.9511, -90.0715" },
    { name: "Uttarakhand", query: "30.3165, 78.0322" },
    { name: "Manila", query: "14.5995, 120.9842" },
  ],
}) => {
  const [query, setQuery] = useState(initialValue);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  return (
    <div className={`w-full max-w-3xl mx-auto flex flex-col gap-3 ${className}`}>
      <form onSubmit={handleSubmit} className="relative flex items-center">
        <div className="absolute left-4.5 text-slate-400 pointer-events-none flex items-center">
          <Search className="w-5 h-5 text-cyan-400" />
        </div>

        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          className="w-full pl-12 pr-32 py-4 rounded-full bg-slate-900/70 border border-white/16 backdrop-blur-2xl text-white placeholder-slate-400 text-sm md:text-base shadow-2xl focus:outline-none focus:border-cyan-400/60 focus:ring-2 focus:ring-cyan-400/20 transition-all duration-300"
          style={{
            boxShadow: '0 12px 36px -4px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.15)'
          }}
        />

        <div className="absolute right-2">
          <LiquidButton
            type="submit"
            variant="primary"
            size="sm"
            rightIcon={<ArrowRight className="w-4 h-4" />}
            glow
          >
            Check Risks
          </LiquidButton>
        </div>
      </form>

      {quickLocations && quickLocations.length > 0 && (
        <div className="flex items-center gap-2 flex-wrap text-xs text-slate-400 px-3">
          <span className="flex items-center gap-1 font-medium text-slate-300">
            <MapPin className="w-3.5 h-3.5 text-cyan-400" /> Popular:
          </span>
          {quickLocations.map((loc) => (
            <button
              key={loc.name}
              type="button"
              onClick={() => {
                setQuery(loc.query);
                onSearch(loc.query);
              }}
              className="px-2.5 py-1 rounded-full bg-white/5 border border-white/10 hover:border-cyan-400/40 hover:text-cyan-300 transition-colors"
            >
              {loc.name}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default GlassSearchBar;
