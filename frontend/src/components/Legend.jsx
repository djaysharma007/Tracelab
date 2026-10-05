import React from 'react';

export default function Legend() {
  const items = [
    { label: 'Default', bg: 'var(--color-almond-silk)', border: '1px solid var(--color-ink)' },
    { label: 'Comparing', bg: 'var(--color-sweet-salmon)', border: '1.5px solid var(--color-ink)' },
    { label: 'Swapping / Active', bg: 'var(--color-blush-rose)', border: '1.5px solid var(--color-ink)' },
    { label: 'Sorted / Visited / Done', bg: 'var(--color-ash-grey)', border: '1px solid var(--color-ink)' },
    { label: 'Pivot / Pointer', bg: 'var(--color-camel)', border: '1px solid var(--color-ink)' },
    { label: 'Found / Result', bg: 'var(--color-ash-grey)', border: '2px solid var(--color-rose-deep)' }
  ];

  return (
    <div style={{
      display: 'flex',
      gap: 14,
      alignItems: 'center',
      padding: '6px 12px',
      background: 'var(--color-paper)',
      border: '1px solid var(--color-line)',
      borderRadius: 4,
      fontSize: 12
    }}>
      <span style={{ fontWeight: 600, color: 'var(--color-ink-muted)' }}>Legend:</span>
      {items.map((item, idx) => (
        <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <div style={{
            width: 14,
            height: 14,
            background: item.bg,
            border: item.border,
            borderRadius: 2
          }} />
          <span>{item.label}</span>
        </div>
      ))}
    </div>
  );
}
