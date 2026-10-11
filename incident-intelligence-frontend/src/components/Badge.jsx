import React from 'react';
export function SeverityBadge({ value = 'SEV3' }) { return <span className={`badge severity ${String(value).toLowerCase()}`}>{value}</span>; }
export function StatusBadge({ value = 'OPEN' }) { return <span className={`badge status ${String(value).toLowerCase()}`}>{String(value).replaceAll('_', ' ')}</span>; }
