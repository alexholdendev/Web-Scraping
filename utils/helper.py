from bs4 import BeautifulSoup
import requests

def get_soup(_url: str, _tag: str, _option: dict):
    _resp = requests.get(_url)
    _soup = BeautifulSoup(_resp.text, features="html.parser")
    _tag_list = _soup.find_all(_tag, _option)
    return _tag_list