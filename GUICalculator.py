import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class CalculatorGUI:

    def __init__(self):
        self.answer = None
        buttons = [
            '1', '2', '3', '/',
            '4', '5', '6', '*',
            '7', '8', '9', '-',
            '.', '0', '+'
        ]
        # defining the window
        self.window = tk.Tk()
        self.window.geometry("500x200")

        # Styling buttons
        self.style = ttk.Style()
        self.style.configure("deletion.TButton", foreground="red", font=("Helvetica", 12, "bold"))

        # Defining entry field
        self.entry = tk.Entry(self.window, width=50)

        # Visualizing it in a grid
        self.entry.grid(column=0, row=0, columnspan=4)

        # First row is already occupied, thus we begin from the second row
        row, col = (1, 0)
        for element in buttons:
            tk.Button(self.window, text=element, command=lambda value=element: self.entry.insert(tk.END, value)).grid(
                column=col, row=row, sticky='news')
            col += 1
            # There are 4 columns, so we need to reset after 4 cycles
            if col == 4:
                row += 1
                col = 0

        tk.Button(self.window, text='=', command=self.eval_expression).grid(
            column=col, row=row, sticky='news')

        deletion_button = ttk.Button(self.window, text='DEL', command=lambda: self.entry.delete(0, tk.END), width=50, style= "deletion.TButton")
        deletion_button.grid(row=5, column=0, columnspan=4)
        self.window.mainloop()


    def eval_expression(self):
        """
        Evaluating the given expression
        """
        expression = self.entry.get()
        try:
            # expression is evaluated
            output = eval(expression)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, output)
            self.answer = output

        # If input is illegal, user gets warning message
        except:
            messagebox.showinfo(title="Input Error", message="wrong syntax!")

CalculatorGUI()
