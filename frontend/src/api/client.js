const API_BASE = '/api';

export async function fetchAlgorithms() {
  const res = await fetch(`${API_BASE}/algorithms`);
  if (!res.ok) throw new Error('Failed to fetch algorithm metadata');
  return res.json();
}

export async function generateInput(algorithm_id, size = 10, preset_name = null, input_type = 'random') {
  const res = await fetch(`${API_BASE}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ algorithm_id, size, preset_name, input_type })
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error?.message || 'Failed to generate input');
  }
  return data.input;
}

export async function runAlgorithm(algorithm_id, input) {
  const res = await fetch(`${API_BASE}/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ algorithm_id, input })
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error?.message || 'Failed to run algorithm execution');
  }
  return data;
}

export async function compareAlgorithms(group, algorithm_ids, input_kind, sizes, repeats = 3, seed = 42) {
  const res = await fetch(`${API_BASE}/compare`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ group, algorithm_ids, input_kind, sizes, repeats, seed })
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error?.message || 'Failed to run comparison benchmark');
  }
  return data;
}
