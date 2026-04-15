import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from dotenv import load_dotenv

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"


def main() -> int:
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    messages = [SystemMessage("You are a helpful assistant.")]
    print("Interactive chat started. Type 'exit' or 'quit' to stop.")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        messages.append(UserMessage(user_input))

        try:
            response = client.complete(
                messages=messages,
                temperature=1.0,
                top_p=1.0,
                model=model,
            )
        except AzureError as exc:
            print(f"Request failed: {exc}")
            messages.pop()
            continue
        except Exception as exc:
            print(f"Unexpected error: {exc}")
            messages.pop()
            continue

        choices = getattr(response, "choices", None)
        if not choices:
            print("Error: No response choices returned by the API.")
            messages.pop()
            continue

        content = getattr(choices[0].message, "content", None)
        if not content:
            print("Error: Empty response content returned by the API.")
            messages.pop()
            continue

        print(f"Assistant: {content}\n")
        messages.append(AssistantMessage(content))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

