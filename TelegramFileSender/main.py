import customtkinter
from tkinter import filedialog
from tkinter.messagebox import showwarning, showinfo
import requests
import json

with open("config.json", "r") as configuration:
    config = json.load(configuration)

VERSION = '1.0'

app = customtkinter.CTk()
app.title(f"Telegram Sender v. {VERSION}")
app.geometry("400x400")
app.minsize(400, 400)

def combobox_callback(choice):
    if choice == "en":
        button_select.configure(text="Select files")
        button_send.configure(text="Send")
        button_clear.configure(text="Clear")
    elif choice == "ru":
        button_select.configure(text="Выбрать файлы")
        button_send.configure(text="Отправить")
        button_clear.configure(text="Очистить")

combobox = customtkinter.CTkComboBox(app, values=["ru", "en"],
                                     command=combobox_callback)
combobox.set("ru")
combobox.grid(row=0)

name_programm = customtkinter.CTkLabel(app, text=f"Telegram Sender v. {VERSION}", fg_color="transparent", font=('Calibri', 20))
name_programm.grid(row=1, column=0, pady=10, columnspan=2)

textbox = customtkinter.CTkTextbox(app, wrap="word", font=('Calibri', 14), height=150)
textbox.grid(row=3, column=0, pady=5, sticky="ew", columnspan=2)

files = []

def select_files():
    global files
    files = list(filedialog.askopenfilenames())
    textbox.delete("1.0", "end")
    if not files and combobox.get() == "ru":
        showwarning(title="Предупреждение!", message="Вы ничего не выбрали.")
    elif not files and combobox.get() == "en":
        showwarning(title="Warning!", message="You chose nothing.")
    else:
        for i in files:
            textbox.insert("insert", i + "\n")
    
def send_file():
    print(files)
    for file in files:
        file = {'document': open(file, 'rb')}
        req = requests.post(f'https://api.telegram.org/bot{config["TOKEN"]}/sendDocument?chat_id={config["chat_id"]}', files=file)
        if req.status_code == 200 and combobox.get() == "ru":
            showinfo(title="Успех!", message="Успешно отправлено.")
        elif req.status_code == 200 and combobox.get() == "en":
            showinfo(title="Success!", message="Successfully sent.")
        else:
            if combobox.get() == "ru":
                showwarning(title="Ошибка!", message=f"Ваши файлы не были отправлены. {req.text}")
            else:
                showwarning(title="Error!", message=f"Your files were not sent. {req.text}")

def clear_list_files():
    textbox.delete("1.0", "end")
    files.clear()

button_select = customtkinter.CTkButton(app, text="Выбрать файлы", command=select_files)
button_select.grid(row=2, column=0, padx=20, pady=5)
button_send = customtkinter.CTkButton(app, text="Отправить", command=send_file)
button_send.grid(row=2, column=1, padx=20, pady=5)

button_clear = customtkinter.CTkButton(textbox, text="Очистить", command=clear_list_files, fg_color="#e74c3c", hover_color="#c0392b")
button_clear.grid(column=0, sticky="ew", padx=50, pady=10)

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

app.mainloop()
