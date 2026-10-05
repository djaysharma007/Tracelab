import React, { useState } from 'react';

export default function Inspector({
  steps = [],
  currentIndex = 0,
  metrics = null,
  complexity = null,
  onJumpToStep
}) {
  const [activeTab, setActiveTab] = useState('steps'); // 'steps' | 'metrics' | 'complexity'

  const currentStep = steps[currentIndex] || null;

  return (
    <div style={{
      width: 320,
      borderLeft: '1px solid var(--color-line)',
      background: 'var(--color-paper)',
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      overflow: 'hidden'
    }}>
      {/* Tabs */}
      <div style={{ display: 'flex', borderBottom: '1px solid var(--color-line)' }}>
        {['steps', 'metrics', 'complexity'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              flex: 1,
              padding: '10px 0',
              borderRadius: 0,
              border: 'none',
              borderBottom: activeTab === tab ? '2px solid var(--color-rose-deep)' : 'none',
              background: activeTab === tab ? 'var(--color-paper)' : 'var(--color-almond-silk)',
              fontWeight: activeTab === tab ? '600' : '400',
              textTransform: 'capitalize',
              fontSize: 13
            }}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div style={{ flex: 1, overflowY: 'auto', padding: 12 }}>
        {/* STEPS TAB */}
        {activeTab === 'steps' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {steps.length === 0 ? (
              <div style={{ color: 'var(--color-ink-muted)', fontSize: 13, textAlign: 'center', padding: 20 }}>
                No steps recorded yet. Run an algorithm to generate trace log.
              </div>
            ) : (
              steps.map((step, idx) => {
                const isSelected = idx === currentIndex;
                return (
                  <div
                    key={idx}
                    onClick={() => onJumpToStep(idx)}
                    style={{
                      padding: '8px 10px',
                      borderRadius: 4,
                      cursor: 'pointer',
                      border: '1px solid',
                      borderColor: isSelected ? 'var(--color-rose-deep)' : 'var(--color-line)',
                      background: isSelected ? 'var(--color-almond-silk)' : 'transparent',
                      transition: 'all 0.1s ease-out'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: 'var(--color-ink-muted)', marginBottom: 2 }}>
                      <span style={{ fontFamily: 'var(--font-mono)' }}>#{step.index}</span>
                      <span style={{ fontWeight: '600', textTransform: 'uppercase' }}>{step.type}</span>
                    </div>
                    <div style={{ fontSize: 13, color: 'var(--color-ink)' }}>{step.message}</div>
                  </div>
                );
              })
            )}
          </div>
        )}

        {/* METRICS TAB */}
        {activeTab === 'metrics' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {/* Run Measured Performance */}
            {metrics ? (
              <div style={{ border: '1px solid var(--color-line)', padding: 12, borderRadius: 4, background: 'var(--color-paper)' }}>
                <div style={{ fontSize: 12, color: 'var(--color-ink-muted)', marginBottom: 8, textTransform: 'uppercase', fontWeight: 600 }}>
                  Run Performance (3-pass measured)
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                  <span>Execution Time:</span>
                  <strong style={{ fontFamily: 'var(--font-mono)' }}>{metrics.execution_time_ms} ms</strong>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                  <span>Peak Memory:</span>
                  <strong style={{ fontFamily: 'var(--font-mono)' }}>{metrics.memory_kb} KB</strong>
                </div>
                {!metrics.is_timing_reliable && metrics.timing_note && (
                  <div style={{ fontSize: 11, color: 'var(--color-camel)', marginTop: 4 }}>
                    Note: {metrics.timing_note}
                  </div>
                )}
              </div>
            ) : (
              <div style={{ fontSize: 13, color: 'var(--color-ink-muted)' }}>Run algorithm to view measured time and memory.</div>
            )}

            {/* Current Step Counters */}
            <div style={{ border: '1px solid var(--color-line)', padding: 12, borderRadius: 4, background: 'var(--color-paper)' }}>
              <div style={{ fontSize: 12, color: 'var(--color-ink-muted)', marginBottom: 8, textTransform: 'uppercase', fontWeight: 600 }}>
                Cumulative Operation Counters (Step {currentIndex + 1})
              </div>
              {currentStep && currentStep.counters && Object.keys(currentStep.counters).length > 0 ? (
                Object.entries(currentStep.counters).map(([key, val]) => (
                  <div key={key} style={{ display: 'flex', justifyContent: 'space-between', padding: '4px 0', borderBottom: '1px solid var(--color-line)', fontSize: 13 }}>
                    <span>{key.replace(/_/g, ' ')}:</span>
                    <strong style={{ fontFamily: 'var(--font-mono)' }}>{val}</strong>
                  </div>
                ))
              ) : (
                <div style={{ fontSize: 13, color: 'var(--color-ink-muted)' }}>No operation counters for this step.</div>
              )}
            </div>
          </div>
        )}

        {/* COMPLEXITY TAB */}
        {activeTab === 'complexity' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            {complexity ? (
              <>
                <div style={{ border: '1px solid var(--color-line)', padding: 12, borderRadius: 4, background: 'var(--color-paper)' }}>
                  <div style={{ fontSize: 12, color: 'var(--color-ink-muted)', marginBottom: 8, textTransform: 'uppercase', fontWeight: 600 }}>
                    Theoretical Complexity (Theory)
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', padding: '4px 0', fontSize: 13 }}>
                    <span>Best Time:</span>
                    <strong style={{ fontFamily: 'var(--font-mono)' }}>{complexity.best}</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', padding: '4px 0', fontSize: 13 }}>
                    <span>Average Time:</span>
                    <strong style={{ fontFamily: 'var(--font-mono)' }}>{complexity.average}</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', padding: '4px 0', fontSize: 13 }}>
                    <span>Worst Time:</span>
                    <strong style={{ fontFamily: 'var(--font-mono)' }}>{complexity.worst}</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', padding: '4px 0', fontSize: 13 }}>
                    <span>Space:</span>
                    <strong style={{ fontFamily: 'var(--font-mono)' }}>{complexity.space}</strong>
                  </div>
                </div>

                <div style={{ fontSize: 12, color: 'var(--color-ink-muted)', lineHeight: 1.4 }}>
                  Theoretical complexities are asymptotic big-O upper/lower bounds. Measured metrics reflect exact execution performance on current input.
                </div>
              </>
            ) : (
              <div style={{ fontSize: 13, color: 'var(--color-ink-muted)' }}>Select an algorithm to view theoretical complexity.</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
