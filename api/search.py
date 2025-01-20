from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from research_assistant import ResearchAssistant

def handle_cors(handler):
    handler.send_response(200)
    handler.send_header('Access-Control-Allow-Origin', '*')
    handler.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    handler.send_header('Access-Control-Allow-Headers', 'Content-Type')
    handler.end_headers()

def error_response(handler, status_code, message):
    handler.send_response(status_code)
    handler.send_header('Content-Type', 'application/json')
    handler.send_header('Access-Control-Allow-Origin', '*')
    handler.end_headers()
    response = json.dumps({
        'status': 'error',
        'message': message
    })
    handler.wfile.write(response.encode())

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        handle_cors(self)
        
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            # Validate input
            query = data.get('query')
            if not query:
                return error_response(self, 400, "Query is required")
            
            num_papers = data.get('num_papers', 100)
            if not isinstance(num_papers, int) or num_papers <= 0:
                return error_response(self, 400, "num_papers must be a positive integer")
            
            # Generate research summary
            assistant = ResearchAssistant()
            result = assistant.generate_research_summary(query, num_papers)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = json.dumps({
                'status': 'success',
                'summary': result['summary'],
                'num_papers': result['num_papers_analyzed'],
                'query': query
            })
            self.wfile.write(response.encode())
            
        except json.JSONDecodeError:
            error_response(self, 400, "Invalid JSON payload")
        except Exception as e:
            error_response(self, 500, str(e)) 