from tkinter import *
from tkinter.scrolledtext import ScrolledText
import difflib

global selected
selected = False

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
    i = 0
    programm = textInput.get("1.0", END).split('\n')
    programm = list(filter(None, programm))
    print(programm)
    if programm[i] != "Начало":
        err['text'] = "Программа должна начинаться со слова Начало"
        return
    i+=1
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
        return
    if ":=" not in programm[i]:
        err['text'] = "После определений должно идти окончание"
        return 1
    if ending(programm[i]):
        return
    i+=1
    if programm[i] != "Конец":
        err['text'] = "Программа должна оканчиваться словом Конец"
        return
    i+=1
    err['text'] = "Программа успешно скомпилированна"

def analys(definition):
    i = 0
    programm = definition.split(' ')
    programm = list(filter(None, programm))
    if programm[i] != "Анализ" and programm[i] != "Синтез":
        err['text'] = "Определение должно начинаться со слов Анализ или Синтез"
        return 1
    i+=1
    while '.' in programm[i]:
        i+=1
    if programm[i] != "Конец" or ("анализа" not in programm[i+1] and "синтеза" not in programm[i+1]):
        err['text'] = "Определение должно заканчиваться фразами Конец анализа или Конец синтеза"
        return 1
    if ";" not in programm[i+1]:
        err['text'] = "Определение должно отделться знаком ;"
        return 1
    return 0

def ending(definition):
    i = 0
    programm = definition.split(' ')
    programm = list(filter(None, programm))
    alph = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    if len(programm[i]) < 3 or programm[i][0] not in alph or programm[i][1] not in alph or difflib.SequenceMatcher(None, programm[i][2:], alph).get_matching_blocks()[0].size:
        err['text'] = "Ошибка в именовании переменной (стандарт именования переменной ББЧ..Ч )"
        return 1
    if ":=" not in programm:
        err['text'] = "После переменной должен стоять знак присваивания :="
        return 1
    blocks = plus(programm[2:])
    bricks = []
    for i in range(len(blocks)):
        for block in mult(blocks[i]):
            bricks.append(block)
    parts = []
    for i in range(len(bricks)):
        for brick in logic(bricks[i]):
            parts.append(brick)
    pieces = []
    for i in range(len(parts)):
        for part in rev(parts[i]):
            pieces.append(part)
    bites = []
    for i in range(len(pieces)):
        for piece in func(pieces[i]):
            bites.append(piece)
    print(bites)
    for bite in bites:
        bite = ''.join(bite)
        if not bite.isdigit() and (len(bite) < 3 or bite[0] not in alph or bite[1] not in alph or difflib.SequenceMatcher(None, bite[2:], alph).get_matching_blocks()[0].size):
            err['text'] = "В правой части можно использовать только целые числа или переменные"
            return 1
    return 0

def plus(programm):
    programm = list(filter(None, programm))
    blocks = []
    while "-" in programm or "+" in programm:
        indm = programm.index("-") if "-" in programm else len(programm)
        indp = programm.index("+") if "+" in programm else len(programm)
        if indm > indp:
            ind = programm.index("+")
            programm.pop(ind)
            blocks.append(programm[:ind])
            programm = programm[ind:]
        else:
            ind = programm.index("-")
            programm.pop(ind)
            blocks.append(programm[:ind])
            programm = programm[ind:]
    blocks.append(programm)
    return blocks

def mult(programm):
    programm = list(filter(None, programm))
    bricks = []
    while "*" in programm or "/" in programm:
        indm = programm.index("*") if "*" in programm else len(programm)
        indp = programm.index("/") if "/" in programm else len(programm)
        if indm > indp:
            ind = programm.index("/")
            programm.pop(ind)
            bricks.append(programm[:ind])
            programm = programm[ind:]
        else:
            ind = programm.index("*")
            programm.pop(ind)
            bricks.append(programm[:ind])
            programm = programm[ind:]
    bricks.append(programm)
    return bricks

def logic(programm):
    programm = list(filter(None, programm))
    blocks = []
    while "и" in programm or "или" in programm:
        indm = programm.index("и") if "и" in programm else len(programm)
        indp = programm.index("или") if "или" in programm else len(programm)
        if indm > indp:
            ind = programm.index("или")
            programm.pop(ind)
            blocks.append(programm[:ind])
            programm = programm[ind:]
        else:
            ind = programm.index("и")
            programm.pop(ind)
            blocks.append(programm[:ind])
            programm = programm[ind:]
    blocks.append(programm)
    return blocks

def rev(programm):
    programm = list(filter(None, programm))
    blocks = []
    while "не" in programm:
        ind = programm.index("не")
        programm.pop(ind)
        programm = programm[ind:]
    blocks.append(programm)
    return blocks

def func(programm):
    programm = list(filter(None, programm))
    blocks = []
    f = ["sin", "cos", "tg", "ctg"]
    if set(programm).intersection(f):
        programm.pop(0)
        programm = programm[0:]
    blocks.append(programm)
    return blocks

app = Tk()
app.title("Интерпритатор Begin")
app.geometry("700x625")
app.iconbitmap("C:/Users/Kirill/PycharmProjects/TextCodeDecode/data/icon.ico")
app.resizable(False, False)
app.bind('<Control-Key-c>', copy)
app.bind('<Control-Key-v>', paste)

textInput = ScrolledText(wrap="char", height=36, width=60)
textInput.place(x=10, y=15)
Button(text="Скомпилировать код", command=execute).place(x=534, y=30)
err = Label(wraplength=170)
err.place(x=517, y=60)

mainMenu = Menu()
app.config(menu=mainMenu)
fileMenu = Menu(mainMenu, tearoff=False)
fileMenu.add_command(label="Выход", command=lambda: app.destroy())
editMenu = Menu(mainMenu, tearoff=False)
mainMenu.add_cascade(label="Правка", menu=editMenu)
editMenu.add_command(label="Копировать", command=lambda: copy(False), accelerator="Clrl+C")
editMenu.add_command(label="Вставить", command=lambda: paste(False), accelerator="Clrl+V")

app.mainloop()

# 2 * 34 + не 45 + sin 4
# [[ 2 * 34 ] [ ne 45 ] [ sin 4 ]]
# [ [2] [34] [45] [4]]
