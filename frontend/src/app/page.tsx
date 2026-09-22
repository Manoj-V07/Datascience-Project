"use client";

import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

export default function Overview() {
  const searchParams = useSearchParams();
  const eventId = searchParams.get('event') || 'EVT001';
  const time = searchParams.get('time') || '0';
  const sim = searchParams.get('sim') || 'SIM001';

  const [assessments, setAssessments] = useState<any[]>([]);
  const [predictions, setPredictions] = useState<any[]>([]);

  useEffect(() => {
    fetch(`http://localhost:8000/api/assessments?event_id=${eventId}&time_window=${time}&sim_id=${sim}`)
      .then(res => res.json())
      .then(data => setAssessments(data));

    fetch(`http://localhost:8000/api/predictions?event_id=${eventId}&time_window=${time}&sim_id=${sim}`)
      .then(res => res.json())
      .then(data => setPredictions(data));
  }, [eventId, time, sim]);

  const totalAffected = assessments.reduce((sum, a: any) => sum + (a.Population_Affected_Est || 0), 0);
  const criticalZones = assessments.filter((a: any) => a.Priority_Level === 'Critical').length;
  
  const foodDemand = predictions.reduce((sum, p: any) => sum + (p.Predicted_Food_Required_packets || 0), 0);
  const waterDemand = predictions.reduce((sum, p: any) => sum + (p.Predicted_Water_Required_Liters || 0), 0);

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'k';
    return Math.floor(num).toLocaleString();
  };

  return (
    <div className="animate-fade-in">
      <h1 className="text-4xl font-extrabold mb-2 tracking-tight text-gradient">Disaster Overview</h1>
      <h2 className="text-lg mb-8 text-slate-500 font-medium">Event: <span className="text-slate-800">{eventId}</span> at <span className="text-slate-800">T+{time}h</span></h2>

      <div className="grid grid-cols-4 gap-6 mb-8">
        <div className="light-card p-6 flex flex-col justify-center">
          <h3 className="text-xs font-bold text-slate-500 mb-2 uppercase tracking-widest">Total Affected</h3>
          <p className="text-3xl font-bold text-slate-800">{formatNumber(totalAffected)}</p>
        </div>
        <div className="light-card p-6 flex flex-col justify-center relative overflow-hidden">
          <div className="absolute top-0 right-0 w-16 h-16 bg-red-100 blur-2xl rounded-full pointer-events-none"></div>
          <h3 className="text-xs font-bold text-slate-500 mb-2 uppercase tracking-widest">Critical Zones</h3>
          <p className="text-3xl font-bold text-red-600">{criticalZones}</p>
        </div>
        <div className="light-card p-6 flex flex-col justify-center">
          <h3 className="text-xs font-bold text-slate-500 mb-2 uppercase tracking-widest">Food Demand</h3>
          <p className="text-3xl font-bold text-slate-800">{formatNumber(foodDemand)} <span className="text-sm font-medium text-slate-400">pkts</span></p>
        </div>
        <div className="light-card p-6 flex flex-col justify-center">
          <h3 className="text-xs font-bold text-slate-500 mb-2 uppercase tracking-widest">Water Demand</h3>
          <p className="text-3xl font-bold text-slate-800">{formatNumber(waterDemand)} <span className="text-sm font-medium text-slate-400">L</span></p>
        </div>
      </div>

      <div className="light-card p-6 h-[450px]">
        <h3 className="text-lg font-bold mb-6 text-slate-800">Affected Population by Zone</h3>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={assessments.slice(0, 20)}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" vertical={false} />
            <XAxis 
              dataKey="Assessment_ID" 
              tick={{ fill: '#64748b', fontSize: 12 }}
              tickLine={{ stroke: 'rgba(0,0,0,0.1)' }}
              axisLine={{ stroke: 'rgba(0,0,0,0.1)' }}
              tickFormatter={(val) => {
                const item = assessments.find((a: any) => a.Assessment_ID === val);
                return item ? item.Response_Zone : val;
              }} 
            />
            <YAxis 
              tick={{ fill: '#64748b', fontSize: 12 }}
              tickLine={{ stroke: 'rgba(0,0,0,0.1)' }}
              axisLine={{ stroke: 'rgba(0,0,0,0.1)' }}
            />
            <Tooltip 
              cursor={{ fill: 'rgba(0,0,0,0.05)' }}
              contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.95)', borderColor: 'rgba(0,0,0,0.1)', borderRadius: '8px', color: '#0f172a', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)' }}
              itemStyle={{ color: '#0f172a', fontWeight: 'bold' }}
            />
            <Legend wrapperStyle={{ paddingTop: '20px' }} />
            <Bar dataKey="Population_Affected_Est" name="Affected Population" radius={[4, 4, 0, 0]}>
              {
                assessments.slice(0, 20).map((entry, index) => (
                  <Cell key={`cell-${index}`} fill="url(#colorUv)" />
                ))
              }
            </Bar>
            <defs>
              <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0.8}/>
              </linearGradient>
            </defs>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
