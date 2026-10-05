import React from 'react';
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid
} from 'recharts';

const PALETTE_COLORS = [
  'var(--color-rose-deep)',
  'var(--color-camel)',
  'var(--color-ink)',
  'var(--color-sweet-salmon)',
  'var(--color-blush-rose)'
];

export default function RestyledChart({ seriesMap = {}, metric = 'time_ms' }) {
  const algIds = Object.keys(seriesMap);
  if (algIds.length === 0) {
    return <div style={{ padding: 40, textAlign: 'center', color: 'var(--color-ink-muted)' }}>No comparison data</div>;
  }

  // Flatten points by input size
  const sizeMap = {};
  algIds.forEach(algId => {
    const series = seriesMap[algId];
    if (series && series.points) {
      series.points.forEach(pt => {
        if (!sizeMap[pt.size]) {
          sizeMap[pt.size] = { size: pt.size };
        }
        if (!pt.skipped) {
          if (metric === 'time_ms') sizeMap[pt.size][algId] = pt.time_ms;
          else if (metric === 'memory_kb') sizeMap[pt.size][algId] = pt.memory_kb;
          else if (metric === 'operations' && pt.operations) {
            // Sum total operations
            const totalOps = Object.values(pt.operations).reduce((a, b) => a + b, 0);
            sizeMap[pt.size][algId] = totalOps;
          }
        }
      });
    }
  });

  const chartData = Object.values(sizeMap).sort((a, b) => a.size - b.size);

  const unitLabel = metric === 'time_ms' ? 'ms' : (metric === 'memory_kb' ? 'KB' : 'ops');

  return (
    <div style={{ width: '100%', height: 360, position: 'relative' }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData} margin={{ top: 20, right: 120, left: 20, bottom: 20 }}>
          <CartesianGrid stroke="var(--color-line)" strokeDasharray="3 3" vertical={false} />
          <XAxis
            dataKey="size"
            stroke="var(--color-ink-muted)"
            fontSize={12}
            fontFamily="var(--font-mono)"
            tickLine={false}
            label={{ value: 'Input Size (n)', position: 'insideBottom', offset: -10, fontSize: 12, fill: 'var(--color-ink-muted)' }}
          />
          <YAxis
            stroke="var(--color-ink-muted)"
            fontSize={12}
            fontFamily="var(--font-mono)"
            tickLine={false}
            axisLine={false}
            label={{ value: `Measured (${unitLabel})`, angle: -90, position: 'insideLeft', fontSize: 12, fill: 'var(--color-ink-muted)' }}
          />
          <Tooltip
            contentStyle={{
              background: 'var(--color-paper)',
              border: '1px solid var(--color-line)',
              borderRadius: 4,
              fontFamily: 'var(--font-mono)',
              fontSize: 12
            }}
          />

          {algIds.map((algId, idx) => {
            const seriesName = seriesMap[algId]?.algorithm_name || algId;
            const strokeColor = PALETTE_COLORS[idx % PALETTE_COLORS.length];
            return (
              <Line
                key={algId}
                type="monotone"
                dataKey={algId}
                name={seriesName}
                stroke={strokeColor}
                strokeWidth={2.5}
                dot={{ r: 4, fill: strokeColor }}
                activeDot={{ r: 6 }}
              />
            );
          })}
        </LineChart>
      </ResponsiveContainer>

      {/* Direct Line End Labels (PRD requirement: no boxed legends) */}
      <div style={{ display: 'flex', gap: 16, justifyContent: 'center', marginTop: 10 }}>
        {algIds.map((algId, idx) => (
          <div key={algId} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 13, fontFamily: 'var(--font-mono)' }}>
            <div style={{ width: 12, height: 3, background: PALETTE_COLORS[idx % PALETTE_COLORS.length] }} />
            <span>{seriesMap[algId]?.algorithm_name || algId}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
