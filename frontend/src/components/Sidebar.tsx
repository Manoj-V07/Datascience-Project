"use client";

import { usePathname, useSearchParams, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function Sidebar() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const pathname = usePathname();

  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(searchParams.get('event') || 'EVT001');
  const [selectedTime, setSelectedTime] = useState(searchParams.get('time') || '0');
  const [selectedSim, setSelectedSim] = useState(searchParams.get('sim') || 'SIM001');

  useEffect(() => {
    fetch('http://localhost:8000/api/events')
      .then(res => res.json())
      .then(data => setEvents(data));
  }, []);

  const updateFilters = (event: string, time: string, sim: string) => {
    setSelectedEvent(event);
    setSelectedTime(time);
    setSelectedSim(sim);
    const params = new URLSearchParams(searchParams.toString());
    params.set('event', event);
    params.set('time', time);
    params.set('sim', sim);
    router.push(pathname + '?' + params.toString());
  };

  const navLinks = [
    { name: 'Overview', href: '/' },
    { name: 'Disaster Impact', href: '/impact' },
    { name: 'Demand Prediction', href: '/demand' },
    { name: 'Resource Status', href: '/status' },
    { name: 'Resource Allocation', href: '/allocation' },
    { name: 'Live Simulator', href: '/simulator' }
  ];

  return (
    <div className="w-64 light-panel bg-white text-slate-800 h-screen fixed top-0 left-0 flex flex-col z-50">
      <div className="p-6 relative border-b border-slate-100">
        <h1 className="text-xl font-bold mb-1 text-gradient">Disaster Allocation</h1>
        <p className="text-xs text-slate-500 italic font-mono tracking-tight">Right Resource. Right Place. Right Time.</p>
      </div>

      <div className="px-6 py-4 border-b border-slate-100">
        <label className="block text-xs font-semibold mb-2 text-slate-500 uppercase tracking-wider">Select Event</label>
        <select 
          className="w-full bg-slate-50 border border-slate-200 rounded-md p-2 text-slate-800 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all text-sm"
          value={selectedEvent}
          onChange={(e) => updateFilters(e.target.value, selectedTime, selectedSim)}
        >
          {events.map((e: any) => (
            <option key={e.Event_ID} value={e.Event_ID}>{e.Event_ID} - {e.Event_Name}</option>
          ))}
        </select>
      </div>

      <div className="px-6 py-4 border-b border-slate-100">
        <label className="block text-xs font-semibold mb-2 text-slate-500 uppercase tracking-wider">Assessment Time</label>
        <select 
          className="w-full bg-slate-50 border border-slate-200 rounded-md p-2 text-slate-800 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all text-sm"
          value={selectedTime}
          onChange={(e) => updateFilters(selectedEvent, e.target.value, selectedSim)}
        >
          {[0, 3, 6, 12, 24, 36, 48, 72].map(t => (
            <option key={t} value={t}>T+{t}h</option>
          ))}
        </select>
      </div>

      <div className="px-6 py-4 border-b border-slate-100 mb-2">
        <label className="block text-xs font-semibold mb-2 text-slate-500 uppercase tracking-wider">Simulation Type</label>
        <select 
          className="w-full bg-slate-50 border border-slate-200 rounded-md p-2 text-slate-800 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all text-sm"
          value={selectedSim}
          onChange={(e) => updateFilters(selectedEvent, selectedTime, e.target.value)}
        >
          <option value="SIM001">SIM001 (Baseline)</option>
          <option value="SIM002">SIM002 (Scenario B)</option>
          <option value="SIM003">SIM003 (Scenario C)</option>
          <option value="SIM004">SIM004 (Scenario D)</option>
          <option value="SIM005">SIM005 (Scenario E)</option>
        </select>
      </div>

      <div className="flex-1 overflow-y-auto py-2">
        {navLinks.map(link => {
          const isActive = pathname === link.href;
          return (
            <button
              key={link.name}
              onClick={() => {
                const params = new URLSearchParams(searchParams.toString());
                params.set('event', selectedEvent);
                params.set('time', selectedTime);
                params.set('sim', selectedSim);
                router.push(link.href + '?' + params.toString());
              }}
              className={`w-full text-left px-6 py-3 transition-all duration-300 relative group flex items-center ${isActive ? 'text-blue-700 bg-blue-50/50' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'}`}
            >
              {isActive && (
                <div className="absolute left-0 top-0 bottom-0 w-[4px] bg-blue-600"></div>
              )}
              <span className="relative z-10 text-sm font-medium">{link.name}</span>
            </button>
          )
        })}
      </div>
    </div>
  );
}
