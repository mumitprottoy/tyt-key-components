
def form_fields_are_valid(inputs: list, fields: list, csrf=True) -> tuple[bool, list]:
    
    error_msg = 'The form is corrupted. Probably through inspection tools.'
    
    if csrf: fields = ['csrfmiddlewaretoken']+fields
    
    if len(fields)!=len(inputs): 
        return False, [error_msg]
    
    for inp in inputs:  
        if inp not in fields: return False, [error_msg]
    
    return True, None




 
 