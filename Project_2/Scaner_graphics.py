import customtkinter as ctk
from tkinter import filedialog
import threading
import time
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GradientFrame(ctk.CTkFrame):
    def __init__(self, master, color1, color2, **kwargs):
        super().__init__(master, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.bind("<Configure>", self._draw_gradient)
        
    def _draw_gradient(self, event=None):
        self.canvas.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        
        for i in range(height):
            ratio = i / height
            r = int(self.color1[0] + (self.color2[0] - self.color1[0]) * ratio)
            g = int(self.color1[1] + (self.color2[1] - self.color1[1]) * ratio)
            b = int(self.color1[2] + (self.color2[2] - self.color1[2]) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, width, i, fill=color)

def animate_result():
    result_frame.configure(fg_color=["#1a1a2e", "#1a1a2e"])
    for i in range(10):
        alpha = i / 10
        color = f"#{int(26 + 40*alpha):02x}{int(26 + 40*alpha):02x}{int(46 + 40*alpha):02x}"
        result_frame.configure(fg_color=color)
        time.sleep(0.03)

def analyze_text():
    text = text_input.get("1.0", "end-1c").strip()
    if not text:
        result_label.configure(text="⚠️ Введите текст для анализа")
        return
    
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    unique_words = len(set(words))
    sentences = text.count('.') + text.count('!') + text.count('?')
    avg_word_len = sum(len(w) for w in words) / len(words) if words else 0
    
    result_text = f"""✨ РЕЗУЛЬТАТЫ АНАЛИЗА
{'─'*35}

📝 Слов: {word_count}
🔤 Символов: {char_count}
✨ Уникальных слов: {unique_words}
💬 Предложений: {sentences}
📊 Сред. длина слова: {avg_word_len:.1f}

🏆 Самые частые слова:
{get_top_words(words)}"""
    
    result_label.configure(text=result_text)
    threading.Thread(target=animate_result, daemon=True).start()

def open_file():
    filepath = filedialog.askopenfilename(
        title="Выберите текстовый файл",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if filepath:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            text_input.delete("1.0", "end")
            text_input.insert("1.0", content)
            file_label.configure(text=f"📄 {os.path.basename(filepath)}")
        except Exception as e:
            result_label.configure(text=f"❌ Ошибка чтения файла: {e}")

def get_top_words(words):
    from collections import Counter
    if not words:
        return "  (нет данных)"
    top = Counter(words).most_common(3)
    return "\n".join(f"  • {w}: {c}" for w, c in top)

root = ctk.CTk()
root.title("✨ Text Analyzer Pro")
root.geometry("700x600")
root.configure(fg_color=["#0f0f23", "#0f0f23"])

header = ctk.CTkFrame(root, fg_color=["#0f0f23", "#0f0f23"], height=100, corner_radius=0)
header.pack(fill="x")
header.pack_propagate(False)

title_plate = ctk.CTkFrame(header, fg_color=["#1a1a2e", "#1a1a2e"], 
                             corner_radius=15, border_width=2, border_color="#e94560")
title_plate.pack(pady=20, padx=50, fill="x")

title_label = ctk.CTkLabel(title_plate, text="✨ Text Scanner Pro", 
                            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
                            text_color="#e94560")
title_label.pack(pady=15)

main_container = ctk.CTkFrame(root, fg_color="transparent")
main_container.pack(fill="both", expand=True, padx=30, pady=20)

input_label = ctk.CTkLabel(main_container, text="💬 Введите текст или выберите файл:", 
                            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                            text_color="#16f4d0")
input_label.pack(anchor="w", pady=(0, 10))

file_frame = ctk.CTkFrame(main_container, fg_color="transparent")
file_frame.pack(fill="x", pady=(0, 10))

file_btn = ctk.CTkButton(file_frame, text="📁 Выбрать файл", 
                          font=ctk.CTkFont(family="Segoe UI", size=12),
                          fg_color=["#533483", "#533483"],
                          hover_color=["#e94560", "#e94560"],
                          command=open_file, width=150, height=35)
file_btn.pack(side="left")

file_label = ctk.CTkLabel(file_frame, text="Файл не выбран", 
                           font=ctk.CTkFont(family="Segoe UI", size=11),
                           text_color="#aaaaaa")
file_label.pack(side="left", padx=(10, 0))

text_input = ctk.CTkTextbox(main_container, height=150, 
                             font=ctk.CTkFont(family="Segoe UI", size=13),
                             fg_color=["#1a1a2e", "#1a1a2e"],
                             border_color="#e94560", border_width=2)
text_input.pack(fill="x", pady=(0, 20))

analyze_btn = ctk.CTkButton(main_container, text="▶ АНАЛИЗИРОВАТЬ", 
                             font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                             fg_color=["#e94560", "#e94560"],
                             hover_color=["#16f4d0", "#16f4d0"],
                             text_color="#ffffff",
                             height=50, corner_radius=25,
                             command=analyze_text)
analyze_btn.pack(pady=(0, 20))

result_frame = ctk.CTkFrame(main_container, fg_color=["#1a1a2e", "#1a1a2e"], 
                              corner_radius=15, border_width=2, border_color="#16f4d0")
result_frame.pack(fill="both", expand=True)

result_label = ctk.CTkLabel(result_frame, text="📊 Нажмите кнопку для анализа текста",
                             font=ctk.CTkFont(family="Consolas", size=13),
                             text_color="#16f4d0", justify="left",
                             wraplength=600)
result_label.pack(padx=20, pady=20, fill="both", expand=True)

root.mainloop()
