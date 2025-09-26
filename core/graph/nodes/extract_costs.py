from ..state import GraphState
from utils.complexity import extract_cost_model

def extract_cost_model(state: GraphState) -> GraphState:
    """Extrae el modelo de costos del CFG."""
    try:
        cfg = state["cfg"]

        if cfg:
            # Extraer modelo de costos
            complexity_info = extract_cost_model(cfg)
            state["complexity"].update(complexity_info)
        else:
            state["errors"].append("No CFG available to extract costs")

    except Exception as e:
        state["errors"].append(f"Error extracting costs: {str(e)}")

    return state
