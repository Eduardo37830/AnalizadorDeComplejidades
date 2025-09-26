from ..state import GraphState

def analyze_cases(state: GraphState) -> GraphState:
    """Analiza los casos best, worst y average del algoritmo - implementación básica."""
    try:
        complexity = state.get("complexity", {})
        pseudocode = state.get("pseudocode", "")

        if complexity:
            time_complexity = complexity.get("time", "O(1)")

            # Análisis básico de casos basado en patrones conocidos
            cases = {
                "best": time_complexity,
                "worst": time_complexity,
                "average": time_complexity
            }

            # Análisis más específico para algunos algoritmos conocidos
            if "for" in pseudocode.lower() and pseudocode.lower().count("for") >= 2:
                # Bucles anidados - típicamente Selection Sort, Bubble Sort, etc.
                cases = {
                    "best": "O(n²)",
                    "worst": "O(n²)",
                    "average": "O(n²)"
                }
            elif "for" in pseudocode.lower() or "while" in pseudocode.lower():
                # Un solo bucle
                cases = {
                    "best": "O(n)",
                    "worst": "O(n)",
                    "average": "O(n)"
                }
            else:
                # Sin bucles detectados
                cases = {
                    "best": "O(1)",
                    "worst": "O(1)",
                    "average": "O(1)"
                }

            state["cases"] = cases
        else:
            state["errors"].append("No hay información de complejidad para análisis de casos")
            state["cases"] = {
                "best": "No determinado",
                "worst": "No determinado",
                "average": "No determinado"
            }

    except Exception as e:
        state["errors"].append(f"Error analyzing cases: {str(e)}")

    return state
