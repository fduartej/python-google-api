import julian
import datetime as dt

from googleapiclient.discovery import build

def google_search(search_term, api_key, cse_id, num_results, **kwargs):
    service = build("customsearch", "v1", 
        developerKey=api_key)
    res = service.cse().list(
        q=search_term, 
        cx=cse_id, 
        num=num_results,
        **kwargs).execute()
        
    return res

def get_fechas():

    return "fechas"

class KeyTerm:
    VETO_LKDIN = "veto_lkdin"
    VETO_NEWS = "veto_news"
    WISH_LKDIN = "wish_lkdin"
    WISH_NEWS = "wish_news"
    ZOOM_NEWS = "zoom_news"
    SITE_BIZZ = "site_bizz"
    SITE_CLUB = "site_club"
    SITE_OTHER = "site_otro"
    ALL_LKDIN = "all_lkdin"
    Q_BASE = "query_base"
    Q_BASE_CTG = "Category"
    Q_BASE_CTG_VETO = "veto"
    Q_BASE_CTG_WISH = "wish"
    Q_BASE_CTG_OTROS = "z_otros"
    Q_BASE_LVL = "Level"
    Q_BASE_TRM = "Termino"
 
class Setting:
    NUM_RESULTS_DEFAULT=10
    API_KEY=""
    CSE_ID="97b63507f96534ae5"