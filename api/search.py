import json
import sys
import os
import logging
from http.server import BaseHTTPRequestHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from research_assistant import ResearchAssistant

def handler(request):
    """Vercel serverless function handler"""
    try:
        # Parse request body
        body = json.loads(request.body)
        logger.info(f"Received request data: {body}")
        
        # Validate input
        query = body.get("query")
        if not query:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "status": "error",
                    "message": "Query is required"
                })
            }
            
        num_papers = body.get("num_papers", 100)
        if not isinstance(num_papers, int) or num_papers <= 0:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "status": "error",
                    "message": "num_papers must be a positive integer"
                })
            }
            
        # Generate research summary
        logger.info(f"Initializing ResearchAssistant for query: {query}")
        assistant = ResearchAssistant()
        result = assistant.generate_research_summary(query, num_papers)
        
        # Return successful response
        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "success",
                "summary": result["summary"],
                "num_papers": result["num_papers_analyzed"],
                "query": query
            })
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "error",
                "message": str(e)
            })
        } 