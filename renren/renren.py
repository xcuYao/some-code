import requests
import re
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import json


def findAreaSchools(code):
    rsp = requests.get('http://support.renren.com/juniorschool/' + code +
                       '.html')
    parser = HTMLParser()
    if rsp.status_code != 200:
        print("request error!")
        return ""
    else:
        content = parser.unescape(rsp.content.decode("utf-8"))

    soup = BeautifulSoup(content, "html.parser")
    alinks = soup.find_all('a', href='#highschool_anchor')
    dic = {}
    for alink in alinks:
        key = re.findall('\'(.*)\'', alink['onclick'])[0]
        value = alink.text
        dic[key] = value

    result = []
    for key in dic.keys():
        name = dic[key]
        items = soup.find(id=key).find_all('a')
        names = []
        for item in items:
            names.append(item.text)
        d1 = {}
        d1["area"] = name
        d1["scholls"] = names
        result.append(d1)
    return result


def main():
    f = open('./area.json', 'r')
    bigArray = json.loads(f.read())
    index = 0
    for array in bigArray:
        content = []
        for item in array:
            dic = {}
            values = item.split(':', 1)
            scholls = findAreaSchools(values[0])
            dic["area"] = values[1]
            dic["data"] = scholls
            content.append(dic)
        f2 = open('./data/' + str(index) + '.json', 'w+')
        f2.write(json.dumps(content))
        f2.close()
        print("-----" + str(index) + " ok -----")
        index += 1
    f.close()
    print("over")


if __name__ == '__main__':
    main()