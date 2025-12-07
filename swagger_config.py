"""
Swagger UI Configuration for Smart Absen API Documentation
"""
from flask_swagger_ui import get_swaggerui_blueprint

# Swagger UI configuration
SWAGGER_URL = '/api/docs'  # URL untuk akses Swagger UI
API_URL = '/static/openapi.yaml'  # Path ke OpenAPI spec file

def setup_swagger(app):
    """Setup Swagger UI blueprint"""
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Smart Absen API",
            'docExpansion': 'list',
            'defaultModelsExpandDepth': 3,
            'displayRequestDuration': True,
            'filter': True,
            'syntaxHighlight.theme': 'monokai'
        }
    )
    
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    print(f"📚 Swagger UI available at: http://localhost:5001{SWAGGER_URL}")
