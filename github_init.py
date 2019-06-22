# coding=utf-8

from urllib import parse

url_prefix = 'https://github.com/search?q='
param_split = '+'


def github_init():
    stars_array = [30000, 10000]
    languages = ['java', 'c', 'python', 'c++', 'c#', 'javascript', 'php', 'sql', 'swift', 'ruby', 'groovy',
                 'go', 'perl', 'r', 'dart', 'lua', 'scala', 'kotlin', 'typescript', 'shell', 'clojure']
    themes = ['ui']

    urls = []
    for stars in stars_array:
        for language in languages:
            url = 'stars' + parse.quote(':') + '>' + str(stars) + param_split + 'language' + parse.quote(
                ':' + language)
            urls.append(url_prefix + url)
            # print(url)
    return urls


if __name__ == '__main__':
    urls = github_init()
    for url in urls:
        print('curl ' + url)
