from fastmcp import FastMCP
from tools.paper_fetcher import PaperFetcher
from typing import Optional

mcp = FastMCP("ResearchMCP")
fetcher = PaperFetcher()


@mcp.tool()
def search_papers(query: str, max_results: int = 5, year_from: Optional[int] = None) -> str:
    """
    Search for academic papers on OpenAlex based on a query.

    Args:
        query: The research topic or keywords to search for
        max_results: Maximum number of papers to return (default: 5)
        year_from: Only include papers from this year onwards (optional)

    Returns:
        A formatted string with paper details including titles, authors, citations, and URLs
    """
    papers = fetcher.search_papers(
        query=query,
        max_results=max_results,
        year_from=year_from
    )

    if papers and "error" in papers[0]:
        return papers[0]["error"]

    if not papers:
        return f"No papers found for query: {query}"

    result = f"Found {len(papers)} papers for '{query}':\n\n"

    for i, paper in enumerate(papers, 1):
        result += f"{i}. **{paper['title']}**\n"
        result += f"   Authors: {paper['authors']}\n"
        result += f"   Year: {paper['publication_year']}\n"
        result += f"   Citations: {paper['cited_by_count']}\n"
        result += f"   URL: {paper['url']}\n"
        result += f"   ID: {paper['id']}\n\n"

    return result


@mcp.tool()
def get_paper_abstract(paper_id: str) -> str:
    """
    Get the full abstract for a specific paper.

    Args:
        paper_id: The OpenAlex paper ID (from search_papers results)

    Returns:
        The paper's abstract text with title and metadata
    """
    paper = fetcher.fetch_paper_by_id(paper_id)

    if "error" in paper:
        return paper["error"]

    abstract_text = fetcher.get_paper_abstract(paper)

    result = f"**{paper['title']}**\n"
    result += f"Authors: {paper['authors']}\n"
    result += f"Year: {paper['publication_year']}\n"
    result += f"Citations: {paper['cited_by_count']}\n\n"
    result += f"**Abstract:**\n{abstract_text}\n"

    return result

@mcp.tool()
def extract_claims(paper_id: str) -> str:
    """
    Extract key claims and findings from a paper's abstract.

    Args:
        paper_id: The OpenAlex paper ID

    Returns:
        Structured list of claims extracted from the paper
    """
    paper = fetcher.fetch_paper_by_id(paper_id)

    if "error" in paper:
        return paper["error"]

    abstract_text = fetcher.get_paper_abstract(paper)

    if abstract_text == "No abstract available":
        return "Cannot extract claims: No abstract available for this paper"

    result = f"**Paper:** {paper['title']}\n"
    result += f"**Authors:** {paper['authors']}\n"
    result += f"**Year:** {paper['publication_year']}\n\n"
    result += f"**Abstract:**\n{abstract_text}\n\n"
    result += f"**Instructions for claim extraction:**\n"
    result += f"Please analyze the abstract above and extract:\n"
    result += f"1. Main research question or hypothesis\n"
    result += f"2. Key methodology or approach\n"
    result += f"3. Primary findings or results\n"
    result += f"4. Main conclusions or implications\n"

    return result

@mcp.tool()
def compare_papers(paper_ids: str) -> str:
    """
    Compare claims across multiple papers to find contradictions and consensus.

    Args:
        paper_ids: Comma-separated list of OpenAlex paper IDs (e.g., "W123,W456,W789")

    Returns:
        Abstracts from all papers for comparison analysis
    """
    ids = [pid.strip() for pid in paper_ids.split(",")]

    if len(ids) < 2:
        return "Error: Please provide at least 2 paper IDs separated by commas"

    if len(ids) > 5:
        return "Error: Maximum 5 papers can be compared at once"

    papers_data = []
    for paper_id in ids:
        paper = fetcher.fetch_paper_by_id(paper_id)

        if "error" in paper:
            papers_data.append(f"**Error fetching {paper_id}:** {paper['error']}\n")
            continue

        abstract_text = fetcher.get_paper_abstract(paper)

        paper_info = f"**Paper {len(papers_data) + 1}:**\n"
        paper_info += f"Title: {paper['title']}\n"
        paper_info += f"Authors: {paper['authors']}\n"
        paper_info += f"Year: {paper['publication_year']}\n"
        paper_info += f"Citations: {paper['cited_by_count']}\n\n"
        paper_info += f"Abstract: {abstract_text}\n"
        paper_info += f"{'-' * 80}\n\n"

        papers_data.append(paper_info)

    result = f"**Comparing {len(papers_data)} papers:**\n\n"
    result += "".join(papers_data)
    result += "\n**Analysis Instructions:**\n"
    result += "Please analyze these papers and identify:\n"
    result += "1. **Contradictions:** Where do the papers disagree or present conflicting findings?\n"
    result += "2. **Consensus:** What do the papers agree on?\n"
    result += "3. **Gaps:** What questions remain unanswered or areas need more research?\n"

    return result


if __name__ == "__main__":
    mcp.run()
