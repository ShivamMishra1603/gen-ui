// Simple analytics utility for GenUI
class Analytics {
  constructor() {
    this.sessionId = this.generateSessionId();
    this.startTime = Date.now();
    this.events = [];
    
    // Initialize session
    this.trackEvent('session_start', {
      timestamp: new Date().toISOString(),
      user_agent: navigator.userAgent,
      screen_resolution: `${screen.width}x${screen.height}`,
      viewport_size: `${window.innerWidth}x${window.innerHeight}`
    });
    
    // Track page unload
    window.addEventListener('beforeunload', () => {
      this.trackEvent('session_end', {
        session_duration_ms: Date.now() - this.startTime
      });
      this.flush();
    });
  }

  generateSessionId() {
    return 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  trackEvent(eventName, properties = {}) {
    const event = {
      session_id: this.sessionId,
      event_name: eventName,
      timestamp: new Date().toISOString(),
      properties: {
        ...properties,
        url: window.location.href,
        referrer: document.referrer || 'direct'
      }
    };

    this.events.push(event);
    
    // Auto-flush every 10 events or every 5 minutes
    if (this.events.length >= 10 || !this.lastFlush || Date.now() - this.lastFlush > 5 * 60 * 1000) {
      this.flush();
    }

    console.log('📊 Analytics Event:', eventName, properties);
  }

  trackError(error, context = {}) {
    this.trackEvent('error_occurred', {
      error_message: error.message || error.toString(),
      error_stack: error.stack,
      context: context
    });
  }

  trackPerformance(operation, duration_ms, metadata = {}) {
    this.trackEvent('performance_metric', {
      operation,
      duration_ms: Math.round(duration_ms),
      ...metadata
    });
  }

  flush() {
    if (this.events.length === 0) return;

    try {
      // Store in localStorage (in production, send to analytics service)
      const existingEvents = JSON.parse(localStorage.getItem('genui_analytics') || '[]');
      existingEvents.push(...this.events);
      
      // Keep only last 100 events to avoid storage bloat
      if (existingEvents.length > 100) {
        existingEvents.splice(0, existingEvents.length - 100);
      }
      
      localStorage.setItem('genui_analytics', JSON.stringify(existingEvents));
      
      console.log(`📊 Flushed ${this.events.length} analytics events to localStorage`);
      
      this.events = [];
      this.lastFlush = Date.now();
    } catch (error) {
      console.error('Failed to flush analytics events:', error);
    }
  }

  // Convenience methods for common events
  trackFileUpload(fileInfo) {
    this.trackEvent('file_upload', {
      file_name: fileInfo.name,
      file_size: fileInfo.size,
      file_type: fileInfo.type,
      file_extension: fileInfo.name.split('.').pop()?.toLowerCase()
    });
  }

  trackApiKeyInput() {
    this.trackEvent('api_key_input', {
      // Don't log the actual key, just that it was entered
      has_api_key: true
    });
  }

  trackGenerateRequest(startTime) {
    const duration = Date.now() - startTime;
    this.trackEvent('generate_request_start');
    return duration;
  }

  trackGenerateResponse(success, duration_ms, metadata = {}) {
    this.trackEvent('generate_request_complete', {
      success,
      duration_ms: Math.round(duration_ms),
      ...metadata
    });
  }

  trackCodeDownload(codeLength) {
    this.trackEvent('code_download', {
      code_length: codeLength
    });
  }

  trackPreviewToggle(showingPreview) {
    this.trackEvent('preview_toggle', {
      showing_preview: showingPreview
    });
  }
}

// Create singleton instance
const analytics = new Analytics();

export default analytics;
