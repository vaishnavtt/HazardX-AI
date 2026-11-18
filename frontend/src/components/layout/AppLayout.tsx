import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Navbar } from './Navbar';
import { Sidebar } from './Sidebar';

export const AppLayout: React.FC = () => {
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#F4F7FB] text-[#172B4D] flex flex-col font-sans relative overflow-x-hidden selection:bg-cyan-500/20 selection:text-cyan-900">
      {/* Ambient background pastel glows for liquid glass optical depth */}
      <div 
        aria-hidden="true" 
        className="fixed top-[-10%] left-[20%] w-[550px] h-[550px] rounded-full bg-blue-100/40 blur-[130px] pointer-events-none -z-10" 
      />
      <div 
        aria-hidden="true" 
        className="fixed bottom-[10%] right-[10%] w-[500px] h-[500px] rounded-full bg-cyan-100/50 blur-[140px] pointer-events-none -z-10" 
      />
      <div 
        aria-hidden="true" 
        className="fixed top-[40%] left-[5%] w-[400px] h-[400px] rounded-full bg-purple-100/30 blur-[120px] pointer-events-none -z-10" 
      />

      <Navbar 
        onToggleSidebar={() => setMobileSidebarOpen(!mobileSidebarOpen)} 
        isSidebarOpen={mobileSidebarOpen} 
      />

      <div className="flex flex-1 pt-0">
        <Sidebar isOpen={mobileSidebarOpen} onClose={() => setMobileSidebarOpen(false)} />

        <main className="flex-1 lg:pl-64 min-w-0 flex flex-col">
          <div className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto w-full">
            <Outlet />
          </div>

          <footer className="border-t border-slate-200/80 px-6 py-5 text-xs text-slate-500 flex flex-col sm:flex-row justify-between items-center gap-3 bg-white/80 mt-8 shadow-xs">
            <div className="flex items-center gap-2">
              <span className="font-bold text-slate-700">HAZARDX AI</span>
              <span>&bull;</span>
              <span>Global Multi-Hazard Intelligence & Early Warning System</span>
            </div>
            <div className="flex items-center gap-3 text-[11px] text-slate-500 font-medium">
              <span>USGS Seismicity</span>
              <span>&bull;</span>
              <span>NASA FIRMS</span>
              <span>&bull;</span>
              <span>Copernicus GloFAS</span>
              <span>&bull;</span>
              <span>NOAA NHC</span>
              <span>&bull;</span>
              <span>Open-Meteo</span>
            </div>
          </footer>
        </main>
      </div>
    </div>
  );
};

export default AppLayout;
