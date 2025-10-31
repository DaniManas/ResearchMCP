# ResearchMCP - AI-Powered Research Paper Assistant

An MCP (Model Context Protocol) server that helps analyze academic papers by fetching research from OpenAlex's database of 250M+ papers.

<a href="https://glama.ai/mcp/servers/@DaniManas/ResearchMCP">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@DaniManas/ResearchMCP/badge" alt="ResearchMCP MCP server" />
</a>

## Features

- **Search Papers**: Search for academic papers by topic/keywords with advanced filtering
- **Extract Claims**: Automatically extract key findings and research claims from papers
- **Compare Papers**: Identify contradictions and consensus across multiple papers
- **Citation Analysis**: Explore citation networks to discover related research
- **Research Gap Finder**: Analyze multiple papers to identify gaps and future research opportunities
- Powered by OpenAlex API (millions of papers, no API key needed!)

## Tools

### `search_papers`
Search for academic papers on OpenAlex.

**Parameters:**
- `query` (string, required): Research topic or keywords
- `max_results` (int, optional): Maximum papers to return (default: 5)
- `year_from` (int, optional): Only papers from this year onwards

**Example:** "Search for papers on transformer models in NLP"

### `get_paper_abstract`
Get the full abstract for a specific paper.

**Parameters:**
- `paper_id` (string, required): OpenAlex paper ID from search results

**Example:** "Get abstract for paper W2964027837"

### `extract_claims`
Extract key claims and findings from a paper's abstract.

**Parameters:**
- `paper_id` (string, required): OpenAlex paper ID

**Returns:** Structured extraction of research questions, methodology, findings, and conclusions

**Example:** "Extract claims from paper W2964027837"

### `compare_papers`
Compare claims across multiple papers to find contradictions and consensus.

**Parameters:**
- `paper_ids` (string, required): Comma-separated list of paper IDs (2-5 papers)

**Returns:** Comparative analysis showing agreements, contradictions, and research gaps

**Example:** "Compare these papers: W2964027837, W3177828909, W2123456789"

### `get_citations`
Get citation network for a paper - see what cites it and what it references.

**Parameters:**
- `paper_id` (string, required): OpenAlex paper ID
- `direction` (string, optional): "cited_by", "references", or "both" (default: "both")
- `max_results` (int, optional): Maximum citations per direction (default: 10)

**Returns:** Lists of papers that cite this work and papers it references

**Example:** "Show me the citation network for W2964027837"

### `find_research_gaps`
Analyze multiple papers on a topic to identify research gaps and unanswered questions.

**Parameters:**
- `query` (string, required): Research topic to analyze
- `num_papers` (int, optional): Number of papers to analyze (default: 5, max: 10)

**Returns:** Comprehensive gap analysis including:
- Unanswered research questions
- Methodological limitations
- Understudied areas
- Contradictions requiring further investigation
- Emerging research opportunities

**Example:** "Find research gaps in transformer architecture optimization"

## Installation

### Option 1: Deploy to FastMCP Cloud (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/ResearchMCP.git
cd ResearchMCP
```

2. Deploy to FastMCP Cloud:
```bash
fastmcp deploy
```

3. Set the entrypoint as: `src/server.py`

4. Connect to Claude Desktop by adding to your MCP settings

### Option 2: Run Locally

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ResearchMCP.git
cd ResearchMCP

# Install dependencies
uv sync

# Run the server
uv run src/server.py
```

## Usage with Claude Desktop

Once deployed or running locally, you can use natural language prompts in Claude Desktop:

**Search for papers:**
- "Search for recent papers on quantum computing"
- "Find papers about CRISPR gene editing from 2020 onwards"

**Analyze specific papers:**
- "Extract the key claims from paper W2964027837"
- "Get the abstract for paper W3177828909"

**Compare research:**
- "Compare these papers: W2964027837, W3177828909"
- "What do these papers agree and disagree on?"

**Explore citations:**
- "Show me what papers cite W2964027837"
- "What papers does W2964027837 reference?"

**Find research gaps:**
- "Find research gaps in transformer architecture optimization"
- "What are the unanswered questions in climate change modeling?"

## Architecture

ResearchMCP uses a clean separation of concerns architecture:

- **[server.py](src/server.py)**: MCP server that defines tools available to Claude Desktop
- **[paper_fetcher.py](src/tools/paper_fetcher.py)**: Worker class handling all OpenAlex API interactions

This design pattern ensures:
- Clean code organization
- Easy maintenance and testing
- Separation between tool orchestration and API logic

## Technology Stack

- **FastMCP**: Python framework for building MCP servers
- **OpenAlex API**: Access to 250M+ academic papers with no API key required
- **httpx**: Modern async-capable HTTP client
- **Python 3.12+**: Type hints and modern Python features

## Why MCP over RAG?

Traditional RAG systems require:
- Pre-indexing large document collections
- Vector database setup and maintenance
- Embedding generation costs
- Limited to pre-indexed documents

ResearchMCP with MCP:
- **Live access** to 250M+ papers without pre-indexing
- **No infrastructure** - no vector databases needed
- **Always up-to-date** - accesses latest published research
- **Cost-effective** - no embedding generation costs
- **Tool orchestration** - Claude intelligently chains multiple API calls

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

MIT License - feel free to use this project for your research needs!