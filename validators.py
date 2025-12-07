"""
Input validation decorators for API endpoints
"""
from functools import wraps
from flask import request
from helpers import api_response
import re

def validate_employee_data(f):
    """Validate employee data in request"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json() or request.form.to_dict()
        
        # Required fields
        required = ['employee_name', 'employee_id']
        for field in required:
            if not data.get(field):
                return api_response(False, f'{field} is required', status_code=400)
        
        # Validate employee_id format (alphanumeric only)
        if not re.match(r'^[a-zA-Z0-9_-]+$', str(data['employee_id'])):
            return api_response(False, 'Invalid employee_id format', status_code=400)
        
        # Validate name (letters, spaces, and common characters)
        if not re.match(r'^[a-zA-Z\s\'-]+$', data['employee_name']):
            return api_response(False, 'Invalid employee_name format', status_code=400)
            
        return f(*args, **kwargs)
    return decorated_function

def validate_attendance_data(f):
    """Validate attendance data in request"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.form.to_dict()
        
        # Validate mode
        if data.get('mode') not in ['masuk', 'pulang']:
            return api_response(False, 'Invalid mode. Must be "masuk" or "pulang"', status_code=400)
        
        return f(*args, **kwargs)
    return decorated_function

def validate_json(f):
    """Ensure request has JSON content type"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return api_response(False, 'Content-Type must be application/json', status_code=400)
        return f(*args, **kwargs)
    return decorated_function
