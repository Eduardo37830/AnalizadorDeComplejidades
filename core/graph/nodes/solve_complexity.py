from ..state import GraphState

def solve_recurrence(state: GraphState) -> GraphState:
    """Resuelve las relaciones de recurrencia encontradas."""
    try:
        complexity = state["complexity"]

        if "recurrence_relation" in complexity:
            # Implementación básica - por ahora asumimos que ya tenemos la solución
            solution = complexity.get("time", "O(n)")
            state["complexity"]["solution"] = solution
            state["recurrence"] = str(solution)
        else:
            # Si no hay recurrencia, usar el análisis de complejidad existente
            time_complexity = complexity.get("time", "O(1)")
            state["recurrence"] = time_complexity

    except Exception as e:
        state["errors"].append(f"Error solving recurrence: {str(e)}")

    return state
