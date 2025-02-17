from smolagents import tool
import wikipediaapi

@tool
def get_wikipedia_summary(topic: str) -> str:
    """Get a summary of a Wikipedia article
    Args:
        topic: Topic to get summary for
    """
    wiki = wikipediaapi.Wikipedia(
        user_agent='HuggingFaceAgent/1.0 (https://huggingface.co/; contact@huggingface.co)',
        language='en'
    )
    try:
        page = wiki.page(topic)
        if page.exists():
            # Get first two sentences or first 500 characters, whichever is shorter
            summary = page.summary[:500]
            if len(summary) == 500:
                summary = summary[:summary.rindex('.')] + '.'
            return summary
        return f"No Wikipedia article found for: {topic}"
    except Exception as e:
        return f"Error fetching Wikipedia summary: {str(e)}" 