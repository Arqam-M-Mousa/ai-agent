import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.call_functions import call_function
from functions.available_functions import available_functions


def parse_args():
    parser = argparse.ArgumentParser(description="Chatbot")

    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    return parser.parse_args()


def get_api_key() -> str:
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found")

    return api_key


def build_messages(prompt: str):
    return [
        types.Content(
            role="user",
            parts=[types.Part(text=prompt)],
        )
    ]


def generate_response(client, messages):
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )


def print_output(response, verbose: bool, user_prompt: str):
    if response.usage_metadata is None:
        raise RuntimeError("No usage metadata returned by Gemini API")

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    function_calls = getattr(response, "function_calls", None)

    if function_calls:
        function_results = []

        for function_call in function_calls:
            function_call_result = call_function(function_call, verbose=verbose)

            if not function_call_result.parts:
                raise RuntimeError("Tool returned empty parts")

            fn_response = function_call_result.parts[0].function_response
            if fn_response is None or fn_response.response is None:
                raise RuntimeError("Invalid tool response")

            function_results.append(function_call_result.parts[0])

            if verbose:
                print(f"-> {fn_response.response}")

        return function_results

    print(response.text)


def main():
    args = parse_args()

    client = genai.Client(api_key=get_api_key())

    messages = build_messages(args.user_prompt)

    response = generate_response(client, messages)

    print_output(response, args.verbose, args.user_prompt)


if __name__ == "__main__":
    main()
