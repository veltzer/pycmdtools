import click
import requests
from pylogconf import setup

"""
This script downloads stuff from google drive.
If you have a link to a google drive file like this:
    https://drive.google.com/open?id=0BwNoUKizWBdnRmRmLVlWSWxzWnM
or like this:
    https://drive.google.com/file/d/0BwNoUKizWBdnSHF4SFlyRkxNSVE/view?usp=sharing
Then the file id of the relevant files are:
    0BwNoUKizWBdnRmRmLVlWSWxzWnM
    0BwNoUKizWBdnSHF4SFlyRkxNSVE
And this is what you have to supply to this script to download the files.

References:
- http://stackoverflow.com/questions/25010369/wget-curl-large-file-from-google-drive
"""


def download_file_from_google_drive(file_id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
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
@click.argument(
    'file_id',
    required=True,
)
@click.argument(
    'destination',
    required=True,
)
def main(
        file_id: str,
        destination: str,
) -> None:
    """
    Download a file from a google drive using it's id.
    :param file_id: 
    :param destination: 
    :return: 
    """
    setup()
    download_file_from_google_drive(file_id, destination)

if __name__ == '__main__':
    main()
