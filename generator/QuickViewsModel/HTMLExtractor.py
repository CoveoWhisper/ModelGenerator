import hashlib
import re
import requests
from bs4 import BeautifulSoup


class HTMLExtractor:
    def __init__(self):
        self.visitedFiles = set()

    def extract_from_file_path(self, path, headers={}):
        try:
            response = requests.get(path, headers=headers, allow_redirects=True)
        except requests.exceptions.InvalidSchema as e:
            print("Invalid schema for Uri: " + path)
            return None
        except Exception as e:
            print("Exception happened for Uri: " + path)
            return None

        if response.status_code != 200:
            return None

        fileHash = hashlib.sha256(response.content).hexdigest()
        if fileHash in self.visitedFiles:
            return None
        self.visitedFiles.add(fileHash)

        soup = BeautifulSoup(response.content.decode(response.encoding, 'ignore'), features='html.parser')
        data = soup.findAll(text=True)
        result = filter(visible, data)
        return ' '.join(result)


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True
