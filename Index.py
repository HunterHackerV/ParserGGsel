from bs4 import BeautifulSoup
import requests as rq
import json
def parsing():
    counter = 0
    htmlCodeProducts = ""
    while True:
        url = f"https://ggsel.com/games-filter-ajax?page={counter}&sort=SUMMPAY&category=1085"
        htmlcode = json.loads(rq.get(url).text)
        if htmlcode["html"] != "":
            htmlCodeProducts += str(htmlcode["html"]).replace("\n", "")
            print(counter)
        else:
            break
        counter += 1
    file = open("result.txt", "w", encoding='utf-8')
    file.writelines(htmlCodeProducts)
    file.close()
def filter():
    file = open("result.txt", "r", encoding='utf-8')
    games = {}
    games["game"] = []
    fileText = file.read().replace("product-item yellow load ", "yellow").replace("product-item violet load ", "yellow")
    htmlcode = BeautifulSoup(fileText, "html.parser")
    for game in htmlcode:
        typeStr  = ""
        if game.find("span", class_="product-item-cat").text.replace("\n",  "").replace(" ", "") == "ключ":
            typeStr = "key"
        elif game.find("span", class_="product-item-cat").text.replace("\n",  "").replace(" ", "") == "другое":
            typeStr = "other"
        elif game.find("span", class_="product-item-cat").text.replace("\n",  "").replace(" ", "") == "аккаунт":
            typeStr = "akk"
        games["game"].append({
            "name": game.find("a", class_="product-item-descr").text,
            "href": game.find("a", class_="product-item-descr")["href"],
            "type": typeStr,
            "price": game.find("div", class_="cost").text
        })
    
    with open('data.json', 'w') as outfile:
        json.dump(games, outfile)
if __name__ == '__main__':
    filter()