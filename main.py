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

    parser.add_argument("user_prompt", type=str)
    parser.add_argument("--verbose", action="store_true")

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


def handle_response(response, verbose: bool):
    if response.usage_metadata and verbose:
        print(f"prompt_tokens={response.usage_metadata.prompt_token_count}")
        print(f"output_tokens={response.usage_metadata.candidates_token_count}")

    function_calls = getattr(response, "function_calls", None)

    if not function_calls:
        return None  # signals final answer

    function_results = []

    for function_call in function_calls:
        result = call_function(function_call, verbose=verbose)

        if not result.parts:
            raise RuntimeError("Tool returned empty parts")

        part = result.parts[0]
        fn_response = part.function_response

        if fn_response is None or fn_response.response is None:
            raise RuntimeError("Invalid tool response")

        function_results.append(part)

        if verbose:
            print(f"-> {fn_response.response}")

    return function_results


def main():
    args = parse_args()
    client = genai.Client(api_key=get_api_key())

    messages = build_messages(args.user_prompt)

    MAX_ITERS = 20

    for _ in range(MAX_ITERS):

        response = generate_response(client, messages)

        # 1. append model candidates (critical memory step)
        if response.candidates:
            for c in response.candidates:
                if c.content:
                    messages.append(c.content)

        # 2. handle tools
        tool_results = handle_response(response, args.verbose)

        # 3. final answer case
        if tool_results is None:
            print(response.text)
            return

        # 4. feed tool results back into conversation
        messages.append(
            types.Content(
                role="user",
                parts=tool_results
            )
        )

    print("Error: max iterations reached without final answer")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
