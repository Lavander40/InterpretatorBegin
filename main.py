from tkinter import *
from tkinter.scrolledtext import ScrolledText
import difflib
import re
import math
import numexpr

global selected
selected = False
global ansv
ansv = ''
global lines
global pointer
global l_point
def copy(keyboardInput):
    global selected
    if keyboardInput:
        selected = app.clipboard_get()
    if textInput.selection_get():
        selected = textInput.selection_get()
        app.clipboard_clear()
        app.clipboard_append(selected)

def paste(keyboardInput):
    global selected
    selected = app.clipboard_get()
    if not keyboardInput:
        pos = textInput.index(INSERT)
        textInput.insert(pos, selected)

def execute():
    global lines, l_point, ansv
    global pointer
    pointer = 0
    l_point = 0
    i = 0
    err['text'] = ''
    textInput.tag_remove("red", "1.0", "end-1c")
    textInput.tag_config('red', background='#FF6767')
    programm = textInput.get("1.0", END).split('\n')
    programm = list(filter(None, programm))
    programm.append('')
    lines = programm
    if not programm:
        return
    if programm[i].strip() != "Начало":
        err['text'] = "Программа должна начинаться со слова Начало"
        color()
        return
    i+=1
    pointer = 0
    l_point += 1
    if "Анализ" in programm[i] or "Синтез" in programm[i]:
        if analys(programm[i]):
            return
        i += 1
        while "Анализ" in programm[i] or "Синтез" in programm[i]:
            if analys(programm[i]):
                return
            i+=1
    else:
        err['text'] = "В программе должно быть минимум одно определение"
        color()
        return
    if ":=" not in programm[i]:
        err['text'] = "После определений должно идти окончание"
        color()
        return
    if ending(programm[i]):
        return
    i+=1
    l_point += 1
    pointer = 0
    if programm[i].strip() != "Конец":
        err['text'] = "Программа должна оканчиваться словом Конец"
        color()
        return
    i+=1
    pointer += 1
    err['text'] = f"Программа успешно скомпилированна\nОтвет: {eval(ansv)}"

def analys(definition):
    global pointer, l_point
    pointer = 0
    i = 0
    programm = definition.split(' ')
    programm = list(filter(None, programm))
    if programm[i] != "Анализ" and programm[i] != "Синтез":
        err['text'] = "Определение должно начинаться со слов Анализ или Синтез"
        color()
        return 1
    i+=1
    pointer += 1
    while '.' in programm[i]:
        # число . число ; число . число
        # \d+\.\d+;\d+\.\d+
        if not re.fullmatch(r"\d+\.\d+;\d+\.\d+", programm[i]):
            err['text'] = "Ошибка, встречено не комплексное в анализе"
            color()
            return 1
        i += 1
        pointer += 1
    if programm[i] != "Конец" or ("анализа" not in programm[i+1] and "синтеза" not in programm[i+1]):
        err['text'] = "Определение должно заканчиваться фразами Конец анализа или Конец синтеза"
        color()
        return 1
    if ";" not in programm[i+1]:
        err['text'] = "Определение должно отделться знаком ;"
        color()
        return 1
    pointer += 2
    l_point += 1
    return 0

def ending(definition):
    global pointer
    pointer = 0
    i = 0
    global ansv
    ansv = ''
    programm = definition
    programm = programm.replace(":=", " := ")
    programm = programm.replace("-", " - ")
    programm = programm.replace("+", " + ")
    programm = programm.replace("/", " / ")
    programm = programm.replace("*", " * ")
    programm = programm.replace("&", " & ")
    programm = programm.replace("|", " | ")
    programm = programm.replace("!", " ! ")
    programm = programm.replace("sin", " sin ")
    programm = programm.replace("cos", " cos ")
    programm = programm.replace("tg", " tg ")
    programm = programm.replace("ctg", " ctg ")
    programm = programm.split(' ')
    programm = list(filter(None, programm))
    alph = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    if len(programm[i]) < 3 or programm[i][0] not in alph or programm[i][1] not in alph or difflib.SequenceMatcher(None, programm[i][2:], alph).get_matching_blocks()[0].size:
        err['text'] = "Ошибка в именовании переменной (стандарт именования переменной ББЧ..Ч )"
        color()
        return 1
    pointer += 1
    if ":=" not in programm:
        err['text'] = "После переменной должен стоять знак присваивания :="
        color()
        return 1
    pointer += 1
    ansv = programm[2:]
    for i in range(len(ansv)):
        if ansv[i] not in "+-*/&|!sincosctg":
            ansv[i] = f"({ansv[i]})"
    ansv = ''.join(ansv)

    if "sinsin" in ansv:
        sinner = ansv.find("sinsin") #sinsin(4) = sin + ( + sin(4) + )
        ansv = f'{ansv[:sinner+3]}({ansv[sinner+6:]})'

    if "sincos" in ansv:
        sinner = ansv.find("sincos") #sinsin(4) = sin + ( + sin(4) + )
        ansv = f'{ansv[:sinner+3]}({ansv[sinner+6:]})'

    if "cossin" in ansv:
        sinner = ansv.find("cossin") #sinsin(4) = sin + ( + sin(4) + )
        ansv = f'{ansv[:sinner+3]}({ansv[sinner+6:]})'

    if "coscos" in ansv:
        sinner = ansv.find("coscos") #sinsin(4) = sin + ( + sin(4) + )
        ansv = f'{ansv[:sinner+3]}({ansv[sinner+6:]})'

    ansv = ansv.replace("sin", "math.sin")
    ansv = ansv.replace("cos", "math.cos")
    ansv = ansv.replace("!", "~")
    if comp(programm[2:]):
        return 1
    # parts = oper(programm[2:])
    # blocks = plus(programm[2:])
    # if blocks == -1:
    #     return 1
    # bricks = []
    # for i in range(len(blocks)):
    #     for block in mult(blocks[i]):
    #         if block == -1:
    #             return 1
    #         bricks.append(block)
    # parts = []
    # for i in range(len(bricks)):
    #     for brick in logic(bricks[i]):
    #         parts.append(brick)
    # pieces = []
    # for i in range(len(parts)):
    #     for part in rev(parts[i]):
    #         pieces.append(part)
    # bites = []
    # for i in range(len(pieces)):
    #     for piece in func(pieces[i]):
    #         bites.append(piece)
    # for bite in bites:
    #     bite = ''.join(bite)
    #     if not bite.isdigit() and (len(bite) < 3 or bite[0] not in alph or bite[1] not in alph or difflib.SequenceMatcher(None, bite[2:], alph).get_matching_blocks()[0].size):
    #         err['text'] = "В правой части можно использовать только целые числа или переменные"
    #         color()
    #         return 1
    return 0
