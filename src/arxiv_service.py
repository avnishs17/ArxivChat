"""
Simple ArXiv service for fetching papers
"""
import arxiv
from typing import List
from models import Paper

class ArxivService:
    def __init__(self):
        self.client = arxiv.Client()
    
    def search_papers(self, query: str, max_results: int = 10) -> List[dict]:
        """Search for papers on ArXiv"""
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            papers = []
            for result in self.client.results(search):
                paper = {
                    "id": result.entry_id.split('/')[-1],
                    "title": result.title,
                    "authors": [author.name for author in result.authors],
                    "abstract": result.summary,
                    "published": result.published.isoformat(),
                    "pdf_url": result.pdf_url,
                    "categories": [cat for cat in result.categories]
                }
                papers.append(paper)
            
            return papers
        except Exception as e:
            raise Exception(f"Error searching ArXiv: {str(e)}")
    
    def get_paper_by_id(self, paper_id: str) -> dict:
        """Get a specific paper by ID"""
        try:
            search = arxiv.Search(id_list=[paper_id])
            result = next(self.client.results(search))
            
            return {
                "id": result.entry_id.split('/')[-1],
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "abstract": result.summary,
                "published": result.published.isoformat(),
                "pdf_url": result.pdf_url,
                "categories": [cat for cat in result.categories]
            }
        except Exception as e:
            raise Exception(f"Error fetching paper: {str(e)}")
