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


if __name__ == "__main__":
    mcp.run()
