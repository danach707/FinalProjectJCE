import requests
import re
import sys


if __name__ == '__main__':

    linkedinDomain = sys.argv[0]

    r = requests.get(linkedinDomain)
    print(r.content)
    result = re.findall('<p class="badge-preview__name">(\w*)</p>', r.text)
    print(result)

