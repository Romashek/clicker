import tkinter as tk
from datetime import datetime, timedelta
import cv2
from PIL import Image, ImageTk
import keyboard  # Импортируем библиотеку keyboard

class ReactionTest:
    def __init__(self, master):
        self.master = master
        master.title("Проверка на реакцию")

        # Создаем элементы интерфейса
        self.delay_label = tk.Label(master, text="Задержка (мин:сек:мс):")
        self.delay_entry = tk.Entry(master)
        self.delay_entry.insert(0, "0:3:0")
        self.start_button = tk.Button(master, text="Начать", command=self.start_test)
        self.result_label = tk.Label(master, text="", font=("Arial", 24))
        self.video_label = tk.Label(master)

        # Размещаем элементы на экране
        self.delay_label.grid(row=0, column=0, padx=20, pady=20)
        self.delay_entry.grid(row=0, column=1, padx=20, pady=20)
        self.start_button.grid(row=1, column=0, columnspan=2, padx=20, pady=20)
        self.result_label.grid(row=2, column=0, columnspan=2, padx=20, pady=20)
        self.video_label.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

        # Переменные для хранения данных
        self.start_time = None
        self.left_click_time = None
        self.right_click_time = None
        self.is_running = False
        self.left_clicked = False
        self.right_clicked = False
        self.cap = None

    def start_test(self):
        if not self.is_running:
            # Получаем значение задержки из Entry
            delay_parts = self.delay_entry.get().split(":")
            minutes = int(delay_parts[0])
            seconds = int(delay_parts[1])
            milliseconds = int(delay_parts[2])
            delay = timedelta(minutes=minutes, seconds=seconds, milliseconds=milliseconds)

            # Отображаем задержку
            self.result_label.config(text=f"Ждите {delay}", fg="black")

            # Запускаем таймер
            self.master.after(int(delay.total_seconds() * 1000), self.start_reaction)
            self.is_running = True

            # Запускаем воспроизведение видео
            self.cap = cv2.VideoCapture("abc.mp4")
            self.play_video()

    def start_reaction(self):
        # Запоминаем время начала
        self.start_time = datetime.now()

        # Включаем зеленый цвет
        self.result_label.config(text="Нажмите левую или правую кнопку мыши", fg="green")

        # Добавляем обработчики событий на окно
        self.master.bind("<Button-1>", self.handle_left_click)  # ЛКМ
        self.master.bind("<Button-3>", self.handle_right_click)  # ПКМ

        # Также добавляем обработчики для клавиш A и D
        keyboard.on_press_key('a', self.handle_left_click_key)
        keyboard.on_press_key('d', self.handle_right_click_key)

    def handle_left_click(self, event):
        if self.is_running and not self.left_clicked:
            self.left_click_time = datetime.now()
            self.left_clicked = True
            self.update_result()

            # Если правая кнопка уже была нажата, выводим результаты
            if self.right_clicked:
                self.display_results()

    def handle_right_click(self, event):
        if self.is_running and not self.right_clicked:
            self.right_click_time = datetime.now()
            self.right_clicked = True
            self.update_result()

            # Если левая кнопка уже была нажата, выводим результаты
            if self.left_clicked:
                self.display_results()

    def handle_left_click_key(self, event):
        # Эмулируем нажатие левой кнопки мыши
        if self.is_running and not self.left_clicked:
            self.left_click_time = datetime.now()
            self.left_clicked = True
            self.update_result()

            # Если правая кнопка уже была нажата, выводим результаты
            if self.right_clicked:
                self.display_results()

    def handle_right_click_key(self, event):
        # Эмулируем нажатие правой кнопки мыши
        if self.is_running and not self.right_clicked:
            self.right_click_time = datetime.now()
            self.right_clicked = True
            self.update_result()

            # Если левая кнопка уже была нажата, выводим результаты
            if self.left_clicked:
                self.display_results()

    def update_result(self):
        current_time = datetime.now()
        result_text = f"Время нажатия: {self.format_time(current_time - self.start_time)}"
        self.result_label.config(text=result_text, fg="black")

    def display_results(self):
        # Удаляем обработчики событий
        self.master.unbind("<Button-1>")
        self.master.unbind("<Button-3>")
        keyboard.unhook_all()  # Удаляем обработчики клавиш
        self.is_running = False

        # Останавливаем воспроизведение видео
        self.cap.release()

        # Выводим результаты
        result_text = ""
        if self.left_clicked and self.right_clicked:
            if self.left_click_time < self.right_click_time:
                result_text += f"\n"
                result_text += f"Время нажатия левой кнопки: {self.format_time(self.left_click_time - self.start_time)}\n"
                result_text += f"Время нажатия правой кнопки: {self.format_time(self.right_click_time - self.start_time)}"
            else:
                result_text += f"\n"
                result_text += f"Время нажатия правой кнопки: {self.format_time(self.right_click_time - self.start_time)}\n"
                result_text += f"Время нажатия левой кнопки: {self.format_time(self.left_click_time - self.start_time)}"
        elif self.left_clicked:
            result_text += f"Время нажатия левой кнопки: {self.format_time(self.left_click_time - self.start_time)}"
        elif self.right_clicked:
            result_text += f"Время нажатия правой кнопки: {self.format_time(self.right_click_time - self.start_time)}"
        self.result_label.config(text=result_text, fg="black")

    def format_time(self, time_delta):
        total_seconds = time_delta.total_seconds()
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int(time_delta.microseconds / 1000)
        return f"{minutes}:{seconds:02d}:{milliseconds:03d}"

    def play_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=img)
            self.video_label.configure(image=photo)
            self.video_label.image = photo
            self.master.after(30, self.play_video)
        else:
            self.cap.release()

root = tk.Tk()
app = ReactionTest(root)
root.mainloop()