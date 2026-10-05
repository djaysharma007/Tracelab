import React, { useState, useEffect } from 'react';
import { fetchAlgorithms, compareAlgorithms, generateInput } from '../api/client';
import Header from '../components/Header';
import RestyledChart from '../components/RestyledChart';
import { Play, AlertCircle, Info } from 'lucide-react';

const INPUT_KIND_MAP = {
  'Sorting': [
    { value: 'random', label: 'Random Input' },
    { value: 'sorted', label: 'Already Sorted' },
    { value: 'reverse', label: 'Reverse Sorted' },
    { value: 'duplicates', label: 'Many Duplicates' },
    { value: 'nearly_sorted', label: 'Nearly Sorted' }
  ],
  'Searching': [
    { value: 'sorted', label: 'Sorted Array (Element Present)' },
    { value: 'not_found', label: 'Sorted Array (Element Absent)' },
    { value: 'duplicates', label: 'Sorted Array with Duplicates' },
    { value: 'reverse', label: 'Reverse Sorted Array' }
  ],
  'String matching': [
    { value: 'random', label: 'Random Text & Pattern' },
    { value: 'multiple', label: 'Multiple Matches' },
    { value: 'worst_case', label: 'Worst-Case Overlapping Pattern' },
    { value: 'no_match', label: 'No Match' }
  ],
  'Traversal': [
    { value: 'random', label: 'Random Graph' },
    { value: 'dense', label: 'Dense Graph (Many Edges)' },
    { value: 'sparse', label: 'Sparse / Path Graph' }
  ],
  'Shortest path': [
    { value: 'random', label: 'Random Weighted Graph' },
    { value: 'dense', label: 'Dense Graph' },
    { value: 'sparse', label: 'Sparse Graph' }
  ],
  'Minimum spanning tree': [
    { value: 'random', label: 'Random Weighted Graph' },
    { value: 'dense', label: 'Dense Graph' },
    { value: 'sparse', label: 'Sparse Graph' }
  ]
};

