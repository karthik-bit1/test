# test

Simple Python example that calls GitHub Models Inference using the Azure AI Inference SDK.

## Prerequisites

- Python 3.10+
- A valid GitHub token with access to GitHub Models

## Setup

1. Create and activate a virtual environment:

	```bash
	python -m venv .venv
	source .venv/bin/activate
	```

2. Install dependencies:

	```bash
	pip install -r requirements.txt
	```

3. Create a `.env` file in the project root:

	```bash
	echo "GITHUB_TOKEN=<your_token>" > .env
	```

## Run

```bash
python AI.py
```

The script sends a sample prompt and prints the model response.
The script starts an interactive chat session and keeps conversation context.
Type `exit` or `quit` to stop.