from main import scrape_web_impl

if __name__ == "__main__":
    url = "https://github.com/alexeygrigorev/minsearch"
    content = scrape_web_impl(url)
    print(f"Content length: {len(content)} characters")
    print(f"\nFirst 500 characters:\n{content[:500]}")

