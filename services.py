from datetime import datetime
from zoneinfo import ZoneInfo

def current_time():
    now = datetime.now(ZoneInfo("Africa/Lagos"))

    formatted = now.strftime("%b %d %Y %I:%M%p")
    formatted = formatted[:-2] + formatted[-2:].lower()

    return formatted


print(current_time())