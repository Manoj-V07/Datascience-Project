"use client";

import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function ResourceAllocation() {
  const searchParams = useSearchParams();
  const eventId = searchParams.get('event') || 'EVT001';
  const time = searchParams.get('time') || '0';
  const sim = searchParams.get('sim') || 'SIM001';

  const [allocations, setAllocations] = useState<any[]>([]);

  useEffect(() => {
    fetch(`http://localhost:8000/api/allocations?event_id=${eventId}&time_window=${time}&sim_id=${sim}`)
      .then(res => res.json())
      .then(data => setAllocations(data));
  }, [eventId, time, sim]);

  const formatNumber = (num: number) => num ? Math.floor(num).toLocaleString() : '0';

  // Filter out completely 0 allocations for cleaner display
  const displayAllocations = allocations.filter(a => 
    a.Food_Allocated > 0 || a.Water_Allocated > 0 || 
    a.Medical_Allocated > 0 || a.Shelter_Allocated > 0 ||
    a.Food_Unmet > 0 // Keep if there's unmet demand too
  );

  return (
    <div className="animate-fade-in">
      <h1 className="text-4xl font-extrabold mb-4 tracking-tight text-gradient">Phase 4: Resource Allocation Optimization</h1>
      
      <div className="light-card bg-blue-50 border-l-4 border-blue-400 p-4 mb-8 text-sm text-blue-900 relative overflow-hidden flex items-center">
        <span className="w-2 h-2 rounded-full bg-blue-500 mr-3"></span>
        <p>This page displays the output of the Phase 4 Optimization Engine. The engine uses PuLP to maximize priority-weighted fulfillment while adhering to strict temporal inventory limits.</p>
      </div>

      <div className="light-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left text-slate-800">
            <thead className="bg-slate-50 text-slate-500 uppercase text-xs font-bold tracking-wider border-b border-slate-200">
              <tr>
                <th className="px-6 py-4">Zone</th>
                <th className="px-6 py-4">Priority</th>
                <th className="px-6 py-4">Hub ID</th>
                <th className="px-6 py-4 text-right">Food Alloc</th>
                <th className="px-6 py-4 text-right text-red-500">Food Unmet</th>
                <th className="px-6 py-4 text-right">Water Alloc</th>
                <th className="px-6 py-4 text-right text-red-500">Water Unmet</th>
              </tr>
            </thead>
            <tbody>
              {displayAllocations.map((a, i) => (
                <tr key={i} className="table-row-light">
                  <td className="px-6 py-4 font-medium text-slate-900">{a.Response_Zone}</td>
                  <td className="px-6 py-4">
                    <span className={
                      a.Priority_Level === 'Critical' ? 'badge-critical' : 
                      a.Priority_Level === 'High' ? 'badge-high' : 
                      a.Priority_Level === 'Moderate' ? 'badge-moderate' : 'badge-low'
                    }>
                      {a.Priority_Level}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-slate-500">{a.Hub_ID}</td>
                  <td className="px-6 py-4 text-right font-mono text-emerald-600">{formatNumber(a.Food_Allocated)}</td>
                  <td className="px-6 py-4 text-right font-mono text-red-600 font-bold">{formatNumber(a.Food_Unmet)}</td>
                  <td className="px-6 py-4 text-right font-mono text-blue-600">{formatNumber(a.Water_Allocated)}</td>
                  <td className="px-6 py-4 text-right font-mono text-red-600 font-bold">{formatNumber(a.Water_Unmet)}</td>
                </tr>
              ))}
              {displayAllocations.length === 0 && (
                <tr>
                  <td colSpan={7} className="px-6 py-12 text-center text-slate-500 italic">No allocation data for this view.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
