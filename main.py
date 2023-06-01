import PySimpleGUI as sg
import json
import random


def check_answer(key_answer, points):
    answers = ["a", "b", "c", "d"]
    if questions[i]["prawidłowa odpowiedź"] == key_answer:
        window['-CHECK-'].update("Brawo! To poprawna odpowiedź!")
        points += 1
        window['-POINTS-'].update(f"Liczba zdobytych punktów: {points}")
    else:
        window['-CHECK-'].update(f"Niestety, prawidłowa odpowiedź to: "
                                 f"{questions[i]['prawidłowa odpowiedź']}")
    answers.remove(questions[i]["prawidłowa odpowiedź"])
    for answer in answers:
        window[answer].update(visible=False)
    return points


def last_answer(key_answer, points):
    answers = ["a", "b", "c", "d"]
    if questions[i]["prawidłowa odpowiedź"] == key_answer:
        window['-CHECK-'].update("Brawo! To poprawna odpowiedź!")
        points += 1
        window['-POINTS-'].update(f"Liczba zdobytych punktów: {points}")
    else:
        window['-CHECK-'].update(f"Niestety, prawidłowa odpowiedź to: "
                                 f"{questions[i]['prawidłowa odpowiedź']}")
    window['-POINTS-'].update(f"Rozwiązałeś cały quiz. Łączna liczba zdobytych "
                              f"punktów: {points}.")
    answers.remove(questions[i]["prawidłowa odpowiedź"])
    for answer in answers:
        window[answer].update(visible=False)


def next_question(i):
    sg.theme('DarkBlue3')
    layout = [
        [sg.Text(f"{x}. {questions[i]['pytanie']}")],
        [sg.Radio(f"a) {questions[i]['a']}", group_id="question1",
                  enable_events=True, key="a")],
        [sg.Radio(f"b) {questions[i]['b']}", group_id="question1",
                  enable_events=True, key="b")],
        [sg.Radio(f"c) {questions[i]['c']}", group_id="question1",
                  enable_events=True, key="c")],
        [sg.Radio(f"d) {questions[i]['d']}", group_id="question1",
                  enable_events=True, key="d")],
        [sg.Text('', key="-CHECK-")],
        [sg.Text(f"Liczba zdobytych punktów: {points}", key="-POINTS-")],
        [sg.Button('Następne pytanie', key="-NEXT-"), sg.Button('Zakończ')],
        [sg.Text('Koło ratunkowe:', key='-HELP-'),
         sg.Button('50:50', tooltip="Usunięcie dwóch błędnych odpowiedzi. "
                                    "Można wykorzystać raz w ciągu gry.",
                   button_color="green", key="-50/50-")]
    ]
    return sg.Window('Quiz z wiedzy ogólnej', layout, size=(400,300))


def next_question_50_50(i):
    sg.theme('DarkBlue3')
    layout = [
        [sg.Text(f"{x}. {questions[i]['pytanie']}")],
        [sg.Radio(f"a) {questions[i]['a']}", group_id="question1",
                  enable_events=True, key="a")],
        [sg.Radio(f"b) {questions[i]['b']}", group_id="question1",
                  enable_events=True, key="b")],
        [sg.Radio(f"c) {questions[i]['c']}", group_id="question1",
                  enable_events=True, key="c")],
        [sg.Radio(f"d) {questions[i]['d']}", group_id="question1",
                  enable_events=True, key="d")],
        [sg.Text('', key="-CHECK-")],
        [sg.Text(f"Liczba zdobytych punktów: {points}", key="-POINTS-")],
        [sg.Button('Następne pytanie >>', key="-NEXT-"), sg.Button('Zakończ')],
        [sg.Text('Koło ratunkowe zostało wykorzystane', key='-HELP-'),
         sg.Button('50:50',
                   tooltip="Usunięcie dwóch błędnych odpowiedzi. Można "
                           "wykorzystać raz w ciągu gry.",
                   button_color="green", visible=False, key="-50/50-")]
    ]
    return sg.Window('Quiz z wiedzy ogólnej', layout, size=(400, 300))


with open("quiz.json", encoding="utf-8") as file:
    questions = json.load(file)

x = 1
points = 0
question_numbers = []
for i in range(len(questions)):
    question_numbers.append(i)

i = random.choice(question_numbers)
window = next_question(i)
question_numbers.remove(i)
help_50 = []

try:
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Zakończ'):
            break

        if event == "a":
            if x < 15:
                check_answer("a", points)
                points = check_answer("a", points)
            if x == 15:
                last_answer("a", points)

        if event == "b":
            if x < 15:
                check_answer("b", points)
                points = check_answer("b", points)
            if x == 15:
                last_answer("b", points)

        if event == "c":
            if x < 15:
                check_answer("b", points)
                points = check_answer("b", points)
            if x == 15:
                last_answer("b", points)

        if event == "d":
            if x < 15:
                check_answer("d", points)
                points = check_answer("d", points)
            if x == 15:
                last_answer("d", points)

        if event == "-NEXT-":
            window.close()
            if len(help_50) == 0:
                x += 1
                i = random.choice(question_numbers)
                question_numbers.remove(i)
                window = next_question(i)

            elif len(help_50) == 1:
                x += 1
                i = random.choice(question_numbers)
                question_numbers.remove(i)
                window = next_question_50_50(i)

        if event == "-50/50-":
            help_50.append(1)
            answers = ["a", "b", "c", "d"]
            answers.remove(questions[i]["prawidłowa odpowiedź"])
            answer_numbers = [0, 1, 2]
            answer_numbers_1 = random.choice(answer_numbers)
            answer_numbers.remove(answer_numbers_1)
            answer_numbers_2 = random.choice(answer_numbers)
            window[answers[answer_numbers_1]].update(visible=False)
            window[answers[answer_numbers_2]].update(visible=False)
            window["-50/50-"].update(visible=False)
            window["-HELP-"].update('Koło ratunkowe zostało wykorzystane')

except IndexError:
    window.close()