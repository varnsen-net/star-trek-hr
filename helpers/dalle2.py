import os
import dotenv

import openai
import base64

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def fetch_dalle_response(scene_text):
    """Fetches an image from DALL-E using the OpenAI API.

    :param str scene_text: The scene to generate an image for.
    :return: OpenAI response.
    :rtype: dict
    """
    prompt = f"black and white pixel art of the following scene: {scene_text}"
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size='512x512',
        response_format='b64_json'
    )
    return response


def extract_dalle_image(response):
    """Extracts the b64 image from the OpenAI API response.

    :param dict response: The OpenAI API response.
    :return: PIL image.
    :rtype: PIL.Image.Image
    """
    image_data = response['data'][0]['b64_json']
    image = base64.b64decode(image_data)
    return image


if __name__ == '__main__':
    response = fetch_dalle_response("captain picard relaxing on risa.")
    image = extract_dalle_image(response)
    with open('image.png', 'wb') as f:
        f.write(image)


# response = response['data'][0]['url']
# print(response)

# send response to output.html
# with open('output.txt', 'w') as f:
    # f.write(response)
