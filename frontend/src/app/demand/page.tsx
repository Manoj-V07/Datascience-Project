"use client";

import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function DemandPrediction() {
  const searchParams = useSearchParams();
  const eventId = searchParams.get('event') || 'EVT001';
  const time = searchParams.get('time') || '0';
  const sim = searchParams.get('sim') || 'SIM001';

  const [assessments, setAssessments] = useState<any[]>([]);
  const [predictions, setPredictions] = useState<any[]>([]);
  const [selectedZone, setSelectedZone] = useState<string>('');

  useEffect(() => {
    fetch(`http://localhost:8000/api/assessments?event_id=${eventId}&time_window=${time}&sim_id=${sim}`)
      .then(res => res.json())
      .then(data => {
        setAssessments(data);
        if (data.length > 0 && !selectedZone) {
          setSelectedZone(data[0].Response_Zone);
        }
      });

    fetch(`http://localhost:8000/api/predictions?event_id=${eventId}&time_window=${time}&sim_id=${sim}`)
      .then(res => res.json())
      .then(data => setPredictions(data));
  }, [eventId, time, sim]);

  const zoneAssessment = assessments.find(a => a.Response_Zone === selectedZone);
  // Match prediction via Assessment_ID
  const zonePrediction = predictions.find(p => p.Assessment_ID === zoneAssessment?.Assessment_ID);

  const formatNumber = (num: number) => num ? Math.floor(num).toLocaleString() : '0';

  return (
    <div className="animate-fade-in">
      <h1 className="text-4xl font-extrabold mb-4 tracking-tight text-gradient">Phase 3.1: ML Demand Prediction</h1>
      
      <div className="light-card bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-8 text-sm text-yellow-800 relative overflow-hidden">
        <p className="font-bold text-yellow-900 mb-1">Note on AI Explainability</p>
        <p>The trained Random Forest models relied on these assessment variables to produce the predictions below. These are correlative indicators of demand, not strictly causal explanations.</p>
      </div>

      <div className="mb-8">
        <label className="block text-xs font-semibold mb-2 text-slate-500 uppercase tracking-wider">Select Response Zone to Inspect Prediction Context</label>
        <select 
          className="w-1/2 bg-white border border-slate-300 rounded-md p-3 text-slate-800 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all text-sm shadow-sm"
          value={selectedZone}
          onChange={(e) => setSelectedZone(e.target.value)}
        >
          {assessments.map(a => (
            <option key={a.Assessment_ID || a.Response_Zone} value={a.Response_Zone}>{a.Response_Zone} (District: {a.District})</option>
          ))}
        </select>
      </div>

      {zoneAssessment && zonePrediction && (
        <div className="grid grid-cols-2 gap-8">
          <div className="light-card p-8">
            <h3 className="text-xl font-bold mb-6 text-blue-600 border-b border-slate-200 pb-3 flex items-center">
              <span className="w-2 h-2 rounded-full bg-blue-500 mr-3"></span>
              Model Inputs (Context)
            </h3>
            <table className="w-full text-left text-sm">
              <tbody>
                <tr className="table-row-light"><td className="py-3 text-slate-500">Affected Population</td><td className="font-bold text-slate-800 text-right">{formatNumber(zoneAssessment.Population_Affected_Est)}</td></tr>
                <tr className="table-row-light"><td className="py-3 text-slate-500">Severity Score</td><td className="font-bold text-slate-800 text-right">{Number(zoneAssessment.Severity_Score).toFixed(1)}<span className="text-slate-400 font-normal">/100</span></td></tr>
                <tr className="table-row-light"><td className="py-3 text-slate-500">Infrastructure Damage</td><td className="font-bold text-slate-800 text-right">{Number(zoneAssessment.Infrastructure_Damage_Score).toFixed(1)}<span className="text-slate-400 font-normal">/100</span></td></tr>
                <tr className="table-row-light"><td className="py-3 text-slate-500">Medical Urgency</td><td className="font-bold text-slate-800 text-right">{Number(zoneAssessment.Medical_Urgency_Score).toFixed(1)}<span className="text-slate-400 font-normal">/100</span></td></tr>
                <tr className="table-row-light"><td className="py-3 text-slate-500">Accessibility</td><td className="font-bold text-slate-800 text-right">{Number(zoneAssessment.Accessibility_Score).toFixed(1)}<span className="text-slate-400 font-normal">/100</span></td></tr>
                <tr className="border-none hover:bg-slate-50 transition-colors duration-200"><td className="py-3 text-slate-500 rounded-bl-md">Houses Damaged</td><td className="font-bold text-slate-800 text-right rounded-br-md">{formatNumber(zoneAssessment.Houses_Damaged_Est)}</td></tr>
              </tbody>
            </table>
          </div>

          <div className="light-card p-8">
            <h3 className="text-xl font-bold mb-6 text-emerald-600 border-b border-slate-200 pb-3 flex items-center">
              <span className="w-2 h-2 rounded-full bg-emerald-500 mr-3"></span>
              Model Outputs (Predictions)
            </h3>
            <table className="w-full text-left text-sm">
              <tbody>
                <tr className="table-row-light"><td className="py-3 text-slate-500">Food Required</td><td className="font-bold text-emerald-600 text-right text-lg">{formatNumber(zonePrediction.Predicted_Food_Required_packets)} <span className="text-slate-400 font-normal text-sm">packets</span></td></tr>
                <tr className="table-row-light"><td className="py-3 text-slate-500">Water Required</td><td className="font-bold text-blue-600 text-right text-lg">{formatNumber(zonePrediction.Predicted_Water_Required_Liters)} <span className="text-slate-400 font-normal text-sm">L</span></td></tr>
                <tr className="table-row-light"><td className="py-3 text-slate-500">Medical Kits</td><td className="font-bold text-red-600 text-right text-lg">{formatNumber(zonePrediction.Predicted_Medical_Kits_Required)} <span className="text-slate-400 font-normal text-sm">kits</span></td></tr>
                <tr className="border-none hover:bg-slate-50 transition-colors duration-200"><td className="py-3 text-slate-500 rounded-bl-md">Shelter Spaces</td><td className="font-bold text-orange-600 text-right text-lg rounded-br-md">{formatNumber(zonePrediction.Predicted_Shelter_Spaces_Required)} <span className="text-slate-400 font-normal text-sm">spaces</span></td></tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
