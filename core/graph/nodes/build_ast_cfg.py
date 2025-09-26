from ..state import GraphState

def build_structures(state: GraphState) -> GraphState:
    """Construye AST y CFG (Control Flow Graph) del código - implementación básica."""
    try:
        ast = state.get("ast")

        if ast and isinstance(ast, dict):
            # Construir CFG mock básico sin dependencias externas
            cfg = {
                "nodes": ["start", "end"],
                "edges": [("start", "end")],
                "entry": "start",
                "exit": "end",
                "loop_count": ast.get("loop_count", 0),
                "has_nested_loops": ast.get("loop_count", 0) > 1
            }

            # Si hay bucles, crear estructura más compleja
            if ast.get("has_loops", False):
                if ast.get("loop_count", 0) > 1:
                    # Bucles anidados
                    cfg["nodes"] = ["start", "outer_loop", "inner_loop", "end"]
                    cfg["edges"] = [
                        ("start", "outer_loop"),
                        ("outer_loop", "inner_loop"),
                        ("inner_loop", "inner_loop"),
                        ("inner_loop", "outer_loop"),
                        ("outer_loop", "end")
                    ]
                else:
                    # Un solo bucle
                    cfg["nodes"] = ["start", "loop", "end"]
                    cfg["edges"] = [("start", "loop"), ("loop", "loop"), ("loop", "end")]

            state["cfg"] = cfg
        else:
            state["errors"].append("No AST available to build CFG")
            state["cfg"] = None

    except Exception as e:
        state["errors"].append(f"Error building AST/CFG: {str(e)}")
        state["cfg"] = None

    return state
