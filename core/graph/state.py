from typing import Dict, List, Any, Optional
from typing_extensions import TypedDict

class GraphState(TypedDict):
    """Estado compartido del grafo de análisis."""

    # Input
    code: str
    language: str

    # Processing stages
    pseudocode: str
    ast: Optional[Any]
    cfg: Optional[Any]

    # Analysis results
    complexity: Dict[str, Any]
    recurrence: str
    cases: Dict[str, str]  # best, worst, average
    tight_bound: str

    # Output
    diagram: str
    report: str

    # Error handling
    errors: List[str]
