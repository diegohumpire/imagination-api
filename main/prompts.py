import os
import json
import logging

from openai import OpenAI

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)


def generate_prompts_json() -> dict:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """Give me a list of 6 examples of prompts that you can use to generate creative images.
                Each prompt text must have 15 words at least.
                Do it in JSON format, each object must have a title and text field inside 'prompts' key.
                Each prompt must be in spanish."""
            }
        ],
        temperature=0.4,
        max_tokens=800,
        frequency_penalty=1.0,
        presence_penalty=0.5,
    )

    logging.info(completion.choices[0].message.content)

    data = json.loads(completion.choices[0].message.content)

    return data


def generate_prompts() -> list:
    tries = 1
    data = generate_prompts_json()

    logging.info(f"------ Try: {tries}")

    while "prompts" not in data and not isinstance(data["prompts"], list):
        tries += 1
        data = generate_prompts_json()
        logging.info(f"------ Try: {tries}")

    return data.get("prompts", [])


def generate_image(prompt_from_user: str) -> str | None:
    # random_prompt = "Create a random image of a cat with a hat and a monocle."
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt_from_user,
        size="512x512",
        quality="standard",
        n=1
    )

    image_url = response.data[0].url

    logging.info(image_url)

    return image_url
