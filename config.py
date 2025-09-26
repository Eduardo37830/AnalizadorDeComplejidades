import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración base de la aplicación Flask."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # API limits
    MAX_REQUEST_SIZE = int(os.getenv('MAX_REQUEST_SIZE', '1048576'))  # 1MB
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))
    
    # Analysis settings
    MAX_CODE_LENGTH = int(os.getenv('MAX_CODE_LENGTH', '10000'))
    TIMEOUT_SECONDS = int(os.getenv('TIMEOUT_SECONDS', '300'))