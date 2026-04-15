import streamlit as st
from ForYou import get_mock_articles

selected_id = st.query_params.get("id")

st.set_page_config(layout="centered")
articles=get_mock_articles()#temp
if "reaction" not in st.session_state:
    st.session_state["reaction"] = None
if "save" not in st.session_state:
    st.session_state["save"] = False   


for article in articles:
    if article["id"] == selected_id:
        selected_article = article
        st.title(selected_article["title"])
        st.image(selected_article["cover_image"])
        st.write(selected_article["content"])
        st.caption(
        f"{selected_article['date']}  |  "
        f"By {selected_article['author']}  |  "
        f"Source: {selected_article['source']}")
        like, dislike ,save, space = st.columns([1,1,1, 12])
        with like:
            if st.button("", key="like_btn",icon=":material/thumb_up:"):
                st.session_state["reaction"] = "like"
                
        with dislike:
            if st.button("", key="dislike_btn",icon=":material/thumb_down:"):
                st.session_state["reaction"] = "dislike"
        with save:
            if st.button("",key="save_btn",icon=":material/bookmark:"):
                st.session_state["save"] = True

if st.session_state["reaction"] == "like":
    st.markdown("""
<style>
    .st-key-like_btn button 
    , .st-key-like_btn button:hover {
    background-color: #28a745;
}
</style>
    """, unsafe_allow_html=True)
elif st.session_state["reaction"] == "dislike":
    st.markdown("""<style>
    .st-key-dislike_btn button 
     , .st-key-dislike_btn button:hover {
    background: #dc3545;
}
</style>
    """, unsafe_allow_html=True)
if st.session_state["save"] == True:
    st.markdown("""<style>
    .st-key-save_btn button
     , .st-key-save_btn button:hover {
    background: #007bff;
}
</style>
    """, unsafe_allow_html=True)
       
    
    
