import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { fetchAlgorithms, generateInput, runAlgorithm } from '../api/client';
import { usePlayback } from '../playback/usePlayback';

import Header from '../components/Header';
import InputPanel from '../components/InputPanel';
import TransportBar from '../components/TransportBar';
import Inspector from '../components/Inspector';
import Legend from '../components/Legend';

import ArrayStage from '../stages/ArrayStage';
import StringStage from '../stages/StringStage';
import DPTableStage from '../stages/DPTableStage';
import GraphStage from '../stages/GraphStage';
import GreedyStage from '../stages/GreedyStage';

export default function Lab() {
  const { algorithmId } = useParams();
  const [meta, setMeta] = useState(null);
  const [inputData, setInputData] = useState(null);
  const [runResult, setRunResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const playback = usePlayback();

  // Load Metadata & default preset
  useEffect(() => {
    fetchAlgorithms().then(allMeta => {
      const found = allMeta.find(a => a.id === algorithmId);
      if (found) {
        setMeta(found);
        const defaultPreset = found.presets && found.presets.length > 0 ? found.presets[0].input : {};
        setInputData(defaultPreset);
        // Auto run default preset
        executeRun(found.id, defaultPreset);
      }
    }).catch(err => {
      setError(err.message);
    });
  }, [algorithmId]);

  const executeRun = async (algId, inp) => {
    setLoading(true);
    setError(null);
    try {
      const res = await runAlgorithm(algId, inp);
      setRunResult(res);
      playback.loadTrace(res.steps);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleGenerateRandom = async () => {
    if (!meta) return;
    try {
      const generated = await generateInput(meta.id, 10);
      setInputData(generated);
      executeRun(meta.id, generated);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleSelectPreset = (presetName) => {
    if (!meta) return;
    const found = meta.presets.find(p => p.name === presetName);
    if (found) {
      setInputData(found.input);
      executeRun(meta.id, found.input);
    }
  };

  const handleRun = () => {
    if (meta && inputData) {
      executeRun(meta.id, inputData);
    }
  };

  // Render appropriate visualizer stage
  const renderStage = () => {
    if (!meta) return null;
    const stageType = meta.stage;
    const currentStep = playback.currentStep;

    switch (stageType) {
      case 'array':
        return <ArrayStage step={currentStep} />;
      case 'string':
        return <StringStage step={currentStep} />;
      case 'dp':
        return <DPTableStage step={currentStep} />;
      case 'graph':
        return <GraphStage step={currentStep} />;
      case 'greedy':
        return <GreedyStage step={currentStep} />;
      default:
        return <ArrayStage step={currentStep} />;
    }
  };

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', background: 'var(--color-paper)', overflow: 'hidden' }}>
      <Header algorithmName={meta?.name} category={meta?.category} />

      {/* Main Workbench Layout */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Left Input Panel */}
        <InputPanel
          meta={meta}
          inputData={inputData}
          onInputChange={setInputData}
          onGenerateRandom={handleGenerateRandom}
          onSelectPreset={handleSelectPreset}
          onRun={handleRun}
          isLoading={loading}
          error={error}
        />

        {/* Center Stage & Visualizer */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', padding: 16 }}>
          {/* Visualizer Container */}
          <div style={{
            flex: 1,
            border: '1px solid var(--color-line)',
            borderRadius: 'var(--radius)',
            background: 'var(--color-paper)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            overflow: 'hidden',
            position: 'relative'
          }}>
            {renderStage()}
          </div>

          {/* Plain English Step Message Banner */}
          <div style={{
            margin: '12px 0 8px 0',
            padding: '10px 16px',
            background: 'var(--color-paper)',
            border: '1px solid var(--color-line)',
            borderRadius: 'var(--radius)',
            fontFamily: 'var(--font-mono)',
            fontSize: 13,
            color: 'var(--color-ink)',
            minHeight: 42,
            display: 'flex',
            alignItems: 'center'
          }} aria-live="polite">
            <strong>Step Message:&nbsp;</strong>
            <span>{playback.currentStep?.message || 'Ready. Click play or step to visualize.'}</span>
          </div>

          {/* Color Legend */}
          <Legend />
        </div>

        {/* Right Inspector */}
        <Inspector
          steps={playback.state.steps}
          currentIndex={playback.state.currentIndex}
          metrics={runResult?.metrics}
          complexity={meta?.complexity}
          onJumpToStep={playback.jumpTo}
        />
      </div>

      {/* Bottom Transport Bar */}
      <TransportBar
        playbackState={playback.state}
        onPlay={playback.play}
        onPause={playback.pause}
        onStepForward={playback.stepForward}
        onStepBackward={playback.stepBackward}
        onJumpStart={playback.jumpToStart}
        onJumpEnd={playback.jumpToEnd}
        onJumpTo={playback.jumpTo}
        onSetSpeed={playback.setSpeed}
      />
    </div>
  );
}
