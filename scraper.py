from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from teoria import Progression
import re

class Link:
    def __init__(self, url):
        self.url = url
        self._request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        self._html = urlopen(self._request).read().decode("utf-8")
        self.soup = BeautifulSoup(self._html, "html.parser")

class LaCuerda(Link):
    def __init__(self, url):
        super().__init__(url)
        self.chords = self.soup.find(id="t_body").find_all("a")
        self.chord_list = [x.get_text() for x in self.chords]
        self.prog = Progression(self.chord_list)
        self.__add_to_lyrics()

    def __add_to_lyrics(self):
        for x,y in zip(self.chords, self.prog.analysis):
            x.string = x.get_text() + " (" + y + ") "

    def print_page(self):
        print(self.soup.find(id="t_body").get_text())

class AcordesDCanciones(Link):
    def __init__(self, url):
        super().__init__(url)
        self.chords = self.soup.find(itemprop="articleBody").select('[style*="color: red"]')
        self.chord_list = self.get_chords()
        self.prog = Progression(self.chord_list)

    def get_chords(self):
        chords = [re.sub("\\xa0", "", x.get_text()) for x in self.chords]
        chords = " ".join(chords)
        return chords
    
class UltimateGuitar(Link):
    def __init__(self, url):
        super().__init__(url)
        self.chord_list = self.get_chords()
        self.prog = Progression(self.chord_list)

    def get_chords(self):
        chords = str(self.soup.select('[class*="js-store"]')[0])
        chords = re.findall(r"\[ch\](.{1}|.{2}|.{3}|.{4}|.{5}|.{6}|.{7}|.{8}|.{9}|.{10})\[/ch\]", chords)
        return chords


# url = "https://acordes.lacuerda.net/charly_garcia/cuando_ya_me_empiece_a_quedar_solo.shtml"
# url = "https://www.acordesdcanciones.com/2019/11/soy-lo-que-soy-sandra-mihanovich.html"
# url = "https://tabs.ultimate-guitar.com/tab/bruno-mars/when-i-was-your-man-chords-1198871"
# if "acordes.lacuerda.net" in url:
#     w1 = LaCuerda(url)
#     w1.print_page()
#     w1.prog.is_in_prog(["V/VI", "VI"])
# elif "acordesdcanciones" in url: ## Tengo que cranear como printear la página
#     w1 = AcordesDCanciones(url)
#     # print(w1.chord_list)
#     print(w1.prog.analysis)
#     w1.prog.is_in_prog(["IIm", "V", "I"])
# elif "tabs.ultimate-guitar.com" in url:
#     w1 = UltimateGuitar(url)
#     # print(w1.chord_list)
#     print(w1.prog.analysis)
#     w1.prog.is_in_prog(["IV", "V", "I"])

# url = "https://acordes.lacuerda.net/abel_pintos/"
# test = Link(url)
# # print(test.soup)
# div_container = test.soup.find('div', {'class': 'tNav'})
# links = div_container.find_all("a")
# for link in links:
#     print(link.get('href'))
# links = [url + link.get('href') for link in links]
# print(links)

# for link in links:
#     all_tabs = Link(link)
#     best_tab = re.findall(r"\d+", str(all_tabs.soup.select('[id*="cal"]')[0]))[0]
#     best_tab = best_tab if int(best_tab) > 1 else ""
#     best_tab = LaCuerda(link + "-" + best_tab + ".shtml")
#     print(best_tab.url, best_tab.prog.scale)
