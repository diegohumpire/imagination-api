import os
import json
import logging

from fastapi import HTTPException, status
from openai import OpenAI

from main.services.cache import ICacheService, RedisCacheService

CACHE_PROMPTS_KEY = "prompts"
CACHE_IMAGES_GENERATED_KEY = "images"
TTL_IMAGES_GENERATED = 1800

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)

cache_service: ICacheService = RedisCacheService()


def __cache_prompt_key_by_session(uuid: str) -> str:
    return f"{CACHE_PROMPTS_KEY}:{uuid}"


def __save_prompts_in_cache(key: str, prompts: list) -> None:
    cache_service.save(__cache_prompt_key_by_session(key), json.dumps(prompts))


def __exists_prompts_in_cache(key: str) -> bool:
    return cache_service.exists(__cache_prompt_key_by_session(key))


def __get_prompts_from_cache(key: str) -> list:
    return json.loads(cache_service.get(__cache_prompt_key_by_session(key)))


def __generate_prompts_json() -> dict:
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
        n=1
    )

    logging.info(completion.choices[0].message.content)

    data = completion.choices[0].message.content

    return json.loads(data)


def generate_prompts(session_uuid: str) -> list:
    if __exists_prompts_in_cache(session_uuid):
        return __get_prompts_from_cache(session_uuid)

    tries = 1
    data = __generate_prompts_json()

    logging.info(f"------ Try: {tries}")

    while "prompts" not in data and not isinstance(data["prompts"], list):
        if tries == 3:
            raise HTTPException(
                status.HTTP_504_GATEWAY_TIMEOUT, "Error generating prompts")

        tries += 1
        data = __generate_prompts_json()
        logging.info(f"------ Try: {tries}")

    prompts: list = data.get("prompts", [])

    __save_prompts_in_cache(session_uuid, prompts)

    return prompts


def __cache_images_key_by_session(uuid: str) -> str:
    return f"{CACHE_IMAGES_GENERATED_KEY}:{uuid}"


def __exists_images_in_cache(key: str) -> bool:
    return cache_service.exists(__cache_images_key_by_session(key))


def __get_images_from_cache(key: str) -> list:
    return json.loads(cache_service.get(__cache_images_key_by_session(key)))


def __add_images_in_cache(key: str, image_url: str) -> None:
    if not __exists_images_in_cache(key):
        cache_service.set_ttl(TTL_IMAGES_GENERATED).save(
            __cache_images_key_by_session(key), json.dumps([image_url]))
    else:
        images = __get_images_from_cache(key)
        images.append(image_url)
        cache_service.set_ttl(TTL_IMAGES_GENERATED).save(
            __cache_images_key_by_session(key), json.dumps(images))


def generate_image(prompt_from_user: str, session_uuid: str) -> str | None:
    if __exists_images_in_cache(session_uuid):
        images = __get_images_from_cache(session_uuid)

        if len(images) == 3:
            raise HTTPException(
                status.HTTP_429_TOO_MANY_REQUESTS, "You have reached the limit of images generated")

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

    __add_images_in_cache(session_uuid, image_url)

    return image_url


def get_images(session_uuid: str) -> list:
    if __exists_images_in_cache(session_uuid):
        return __get_images_from_cache(session_uuid)

    return []
