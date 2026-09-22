"use client";

import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid } from 'recharts';

export default function Impact() {
  const searchParams = useSearchParams();
  const eventId = searchParams.get('event') || 'EVT001';
  const time = searchParams.get('time') || '0';
  const sim = searchParams.get('sim') || 'SIM001';

  const [assessments, setAssessments] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:8000/api/assessments?event_id=${eventId}&time_window=${time}&sim_id=${sim}`)
      .then(res => res.json())
      .then(data => setAssessments(data));
  }, [eventId, time, sim]);

  const totalBaseline = assessments.reduce((sum, a: any) => sum + (a.Population_Baseline || 0), 0);
  const totalAffected = assessments.reduce((sum, a: any) => sum + (a.Population_Affected_Est || 0), 0);
  const pctAffected = totalBaseline > 0 ? ((totalAffected / totalBaseline) * 100).toFixed(1) : "0.0";

  const totalInjured = assessments.reduce((sum, a: any) => sum + (a.Injured_Population_Est || 0), 0);
  const totalFatalities = assessments.reduce((sum, a: any) => sum + (a.Fatalities_Est || 0), 0);
  const totalHouses = assessments.reduce((sum, a: any) => sum + (a.Houses_Damaged_Est || 0), 0);

  // Prepare Priority data for Pie chart
  const priorityCounts = assessments.reduce((acc: any, curr: any) => {
    acc[curr.Priority_Level] = (acc[curr.Priority_Level] || 0) + 1;
    return acc;
  }, {});

  const priorityData = Object.keys(priorityCounts).map(k => ({ name: k, value: priorityCounts[k] }));
  const COLORS: Record<string, string> = { Critical: '#d32f2f', High: '#f57c00', Moderate: '#fbc02d', Low: '#388e3c' };

  const formatNumber = (num: number) => Math.floor(num).toLocaleString();

  return (
    <div className="animate-fade-in">
      <h1 className="text-4xl font-extrabold mb-8 tracking-tight text-gradient">Disaster Impact Analysis</h1>

      <div className="grid grid-cols-3 gap-6 mb-8">
        <div className="light-card p-6 flex flex-col justify-center">
          <h3 className="text-xs font-bold text-slate-500 mb-2 uppercase tracking-widest">Total Population</h3>
          <p className="text-3xl font-bold text-slate-800">{formatNumber(totalBaseline)}</p>
        </div>
        <div className="light-card p-6 flex flex-col justify-center">
          <h3 className="text-xs font-bold text-slate-500 mb-2 uppercase tracking-widest">Affected Population</h3>
          <p className="text-3xl font-bold text-orange-600">{formatNumber(totalAffected)}</p>
        </div>
        <div className="light-card p-6 flex flex-col justify-center">
          <h3 className="text-xs font-bold text-slate-500 mb-2 uppercase tracking-widest">Affected %</h3>
          <p className="text-3xl font-bold text-slate-800">{pctAffected}%</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-8 mb-8">
        <div className="light-card p-6 h-96 relative flex flex-col">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-32 h-32 bg-blue-100 blur-3xl rounded-full pointer-events-none"></div>
          <h3 className="text-lg font-bold mb-4 text-slate-800 shrink-0">Zones by Priority Level</h3>
          <div className="flex-1 w-full min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={priorityData} cx="50%" cy="50%" innerRadius={60} outerRadius={100} dataKey="value" stroke="none">
                  {priorityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[entry.name] || '#ccc'} />
                  ))}
                </Pie>
                <RechartsTooltip
                  contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.95)', borderColor: 'rgba(0,0,0,0.1)', borderRadius: '8px', color: '#0f172a', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
                  itemStyle={{ color: '#0f172a', fontWeight: 'bold' }}
                />
                <Legend verticalAlign="bottom" height={36} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="light-card p-6 flex flex-col justify-center relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-red-100 blur-3xl rounded-full pointer-events-none"></div>
          <h3 className="text-lg font-bold mb-8 text-slate-800 relative z-10">Human Impact Summary</h3>
          <div className="space-y-6 relative z-10">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <p className="text-sm text-slate-500 uppercase tracking-widest font-semibold">Injured Population</p>
              <p className="text-2xl font-bold text-orange-600">{formatNumber(totalInjured)}</p>
            </div>
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <p className="text-sm text-slate-500 uppercase tracking-widest font-semibold">Fatalities</p>
              <p className="text-2xl font-bold text-red-600">{formatNumber(totalFatalities)}</p>
            </div>
            <div className="flex items-center justify-between pb-2">
              <p className="text-sm text-slate-500 uppercase tracking-widest font-semibold">Houses Damaged</p>
              <p className="text-2xl font-bold text-slate-700">{formatNumber(totalHouses)}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
