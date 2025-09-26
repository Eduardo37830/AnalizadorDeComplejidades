from flask_smorest import Api
from flask import Blueprint

def create_api(app):
    """Crea la instancia de API y registra los blueprints."""
    api = Api(app)

    # Importar y registrar blueprints
    from .analysis import blp as analysis_blp
    api.register_blueprint(analysis_blp)

    return api
