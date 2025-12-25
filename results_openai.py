from langchain_core.tools import tool
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
openai_api_key = os.getenv("OPEN_AI_KEY")


def get_llm_response(prompt: str) -> str:
    """Function to get response from LLM"""
    client_llm = OpenAI(api_key=openai_api_key)
    response = client_llm.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

## testing the LLM response
prompt = "Explain the theory of relativity in simple terms in 30 words"
response = get_llm_response(prompt)

print(response)


### Results from the OpenAI API:
"""Relativity says motion and measurements depend on the observer.
 Light's speed is constant. Time and space bend with gravity and energy,
  connecting matter, energy, and geometry into one physics description"""