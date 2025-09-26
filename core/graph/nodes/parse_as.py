from ..state import GraphState
from utils.parsing import parse_code_to_ast

def parse_code(state: GraphState) -> GraphState:
    """Parsea el código a AST."""
    try:
        pseudocode = state["pseudocode"]
        language = state["language"]

        ast = parse_code_to_ast(pseudocode, language)
        state["ast"] = ast

    except Exception as e:
        state["errors"].append(f"Error parsing code: {str(e)}")

    return state
