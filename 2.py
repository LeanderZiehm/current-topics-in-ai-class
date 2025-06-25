from tools import get_recent_emails, add_event_to_calender
from llm_code import get_llm_response

emails = get_recent_emails("my-email@gmail.com")
name = "Leander"
prompt = f"You are a email assistant. Here are {name}'s recent emails {emails}"
llm_response = get_llm_response(prompt)

# if x 
# add_event_to_calender
