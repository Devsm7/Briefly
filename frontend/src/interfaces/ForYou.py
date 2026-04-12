import streamlit as st
import profile

st.set_page_config(layout="wide")

def render_sidebar():
    with st.sidebar:
        st.markdown("profile page")
      

def render_news_card(article):
    with st.container():
        st.image(article['cover_image'])
        st.subheader(article['title']) 
        st.write(article['preview'])
        st.caption(article['date'])
        st.markdown(f"[read more..]({article['url']})")
        

def render_news_grid(articles, num_columns=3):
    columns=st.columns(num_columns)
    for i,article in enumerate(articles):
        column_index = i % num_columns
        with columns[column_index]:
            render_news_card(article)
#temp
def get_mock_articles() :
    articles = [
        {
            "cover_image": "https://images.unsplash.com/photo-1677442136019-21780ecad995",
            "title": "New AI Model Released",
            "preview": "A new AI model has been released with advanced reasoning capabilities.",
            "date": "2 hours ago",
            "url": "https://example.com/ai-news"
        },
        {
            "cover_image": "https://images.unsplash.com/photo-1518770660439-4636190af475",
            "title": "Tech Trends in 2026",
            "preview": "Discover the biggest technology trends shaping the future.",
            "date": "Yesterday",
            "url": "https://example.com/tech-trends"
        },
        {
            "cover_image": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d",
            "title": "Startups and Innovation",
            "preview": "How startups are driving innovation across industries.",
            "date": "April 10, 2026",
            "url": "https://example.com/startups"
        }
    ]

    return articles

def for_you_page():
    render_sidebar()
    st.markdown("# For you page<br>", unsafe_allow_html=True)

    articles = get_mock_articles()#temp
    render_news_grid(articles)
    
for_you_page()