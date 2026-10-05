import { useReducer, useEffect, useCallback } from 'react';
import { playbackReducer, INITIAL_STATE } from './reducer';

export function usePlayback(initialSteps = []) {
  const [state, dispatch] = useReducer(playbackReducer, {
    ...INITIAL_STATE,
    steps: initialSteps,
    status: initialSteps.length > 0 ? 'ready' : 'idle'
  });

  const loadTrace = useCallback((steps) => {
    dispatch({ type: 'LOAD_TRACE', payload: { steps } });
  }, []);

  const play = useCallback(() => dispatch({ type: 'PLAY' }), []);
  const pause = useCallback(() => dispatch({ type: 'PAUSE' }), []);
  const stepForward = useCallback(() => dispatch({ type: 'STEP_FORWARD' }), []);
  const stepBackward = useCallback(() => dispatch({ type: 'STEP_BACKWARD' }), []);
  const jumpTo = useCallback((index) => dispatch({ type: 'JUMP_TO', payload: index }), []);
  const jumpToStart = useCallback(() => dispatch({ type: 'JUMP_TO_START' }), []);
  const jumpToEnd = useCallback(() => dispatch({ type: 'JUMP_TO_END' }), []);
  const setSpeed = useCallback((speed) => dispatch({ type: 'SET_SPEED', payload: speed }), []);

  // Tick timer interval
  useEffect(() => {
    if (state.status !== 'playing') return;

    const baseInterval = 400; // 1x = 400ms per step
    const interval = baseInterval / state.speed;

    const timer = setInterval(() => {
      dispatch({ type: 'TICK' });
    }, interval);

    return () => clearInterval(timer);
  }, [state.status, state.speed]);

  // Keyboard navigation shortcuts (PRD Section 6.3)
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Don't override if typing in an input
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName)) return;

      if (e.code === 'Space') {
        e.preventDefault();
        if (state.status === 'playing') pause();
        else play();
      } else if (e.code === 'ArrowLeft') {
        e.preventDefault();
        stepBackward();
      } else if (e.code === 'ArrowRight') {
        e.preventDefault();
        stepForward();
      } else if (e.code === 'Home') {
        e.preventDefault();
        jumpToStart();
      } else if (e.code === 'End') {
        e.preventDefault();
        jumpToEnd();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [state.status, play, pause, stepForward, stepBackward, jumpToStart, jumpToEnd]);

  const currentStep = state.steps[state.currentIndex] || null;

  return {
    state,
    currentStep,
    loadTrace,
    play,
    pause,
    stepForward,
    stepBackward,
    jumpTo,
    jumpToStart,
    jumpToEnd,
    setSpeed
  };
}
