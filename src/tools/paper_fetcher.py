import httpx
from typing import List, Dict, Optional


class PaperFetcher:
    """Handles fetching papers from OpenAlex API"""

    BASE_URL = "https://api.openalex.org"

    def __init__(self):
        self.client = httpx.Client(timeout=30.0)

    def search_papers(
        self,
        query: str,
        max_results: int = 5,
        sort_by: str = "cited_by_count",
        year_from: Optional[int] = None
    ) -> List[Dict]:
        """
        Search for papers on OpenAlex.

        Args:
            query: Search keywords
            max_results: Maximum number of results
            sort_by: Sort by 'cited_by_count', 'publication_date', or 'relevance'
            year_from: Only papers from this year onwards

        Returns:
            List of paper dictionaries with title, authors, abstract, etc.
        """
        url = f"{self.BASE_URL}/works"

        params = {
            "search": query,
            "per_page": max_results,
            "sort": sort_by + ":desc"
        }

        if year_from:
            params["filter"] = f"publication_year:>{year_from-1}"

        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            papers = []
            for work in data.get("results", []):
                paper = self._parse_paper(work)
                papers.append(paper)

            return papers

        except httpx.HTTPError as e:
            return [{"error": f"Failed to fetch papers: {str(e)}"}]
    
    def _parse_paper(self, work: Dict) -> Dict:
        """Parse a single paper from OpenAlex response"""
        authors = []
        for authorship in work.get("authorships", [])[:5]:
            author = authorship.get("author", {})
            if author.get("display_name"):
                authors.append(author["display_name"])

        authors_str = ", ".join(authors)
        if len(work.get("authorships", [])) > 5:
            authors_str += " et al."

        return {
            "id": work.get("id", ""),
            "title": work.get("title", "No title"),
            "authors": authors_str,
            "publication_year": work.get("publication_year"),
            "cited_by_count": work.get("cited_by_count", 0),
            "abstract": work.get("abstract_inverted_index"),
            "doi": work.get("doi"),
            "url": work.get("doi") or work.get("id"),
            "type": work.get("type"),
        }

    def fetch_paper_by_id(self, paper_id: str) -> Dict:
        """
        Fetch a specific paper's details by its OpenAlex ID.

        Args:
            paper_id: The OpenAlex paper ID (e.g., "https://openalex.org/W123456")

        Returns:
            Dictionary with paper details including abstract
        """
        try:
            paper_id = paper_id.strip()

            if "openalex.org/" in paper_id:
                work_id = paper_id.split("/")[-1]
            else:
                work_id = paper_id

            api_url = f"{self.BASE_URL}/works/{work_id}"
            response = self.client.get(api_url)

            if response.status_code != 200:
                return {"error": f"OpenAlex returned status {response.status_code}"}

            if not response.text:
                return {"error": "OpenAlex returned empty response"}

            work = response.json()
            return self._parse_paper(work)

        except httpx.HTTPError as e:
            return {"error": f"HTTP Error: {str(e)}"}
        except Exception as e:
            return {"error": f"Error: {type(e).__name__}: {str(e)}"}

    def get_paper_abstract(self, paper_data: Dict) -> str:
        """
        Convert OpenAlex inverted index abstract to readable text.

        Args:
            paper_data: Paper dictionary containing abstract in inverted index format

        Returns:
            Readable abstract text
        """
        inverted_index = paper_data.get("abstract")

        if not inverted_index:
            return "No abstract available"

        word_positions = []
        for word, positions in inverted_index.items():
            for pos in positions:
                word_positions.append((pos, word))

        word_positions.sort(key=lambda x: x[0])
        abstract = " ".join([word for _, word in word_positions])

        return abstract

    def close(self):
        """Close the HTTP client"""
        self.client.close()