from ..state import GraphState

def generate_diagrams(state: GraphState) -> GraphState:
    """Genera diagramas visuales del CFG y árbol de recursión."""
    try:
        cfg = state.get("cfg")
        complexity = state.get("complexity", {})
        pseudocode = state.get("pseudocode", "")

        diagrams = []

        # Generar descripción textual del flujo del algoritmo
        if pseudocode:
            diagram_text = f"""
## Diagrama de Flujo del Algoritmo

```
Pseudocódigo:
{pseudocode}
```

## Análisis de Complejidad:
- Complejidad temporal: {complexity.get('time', 'No determinada')}
- Descripción: {complexity.get('description', 'Análisis básico')}
"""
            diagrams.append(diagram_text)

        state["diagram"] = "\n".join(diagrams) if diagrams else "No se pudo generar diagrama"

    except Exception as e:
        state["errors"].append(f"Error generating diagrams: {str(e)}")
        state["diagram"] = "Error generando diagrama"

    return state
