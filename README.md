# ArXiv Researcher API

A serverless API that generates research summaries from arXiv papers using OpenAI and Pinecone for semantic search.

## API Usage

Endpoint: `POST https://arxiv-researcher.vercel.app/api/search`

Request body:
```json
{
    "query": "your research topic",
    "num_papers": 100  // optional, defaults to 100
}
```

Response:
```json
{
    "status": "success",
    "summary": "comprehensive research summary...",
    "num_papers": 100,
    "query": "your research topic"
}
```

## Development

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your API keys
3. Install dependencies: `pip install -r requirements.txt`
4. Run locally: `vercel dev`

## Environment Variables Required

- `OPENAI_API_KEY`: Your OpenAI API key
- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_ENV`: Your Pinecone environment