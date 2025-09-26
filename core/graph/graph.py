from langgraph.graph import StateGraph, END
from .state import GraphState
from .nodes import (
    nl_to_pseud, parse_as, validate_syntax, build_ast_cfg,
    extract_costs, solve_complexity, split_cases, prove_tight_bound,
    diagram, llm_analyz
)

def should_continue_after_llm(state: GraphState) -> str:
    """Decide si continuar después del procesamiento LLM o terminar con error."""
    if len(state.get("errors", [])) > 0:
        # Si hay errores críticos del LLM, ir directo al reporte de error
        critical_errors = [e for e in state["errors"] if "conexión" in e.lower() or "inesperado" in e.lower()]
        if critical_errors:
            return "error_report"
    return "parse_as"

def should_continue_after_parsing(state: GraphState) -> str:
    """Decide si continuar después del parsing o intentar reparación."""
    if state.get("ast") is None:
        # Si no se pudo generar AST, ir a validación para intentar reparar
        return "validate_syntax"
    return "build_ast_cfg"

def should_continue_after_validation(state: GraphState) -> str:
    """Decide si continuar después de validación o reportar error."""
    # Intentar parsing nuevamente después de reparación
    if state.get("ast") is None:
        return "parse_as_retry"
    return "build_ast_cfg"

def should_continue_after_cfg(state: GraphState) -> str:
    """Decide si continuar con análisis completo o simplificado."""
    if state.get("cfg") is None:
        # Sin CFG, hacer análisis simplificado
        return "simple_analysis"
    return "extract_costs"

def should_continue_after_costs(state: GraphState) -> str:
    """Decide si hacer análisis de recurrencias o casos simples."""
    complexity = state.get("complexity", {})
    if "recurrence_relation" in complexity:
        return "solve_complexity"
    else:
        # Sin recurrencia, ir directo a análisis de casos
        return "split_cases"

def create_error_report(state: GraphState) -> GraphState:
    """Crea un reporte de error cuando el procesamiento falla."""
    state["report"] = f"""# Error en el Análisis

## Errores Encontrados:
{chr(10).join(f"- {error}" for error in state.get("errors", []))}

## Texto Original:
```
{state.get("pseudocode", "No disponible")}
```

No fue posible completar el análisis de complejidad debido a los errores mencionados.
"""
    return state

def create_simple_analysis(state: GraphState) -> GraphState:
    """Crea un análisis simplificado cuando no se puede construir CFG."""
    pseudocode = state.get("pseudocode", "")

    # Análisis básico por patrones de texto
    simple_complexity = {}
    if "for" in pseudocode.lower() and "for" in pseudocode.lower()[pseudocode.lower().find("for")+10:]:
        simple_complexity["time"] = "O(n²)"
        simple_complexity["description"] = "Bucles anidados detectados"
    elif "for" in pseudocode.lower() or "while" in pseudocode.lower():
        simple_complexity["time"] = "O(n)"
        simple_complexity["description"] = "Bucle simple detectado"
    else:
        simple_complexity["time"] = "O(1)"
        simple_complexity["description"] = "Operaciones constantes"

    state["complexity"] = simple_complexity
    state["cases"] = {
        "best": simple_complexity["time"],
        "worst": simple_complexity["time"],
        "average": simple_complexity["time"]
    }

    return state

def parse_as_retry(state: GraphState) -> GraphState:
    """Segundo intento de parsing después de reparación."""
    return parse_as.parse_code(state)

def create_analysis_graph():
    """Construye el grafo de análisis de complejidad algorítmica - VERSIÓN SIMPLIFICADA PARA DEBUG."""

    workflow = StateGraph(GraphState)

    # Agregar solo los nodos principales sin conditional edges
    workflow.add_node("nl_to_pseud", nl_to_pseud.convert_to_pseudocode)
    workflow.add_node("parse_as", parse_as.parse_code)
    workflow.add_node("validate_syntax", validate_syntax.validate_and_repair)
    workflow.add_node("build_ast_cfg", build_ast_cfg.build_structures)
    workflow.add_node("extract_costs", extract_costs.extract_cost_model)
    workflow.add_node("solve_complexity", solve_complexity.solve_recurrence)
    workflow.add_node("split_cases", split_cases.analyze_cases)
    workflow.add_node("prove_tight_bound", prove_tight_bound.prove_bounds)
    workflow.add_node("generate_diagram", diagram.generate_diagrams)
    workflow.add_node("llm_analyz", llm_analyz.llm_analysis)

    # Definir punto de entrada
    workflow.set_entry_point("nl_to_pseud")

    # FLUJO LINEAL SIMPLE - SIN CONDITIONAL EDGES
    workflow.add_edge("nl_to_pseud", "parse_as")
    workflow.add_edge("parse_as", "validate_syntax")
    workflow.add_edge("validate_syntax", "build_ast_cfg")
    workflow.add_edge("build_ast_cfg", "extract_costs")
    workflow.add_edge("extract_costs", "solve_complexity")
    workflow.add_edge("solve_complexity", "split_cases")
    workflow.add_edge("split_cases", "prove_tight_bound")
    workflow.add_edge("prove_tight_bound", "generate_diagram")
    workflow.add_edge("generate_diagram", "llm_analyz")
    workflow.add_edge("llm_analyz", END)

    return workflow.compile()
