import React from 'react';

export default function StringStage({ step }) {
  if (!step || !step.state) {
    return <div style={{ padding: 20, textAlign: 'center', color: 'var(--color-ink-muted)' }}>No string data</div>;
  }

  const {
    text = '',
    pattern = '',
    position = 0,
    char_states = {},
    matches = [],
    pattern_hash,
    window_hash,
    hash_match,
    lps,
    z_array,
    z_box
  } = step.state;

  const charWidth = 32;

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 20, padding: 10 }}>
      {/* Algorithm specific status banners */}
      {pattern_hash !== undefined && (
        <div style={{ display: 'flex', gap: 20, fontSize: 13, fontFamily: 'var(--font-mono)' }}>
          <div>Pattern Hash: <strong>{pattern_hash}</strong></div>
          <div>Window Hash: <strong>{window_hash}</strong></div>
          {hash_match !== undefined && (
            <div style={{ color: hash_match ? 'var(--color-rose-deep)' : 'var(--color-ink-muted)' }}>
              Status: <strong>{hash_match ? 'HASH MATCH! Verifying chars...' : 'Hash Mismatch'}</strong>
            </div>
          )}
        </div>
      )}

      {/* SVG String Alignment Visualizer */}
      <svg width="100%" height="220" viewBox={`0 0 ${Math.max(500, text.length * charWidth + 60)} 220`}>
        {/* TEXT ROW */}
        <text x="10" y="45" fontSize="13" fontWeight="600" fill="var(--color-ink-muted)">Text:</text>
        {text.split('').map((char, idx) => {
          const x = idx * charWidth + 70;
          const isMatch = matches.some(m => idx >= m && idx < m + pattern.length);
          const isCurrentCompare = char_states.text_index === idx;

          let fill = 'var(--color-almond-silk)';
          let stroke = 'var(--color-line)';

          if (isCurrentCompare) {
            fill = char_states.status === 'match' ? 'var(--color-ash-grey)' : 'var(--color-sweet-salmon)';
            stroke = char_states.status === 'match' ? 'var(--color-ink)' : 'var(--color-blush-rose)';
          } else if (isMatch) {
            fill = 'var(--color-ash-grey)';
            stroke = 'var(--color-rose-deep)';
          }

          return (
            <g key={`text-${idx}`}>
              <rect x={x} y="25" width="28" height="32" fill={fill} stroke={stroke} rx="4" />
              <text x={x + 14} y="46" textAnchor="middle" fontSize="15" fontWeight="600" fontFamily="var(--font-mono)">
                {char}
              </text>
              <text x={x + 14} y="70" textAnchor="middle" fontSize="11" fontFamily="var(--font-mono)" fill="var(--color-ink-muted)">
                {idx}
              </text>
            </g>
          );
        })}

        {/* PATTERN ROW (Shifted to current position) */}
        <text x="10" y="125" fontSize="13" fontWeight="600" fill="var(--color-ink-muted)">Pattern:</text>
        {pattern.split('').map((char, pIdx) => {
          const x = (position + pIdx) * charWidth + 70;
          const isCurrentCompare = char_states.pattern_index === pIdx;

          let fill = 'var(--color-almond-silk)';
          let stroke = 'var(--color-camel)';

          if (isCurrentCompare) {
            fill = char_states.status === 'match' ? 'var(--color-ash-grey)' : 'var(--color-sweet-salmon)';
            stroke = 'var(--color-blush-rose)';
          }

          return (
            <g key={`pat-${pIdx}`}>
              <rect x={x} y="105" width="28" height="32" fill={fill} stroke={stroke} rx="4" />
              <text x={x + 14} y="126" textAnchor="middle" fontSize="15" fontWeight="600" fontFamily="var(--font-mono)">
                {char}
              </text>
            </g>
          );
        })}

        {/* Active Window Outline */}
        {pattern.length > 0 && (
          <rect
            x={position * charWidth + 66}
            y="18"
            width={pattern.length * charWidth + 2}
            height="126"
            fill="none"
            stroke="var(--color-camel)"
            strokeWidth="1.5"
            strokeDasharray="4 4"
            rx="6"
          />
        )}
      </svg>

      {/* LPS / Z-Array Data Rows */}
      {lps && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6, fontSize: 13, fontFamily: 'var(--font-mono)' }}>
          <div><strong>LPS Table:</strong></div>
          <div style={{ display: 'flex', gap: 6 }}>
            {lps.map((val, idx) => (
              <div key={idx} style={{ border: '1px solid var(--color-line)', padding: '2px 8px', borderRadius: 4, background: 'var(--color-paper)' }}>
                {pattern[idx]}: <strong>{val}</strong>
              </div>
            ))}
          </div>
        </div>
      )}

      {z_array && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6, fontSize: 13, fontFamily: 'var(--font-mono)' }}>
          <div><strong>Z-Array & Active Z-box [{z_box ? z_box.join(', ') : ''}]:</strong></div>
          <div style={{ display: 'flex', gap: 4, overflowX: 'auto', maxWidth: 600 }}>
            {z_array.map((val, idx) => (
              <div key={idx} style={{ border: '1px solid var(--color-line)', padding: '2px 6px', borderRadius: 4, background: (z_box && idx >= z_box[0] && idx <= z_box[1]) ? 'var(--color-almond-silk)' : 'var(--color-paper)' }}>
                {val}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
