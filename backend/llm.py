import os
import time

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


DEFAULT_MODEL = "openai/gpt-oss-120b"
MAX_RETRIES = 3
RETRY_DELAY = 2


def get_client():
    """Create and return the Groq client."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. "
            "Add GROQ_API_KEY to your .env file."
        )

    return Groq(
        api_key=api_key,
        timeout=60.0,
    )


def ask_llm(system_prompt, user_prompt):
    """
    Send a request to Groq with retry handling.

    Returns:
        str: Raw LLM response.
    """

    client = get_client()

    model = os.getenv(
        "GROQ_MODEL",
        DEFAULT_MODEL,
    )

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):

        try:

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=0.1,
            )

            if not response.choices:
                raise RuntimeError(
                    "Groq returned an empty response."
                )

            content = response.choices[0].message.content

            if not content:
                raise RuntimeError(
                    "Groq returned an empty message."
                )

            return content.strip()

        except Exception as exc:
            last_error = exc

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                raise RuntimeError(
                    "Groq AI analysis failed after "
                    f"{MAX_RETRIES} attempts: {last_error}"
                ) from last_error