def comp(definition):
    global pointer

    for i in range(len(definition)-1):
        # numbers
        if definition[i].isdigit():
            if not definition[i+1] in "+-*/&|":
                err['text'] = "Ошибка, отсутствует знака операции"
                pointer += 1
                color()
                return 1
            pointer += 1
        # functions
        elif definition[i] in ["sin", "cos", "tg", "ctg"]:
            if definition[i + 1] in "+-*/&|":
                err['text'] = "Ошибка, использование знака операции в функции"
                pointer += 1
                color()
                return 1
            pointer += 1
        # operators
        elif definition[i] in "-+/*!|&":
            if definition[i + 1] in "+-*/&|":
                err['text'] = "Ошибка, дублирование знака операции"
                pointer += 1
                color()
                return 1
            pointer += 1
        else:
            err['text'] = "В правой части можно использовать только целые числа или переменные"
            color()
    if not definition[len(definition)-1].isdigit():
        err['text'] = "Знак операции не закрыт"
        color()
# def oper(programm):
#     global pointer
#     programm = list(filter(None, programm))
#     blocks = []
#     if programm[0] in "-+":
#         programm.pop(0)
#     while "-" in programm or "+" in programm or "*" in programm or "/" in programm or "|" in programm or "&" in programm:
#         if programm[0] in "-+/*&|":
#             err['text'] = "Ошибка, дублирование знака операции"
#             color()
#             return -1
#         inda = programm.index("-") if "-" in programm else len(programm)
#         indb = programm.index("+") if "+" in programm else len(programm)
#         indc = programm.index("*") if "*" in programm else len(programm)
#         indd = programm.index("/") if "/" in programm else len(programm)
#         inde = programm.index("&") if "&" in programm else len(programm)
#         indf = programm.index("|") if "|" in programm else len(programm)
#         s = [inda, indb, indc, indd, inde, indf]
#         if inda == min(s):
#             ind = programm.index("-")
#             programm.pop(ind)
#             blocks.append(programm[:ind])
#             programm = programm[ind:]
#         elif indb == min(s):
#             ind = programm.index("+")
#             programm.pop(ind)
#             blocks.append(programm[:ind])
#             programm = programm[ind:]
#         elif indc == min(s):
#             ind = programm.index("*")
#             programm.pop(ind)
#             blocks.append(programm[:ind])
#             programm = programm[ind:]
#         elif indd == min(s):
#             ind = programm.index("/")
#             programm.pop(ind)
#             blocks.append(programm[:ind])
#             programm = programm[ind:]
#         elif inde == min(s):
#             ind = programm.index("&")
#             programm.pop(ind)
#             blocks.append(programm[:ind])
#             programm = programm[ind:]
#         else:
#             ind = programm.index("|")
#             programm.pop(ind)
#             blocks.append(programm[:ind])
#             programm = programm[ind:]
#     blocks.append(programm)
#     pointer += 2
#     return blocks

