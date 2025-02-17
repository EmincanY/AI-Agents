from smolagents import tool
import os
from newsapi import NewsApiClient
import datetime

@tool
def get_news_headlines(topic: str, count: int = 5) -> str:
    """Get latest news headlines for a specific topic
    Args:
        topic: Topic to search news for
        count: Number of headlines to return (default: 5)
    """
    API_KEY = os.getenv("NEWSAPI_KEY")
    if not API_KEY:
        return "Error: NewsAPI key not found in environment variables"
        
    newsapi = NewsApiClient(api_key=API_KEY)
    
    try:
        # Define search strategies with different parameters
        search_strategies = [
            {
                'query': f'"{topic}"',  # Exact phrase match
                'relevance': 'high'
            },
            {
                'query': topic,  # Normal search
                'relevance': 'high'
            },
            {
                'query': f"{topic} latest",  # Latest news
                'relevance': 'medium'
            }
        ]
        
        relevant_articles = []  # Store only relevant articles
        seen_titles = set()
        required_keywords = set(topic.lower().split())
        
        # Function to check article relevance
        def is_relevant(article, required_words, relevance_level):
            title = article['title'].lower()
            description = (article.get('description') or '').lower()
            content = (article.get('content') or '').lower()
            
            # Count how many required words appear in the article
            title_matches = sum(1 for word in required_words if word in title)
            desc_matches = sum(1 for word in required_words if word in description)
            content_matches = sum(1 for word in required_words if word in content)
            
            # Calculate relevance score
            total_score = (title_matches * 3) + (desc_matches * 2) + content_matches
            
            # For exact phrase matching
            if relevance_level == 'high':
                # Check if the exact topic phrase appears
                if topic.lower() in title or topic.lower() in description:
                    return True
                return total_score >= len(required_words) * 2
            else:
                return total_score >= len(required_words)

        for strategy in search_strategies:
            if len(relevant_articles) >= count:
                break
                
            # Calculate how many more articles we need
            remaining_count = count - len(relevant_articles)
            
            try:
                news = newsapi.get_everything(
                    q=strategy['query'],
                    language='en',
                    sort_by='relevancy',  # Changed to relevancy sort
                    page_size=min(50, remaining_count * 5)  # Request more articles to filter through
                )
                
                if news['articles']:
                    for article in news['articles']:
                        # Skip if we've seen this title or have enough articles
                        if article['title'] in seen_titles:
                            continue
                        
                        # Check if article is relevant enough
                        if is_relevant(article, required_keywords, strategy['relevance']):
                            seen_titles.add(article['title'])
                            pub_date = datetime.datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                            relevant_articles.append({
                                'title': article['title'],
                                'source': article['source']['name'],
                                'date': pub_date,
                                'url': article['url'],
                                'relevance': strategy['relevance']
                            })
                            
                            # Break if we have enough relevant articles
                            if len(relevant_articles) >= count:
                                break
            except Exception as e:
                continue  # If one strategy fails, try the next one
        
        # Sort by date (newest first)
        relevant_articles.sort(key=lambda x: x['date'], reverse=True)
        
        if relevant_articles:
            headlines = []
            for idx, article in enumerate(relevant_articles, 1):
                date_str = article['date'].strftime('%Y-%m-%d %H:%M UTC')
                relevance_indicator = "🎯" if article['relevance'] == 'high' else "✓"
                headlines.append(f"{idx}. {relevance_indicator} [{date_str}] {article['title']} ({article['source']})")
            
            # Add a summary of how many relevant articles were found
            found_count = len(relevant_articles)
            summary = f"Found {found_count} relevant {'article' if found_count == 1 else 'articles'} out of {count} requested.\n\n"
            return summary + "\n".join(headlines)
            
        return f"No relevant news found for topic: {topic}"
    except Exception as e:
        return f"Error fetching news: {str(e)}" 