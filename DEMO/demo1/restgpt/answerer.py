from llms.groq import Groq

groq = Groq()

def answer(infos: list, user_query: str):
    infos_str = "\n".join(f"- {info}" for info in infos)  # Format infos nicely
    
    prompt = f"""
You are an intelligent assistant. Use the following information to answer the user's question as clearly and helpfully as possible.

Information available:
{infos_str}

User's question:
{user_query}

Please provide a thorough, concise, and accurate answer based on the information above. If the information is insufficient to answer fully, politely say so.
"""
    
    answer = groq.generate_response(prompt)
    return answer
