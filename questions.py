from scraper import UltimateGuitar

url = "https://tabs.ultimate-guitar.com/tab/bruno-mars/when-i-was-your-man-chords-1198871"
w1 = UltimateGuitar(url)
# print(w1.chord_list)
print(w1.prog.analysis)
print(w1.prog.scale)
w1.prog.is_in_prog(["IV", "V", "I"])

