from http.server import BaseHTTPRequestHandler
import json
import sys
import os
import logging
from flask import Flask, request, jsonify, Response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from research_assistant import ResearchAssistant

app = Flask(__name__)

def handle_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/api/search', methods=['POST', 'OPTIONS'])
def handler():
    if request.method == 'OPTIONS':
        logger.info("Handling OPTIONS request")
        return handle_cors(Response())

    logger.info("Handling POST request")
    try:
        data = request.get_json()
        logger.info(f"Received request data: {data}")
        
        # Validate input
        query = data.get('query')
        if not query:
            logger.error("Query parameter missing")
            return jsonify({
                'status': 'error',
                'message': 'Query is required'
            }), 400
        
        num_papers = data.get('num_papers', 100)
        if not isinstance(num_papers, int) or num_papers <= 0:
            logger.error(f"Invalid num_papers value: {num_papers}")
            return jsonify({
                'status': 'error',
                'message': 'num_papers must be a positive integer'
            }), 400
        
        # Generate research summary
        logger.info(f"Initializing ResearchAssistant for query: {query}")
        assistant = ResearchAssistant()
        result = assistant.generate_research_summary(query, num_papers)
        
        response = jsonify({
            'status': 'success',
            'summary': result['summary'],
            'num_papers': result['num_papers_analyzed'],
            'query': query
        })
        logger.info("Successfully generated summary")
        return handle_cors(response)
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 