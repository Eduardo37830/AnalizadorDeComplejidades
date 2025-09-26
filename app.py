from flask import Flask
from flask_smorest import Api
from config import Config
from api import create_api

def create_app():
    """Factory function para crear la aplicación Flask."""
    app = Flask(__name__)

    # Configuración
    app.config.from_object(Config)

    # Configuración de Flask-Smorest
    app.config['API_TITLE'] = 'Algoritmo Analyzer API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.2'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    # Crear e inicializar API
    create_api(app)

    @app.route('/')
    def hello_world():
        return {
            'message': 'Algoritmo Analyzer Flask API',
            'version': 'v1',
            'endpoints': {
                'health': '/v1/health',
                'analyze': '/v1/analyze',
                'analyze_stream': '/v1/analyze/stream',
                'docs': '/swagger-ui'
            }
        }

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
