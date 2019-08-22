import re
import requests
import zipfile
import io

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'This command downloads all available fixtures for stemp_abw'

    def add_argument(self, parser):
        pass

    def handle(self, *args, **options):
        FILES_URLS = [
            'https://zenodo.org/record/3374666/files/empty_fixture.zip',
            'https://zenodo.org/record/3374666/files/empty_fixture_error.zip',
        ]
        for file_url in FILES_URLS:
            r = requests.get(file_url)
            if r.ok:
                z = zipfile.ZipFile(io.BytesIO(r.content))
                z.extractall('stemp_abw/fixtures')
                d = r.headers['content-disposition']
                fname = re.findall("filename=(.+)", d)
                print(f"SUCCESS: File {fname[0]} was extracted to 'stemp_abw/fixtures'")
            else:
                print(f"ERROR:   {r}, could not load file from URL: {file_url}")
