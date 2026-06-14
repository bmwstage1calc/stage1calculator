import csv
import tkinter as tk
from tkinter import messagebox

DATABASE_FILE = "bmw_database.csv"


def get_engine_family(engine_code):
    if not engine_code:
        return "-"
    if engine_code == "Electric":
        return "Electric"
    if "Hybrid" in engine_code:
        return "Hybrid"
    return engine_code[:3]


def load_cars():
    cars = []

    with open(DATABASE_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["engine"] = get_engine_family(row.get("engine_code", ""))
            cars.append(row)

    return cars


cars = load_cars()
filtered_cars = cars.copy()


def update_list(event=None):
    search_text = search_entry.get().lower()
    list_box.delete(0, tk.END)
    filtered_cars.clear()

    for car in cars:
        full_name = f"{car['model']} {car['body']} {car['engine']} {car['engine_code']}".lower()

        if search_text in full_name:
            filtered_cars.append(car)
            list_box.insert(
                tk.END,
                f"{car['model']} | {car['body']} | {car['engine_code']}"
            )


def calculate():
    selected = list_box.curselection()

    if not selected:
        messagebox.showwarning("Ошибка", "Выбери автомобиль из списка")
        return

    car = filtered_cars[selected[0]]

    stock_hp = int(car["stock_hp"])
    stock_nm = int(car["stock_nm"])
    stage1_hp = int(car["stage1_hp"])
    stage1_nm = int(car["stage1_nm"])

    hp_gain = stage1_hp - stock_hp
    nm_gain = stage1_nm - stock_nm

    hp_percent = hp_gain / stock_hp * 100
    nm_percent = nm_gain / stock_nm * 100

    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)

    result_text.insert(tk.END, f"Модель: {car['model']}\n")
    result_text.insert(tk.END, f"Кузов: {car['body']}\n")
    result_text.insert(tk.END, f"Двигатель: {car['engine']}\n")
    result_text.insert(tk.END, f"Маркировка двигателя: {car['engine_code']}\n")
    result_text.insert(tk.END, f"Серия двигателя: {car['engine']}\n\n")

    result_text.insert(tk.END, f"Завод: {stock_hp} л.с. / {stock_nm} Нм\n")
    result_text.insert(tk.END, f"Stage 1: {stage1_hp} л.с. / {stage1_nm} Нм\n\n")

    result_text.insert(tk.END, f"Прирост мощности: +{hp_gain} л.с. ({hp_percent:.1f}%)\n")
    result_text.insert(tk.END, f"Прирост момента: +{nm_gain} Нм ({nm_percent:.1f}%)\n")

    result_text.config(state="disabled")


window = tk.Tk()
window.title("BMW Stage1 Calculator")
window.geometry("1100x900")
window.configure(bg="#0f1115")

try:
    logo_img = tk.PhotoImage(file="bmw_logo.png")
    logo_img = logo_img.subsample(7, 7)

    logo_label = tk.Label(window, image=logo_img, bg="#0f1115")
    logo_label.pack(pady=10)

except Exception as e:
    print(e)

title = tk.Label(
    window,
    text="BMW Stage1 Calculator",
    font=("Arial", 24, "bold"),
    bg="#0f1115",
    fg="#00a3ff"
)
title.pack(pady=15)

subtitle = tk.Label(
    window,
    text="Поиск BMW / кузов / двигатель / маркировка",
    font=("Arial", 13),
    bg="#0f1115",
    fg="white"
)
subtitle.pack()

search_entry = tk.Entry(
    window,
    width=60,
    font=("Arial", 12, "bold"),
    bg="#102542",
    fg="#ffffff",
    insertbackground="#00a3ff",
    relief="solid",
    bd=1
)
search_entry.pack(pady=10, ipady=8)
search_entry.bind("<KeyRelease>", update_list)

list_box = tk.Listbox(
    window,
    width=80,
    height=12,
    font=("Arial", 12),
    bg="#151922",
    fg="white",
    selectbackground="#00a3ff",
    selectforeground="black",
    relief="flat"
)
list_box.pack(pady=10)

button = tk.Button(
    window,
    text="Рассчитать Stage 1",
    command=calculate,
    font=("Arial", 13, "bold"),
    bg="#00a3ff",
    fg="black",
    activebackground="#00ff99",
    relief="flat",
    padx=20,
    pady=8
)
button.pack(pady=10)

result_text = tk.Text(
    window,
    width=75,
    height=12,
    font=("Arial", 13, "bold"),
    bg="#151922",
    fg="#ffffff",
    relief="flat"
)
result_text.pack(pady=10)
result_text.config(state="disabled")

footer = tk.Label(
    window,
    text=f"BMW Performance Database 1996–2025 | Моделей в базе: {len(cars)} | v1.5",
    font=("Arial", 10),
    bg="#0f1115",
    fg="#888888"
)
footer.pack(pady=5)

update_list()
window.mainloop()