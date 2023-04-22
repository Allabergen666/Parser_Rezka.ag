from bs4 import BeautifulSoup
from dotenv import load_dotenv
from os import getenv, system
import requests, json
load_dotenv()
system("clear")


URL = getenv("URL")
DOMEN = getenv("DOMEN")
HEADRES = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.1.906 (beta) Yowser/2.5 Safari/537.36"
}


def get_html(Url=URL, Headres=HEADRES):
    response = requests.get(url=Url, headers=Headres)
    if response.status_code == 200:
        return response.text
    else:
        return f"Error in code{response.status_code}"


def get_content(html):
    soup = BeautifulSoup(html, "lxml").find("div", {"class":"b-content__inline_items"}).find_all("div", {"class":"b-content__inline_item"})

    film_informations = {}

    for item in soup:
        film_photo = item.find("img").get("src")
        film_title = item.find("div", {"class": "b-content__inline_item-link"}).find("a").text
        film_url = item.find("div", {"class": "b-content__inline_item-link"}).find("a").get("href")
        film_category = item.find("div", {"class": "b-content__inline_item-link"}).find("a").text
        
        film_informations.update({
            film_title:{
                "photo":film_photo,
                "url": film_url,
                "category": film_category,
            }
        })
    return film_informations   


def pars():
    html = get_html()
    content =  get_content(html)
    with open("core/json/content.json", "w") as file:
        json.dump(content,file,indent=4, ensure_ascii=False)
    return "Ready!"
    # html = get_html()
    # get_content(html)

print(pars())

