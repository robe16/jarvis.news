import threading
from service.news_update_articles import newsUpdater_service

def start_service():
    # Initiate news cache updating
    thread_newsapi = threading.Thread(target=newsUpdater_service)
    thread_newsapi.start()
