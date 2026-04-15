import streamlit as st


st.set_page_config(layout="wide")

def sidebar():
    with st.sidebar:
         st.button("", key="profile_page",icon=":material/account_circle:")
           

def article_card(article):
    with st.container():
        st.image(article['cover_image'])
        st.subheader(article['title']) 
        st.write(article['preview'])
        st.caption(article['date'])
        if st.button("read more..", key=article["id"]): 
            st.session_state["selected_article_id"] = article["id"]
            st.switch_page("pages/article_details.py")

        

def news_grid(articles, num_columns=3):
    columns=st.columns(num_columns)
    for i,article in enumerate(articles):
        column_index = i % num_columns
        with columns[column_index]:
            article_card(article)
#temp
def get_mock_articles() :
    articles = [
        {
            "cover_image": "https://images.unsplash.com/photo-1677442136019-21780ecad995",
            "title": "New AI Model Released",
            "preview": "A new AI model has been released with advanced reasoning capabilities.",
            "date": "2 hours ago",
            "url": "https://example.com/ai-news",
            "id": "1",
            "author": "John Doe",
            "source": "Tech News Daily",
            "content": "The new AI model, named 'ReasonerX', has been developed by a leading research team and is expected to revolutionize the field of artificial intelligence. It boasts improved natural language understanding and can perform complex reasoning tasks with greater accuracy than previous models. Experts believe that ReasonerX will have significant applications in various industries, including healthcare, finance, and customer service. The model is currently in the testing phase, and the research team plans to release it to the public later this year. Stay tuned for more updates on this exciting development in AI technology." 
        },
        {
            "cover_image": "https://images.unsplash.com/photo-1518770660439-4636190af475",
            "title": "Tech Trends in 2026",
            "preview": "Discover the biggest technology trends shaping the future.",
            "date": "Yesterday",
            "url": "https://example.com/tech-trends",
            "id": "2",
            "author": "Jane Smith",
            "source": "Future Tech Magazine",
            "content": "As we look ahead to 2026, several technology trends are poised to shape the future. One of the most significant trends is the continued advancement of artificial intelligence, with AI becoming increasingly integrated into everyday life. Another major trend is the rise of quantum computing, which promises to revolutionize data processing and problem-solving capabilities. Additionally, we can expect to see significant growth in the Internet of Things (IoT), with more devices becoming interconnected and smarter. Virtual reality (VR) and augmented reality (AR) are also set to become more mainstream, transforming how we interact with digital content. Finally, sustainability will be a key focus, with technology playing a crucial role in addressing environmental challenges. These trends will undoubtedly shape the way we live and work in the coming years."    
        },
        {
            "cover_image": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d",
            "title": "Startups and Innovation",
            "preview": "How startups are driving innovation across industries.",
            "date": "April 10, 2026",
            "url": "https://example.com/startups",
            "id": "3",
            "author": "Emily Johnson",
            "source": "Startup Weekly",
            "content": "Startups are playing a crucial role in driving innovation across various industries. These agile and dynamic companies are often at the forefront of technological advancements, bringing fresh ideas and solutions to the market. From healthcare to finance, startups are disrupting traditional business models and creating new opportunities for growth. Many startups are leveraging emerging technologies such as artificial intelligence, blockchain, and the Internet of Things to develop innovative products and services. Additionally, startups often foster a culture of creativity and experimentation, allowing them to quickly adapt to changing market conditions and customer needs. As a result, startups are not only contributing to economic growth but also shaping the future of industries worldwide. With continued support and investment, startups will continue to be a driving force for innovation and progress in the years to come."  
        }
    ]

    return articles

def for_you_page():
    sidebar()
    st.markdown("# For you page<br>", unsafe_allow_html=True)

    articles = get_mock_articles()#temp
    news_grid(articles)
for_you_page()
