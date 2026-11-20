from duckduckgo_search import DDGS

def search_agricultural_web(query: str, crop: str = "", max_results: int = 3):
    """Perform a live web search for agricultural advice and farming solutions."""
    search_terms = f"{crop} {query} agriculture Kerala agronomy" if crop else f"{query} agriculture Kerala agronomy"
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(search_terms, max_results=max_results))
        
        parsed = []
        for r in results:
            parsed.append({
                "title": r.get("title", ""),
                "snippet": r.get("body", ""),
                "url": r.get("href", "")
            })
        return parsed
    except Exception as e:
        # Fallback query with broader terms
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(f"{query} farming pest disease", max_results=max_results))
            parsed = []
            for r in results:
                parsed.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("href", "")
                })
            return parsed
        except Exception:
            return []
