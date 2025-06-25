import tkinter as tk
from tkinter import ttk
import time as tm
import threading

# Initial variables
timelimit = 60
remainingTime = timelimit
elpasedtime = 0
totalwords = 0
wrongwords = 0
accuracy = 0
wpm = 0
key_labels = {}  # Store key label widgets

def start_timer():
    global elpasedtime
    entry.focus()
    entry.config(state='normal')
    btn_start.config(state='disabled')

    for time_counter in range(1, timelimit + 1):
        elpasedtime = time_counter
        lbl_elpasedTimer['text'] = elpasedtime

        updateremainingtime = remainingTime - elpasedtime
        lbl_remainingTimer['text'] = updateremainingtime

        tm.sleep(1)
        window.update()

    entry.config(state='disabled')
    btn_reset.config(state='normal')
    calculate_results()

def calculate_results():
    global wrongwords, totalwords, accuracy, wpm

    para_words = lbl_paragraph['text'].split()
    enteredparagraph = entry.get(1.0, 'end-1c').split()
    totalwords = len(enteredparagraph)
    wrongwords = sum(1 for i, word in enumerate(enteredparagraph) if i >= len(para_words) or word != para_words[i])

    elapsed_minutes = elpasedtime / 60 if elpasedtime != 0 else 1

    wpm = (totalwords - wrongwords) / elapsed_minutes
    gross_wpm = totalwords / elapsed_minutes
    accuracy = (wpm / gross_wpm) * 100 if gross_wpm != 0 else 0

    lbl_wpm['text'] = round(wpm)
    lbl_accuracy['text'] = round(accuracy, 2)
    lbl_tw['text'] = totalwords
    lbl_ww['text'] = wrongwords

def start():
    threading.Thread(target=start_timer).start()

def reset():
    global remainingTime, elpasedtime, totalwords, wrongwords, accuracy, wpm

    btn_reset.config(state='disabled')
    btn_start.config(state='normal')

    entry.config(state='normal')
    entry.delete(1.0, tk.END)
    entry.config(state='disabled')

    remainingTime = timelimit
    elpasedtime = 0
    totalwords = 0
    wrongwords = 0
    accuracy = 0
    wpm = 0

    lbl_elpasedTimer['text'] = 0
    lbl_remainingTimer['text'] = 60
    lbl_wpm['text'] = 0
    lbl_accuracy['text'] = 0
    lbl_tw['text'] = 0
    lbl_ww['text'] = 0

def highlight_key(event):
    char = event.char.upper()
    if char in key_labels:
        lbl = key_labels[char]
        lbl.config(bg='blue')
        window.after(150, lambda: lbl.config(bg='black'))
    elif event.keysym == 'space':
        lbl_space.config(bg='blue')
        window.after(150, lambda: lbl_space.config(bg='black'))

window = tk.Tk()
window.title("Typing Speed Tester")
window.geometry('1140x850')
window.resizable(False, False)

# Main Frame
main_frame = tk.Frame(window, bg='white')
main_frame.pack(expand=True, fill='both')

# Title
lbl_title = tk.Label(main_frame, text='Typing Speed Tester', font='arial 30 bold', bg='white')
lbl_title.pack(pady=10)

# Paragraph
selected_paragraph = ('Cricket is a bat-and-ball game played between two teams of eleven players on a field with a rectangular 22-yard pitch at the center. '
                      'The objective is for one team to score runs by hitting a ball delivered by the opposing team and running between the wickets (a set of three sticks) '
                      'at each end of the pitch, while the other team tries to dismiss the batsmen and restrict their scoring.')
lbl_paragraph = tk.Label(main_frame, text=selected_paragraph, wraplength=1050, justify='left', bg='white', font=('Arial', 14))
lbl_paragraph.pack(pady=10)

# Entry Box
entry = tk.Text(main_frame, height=8, width=120, state='disabled', wrap='word')
entry.pack(pady=10)

# Metrics Frame
metrics_frame = tk.Frame(main_frame, bg='white')
metrics_frame.pack()

lbl_elpasedTimer = tk.Label(metrics_frame, text='0', font='Tahoma 10 bold', fg='black', bg='white')
lbl_remainingTimer = tk.Label(metrics_frame, text='60', font='Tahoma 10 bold', fg='black', bg='white')
lbl_wpm = tk.Label(metrics_frame, text='0', font='Tahoma 10 bold', fg='black', bg='white')
lbl_accuracy = tk.Label(metrics_frame, text='0', font='Tahoma 10 bold', fg='black', bg='white')
lbl_tw = tk.Label(metrics_frame, text='0', font='Tahoma 10 bold', fg='black', bg='white')
lbl_ww = tk.Label(metrics_frame, text='0', font='Tahoma 10 bold', fg='black', bg='white')

# Metrics Labels
for i, (label_text, lbl_widget) in enumerate([
    ('Elapsed Time', lbl_elpasedTimer),
    ('Remaining Time', lbl_remainingTimer),
    ('WPM', lbl_wpm),
    ('Accuracy', lbl_accuracy),
    ('Total Words', lbl_tw),
    ('Wrong Words', lbl_ww),
]):
    tk.Label(metrics_frame, text=label_text, font='Tahoma 10 bold', fg='red', bg='white').grid(row=0, column=i * 2, padx=5)
    lbl_widget.grid(row=0, column=i * 2 + 1, padx=5)

# Control Buttons
controls_frame = tk.Frame(main_frame, bg='white')
controls_frame.pack(pady=10)

btn_start = ttk.Button(controls_frame, text='Start', command=start)
btn_start.grid(row=0, column=0, padx=10)

btn_reset = ttk.Button(controls_frame, text='Reset', command=reset, state='disabled')
btn_reset.grid(row=0, column=1, padx=10)

# Keyboard Frame
keyboard_frame = tk.Frame(main_frame, bg='white')
keyboard_frame.pack(pady=15)

keys = [
    ['1','2','3','4','5','6','7','8','9','0'],
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L'],
    ['Z','X','C','V','B','N','M'],
]

for row_keys in keys:
    row = tk.Frame(keyboard_frame, bg='white')
    for key in row_keys:
        lbl = tk.Label(row, text=key, bg='black', fg='white', width=4, height=2, relief='sunken', bd=4, font=('Arial', 11, 'bold'))
        lbl.pack(side='left', padx=8, pady=8)  # Increased padx from 4 to 8
        key_labels[key] = lbl
    row.pack()

# Space bar
space_frame = tk.Frame(keyboard_frame, bg='white')
lbl_space = tk.Label(space_frame, bg='black', fg='white', width=40, height=2, relief='sunken', bd=4)
lbl_space.pack(pady=4)
space_frame.pack()

# Key bindings for highlight
for char in '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
    window.bind(char, highlight_key)
window.bind('<space>', highlight_key)

window.mainloop()
