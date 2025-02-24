from scraper import UltimateGuitar, LaCuerda, Link
import re

# url = "https://es.ultimate-guitar.com/tab/whitney-houston/i-have-nothing-chords-1760240"
# w1 = UltimateGuitar(url)
# # print(w1.chord_list)
# print(w1.prog.analysis)
# print(w1.prog.scale)
# w1.prog.is_in_prog(["IV"])

def get_popular_from_artist(artist):
    url = "https://acordes.lacuerda.net/" + artist.lower().replace(" ", "_") + "/"
    test = Link(url)
    div_container = test.soup.find('div', {'class': 'tNav'})
    links = div_container.find_all("a")
    links = [url + link.get('href') for link in links]

    tabs = []
    for link in links:
        all_tabs = Link(link)
        best_tab = re.findall(r"\d+", str(all_tabs.soup.select('[id*="cal"]')[0]))[0]
        best_tab = "-" + best_tab if int(best_tab) > 1 else ""
        best_tab = LaCuerda(link + best_tab + ".shtml")
        tabs.append(best_tab)
    
    return tabs

luis_miguel_pops = get_popular_from_artist("luis miguel")
for tab in luis_miguel_pops:
    print(tab.url, tab.prog.scale)