export default function Compare() {
  const [allAlgorithms, setAllAlgorithms] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState('Sorting');
  const [selectedAlgIds, setSelectedAlgIds] = useState([]);
  const [inputKind, setInputKind] = useState('random');
  const [sizesStr, setSizesStr] = useState('10, 50, 100, 500, 1000');
  const [repeats, setRepeats] = useState(3);
  const [samplePreview, setSamplePreview] = useState(null);

  const [activeMetric, setActiveMetric] = useState('time_ms');
  const [compareData, setCompareData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAlgorithms().then(algs => {
      setAllAlgorithms(algs);
    }).catch(err => setError(err.message));
  }, []);

  const groupAlgorithms = allAlgorithms.filter(a => a.compare_group === selectedGroup);

  // Auto-select algorithms & reset inputKind when group changes
  useEffect(() => {
    if (groupAlgorithms.length > 0) {
      setSelectedAlgIds(groupAlgorithms.map(a => a.id));
    }
    const defaultInputKind = INPUT_KIND_MAP[selectedGroup]?.[0]?.value || 'random';
    setInputKind(defaultInputKind);
  }, [selectedGroup, allAlgorithms]);

  // Fetch live sample preview whenever algorithm or inputKind changes
  useEffect(() => {
    if (selectedAlgIds.length === 0) return;
    generateInput(selectedAlgIds[0], 10, null, inputKind)
      .then(inp => setSamplePreview(inp))
      .catch(() => setSamplePreview(null));
  }, [selectedAlgIds, inputKind]);

  const handleToggleAlg = (id) => {
    if (selectedAlgIds.includes(id)) {
      setSelectedAlgIds(selectedAlgIds.filter(i => i !== id));
    } else {
      setSelectedAlgIds([...selectedAlgIds, id]);
    }
  };

  const handleRunCompare = async () => {
    if (selectedAlgIds.length === 0) {
      setError('Please select at least one algorithm to compare.');
      return;
    }
    setError(null);
    setLoading(true);

    const sizes = sizesStr.split(',').map(s => parseInt(s.trim(), 10)).filter(n => !isNaN(n));

    try {
      const res = await compareAlgorithms(selectedGroup, selectedAlgIds, inputKind, sizes, repeats);
      setCompareData(res);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const groups = Array.from(new Set(allAlgorithms.map(a => a.compare_group).filter(Boolean))).sort();
  const availableInputKinds = INPUT_KIND_MAP[selectedGroup] || [{ value: 'random', label: 'Random Input' }];

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: 'var(--color-paper)' }}>
      <Header />

      <main style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Left Controls Panel */}
        <div style={{
          width: 320,
          borderRight: '1px solid var(--color-line)',
          padding: 20,
          display: 'flex',
          flexDirection: 'column',
          gap: 18,
          background: 'var(--color-paper)',
          overflowY: 'auto'
        }}>
          <h2 style={{ fontSize: 18, fontFamily: 'var(--font-heading)' }}>Compare Controls</h2>

          {error && (
            <div style={{ padding: 10, background: 'var(--color-almond-silk)', border: '1px solid var(--color-sweet-salmon)', borderRadius: 4, color: 'var(--color-rose-deep)', fontSize: 12, display: 'flex', gap: 6 }}>
              <AlertCircle size={16} />
              <div>{error}</div>
            </div>
          )}

          {/* Group Selector */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <label style={{ fontSize: 13, color: 'var(--color-ink-muted)' }}>Compare Group:</label>
            <select
              value={selectedGroup}
              onChange={(e) => setSelectedGroup(e.target.value)}
              style={{
                padding: '8px 10px',
                borderRadius: 4,
                border: '1px solid var(--color-camel)',
                background: 'var(--color-ink)',
                color: '#ffffff',
                fontWeight: '500'
              }}
            >
              {groups.map(g => (
                <option key={g} value={g} style={{ background: 'var(--color-ink)', color: '#ffffff' }}>{g}</option>
              ))}
            </select>
          </div>

          {/* Algorithm Checkboxes */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <label style={{ fontSize: 13, color: 'var(--color-ink-muted)' }}>Select Algorithms:</label>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6, border: '1px solid var(--color-line)', padding: 10, borderRadius: 4, background: 'var(--color-paper)' }}>
              {groupAlgorithms.map(alg => (
                <label key={alg.id} style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 13, cursor: 'pointer', color: 'var(--color-ink)' }}>
                  <input
                    type="checkbox"
                    checked={selectedAlgIds.includes(alg.id)}
                    onChange={() => handleToggleAlg(alg.id)}
                    style={{ accentColor: 'var(--color-rose-deep)' }}
                  />
                  <span>{alg.name}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Input Kind Selector */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <label style={{ fontSize: 13, color: 'var(--color-ink-muted)' }}>Input Kind / Scenario:</label>
            <select
              value={inputKind}
              onChange={(e) => setInputKind(e.target.value)}
              style={{
                padding: '8px 10px',
                borderRadius: 4,
                border: '1px solid var(--color-camel)',
                background: 'var(--color-ink)',
                color: '#ffffff',
                fontWeight: '500'
              }}
            >
              {availableInputKinds.map(ik => (
                <option key={ik.value} value={ik.value} style={{ background: 'var(--color-ink)', color: '#ffffff' }}>{ik.label}</option>
              ))}
            </select>
          </div>

          {/* Sample Input Preview Box */}
          {samplePreview && (
            <div style={{
              background: 'var(--color-ink)',
              color: '#ffffff',
              padding: '10px 12px',
              borderRadius: 4,
              border: '1px solid var(--color-camel)',
              fontSize: 12,
              fontFamily: 'var(--font-mono)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 4, color: 'var(--color-almond-silk)', marginBottom: 4, fontWeight: '600' }}>
                <Info size={13} />
                <span>Generated Input Preview (n=10):</span>
              </div>
              <div style={{ wordBreak: 'break-all', opacity: 0.9, lineHeight: 1.4 }}>
                {JSON.stringify(samplePreview)}
              </div>
            </div>
          )}

          {/* Sizes */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <label style={{ fontSize: 13, color: 'var(--color-ink-muted)' }}>Input Sizes (comma-separated):</label>
            <input
              type="text"
              value={sizesStr}
              onChange={(e) => setSizesStr(e.target.value)}
              style={{
                padding: '8px 10px',
                border: '1px solid var(--color-camel)',
                borderRadius: 4,
                fontFamily: 'var(--font-mono)',
                background: 'var(--color-ink)',
                color: '#ffffff'
              }}
            />
          </div>

          {/* Run Button */}
          <button
            onClick={handleRunCompare}
            disabled={loading}
            className="btn-primary"
            style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6, padding: '10px 0', marginTop: 10 }}
          >
            <Play size={16} />
            <span>{loading ? 'Benchmarking...' : 'Run Comparison'}</span>
          </button>
        </div>

        {/* Center Chart & Results Table */}
        <div style={{ flex: 1, padding: 24, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 24 }}>
          {/* Metric Selector Tabs */}
          <div style={{ display: 'flex', gap: 10, borderBottom: '1px solid var(--color-line)', paddingBottom: 10 }}>
            <span style={{ fontWeight: 600, fontSize: 14, alignSelf: 'center', marginRight: 10 }}>Metric:</span>
            {[
              { id: 'time_ms', label: 'Execution Time (ms)' },
              { id: 'operations', label: 'Operations Count' },
              { id: 'memory_kb', label: 'Peak Memory (KB)' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveMetric(tab.id)}
                style={{
                  background: activeMetric === tab.id ? 'var(--color-almond-silk)' : 'transparent',
                  borderColor: activeMetric === tab.id ? 'var(--color-camel)' : 'var(--color-line)',
                  fontWeight: activeMetric === tab.id ? '600' : '400'
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Chart Display */}
          <div style={{ border: '1px solid var(--color-line)', borderRadius: 4, padding: 20, background: 'var(--color-paper)' }}>
            {compareData ? (
              <RestyledChart seriesMap={compareData.series} metric={activeMetric} />
            ) : (
              <div style={{ padding: 60, textAlign: 'center', color: 'var(--color-ink-muted)' }}>
                Configure benchmark controls on the left and click "Run Comparison" to generate charts.
              </div>
            )}
          </div>

          {/* Results Table with Skipped Points Flagged */}
          {compareData && (
            <div style={{ border: '1px solid var(--color-line)', borderRadius: 4, overflow: 'hidden' }}>
              <div style={{ padding: '12px 16px', background: 'var(--color-almond-silk)', fontWeight: 600, fontSize: 14 }}>
                Detailed Benchmark Results & Theoretical Complexity
              </div>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontFamily: 'var(--font-mono)', fontSize: 13 }}>
                <thead>
                  <tr style={{ background: 'var(--color-paper)', borderBottom: '1px solid var(--color-line)' }}>
                    <th style={{ padding: 10, borderRight: '1px solid var(--color-line)' }}>Algorithm</th>
                    <th style={{ padding: 10, borderRight: '1px solid var(--color-line)' }}>Size (n)</th>
                    <th style={{ padding: 10, borderRight: '1px solid var(--color-line)' }}>Time (ms)</th>
                    <th style={{ padding: 10, borderRight: '1px solid var(--color-line)' }}>Memory (KB)</th>
                    <th style={{ padding: 10, borderRight: '1px solid var(--color-line)' }}>Theory (Average)</th>
                    <th style={{ padding: 10 }}>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.values(compareData.series).flatMap(series => {
                    const algMeta = allAlgorithms.find(a => a.id === series.algorithm_id);
                    return series.points.map((pt, pIdx) => (
                      <tr key={`${series.algorithm_id}-${pt.size}`} style={{ borderBottom: '1px solid var(--color-line)' }}>
                        <td style={{ padding: 10, borderRight: '1px solid var(--color-line)', fontWeight: 600 }}>
                          {series.algorithm_name}
                        </td>
                        <td style={{ padding: 10, borderRight: '1px solid var(--color-line)' }}>{pt.size}</td>
                        <td style={{ padding: 10, borderRight: '1px solid var(--color-line)' }}>
                          {pt.skipped ? '—' : pt.time_ms}
                        </td>
                        <td style={{ padding: 10, borderRight: '1px solid var(--color-line)' }}>
                          {pt.skipped ? '—' : pt.memory_kb}
                        </td>
                        <td style={{ padding: 10, borderRight: '1px solid var(--color-line)', color: 'var(--color-ink-muted)' }}>
                          {algMeta?.complexity.average || '—'}
                        </td>
                        <td style={{ padding: 10, color: pt.skipped ? 'var(--color-rose-deep)' : 'var(--color-ink)' }}>
                          {pt.skipped ? `SKIPPED (${pt.skip_reason})` : 'Measured'}
                        </td>
                      </tr>
                    ));
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
