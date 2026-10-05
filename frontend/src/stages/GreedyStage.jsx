import React from 'react';

export default function GreedyStage({ step }) {
  if (!step || !step.state) {
    return <div style={{ padding: 20, textAlign: 'center', color: 'var(--color-ink-muted)' }}>No Greedy data</div>;
  }

  const {
    activities,
    current_activity,
    selected = [],
    rejected = [],
    items,
    capacity,
    remaining_capacity,
    taken_items = [],
    total_value,
    frequencies,
    tree,
    codes,
    jobs,
    slots,
    assigned_jobs = [],
    total_profit
  } = step.state;

  // --- ACTIVITY SELECTION TIMELINE ---
  if (activities) {
    const maxFinish = Math.max(...activities.map(a => a.finish), 14);
    return (
      <div style={{ width: '100%', padding: 10, display: 'flex', flexDirection: 'column', gap: 14 }}>
        <div style={{ fontSize: 14, fontWeight: 600 }}>Activity Selection Timeline (0 to {maxFinish}):</div>
        <svg width="100%" height="260" viewBox={`0 0 ${maxFinish * 40 + 80} 260`}>
          {/* Time axis ticks */}
          {Array.from({ length: maxFinish + 1 }).map((_, t) => (
            <g key={t}>
              <line x1={t * 40 + 60} y1="20" x2={t * 40 + 60} y2="220" stroke="var(--color-line)" strokeDasharray="2 2" />
              <text x={t * 40 + 60} y="240" textAnchor="middle" fontSize="12" fontFamily="var(--font-mono)">{t}</text>
            </g>
          ))}

          {/* Activity Interval Bars */}
          {activities.map((act, i) => {
            const x1 = act.start * 40 + 60;
            const width = (act.finish - act.start) * 40;
            const y = i * 18 + 30;

            const isSel = selected.some(s => s.name === act.name);
            const isRej = rejected.some(r => r.name === act.name);
            const isCurr = current_activity && current_activity.name === act.name;

            let fill = 'var(--color-almond-silk)';
            let stroke = 'var(--color-line)';

            if (isSel) {
              fill = 'var(--color-ash-grey)';
              stroke = 'var(--color-rose-deep)';
            } else if (isRej) {
              fill = 'var(--color-paper)';
              stroke = 'var(--color-ink-muted)';
            } else if (isCurr) {
              fill = 'var(--color-sweet-salmon)';
            }

            return (
              <g key={i}>
                <rect x={x1} y={y} width={width} height="14" fill={fill} stroke={stroke} rx="3" />
                <text x={x1 - 8} y={y + 11} textAnchor="end" fontSize="11" fontFamily="var(--font-mono)">{act.name}</text>
              </g>
            );
          })}
        </svg>
      </div>
    );
  }

  // --- FRACTIONAL KNAPSACK ---
  if (items) {
    const fillPercent = Math.min(100, Math.round(((capacity - (remaining_capacity || 0)) / capacity) * 100));
    return (
      <div style={{ width: '100%', padding: 14, display: 'flex', flexDirection: 'column', gap: 16 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div><strong>Knapsack Capacity Fill Level:</strong> {fillPercent}% ({capacity - remaining_capacity} / {capacity})</div>
          <div style={{ fontSize: 16, fontWeight: 700, color: 'var(--color-rose-deep)' }}>Total Value: {total_value}</div>
        </div>

        {/* Capacity Bar */}
        <div style={{ width: '100%', height: 24, border: '1px solid var(--color-line)', borderRadius: 4, background: 'var(--color-paper)', overflow: 'hidden' }}>
          <div style={{ width: `${fillPercent}%`, height: '100%', background: 'var(--color-sweet-salmon)', transition: 'width 0.3s ease-out' }} />
        </div>

        {/* Item Ratios Table */}
        <table style={{ width: '100%', borderCollapse: 'collapse', fontFamily: 'var(--font-mono)', fontSize: 13 }}>
          <thead>
            <tr style={{ background: 'var(--color-almond-silk)', textAlign: 'left' }}>
              <th style={{ padding: 8, border: '1px solid var(--color-line)' }}>Item</th>
              <th style={{ padding: 8, border: '1px solid var(--color-line)' }}>Weight</th>
              <th style={{ padding: 8, border: '1px solid var(--color-line)' }}>Value</th>
              <th style={{ padding: 8, border: '1px solid var(--color-line)' }}>Ratio (V/W)</th>
              <th style={{ padding: 8, border: '1px solid var(--color-line)' }}>Taken Status</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, idx) => {
              const taken = taken_items.find(t => t.name === item.name);
              return (
                <tr key={idx} style={{ background: taken ? 'var(--color-ash-grey)' : 'var(--color-paper)' }}>
                  <td style={{ padding: 8, border: '1px solid var(--color-line)' }}>{item.name}</td>
                  <td style={{ padding: 8, border: '1px solid var(--color-line)' }}>{item.weight}</td>
                  <td style={{ padding: 8, border: '1px solid var(--color-line)' }}>{item.value}</td>
                  <td style={{ padding: 8, border: '1px solid var(--color-line)', fontWeight: 600 }}>{item.ratio}</td>
                  <td style={{ padding: 8, border: '1px solid var(--color-line)' }}>
                    {taken ? `${Math.round(taken.fraction * 100)}% (${taken.value} val)` : '0%'}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  }

  // --- HUFFMAN CODING ---
  if (codes !== undefined && (tree || frequencies)) {
    return (
      <div style={{ width: '100%', padding: 10, display: 'flex', gap: 20 }}>
        {/* Codes Table */}
        <div style={{ flex: 1, border: '1px solid var(--color-line)', padding: 12, borderRadius: 4, background: 'var(--color-paper)' }}>
          <strong style={{ display: 'block', marginBottom: 8 }}>Generated Huffman Codes:</strong>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontFamily: 'var(--font-mono)', fontSize: 13 }}>
            <thead>
              <tr style={{ background: 'var(--color-almond-silk)' }}>
                <th style={{ padding: 6, border: '1px solid var(--color-line)' }}>Char</th>
                <th style={{ padding: 6, border: '1px solid var(--color-line)' }}>Freq</th>
                <th style={{ padding: 6, border: '1px solid var(--color-line)' }}>Huffman Code</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(frequencies || {}).map(([char, freq]) => (
                <tr key={char}>
                  <td style={{ padding: 6, border: '1px solid var(--color-line)', fontWeight: 600 }}>'{char}'</td>
                  <td style={{ padding: 6, border: '1px solid var(--color-line)' }}>{freq}</td>
                  <td style={{ padding: 6, border: '1px solid var(--color-line)', fontWeight: 700, color: 'var(--color-rose-deep)' }}>
                    {codes[char] || '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

  // --- JOB SEQUENCING ---
  if (jobs && slots) {
    return (
      <div style={{ width: '100%', padding: 10, display: 'flex', flexDirection: 'column', gap: 16 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div><strong>Scheduled Jobs:</strong> {assigned_jobs.join(', ') || 'None'}</div>
          <div style={{ fontSize: 16, fontWeight: 700, color: 'var(--color-rose-deep)' }}>Total Profit: {total_profit}</div>
        </div>

        {/* Time Slot Grid */}
        <div style={{ display: 'flex', gap: 12 }}>
          {slots.map((jobId, sIdx) => (
            <div key={sIdx} style={{
              flex: 1,
              padding: 14,
              textAlign: 'center',
              border: '2px solid var(--color-camel)',
              borderRadius: 6,
              background: jobId !== 'Free' ? 'var(--color-ash-grey)' : 'var(--color-paper)',
              fontFamily: 'var(--font-mono)'
            }}>
              <div style={{ fontSize: 11, color: 'var(--color-ink-muted)', marginBottom: 4 }}>Slot {sIdx + 1}</div>
              <div style={{ fontSize: 16, fontWeight: 700, color: 'var(--color-ink)' }}>{jobId}</div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return <div style={{ padding: 20 }}>Greedy Algorithm View</div>;
}
