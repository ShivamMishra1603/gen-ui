import logging
import logging.handlers
import os
from datetime import datetime


def setup_logger():
    """Configure and return the application logger."""
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('genui')
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation (10MB max, keep 5 files)
    log_file = os.path.join(logs_dir, 'genui.log')
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Error file handler (separate file for errors)
    error_log_file = os.path.join(logs_dir, 'genui_errors.log')
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    return logger


def log_request_info(logger, request, additional_info=None):
    """Log incoming request information."""
    info = {
        'method': request.method,
        'path': request.path,
        'remote_addr': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown')[:100],  # Truncate long user agents
    }
    
    if additional_info:
        info.update(additional_info)
    
    # Don't log sensitive data like API keys
    if 'api_key' in info:
        info['api_key'] = '***masked***'
    
    logger.info(f"Request: {info}")


def log_response_info(logger, status_code, duration_ms, additional_info=None):
    """Log response information."""
    info = {
        'status_code': status_code,
        'duration_ms': round(duration_ms, 2)
    }
    
    if additional_info:
        info.update(additional_info)
    
    log_level = logging.INFO
    if status_code >= 400:
        log_level = logging.WARNING
    if status_code >= 500:
        log_level = logging.ERROR
    
    logger.log(log_level, f"Response: {info}")


def mask_sensitive_data(data):
    """Mask sensitive information in log data."""
    if isinstance(data, dict):
        masked = data.copy()
        sensitive_keys = ['api_key', 'key', 'token', 'password', 'secret']
        for key in masked:
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                masked[key] = '***masked***'
        return masked
    return data
