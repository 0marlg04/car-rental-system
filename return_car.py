import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import sys
from typing import Dict, Optional
from tkcalendar import DateEntry

class ReturnCarWindow:
    def __init__(self, root: tk.Tk):
        """Initialize the return car window with modern UI."""
        self.root = root
        self.setup_window()
        self.create_styles()
        self.create_ui()
        self.load_active_rentals()

    def setup_window(self):
        """Set up the main window properties."""
        self.root.title("إرجاع سيارة")
        self.root.geometry("800x700")
        
        # Modern color scheme (matching main window)
        self.colors = {
            'primary': '#4F46E5',        # Deep indigo
            'primary_light': '#818CF8',   # Light indigo
            'secondary': '#059669',       # Fresh emerald
            'background': '#0F172A',      # Deep navy
            'surface': '#1E293B',         # Slate
            'surface_dark': '#334155',    # Darker slate
            'card': '#1E293B',           # Card background
            'text': '#F8FAFC',           # Bright white
            'text_secondary': '#94A3B8',  # Cool gray
            'danger': '#EF4444',         # Modern red
            'warning': '#F59E0B',        # Amber
            'success': '#10B981',        # Emerald
            'info': '#3B82F6',           # Blue
            'hover': '#2D3B55'           # Hover color
        }

        # Modern icons - Using standard Unicode symbols
        self.icons = {
            'return': '⮌',            # Return icon
            'calendar': '📅',         # Calendar
            'car': '🚗',             # Car
            'customer': '👤',         # Customer
            'check': '✓',            # Success check
            'cancel': '✕',           # Cancel
            'search': '🔍',          # Search
            'info': 'ℹ',            # Info
            'arrow': '➜',           # Arrow
            'time': '⏰',            # Time
            'edit': '✎',            # Edit
            'delete': '⌫',          # Delete
            'save': '💾',            # Save
            'warning': '⚠',         # Warning
            'error': '⮿',           # Error
            'success': '✔',         # Success checkmark
            'plus': '+',            # Plus sign
            'minus': '−',           # Minus sign
            'menu': '☰',            # Menu
            'settings': '⚙',        # Settings
            'help': '?',            # Help
            'close': '×'            # Close
        }
        
        self.root.configure(bg=self.colors['background'])
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_styles(self):
        """Create and configure widget styles."""
        style = ttk.Style()
        
        # Combobox style
        style.configure(
            'Custom.TCombobox',
            background=self.colors['surface'],
            fieldbackground=self.colors['surface'],
            foreground=self.colors['text'],
            arrowcolor=self.colors['primary_light'],
            borderwidth=0
        )

        # Entry style for calendar
        style.configure(
            'Custom.TEntry',
            fieldbackground=self.colors['surface'],
            foreground=self.colors['text'],
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

        self.create_form_elements()
        self.create_buttons()

    def create_top_bar(self):
        """Create the top bar with title and icon."""
        top_bar = tk.Frame(self.root, bg=self.colors['surface'])
        top_bar.pack(fill='x', pady=(0, 20))

        # Inner padding
        inner_top = tk.Frame(top_bar, bg=self.colors['surface'])
        inner_top.pack(fill='x', padx=40, pady=10)

        # Icon and title container
        title_frame = tk.Frame(inner_top, bg=self.colors['surface'])
        title_frame.pack(side='left')

        # Return icon
        tk.Label(
            title_frame,
            text=self.icons['return'],
            font=("Segoe UI", 24),
            fg=self.colors['primary_light'],
            bg=self.colors['surface']
        ).pack(side='left', padx=(0, 10))

        # Title
        tk.Label(
            title_frame,
            text="إرجاع سيارة",
            font=("Segoe UI", 20, "bold"),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(side='left')

    def create_form_elements(self):
        """Create form input elements."""
        # Rental selection section
        rental_section = self.create_section(
            "اختيار السيارة المؤجرة",
            "حدد السيارة المراد إرجاعها من القائمة"
        )

        # Search-like combobox container
        combo_container = tk.Frame(rental_section, bg=self.colors['surface_dark'])
        combo_container.pack(fill='x', pady=(5, 0))

        # Search icon
        tk.Label(
            combo_container,
            text=self.icons['search'],
            font=("Segoe UI", 14),
            fg=self.colors['text_secondary'],
            bg=self.colors['surface_dark']
        ).pack(side='left', padx=10, pady=8)

        # Rental combobox with modern styling
        self.rental_cb = ttk.Combobox(
            combo_container,
            state="readonly",
            font=("Segoe UI", 12),
            style='Custom.TCombobox'
        )
        self.rental_cb.pack(fill='x', padx=(0, 10), pady=8)

        # Date selection section
        date_section = self.create_section(
            "تاريخ الإرجاع",
            "حدد تاريخ إرجاع السيارة"
        )

        # Calendar icon and date picker container
        date_container = tk.Frame(date_section, bg=self.colors['surface_dark'])
        date_container.pack(fill='x', pady=(5, 0))

        # Calendar icon
        tk.Label(
            date_container,
            text=self.icons['calendar'],
            font=("Segoe UI", 14),
            fg=self.colors['text_secondary'],
            bg=self.colors['surface_dark']
        ).pack(side='left', padx=10, pady=8)

        # Date entry with modern styling
        self.return_date_entry = DateEntry(
            date_container,
            width=15,
            background=self.colors['primary'],
            foreground=self.colors['text'],
            borderwidth=0,
            font=("Segoe UI", 12),
            date_pattern='yyyy-mm-dd',
            selectbackground=self.colors['primary_light']
        )
        self.return_date_entry.pack(side='left', padx=(0, 10), pady=8)

    def create_section(self, title: str, description: str) -> tk.Frame:
        """Create a form section with title and description."""
        section = tk.Frame(self.inner_frame, bg=self.colors['surface'])
        section.pack(fill='x', pady=(0, 20))

        # Title with icon
        tk.Label(
            section,
            text=title,
            font=("Segoe UI", 14, "bold"),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(anchor='w')

        # Description
        tk.Label(
            section,
            text=description,
            font=("Segoe UI", 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['surface']
        ).pack(anchor='w', pady=(2, 10))

        return section

    def create_buttons(self):
        """Create action buttons."""
        button_frame = tk.Frame(self.inner_frame, bg=self.colors['surface'])
        button_frame.pack(fill='x', pady=(20, 0))

        # Cancel button
        self.cancel_button = self.create_button(
            button_frame,
            f"{self.icons['cancel']} إلغاء",
            self.colors['surface_dark'],
            self.on_cancel
        )
        self.cancel_button.pack(side='left')

        # Submit button
        self.submit_button = self.create_button(
            button_frame,
            f"{self.icons['check']} تأكيد الإرجاع",
            self.colors['success'],
            self.return_car
        )
        self.submit_button.pack(side='right')

    def create_button(self, parent, text: str, bg_color: str, command) -> tk.Button:
        """Create a styled button."""
        button = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 12),
            fg=self.colors['text'],
            bg=bg_color,
            activebackground=self.colors['hover'],
            activeforeground=self.colors['text'],
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=command
        )
        
        # Hover effects
        button.bind('<Enter>', lambda e: button.configure(bg=self.colors['hover']))
        button.bind('<Leave>', lambda e: button.configure(bg=bg_color))
        
        return button

    def load_active_rentals(self):
        """Load active rentals from the database."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT r.id, c.brand, c.model, cu.name 
                    FROM rentals r
                    JOIN cars c ON r.car_id = c.id
                    JOIN customers cu ON r.customer_id = cu.id
                    WHERE r.returned_date IS NULL OR r.returned_date = ''
                """)
                rentals = cursor.fetchall()

                self.rentals_dict = {}
                display_values = []
                for rental in rentals:
                    rental_id, brand, model, customer_name = rental
                    display_text = f"#{rental_id} - {brand} {model} - {customer_name}"
                    display_values.append(display_text)
                    self.rentals_dict[display_text] = rental_id

                self.rental_cb['values'] = display_values

        except mysql.connector.Error as err:
            self.show_error("خطأ في قاعدة البيانات", f"فشل تحميل بيانات الإيجارات: {err}")
        except Exception as e:
            self.show_error("خطأ", f"حدث خطأ غير متوقع: {e}")

    def return_car(self):
        """Process the car return."""
        if not self.validate_inputs():
            return

        try:
            selected_rental = self.rental_cb.get()
            return_date = datetime.strptime(self.return_date_entry.get(), "%Y-%m-%d").date()
            rental_id = self.rentals_dict.get(selected_rental)

            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Update rental record
                cursor.execute("""
                    UPDATE rentals 
                    SET returned_date = %s 
                    WHERE id = %s
                """, (return_date, rental_id))

                # Update car status
                cursor.execute("""
                    UPDATE cars 
                    SET available = TRUE, status = 'متوفرة' 
                    WHERE id = (SELECT car_id FROM rentals WHERE id = %s)
                """, (rental_id,))

                conn.commit()
                
                self.show_success("تم إرجاع السيارة بنجاح")
                self.root.destroy()

        except mysql.connector.Error as err:
            self.show_error("خطأ في قاعدة البيانات", f"فشل عملية الإرجاع: {err}")
        except Exception as e:
            self.show_error("خطأ", f"حدث خطأ غير متوقع: {e}")

    def validate_inputs(self) -> bool:
        """Validate form inputs."""
        selected_rental = self.rental_cb.get()
        return_date_str = self.return_date_entry.get()

        if not selected_rental:
            self.show_error("خطأ في الإدخال", "يرجى اختيار رقم الإيجار")
            return False

        if not return_date_str:
            self.show_error("خطأ في الإدخال", "يرجى إدخال تاريخ الإرجاع")
            return False

        try:
            datetime.strptime(return_date_str, "%Y-%m-%d")
        except ValueError:
            self.show_error("خطأ في التاريخ", "تنسيق التاريخ غير صحيح. يرجى استخدام yyyy-mm-dd")
            return False

        return True

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
