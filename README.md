# ArXiv Researcher API

A serverless API that generates research summaries from arXiv papers using OpenAI and Pinecone for semantic search.

## API Usage

Endpoint: `POST https://arxiv-researcher.vercel.app/api/search`

### Authentication
All requests require an API key to be sent in the header:
```
x-api-key: your-api-key
```

### Request
```json
{
    "query": "your research topic",
    "num_papers": 100  // optional, defaults to 100
}
```

### Response
```json
{
    "status": "success",
    "summary": "comprehensive research summary...",
    "num_papers": 100,
    "query": "your research topic"
}
```

### Error Responses
- `401`: Invalid or missing API key
- `400`: Invalid request parameters
- `500`: Server error

## Development

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your API keys:
   ```
   OPENAI_API_KEY=your-openai-key
   PINECONE_API_KEY=your-pinecone-key
   PINECONE_ENV=your-pinecone-environment
   API_KEY=your-api-key-for-authentication
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Run locally: `vercel dev`

## Environment Variables Required

- `OPENAI_API_KEY`: Your OpenAI API key
- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_ENV`: Your Pinecone environment
- `API_KEY`: API key for authenticating requests