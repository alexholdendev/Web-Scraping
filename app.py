from email import header
import re
import json

import pandas
import requests

from utils import helper

url = "https://www.academia.edu/"

category_tag_list = helper.get_soup(url, "div", {"class": "research-interest-section-container"})
paper_list = []
for category_tag in category_tag_list:
    category = category_tag.div.h2.text
    paper_tag_list = category_tag.find_all("div", attrs={"class":"research-interest-list-item"})
    for paper_tag in paper_tag_list:
        sub_category_link = paper_tag.a["href"]
        sub_category_link = url + sub_category_link[1:]
        sub_category = paper_tag.a.div.text
        page_source = requests.get(sub_category_link).text
        sub_paper_list = re.findall(r"work: (\{.+),", page_source, re.MULTILINE)
        for sub_paper in sub_paper_list:
            paper_dict = json.loads(sub_paper)
            paper_list.append({
                "category": category,
                "sub-category": sub_category,
                "sub-category-link": sub_category_link,
                "title": paper_dict["title"],
                "author": paper_dict["ordered_authors"][0]["display_name"],
                "keywords": [x["name"] for x in paper_dict["research_interests"]],
            })
    
df = pandas.DataFrame(paper_list)
df.to_csv("full_paper.csv", index=False, header=True, encoding="utf-8")
df.drop(columns = ["category", "sub-category", "sub-category-link"], inplace=True)
df.to_csv("paper.csv", index=False, header=True, encoding="utf-8")
