from scraper import UltimateGuitar

url = "https://es.ultimate-guitar.com/tab/amy-winehouse/back-to-black-chords-467281"
w1 = UltimateGuitar(url)
# print(w1.chord_list)
print(w1.prog.analysis)
print(w1.prog.scale)
w1.prog.is_in_prog(["IV"])
