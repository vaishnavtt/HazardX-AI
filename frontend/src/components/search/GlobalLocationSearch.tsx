import React, { useState, useEffect, useRef } from 'react';
import { Search, MapPin, Loader2, Navigation, Clock, X, ChevronRight, Compass } from 'lucide-react';
import { api } from '../../api/client';
import type { LocationSearchResult } from '../../types/hazard';

interface GlobalLocationSearchProps {
  placeholder?: string;
  onSelectLocation: (loc: LocationSearchResult) => void;
  className?: string;
  autoFocus?: boolean;
}

const RECENT_SEARCHES_KEY = 'hazardx_recent_searches';

export const GlobalLocationSearch: React.FC<GlobalLocationSearchProps> = ({
  placeholder = 'Search any city, town, or GPS coordinates (e.g., Wayanad, Kochi, London, 29.95, -90.07)...',
  onSelectLocation,
  className = '',
  autoFocus = false,
}) => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<LocationSearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState<number>(-1);
  const [recentSearches, setRecentSearches] = useState<LocationSearchResult[]>(() => {
    try {
      const saved = localStorage.getItem(RECENT_SEARCHES_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const wrapperRef = useRef<HTMLDivElement>(null);
  const debounceTimerRef = useRef<number | null>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Fetch geocoding suggestions with 250ms debounce
  useEffect(() => {
    if (!query.trim()) {
      setSuggestions([]);
      setIsLoading(false);
      return;
    }

    if (debounceTimerRef.current) {
      window.clearTimeout(debounceTimerRef.current);
    }

    debounceTimerRef.current = window.setTimeout(async () => {
      setIsLoading(true);
      try {
        const data = await api.geocodeLocation(query.trim(), 8);
        setSuggestions(data.results || []);
        setIsOpen(true);
        setSelectedIndex(-1);
      } catch (err) {
        console.error('Geocode search failed:', err);
        setSuggestions([]);
      } finally {
        setIsLoading(false);
      }
    }, 250);

    return () => {
      if (debounceTimerRef.current) {
        window.clearTimeout(debounceTimerRef.current);
      }
    };
  }, [query]);

  const handleSelect = (loc: LocationSearchResult) => {
    setQuery(loc.display_name || loc.name);
    setIsOpen(false);
    setSelectedIndex(-1);

    // Save to recents
    const updated = [loc, ...recentSearches.filter((s) => s.id !== loc.id)].slice(0, 5);
    setRecentSearches(updated);
    try {
      localStorage.setItem(RECENT_SEARCHES_KEY, JSON.stringify(updated));
    } catch {
      // storage unavailable
    }

    onSelectLocation(loc);
  };

  const handleClear = () => {
    setQuery('');
    setSuggestions([]);
    setIsOpen(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    const list = suggestions.length > 0 ? suggestions : (!query && recentSearches.length > 0 ? recentSearches : []);

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setIsOpen(true);
      setSelectedIndex((prev) => (prev < list.length - 1 ? prev + 1 : 0));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev > 0 ? prev - 1 : list.length - 1));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0 && selectedIndex < list.length) {
        handleSelect(list[selectedIndex]);
      } else if (list.length > 0) {
        handleSelect(list[0]);
      }
    } else if (e.key === 'Escape') {
      setIsOpen(false);
    }
  };

  return (
    <div ref={wrapperRef} className={`relative w-full ${className}`}>
      {/* Search Input Bar */}
      <div className="relative flex items-center">
        <div className="absolute left-4 pointer-events-none text-slate-400">
          <Search className="w-5 h-5 text-cyan-600" />
        </div>

        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          onKeyDown={handleKeyDown}
          autoFocus={autoFocus}
          placeholder={placeholder}
          className="w-full pl-12 pr-12 py-3.5 bg-white border border-slate-200 rounded-2xl shadow-sm text-slate-900 placeholder:text-slate-400 text-sm md:text-base font-medium focus:outline-none focus:ring-2 focus:ring-cyan-500/30 focus:border-cyan-500 transition-all duration-200"
        />

        <div className="absolute right-4 flex items-center gap-1.5">
          {isLoading && <Loader2 className="w-4 h-4 text-cyan-600 animate-spin" />}
          {query && !isLoading && (
            <button
              type="button"
              onClick={handleClear}
              className="p-1 text-slate-400 hover:text-slate-600 rounded-full hover:bg-slate-100 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Autocomplete Dropdown Popup */}
      {isOpen && (
        <div className="absolute left-0 right-0 top-full mt-2 z-50 bg-white/95 backdrop-blur-xl border border-slate-200 rounded-2xl shadow-xl overflow-hidden max-h-80 overflow-y-auto animate-in fade-in-50 zoom-in-95 duration-150">
          {/* 1. Live Geocoding Results */}
          {suggestions.length > 0 && (
            <div className="p-2 space-y-1">
              <div className="px-3 py-1 text-[11px] font-bold text-slate-600 uppercase tracking-wider flex items-center gap-1.5">
                <Compass className="w-3.5 h-3.5 text-cyan-700" />
                Matching Places Worldwide
              </div>
              {suggestions.map((loc, idx) => (
                <button
                  key={loc.id || `${loc.latitude}_${loc.longitude}_${idx}`}
                  type="button"
                  onClick={() => handleSelect(loc)}
                  onMouseEnter={() => setSelectedIndex(idx)}
                  className={`w-full text-left px-3.5 py-2.5 rounded-xl flex items-center justify-between text-sm transition-all duration-150 ${
                    selectedIndex === idx
                      ? 'bg-cyan-50 text-cyan-900 border border-cyan-200/80 shadow-xs'
                      : 'text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <div className="w-8 h-8 rounded-lg bg-cyan-100 text-cyan-700 flex items-center justify-center shrink-0">
                      <MapPin className="w-4 h-4" />
                    </div>
                    <div className="truncate">
                      <div className="font-semibold text-slate-900 truncate">
                        {loc.name}
                      </div>
                      <div className="text-xs text-slate-600 truncate">
                        {loc.state ? `${loc.state}, ` : ''}{loc.country}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0 text-xs text-slate-600 font-mono pl-2">
                    <span>{loc.latitude.toFixed(2)}°, {loc.longitude.toFixed(2)}°</span>
                    <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
                  </div>
                </button>
              ))}
            </div>
          )}

          {/* 2. No Results Message */}
          {!isLoading && query.trim() && suggestions.length === 0 && (
            <div className="p-6 text-center text-slate-500">
              <MapPin className="w-8 h-8 text-slate-300 mx-auto mb-2" />
              <p className="text-sm font-semibold text-slate-700">No locations found for &ldquo;{query}&rdquo;</p>
              <p className="text-xs text-slate-400 mt-1">
                Try searching by city name (e.g. Wayanad, Kochi, London) or enter latitude and longitude coordinates.
              </p>
            </div>
          )}

          {/* 3. Recent Searches (when query is empty) */}
          {!query && recentSearches.length > 0 && (
            <div className="p-2 space-y-1 border-t border-slate-100 first:border-0">
              <div className="px-3 py-1 text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5 text-slate-400" />
                Recent Searches
              </div>
              {recentSearches.map((loc, idx) => (
                <button
                  key={`recent_${loc.id || idx}`}
                  type="button"
                  onClick={() => handleSelect(loc)}
                  onMouseEnter={() => setSelectedIndex(idx)}
                  className={`w-full text-left px-3.5 py-2.5 rounded-xl flex items-center justify-between text-sm transition-all duration-150 ${
                    selectedIndex === idx ? 'bg-cyan-50 text-cyan-900' : 'text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-center gap-3 truncate">
                    <Clock className="w-4 h-4 text-slate-400 shrink-0" />
                    <span className="font-medium truncate">{loc.display_name || loc.name}</span>
                  </div>
                  <span className="text-xs font-mono text-slate-400 shrink-0">
                    {loc.latitude.toFixed(2)}°, {loc.longitude.toFixed(2)}°
                  </span>
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default GlobalLocationSearch;
