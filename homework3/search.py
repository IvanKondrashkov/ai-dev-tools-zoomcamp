import os
import zipfile
import requests
from pathlib import Path
from minsearch import Index

def download_repo_if_needed(url: str, output_path: str) -> str:
    """Download a zip file from URL if it doesn't already exist."""
    if os.path.exists(output_path):
        print(f"File {output_path} already exists, skipping download")
        return output_path
    
    print(f"Downloading {url}...")
    response = requests.get(url)
    response.raise_for_status()
    
    with open(output_path, 'wb') as f:
        f.write(response.content)
    
    print(f"Downloaded to {output_path}")
    return output_path

def extract_and_index_markdown(zip_path: str):
    """Extract zip file, read only .md and .mdx files, and index them with minsearch."""
    index = Index(['content', 'filename'])
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Get list of all files
        file_list = zip_ref.namelist()
        
        # Filter only .md and .mdx files
        markdown_files = [f for f in file_list if f.endswith('.md') or f.endswith('.mdx')]
        
        documents = []
        for file_path in markdown_files:
            try:
                # Read file content
                content = zip_ref.read(file_path).decode('utf-8')
                
                # Remove the first part of the path (e.g., "fastmcp-main/" prefix)
                # Split by "/" and remove first part if it contains "-"
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
                print(f"Error reading {file_path}: {e}")
                continue
    
    # Fit the index with all documents
    index.fit(documents)
    print(f"Indexed {len(documents)} documents")
    
    return index

def search(index: Index, query: str, top_k: int = 5):
    """Search the index and return top K most relevant documents."""
    results = index.search(query, num_results=top_k)
    return results

if __name__ == "__main__":
    # Download the repo
    zip_url = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
    zip_path = "fastmcp-main.zip"
    
    download_repo_if_needed(zip_url, zip_path)
    
    # Extract and index
    index = extract_and_index_markdown(zip_path)
    
    # Test search
    query = "demo"
    print(f"\nSearching for: '{query}'")
    results = search(index, query, top_k=5)
    
    print(f"\nTop {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['filename']}")
        print(f"   Score: {result.get('score', 'N/A')}")
        print()

