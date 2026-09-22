"use client";

import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer } from 'recharts';

export default function ResourceStatus() {
  const searchParams = useSearchParams();
  const eventId = searchParams.get('event') || 'EVT001';
  const time = searchParams.get('time') || '0';
  const sim = searchParams.get('sim') || 'SIM001';

  const [predictions, setPredictions] = useState<any[]>([]);
  const [inventory, setInventory] = useState<any[]>([]);

  useEffect(() => {
    fetch(`http://localhost:8000/api/predictions?event_id=${eventId}&time_window=${time}&sim_id=${sim}`)
      .then(res => res.json())
      .then(data => setPredictions(data));

    fetch(`http://localhost:8000/api/inventory?event_id=${eventId}&time_window=${time}`)
      .then(res => res.json())
      .then(data => setInventory(data));
  }, [eventId, time, sim]);

  const resources = [
    { key: 'Food', unit: 'packets', demKey: 'Predicted_Food_Required_packets', invKey: 'Food_Opening_Inventory' },
    { key: 'Water', unit: 'Liters', demKey: 'Predicted_Water_Required_Liters', invKey: 'Water_Opening_Inventory' },
    { key: 'Medical', unit: 'Kits', demKey: 'Predicted_Medical_Kits_Required', invKey: 'Medical_Opening_Inventory' },
    { key: 'Shelter', unit: 'Spaces', demKey: 'Predicted_Shelter_Spaces_Required', invKey: 'Shelter_Opening_Capacity' }
  ];

  const shortageAlerts: any[] = [];
  const chartData: any[] = [];

  resources.forEach(r => {
    const dem = predictions.reduce((sum, p) => sum + (p[r.demKey] || 0), 0);
    const sup = inventory.reduce((sum, i) => sum + (i[r.invKey] || 0), 0);
    
    if (dem > sup) {
      shortageAlerts.push({ resource: r.key, demand: dem, supply: sup, unit: r.unit });
    }

    chartData.push({
      name: r.key,
      Demand: dem,
      Available_Supply: sup
    });
  });

  const formatNumber = (num: number) => Math.floor(num).toLocaleString();

  return (
    <div className="animate-fade-in">
      <h1 className="text-4xl font-extrabold mb-8 tracking-tight text-gradient">Resource Inventory & Shortage Status</h1>

      <div className="mb-8">
        <h2 className="text-xl font-bold mb-4 text-slate-800">Operational Alerts</h2>
        {shortageAlerts.length === 0 ? (
          <div className="light-card bg-emerald-50 border-emerald-200 p-4 text-emerald-800 font-medium relative overflow-hidden flex items-center">
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-emerald-500"></div>
            <span className="w-2 h-2 rounded-full bg-emerald-500 mr-3"></span>
            Adequate supply for all resources at current time window.
          </div>
        ) : (
          <div className="space-y-3">
            {shortageAlerts.map(alert => (
              <div key={alert.resource} className="light-card bg-red-50 border-red-200 p-4 text-red-800 relative overflow-hidden flex items-center">
                <div className="absolute left-0 top-0 bottom-0 w-1 bg-red-500"></div>
                <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse mr-3"></span>
                <strong className="text-red-700 tracking-wider mr-2">CRITICAL SHORTAGE:</strong> {alert.resource} demand ({formatNumber(alert.demand)} {alert.unit}) exceeds available T+0h supply ({formatNumber(alert.supply)} {alert.unit})!
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="light-card p-6 h-[500px]">
        <h3 className="text-lg font-bold mb-6 text-slate-800">Total Demand vs Available Supply (T+{time}h)</h3>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" vertical={false} />
            <XAxis 
              dataKey="name" 
              tick={{ fill: '#64748b', fontSize: 12 }}
              tickLine={{ stroke: 'rgba(0,0,0,0.1)' }}
              axisLine={{ stroke: 'rgba(0,0,0,0.1)' }}
            />
            <YAxis 
              tickFormatter={(val) => (val >= 1000000 ? (val/1000000).toFixed(1)+'M' : val)} 
              tick={{ fill: '#64748b', fontSize: 12 }}
              tickLine={{ stroke: 'rgba(0,0,0,0.1)' }}
              axisLine={{ stroke: 'rgba(0,0,0,0.1)' }}
            />
            <RechartsTooltip 
              formatter={(val: any) => formatNumber(Number(val))} 
              cursor={{ fill: 'rgba(0,0,0,0.05)' }}
              contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.95)', borderColor: 'rgba(0,0,0,0.1)', borderRadius: '8px', color: '#0f172a', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
              itemStyle={{ color: '#0f172a', fontWeight: 'bold' }}
            />
            <Legend wrapperStyle={{ paddingTop: '20px' }} />
            <Bar dataKey="Available_Supply" fill="#10b981" name="Available Supply" radius={[4, 4, 0, 0]} />
            <Bar dataKey="Demand" fill="#ef4444" name="Predicted Demand" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
