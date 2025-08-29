from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import PIL.Image
import io
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from logger_config import setup_logger, log_request_info, log_response_info, mask_sensitive_data

load_dotenv()

app = Flask(__name__)
CORS(app)

# Setup logging
logger = setup_logger()
logger.info("GenUI Backend starting up...")

# Optional fallback API key from environment
FALLBACK_API_KEY = os.getenv('GOOGLE_API_KEY')

# Don't configure genai globally anymore - we'll do it per request

UI_GENERATION_PROMPT = os.getenv('UI_GENERATION_PROMPT')
if not UI_GENERATION_PROMPT:
    raise ValueError("UI_GENERATION_PROMPT not found in environment variables")

@app.route('/')
def home():
    start_time = time.time()
    log_request_info(logger, request)
    
    response_data = {"message": "GenUI Backend is running!", "timestamp": datetime.utcnow().isoformat()}
    duration_ms = (time.time() - start_time) * 1000
    log_response_info(logger, 200, duration_ms)
    
    return jsonify(response_data)

@app.route('/generate-ui', methods=['POST'])
def generate_ui():
    start_time = time.time()
    request_id = f"req_{int(time.time() * 1000)}"  # Simple request ID
    
    try:
        # Log request start
        log_request_info(logger, request, {
            'request_id': request_id,
            'has_image': 'image' in request.files,
            'has_api_key': bool(request.form.get('api_key'))
        })
        
        if 'image' not in request.files:
            duration_ms = (time.time() - start_time) * 1000
            log_response_info(logger, 400, duration_ms, {'request_id': request_id, 'error': 'No image file'})
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            duration_ms = (time.time() - start_time) * 1000
            log_response_info(logger, 400, duration_ms, {'request_id': request_id, 'error': 'No file selected'})
            return jsonify({"error": "No file selected"}), 400
        
        # Log file details
        logger.info(f"Processing file: {mask_sensitive_data({'request_id': request_id, 'filename': file.filename, 'content_type': file.content_type})}")
        
        # Get API key from form data or use fallback
        api_key = request.form.get('api_key')
        using_fallback = False
        if not api_key:
            api_key = FALLBACK_API_KEY
            using_fallback = True
        
        logger.info(f"API key source: {'fallback' if using_fallback else 'user_provided'} | Request ID: {request_id}")
        
        if not api_key:
            duration_ms = (time.time() - start_time) * 1000
            log_response_info(logger, 400, duration_ms, {'request_id': request_id, 'error': 'No API key'})
            return jsonify({"error": "API key is required. Please provide your Google AI API key or set up environment variables."}), 400
        
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
        file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if file_extension not in allowed_extensions:
            duration_ms = (time.time() - start_time) * 1000
            log_response_info(logger, 400, duration_ms, {'request_id': request_id, 'error': 'Invalid file type'})
            return jsonify({"error": "Invalid file type. Please upload an image file."}), 400
        
        # Read and process image
        image_bytes = file.read()
        image_size_mb = len(image_bytes) / (1024 * 1024)
        logger.info(f"Image processed: {{'request_id': '{request_id}', 'size_mb': {round(image_size_mb, 2)}, 'format': '{file_extension}'}}")
        
        img = PIL.Image.open(io.BytesIO(image_bytes))
        logger.info(f"PIL Image loaded: {{'request_id': '{request_id}', 'dimensions': '{img.size}', 'mode': '{img.mode}'}}")
        
        # Configure genai with the provided API key
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            logger.info(f"Gemini model configured successfully | Request ID: {request_id}")
        except Exception as e:
            logger.error(f"Failed to configure Gemini model: {str(e)} | Request ID: {request_id}")
            duration_ms = (time.time() - start_time) * 1000
            log_response_info(logger, 401, duration_ms, {'request_id': request_id, 'error': 'Invalid API key config'})
            return jsonify({"error": "Invalid API key. Please check your Google AI API key."}), 401
        
        # Generate UI code with Gemini
        logger.info(f"Starting Gemini API call | Request ID: {request_id}")
        gemini_start_time = time.time()
        app_metrics['gemini_calls_total'] += 1
        
        try:
            response = model.generate_content([UI_GENERATION_PROMPT, img])
            generated_code = response.text
            gemini_duration = (time.time() - gemini_start_time) * 1000
            app_metrics['gemini_calls_successful'] += 1
            
            logger.info(f"Gemini API call successful: {{'request_id': '{request_id}', 'gemini_duration_ms': {round(gemini_duration, 2)}, 'response_length': {len(generated_code)}}}")
            
        except Exception as e:
            gemini_duration = (time.time() - gemini_start_time) * 1000
            app_metrics['gemini_calls_failed'] += 1
            logger.error(f"Gemini API call failed: {{'request_id': '{request_id}', 'error': '{str(e)}', 'duration_ms': {round(gemini_duration, 2)}}}")
            
            if "API_KEY_INVALID" in str(e) or "invalid" in str(e).lower():
                duration_ms = (time.time() - start_time) * 1000
                log_response_info(logger, 401, duration_ms, {'request_id': request_id, 'error': 'Invalid API key call'})
                return jsonify({"error": "Invalid API key. Please check your Google AI API key and try again."}), 401
            else:
                raise e
        
        # Process generated code
        original_length = len(generated_code)
        if "```html" in generated_code:
            generated_code = generated_code.split("```html")[1].split("```")[0].strip()
        elif "```" in generated_code:
            generated_code = generated_code.split("```")[1].split("```")[0].strip()
        
        logger.info(f"Code processing complete: {{'request_id': '{request_id}', 'original_length': {original_length}, 'processed_length': {len(generated_code)}}}")
        
        # Success response
        duration_ms = (time.time() - start_time) * 1000
        log_response_info(logger, 200, duration_ms, {
            'request_id': request_id, 
            'success': True,
            'code_length': len(generated_code)
        })
        
        return jsonify({
            "success": True,
            "html_code": generated_code,
            "message": "UI code generated successfully!"
        })
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(f"Unexpected error: {{'request_id': '{request_id}', 'error': '{str(e)}', 'duration_ms': {round(duration_ms, 2)}}}", exc_info=True)
        log_response_info(logger, 500, duration_ms, {'request_id': request_id, 'error': 'Unexpected error'})
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Simple metrics tracking
app_metrics = {
    'start_time': datetime.utcnow(),
    'requests_total': 0,
    'requests_successful': 0,
    'requests_failed': 0,
    'gemini_calls_total': 0,
    'gemini_calls_successful': 0,
    'gemini_calls_failed': 0
}


