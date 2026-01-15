from base64 import b64encode
from bs4 import BeautifulSoup
from itertools import product
from time import sleep


import requests
import random


# 教务账密
username = 'jwgl'
password = 'pswd'

# 基本配置
baseurl = "https://jwgl.bupt.edu.cn"
session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
encoded = b64encode(str(username).encode()).decode() + r"%%%" + b64encode(str(password).encode()).decode()
session.post("https://jwgl.bupt.edu.cn/jsxsd/xk/LoginToXk", data={"encoded": encoded})

# 教学评价 -> 学生评价
url = "https://jwgl.bupt.edu.cn/jsxsd/xspj/xspj_find.do"
resp = session.get(url)
soup = BeautifulSoup(resp.content, "lxml")
element = soup.select_one('#Form1 table tr:nth-of-type(2) td:nth-of-type(7) a')
if element is None or element.get("href") is None:
    print("fail 1")
    exit()
else:
    url = baseurl + str(element.get("href"))

# 评教课程列表
resp = session.get(url)
soup = BeautifulSoup(resp.content, "lxml")
table = soup.find("table", id="dataList")
if not table:
    print("fail 2")
    exit()
rows = table.find_all("tr")[1:]
results = []
for i, row in enumerate(rows):
    tds = row.find_all("td", recursive=False)
    item_id = tds[1].get_text(strip=True)
    label = tds[2].get_text(strip=True)
    is_submit = tds[7].get_text(strip=True) == "是"
    a_tag = tds[8].find("a", recursive=False)
    if a_tag is None:
        print("fail 3")
        exit()
    results.append({
        "id": item_id,
        "label": label,
        "submit": is_submit,
        "url": baseurl + str(a_tag.get("href"))
    })
pj = soup.find('input', {'id': 'pj01id'})
if pj is None:
    print("fail 3")
    exit()
form = soup.find("form", id="Form1")
if form is None:
    print("fail 3.1")
    exit()
submit_url = f"{baseurl}/jsxsd/xspj/xspj_yjtj.do?pj01id={str(pj.get('value'))}"
submit_data = []
for inp in form.find_all("input", type="hidden"):
    name = inp.get("name")
    value = inp.get("value", "")
    if name:
        submit_data.append((name, value))
    else:
        print(f"invalid hidden input {name}")

# 评教
for course in results:
    url = course["url"]
    save_url = "https://jwgl.bupt.edu.cn/jsxsd/xspj/xspj_save.do"
    label = course["label"]
    is_submit = course["submit"]
    score = random.randint(86, 94)  # 避免评语
    if is_submit:
        print(f"{label}已提交")
        continue
    print(f"评教：{label}，期望{score}分")
    resp = session.get(url)
    soup = BeautifulSoup(resp.content, "lxml")

    form = soup.find("form", id="Form1")
    if form is None:
        print("fail 5")
        exit()
    
    data = []
    # 隐藏项
    for inp in form.find_all("input", type="hidden"):
        name = inp.get("name")
        value = inp.get("value", "")
        if name:
            data.append((name, value))
        else:
            print(f"invalid hidden input {name}")
    
    # 两段主观评价
    for i, (key, _) in enumerate(data):
        if key == 'pj03id':
            data.insert(i + 1, ("jynr", ""))

    # 主观评语(zgpyids)
    for i, (key, _) in enumerate(data):
        if key == 'pj03id':
            zgpyids = soup.find_all("input", type="checkbox", attrs={"name": "zgpyids"})
            for cb in zgpyids[:10]:  # 勾选前10个
                data.insert(i, ("zgpyids", cb["value"]))
            break

    # 单选题(zbtd)
    # 每题选择最高分两项之一，暴力穷举所有可能性，使得总分为前述期望分
    items = []
    groups = {}
    for key, val_str in data:
        if key.startswith('pj0601fz'):
            parts = key.split('_') 
            value = float(val_str)
            b_part = parts[1]
            items.append((key, value, b_part))
            groups.setdefault(b_part, []).append((key, value))

    candidate_pool = []
    for b in sorted(groups.keys()):
        top2 = sorted(groups[b], key=lambda x: x[1], reverse=True)[:2]
        candidate_pool.append(top2)

    for combination in product(*candidate_pool):
        total = sum(item[1] for item in combination)
        if int(total) == score:
            print(f"最终得分{total:.2f}\n")
            # 选项插入到表单
            key_to_first_index = {}
            for idx, (k, v) in enumerate(data):
                if k not in key_to_first_index:
                    key_to_first_index[k] = idx

            insertions = []
            for key, _ in combination:
                parts = key.split("_")
                new_key = f"pj0601id_{parts[1]}"
                new_value = parts[2]
                pos = key_to_first_index[key]
                insertions.append((pos, (new_key, new_value)))
            insertions.sort(key=lambda x: x[0], reverse=True)
            for pos, item in insertions:
                data.insert(pos, item)
            break

    resp = session.post(save_url, data=data, headers={"Referer": url})
    sleep(random.randint(1, 5))

session.post(submit_url, data=submit_data)
print("已提交")
