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

@mcp.tool()
def get_citations(paper_id: str, direction: str = "both", max_results: int = 10) -> str:
    """
    Get citation network for a paper - see what cites it and what it cites.

    Args:
        paper_id: The OpenAlex paper ID
        direction: "cited_by" (papers citing this), "references" (papers this cites), or "both"
        max_results: Maximum number of citations to return per direction (default: 10)

    Returns:
        Citation network information with paper details
    """
    paper = fetcher.fetch_paper_by_id(paper_id)

    if "error" in paper:
        return paper["error"]

    result = f"**Citation Network for:** {paper['title']}\n"
    result += f"**Authors:** {paper['authors']}\n"
    result += f"**Year:** {paper['publication_year']}\n"
    result += f"**Total Citations:** {paper['cited_by_count']}\n\n"

    if direction in ["cited_by", "both"]:
        cited_by_papers = fetcher.get_cited_by_papers(paper_id, max_results)
        
        if cited_by_papers and "error" not in cited_by_papers[0]:
            result += f"**📈 Papers Citing This Work ({len(cited_by_papers)} shown):**\n\n"
            for i, citing_paper in enumerate(cited_by_papers, 1):
                result += f"{i}. **{citing_paper['title']}**\n"
                result += f"   Authors: {citing_paper['authors']}\n"
                result += f"   Year: {citing_paper['publication_year']}\n"
                result += f"   Citations: {citing_paper['cited_by_count']}\n"
                result += f"   ID: {citing_paper['id']}\n\n"
        else:
            result += "No citing papers found or error fetching citations.\n\n"

    if direction in ["references", "both"]:
        references = fetcher.get_references(paper_id, max_results)
        
        if references and "error" not in references[0]:
            result += f"**📚 Papers This Work References ({len(references)} shown):**\n\n"
            for i, ref_paper in enumerate(references, 1):
                result += f"{i}. **{ref_paper['title']}**\n"
                result += f"   Authors: {ref_paper['authors']}\n"
                result += f"   Year: {ref_paper['publication_year']}\n"
                result += f"   Citations: {ref_paper['cited_by_count']}\n"
                result += f"   ID: {ref_paper['id']}\n\n"
        else:
            result += "No references found or error fetching references.\n\n"

    return result

@mcp.tool()
def find_research_gaps(query: str, num_papers: int = 5) -> str:
    """
    Analyze multiple papers on a topic to identify research gaps and unanswered questions.

    Args:
        query: Research topic to analyze
        num_papers: Number of papers to analyze (default: 5, max: 10)

    Returns:
        Analysis of research gaps, limitations, and future research directions
    """
    if num_papers > 10:
        num_papers = 10

    papers = fetcher.search_papers(query=query, max_results=num_papers, sort_by="cited_by_count")

    if papers and "error" in papers[0]:
        return papers[0]["error"]

    if not papers:
        return f"No papers found for query: {query}"

    result = f"**Research Gap Analysis for: '{query}'**\n"
    result += f"**Analyzing {len(papers)} highly-cited papers**\n\n"

    result += "**Papers Analyzed:**\n"
    paper_ids = []
    for i, paper in enumerate(papers, 1):
        result += f"{i}. {paper['title']} ({paper['publication_year']}) - {paper['cited_by_count']} citations\n"
        paper_ids.append(paper['id'])

    result += "\n**Fetching abstracts for deep analysis...**\n\n"

    abstracts_data = []
    for i, paper_id in enumerate(paper_ids, 1):
        paper_detail = fetcher.fetch_paper_by_id(paper_id)
        if "error" not in paper_detail:
            abstract_text = fetcher.get_paper_abstract(paper_detail)
            abstracts_data.append(f"**Paper {i}:** {paper_detail['title']}\n{abstract_text}\n")

    result += "".join(abstracts_data)

    result += "\n**Gap Analysis Instructions:**\n"
    result += "Based on the abstracts above, please identify:\n\n"
    result += "1. **Unanswered Research Questions:**\n"
    result += "   - What questions do these papers raise but not answer?\n"
    result += "   - What do the authors suggest for future research?\n\n"
    result += "2. **Methodological Limitations:**\n"
    result += "   - What limitations do the authors acknowledge?\n"
    result += "   - What methods or approaches are missing?\n\n"
    result += "3. **Understudied Areas:**\n"
    result += "   - What aspects of the topic receive less attention?\n"
    result += "   - What populations, contexts, or scenarios are not covered?\n\n"
    result += "4. **Contradictions & Inconsistencies:**\n"
    result += "   - Where do findings conflict?\n"
    result += "   - What requires further investigation to resolve?\n\n"
    result += "5. **Emerging Opportunities:**\n"
    result += "   - What new research directions are suggested?\n"
    result += "   - What interdisciplinary connections could be made?\n"

    return result


if __name__ == "__main__":
    mcp.run()
