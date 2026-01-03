import os
import requests
import zipfile
from fastmcp import FastMCP
from minsearch import Index

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def scrape_web_impl(url: str) -> str:
    """Scrape content from a web page using Jina Reader. Returns the page content in markdown format."""
    jina_url = f"https://r.jina.ai/{url}"
    response = requests.get(jina_url)
    response.raise_for_status()
    return response.text

@mcp.tool
def scrape_web(url: str) -> str:
    """Scrape content from a web page using Jina Reader. Returns the page content in markdown format."""
    return scrape_web_impl(url)

# Search functionality
_search_index = None
_zip_path = "fastmcp-main.zip"

def get_or_create_index():
    """Get or create the search index."""
    global _search_index
    
    if _search_index is not None:
        return _search_index
    
    # Download if needed
    zip_url = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
    if not os.path.exists(_zip_path):
        print(f"Downloading {zip_url}...")
        response = requests.get(zip_url)
        response.raise_for_status()
        with open(_zip_path, 'wb') as f:
            f.write(response.content)
    
    # Extract and index
    index = Index(['content', 'filename'])
    documents = []
    
    with zipfile.ZipFile(_zip_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        markdown_files = [f for f in file_list if f.endswith('.md') or f.endswith('.mdx')]
        
        for file_path in markdown_files:
            try:
                content = zip_ref.read(file_path).decode('utf-8')
                parts = file_path.split('/')
                if parts[0].endswith('-main') or parts[0].endswith('-master'):
                    clean_path = '/'.join(parts[1:])
                else:
                    clean_path = file_path
                
                documents.append({
                    'content': content,
                    'filename': clean_path
                })
            except Exception as e:
                continue
    
    index.fit(documents)
    _search_index = index
    return index

@mcp.tool
def search_docs(query: str, num_results: int = 5) -> list:
    """Search the fastmcp documentation. Returns a list of relevant documents with filename and content preview."""
    index = get_or_create_index()
    results = index.search(query, num_results=num_results)
    return results

if __name__ == "__main__":
    mcp.run()
