import re
import itertools
import more_itertools
import collections

## !!!!
## Funca como prototipo, tengo que testear con muchas progresiones, comunes y raras
## No implementé lo de las enarmonías, si lo uso en LaCuerda o similares lo voy a necesitar
## El programa no sabe procesar inversiones
## Solo puede leer cifrado americano

class Note:
    notes = {
        "#": ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"),
        "b": ("C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"),
        "x": ("B#", "Bx", "Cx", "D#", "Dx", "E#", "Ex", "Fx", "G#", "Gx", "A#", "Ax"),
        "bb": ("Dbb", "Db", "Ebb", "Fbb", "Fb", "Gbb", "Gb", "Abb", "Ab", "Bbb", "Cbb", "Cb")
        }

    names = ("C", "D", "E", "F", "G", "A", "B")
    names_latin = ("DO", "RE", "MI", "FA", "SO", "LA", "SI")

    l_to_a = {"DO": "C", "RE": "D", "MI": "E", "FA": "F", "SO": "G", "LA": "A", "SI": "B"}

    ## ??? Podría generarlo con un iterador, tal vez, pero por ahora sirve
    circle_of_fifths = ("Fbb", "Cbb", "Gbb", "Dbb", "Abb", "Ebb", "Bbb", "Fb", "Cb", "Gb", 
                        "Db", "Ab", "Eb", "Bb", "F", "C", "G", "D", "A", "E", "B", "F#", "C#",
                        "G#", "D#", "A#", "E#", "B#", "Fx", "Cx", "Gx", "Dx", "Ax", "Ex", "Bx")


    def __init__(self, note):
        if self.is_valid_note(note):
            self.note = self.to_american(note)
            self.name = self.note[0]
            self.alt = self.note.split(self.name)[1]
            self._notes_list = [lst for lst in Note.notes.values() if self.note in lst][0]
            self._index = self._notes_list.index(self.note)
            self._name_idx = Note.names.index(self.name)
        else:
            raise Exception("Invalid note")

    def is_valid_note(self, note):
        return note[0] in Note.names or note[0:2] in Note.names_latin
    
    def to_american(self, note):
        if note[0:2] in Note.names_latin:
            return self.l_to_a[note[0:2]] + note[2:]
        else:
            return note

    def get_enharmonics(self):
        idx = self._index
        ans = []
        for lst in list(Note.notes.values()):
            if lst[idx] not in ans:
                ans.append(lst[idx])
        return ans

    def get_interval(self, note):
        cf = Note.circle_of_fifths
        x = self._name_idx
        for y in itertools.count(x):
            if Note.names[y%7] == note.name:
                break
        interval = str(y - x + 1)

        cf_idx = cf.index(self.note)
        quality = False
        for i in range(0, len(cf)):
            if cf[i] == note.note:
                quality = i - cf_idx
                break

        if quality in range(-16, -5):
            interval += "dim"
        elif quality in range(-5, -1):
            interval += "m"
        elif quality in range(-1, 2):
            interval += "P"
        elif quality in range(2, 6):
            interval += "M"
        elif quality in range(6, 16):
            interval += "Aug"
        else:
            raise Exception("Interval not defined")

        return interval


