import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime
import time

class ProductivitySuite:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Productivity Suite")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f4f8')
        
        # Data storage
        self.notes = []
        self.files = []
        self.load_data()
        
        # Timer variables
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_mode = "stopwatch"
        
        # Create main interface
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="Personal Productivity Suite", 
                              font=('Arial', 24, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(expand=True)
        
        # Tab buttons
        button_frame = tk.Frame(self.root, bg='#ecf0f1', height=60)
        button_frame.pack(fill='x', pady=10)
        button_frame.pack_propagate(False)
        
        button_style = {'font': ('Arial', 12, 'bold'), 'width': 15, 'height': 2}
        
        self.calc_btn = tk.Button(button_frame, text="Calculator", bg='#3498db', fg='white',
                                  command=self.show_calculator, **button_style)
        self.calc_btn.pack(side='left', padx=10, expand=True)
        
        self.notes_btn = tk.Button(button_frame, text="Notes", bg='#95a5a6', fg='white',
                                   command=self.show_notes, **button_style)
        self.notes_btn.pack(side='left', padx=10, expand=True)
        
        self.timer_btn = tk.Button(button_frame, text="Timer", bg='#95a5a6', fg='white',
                                   command=self.show_timer, **button_style)
        self.timer_btn.pack(side='left', padx=10, expand=True)
        
        self.files_btn = tk.Button(button_frame, text="File Organizer", bg='#95a5a6', fg='white',
                                   command=self.show_files, **button_style)
        self.files_btn.pack(side='left', padx=10, expand=True)
        
        # Content frame
        self.content_frame = tk.Frame(self.root, bg='#f0f4f8')
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Show calculator by default
        self.show_calculator()
    
    # ==================== CALCULATOR ====================
    def show_calculator(self):
        self.clear_content()
        self.calc_btn.config(bg='#3498db')
        self.notes_btn.config(bg='#95a5a6')
        self.timer_btn.config(bg='#95a5a6')
        self.files_btn.config(bg='#95a5a6')
        
        calc_frame = tk.Frame(self.content_frame, bg='white', relief='raised', bd=2)
        calc_frame.pack(pady=20)
        
        # Display
        self.calc_display = tk.Entry(calc_frame, font=('Arial', 32), width=20, 
                                     justify='right', bd=10, bg='#2c3e50', fg='white')
        self.calc_display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.calc_display.insert(0, '0')
        
        # Calculator state
        self.calc_current = '0'
        self.calc_operator = None
        self.calc_previous = None
        self.calc_new_number = True
        
        # Button layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('÷', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('×', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
        ]
        
        for (text, row, col) in buttons:
            if text in '0123456789.':
                cmd = lambda t=text: self.calc_number_click(t)
                bg = '#ecf0f1'
            elif text in '÷×-+':
                cmd = lambda t=text: self.calc_operator_click(t)
                bg = '#e67e22'
            else:  # equals
                cmd = self.calc_equals
                bg = '#27ae60'
            
            btn = tk.Button(calc_frame, text=text, font=('Arial', 18, 'bold'),
                          width=5, height=2, command=cmd, bg=bg, fg='white')
            btn.grid(row=row, column=col, padx=5, pady=5)
        
        # Clear button
        clear_btn = tk.Button(calc_frame, text='Clear', font=('Arial', 18, 'bold'),
                            width=11, height=2, command=self.calc_clear, bg='#e74c3c', fg='white')
        clear_btn.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
    
    def calc_number_click(self, num):
        if self.calc_new_number:
            self.calc_current = num
            self.calc_new_number = False
        else:
            if self.calc_current == '0':
                self.calc_current = num
            else:
                self.calc_current += num
        self.calc_display.delete(0, tk.END)
        self.calc_display.insert(0, self.calc_current)
    
    def calc_operator_click(self, op):
        current_val = float(self.calc_current)
        if self.calc_previous is None:
            self.calc_previous = current_val
        elif self.calc_operator:
            result = self.calc_calculate(self.calc_previous, current_val, self.calc_operator)
            self.calc_display.delete(0, tk.END)
            self.calc_display.insert(0, str(result))
            self.calc_previous = result
        self.calc_operator = op
        self.calc_new_number = True
    
    def calc_calculate(self, a, b, op):
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '×':
            return a * b
        elif op == '÷':
            return a / b if b != 0 else 0
    
    def calc_equals(self):
        if self.calc_operator and self.calc_previous is not None:
            result = self.calc_calculate(self.calc_previous, float(self.calc_current), self.calc_operator)
            self.calc_display.delete(0, tk.END)
            self.calc_display.insert(0, str(result))
            self.calc_current = str(result)
            self.calc_previous = None
            self.calc_operator = None
            self.calc_new_number = True
    
    def calc_clear(self):
        self.calc_current = '0'
        self.calc_operator = None
        self.calc_previous = None
        self.calc_new_number = True
        self.calc_display.delete(0, tk.END)
        self.calc_display.insert(0, '0')
    
    # ==================== NOTES ====================
    def show_notes(self):
        self.clear_content()
        self.calc_btn.config(bg='#95a5a6')
        self.notes_btn.config(bg='#3498db')
        self.timer_btn.config(bg='#95a5a6')
        self.files_btn.config(bg='#95a5a6')
        
        # Left panel - notes list
        left_panel = tk.Frame(self.content_frame, bg='white', width=250)
        left_panel.pack(side='left', fill='both', padx=(0, 10))
        
        # New note button
        new_note_btn = tk.Button(left_panel, text="+ New Note", font=('Arial', 12, 'bold'),
                                bg='#27ae60', fg='white', command=self.create_new_note)
        new_note_btn.pack(pady=10, padx=10, fill='x')
        
        # Notes list
        notes_list_frame = tk.Frame(left_panel, bg='white')
        notes_list_frame.pack(fill='both', expand=True, padx=10)
        
        self.notes_listbox = tk.Listbox(notes_list_frame, font=('Arial', 11), height=20)
        self.notes_listbox.pack(side='left', fill='both', expand=True)
        self.notes_listbox.bind('<<ListboxSelect>>', self.load_selected_note)
        
        scrollbar = tk.Scrollbar(notes_list_frame, command=self.notes_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.notes_listbox.config(yscrollcommand=scrollbar.set)
        
        # Right panel - note editor
        right_panel = tk.Frame(self.content_frame, bg='white')
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Title
        tk.Label(right_panel, text="Title:", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', padx=10, pady=(10, 0))
        self.note_title = tk.Entry(right_panel, font=('Arial', 14), width=50)
        self.note_title.pack(padx=10, pady=5, fill='x')
        
        # Content
        tk.Label(right_panel, text="Content:", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', padx=10, pady=(10, 0))
        self.note_content = scrolledtext.ScrolledText(right_panel, font=('Arial', 11), 
                                                      width=50, height=20, wrap=tk.WORD)
        self.note_content.pack(padx=10, pady=5, fill='both', expand=True)
        
        # Buttons
        btn_frame = tk.Frame(right_panel, bg='white')
        btn_frame.pack(pady=10)
        
        save_btn = tk.Button(btn_frame, text="Save Note", font=('Arial', 11, 'bold'),
                           bg='#27ae60', fg='white', width=12, command=self.save_note)
        save_btn.pack(side='left', padx=5)
        
        delete_btn = tk.Button(btn_frame, text="Delete Note", font=('Arial', 11, 'bold'),
                             bg='#e74c3c', fg='white', width=12, command=self.delete_note)
        delete_btn.pack(side='left', padx=5)
        
        self.refresh_notes_list()
        self.current_note_index = None
    
    def refresh_notes_list(self):
        self.notes_listbox.delete(0, tk.END)
        for note in self.notes:
            self.notes_listbox.insert(tk.END, note['title'])
    
    def create_new_note(self):
        new_note = {
            'title': 'Untitled Note',
            'content': '',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.notes.insert(0, new_note)
        self.refresh_notes_list()
        self.notes_listbox.selection_clear(0, tk.END)
        self.notes_listbox.selection_set(0)
        self.load_selected_note(None)
        self.save_data()
    
    def load_selected_note(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            self.current_note_index = selection[0]
            note = self.notes[self.current_note_index]
            self.note_title.delete(0, tk.END)
            self.note_title.insert(0, note['title'])
            self.note_content.delete('1.0', tk.END)
            self.note_content.insert('1.0', note['content'])
    
    def save_note(self):
        if self.current_note_index is not None:
            self.notes[self.current_note_index]['title'] = self.note_title.get()
            self.notes[self.current_note_index]['content'] = self.note_content.get('1.0', tk.END).strip()
            self.notes[self.current_note_index]['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.refresh_notes_list()
            self.save_data()
            messagebox.showinfo("Success", "Note saved successfully!")
    
    def delete_note(self):
        if self.current_note_index is not None:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?"):
                del self.notes[self.current_note_index]
                self.note_title.delete(0, tk.END)
                self.note_content.delete('1.0', tk.END)
                self.current_note_index = None
                self.refresh_notes_list()
                self.save_data()
    
    # ==================== TIMER ====================
    def show_timer(self):
        self.clear_content()
        self.calc_btn.config(bg='#95a5a6')
        self.notes_btn.config(bg='#95a5a6')
        self.timer_btn.config(bg='#3498db')
        self.files_btn.config(bg='#95a5a6')
        
        timer_frame = tk.Frame(self.content_frame, bg='white')
        timer_frame.pack(fill='both', expand=True)
        
        # Mode buttons
        mode_frame = tk.Frame(timer_frame, bg='white')
        mode_frame.pack(pady=20)
        
        tk.Button(mode_frame, text="Stopwatch", font=('Arial', 12, 'bold'),
                 bg='#3498db', fg='white', width=12, command=lambda: self.set_timer_mode('stopwatch')).pack(side='left', padx=5)
        tk.Button(mode_frame, text="Countdown", font=('Arial', 12, 'bold'),
                 bg='#9b59b6', fg='white', width=12, command=lambda: self.set_timer_mode('countdown')).pack(side='left', padx=5)
        tk.Button(mode_frame, text="Pomodoro", font=('Arial', 12, 'bold'),
                 bg='#e67e22', fg='white', width=12, command=lambda: self.set_timer_mode('pomodoro')).pack(side='left', padx=5)
        
        # Timer display
        display_frame = tk.Frame(timer_frame, bg='#2c3e50', width=400, height=200)
        display_frame.pack(pady=30)
        display_frame.pack_propagate(False)
        
        self.timer_label = tk.Label(display_frame, text="00:00:00", font=('Arial', 48, 'bold'),
                                    bg='#2c3e50', fg='white')
        self.timer_label.pack(expand=True)
        
        # Timer input (for countdown)
        self.timer_input_frame = tk.Frame(timer_frame, bg='white')
        
        tk.Label(self.timer_input_frame, text="Set Minutes:", font=('Arial', 12), bg='white').pack(side='left', padx=5)
        self.timer_input = tk.Entry(self.timer_input_frame, font=('Arial', 14), width=10)
        self.timer_input.pack(side='left', padx=5)
        self.timer_input.insert(0, "25")
        tk.Button(self.timer_input_frame, text="Set", font=('Arial', 11, 'bold'),
                 bg='#3498db', fg='white', command=self.set_timer_value).pack(side='left', padx=5)
        
        # Control buttons
        control_frame = tk.Frame(timer_frame, bg='white')
        control_frame.pack(pady=20)
        
        self.start_btn = tk.Button(control_frame, text="Start", font=('Arial', 14, 'bold'),
                                   bg='#27ae60', fg='white', width=12, command=self.start_timer)
        self.start_btn.pack(side='left', padx=5)
        
        self.pause_btn = tk.Button(control_frame, text="Pause", font=('Arial', 14, 'bold'),
                                   bg='#f39c12', fg='white', width=12, command=self.pause_timer)
        self.pause_btn.pack(side='left', padx=5)
        
        self.reset_btn = tk.Button(control_frame, text="Reset", font=('Arial', 14, 'bold'),
                                   bg='#e74c3c', fg='white', width=12, command=self.reset_timer)
        self.reset_btn.pack(side='left', padx=5)
        
        self.set_timer_mode('stopwatch')
    
    def set_timer_mode(self, mode):
        self.timer_mode = mode
        self.reset_timer()
        if mode == 'countdown' or mode == 'pomodoro':
            self.timer_input_frame.pack(pady=10)
            if mode == 'pomodoro':
                self.timer_input.delete(0, tk.END)
                self.timer_input.insert(0, "25")
        else:
            self.timer_input_frame.pack_forget()
    
    def set_timer_value(self):
        try:
            minutes = int(self.timer_input.get())
            self.timer_seconds = minutes * 60
            self.update_timer_display()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
    
    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.run_timer()
    
    def pause_timer(self):
        self.timer_running = False
    
    def reset_timer(self):
        self.timer_running = False
        self.timer_seconds = 0
        if self.timer_mode == 'pomodoro':
            self.timer_seconds = 25 * 60
        self.update_timer_display()
    
    def run_timer(self):
        if self.timer_running:
            if self.timer_mode == 'stopwatch':
                self.timer_seconds += 1
            else:
                if self.timer_seconds > 0:
                    self.timer_seconds -= 1
                else:
                    self.timer_running = False
                    messagebox.showinfo("Timer", "Time's up!")
                    return
            
            self.update_timer_display()
            self.root.after(1000, self.run_timer)
    
    def update_timer_display(self):
        hours = self.timer_seconds // 3600
        minutes = (self.timer_seconds % 3600) // 60
        seconds = self.timer_seconds % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=time_str)
    
    # ==================== FILE ORGANIZER ====================
    def show_files(self):
        self.clear_content()
        self.calc_btn.config(bg='#95a5a6')
        self.notes_btn.config(bg='#95a5a6')
        self.timer_btn.config(bg='#95a5a6')
        self.files_btn.config(bg='#3498db')
        
        files_frame = tk.Frame(self.content_frame, bg='white')
        files_frame.pack(fill='both', expand=True)
        
        # Top controls
        top_frame = tk.Frame(files_frame, bg='white')
        top_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Button(top_frame, text="+ Add File", font=('Arial', 11, 'bold'),
                 bg='#27ae60', fg='white', width=12, command=self.add_file).pack(side='left', padx=5)
        
        tk.Label(top_frame, text="Filter:", font=('Arial', 11), bg='white').pack(side='left', padx=(20, 5))
        
        self.filter_var = tk.StringVar(value="All")
        filters = ["All", "Work", "Personal", "Finance", "Other"]
        for f in filters:
            tk.Radiobutton(top_frame, text=f, variable=self.filter_var, value=f,
                          bg='white', font=('Arial', 10), command=self.refresh_files_list).pack(side='left', padx=5)
        
        # Files table
        table_frame = tk.Frame(files_frame, bg='white')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create treeview
        columns = ('Name', 'Category', 'Size', 'Date')
        self.files_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.files_tree.heading(col, text=col)
            self.files_tree.column(col, width=150)
        
        self.files_tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(table_frame, command=self.files_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.files_tree.config(yscrollcommand=scrollbar.set)
        
        # Delete button
        tk.Button(files_frame, text="Delete Selected", font=('Arial', 11, 'bold'),
                 bg='#e74c3c', fg='white', width=15, command=self.delete_file).pack(pady=10)
        
        self.refresh_files_list()
    
    def add_file(self):
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add File")
        dialog.geometry("400x300")
        dialog.configure(bg='white')
        
        tk.Label(dialog, text="File Name:", font=('Arial', 11), bg='white').pack(pady=(20, 5))
        name_entry = tk.Entry(dialog, font=('Arial', 11), width=30)
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Category:", font=('Arial', 11), bg='white').pack(pady=(10, 5))
        category_var = tk.StringVar(value="Work")
        categories = ["Work", "Personal", "Finance", "Other"]
        for cat in categories:
            tk.Radiobutton(dialog, text=cat, variable=category_var, value=cat,
                          bg='white', font=('Arial', 10)).pack()
        
        tk.Label(dialog, text="Size:", font=('Arial', 11), bg='white').pack(pady=(10, 5))
        size_entry = tk.Entry(dialog, font=('Arial', 11), width=30)
        size_entry.pack(pady=5)
        size_entry.insert(0, "1.5 MB")
        
        def save_file():
            new_file = {
                'name': name_entry.get(),
                'category': category_var.get(),
                'size': size_entry.get(),
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            self.files.append(new_file)
            self.save_data()
            self.refresh_files_list()
            dialog.destroy()
        
        tk.Button(dialog, text="Add File", font=('Arial', 12, 'bold'),
                 bg='#27ae60', fg='white', width=15, command=save_file).pack(pady=20)
    
    def refresh_files_list(self):
        for item in self.files_tree.get_children():
            self.files_tree.delete(item)
        
        filter_val = self.filter_var.get()
        for file in self.files:
            if filter_val == "All" or file['category'] == filter_val:
                self.files_tree.insert('', tk.END, values=(file['name'], file['category'], 
                                                           file['size'], file['date']))
    
    def delete_file(self):
        selection = self.files_tree.selection()
        if selection:
            item = self.files_tree.item(selection[0])
            file_name = item['values'][0]
            if messagebox.askyesno("Confirm Delete", f"Delete {file_name}?"):
                self.files = [f for f in self.files if f['name'] != file_name]
                self.save_data()
                self.refresh_files_list()
    
    # ==================== DATA MANAGEMENT ====================
    def load_data(self):
        try:
            if os.path.exists('productivity_data.json'):
                with open('productivity_data.json', 'r') as f:
                    data = json.load(f)
                    self.notes = data.get('notes', [])
                    self.files = data.get('files', [])
        except Exception as e:
            print(f"Error loading data: {e}")
            self.notes = []
            self.files = []
    
    def save_data(self):
        try:
            data = {
                'notes': self.notes,
                'files': self.files
            }
            with open('productivity_data.json', 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ProductivitySuite(root)
    root.mainloop()
