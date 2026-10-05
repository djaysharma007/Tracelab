import React from 'react';

export default function ArrayStage({ step }) {
  if (!step || !step.state || !step.state.array) {
    return <div style={{ padding: 20, textAlign: 'center', color: 'var(--color-ink-muted)' }}>No array data</div>;
  }

  const { array, highlights = {}, pointers = {}, sorted_indices = [], subranges = [] } = step.state;
  const maxVal = Math.max(...array.map(v => (typeof v === 'number' ? Math.abs(v) : 1)), 1);

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <svg width="100%" height="320" viewBox={`0 0 ${Math.max(600, array.length * 60)} 320`} style={{ overflow: 'visible' }}>
        <defs>
          <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--color-ink)" />
          </marker>
        </defs>

        {/* Render subrange boundaries if any (e.g. Merge Sort) */}
        {subranges.map((range, idx) => {
          const [start, end] = range;
          const x1 = start * 55 + 10;
          const x2 = (end + 1) * 55 + 5;
          return (
            <rect
              key={`subrange-${idx}`}
              x={x1}
              y={40}
              width={x2 - x1}
              height={220}
              fill="none"
              stroke="var(--color-camel)"
              strokeDasharray="4 4"
              strokeWidth="1.5"
              rx="6"
            />
          );
        })}

        {/* Array Elements */}
        {array.map((val, idx) => {
          const x = idx * 55 + 20;
          const h = typeof val === 'number' ? Math.max(30, (Math.abs(val) / maxVal) * 140) : 40;
          const y = 220 - h;

          const hState = highlights[idx];
          const isSorted = sorted_indices.includes(idx) || hState === 'sorted';

          let fillColor = 'var(--color-almond-silk)';
          let strokeColor = 'var(--color-ink)';
          let strokeWidth = 1;

          if (hState === 'comparing') {
            fillColor = 'var(--color-sweet-salmon)';
            strokeWidth = 2;
          } else if (hState === 'swapping') {
            fillColor = 'var(--color-blush-rose)';
            strokeWidth = 2;
          } else if (hState === 'pivot' || hState === 'pointer') {
            fillColor = 'var(--color-camel)';
          } else if (hState === 'found') {
            fillColor = 'var(--color-ash-grey)';
            strokeColor = 'var(--color-rose-deep)';
            strokeWidth = 3;
          } else if (isSorted) {
            fillColor = 'var(--color-ash-grey)';
          }

          return (
            <g key={idx}>
              {/* Bar / Box */}
              <rect
                x={x}
                y={y}
                width="45"
                height={h}
                fill={fillColor}
                stroke={strokeColor}
                strokeWidth={strokeWidth}
                rx="4"
                style={{ transition: 'all 0.2s ease-out' }}
              />

              {/* Element Value */}
              <text
                x={x + 22.5}
                y={y + h / 2 + 5}
                textAnchor="middle"
                fontSize="14"
                fontWeight="600"
                fontFamily="var(--font-mono)"
                fill={hState === 'swapping' ? '#ffffff' : 'var(--color-ink)'}
              >
                {val}
              </text>

              {/* Element Index */}
              <text
                x={x + 22.5}
                y="245"
                textAnchor="middle"
                fontSize="12"
                fontFamily="var(--font-mono)"
                fill="var(--color-ink-muted)"
              >
                {idx}
              </text>
            </g>
          );
        })}

        {/* Pointers / Markers */}
        {Object.entries(pointers).map(([pName, pVal], idx) => {
          if (typeof pVal !== 'number' || pVal < 0 || pVal >= array.length) return null;
          const px = pVal * 55 + 42.5;
          const py = 270 + idx * 18;

          return (
            <g key={pName}>
              <polygon points={`${px},252 ${px - 5},260 ${px + 5},260`} fill="var(--color-camel)" />
              <text
                x={px}
                y={py}
                textAnchor="middle"
                fontSize="11"
                fontWeight="600"
                fontFamily="var(--font-mono)"
                fill="var(--color-ink)"
              >
                {pName}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
