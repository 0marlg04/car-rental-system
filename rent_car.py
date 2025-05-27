import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from typing import Dict, Optional
from tkcalendar import Calendar

class RentCarWindow:
    def __init__(self, root: tk.Tk):
        """Initialize the rent car window with modern UI."""
        self.root = root
        self.setup_window()
        self.create_styles()
        self.create_ui()
        self.load_data()

    def setup_window(self):
        """Set up the main window properties."""
        self.root.title("تأجير سيارة")
        self.root.geometry("1200x800")
        
        # Center the window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Modern color scheme
        self.colors = {
            'primary': '#6366F1',        # Modern indigo
            'primary_dark': '#4F46E5',   # Darker indigo
            'secondary': '#10B981',      # Fresh emerald
            'background': '#0F172A',     # Deep navy
            'surface': '#1E293B',        # Slate
            'surface_dark': '#334155',   # Darker slate
            'card': '#1E293B',           # Card background
            'text': '#F8FAFC',           # Bright white
            'text_secondary': '#94A3B8',  # Cool gray
            'danger': '#EF4444',         # Modern red
            'warning': '#F59E0B',        # Amber
            'success': '#10B981',        # Emerald
            'info': '#3B82F6'            # Blue
        }

        # Modern icons
        self.icons = {
            'rent': '🔑',              # Key
            'customer': '👤',          # Customer
            'car': '🚗',              # Car
            'calendar': '📅',          # Calendar
            'money': '💰',            # Money
            'duration': '⏱️',          # Duration
            'start': '▶️',            # Start
            'end': '⏹️',              # End
            'check': '✓',             # Checkmark
            'cancel': '✕',            # Close
            'info': 'ℹ',             # Info
            'save': '💾'              # Save
        }
        
        self.root.configure(bg=self.colors['background'])
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_styles(self):
        """Create and configure widget styles."""
        style = ttk.Style()
        
        # Entry style
        style.configure(
            'Custom.TEntry',
            fieldbackground=self.colors['surface_dark'],
            foreground=self.colors['text'],
            borderwidth=0
        )

        # Combobox style
        style.configure(
            'Custom.TCombobox',
            background=self.colors['surface_dark'],
            fieldbackground=self.colors['surface_dark'],
            foreground=self.colors['text'],
            arrowcolor=self.colors['primary'],
            borderwidth=0
        )

    def create_ui(self):
        """Create the user interface elements."""
        # Top bar
        self.create_top_bar()
        
        # Main container with padding
        self.container = tk.Frame(self.root, bg=self.colors['background'])
        self.container.pack(expand=True, fill='both', padx=40, pady=(0, 40))

        # Content card
        self.content_frame = tk.Frame(
            self.container,
            bg=self.colors['surface'],
            highlightbackground=self.colors['primary'],
            highlightthickness=1
        )
        self.content_frame.pack(fill='both', expand=True)

        # Inner padding
        self.inner_frame = tk.Frame(self.content_frame, bg=self.colors['surface'])
        self.inner_frame.pack(fill='both', expand=True, padx=30, pady=30)

        # Welcome message
        self.create_welcome_section()
        
        # Form elements in a card layout
        self.create_form_card()

    def create_top_bar(self):
        """Create the top bar with title and icon."""
        top_bar = tk.Frame(self.root, bg=self.colors['surface'])
        top_bar.pack(fill='x', pady=(0, 15))

        # Inner padding
        inner_top = tk.Frame(top_bar, bg=self.colors['surface'])
        inner_top.pack(fill='x', padx=30, pady=8)

        # Icon and title container
        title_frame = tk.Frame(inner_top, bg=self.colors['surface'])
        title_frame.pack(side='left')

        # Rent icon
        tk.Label(
            title_frame,
            text=self.icons['rent'],
            font=("Segoe UI", 20),
            fg=self.colors['primary'],
            bg=self.colors['surface']
        ).pack(side='left', padx=(0, 8))

        # Title
        tk.Label(
            title_frame,
            text="تأجير سيارة",
            font=("Segoe UI", 16, "bold"),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(side='left')

    def create_welcome_section(self):
        """Create welcome section with description."""
        welcome_frame = tk.Frame(self.inner_frame, bg=self.colors['surface'])
        welcome_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            welcome_frame,
            text="تأجير سيارة جديدة 🚗",
            font=("Segoe UI", 18, "bold"),
            fg=self.colors['text'],
            bg=self.colors['surface'],
            justify='right',
            anchor='e'
        ).pack(fill='x', anchor='e')
        
        tk.Label(
            welcome_frame,
            text="قم باختيار العميل والسيارة وتفاصيل التأجير",
            font=("Segoe UI", 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['surface'],
            justify='right',
            anchor='e'
        ).pack(fill='x', anchor='e')

    def create_form_card(self):
        """Create form elements in a card layout."""
        # Form container with card styling
        form_card = tk.Frame(
            self.inner_frame,
            bg=self.colors['surface_dark'],
            highlightbackground=self.colors['primary'],
            highlightthickness=1
        )
        form_card.pack(fill='both', expand=True, pady=(0, 20))

        # Inner form padding
        form_inner = tk.Frame(form_card, bg=self.colors['surface_dark'])
        form_inner.pack(fill='both', expand=True, padx=40, pady=30)

        # Create three sections
        customer_section = tk.LabelFrame(
            form_inner,
            text=" معلومات العميل ",
            font=("Segoe UI", 11, "bold"),
            fg=self.colors['text'],
            bg=self.colors['surface_dark']
        )
        customer_section.pack(fill='x', pady=(0, 20))

        car_section = tk.LabelFrame(
            form_inner,
            text=" معلومات السيارة ",
            font=("Segoe UI", 11, "bold"),
            fg=self.colors['text'],
            bg=self.colors['surface_dark']
        )
        car_section.pack(fill='x', pady=(0, 20))

        rental_section = tk.LabelFrame(
            form_inner,
            text=" تفاصيل التأجير ",
            font=("Segoe UI", 11, "bold"),
            fg=self.colors['text'],
            bg=self.colors['surface_dark']
        )
        rental_section.pack(fill='x')

        # Create fields for each section
        self.create_customer_fields(customer_section)
        self.create_car_fields(car_section)
        self.create_rental_fields(rental_section)

        # Buttons container
        button_container = tk.Frame(self.inner_frame, bg=self.colors['surface'])
        button_container.pack(fill='x', pady=(20, 0))

        # Cancel button
        self.cancel_button = self.create_button(
            button_container,
            f"{self.icons['cancel']} إلغاء",
            self.colors['surface_dark'],
            self.on_cancel
        )
        self.cancel_button.pack(side='left', padx=5)

        # Submit button
        self.submit_button = self.create_button(
            button_container,
            f"{self.icons['save']} تأكيد التأجير",
            self.colors['success'],
            self.rent_car
        )
        self.submit_button.pack(side='right', padx=5)

    def create_customer_fields(self, parent):
        """Create customer selection fields."""
        frame = tk.Frame(parent, bg=self.colors['surface_dark'])
        frame.pack(fill='x', padx=20, pady=15)

        # Customer selection
        label_frame = tk.Frame(frame, bg=self.colors['surface_dark'])
        label_frame.pack(fill='x', pady=(0, 8))

        tk.Label(
            label_frame,
            text=self.icons['customer'],
            font=("Segoe UI", 16),
            fg=self.colors['primary'],
            bg=self.colors['surface_dark']
        ).pack(side='right', padx=(0, 5))

        tk.Label(
            label_frame,
            text="اختر العميل",
            font=("Segoe UI", 12),
            fg=self.colors['text'],
            bg=self.colors['surface_dark']
        ).pack(side='right')

        self.customer_combobox = ttk.Combobox(
            frame,
            font=("Segoe UI", 11),
            style='Custom.TCombobox',
            state='readonly',
            justify='right'
        )
        self.customer_combobox.pack(fill='x', ipady=8)
        self.customer_combobox.bind('<<ComboboxSelected>>', self.on_customer_selected)

    def create_car_fields(self, parent):
        """Create car selection fields."""
        frame = tk.Frame(parent, bg=self.colors['surface_dark'])
        frame.pack(fill='x', padx=20, pady=15)

        # Car selection
        label_frame = tk.Frame(frame, bg=self.colors['surface_dark'])
        label_frame.pack(fill='x', pady=(0, 8))

        tk.Label(
            label_frame,
            text=self.icons['car'],
            font=("Segoe UI", 16),
            fg=self.colors['primary'],
            bg=self.colors['surface_dark']
        ).pack(side='right', padx=(0, 5))

        tk.Label(
            label_frame,
            text="اختر السيارة",
            font=("Segoe UI", 12),
            fg=self.colors['text'],
            bg=self.colors['surface_dark']
        ).pack(side='right')

        self.car_combobox = ttk.Combobox(
            frame,
            font=("Segoe UI", 11),
            style='Custom.TCombobox',
            state='readonly',
            justify='right'
        )
        self.car_combobox.pack(fill='x', ipady=8)
        self.car_combobox.bind('<<ComboboxSelected>>', self.on_car_selected)

        # Car details (will be updated when car is selected)
        self.car_details_frame = tk.Frame(frame, bg=self.colors['surface_dark'])
        self.car_details_frame.pack(fill='x', pady=(15, 0))

    def create_rental_fields(self, parent):
        """Create rental details fields."""
        frame = tk.Frame(parent, bg=self.colors['surface_dark'])
        frame.pack(fill='x', padx=20, pady=15)

        # Create two columns
        left_column = tk.Frame(frame, bg=self.colors['surface_dark'])
        right_column = tk.Frame(frame, bg=self.colors['surface_dark'])
        
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        right_column.pack(side='right', fill='both', expand=True, padx=(10, 0))

        # Start date
        self.create_date_field(
            right_column,
            "تاريخ البداية",
            self.icons['start'],
            'start_date'
        )

        # End date
        self.create_date_field(
            left_column,
            "تاريخ النهاية",
            self.icons['end'],
            'end_date'
        )

        # Total cost frame
        total_frame = tk.Frame(frame, bg=self.colors['surface_dark'])
        total_frame.pack(fill='x', pady=(15, 0))

        tk.Label(
            total_frame,
            text=f"{self.icons['money']} التكلفة الإجمالية:",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors['text'],
            bg=self.colors['surface_dark']
        ).pack(side='right')

        self.total_cost_label = tk.Label(
            total_frame,
            text="0 درهم",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors['success'],
            bg=self.colors['surface_dark']
        )
        self.total_cost_label.pack(side='right', padx=(10, 0))

    def create_date_field(self, parent, label: str, icon: str, name: str):
        """Create a date field with label and icon."""
        label_frame = tk.Frame(parent, bg=self.colors['surface_dark'])
        label_frame.pack(fill='x', pady=(0, 8))

        tk.Label(
            label_frame,
            text=icon,
            font=("Segoe UI", 16),
            fg=self.colors['primary'],
            bg=self.colors['surface_dark']
        ).pack(side='right', padx=(0, 5))

        tk.Label(
            label_frame,
            text=label,
            font=("Segoe UI", 12),
            fg=self.colors['text'],
            bg=self.colors['surface_dark']
        ).pack(side='right')

        # Create a frame for the date selection
        date_frame = tk.Frame(parent, bg=self.colors['surface_dark'])
        date_frame.pack(fill='x', pady=(0, 5))

        # Create a button to show calendar
        date_button = tk.Button(
            date_frame,
            text=datetime.now().strftime('%Y-%m-%d'),
            font=("Segoe UI", 11),
            fg=self.colors['text'],
            bg=self.colors['surface'],
            bd=1,
            relief='solid',
            cursor='hand2',
            command=lambda: self.show_calendar(name)
        )
        date_button.pack(fill='x', ipady=8)

        # Store the button and initial date
        setattr(self, f"{name}_button", date_button)
        setattr(self, f"{name}_date", datetime.now().date())

    def show_calendar(self, name: str):
        """Show calendar popup for date selection."""
        try:
            # Create a new toplevel window
            calendar_window = tk.Toplevel(self.root)
            calendar_window.title("اختر التاريخ")
            calendar_window.geometry("300x300")
            calendar_window.configure(bg=self.colors['surface'])

            # Create calendar widget
            cal = Calendar(
                calendar_window,
                selectmode='day',
                year=datetime.now().year,
                month=datetime.now().month,
                day=datetime.now().day,
                background=self.colors['surface'],
                foreground=self.colors['text'],
                selectbackground=self.colors['primary'],
                normalbackground=self.colors['surface_dark'],
                normalforeground=self.colors['text'],
                weekendbackground=self.colors['surface_dark'],
                weekendforeground=self.colors['text'],
                othermonthbackground=self.colors['surface'],
                othermonthforeground=self.colors['text_secondary']
            )
            cal.pack(padx=10, pady=10, fill='both', expand=True)

            # Add OK button
            ok_button = tk.Button(
                calendar_window,
                text="موافق",
                font=("Segoe UI", 10),
                fg=self.colors['text'],
                bg=self.colors['primary'],
                bd=0,
                padx=15,
                pady=5,
                cursor='hand2',
                command=lambda: self.on_date_selected(name, cal.get_date(), calendar_window)
            )
            ok_button.pack(pady=10)

            # Center the window
            calendar_window.update_idletasks()
            width = calendar_window.winfo_width()
            height = calendar_window.winfo_height()
            x = (calendar_window.winfo_screenwidth() // 2) - (width // 2)
            y = (calendar_window.winfo_screenheight() // 2) - (height // 2)
            calendar_window.geometry(f'{width}x{height}+{x}+{y}')

            # Make window modal
            calendar_window.transient(self.root)
            calendar_window.grab_set()
            self.root.wait_window(calendar_window)

        except Exception as e:
            self.show_error("خطأ", f"حدث خطأ في فتح التقويم: {str(e)}")

    def on_date_selected(self, name: str, selected_date: datetime.date, window: tk.Toplevel):
        """Handle date selection."""
        try:
            # Update the button text
            button = getattr(self, f"{name}_button")
            button.configure(text=selected_date.strftime('%Y-%m-%d'))
            
            # Store the selected date
            setattr(self, f"{name}_date", selected_date)
            
            # Close the calendar window
            window.destroy()
            
            # Calculate total
            self.calculate_total(None)
            
        except Exception as e:
            self.show_error("خطأ", f"حدث خطأ في اختيار التاريخ: {str(e)}")

    def create_button(self, parent, text: str, bg_color: str, command) -> tk.Button:
        """Create a styled button."""
        button = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 10),
            fg=self.colors['text'],
            bg=bg_color,
            activebackground=self.colors['primary_dark'],
            activeforeground=self.colors['text'],
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2',
            command=command
        )
        
        button.bind('<Enter>', lambda e: button.configure(bg=self.colors['primary_dark']))
        button.bind('<Leave>', lambda e: button.configure(bg=bg_color))
        
        return button

    def load_data(self):
        """Load customers and cars data from database."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Load customers
                cursor.execute("SELECT id, name, national_id FROM customers")
                customers = cursor.fetchall()
                self.customers = {f"{name} - {id_number}": id for id, name, id_number in customers}
                self.customer_combobox['values'] = list(self.customers.keys())

                # Load available cars
                cursor.execute("""
                    SELECT id, brand, model, plate, price 
                    FROM cars 
                    WHERE available = TRUE
                """)
                cars = cursor.fetchall()
                self.cars = {f"{brand} {model} - {plate}": (id, rate) 
                           for id, brand, model, plate, rate in cars}
                self.car_combobox['values'] = list(self.cars.keys())

        except mysql.connector.Error as err:
            self.show_error("خطأ في قاعدة البيانات", f"فشل تحميل البيانات: {err}")

    def on_customer_selected(self, event):
        """Handle customer selection."""
        self.selected_customer = self.customers.get(self.customer_combobox.get())

    def on_car_selected(self, event):
        """Handle car selection and update car details."""
        selected = self.car_combobox.get()
        if selected in self.cars:
            car_id, daily_rate = self.cars[selected]
            self.selected_car = car_id
            self.daily_rate = daily_rate
            
            # Update car details
            for widget in self.car_details_frame.winfo_children():
                widget.destroy()

            tk.Label(
                self.car_details_frame,
                text=f"{self.icons['money']} السعر اليومي: {daily_rate} درهم",
                font=("Segoe UI", 11),
                fg=self.colors['text'],
                bg=self.colors['surface_dark']
            ).pack(side='right', padx=5)

            self.calculate_total(None)

    def calculate_total(self, event):
        """Calculate total rental cost."""
        try:
            if hasattr(self, 'daily_rate'):
                start_date = getattr(self, 'start_date_date')
                end_date = getattr(self, 'end_date_date')
                
                if start_date and end_date:
                    # Convert dates to datetime objects for proper comparison
                    start_datetime = datetime.combine(start_date, datetime.min.time())
                    end_datetime = datetime.combine(end_date, datetime.min.time())
                    
                    # Validate dates
                    if end_datetime < start_datetime:
                        self.show_error("خطأ", "تاريخ النهاية يجب أن يكون بعد تاريخ البداية")
                        self.total_cost_label.config(text="0 درهم")
                        return
                    
                    # Calculate days difference
                    days = (end_datetime - start_datetime).days + 1
                    
                    # Validate minimum rental period
                    if days < 1:
                        self.show_error("خطأ", "مدة التأجير يجب أن تكون يوم واحد على الأقل")
                        self.total_cost_label.config(text="0 درهم")
                        return
                    
                    # Calculate total cost
                    total = days * self.daily_rate
                    self.total_cost_label.config(text=f"{total:.2f} درهم")
                    self.rental_days = days
                    self.total_cost = total
            
        except AttributeError:
            pass  # Ignore if not all fields are set yet
        except Exception as e:
            self.show_error("خطأ", f"حدث خطأ في حساب التكلفة: {str(e)}")
            self.total_cost_label.config(text="0 درهم")

    def rent_car(self):
        """Process the car rental."""
        if not hasattr(self, 'selected_customer') or not self.selected_customer:
            self.show_error("خطأ", "الرجاء اختيار العميل")
            return

        if not hasattr(self, 'selected_car') or not self.selected_car:
            self.show_error("خطأ", "الرجاء اختيار السيارة")
            return

        try:
            # Get and validate dates
            start_date = self.start_date_date
            end_date = self.end_date_date
            
            # Convert to datetime for proper comparison
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.min.time())
            
            if end_datetime < start_datetime:
                self.show_error("خطأ", "تاريخ النهاية يجب أن يكون بعد تاريخ البداية")
                return
            
            # Calculate days and validate
            days = (end_datetime - start_datetime).days + 1
            if days < 1:
                self.show_error("خطأ", "مدة التأجير يجب أن تكون يوم واحد على الأقل")
                return
            
            # Calculate total cost
            total_cost = days * self.daily_rate
            
            # Connect to database
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Check if car is still available
                cursor.execute("SELECT available FROM cars WHERE id = %s", (self.selected_car,))
                result = cursor.fetchone()
                if not result or not result[0]:
                    self.show_error("خطأ", "عذراً، السيارة غير متوفرة حالياً")
                    return
                
                # Insert rental record
                cursor.execute("""
                    INSERT INTO rentals (customer_id, car_id, rent_date, return_date, total_price)
                    VALUES (%s, %s, %s, %s, %s)
                """, (self.selected_customer, self.selected_car, start_date, end_date, total_cost))
                
                # Update car availability
                cursor.execute("""
                    UPDATE cars 
                    SET available = FALSE 
                    WHERE id = %s
                """, (self.selected_car,))
                
                conn.commit()
                self.show_success("تم تأجير السيارة بنجاح")
                self.root.destroy()
                
        except mysql.connector.Error as err:
            self.show_error("خطأ في قاعدة البيانات", f"فشل تأجير السيارة: {err}")
        except Exception as e:
            self.show_error("خطأ", f"حدث خطأ غير متوقع: {str(e)}")

    def get_db_connection(self) -> mysql.connector.MySQLConnection:
        """Get database connection."""
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="car_rental"
            )
        except mysql.connector.Error as err:
            self.show_error("خطأ في الاتصال", "فشل الاتصال بقاعدة البيانات")
            raise

    def show_error(self, title: str, message: str):
        """Show error message with icon."""
        messagebox.showerror(f"{self.icons['cancel']} {title}", message)

    def show_success(self, message: str):
        """Show success message with icon."""
        messagebox.showinfo(f"{self.icons['check']} نجاح", message)

    def on_cancel(self):
        """Handle cancel button click."""
        if messagebox.askyesno(f"{self.icons['info']} تأكيد", "هل أنت متأكد من إلغاء العملية؟"):
            self.root.destroy()

    def on_closing(self):
        """Handle window closing."""
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RentCarWindow(root)
    root.mainloop()