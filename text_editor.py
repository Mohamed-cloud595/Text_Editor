import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file():
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt") , ("All Files", "*.*")])
    
    if not filepath:
        return
    
    txt_edit.delete("1.0" , tk.END)
 
    with open(filepath , 'r') as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END , text)
        
    window.title(f"Text Editor - {filepath}")
def save_file():
    filepath = asksaveasfilename(defaultextension="txt" , filetypes=[("Text Files", "*.txt") , ("All Files", "*.*")])
    
    if not filepath:
        return
    
    with open(filepath , 'w') as output_file:
        text = txt_edit.get("1.0" , tk.END)
        output_file.write(text)

    window.title(f"Text Editor - {filepath}")
window = tk.Tk()
window.title("Text Editor")
window.rowconfigure(0 , minsize=400)
window.columnconfigure( 1 , minsize=600)

txt_edit = tk.Text(window)
frame_buttons = tk.Frame(window , relief=tk.RAISED)
btn_open = tk.Button(frame_buttons , text="Open File" , command=open_file)
btn_save = tk.Button(frame_buttons , text="Save As" , command=save_file)

btn_open.grid(row=0 , column=0 , sticky="ew" , padx=5 , pady=5)
btn_save.grid(row=1 , column=0 , sticky="ew" , padx=5 )

frame_buttons.grid(row=0 , column=0 , sticky="nw") 
txt_edit.grid(row=0 , column=1)

window.mainloop()