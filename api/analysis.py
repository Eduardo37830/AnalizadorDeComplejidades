from flask import request, jsonify
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from core.services import run_analysis
from core.graph.nodes.nl_to_pseud import convert_to_pseudocode

blp = Blueprint('analysis', 'analysis', url_prefix='/v1')

class AnalysisRequestSchema(Schema):
    pseudocode = fields.Str(required=True, description="Pseudocódigo a analizar")

class PseudocodeProcessRequestSchema(Schema):
    text = fields.Str(required=True, description="Texto a procesar (lenguaje natural o pseudocódigo)")

class PseudocodeProcessResponseSchema(Schema):
    original_text = fields.Str(description="Texto original enviado")
    processed_pseudocode = fields.Str(description="Pseudocódigo procesado por el LLM")
    errors = fields.List(fields.Str(), description="Errores durante el procesamiento")
    llm_used = fields.Bool(description="Si se usó el LLM local")

class AnalysisResponseSchema(Schema):
    complexity = fields.Dict(description="Análisis de complejidad")
    diagram = fields.Str(description="Diagrama generado")
    report = fields.Str(description="Reporte en markdown")
    cases = fields.Dict(description="Análisis por casos")
    tight_bound = fields.Str(description="Cota ajustada")
    errors = fields.List(fields.Str(), description="Errores encontrados")

@blp.route('/health')
def health():
    """Endpoint de salud del servicio."""
    return {'status': 'healthy', 'service': 'algo-analyzer-flask'}

@blp.route('/pseudocode/process', methods=['POST'])
@blp.arguments(PseudocodeProcessRequestSchema)
@blp.response(200, PseudocodeProcessResponseSchema)
def process_pseudocode(args):
    """
    Procesa texto usando el LLM local para convertir lenguaje natural a pseudocódigo
    o corregir pseudocódigo existente.
    """
    try:
        # Crear un estado mock para probar solo el nodo del LLM
        mock_state = {
            "pseudocode": args['text'],
            "code": "",
            "errors": [],
            "language": "pseudocode"
        }

        # Procesar con el LLM
        result_state = convert_to_pseudocode(mock_state)

        return {
            "original_text": args['text'],
            "processed_pseudocode": result_state.get("pseudocode", ""),
            "errors": result_state.get("errors", []),
            "llm_used": len(result_state.get("errors", [])) == 0
        }
    except Exception as e:
        abort(500, message=f"Error procesando pseudocódigo: {str(e)}")

@blp.route('/analyze', methods=['POST'])
@blp.arguments(AnalysisRequestSchema)
@blp.response(200, AnalysisResponseSchema)
def analyze(args):
    """Analiza pseudocódigo y devuelve complejidad algorítmica."""
    try:
        result = run_analysis(args['pseudocode'])
        return result
    except Exception as e:
        abort(500, message=str(e))

@blp.route('/analyze/stream', methods=['POST'])
@blp.arguments(AnalysisRequestSchema)
def analyze_stream(args):
    """Análisis con streaming de respuesta."""
    # Implementar streaming con Server-Sent Events
    return analyze(args)
