import React from 'react';
export default function MetricCard({label,value,sub,icon:Icon,tone='mint'}){return <div className={`metric-card ${tone}`}><div className="metric-top"><span>{label}</span>{Icon&&<Icon size={17}/>}</div><strong>{value}</strong><small>{sub}</small></div>}
