import React from 'react';
import {ResponsiveContainer, AreaChart, Area, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, Legend} from 'recharts';
export function GlucoseChart({observations=[],forecast,threshold=180,scenario}){
 const past=observations.slice(-288).map(o=>({t:new Date(o.timestamp).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'}),actual:Number(o.glucose_mg_dl),forecast:null,scenario:null}));
 const last=past.length?past[past.length-1]:{t:'Now',actual:100};
 const base=forecast?.prediction_points||[];
 const next=base.map((p,i)=>({t:`+${p.minutes_ahead}m`,actual:null,forecast:p.glucose_mg_dl,scenario:scenario?.comparison?.[i]?.scenario_mg_dl??null}));
 // Join actual and forecast series with a visual bridge at the current reading.
 const data=[...past,{t:'Now',actual:last.actual??null,forecast:last.actual??null,scenario:last.actual??null},...next];
 return <div className="chart"><ResponsiveContainer width="100%" height="100%"><LineChart data={data} margin={{top:12,right:8,left:0,bottom:0}}><CartesianGrid strokeDasharray="3 3" stroke="#243043"/><XAxis dataKey="t" minTickGap={20} tick={{fill:'#90a0b7',fontSize:11}} axisLine={{stroke:'#344155'}} tickLine={false}/><YAxis domain={['auto','auto']} width={42} tick={{fill:'#90a0b7',fontSize:11}} axisLine={false} tickLine={false}/><Tooltip contentStyle={{background:'#0f1726',border:'1px solid #2c3a50',borderRadius:12,color:'#f4f7fb'}}/><ReferenceLine y={threshold} stroke="#f59e0b" strokeDasharray="5 5" label={{value:`Threshold ${threshold}`,fill:'#fbbf24',fontSize:11,position:'insideTopRight'}}/><Line type="monotone" dataKey="actual" name="Observed (synthetic)" stroke="#61d9c4" strokeWidth={2} dot={false} connectNulls={false}/><Line type="monotone" dataKey="forecast" name="Baseline forecast" stroke="#9b8cff" strokeWidth={2.5} strokeDasharray="6 4" dot={{r:3,fill:'#9b8cff'}} connectNulls={false}/>{scenario&&<Line type="monotone" dataKey="scenario" name="What-if scenario" stroke="#f6a96c" strokeWidth={2} strokeDasharray="3 4" dot={false} connectNulls={false}/>}<Legend wrapperStyle={{fontSize:12,color:'#9caec6'}}/></LineChart></ResponsiveContainer></div>
}