# def plus(programm):
#     programm = list(filter(None, programm))
#     blocks = []
#     if programm[0] in "-+":
#         programm.pop(0)
#     while "-" in programm or "+" in programm:
#         if programm[0] in "-+/*|&":
#             err['text'] = "Ошибка, дублирование знака операции"
#             color()
#             return -1
#         indm = programm.index("-") if "-" in programm else len(programm)
#         indp = programm.index("+") if "+" in programm else len(programm)
#         if indm > indp:
#             ind = programm.index("+")
#             programm.pop(ind)
#             blocks.append(programm[:ind])
#             programm = programm[ind:]
#         else:
#             ind = programm.index("-")
#             programm.pop(ind)
#             blocks.append(programm[:ind])
#             programm = programm[ind:]
#     blocks.append(programm)
#     return blocks
#
# def mult(programm):
#     programm = list(filter(None, programm))
#     bricks = []
#     while "*" in programm or "/" in programm:
#         if programm[0] in "-+/*&|":
#             err['text'] = "Ошибка, дублирование знака операции"
#             color()
#             return -1
#         indm = programm.index("*") if "*" in programm else len(programm)
#         indp = programm.index("/") if "/" in programm else len(programm)
#         if indm > indp:
#             ind = programm.index("/")
#             programm.pop(ind)
#             bricks.append(programm[:ind])
#             programm = programm[ind:]
#         else:
#             ind = programm.index("*")
#             programm.pop(ind)
#             bricks.append(programm[:ind])
#             programm = programm[ind:]
#     bricks.append(programm)
#     return bricks
#
# def logic(programm):
#     programm = list(filter(None, programm))
#     blocks = []
#     while "и" in programm or "или" in programm:
#         if programm[0] in "-+/*&|":
#             err['text'] = "Ошибка, дублирование знака операции"
#             color()
#             return -1
#         indm = programm.index("и") if "и" in programm else len(programm)
#         indp = programm.index("или") if "или" in programm else len(programm)
#         if indm > indp:
#             ind = programm.index("или")
#             programm.pop(ind)
#             blocks.append(programm[:ind])
#             programm = programm[ind:]
#         else:
#             ind = programm.index("и")
#             programm.pop(ind)
#             blocks.append(programm[:ind])
#             programm = programm[ind:]
#     blocks.append(programm)
#     return blocks

# def rev(programm):
#     global pointer
#     programm = list(filter(None, programm))
#     blocks = []
#     while "!" in programm:
#         if programm[0] in "-+/*&|":
#             err['text'] = "Ошибка, дублирование знака операции"
#             color()
#             return -1
#         ind = programm.index("!")
#         programm.pop(ind)
#         programm = programm[ind:]
#     blocks.append(programm)
#     pointer += 2
#     return blocks
#
# def func(programm):
#     global pointer
#     programm = list(filter(None, programm))
#     blocks = []
#     f = ["sin", "cos", "tg", "ctg"]
#     while set(programm).intersection(f):
#         programm.pop(0)
#         programm = programm[0:]
#     blocks.append(programm)
#     pointer += 2
#     return blocks

def color():
    start_p = 0
    print(lines, l_point, pointer)
    lines[l_point] = lines[l_point].split(' ')
    for i in range(0, pointer):
        start_p += len(lines[l_point][i]) + 1
    end_p = start_p + len(lines[l_point][pointer])
    print(start_p, end_p, l_point)
    textInput.tag_add('red', f"{l_point+1}.{start_p}", f"{l_point+1}.{end_p}")

app = Tk()
app.title("Интерпритатор Begin")
app.geometry("820x700")
#app.iconbitmap("C:/Users/Kirill/PycharmProjects/TextCodeDecode/data/icon.ico")
app.resizable(False, False)
app.bind('<Control-Key-c>', copy)
app.bind('<Control-Key-v>', paste)

textInput = ScrolledText(wrap="char", height=36, width=60)
textInput.place(x=10, y=15)
Button(text="Скомпилировать код", command=execute).place(x=534, y=30)
err = Label(wraplength=170)
err.place(x=517, y=60)
Label(text='Язык = "Начало" Опр";"...Опр Оконч "Конец"\nОпр = ["Анализ" ! "Синтез"] Компл...Компл ["Конец анализа" ! "Конец синтеза"]\nОконч = Перем ":=" ПрЧасть\nПерем = БукБукЦиф...Циф\nПрЧасть = </"-"/>Блок["-"!"+"]...Блок\nБлок = Часть["*"!"/"]...Часть\nЧасть = Доля["и"!"или"]...Доля\nДоля = </"не"/>Кусок\nКусок = </Функ...Функ/>Кусочек\nФунк = "sin" ! "cos"\nКусочек = Перем ! Цел\nКомпл = Цел "." Цел ";" Цел "." Цел\nЦел = Циф...Циф\nЦиф = "0"!"1"!...!"9"\nБук = "а"!"б"!...!"я"', wraplength=300).place(x=517, y=150)

mainMenu = Menu()
app.config(menu=mainMenu)
fileMenu = Menu(mainMenu, tearoff=False)
fileMenu.add_command(label="Выход", command=lambda: app.destroy())
editMenu = Menu(mainMenu, tearoff=False)
mainMenu.add_cascade(label="Правка", menu=editMenu)
editMenu.add_command(label="Копировать", command=lambda: copy(False), accelerator="Clrl+C")
editMenu.add_command(label="Вставить", command=lambda: paste(False), accelerator="Clrl+V")

app.mainloop()
