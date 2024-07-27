from datetime import datetime



def passes_check_list(check_list: tuple, check_all: bool=False) -> tuple:
    issues = list()
    for check in check_list:
        if not check[0]:
            if check_all: issues.append(check)
            else: return (False, check)
    
    return (True, None) if not issues else (False, issues)



def get_object_with_method(method, default=None, **kwargs):
    try: return method(**kwargs)
    except: return default



def get_object(cls, default=None, **kwargs):
    try: return cls(**kwargs)
    except: return default



def get_rid_of_list_type_values(form_data: dict) -> dict:
    
    for key in form_data.keys():
        if type(form_data[key]) is list:
            if len(form_data[key]) < 2:
                form_data[key] = form_data[key][0]
    
    return form_data 



def get_serializable_dict(
        obj, pop_state: bool=True, pop_id: bool=False, pop_csrf: bool=True) -> dict:
    d = obj.__dict__.copy(); 
    
    if pop_state:
        if '_state' in d.keys(): d.pop('_state')
    
    if pop_id: 
        if 'id' in d.keys(): d.pop('id')

    if pop_csrf:
        if 'csrfmiddlewaretoken' in d.keys():
            d.pop('csrfmiddlewaretoken')

    return d


def object_to_dict(obj, pop_state: bool=True, pop_id: bool=False) -> dict:
    d = obj.__dict__.copy()
    
    if pop_state: 
        if '_state' in d: d.pop('_state')
    if pop_id:
        if 'id' in d: d.pop('id')
    
    from django.db.models import Model
    for k in d.keys(): 
        if isinstance(d[k], Model): d[k] = d[k].id
    
    return d
    
    


def make_datetime_aware(date_time: datetime) -> datetime:
    from django.utils import timezone
    date_time = timezone.make_aware(
        date_time, timezone=timezone.get_current_timezone())
    
    return date_time




def dict_to_object(dic: dict):
    
    class DictToObject:
    
        def __init__(self, **kwargs) -> None:
            self.__dict__.update(**kwargs)
    
    return DictToObject(**dic)



def resolve_apnt_url(*args):
    from .constants import APNT_BASE_URL
    url = APNT_BASE_URL
    for _ in args: url += str(_)+'/'

    return url


def resolve_trx_check_url(trx: str):
    return f"https://secure.aamarpay.com/api/v1/trxcheck/request.php?request_id={trx}&store_id=theyellowtherapist&signature_key=bd32dd400c563ceeeceb60faf2a9efeb&type=json"