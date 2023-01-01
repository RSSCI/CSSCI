import time
import json
import requests
from lxml import etree

journalInfoDict = {}

with open("cssci-expanded/cssci-expanded.json") as f:
    data = json.load(f)
    keys = list(data.keys())
    length = len(keys)

for i in range(length):
    key = keys[i]
    journalInfoDict.update({key: {}})

    # url
    url = "https://navi.cnki.net/knavi/journals/{}/detail".format(key)
    journalInfoDict[key]["url"] = url

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)

    # title
    title = html.xpath("string(/html/head/title)").strip()
    journalInfoDict[key]["title"] = title

    # publish types
    publishType = list(
        map(
            lambda item: item.strip(),
            html.xpath(
                '//*[@id="qk"]/div[2]/dl/dd/p[@class="journalType journalType1"]/span/descendant-or-self::*/text()'
            ),
        )
    )
    journalInfoDict[key]["type"] = publishType

    # included in databases
    database = list(
        map(
            lambda item: item.strip(),
            html.xpath(
                '//*[@id="qk"]/div[2]/dl/dd/p[@class="journalType journalType2"]/span/descendant-or-self::*/text()'
            ),
        )
    )
    journalInfoDict[key]["database"] = database

    # journal base info
    baseInfoKey = html.xpath('//*[@id="JournalBaseInfo"]/li/p/label/text()')
    baseInfoVal = html.xpath('//*[@id="JournalBaseInfo"]/li/p/span/text()')
    baseInfoNo = len(baseInfoKey)
    for i in range(baseInfoNo):
        journalInfoDict[key][baseInfoKey[i]] = baseInfoVal[i]

    # publish info
    publishInfoKey = html.xpath(
        '//*[@id="publishInfo"]/li/descendant-or-self::*/p/label/text()'
    )
    publishinfoVal = html.xpath(
        '//*[@id="publishInfo"]/li/descendant-or-self::*/p/span/text()'
    )
    publishinfoNo = len(publishInfoKey)
    for i in range(publishinfoNo):
        journalInfoDict[key][publishInfoKey[i]] = publishinfoVal[i]

    # evaluate info
    evaluateInfoKey = html.xpath(
        '//*[@id="evaluateInfo"]/li[2]/p[position()<3]/label/text()'
    )
    evaluateInfoVal = html.xpath(
        '//*[@id="evaluateInfo"]/li[2]/p[position()<3]/span/text()'
    )
    if len(evaluateInfoKey) == len(evaluateInfoVal):
        for i in range(len(evaluateInfoKey)):
            journalInfoDict[key][evaluateInfoKey[i]] = evaluateInfoVal[i]
    else:
        pass

    # print info
    print("finished {}: {}".format(key, title))

    # sleep 3 seconds
    time.sleep(3)

json_object = json.dumps(journalInfoDict, indent=4)
journalCount = len(json.loads(json_object))

print("total number: " + str(journalCount))

if journalCount == length:
    with open("cssci-expanded/cssci-expanded_info.json", "w", encoding="utf-8") as f:
        f.write(json_object)
else:
    print("something wrong!")
