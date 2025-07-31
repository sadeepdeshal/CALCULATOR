import tkinter as tk
from tkinter import messagebox
import math

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("350x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#1e1e1e')
        
        # Variables
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.result_displayed = False
        
        # Create display
        self.create_display()
        
        # Create buttons
        self.create_buttons()
    
    def create_display(self):
        # Display frame with padding
        display_frame = tk.Frame(self.root, bg='#1e1e1e', height=120)
        display_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        display_frame.pack_propagate(False)
        
        # Secondary display (for operation history)
        self.secondary_display = tk.Label(
            display_frame,
            text="",
            font=('SF Pro Display', 16),
            bg='#1e1e1e',
            fg='#8e8e93',
            anchor='e',
            height=1
        )
        self.secondary_display.pack(fill=tk.X, side=tk.TOP)
        
        # Main display
        self.display = tk.Label(
            display_frame,
            text=self.current,
            font=('SF Pro Display', 40, 'bold'),
            bg='#1e1e1e',
            fg='white',
            anchor='e',
            height=2
        )
        self.display.pack(fill=tk.BOTH, expand=True)
    
    def create_buttons(self):
        # Button frame
        button_frame = tk.Frame(self.root, bg='#1e1e1e')
        button_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Button configuration
        button_config = {
            'font': ('SF Pro Display', 24, 'bold'),
            'border': 0,
            'relief': 'flat',
            'cursor': 'hand2'
        }
        
        # Button layout with styling
        buttons = [
            [('AC', '#a6a6a6', 'black'), ('±', '#a6a6a6', 'black'), ('%', '#a6a6a6', 'black'), ('÷', '#ff9500', 'white')],
            [('7', '#333333', 'white'), ('8', '#333333', 'white'), ('9', '#333333', 'white'), ('×', '#ff9500', 'white')],
            [('4', '#333333', 'white'), ('5', '#333333', 'white'), ('6', '#333333', 'white'), ('-', '#ff9500', 'white')],
            [('1', '#333333', 'white'), ('2', '#333333', 'white'), ('3', '#333333', 'white'), ('+', '#ff9500', 'white')],
            [('0', '#333333', 'white', 2), ('.', '#333333', 'white'), ('=', '#ff9500', 'white')]
        ]
        
        # Create buttons with proper styling
        for i, row in enumerate(buttons):
            for j, btn_info in enumerate(row):
                text = btn_info[0]
                bg_color = btn_info[1]
                fg_color = btn_info[2]
                colspan = btn_info[3] if len(btn_info) > 3 else 1
                
                btn = tk.Button(
                    button_frame,
                    text=text,
                    bg=bg_color,
                    fg=fg_color,
                    activebackground=self.get_active_color(bg_color),
                    activeforeground=fg_color,
                    command=lambda t=text: self.button_click(t),
                    **button_config
                )
                
                btn.grid(
                    row=i, 
                    column=j, 
                    columnspan=colspan,
                    sticky='nsew', 
                    padx=3, 
                    pady=3,
                    ipady=15
                )
                
                # Add hover effects
                self.add_hover_effect(btn, bg_color)
        
        # Configure grid weights for responsive design
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            button_frame.grid_columnconfigure(j, weight=1)
    
    def get_active_color(self, color):
        """Get a lighter shade for active state"""
        color_map = {
            '#333333': '#4d4d4d',
            '#a6a6a6': '#bfbfbf',
            '#ff9500': '#ffb143'
        }
        return color_map.get(color, color)
    
    def add_hover_effect(self, button, original_color):
        """Add hover effect to buttons"""
        hover_color = self.get_active_color(original_color)
        
        def on_enter(e):
            button.configure(bg=hover_color)
        
        def on_leave(e):
            button.configure(bg=original_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def button_click(self, value):
        try:
            if value.isdigit():
                self.number_click(value)
            elif value == '.':
                self.decimal_click()
            elif value in ['÷', '×', '-', '+']:
                self.operator_click(value)
            elif value == '=':
                self.equals_click()
            elif value == 'AC':
                self.clear_click()
            elif value == '±':
                self.plus_minus_click()
            elif value == '%':
                self.percentage_click()
        except Exception:
            self.show_error()
    
    def number_click(self, number):
        if self.current == "0" or self.result_displayed:
            self.current = number
            self.result_displayed = False
        else:
            if len(self.current) < 12:  
                self.current += number
        self.update_display()
    
    def decimal_click(self):
        if self.result_displayed:
            self.current = "0."
            self.result_displayed = False
        elif '.' not in self.current and len(self.current) < 11:
            self.current += '.'
        self.update_display()
    
    def operator_click(self, op):
        if self.operator and not self.result_displayed:
            self.equals_click()
        
        self.previous = self.current
        self.operator = op
        self.result_displayed = True
        self.update_secondary_display()
    
    def equals_click(self):
        if self.operator and self.previous:
            try:
                prev = float(self.previous)
                curr = float(self.current)
                
                operations = {
                    '+': lambda x, y: x + y,
                    '-': lambda x, y: x - y,
                    '×': lambda x, y: x * y,
                    '÷': lambda x, y: x / y if y != 0 else None
                }
                
                result = operations[self.operator](prev, curr)
                
                if result is None:
                    self.show_error("Cannot divide by zero")
                    return
                
                # Format result nicely
                if abs(result) < 1e-10:
                    result = 0
                
                if result == int(result) and abs(result) < 1e10:
                    self.current = str(int(result))
                else:
                    # Handle very large or very small numbers
                    if abs(result) >= 1e10 or (abs(result) < 1e-4 and result != 0):
                        self.current = f"{result:.6e}"
                    else:
                        self.current = f"{result:.10g}"
                
                self.previous = ""
                self.operator = ""
                self.result_displayed = True
                self.secondary_display.config(text="")
                self.update_display()
                
            except Exception:
                self.show_error()
    
    def clear_click(self):
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.result_displayed = False
        self.secondary_display.config(text="")
        self.update_display()
    
    def plus_minus_click(self):
        if self.current != "0":
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
        self.update_display()
    
    def percentage_click(self):
        try:
            result = float(self.current) / 100
            if result == int(result):
                self.current = str(int(result))
            else:
                self.current = f"{result:.10g}"
            self.result_displayed = True
            self.update_display()
        except Exception:
            self.show_error()
    
    def update_display(self):
        # Format display text
        display_text = self.current
        
        # Handle very long numbers
        if len(display_text) > 12:
            try:
                num = float(display_text)
                if abs(num) >= 1e12:
                    display_text = f"{num:.4e}"
                else:
                    display_text = display_text[:12]
            except:
                display_text = display_text[:12]
        
        self.display.config(text=display_text)
    
    def update_secondary_display(self):
        if self.previous and self.operator:
            self.secondary_display.config(text=f"{self.previous} {self.operator}")
    
    def show_error(self, message="Error"):
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.result_displayed = False
        self.secondary_display.config(text="")
        self.update_display()
        
        # Flash the display red briefly
        self.display.config(fg='#ff453a')
        self.root.after(500, lambda: self.display.config(fg='white'))

def main():
    root = tk.Tk()
    
    # Try to set app icon if available
    try:
        # This would work if you have an icon file
        # root.iconbitmap('calculator.ico')
        pass
    except:
        pass
    
    calculator = ModernCalculator(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
