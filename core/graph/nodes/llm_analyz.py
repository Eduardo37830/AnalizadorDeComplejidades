from ..state import GraphState

def llm_analysis(state: GraphState) -> GraphState:
    """Análisis final usando LLM para generar explicaciones y reporte."""
    try:
        complexity = state.get("complexity", {})
        cases = state.get("cases", {})
        tight_bound = state.get("tight_bound", "")
        diagram = state.get("diagram", "")
        pseudocode = state.get("pseudocode", "")

        # Generar reporte final en markdown
        report = f"""# Análisis de Complejidad Algorítmica

## Algoritmo Analizado
```
{pseudocode}
```

## Complejidad Temporal
- **Complejidad**: {complexity.get('time', 'No determinada')}
- **Descripción**: {complexity.get('description', 'Análisis automático')}

## Análisis por Casos
- **Mejor caso**: {cases.get('best', 'No determinado')}
- **Peor caso**: {cases.get('worst', 'No determinado')}
- **Caso promedio**: {cases.get('average', 'No determinado')}

## Cota Ajustada
{tight_bound}

## Diagramas
{diagram}

## Conclusión
El algoritmo analizado tiene una complejidad de {complexity.get('time', 'tiempo indeterminado')}.
"""

        state["report"] = report

    except Exception as e:
        state["errors"].append(f"Error in LLM analysis: {str(e)}")
        state["report"] = "Error generando reporte final"

    return state

