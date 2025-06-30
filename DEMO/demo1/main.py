import dotenv 
import os
from get_weather_function import get_weather

dotenv.load_dotenv()

OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")


tools = [get_weather]