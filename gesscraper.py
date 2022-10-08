import requests as r
from bs4 import BeautifulSoup
import time
from random import choice
import sys
from csv import writer


def scrape_url(url):

    global url_page

    with open("quotes.csv", "w", newline="") as f:
        csvw = writer(f)
        csvw.writerow(["Quote", "Author", "Bio"])

    while url_page:

        answer = r.get(f"{url}{url_page}")
        soup = BeautifulSoup(answer.text, "html.parser")
        quotes = soup.find_all(class_="quote")
        next_btn = soup.find(class_="next")
        url_page = next_btn.find("a")["href"] if next_btn else None

        with open("quotes.csv", "a", newline="") as f:
            csvw = writer(f)
            for quote in quotes:
                text = quote.find(class_="text").get_text()
                author = quote.find(class_="author").get_text()
                bio_link = quote.find("a")["href"]
                fullbio = url + bio_link
                try:

                    csvw.writerow([text, author, fullbio])
                except UnicodeError:
                    pass
                ###DATA-LIST###
                data_list.append([text, author, fullbio])

        if url_page:
            print(f"Scrapring {url}{url_page}")
        else:
            pass
    print("Scrapping DONE!")
    return data_list


def guess_quote():

    count = 0
    random_quote = choice(data_list)

    while count < 4:

        print(random_quote[0])
        answer = input("whos said that shit: ")
        if answer.lower() == random_quote[1].lower():
            print("YOU WON !!!!!!!!!!!!!!")
            sys.exit()
        else:
            count += 1
            delta = 4 - count

            author_raw = r.get(random_quote[2])
            author = BeautifulSoup(author_raw.text, "html.parser")
            # example: March 14, 1986
            date = author.find(class_="author-born-date").get_text()
            # ex: in Paris france
            location = author.find(class_="author-born-location").get_text()
            if delta != 0:
                print(f"NOP ! You have {delta} more trials remaining.")
            else:
                pass
            time.sleep(1)
            if count == 1:
                print(f"""Hint 1: Born on {date} in {location}.""")
                time.sleep(1)
            elif count == 2:
                name_list = random_quote[1].split()
                initials1 = [x[0] for x in name_list]
                initials = ".".join(initials1)
                print(f"""Hint 2: Initials -> {initials}.""")
                time.sleep(1)
            elif count == 3:
                print(f"""Hint 3: First name -> {name_list[0]}.""")
                time.sleep(1)
            else:
                print(f"Better Luck Next Time ! The answer was {random_quote[1]}.")
    sys.exit()


url = "http://quotes.toscrape.com"
url_page = "/"
data_list = []

print("Scrapping The Quotes Database...")
scrape_url(url)


###QUOTE_LIST###
quotes_list = [q[0] for q in data_list]

guess_quote()