@app.before_request
def before_request():
    """Track request metrics."""
    app_metrics['requests_total'] += 1


@app.after_request
def after_request(response):
    """Track response metrics."""
    if response.status_code < 400:
        app_metrics['requests_successful'] += 1
    else:
        app_metrics['requests_failed'] += 1
    return response


@app.route('/health')
def health():
    """Health check endpoint."""
    start_time = time.time()
    log_request_info(logger, request)
    
    uptime_seconds = (datetime.utcnow() - app_metrics['start_time']).total_seconds()
    
    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": round(uptime_seconds, 2),
        "version": "1.0.0"
    }
    
    duration_ms = (time.time() - start_time) * 1000
    log_response_info(logger, 200, duration_ms, {'endpoint': 'health'})
    
    return jsonify(health_data)


@app.route('/metrics')
def metrics():
    """Simple metrics endpoint."""
    start_time = time.time()
    log_request_info(logger, request)
    
    uptime_seconds = (datetime.utcnow() - app_metrics['start_time']).total_seconds()
    
    metrics_data = {
        "uptime_seconds": round(uptime_seconds, 2),
        "requests": {
            "total": app_metrics['requests_total'],
            "successful": app_metrics['requests_successful'],
            "failed": app_metrics['requests_failed'],
            "success_rate": round(app_metrics['requests_successful'] / max(app_metrics['requests_total'], 1) * 100, 2)
        },
        "gemini_api": {
            "calls_total": app_metrics['gemini_calls_total'],
            "calls_successful": app_metrics['gemini_calls_successful'],
            "calls_failed": app_metrics['gemini_calls_failed'],
            "success_rate": round(app_metrics['gemini_calls_successful'] / max(app_metrics['gemini_calls_total'], 1) * 100, 2)
        },
        "timestamp": datetime.utcnow().isoformat()
    }
    
    duration_ms = (time.time() - start_time) * 1000
    log_response_info(logger, 200, duration_ms, {'endpoint': 'metrics'})
    
    return jsonify(metrics_data)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    logger.info(f"Starting Flask application on host=0.0.0.0, port={port}")
    app.run(debug=False, host='0.0.0.0', port=port)
