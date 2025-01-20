"""
Research Assistant: A tool that uses ArxivIndexer and OpenAI to generate summaries of research papers.
"""

from arxiv_indexer import ArxivIndexer
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

class ResearchAssistant:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.indexer = ArxivIndexer(openai_client=self.client)

    def generate_research_summary(self, query: str, num_papers: int = 100) -> Dict:
        """
        Generate a comprehensive research summary based on arXiv papers.
        
        Args:
            query (str): Research topic to search for
            num_papers (int): Number of papers to analyze (default: 100)
            
        Returns:
            Dict: Contains the summary and key findings
        """
        # First fetch and index papers related to the query
        papers = self.indexer.fetch_papers(query, max_results=num_papers)
        print(f"\nFetched {len(papers)} papers. Indexing them...")
        self.indexer.index_papers(papers)
        
        # Then search for the most relevant ones
        print("\nGenerating research summary...")
        results = self.indexer.search_papers(query, top_k=min(num_papers, len(papers)))
        
        # Prepare paper summaries for the prompt
        papers_text = "\n\n".join([
            f"Title: {result.metadata['title']}\nAbstract: {result.metadata['abstract']}"
            for result in results
        ])
        
        # Generate research summary using GPT-4
        prompt = f"""You are a research assistant analyzing papers about {query}.
        Based on the following paper abstracts, provide:
        1. A comprehensive summary of the current state of research
        2. Key findings and trends
        3. Major open questions and challenges
        4. Potential future research directions

        Papers:
        {papers_text}
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a helpful research assistant specializing in physics and cosmology."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return {
            "summary": response.choices[0].message.content,
            "num_papers_analyzed": len(results)
        }

def main():
    assistant = ResearchAssistant()
    query = input("Enter your research topic: ")
    print("\nFetching and analyzing papers... This may take a few minutes...")
    result = assistant.generate_research_summary(query)
    
    print("\n=== Research Summary ===")
    print(f"\nBased on {result['num_papers_analyzed']} papers:")
    print(result['summary'])

if __name__ == "__main__":
    main() 