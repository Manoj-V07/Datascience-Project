"use client";

import { useState } from 'react';

export default function Simulator() {
  const [formData, setFormData] = useState({
    Disaster_Type: 'Earthquake',
    District: 'District_A',
    Hours_Since_Disaster: 24,
    Population_Baseline: 50000,
    Population_Affected_Est: 10000,
    Affected_Population_pct: 20.0,
    Fatalities_Est: 50,
    Injured_Est: 300,
    Rescue_Cases_Est: 150,
    Houses_Damaged_Est: 1200,
    Severity_Score: 75.5,
    Infrastructure_Damage_Score: 80.0,
    Accessibility_Score: 40.0,
    Medical_Urgency_Score: 85.0,
    Distance_to_Hub_km: 25.5,
    Estimated_Travel_Time_min: 60.0,
    Temperature_C: 30.0,
    Rainfall_mm: 0.0,
    Wind_Speed_kmph: 15.0
  });

  const [predictions, setPredictions] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: ['Disaster_Type', 'District'].includes(name) ? value : Number(value)
    }));
  };

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setPredictions(null);

    try {
      const res = await fetch('http://localhost:8000/api/predict_custom', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (!res.ok) throw new Error('Prediction failed.');
      const data = await res.json();
      setPredictions(data.predictions);
    } catch (err: any) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num: number) => Math.floor(num).toLocaleString();

  return (
    <div className="animate-fade-in max-w-6xl mx-auto">
      <h1 className="text-4xl font-extrabold mb-2 tracking-tight text-gradient">Live Demand Simulator</h1>
      <p className="text-slate-500 mb-8">Enter real-time disaster metrics to instantly predict resource requirements using Phase 3.1 Random Forest models.</p>

      <div className="grid grid-cols-3 gap-8">
        <div className="col-span-2">
          <form onSubmit={handlePredict} className="light-card p-8">
            <h3 className="text-xl font-bold mb-6 text-slate-800 border-b border-slate-200 pb-3">Simulation Parameters</h3>
            
            <div className="grid grid-cols-2 gap-x-6 gap-y-4 mb-6">
              {/* Categorical Inputs */}
              <div>
                <label className="block text-xs font-semibold mb-1 text-slate-500 uppercase">Disaster Type</label>
                <select name="Disaster_Type" value={formData.Disaster_Type} onChange={handleChange} className="w-full bg-white border border-slate-300 rounded p-2 text-sm text-slate-800">
                  <option value="Earthquake">Earthquake</option>
                  <option value="Flood">Flood</option>
                  <option value="Cyclone">Cyclone</option>
                  <option value="Tsunami">Tsunami</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold mb-1 text-slate-500 uppercase">District</label>
                <select name="District" value={formData.District} onChange={handleChange} className="w-full bg-white border border-slate-300 rounded p-2 text-sm text-slate-800">
                  <option value="District_A">District A</option>
                  <option value="District_B">District B</option>
                  <option value="District_C">District C</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-x-6 gap-y-4">
              {/* Numerical Inputs */}
              {Object.keys(formData).filter(k => !['Disaster_Type', 'District'].includes(k)).map(key => (
                <div key={key}>
                  <label className="block text-[10px] font-semibold mb-1 text-slate-500 uppercase truncate" title={key}>
                    {key.replace(/_/g, ' ')}
                  </label>
                  <input
                    type="number"
                    step="any"
                    name={key}
                    value={(formData as any)[key]}
                    onChange={handleChange}
                    className="w-full bg-slate-50 border border-slate-200 rounded p-2 text-sm text-slate-800 focus:border-blue-500 outline-none transition-colors"
                  />
                </div>
              ))}
            </div>

            <div className="mt-8 flex justify-end">
              <button 
                type="submit" 
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-md shadow-md transition-colors disabled:opacity-50"
              >
                {loading ? 'Predicting...' : 'Run Simulation'}
              </button>
            </div>
            {error && <p className="text-red-500 mt-4 text-sm">{error}</p>}
          </form>
        </div>

        <div className="col-span-1">
          <div className="light-card p-6 sticky top-8">
            <h3 className="text-lg font-bold mb-6 text-slate-800 border-b border-slate-200 pb-3 flex items-center">
              <span className="w-2 h-2 rounded-full bg-emerald-500 mr-3"></span>
              Predicted Demand
            </h3>
            
            {!predictions && !loading && (
              <div className="text-center py-12 text-slate-400 text-sm italic">
                Run a simulation to view predicted requirements.
              </div>
            )}

            {loading && (
              <div className="text-center py-12 text-blue-500 font-medium animate-pulse">
                Analyzing parameters...
              </div>
            )}

            {predictions && (
              <div className="space-y-6">
                <div>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Food Required</p>
                  <p className="text-3xl font-bold text-emerald-600">{formatNumber(predictions.Food_Required_packets)} <span className="text-sm font-medium text-slate-400">pkts</span></p>
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Water Required</p>
                  <p className="text-3xl font-bold text-blue-600">{formatNumber(predictions.Water_Required_Liters)} <span className="text-sm font-medium text-slate-400">L</span></p>
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Medical Kits</p>
                  <p className="text-3xl font-bold text-red-600">{formatNumber(predictions.Medical_Kits_Required)} <span className="text-sm font-medium text-slate-400">kits</span></p>
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Shelter Spaces</p>
                  <p className="text-3xl font-bold text-orange-600">{formatNumber(predictions.Shelter_Spaces_Required)} <span className="text-sm font-medium text-slate-400">spaces</span></p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
