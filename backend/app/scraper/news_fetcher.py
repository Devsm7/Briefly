"""RSS feed fetcher — collects articles from verified publisher RSS feeds."""

# TODO: import feedparser, requests, BeautifulSoup, cleaner, deduplicator

# RSS feed sources per category
RSS_SOURCES = {
    "tech": [
        "https://feeds.feedburner.com/TechCrunch",
        "https://www.theverge.com/rss/index.xml",
        "https://feeds.arstechnica.com/arstechnica/index",
    ],
    "business": [
        "https://feeds.reuters.com/reuters/businessNews",
        "https://feeds.bbci.co.uk/news/business/rss.xml",
        "https://www.cnbc.com/id/10001147/device/rss/rss.html",
    ],
    "politics": [
        "https://feeds.reuters.com/Reuters/PoliticsNews",
        "https://feeds.bbci.co.uk/news/politics/rss.xml",
        "https://feeds.npr.org/1014/rss.xml",
    ],
    "sports": [
        "https://www.espn.com/espn/rss/news",
        "https://feeds.bbci.co.uk/sport/rss.xml",
        "https://www.skysports.com/rss/12040",
    ],
}


class NewsFetcher:
    """Fetches articles from RSS feeds and returns cleaned, deduplicated records."""

    def fetch_category(self, category: str) -> list[dict]:
        """
        Fetch articles from all RSS sources for the given category.
        Returns a list of dicts with keys:
            title, description, url, source, category, published_at
        Minimum 10 articles per category per run.
        """
        # TODO: loop RSS_SOURCES[category]
        # TODO: feedparser.parse(url) for each feed
        # TODO: extract entry fields (title, link, summary, published)
        # TODO: clean with cleaner.clean_text()
        # TODO: return collected article dicts
        raise NotImplementedError

    def fetch_all(self) -> list[dict]:
        """
        Fetch articles across all 4 categories.
        Returns a combined flat list of article dicts.
        """
        # TODO: call fetch_category for each key in RSS_SOURCES; flatten results
        raise NotImplementedError

    def save_to_db(self, db, articles: list[dict]) -> tuple[int, int]:
        """
        Insert fetched articles into the `news` table.
        Skips duplicates (by url_hash).
        Returns (inserted_count, skipped_count).
        """
        # TODO: for each article dict:
        #   - compute Article.make_hash(url)
        #   - check if url_hash exists in DB → skip if yes
        #   - else insert new Article row
        raise NotImplementedError
