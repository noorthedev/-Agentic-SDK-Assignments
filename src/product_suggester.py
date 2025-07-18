import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def create_product_suggester_agent():
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 512,
        }
    )
    return model

def suggest_product(user_need: str) -> str:
    model = create_product_suggester_agent()
    prompt = (
        "You are a helpful smart store agent. Suggest a product based on user's need.\n\n"
        "Example:\n"
        "User: 'I have a headache'\n"
        "Agent: 'You might consider ibuprofen. It's an anti-inflammatory for pain relief.'\n\n"
        f"User: '{user_need}'\nAgent:"
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("Smart Store Agent")
    while True:
        user_input = input("Need help finding a product? (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        print(suggest_product(user_input))
        print("-" * 30)
