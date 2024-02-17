import glob
import re

import requests
from lxml.html.clean import Cleaner


def main():
    with open('sites.txt') as f:
        urls = f.readlines()

    i = 0
    for url in urls:
        i += 1
        url = re.sub(r"[\n\t\s]*", "", url)
        response = requests.get(url).content

        cleaner = Cleaner()
        cleaner.javascript = True
        cleaner.style = True

        response = cleaner.clean_html(response)
        filename = 'выкачка/%s-%s.html' % (str(i), url[18:])
        with open(filename, "wb") as htmlFile:
            htmlFile.write(response)

        with open("index.txt", "a") as indexFile:
            line = '%s-%s.html %s \n' % (str(i), url[18:], url)
            indexFile.write(line)

        read_files = glob.glob("выкачка/*.html")

        with open("выкачка.html", "wb") as outfile:
            for f in read_files:
                with open(f, "rb") as infile:
                    outfile.write(infile.read())


if __name__ == "__main__":
    main()
