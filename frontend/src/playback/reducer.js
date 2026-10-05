export const INITIAL_STATE = {
  status: 'idle', // 'idle' | 'ready' | 'playing' | 'paused' | 'finished'
  steps: [],
  currentIndex: 0,
  speed: 1, // 0.25x, 0.5x, 1x, 2x, 4x
  autoPlay: false
};

export function playbackReducer(state, action) {
  switch (action.type) {
    case 'LOAD_TRACE':
      return {
        ...state,
        status: action.payload.steps && action.payload.steps.length > 0 ? 'ready' : 'idle',
        steps: action.payload.steps || [],
        currentIndex: 0,
        autoPlay: false
      };

    case 'PLAY':
      if (state.steps.length === 0) return state;
      if (state.currentIndex >= state.steps.length - 1) {
        // If at end, restart from beginning
        return { ...state, status: 'playing', currentIndex: 0, autoPlay: true };
      }
      return { ...state, status: 'playing', autoPlay: true };

    case 'PAUSE':
      return { ...state, status: 'paused', autoPlay: false };

    case 'STEP_FORWARD':
      if (state.steps.length === 0) return state;
      {
        const nextIdx = Math.min(state.currentIndex + 1, state.steps.length - 1);
        const isEnd = nextIdx === state.steps.length - 1;
        return {
          ...state,
          currentIndex: nextIdx,
          status: isEnd ? 'finished' : 'paused',
          autoPlay: false
        };
      }

    case 'STEP_BACKWARD':
      if (state.steps.length === 0) return state;
      return {
        ...state,
        currentIndex: Math.max(state.currentIndex - 1, 0),
        status: 'paused',
        autoPlay: false
      };

    case 'JUMP_TO':
      if (state.steps.length === 0) return state;
      {
        const idx = Math.max(0, Math.min(action.payload, state.steps.length - 1));
        const isEnd = idx === state.steps.length - 1;
        return {
          ...state,
          currentIndex: idx,
          status: isEnd ? 'finished' : 'paused',
          autoPlay: false
        };
      }

    case 'JUMP_TO_START':
      return {
        ...state,
        currentIndex: 0,
        status: 'ready',
        autoPlay: false
      };

    case 'JUMP_TO_END':
      if (state.steps.length === 0) return state;
      return {
        ...state,
        currentIndex: state.steps.length - 1,
        status: 'finished',
        autoPlay: false
      };

    case 'SET_SPEED':
      return { ...state, speed: action.payload };

    case 'TICK':
      if (state.status !== 'playing') return state;
      if (state.currentIndex >= state.steps.length - 1) {
        return { ...state, status: 'finished', autoPlay: false };
      }
      return { ...state, currentIndex: state.currentIndex + 1 };

    default:
      return state;
  }
}
