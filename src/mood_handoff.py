# mood_handoff.py
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re # For simple mood extraction

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Agent 1: Mood Analyzer ---
def analyze_mood_agent(message: str) -> str:
    """
    Agent 1: Analyzes the user's message and determines their mood.
    Returns: A single word representing the mood (e.g., 'happy', 'sad', 'stressed', 'neutral').
    """
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    prompt = (
        "Analyze the following message and determine the user's primary mood. "
        "Respond with only a single, lowercase word: 'happy', 'sad', 'stressed', 'angry', 'neutral', 'excited'.\n"
        f"Message: \"{message}\"\n"
        "Mood:"
    )
    try:
        response = model.generate_content(prompt)
        # Simple regex to get the first word, assuming LLM follows instructions
        mood = response.text.strip().lower()
        # Basic validation for expected moods
        if mood in ['happy', 'sad', 'stressed', 'angry', 'neutral', 'excited']:
            return mood
        else:
            # If LLM gives something unexpected, default to neutral
            return 'neutral'
    except Exception as e:
        print(f"Error in mood analysis: {e}")
        return "neutral" # Default to neutral on error

# --- Agent 2: Activity Suggester ---
def suggest_activity_agent(mood: str) -> str:
    """
    Agent 2: Suggests an activity based on a given mood.
    """
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    prompt = (
        f"You are an empathetic activity recommender. "
        f"Based on the user's mood being '{mood}', suggest a short, helpful activity. "
        f"For example, if 'sad', suggest 'listening to calming music and reflecting'. "
        f"If 'stressed', suggest 'taking a 10-minute walk outside'. "
        f"Be encouraging and concise.\n\n"
        f"Mood: '{mood}'\n"
        f"Activity Suggestion:"
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I couldn't suggest an activity. Error: {e}"

# --- Orchestration / Handoff Logic ---
def run_mood_handoff_system(user_message: str):
    """
    Simulates the Runner.run() concept for both agents and handles the handoff.
    """
    print(f"\nUser Message: \"{user_message}\"")

    # Agent 1 processes the message
    print("Agent 1 (Mood Analyzer) is at work...")
    mood_result = analyze_mood_agent(user_message)
    print(f"Mood Detected: {mood_result}")

    # Handoff condition
    if mood_result in ["sad", "stressed"]:
        print(f"Mood is '{mood_result}'. Handoff to Agent 2 (Activity Suggester)...")
        activity_suggestion = suggest_activity_agent(mood_result)
        print(f"Agent 2's Suggestion: {activity_suggestion}")
    else:
        print(f"Mood is '{mood_result}'. No specific activity suggestion needed for this mood.")

if __name__ == "__main__":
    print("Welcome to the Mood Analyzer with Handoff!")
    while True:
        message = input("How are you feeling today? (Type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        run_mood_handoff_system(message)
        print("-" * 50)