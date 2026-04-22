import sys; 
sys.path.insert(0, 'backend')                                                                                                        
from backend.app.db.session import SessionLocal                                                                                                          
from backend.app.models.news import News                                                                                                                
db = SessionLocal()                                                                                                                              
total = db.query(News).count()                                                                                                                   
with_sum = db.query(News).filter(News.summary.isnot(None)).count()                                                                               
print(f'{with_sum}/{total} articles summarized')                                                                                                 
db.close()                                                                                                                                     
     