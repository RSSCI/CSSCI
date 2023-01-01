import time
import math
import json
import requests
from lxml import etree

url = "https://navi.cnki.net/knavi/journals/searchbaseinfo"

headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}

searchStateJson = {
    "StateID": "",
    "Platfrom": "",
    "QueryTime": "",
    "Account": "knavi",
    "ClientToken": "",
    "Language": "",
    "CNode": {"PCode": "JOURNAL", "SMode": "", "OperateT": ""},
    "QNode": {
        "SelectT": "",
        "Select_Fields": "",
        "S_DBCodes": "",
        "QGroup": [
            {
                "Key": "Navi",
                "Logic": 1,
                "Items": [],
                "ChildItems": [
                    {
                        "Key": "journals",
                        "Logic": 1,
                        "Items": [
                            {
                                "Key": "datasource",
                                "Title": "",
                                "Logic": 1,
                                "Name": "EI",
                                "Operate": "",
                                "Value": "0010?",
                                "ExtendType": 0,
                                "ExtendValue": "",
                                "Value2": "",
                            }
                        ],
                        "ChildItems": [],
                    }
                ],
            }
        ],
        "OrderBy": "OTA|DESC",
        "GroupBy": "",
        "Additon": "",
    },
}

payload = {
    "searchStateJson": json.dumps(searchStateJson),
    "displaymode": 1,
    "pageindex": 1,
    "pagecount": 21,
    "index": "datasource",
    "searchType": "刊名(曾用刊名)",
    "clickName": "CSSCI 中文社会科学引文索引(2021-2022)来源期刊(扩展版)",
    "switchdata": "leftnavi",
}

journalDict = {}

print("started!")

# 第一页
response = requests.post(url, data=payload, headers=headers)
html = etree.HTML(response.text)
totalcount = html.xpath('number(//span[@class="totalcount"]/em)')
journals = html.xpath('//ul[@class="list_tup"]/li')
for journal in journals:
    code = journal.xpath("string(a/@href)")[-4:]
    name = journal.xpath("string(a/@title)").strip()
    journalDict.update({code: name})
print("finished page 1")
time.sleep(3)

pageTotal = math.floor(totalcount / payload["pagecount"] + 2)

# 后续页
for pageNo in range(2, pageTotal):
    payload["pageindex"] = pageNo
    response = requests.post(url, data=payload, headers=headers)

    html = etree.HTML(response.text)
    journals = html.xpath('//ul[@class="list_tup"]/li')
    for journal in journals:
        code = journal.xpath("string(a/@href)")[-4:]
        name = journal.xpath("string(a/@title)").strip()
        journalDict.update({code: name})
    print("finished page " + str(pageNo))
    time.sleep(3)

print("finished!")

json_object = json.dumps(journalDict, indent=4)
journalCount = len(json.loads(json_object))

print("total number: " + str(journalCount))

if journalCount == totalcount:
    with open("cssci-expanded/cssci-expanded.json", "w", encoding="utf-8") as f:
        f.write(json_object)
else:
    print("something wrong!")
