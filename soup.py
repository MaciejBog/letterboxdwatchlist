from bs4 import BeautifulSoup
import requests
import json

class SoupMaker:
    def __init__(self, html):
        self.html = html
        self.soup = self.make_soup(self.html)
        self.page_number = self.check_for_multiple_pages()
        self.raw_data = self.get_raw_data(self.soup)
        self.title_list = self.get_titles(self.raw_data)
        self.link_list = self.get_links(self.raw_data)
        self.get_soup_if_multiple_pages()


    def check_for_multiple_pages(self):
        if self.soup.find(name="li", class_="paginate-page") is None:
            return 1
        else:
            raw_pages = self.soup.find_all(name="li", class_="paginate-page")
            pages_list = [page.find(name="a") for page in raw_pages]
            if pages_list[-1] is None:
                return 1
            highest_number = int(pages_list[-1].string)
            return highest_number

    def make_soup(self, html):
        try:
            response = requests.get(html)
        except requests.exceptions.RequestException:
            print("Error connecting!")
        raw_html = response.text
        soup = BeautifulSoup(raw_html, "html.parser")
        return soup

    def get_raw_data(self, soup):
        if soup.find(name="li", class_="poster-container numbered-list-item") is None:
            raw_films = soup.find_all(name="li", class_="poster-container")
        else:
            raw_films = soup.find_all(name="li", class_="poster-container numbered-list-item")
        return raw_films

    def get_links(self, raw_data):
        link_list = [("letterboxd.com" + film.find(name="div").get("data-target-link")) for film in raw_data]
        return link_list

    def get_titles(self, raw_data):
        title_list = [film.find(name="img").get("alt") for film in raw_data]
        return title_list

    def get_soup_if_multiple_pages(self):
        if self.page_number > 1:
            for page in range(2, self.page_number + 1):
                new_html = self.html + f"page/{page}/"
                new_soup = self.make_soup(new_html)
                new_raw_data = self.get_raw_data(new_soup)
                self.title_list.extend(self.get_titles(new_raw_data))
                self.link_list.extend(self.get_links(new_raw_data))

    def find_poster_image(self, html):
        soup = self.make_soup(html)
        script_w_data = soup.select_one('script[type="application/ld+json"]')
        json_obj = json.loads(script_w_data.text.split(' */')[1].split('/* ]]>')[0])
        image_link = json_obj['image']
        with open('pic1.jpg', 'wb') as handle:
            response = requests.get(image_link, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)




