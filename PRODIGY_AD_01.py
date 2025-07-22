import tkinter as tk
from tkinter import font

class VibrantCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Vibrant Calculator")
        self.root.geometry("380x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#2E3440")  # Dark background
        
        # Color palette 
        self.colors = {
            'display_bg': "#3B4252",
            'display_fg': "#ECEFF4",
            'num_bg': "#434C5E",
            'num_fg': "#E5E9F0",
            'num_hover': "#4C566A",
            'op_bg': "#5E81AC",
            'op_fg': "#E5E9F0",
            'op_hover': "#81A1C1",
            'special_bg': "#BF616A",
            'special_fg': "#ECEFF4",
            'special_hover': "#D08770",
            'equals_bg': "#A3BE8C",
            'equals_fg': "#2E3440",
            'equals_hover': "#B48EAD"
        }
        
        # Initialize calculator state
        self.current_input = ""
        self.total_expression = ""
        self.last_operation = None
        
        # Custom fonts
        self.display_font = font.Font(size=24, weight="bold")
        self.button_font = font.Font(size=16)
        
        # Setup UI
        self.setup_display()
        self.setup_buttons()
        
        # Bind keyboard events
        self.root.bind('<Key>', self.handle_key_press)
        
    def setup_display(self):
        """Create the display area showing input and results"""
        display_frame = tk.Frame(self.root, bg=self.colors['display_bg'], height=120)
        display_frame.pack(fill=tk.BOTH, padx=10, pady=(10, 5))
        
        # Total expression (smaller, top)
        self.total_label = tk.Label(
            display_frame, 
            text="", 
            anchor=tk.E,
            bg=self.colors['display_bg'],
            fg=self.colors['display_fg'],
            font=font.Font(size=14)
        )
        self.total_label.pack(expand=True, fill=tk.BOTH, padx=20)
        
        # Current input (larger, bottom)
        self.current_label = tk.Label(
            display_frame, 
            text="0", 
            anchor=tk.E,
            bg=self.colors['display_bg'],
            fg=self.colors['display_fg'],
            font=self.display_font
        )
        self.current_label.pack(expand=True, fill=tk.BOTH, padx=20)
    
    def setup_buttons(self):
        """Create and arrange all calculator buttons"""
        button_frame = tk.Frame(self.root, bg="#2E3440")
        button_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
        
        # Button layout
        buttons = [
    ('C', 0, 0, 'special'), ('(', 0, 1, 'special'), (')', 0, 2, 'special'), ('/', 0, 3, 'op'),
    ('7', 1, 0, 'num'), ('8', 1, 1, 'num'), ('9', 1, 2, 'num'), ('*', 1, 3, 'op'),
    ('4', 2, 0, 'num'), ('5', 2, 1, 'num'), ('6', 2, 2, 'num'), ('-', 2, 3, 'op'),
    ('1', 3, 0, 'num'), ('2', 3, 1, 'num'), ('3', 3, 2, 'num'), ('+', 3, 3, 'op'),
    ('00', 4, 0, 'num'), ('0', 4, 1, 'num'), ('.', 4, 2, 'num'), ('=', 4, 3, 'equals')
]

        
        # Create buttons
        for (text, row, col, btn_type) in buttons:
            # Determine colors based on button type
            bg = self.colors[f"{btn_type}_bg"]
            fg = self.colors[f"{btn_type}_fg"]
            active_bg = self.colors[f"{btn_type}_hover"]
            
            btn = tk.Button(
                button_frame,
                text=text,
                font=self.button_font,
                bg=bg,
                fg=fg,
                activebackground=active_bg,
                activeforeground=fg,
                relief=tk.FLAT,
                borderwidth=0,
                command=lambda t=text: self.handle_button_click(t)
            )
            
            # Add hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors[f"{btn_type}_hover"]))
            btn.bind("<Leave>", lambda e, b=btn, c=bg: b.config(bg=c))
            
            # Add click animation
            btn.bind("<Button-1>", lambda e: self.button_press_animation(e.widget))
            
            btn.grid(
                row=row, 
                column=col, 
                sticky=tk.NSEW, 
                padx=2, 
                pady=2,
                ipadx=10,
                ipady=15
            )
            
            # Configure grid weights
            button_frame.rowconfigure(row, weight=1)
            button_frame.columnconfigure(col, weight=1)
    
    def button_press_animation(self, button):
        """Create a pressed animation effect"""
        original_bg = button.cget("background")
        button.config(relief=tk.SUNKEN)
        self.root.update()
        button.after(100, lambda: button.config(relief=tk.FLAT))
    
    def handle_button_click(self, value):
        """Handle button click events"""
        if value == 'C':
            self.clear_all()
        elif value == '⌫':
            self.backspace()
        elif value == '=':
            self.calculate_result()
        elif value == '%':
            self.handle_percentage()
        elif value in '+-*/':
            self.handle_operator(value)
        elif value in '()':
            self.handle_bracket(value)
        else:
            self.handle_number(value)

    def handle_bracket(self, bracket):
        """Handle bracket input"""
        self.current_input += bracket
        self.update_display()

    
    def handle_key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        if key in '0123456789':
            self.handle_number(key)
        elif key in '+-*/':
            self.handle_operator(key)
        elif key in '()':
            self.handle_bracket(key)
        elif key == '\r':  # Enter
            self.calculate_result()
        elif key == '\x08':  # Backspace
            self.backspace()
        elif key == '\x1b':  # Escape
            self.clear_all()
        elif key == '%':
            self.handle_percentage()
        elif key == '.':
            self.handle_number('.')
    
    def handle_number(self, number):
        """Handle number input"""
        if self.current_input == "0" and number != "00":
            self.current_input = number
        elif number == "00":
            if self.current_input != "0":
                self.current_input += "00"
        else:
            self.current_input += number
        
        self.update_display()
    
    def handle_operator(self, operator):
        """Handle operator input"""
        if self.current_input:
            self.total_expression += self.current_input + operator
            self.current_input = ""
            self.update_display()
        elif self.total_expression and self.total_expression[-1] in '+-*/':
            # Replace last operator if current input is empty
            self.total_expression = self.total_expression[:-1] + operator
            self.update_display()
    
    def handle_percentage(self):
        """Handle percentage calculation"""
        if self.current_input:
            try:
                value = float(self.current_input) / 100
                self.current_input = str(value)
                self.update_display()
            except ValueError:
                self.show_error()
    
    def calculate_result(self):
        """Calculate and display the result"""
        if not self.current_input and not self.total_expression:
            return
        
        try:
            expression = self.total_expression + self.current_input
            result = eval(expression)
            
            self.total_expression = ""
            self.current_input = str(result)
            self.update_display()
        except:
            self.show_error()
    
    def backspace(self):
        """Remove the last character from current input"""
        if self.current_input:
            self.current_input = self.current_input[:-1]
            if not self.current_input:
                self.current_input = "0"
            self.update_display()
    
    def clear_all(self):
        """Reset the calculator"""
        self.current_input = "0"
        self.total_expression = ""
        self.update_display()
    
    def show_error(self):
        """Display error message"""
        self.current_input = "Error"
        self.total_expression = ""
        self.update_display()
        self.current_input = "0"
    
    def update_display(self):
        """Update the display labels"""
        self.current_label.config(text=self.current_input)
        self.total_label.config(text=self.total_expression)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = VibrantCalculator(root)
    root.mainloop()