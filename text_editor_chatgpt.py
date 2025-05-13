import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                txt_edit.delete("1.0", tk.END)
                txt_edit.insert(tk.END, file.read())
            window.title(f"Text Editor - {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(txt_edit.get("1.0", tk.END).strip())
            window.title(f"Text Editor - {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

window = tk.Tk()
window.title("Text Editor")
window.geometry("800x500")
window.configure(bg="#1C1C1C")

window.rowconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

txt_edit = tk.Text(window, wrap="word", font=("Arial", 12), bg="#2B2B2B", fg="#F8F8F2", insertbackground="white")
txt_edit.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

frame_buttons = ttk.Frame(window, padding=5, style="TFrame")
frame_buttons.grid(row=0, column=0, sticky="ns")

btn_open = ttk.Button(frame_buttons, text="Open", command=open_file, style="TButton")
btn_save = ttk.Button(frame_buttons, text="Save", command=save_file, style="TButton")
btn_open.pack(fill="x", pady=5)
btn_save.pack(fill="x", pady=5)

style = ttk.Style()
style.configure("TFrame", background="#1C1C1C")
style.configure("TButton", background="#3C3F41", foreground="white", font=("Arial", 10, "bold"))
style.map("TButton", background=[("active", "#4F5255")])

window.mainloop()
