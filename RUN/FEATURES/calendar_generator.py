import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime

COLORS = {
    'header': '#4B8BBE',
    'weekdays': '#306998',
    'weekend': 'red',
    'current_day': '#77DD77',
    'month_title': '#333333',
    'bg': '#FFFFFF',
    'hover': '#F0F0F0'
}

class DynamicCalendarApp:
    def __init__(self, parent, year=None, month=None):
        self.parent = parent
        self.year = year
        self.month = month
        self.setup_ui()
        if year is not None:
            self.year_entry.insert(0, str(year))
        if month is not None:
            self.month_entry.insert(0, str(month))
        if year:
            self.generate_calendar()

    def setup_ui(self):
        self.input_frame = ttk.Frame(self.parent, padding="10 10 10 10")
        self.input_frame.pack(fill='x')

        ttk.Label(self.input_frame, text="Year:").grid(row=0, column=0, sticky='w')
        self.year_entry = ttk.Entry(self.input_frame, width=10)
        self.year_entry.grid(row=0, column=1, sticky='w')
        self.year_entry.bind('<Return>', lambda event: self.generate_calendar())

        ttk.Label(self.input_frame, text="Month (optional):").grid(row=1, column=0, sticky='w')
        self.month_entry = ttk.Entry(self.input_frame, width=10)
        self.month_entry.grid(row=1, column=1, sticky='w')
        self.month_entry.bind('<Return>', lambda event: self.generate_calendar())

        generate_btn = ttk.Button(
            self.input_frame,
            text="Generate Calendar",
            command=self.generate_calendar
        )
        generate_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill='both', expand=True)

    def generate_calendar(self):
        year_input = self.year_entry.get()
        month_input = self.month_entry.get()

        try:
            year = int(year_input)
            month = int(month_input) if month_input else None
            if month and (month < 1 or month > 12):
                raise ValueError("Month must be between 1-12")
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")
            return

        # Clear previous widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if month:
            self.show_month_calendar(year, month)
        else:
            self.show_year_calendar(year)

    def show_month_calendar(self, year, month):
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        today = datetime.now()

        title_label = tk.Label(
            self.main_frame,
            text=f"{month_name} {year}",
            font=('Arial', 14, 'bold'),
            bg=COLORS['header'],
            fg='white',
            pady=5
        )
        title_label.grid(row=0, column=0, columnspan=7, sticky='ew')

        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for col, day in enumerate(weekdays):
            bg_color = COLORS['weekdays'] if col < 5 else COLORS['weekend']
            tk.Label(
                self.main_frame,
                text=day,
                width=5,
                relief='flat',
                anchor='center',
                bg=bg_color,
                fg='white',
                font=('Arial', 9, 'bold')
            ).grid(row=1, column=col, sticky='nsew')

        for row_idx, week in enumerate(cal, start=2):
            for col_idx, day in enumerate(week):
                is_today = (year == today.year and month == today.month and day == today.day)
                bg_color = COLORS['bg']
                fg_color = 'black'
                text = str(day) if day != 0 else ''
                
                if day != 0:
                    if col_idx >= 5:
                        bg_color = COLORS['weekend']
                        fg_color = 'white'
                    if is_today:
                        bg_color = COLORS['current_day']
                
                tk.Label(
                    self.main_frame,
                    text=text,
                    width=5,
                    relief='groove',
                    anchor='e',
                    bg=bg_color,
                    fg=fg_color,
                    font=('Arial', 9)
                ).grid(row=row_idx, column=col_idx, sticky='nsew', padx=1, pady=1)

        for col in range(7):
            self.main_frame.columnconfigure(col, weight=1)

    def show_year_calendar(self, year):
        canvas = tk.Canvas(self.main_frame, bg=COLORS['bg'])
        scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        frame = tk.Frame(canvas, bg=COLORS['bg'])
        canvas.create_window((0, 0), window=frame, anchor='nw')
        frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        month_colors = ['#4B8BBE', '#306998', '#029359', '#77DD77', 
                       '#AEC6CF', '#836953', 'blue', '#B19CD9',
                       '#FFB347', '#C23B22', '#6A5ACD', '#008080']
        
        today = datetime.now()
        for month_num in range(1, 13):
            month_frame = tk.Frame(frame, relief='groove', borderwidth=1, bg=COLORS['bg'])
            row = (month_num - 1) // 4
            col = (month_num - 1) % 4
            month_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            self.add_month_content(year, month_num, month_frame, month_colors[month_num-1], today)

        for i in range(4):
            frame.columnconfigure(i, weight=1)
        for i in range(3):
            frame.rowconfigure(i, weight=1)
        
    def add_month_content(self, year, month, frame, title_color, today):
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]

        tk.Label(
            frame,
            text=f"{month_name} {year}",
            font=('Arial', 10, 'bold'),
            bg=title_color,
            fg='white',
            pady=2
        ).grid(row=0, column=0, columnspan=7, sticky='ew')

        weekdays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        for col, day in enumerate(weekdays):
            bg_color = COLORS['weekdays'] if col < 5 else COLORS['weekend']
            tk.Label(
                frame,
                text=day,
                width=3,
                relief='flat',
                anchor='center',
                bg=bg_color,
                fg='white',
                font=('Arial', 8, 'bold')
            ).grid(row=1, column=col)

        for row_idx, week in enumerate(cal, start=2):
            for col_idx, day in enumerate(week):
                is_today = (year == today.year and month == today.month and day == today.day)
                bg_color = COLORS['bg']
                fg_color = 'black'
                text = str(day) if day != 0 else ''
                
                if day != 0:
                    if col_idx >= 5:
                        bg_color = COLORS['weekend']
                        fg_color = 'white'
                    if is_today:
                        bg_color = COLORS['current_day']
                
                tk.Label(
                    frame,
                    text=text,
                    width=3,
                    relief='groove',
                    anchor='e',
                    bg=bg_color,
                    fg=fg_color,
                    font=('Arial', 8)
                ).grid(row=row_idx, column=col_idx, sticky='nsew', padx=1, pady=1)