class Scale(Note):
    scales = {
        "Major": (0, 2, 4, 5, 7, 9, 11),
        "Minor": (0, 2, 3, 5, 7, 8, 10),
        "Dorian": (0, 2, 3, 5, 7, 9, 10),
        "Lydian b7": (0, 2, 4, 6, 7, 9, 10)
        ## !!! Seguir completando escalas
        }

    degrees = {
        0: "I",
        1: "II",
        2: "III",
        3: "IV",
        4: "V",
        5: "VI",
        6: "VII"
        }

    def __init__(self, note, type):
        super().__init__(note)
        self.scale_type = type
        self.scale = self.make_scale(type=type)
        self.scale_name = self.scale[0] + " " + self.scale_type

    def make_scale(self, type):
        note = self.note
        scales = Scale.scales
        names = Note.names

        collection = self._notes_list
        idx = collection.index(note)
        intervals = [(x + idx) for x in scales[type]]

        i = names.index(note[0])
        new_scale = []
        for n in intervals:
            new_note = collection[n % 12]
            name = new_note[0]
            if name != names[i%7]:
                new_note = [n for n in Note(new_note).get_enharmonics() if n[0] == names[i%7]][0]
            i += 1    
            new_scale.append(new_note)

        return new_scale

    def analyze_chord(self, chord, next_chord=False):
        try:
            if next_chord:
                ## !!! Tengo que mejorar la implementación de chord_type (Dominant, Tonic, etc)
                if chord.get_interval(next_chord) == "4P" and chord.chord_type in ("", "7", "9", "13"):
                    next = self.analyze_chord(Chord(next_chord.note))
                    if next == "I":
                        degree = "V" + chord.chord_type
                    elif next == "IV" and chord.chord_type == "":
                        degree = "I" + chord.chord_type
                    elif self.analyze_chord(next_chord)[0] in ("#", "b"):
                        degree = self.analyze_chord(chord)
                    else:
                        degree = "V" + chord.chord_type + "/" + next
                    return degree
                elif chord.get_interval(next_chord) == "7M" and chord.chord_type in ("7", "9", "13"):
                    next = self.analyze_chord(next_chord)
                    if next[0] in ("#", "b") or "VII" in next:
                        degree = self.analyze_chord(chord)
                    else:
                        degree = "subV" + chord.chord_type + "/" + self.analyze_chord(Chord(next_chord.note))
                    return degree
        except Exception:
            self.analyze_chord(chord)
        if chord.note in self.scale:
            degree = Scale.degrees[self.scale.index(chord.note)]
            degree += chord.chord_type
            interval = self.get_interval(chord)
            if "m" in interval:
                degree = "b" + degree
        else:
            if "Aug" in self.get_interval(chord):
                if "°" in chord.chord_type: ## Chequear, solo lo probé con un tema
                    scale_names = [n[0] for n in self.scale]
                    degree = "#" + Scale.degrees[scale_names.index(chord.name)]
                    degree += chord.chord_type
                else:
                    degree = " "
            else: 
                scale_names = [n[0] for n in self.scale]
                degree = "b" + Scale.degrees[scale_names.index(chord.name)]
                degree += chord.chord_type
        return degree

    def analyze_progression(self, prog, loop=False):
        if loop:
            next_chord = Chord(prog[-1])
        else:
            next_chord = False
        ans = []
        for c in prog:
            c = c.split("/")[0] ## !!! Temporal, no están implementadas las inversiones
            c = Chord(c)
            current = self.analyze_chord(c, next_chord)
            next_chord = c
            ans.append(current)
        ans.reverse()
        return ans

    def print_scale(self):
        ans = self.note + " " + self.scale_type + ":"
        for note in self.scale:
            ans += " " + note
        print(ans)


class Chord(Scale):
    def __init__(self, chord):
        self.chord = chord  
        Note.__init__(self, self.get_note())
        self.chord_type = self.get_chord_type()

    def get_note(self):
        ans = re.search("([DRMFSL][AEIO]|[A-G])(b{2}|[b#x])?", self.chord)
        if ans:
            return ans.group()
        else:
            raise Exception("Invalid chord")   

    def get_chord_type(self):
        return re.split("([DRMFSL][AEIO][L]?|[A-G])(b{2}|[b#x])?", self.chord)[-1] ## Así o lo hago más específico?

    def is_diatonic(self, scale):
        return self.note in scale.scale ## !!! Incompleto, solo mira el nombre y no el tipo
    
