import React, { useState, useEffect } from 'react';
import { Play, Shuffle, Bookmark, AlertCircle } from 'lucide-react';

export default function InputPanel({
  meta,
  inputData,
  onInputChange,
  onGenerateRandom,
  onSelectPreset,
  onRun,
  isLoading,
  error
}) {
  const [arrayStr, setArrayStr] = useState('');
  const [targetVal, setTargetVal] = useState('');
  const [textStr, setTextStr] = useState('');
  const [patternStr, setPatternStr] = useState('');
  const [edgesStr, setEdgesStr] = useState('');
  const [startNode, setStartNode] = useState('');

  // Sync form controls with inputData
  useEffect(() => {
    if (!inputData) return;
    setArrayStr(inputData.array ? inputData.array.join(', ') : '');
    setTargetVal(inputData.target !== undefined ? String(inputData.target) : '');
    setTextStr(inputData.text !== undefined ? inputData.text : '');
    setPatternStr(inputData.pattern !== undefined ? inputData.pattern : '');
    setEdgesStr(inputData.edges !== undefined ? inputData.edges : '');
    setStartNode(inputData.start !== undefined ? inputData.start : '');
  }, [inputData]);

  if (!meta) return null;

  const kind = meta.input_schema?.kind;

  const handleArrayChange = (e) => {
    const val = e.target.value;
    setArrayStr(val);
    const parsed = val.split(',').map(s => parseInt(s.trim(), 10)).filter(n => !isNaN(n));
    onInputChange({ ...inputData, array: parsed });
  };

  const handleTargetChange = (e) => {
    const val = parseInt(e.target.value, 10);
    setTargetVal(e.target.value);
    onInputChange({ ...inputData, target: isNaN(val) ? 0 : val });
  };

  const handleTextChange = (e) => {
    const val = e.target.value;
    setTextStr(val);
    onInputChange({ ...inputData, text: val });
  };

  const handlePatternChange = (e) => {
    const val = e.target.value;
    setPatternStr(val);
    onInputChange({ ...inputData, pattern: val });
  };

  const handleEdgesChange = (e) => {
    const val = e.target.value;
    setEdgesStr(val);
    onInputChange({ ...inputData, edges: val });
  };

  return (
    <div style={{
      width: 280,
      borderRight: '1px solid var(--color-line)',
      background: 'var(--color-paper)',
      display: 'flex',
      flexDirection: 'column',
      padding: 16,
      gap: 16,
      height: '100%',
      overflowY: 'auto'
    }}>
      <div style={{ fontWeight: 600, fontSize: 14, color: 'var(--color-ink)' }}>Input Configuration</div>

      {/* Validation Error Banner */}
      {error && (
        <div style={{
          padding: 10,
          background: 'var(--color-almond-silk)',
          border: '1px solid var(--color-sweet-salmon)',
          borderRadius: 4,
          color: 'var(--color-rose-deep)',
          fontSize: 12,
          display: 'flex',
          gap: 6
        }}>
          <AlertCircle size={16} style={{ shrink: 0 }} />
          <div>{error}</div>
        </div>
      )}

      {/* Presets Selector */}
      {meta.presets && meta.presets.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <label style={{ fontSize: 12, color: 'var(--color-ink-muted)', display: 'flex', alignItems: 'center', gap: 4 }}>
            <Bookmark size={13} />
            <span>Preset Inputs:</span>
          </label>
          <select
            onChange={(e) => onSelectPreset(e.target.value)}
            defaultValue=""
            style={{
              padding: '8px 10px',
              borderRadius: 4,
              border: '1px solid var(--color-camel)',
              background: 'var(--color-ink)',
              color: '#ffffff',
              fontWeight: '500'
            }}
          >
            <option value="" disabled style={{ background: 'var(--color-ink)', color: '#ffffff' }}>Select a preset...</option>
            {meta.presets.map(p => (
              <option key={p.name} value={p.name} style={{ background: 'var(--color-ink)', color: '#ffffff' }}>{p.label}</option>
            ))}
          </select>
        </div>
      )}

      {/* Form Fields Based on Kind */}
      {kind === 'array' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
          <label style={{ fontSize: 12, color: 'var(--color-ink-muted)' }}>Array (comma-separated):</label>
          <input
            type="text"
            value={arrayStr}
            onChange={handleArrayChange}
            placeholder="e.g. 45, 12, 89, 34"
            style={{ padding: '8px 10px', border: '1px solid var(--color-camel)', borderRadius: 4, fontFamily: 'var(--font-mono)', background: 'var(--color-ink)', color: '#ffffff' }}
          />
        </div>
      )}

      {kind === 'searching' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <label style={{ fontSize: 12, color: 'var(--color-ink-muted)' }}>Array (comma-separated):</label>
            <input
              type="text"
              value={arrayStr}
              onChange={handleArrayChange}
              style={{ padding: '8px 10px', border: '1px solid var(--color-camel)', borderRadius: 4, fontFamily: 'var(--font-mono)', background: 'var(--color-ink)', color: '#ffffff' }}
            />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <label style={{ fontSize: 12, color: 'var(--color-ink-muted)' }}>Target Value:</label>
            <input
              type="number"
              value={targetVal}
              onChange={handleTargetChange}
              style={{ padding: '8px 10px', border: '1px solid var(--color-camel)', borderRadius: 4, fontFamily: 'var(--font-mono)', background: 'var(--color-ink)', color: '#ffffff' }}
            />
          </div>
        </div>
      )}

      {kind === 'string' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <label style={{ fontSize: 12, color: 'var(--color-ink-muted)' }}>Text:</label>
            <input
              type="text"
              value={textStr}
              onChange={handleTextChange}
              style={{ padding: '8px 10px', border: '1px solid var(--color-camel)', borderRadius: 4, fontFamily: 'var(--font-mono)', background: 'var(--color-ink)', color: '#ffffff' }}
            />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <label style={{ fontSize: 12, color: 'var(--color-ink-muted)' }}>Pattern:</label>
            <input
              type="text"
              value={patternStr}
              onChange={handlePatternChange}
              style={{ padding: '8px 10px', border: '1px solid var(--color-camel)', borderRadius: 4, fontFamily: 'var(--font-mono)', background: 'var(--color-ink)', color: '#ffffff' }}
            />
          </div>
        </div>
      )}

      {kind === 'graph' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <label style={{ fontSize: 12, color: 'var(--color-ink-muted)' }}>Edge List (A B 4):</label>
            <textarea
              rows={5}
              value={edgesStr}
              onChange={handleEdgesChange}
              style={{ padding: '8px 10px', border: '1px solid var(--color-camel)', borderRadius: 4, fontFamily: 'var(--font-mono)', fontSize: 12, background: 'var(--color-ink)', color: '#ffffff' }}
            />
          </div>
        </div>
      )}

      {/* Actions */}
      <div style={{ display: 'flex', gap: 8, marginTop: 'auto' }}>
        <button
          onClick={onGenerateRandom}
          disabled={isLoading}
          style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 4 }}
        >
          <Shuffle size={14} />
          <span>Random</span>
        </button>
        <button
          onClick={onRun}
          disabled={isLoading}
          className="btn-primary"
          style={{ flex: 1.2, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6 }}
        >
          <Play size={14} />
          <span>{isLoading ? 'Running...' : 'Run'}</span>
        </button>
      </div>
    </div>
  );
}
