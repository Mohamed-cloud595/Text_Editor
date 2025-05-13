import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font
import os

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor - Untitled")
        self.root.geometry("800x600")
        self.current_file = None
        self.setup_ui()
        self.create_menu()
        self.bind_shortcuts()
        
    def setup_ui(self):
        # Configure grid weights
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        
        # Create toolbar
        self.toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        
        # Toolbar buttons with icons would be better, but using text for simplicity
        self.open_btn = tk.Button(self.toolbar, text="Open", command=self.open_file)
        self.save_btn = tk.Button(self.toolbar, text="Save", command=self.save_file)
        self.save_as_btn = tk.Button(self.toolbar, text="Save As", command=self.save_file_as)
        
        self.open_btn.pack(side=tk.LEFT, padx=2, pady=2)
        self.save_btn.pack(side=tk.LEFT, padx=2, pady=2)
        self.save_as_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.toolbar.grid(row=0, column=0, sticky="ew")
        
        # Text area with scrollbar
        self.text_frame = tk.Frame(self.root)
        self.text_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        
        self.text_area = scrolledtext.ScrolledText(
            self.text_frame, 
            wrap=tk.WORD, 
            font=('Consolas', 12),
            undo=True
        )
        self.text_area.pack(expand=True, fill=tk.BOTH)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root, 
            text="Ready", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky="ew")
        
    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_editor)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        
        # View menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.font_size = tk.IntVar(value=12)
        self.view_menu.add_radiobutton(label="Small Font", variable=self.font_size, value=10, command=self.change_font)
        self.view_menu.add_radiobutton(label="Medium Font", variable=self.font_size, value=12, command=self.change_font)
        self.view_menu.add_radiobutton(label="Large Font", variable=self.font_size, value=14, command=self.change_font)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        
        self.root.config(menu=self.menu_bar)
    
    def bind_shortcuts(self):
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-S>', lambda e: self.save_file_as())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        
    def change_font(self):
        font_size = self.font_size.get()
        current_font = font.Font(font=self.text_area['font'])
        new_font = (current_font.actual()['family'], font_size)
        self.text_area.configure(font=new_font)
    
    def update_title(self):
        if self.current_file:
            self.root.title(f"Text Editor - {os.path.basename(self.current_file)}")
        else:
            self.root.title("Text Editor - Untitled")
    
    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.after(3000, lambda: self.status_bar.config(text="Ready"))
    
    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.update_title()
        self.update_status("New file created")
    
    def open_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("HTML Files", "*.html"),
                ("CSS Files", "*.css"),
                ("JavaScript Files", "*.js"),
                ("All Files", "*.*")
            ]
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'r') as input_file:
                content = input_file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            
            self.current_file = filepath
            self.update_title()
            self.update_status(f"Opened: {os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file:\n{str(e)}")
    
    def save_file(self):
        if not self.current_file:
            self.save_file_as()
            return
        
        try:
            with open(self.current_file, 'w') as output_file:
                text = self.text_area.get(1.0, tk.END)
                output_file.write(text)
            
            self.update_status(f"Saved: {os.path.basename(self.current_file)}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
            return False
    
    def save_file_as(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension="txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("HTML Files", "*.html"),
                ("CSS Files", "*.css"),
                ("JavaScript Files", "*.js"),
                ("All Files", "*.*")
            ]
        )
        
        if not filepath:
            return False
        
        try:
            with open(filepath, 'w') as output_file:
                text = self.text_area.get(1.0, tk.END)
                output_file.write(text)
            
            self.current_file = filepath
            self.update_title()
            self.update_status(f"Saved as: {os.path.basename(filepath)}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
            return False
    
    def exit_editor(self):
        if self.check_unsaved_changes():
            self.root.destroy()
    
    def check_unsaved_changes(self):
        if not self.current_file and self.text_area.get(1.0, "end-1c"):
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before exiting?"
            )
            
            if response is None:  # Cancel
                return False
            elif response:  # Yes
                return self.save_file_as()
            else:  # No
                return True
        
        return True
    
    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")
    
    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")
    
    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")
    
    def select_all(self):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        return 'break'

def main():
    root = tk.Tk()
    editor = TextEditor(root)
    
    # Handle window close
    root.protocol("WM_DELETE_WINDOW", editor.exit_editor)
    
    root.mainloop()

if __name__ == "__main__":
    main()