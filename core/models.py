from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CounterDef(BaseModel):
    id: str
    name: str
    description: str


class PresetDef(BaseModel):
    name: str
    label: str
    input: Dict[str, Any]


class InputSchemaDef(BaseModel):
    kind: str  # "array", "searching", "string", "dp_knapsack", "dp_lcs", "dp_lis", "dp_mcm", "dp_edit_distance", "graph", "greedy_activity", "greedy_knapsack", "greedy_huffman", "greedy_jobs"
    description: str
    fields: Dict[str, Any]


class AlgorithmMetadata(BaseModel):
    id: str
    name: str
    category: str  # "Sorting", "Searching", "String matching", "Dynamic programming", "Graph: traversal", "Graph: shortest paths", "Graph: spanning trees", "Greedy"
    compare_group: Optional[str] = None  # "Sorting", "Searching", "String matching", "Traversal", "Shortest path", "Minimum spanning tree", None
    stage: str  # "array", "string", "dp", "graph", "greedy"
    description: str
    complexity: Dict[str, str]  # best, average, worst, space
    input_schema: InputSchemaDef
    presets: List[PresetDef]
    max_visual_size: int
    max_benchmark_size: int
    counters: List[str]


class StepEvent(BaseModel):
    type: str
    message: str
    state: Dict[str, Any]
    counters: Dict[str, int] = Field(default_factory=dict)


class StepSnapshot(BaseModel):
    index: int
    type: str
    message: str
    state: Dict[str, Any]
    counters: Dict[str, int]


class PerformanceMetrics(BaseModel):
    execution_time_ms: float
    memory_kb: float
    operations: Dict[str, int]
    is_timing_reliable: bool = True
    timing_note: Optional[str] = None


class RunResult(BaseModel):
    algorithm_id: str
    algorithm_name: str
    input: Dict[str, Any]
    output: Any
    solution: Optional[Any] = None
    steps: List[StepSnapshot]
    total_steps: int
    metrics: PerformanceMetrics


class ComparePoint(BaseModel):
    size: int
    time_ms: Optional[float] = None
    memory_kb: Optional[float] = None
    operations: Optional[Dict[str, int]] = None
    skipped: bool = False
    skip_reason: Optional[str] = None


class CompareSeries(BaseModel):
    algorithm_id: str
    algorithm_name: str
    points: List[ComparePoint]


class CompareResponse(BaseModel):
    group: str
    metrics: List[str]
    series: Dict[str, CompareSeries]
