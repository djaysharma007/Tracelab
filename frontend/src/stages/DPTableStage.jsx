import React from 'react';

export default function DPTableStage({ step }) {
  if (!step || !step.state || !step.state.table) {
    return <div style={{ padding: 20, textAlign: 'center', color: 'var(--color-ink-muted)' }}>No DP Table data</div>;
  }

  const {
    table,
    row_labels = [],
    col_labels = [],
    current_cell = [-1, -1],
    dependent_cells = [],
    solution_path = [],
    formula = ''
  } = step.state;

  const isDepCell = (r, c) => dependent_cells.some(([dr, dc]) => dr === r && dc === c);
  const isSolCell = (r, c) => solution_path.some(([sr, sc]) => sr === r && sc === c);
  const isCurrCell = (r, c) => current_cell[0] === r && current_cell[1] === c;

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14, padding: 10 }}>
      {/* Recurrence Formula Banner */}
      {formula && (
        <div style={{
          padding: '8px 16px',
          background: 'var(--color-paper)',
          border: '1px solid var(--color-camel)',
          borderRadius: 4,
          fontFamily: 'var(--font-mono)',
          fontSize: 13,
          color: 'var(--color-ink)'
        }}>
          {formula}
        </div>
      )}

      {/* Render Table */}
      <div style={{ overflow: 'auto', maxWidth: '100%', maxHeight: 320, border: '1px solid var(--color-line)', borderRadius: 4 }}>
        <table style={{ borderCollapse: 'collapse', fontFamily: 'var(--font-mono)', fontSize: 13, textVariantNumeric: 'tabular-nums' }}>
          <thead>
            <tr>
              <th style={{ background: 'var(--color-almond-silk)', padding: '6px 12px', border: '1px solid var(--color-line)' }}>i \ j</th>
              {col_labels.map((colLabel, j) => (
                <th key={j} style={{ background: 'var(--color-almond-silk)', padding: '6px 12px', border: '1px solid var(--color-line)', fontWeight: '600' }}>
                  {colLabel}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {table.map((row, r) => (
              <tr key={r}>
                <td style={{ background: 'var(--color-almond-silk)', padding: '6px 12px', border: '1px solid var(--color-line)', fontWeight: '600' }}>
                  {row_labels[r] || r}
                </td>
                {row.map((val, c) => {
                  const curr = isCurrCell(r, c);
                  const dep = isDepCell(r, c);
                  const sol = isSolCell(r, c);

                  let bg = 'var(--color-paper)';
                  let color = 'var(--color-ink)';
                  let fontWeight = '400';
                  let border = '1px solid var(--color-line)';

                  if (curr) {
                    bg = 'var(--color-sweet-salmon)';
                    fontWeight = '700';
                    border = '2px solid var(--color-rose-deep)';
                  } else if (dep) {
                    bg = 'var(--color-almond-silk)';
                    fontWeight = '600';
                    border = '1.5px solid var(--color-camel)';
                  } else if (sol) {
                    bg = 'var(--color-ash-grey)';
                    fontWeight = '700';
                    border = '2px solid var(--color-rose-deep)';
                  }

                  return (
                    <td
                      key={c}
                      style={{
                        padding: '8px 14px',
                        textAlign: 'center',
                        background: bg,
                        color: color,
                        fontWeight: fontWeight,
                        border: border,
                        transition: 'all 0.15s ease-out'
                      }}
                    >
                      {val}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
