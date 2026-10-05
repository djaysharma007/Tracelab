import React, { useMemo } from 'react';
import { forceSimulation, forceLink, forceManyBody, forceCenter } from 'd3-force';

export default function GraphStage({ step }) {
  if (!step || !step.state) {
    return <div style={{ padding: 20, textAlign: 'center', color: 'var(--color-ink-muted)' }}>No Graph data</div>;
  }

  const {
    nodes = [],
    edges = [],
    node_states = {},
    edge_states = {},
    queue_or_stack = [],
    distance_table,
    distance_matrix,
    row_labels,
    mst_cost
  } = step.state;

  // Use d3-force with deterministic layout
  const layoutNodes = useMemo(() => {
    if (!nodes || nodes.length === 0) return [];

    const simNodes = nodes.map((n, i) => ({
      ...n,
      // Fixed layout positions based on node index / circle layout fallback
      x: 300 + 160 * Math.cos((2 * Math.PI * i) / nodes.length),
      y: 160 + 110 * Math.sin((2 * Math.PI * i) / nodes.length)
    }));

    const simLinks = edges.map(e => ({
      source: e.u || e.source,
      target: e.v || e.target
    }));

    const sim = forceSimulation(simNodes)
      .force('link', forceLink(simLinks).id(d => d.id).distance(100))
      .force('charge', forceManyBody().strength(-300))
      .force('center', forceCenter(300, 160))
      .stop();

    for (let i = 0; i < 150; ++i) sim.tick();

    const nodePosMap = {};
    simNodes.forEach(n => {
      nodePosMap[n.id] = { x: n.x, y: n.y };
    });
    return nodePosMap;
  }, [nodes, edges]);

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', gap: 20, padding: 10 }}>
      {/* SVG Graph Drawing */}
      <div style={{ flex: 1, height: 320, border: '1px solid var(--color-line)', borderRadius: 4, background: 'var(--color-paper)', position: 'relative' }}>
        <svg width="100%" height="100%" viewBox="0 0 600 320">
          <defs>
            <marker id="graph-arrow" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--color-ink)" />
            </marker>
          </defs>

          {/* EDGES */}
          {edges.map((e, idx) => {
            const u = e.u || e.source;
            const v = e.v || e.target;
            const p1 = layoutNodes[u] || { x: 100, y: 100 };
            const p2 = layoutNodes[v] || { x: 200, y: 200 };

            const stateKey = `${u}-${v}`;
            const eState = edge_states[stateKey] || edge_states[`${v}-${u}`] || 'default';

            let stroke = 'var(--color-line)';
            let strokeWidth = 1.5;
            let strokeDasharray = 'none';

            if (eState === 'selected') {
              stroke = 'var(--color-rose-deep)';
              strokeWidth = 3;
            } else if (eState === 'considering') {
              stroke = 'var(--color-sweet-salmon)';
              strokeWidth = 2.5;
            } else if (eState === 'rejected') {
              stroke = 'var(--color-ink-muted)';
              strokeDasharray = '4 4';
            }

            const midX = (p1.x + p2.x) / 2;
            const midY = (p1.y + p2.y) / 2;

            return (
              <g key={`edge-${idx}`}>
                <line
                  x1={p1.x}
                  y1={p1.y}
                  x2={p2.x}
                  y2={p2.y}
                  stroke={stroke}
                  strokeWidth={strokeWidth}
                  strokeDasharray={strokeDasharray}
                />
                {e.weight !== undefined && (
                  <text
                    x={midX}
                    y={midY - 4}
                    textAnchor="middle"
                    fontSize="12"
                    fontWeight="600"
                    fontFamily="var(--font-mono)"
                    fill="var(--color-ink)"
                    style={{ background: 'var(--color-paper)', padding: 2 }}
                  >
                    {e.weight}
                  </text>
                )}
              </g>
            );
          })}

          {/* NODES */}
          {nodes.map(n => {
            const pos = layoutNodes[n.id] || { x: 150, y: 150 };
            const nState = node_states[n.id] || 'default';

            let fill = 'var(--color-almond-silk)';
            let stroke = 'var(--color-ink)';
            let strokeWidth = 1.5;

            if (nState === 'current') {
              fill = 'var(--color-sweet-salmon)';
              strokeWidth = 3;
            } else if (nState === 'visited') {
              fill = 'var(--color-ash-grey)';
            } else if (nState === 'selected') {
              fill = 'var(--color-rose-deep)';
            }

            return (
              <g key={`node-${n.id}`}>
                <circle
                  cx={pos.x}
                  cy={pos.y}
                  r="20"
                  fill={fill}
                  stroke={stroke}
                  strokeWidth={strokeWidth}
                />
                <text
                  x={pos.x}
                  y={pos.y + 5}
                  textAnchor="middle"
                  fontSize="14"
                  fontWeight="600"
                  fontFamily="var(--font-mono)"
                  fill={nState === 'selected' ? '#ffffff' : 'var(--color-ink)'}
                >
                  {n.label || n.id}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* SIDE DATA (Queue/Stack/Distances/Matrix) */}
      <div style={{ width: 220, border: '1px solid var(--color-line)', borderRadius: 4, padding: 12, background: 'var(--color-paper)', fontSize: 13, fontFamily: 'var(--font-mono)', overflowY: 'auto' }}>
        {queue_or_stack && queue_or_stack.length > 0 && (
          <div style={{ marginBottom: 14 }}>
            <strong>Queue / Stack:</strong>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4, marginTop: 4 }}>
              {queue_or_stack.map((item, i) => (
                <div key={i} style={{ padding: '3px 6px', background: 'var(--color-almond-silk)', borderRadius: 3 }}>
                  {item}
                </div>
              ))}
            </div>
          </div>
        )}

        {distance_table && (
          <div style={{ marginBottom: 14 }}>
            <strong>Distances:</strong>
            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: 4 }}>
              <tbody>
                {Object.entries(distance_table).map(([v, d]) => (
                  <tr key={v} style={{ borderBottom: '1px solid var(--color-line)' }}>
                    <td style={{ padding: '2px 4px' }}>{v}</td>
                    <td style={{ padding: '2px 4px', textAlign: 'right', fontWeight: '600' }}>{d}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {mst_cost !== undefined && (
          <div style={{ marginTop: 10 }}>
            <strong>MST Total Cost:</strong>
            <div style={{ fontSize: 18, fontWeight: '700', color: 'var(--color-rose-deep)' }}>{mst_cost}</div>
          </div>
        )}
      </div>
    </div>
  );
}
