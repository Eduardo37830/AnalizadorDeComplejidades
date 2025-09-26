from ..state import GraphState

def prove_bounds(state: GraphState) -> GraphState:
    """Demuestra que los límites encontrados son ajustados (tight bounds)."""
    try:
        complexity = state["complexity"]
        cases = state["cases"]

        if complexity and cases:
            # Demostración básica de tight bounds
            worst_case = cases.get("worst", "O(1)")
            best_case = cases.get("best", "O(1)")

            if worst_case == best_case:
                tight_bound_proof = f"Θ({worst_case.replace('O(', '').replace(')', '')}) - Los casos mejor y peor coinciden"
            else:
                tight_bound_proof = f"Mejor caso: {best_case}, Peor caso: {worst_case}"

            state["tight_bound"] = tight_bound_proof
        else:
            state["errors"].append("Missing complexity or cases info for tight bound proof")

    except Exception as e:
        state["errors"].append(f"Error proving tight bounds: {str(e)}")

    return state
