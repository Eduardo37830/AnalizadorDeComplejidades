from ..state import GraphState

def validate_and_repair(state: GraphState) -> GraphState:
    """Valida la sintaxis del código y repara automáticamente errores comunes - implementación básica."""
    try:
        pseudocode = state.get("pseudocode", "")

        # Validación básica sin dependencias externas
        if not pseudocode.strip():
            state["errors"].append("Pseudocódigo vacío")
            return state

        # Validaciones básicas de sintaxis Pascal
        errors = []

        # Verificar que los bloques begin/end estén balanceados
        begin_count = pseudocode.lower().count("begin")
        end_count = pseudocode.lower().count("end")

        if begin_count != end_count:
            errors.append("Bloques begin/end no balanceados")
            # Reparación básica: agregar end faltantes
            if begin_count > end_count:
                missing_ends = begin_count - end_count
                state["pseudocode"] = pseudocode + "\n" + "end " * missing_ends
                state["errors"].append(f"Reparado: agregados {missing_ends} 'end' faltantes")

        # Verificar sintaxis básica de for loops
        if "for" in pseudocode.lower() and "do" not in pseudocode.lower():
            errors.append("For loop sin 'do'")

        if len(errors) == 0:
            # Sin errores de sintaxis
            pass
        else:
            state["errors"].extend([f"Validación: {error}" for error in errors])

    except Exception as e:
        state["errors"].append(f"Error in validation: {str(e)}")

    return state
