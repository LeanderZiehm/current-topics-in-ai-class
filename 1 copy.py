from email_code import get_recent_emails
from application_code import get_users_name
from llm_code import get_llm_response

emails = get_recent_emails("my-email@gmail.com")
name = get_users_name() #"Leander"
prompt = f"You are a email assistant. Here are {name}'s recent emails {emails}"
llm_response = get_llm_response(prompt)