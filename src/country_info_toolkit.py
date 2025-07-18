
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Define Tool Functions ---
# For a real-world application, you'd use a robust library or API here.
# For this assignment, we'll use a simple dictionary for demonstration.

COUNTRY_DATA = {
    "france": {"capital": "Paris", "language": "French", "population": "65 million"},
    "germany": {"capital": "Berlin", "language": "German", "population": "83 million"},
    "japan": {"capital": "Tokyo", "language": "Japanese", "population": "125 million"},
    "india": {"capital": "New Delhi", "language": "Hindi, English", "population": "1.4 billion"},
    "usa": {"capital": "Washington D.C.", "language": "English", "population": "330 million"},
    "pakistan": {"capital": "Islamabad", "language": "Urdu, English", "population": "240 million"},
    "china": {"capital": "Beijing", "language": "Mandarin", "population": "1.4 billion"},
}

def get_country_capital(country_name: str) -> str:
    """
    Provides the capital city of a given country.

    Args:
        country_name: The name of the country (e.g., "France", "Japan").

    Returns:
        The capital city of the country, or an error message if not found.
    """
    country = country_name.lower()
    return COUNTRY_DATA.get(country, {}).get("capital", f"Capital for {country_name} not found.")

def get_country_language(country_name: str) -> str:
    """
    Provides the official language(s) of a given country.

    Args:
        country_name: The name of the country.

    Returns:
        The official language(s) of the country, or an error message if not found.
    """
    country = country_name.lower()
    return COUNTRY_DATA.get(country, {}).get("language", f"Language for {country_name} not found.")

def get_country_population(country_name: str) -> str:
    """
    Provides the approximate population of a given country.

    Args:
        country_name: The name of the country.

    Returns:
        The population of the country, or an error message if not found.
    """
    country = country_name.lower()
    return COUNTRY_DATA.get(country, {}).get("population", f"Population for {country_name} not found.")

# --- Orchestrator Agent (using Function Calling) ---

def create_country_info_orchestrator():
    """
    Creates a generative model (orchestrator) capable of using defined tools.
    """
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        tools=[
            get_country_capital,      # Register Python functions as tools
            get_country_language,
            get_country_population
        ],
        generation_config={
            "temperature": 0.2, # Lower temperature for factual accuracy
        }
    )
    return model

def get_country_full_info(country_name: str) -> str:
    """
    Orchestrates the tool calls to get complete information about a country.
    """
    model = create_country_info_orchestrator()
    chat = model.start_chat(enable_automatic_function_calling=True)

    # Initial prompt to trigger tool use
    prompt = f"Tell me everything you know about {country_name}."

    try:
        response = chat.send_message(prompt)

        # The response will contain the result of the function calls
        # If automatic function calling is enabled, the model will execute and return results
        return response.text
    except Exception as e:
        return f"Could not retrieve information for {country_name}. Error: {e}"

if __name__ == "__main__":
    print("🌎  Welcome to the Country Info Bot!")
    print("Available countries: France, Germany, Japan, India, USA, Pakistan, China")
    while True:
        country_input = input("Enter a country name (or 'exit' to quit): ")
        if country_input.lower() == 'exit':
            break

        print(f"\n 🔎  Retrieving info for {country_input}...\n")
        info = get_country_full_info(country_input)
        print(info)
        print("-" * 50)