import React from 'react';
import {
  Play, Pause, SkipBack, SkipForward, ChevronLeft, ChevronRight
} from 'lucide-react';

export default function TransportBar({
  playbackState,
  onPlay,
  onPause,
  onStepForward,
  onStepBackward,
  onJumpStart,
  onJumpEnd,
  onJumpTo,
  onSetSpeed
}) {
  const { status, steps, currentIndex, speed } = playbackState;
  const totalSteps = steps.length;
  const isPlaying = status === 'playing';

  const handleScrub = (e) => {
    const val = parseInt(e.target.value, 10);
    onJumpTo(val);
  };

  const speeds = [0.25, 0.5, 1, 2, 4];

  return (
    <div style={{
      height: 64,
      borderTop: '1px solid var(--color-line)',
      background: 'var(--color-paper)',
      display: 'flex',
      alignItems: 'center',
      padding: '0 20px',
      gap: 16,
      zIndex: 10
    }}>
      {/* Control Buttons */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        <button title="Jump to Start (Home)" onClick={onJumpStart} disabled={totalSteps === 0}>
          <SkipBack size={16} />
        </button>
        <button title="Step Backward (←)" onClick={onStepBackward} disabled={totalSteps === 0 || currentIndex === 0}>
          <ChevronLeft size={16} />
        </button>

        {isPlaying ? (
          <button title="Pause (Space)" onClick={onPause} className="btn-primary" style={{ padding: '6px 16px' }}>
            <Pause size={18} />
          </button>
        ) : (
          <button title="Play (Space)" onClick={onPlay} className="btn-primary" style={{ padding: '6px 16px' }} disabled={totalSteps === 0}>
            <Play size={18} />
          </button>
        )}

        <button title="Step Forward (→)" onClick={onStepForward} disabled={totalSteps === 0 || currentIndex >= totalSteps - 1}>
          <ChevronRight size={16} />
        </button>
        <button title="Jump to End (End)" onClick={onJumpEnd} disabled={totalSteps === 0}>
          <SkipForward size={16} />
        </button>
      </div>

      {/* Scrubber Timeline */}
      <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 12 }}>
        <input
          type="range"
          min="0"
          max={Math.max(0, totalSteps - 1)}
          value={currentIndex}
          onChange={handleScrub}
          disabled={totalSteps === 0}
          style={{
            flex: 1,
            height: 6,
            accentColor: 'var(--color-rose-deep)',
            cursor: totalSteps > 0 ? 'pointer' : 'not-allowed'
          }}
        />
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: 13, color: 'var(--color-ink)', minWidth: 100, textAlign: 'right' }}>
          Step {totalSteps > 0 ? currentIndex + 1 : 0} / {totalSteps}
        </span>
      </div>

      {/* Speed Selector */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
        <span style={{ fontSize: 12, color: 'var(--color-ink-muted)', marginRight: 4 }}>Speed:</span>
        {speeds.map((s) => (
          <button
            key={s}
            onClick={() => onSetSpeed(s)}
            style={{
              padding: '2px 8px',
              fontSize: 12,
              fontFamily: 'var(--font-mono)',
              background: speed === s ? 'var(--color-almond-silk)' : 'transparent',
              borderColor: speed === s ? 'var(--color-camel)' : 'var(--color-line)',
              fontWeight: speed === s ? '600' : '400'
            }}
          >
            {s}x
          </button>
        ))}
      </div>
    </div>
  );
}
