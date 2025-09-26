from core.graph.graph import create_analysis_graph

# Crear el grafo una sola vez al importar el módulo
_analysis_graph = None

def get_analysis_graph():
    """Obtiene una instancia singleton del grafo de análisis."""
    global _analysis_graph
    if _analysis_graph is None:
        print("🔧 Construyendo grafo de análisis por primera vez...")
        _analysis_graph = create_analysis_graph()
        print("✅ Grafo de análisis construido y cached")
    return _analysis_graph

def run_analysis(pseudocode: str):
    """
    Ejecuta el análisis completo de complejidad algorítmica a partir de pseudocódigo.

    Args:
        pseudocode: Pseudocódigo a analizar

    Returns:
        dict: Resultado del análisis con complejidad, diagramas y reporte
    """
    # Obtener el grafo (se construye solo una vez)
    graph = get_analysis_graph()

    # Estado inicial - el pseudocódigo es la entrada principal
    initial_state = {
        "code": "",  # Se llenará después de procesar el pseudocódigo
        "language": "pseudocode",  # Siempre pseudocódigo
        "pseudocode": pseudocode,  # El pseudocódigo es la entrada principal
        "ast": None,
        "cfg": None,
        "complexity": {},
        "recurrence": "",
        "cases": {},
        "tight_bound": "",
        "diagram": "",
        "report": "",
        "errors": []
    }

    # Ejecutar el grafo
    result = graph.invoke(initial_state)

    # Empaquetar la respuesta
    return {
        "complexity": result.get("complexity", {}),
        "diagram": result.get("diagram", ""),
        "report": result.get("report", ""),
        "cases": result.get("cases", {}),
        "tight_bound": result.get("tight_bound", ""),
        "errors": result.get("errors", [])
    }
