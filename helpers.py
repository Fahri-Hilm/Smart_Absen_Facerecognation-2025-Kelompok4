"""
Helper functions for Smart Absen application
"""
from flask import jsonify
from datetime import datetime

def api_response(success=True, message='', data=None, status_code=200):
    """
    Standardized API response format
    
    Args:
        success (bool): Success status
        message (str): Response message
        data (any): Response data
        status_code (int): HTTP status code
    
    Returns:
        tuple: (jsonify response, status_code)
    """
    response = {
        'success': success,
        'status': 'success' if success else 'error',
        'message': message,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(response), status_code
