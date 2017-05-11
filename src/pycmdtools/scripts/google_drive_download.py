import click
import requests

"""
This script downloads stuff from google drive.

References:
- http://stackoverflow.com/questions/25010369/wget-curl-large-file-from-google-drive
"""


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


@click.command()
@click.argument('permalink', required=True, type=str)
@click.argument('destination', required=True, type=str)
def main(permalink: str, destination: str) -> None:
    download_file_from_google_drive(permalink, destination)

if __name__ == '__main__':
    main()
