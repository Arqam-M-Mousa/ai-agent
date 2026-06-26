import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types


def get_api_key() -> str:
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found")

    return api_key


def get_user_prompt() -> str:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    return args.user_prompt


def build_messages(prompt: str) -> list[types.Content]:
    return [
        types.Content(
            role="user",
            parts=[types.Part(text=prompt)],
        )
    ]


def generate_response(
    client: genai.Client,
    messages: list[types.Content],
):
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
    )


def print_response(response) -> None:
    if response.usage_metadata is None:
        raise RuntimeError("No usage metadata returned by Gemini API")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)


def main() -> None:
    client = genai.Client(api_key=get_api_key())

    prompt = get_user_prompt()
    messages = build_messages(prompt)

    response = generate_response(client, messages)

    print_response(response)

if __name__ == "__main__":
    main()