class Progression(Scale):

    degrees_major = (
        ("I", "I6", "IMaj7", "IMaj9", "IMaj13"),
        ("IIm", "IIm7", "IIm9", "IIm11", "IIm13"),
        ("IIIm", "IIIm7", "IIIm9"),
        ("IV", "IVMaj7", "IVMaj9", "IVMaj13", "IVMaj7(#11)", "IVMaj9(#11)", "IVMaj13(#11)"),
        ("V", "V7", "V9", "V7(b9)", "V7(b13)"), ## Hay más, el quinto es un bardo
        ("VIm", "VIm7", "VIm9", "VIm11"),
        ("VIIm7b5")
    )
    
    ## !!! Chequear tensiones disponibles para menores, apuntes de Armo
    degrees_minor = (
        ("Im", "Im7", "Im9", "Im11"),
        ("IIm7b5", "IIm11b5"),
        ("bIII", "bIIIMaj7", "bIIIMaj9", "bIIIMaj13"),
        ("IVm", "IVm7", "IVm6", "IVm9", "IV", "IV7"),
        ("Vm", "Vm7", "Vm9"), ## Hay más, el quinto es un bardo
        ("bVI", "bVIMaj7", "bVIMaj9", "bVIMaj11"),
        ("bVII", "bVII7", "bVII9")
    )

    def __init__(self, prog, loop=False):
        if isinstance(prog, str):
            self.prog = prog.split()
        elif isinstance(prog, list):
            self.prog = prog
        self.loop = loop
        self.scale = None
        self.analysis = self.analyze()

    def set_scale(self, scale):
        self.scale = scale

    def analyze(self, scale=False):
        prog = self.prog[:]
        prog.reverse()
        if scale:
            ans = scale.analyze_progression(prog, loop=self.loop)
            return ans
        else:
            ans = []
            scales = []
            for c in prog:
                new_scale = Scale(Chord(c).note, "Major")
                ans.append(new_scale.analyze_progression(prog, loop=self.loop))
                scales.append(new_scale.scale_name)
        points_major = [self.evaluate_major(x) for x in ans]
        winner_idx = points_major.index(max(points_major))
        self.set_scale(scales[winner_idx])
        return ans[winner_idx]
    
    ## Tiene mérito, pero tengo que incorporar algo para chequear las séptimas apropiadas
    # points = {
    #     ("I"): 10, 
    #     ("IIm"): 6,
    #     ("IIIm"): 5,
    #     ("IV"): 8,
    #     ("V"): 9,
    #     ("VIm"): 7,
    #     ("VIImb5"): 2,
    #     ("V", "I"): 5,
    #     ("IV", "I"): 4,
    #     ("IVm", "I"): 4,
    #     ("bVII", "I"): 2,
    #     ("IIm", "V"): 5,
    #     ("IV", "V"): 5,
    #     ("bVI", "bVII"): 2
    # }

    # def new_evaluate(self, ans):
    #     test_ans = ans[:]
    #     points = 0
    #     if self.loop:
    #         test_ans.append(ans[0])
        
    #     for prog, p in zip(Progression.points.keys(), Progression.points.values()):
    #         if isinstance(prog, str):
    #             prog = [prog]
    #         if self.is_in_prog(prog, test_ans):
    #             points += p

    #     return points

    def evaluate_major(self, ans):
        ## La diva, chequea por grados diatónicos y por algunas cadencias
        points = 0
        last = ""
        for c in ans:
            if c in Progression.degrees_major[0]:
                points += 10
                if last in Progression.degrees_major[4]:
                    ## V I
                    points += 5
                elif last in Progression.degrees_major[3] or last in Progression.degrees_minor[3]:
                    ## IV I o IVm I
                    points += 4
                elif last in Progression.degrees_minor[6]:
                    ## bVII I
                    points += 2
            elif c in Progression.degrees_major[1]:
                points += 6
            elif c in Progression.degrees_major[2]:
                points += 5
            elif c in Progression.degrees_major[3]:
                points += 8
            elif c in Progression.degrees_major[4]:
                points += 9
                if last in Progression.degrees_major[1] or last in Progression.degrees_major[3]:
                    ## IIm V o IV V
                    points += 5
            elif c in Progression.degrees_major[5]:
                points += 7
            elif c in Progression.degrees_major[6]:
                points += 2
            elif c in Progression.degrees_minor[6] and last in Progression.degrees_minor[5]:
                ## bVI bVII
                points += 2
            last = c
        if self.loop:
            if c[0] in Progression.degrees_major[0]:
                if last in Progression.degrees_major[4]:
                    ## V I
                    points += 5
                elif last in Progression.degrees_major[3] or last in Progression.degrees_minor[3]:
                    ## IV I o IVm I
                    points += 4
                elif last in Progression.degrees_minor[6]:
                    ## bVII I
                    points += 2
        return points
    
    def is_in_prog(self, test_prog, ans=False):
        if not ans:
            ans = self.analysis

        size = len(test_prog)
        windows = more_itertools.windowed(ans, size)
        progs = []
        for w in windows:
            prog = list(w)
            prog = [re.sub("[0-9Maj]", "", x) for x in prog] ## Chequear mb5
            progs.append(prog)
        if test_prog in progs:
            print(test_prog, "appears in this progression")
            return True
        else:
            return False

## !!! Puedo hacer una lista de los tipos de acordes diatónicos usando regex

### Progression Tests
# p1 = Progression(["A7", "Dm", "G", "C"])
# print(p1.prog, p1.scale, p1.analysis)

# p2 = Progression("C G Am F")
# print(p2.prog, p2.scale, p2.analysis)

# p3 = Progression("C#Maj7 A#7 D#7 G#7", loop=True)
# print(p3.prog, p3.scale, p3.analysis)

# p4 = Progression("Bb C7 Am Dm Gm7 C7 F")
# print(p4.prog, p4.scale, p4.analysis)

# p5 = Progression("G B7 C Cm", loop=True)
# print(p5.prog, p5.scale, p5.analysis)

# p6 = Progression("C D F C")
# print(p6.prog, p6.scale, p6.analysis)

# p7 = Progression("Ab Bb C")
# print(p7.prog, p7.scale, p7.analysis)

# p8 = Progression("EbMaj7 Bbm7 Eb7 AbMaj7 Abm7 Db7 EbMaj7 Cm7 Fm7 Bb7 Eb6")
# print(p8.prog, p8.scale, p8.analysis)