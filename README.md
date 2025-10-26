# ResearchMCP - AI-Powered Research Paper Assistant

An MCP (Model Context Protocol) server that helps analyze academic papers by fetching research from OpenAlex.

## Features

- **Search Papers**: Search for academic papers by topic/keywords
- **Get Abstracts**: Retrieve full abstracts for specific papers
- Powered by OpenAlex API (millions of papers, no API key needed!)

## Tools

### `search_papers`
Search for academic papers on OpenAlex.

**Parameters:**
- `query` (string, required): Research topic or keywords
- `max_results` (int, optional): Maximum papers to return (default: 5)
- `year_from` (int, optional): Only papers from this year onwards

### `get_paper_abstract`
Get the full abstract for a specific paper.

**Parameters:**
- `paper_id` (string, required): OpenAlex paper ID from search results

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ResearchMCP.git
cd ResearchMCP

# Install dependencies
uv sync

# Run the server
uv run src/server.py
