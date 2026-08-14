from datetime import datetime

def current_time():
    now = datetime.now()
    
    formatted = now.strftime("%b %d %Y %I:%M%p")
    formatted = formatted[:-2] + formatted[-2:].lower()
    
    return formatted


