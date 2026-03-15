import requests as req
from app.services.database_service import insert_article
spaUrl ="https://portalapi.spa.gov.sa/api/v1/news/"

"""
overview:
    this method design for spa source it takes spa api resonse and transform it into json file
    then extract articles blocks into list and return it
parameters:
    -language of articles u want: "en" or " "ar"
    -category id and categoryName based on spa:
    categoryName              | category id 
    -------------------------------------------
    General                   | 1
    Political                 | 2
    Economic                  | 3
    Sports                    | 4
    Social                    | 5
    Cultural                  | 6
    Science and Technology    | 7
    Health                    | 8
    Environment               | 9
    Global Varieties          | 10
    Tourism and entertainment | 11

returns:
list ofnews in this category 

"""
def spaNewsFetcher(language:str,categoryId:int ,categoryName:str):
    parameters={
       "w_content":1,
        "w_tag":1,
        "per_page": 20,
        "category_id": categoryId,
        "page": 1,
        "l": language,
    }
    categoryNewsURL=req.get(spaUrl,params=parameters)
    categoryNewsURL.raise_for_status()
    jsonCategoryNews=categoryNewsURL.json()
    categoryNews=jsonCategoryNews["data"]
    for article in categoryNews:
        article["category"]=categoryName
        article["source"]="spa"
    return categoryNews

"""
overview:
    this method takes unStructuredArticle which is dictionary of all unnessary elements in article
    and extract the nessary keys and elements of the article thin store it in DB
parameters:
     -unStructuredArticle: which is dictionary of article with all unnessary elements in article
returns:
    nothing
"""
def extractArticleDataAndLoadToDB(unStructuredArticle):
    #image
    img=unStructuredArticle.get("image","")
    imgURL= ""
    if img:
        imgURL=img["path"]
    #title
    title=unStructuredArticle.get("title", "")
    #link of article
    url=unStructuredArticle.get("sharable_link","")
    #date
    published_date=unStructuredArticle.get("date_hijri","")
    #language
    language=unStructuredArticle.get("locale","")
    #category
    category=unStructuredArticle.get("category","")
    #source
    source=unStructuredArticle.get("source","")
    #description
    description=unStructuredArticle.get("content","")

    insert_article(title, description, url, category, source, published_date ,imgURL,language)
    

"""
overview:
    this method takes list of articles and excute extractArticleDataAndLoadToDB method on them
parameters: 
    -articles: list of unstructeredArticles
returns:
    nothing
"""
def transformAllArticlesData(articles):
    for article in articles:
        extractArticleDataAndLoadToDB(article)


    
    


    
 
