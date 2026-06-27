# ai-agent

A small Python-based AI coding agent that integrates with Google's GenAI (Gemini) to perform tool-enabled code inspection and execution workflows. It is designed for experiments with function-calling flows: the model can list files, read file contents, run Python files (with arguments), and write files. The repository also includes a simple calculator mini-app used by the agent for execution examples and tests.

## Stack
- Language(s): Python (100%)
- Framework / runtime: Python 3.14+ 
- Notable libraries:
  - google-genai (Gemini client)
  - python-dotenv (env file loading)

## Features
- Conversational orchestration around the Gemini model (model: `gemini-2.5-flash`).
- Declarative tool definitions exposed to the model:
  - get_files_info — list files and directories
  - get_file_content — read file contents
  - run_python_file — execute Python files with arguments
  - write_file — write/overwrite files
- Execution sandboxing: function calls are scoped by default to the `./calculator` working directory.
- Example subproject (calculator) with its own entrypoint and tests.

---

## How it's organized

Top-level layout:

```
.  
├── calculator/               # Mini-app: expression evaluator + tests
│   ├── main.py               # CLI entrypoint for calculator
│   ├── pkg/                  # Calculator package (logic + rendering)
│   ├── test_calculator.py    # Unit tests for calculator logic
│   └── tests.py              # Additional tests / examples
├── functions/                # Tool implementations & schemas exposed to Gemini
│   ├── available_functions.py
│   ├── call_functions.py     # Maps incoming function calls to implementations
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
├── main.py                   # Orchestrator: interacts with Gemini and the tools
├── prompts.py                # System prompt (instructions provided to the model)
├── pyproject.toml            # Project metadata & dependencies
├── uv.lock                   # Lock file (dependency lock)
├── tests/                    # Top-level test directory (if present)
└── README.md
```

How it fits together:
- `main.py` drives a conversation loop with the GenAI client. It builds messages, asks the model to generate content, inspects any function calls returned, dispatches those to local functions (in `functions/`), and feeds tool outputs back into the conversation until a final answer is produced or a max iteration limit is reached.
- `functions/` defines both the tool schemas exposed to the model (declaration) and the Python implementations that perform file listing, reading, writing, and running Python files.
- The `calculator/` subproject is a self-contained target used by the agent for running Python code as an example/sandbox.

---

## Quick start

Prerequisites:
- Python 3.14 or newer
- A Gemini API key (set as environment variable `GEMINI_API_KEY`)

Install (recommended inside a virtualenv):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
```

Or, for development editable install:

```bash
python -m pip install -e .
```

Create a `.env` file in the project root (or export env var) with:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## Usage

Agent (top-level)
- Basic usage:

```bash
python main.py "Summarize the repository structure"
```

- With verbose token / function-call info:

```bash
python main.py "Run the calculator to evaluate 3 + 5" --verbose
```

Notes:
- The agent uses the environment variable `GEMINI_API_KEY`. If it's not set a runtime error is raised.
- The agent runs up to 20 iterations (change `MAX_ITERS` in `main.py` if needed).
- Model configuration is set to use `gemini-2.5-flash` in `main.py`.

Calculator (standalone mini-app)
- Run the calculator CLI directly:

```bash
python calculator/main.py "3 + 5"
# Example output: JSON-formatted result printed to stdout
```

---

## Development notes & implementation details

- main orchestration:
  - main.py:
    - loads GEMINI API key via dotenv
    - constructs `types.Content` messages and calls `client.models.generate_content`
    - tools are provided through `functions.available_functions`
    - tool responses are handled by `functions.call_functions`
- tool dispatch:
  - `functions/call_functions.py` maps function call names to local implementations and injects a `working_directory` argument set to `./calculator`. This means tool executions operate by default on the calculator subproject — change this behavior carefully.
- prompts:
  - `prompts.py` includes the system prompt instructing the model about available operations and that file paths should be relative to the working directory.
- Security:
  - Running arbitrary code (the `run_python_file` tool) is potentially dangerous. The repository currently runs code within `./calculator` by default, but be cautious and audit any code before executing, especially when using the agent against untrusted inputs.
  - Consider stricter sandboxing, process isolation, or disabling execution in untrusted environments.

---

## Extending the agent

- Add new tools:
  - Define a schema/Tool declaration and implementation file in `functions/`.
  - Register the new function in `functions/available_functions.py`.
  - Update `functions/call_functions.py` to map the function name to the implementation.
- Change the agent’s working directory:
  - By default, `call_functions` injects `"working_directory": "./calculator"`. Modify this carefully to point elsewhere or to accept a configurable path.
- Adjust model/config:
  - `main.py` currently builds a `GenerateContentConfig` with `system_instruction` and the declared tools. Tune model name, temperature, and other generation settings as needed.

---

## Troubleshooting

- GEMINI_API_KEY errors: ensure `.env` exists or the environment variable is exported.
- Dependency errors: install packages from `pyproject.toml` (`google-genai==1.12.1`, `python-dotenv==1.1.0`) or perform an editable install.
- Unexpected or unsafe function outputs: inspect `functions/` implementations and the calculator code; execution is currently targeted to `./calculator`.

---

## Where to look next

- Orchestrator: `main.py`
- Tool dispatch and mapping: `functions/call_functions.py`
- Tool definitions: `functions/available_functions.py`
- Tool implementations: `functions/*.py`
- Sandbox example & tests: `calculator/`
