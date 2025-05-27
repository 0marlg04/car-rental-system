import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from typing import Dict, Optional

class AddCustomerWindow:
    def __init__(self, root: tk.Tk):
        """Initialize the add customer window with modern UI."""
        self.root = root
        self.setup_window()
        self.create_styles()
        self.create_ui()

    def setup_window(self):
        """Set up the main window properties."""
        self.root.title("إضافة عميل")
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
            'customer': '👤',           # Customer icon
            'name': '📝',              # Name
            'id': '🆔',                # ID
            'phone': '📱',             # Phone
            'email': '📧',             # Email
            'address': '🏠',           # Address
            'license': '🚗',           # Driving License
            'check': '✓',              # Checkmark
            'cancel': '✕',             # Close
            'info': 'ℹ',              # Info
            'add': '+',                # Plus
            'save': '💾'               # Save
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
            borderwidth=1,
            relief='solid'
        )

        # Combobox style
        style.configure(
            'Custom.TCombobox',
            background=self.colors['surface_dark'],
            fieldbackground=self.colors['surface_dark'],
            foreground=self.colors['text'],
            arrowcolor=self.colors['primary'],
            borderwidth=1,
            relief='solid'
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

        # Customer icon
        tk.Label(
            title_frame,
            text=self.icons['customer'],
            font=("Segoe UI", 20),
            fg=self.colors['primary'],
            bg=self.colors['surface']
        ).pack(side='left', padx=(0, 8))

        # Title
        tk.Label(
            title_frame,
            text="إضافة عميل جديد",
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
            text="إضافة عميل جديد 👋",
            font=("Segoe UI", 18, "bold"),
            fg=self.colors['text'],
            bg=self.colors['surface'],
            justify='right',
            anchor='e'
        ).pack(fill='x', anchor='e')
        
        tk.Label(
            welcome_frame,
            text="قم بإدخال بيانات العميل الجديد",
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

        # Create form fields with increased spacing
        fields = [
            ("الاسم الكامل", "أدخل اسم العميل", 'name', 'entry'),
            ("رقم الهوية", "أدخل رقم الهوية", 'id', 'entry'),
            ("رقم الهاتف", "أدخل رقم الهاتف", 'phone', 'entry'),
            ("البريد الإلكتروني", "أدخل البريد الإلكتروني", 'email', 'entry'),
            ("العنوان", "أدخل العنوان", 'address', 'entry'),
            ("رخصة القيادة", "أدخل رقم رخصة القيادة", 'license', 'entry')
        ]

        # Create two columns for form fields
        left_column = tk.Frame(form_inner, bg=self.colors['surface_dark'])
        right_column = tk.Frame(form_inner, bg=self.colors['surface_dark'])
        
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 20))
        right_column.pack(side='right', fill='both', expand=True, padx=(20, 0))

        # Distribute fields between columns
        for i, field_data in enumerate(fields):
            if i < len(fields) // 2:
                parent = left_column
            else:
                parent = right_column
            
            label, placeholder, name, type_ = field_data
            self.create_input_field(parent, label, placeholder, name, type_)

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
            f"{self.icons['save']} حفظ العميل",
            self.colors['success'],
            self.add_customer
        )
        self.submit_button.pack(side='right', padx=5)

    def create_input_field(self, parent, label: str, placeholder: str, field_name: str, 
                         field_type: str, values: list = None):
        """Create a form input field with icon and label."""
        # Field container
        field_container = tk.Frame(parent, bg=self.colors['surface_dark'])
        field_container.pack(fill='x', pady=15)

        # Label with icon - Right aligned for Arabic
        label_frame = tk.Frame(field_container, bg=self.colors['surface_dark'])
        label_frame.pack(fill='x', pady=(0, 8))

        # Icon - Right of the label
        icon_label = tk.Label(
            label_frame,
            text=self.icons.get(field_name, self.icons['info']),
            font=("Segoe UI", 16),
            fg=self.colors['primary'],
            bg=self.colors['surface_dark']
        )
        icon_label.pack(side='right', padx=(0, 5))

        # Label text - Right aligned
        label_text = tk.Label(
            label_frame,
            text=label,
            font=("Segoe UI", 12),
            fg=self.colors['text'],
            bg=self.colors['surface_dark'],
            justify='right',
            anchor='e'
        )
        label_text.pack(side='right', fill='x', expand=True)

        # Input field
        if field_type == 'entry':
            field = tk.Entry(
                field_container,
                font=("Segoe UI", 11),
                fg=self.colors['text_secondary'],
                bg=self.colors['surface_dark'],
                bd=1,
                relief='solid',
                justify='right',
                insertbackground=self.colors['text']  # Cursor color
            )
            field.insert(0, placeholder)
            field.bind('<FocusIn>', lambda e: self.on_entry_click(e, placeholder))
            field.bind('<FocusOut>', lambda e: self.on_entry_leave(e, placeholder))
            field.bind('<Key>', lambda e: self.on_entry_key(e, placeholder))
        else:  # combobox
            field = ttk.Combobox(
                field_container,
                values=values,
                font=("Segoe UI", 11),
                style='Custom.TCombobox',
                state="readonly",
                justify='right'
            )
            field.set(placeholder)

        field.pack(fill='x', ipady=8)
        setattr(self, f"{field_name}_field", field)

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
        
        # Hover effects
        button.bind('<Enter>', lambda e: button.configure(bg=self.colors['primary_dark']))
        button.bind('<Leave>', lambda e: button.configure(bg=bg_color))
        
        return button

    def on_entry_click(self, event, placeholder):
        """Handle entry field focus in."""
        if event.widget.get() == placeholder:
            event.widget.delete(0, "end")
            event.widget.configure(fg=self.colors['text'])

    def on_entry_leave(self, event, placeholder):
        """Handle entry field focus out."""
        if event.widget.get() == '':
            event.widget.insert(0, placeholder)
            event.widget.configure(fg=self.colors['text_secondary'])

    def on_entry_key(self, event, placeholder):
        """Handle key press in entry field."""
        if event.widget.get() == placeholder:
            event.widget.delete(0, "end")
            event.widget.configure(fg=self.colors['text'])

    def add_customer(self):
        """Add a new customer to the database."""
        # Get values from fields
        name = self.name_field.get().strip()
        id_number = self.id_field.get().strip()
        phone = self.phone_field.get().strip()
        email = self.email_field.get().strip()
        address = self.address_field.get().strip()
        license_number = self.license_field.get().strip()

        # Validate inputs
        if not all([name, id_number, phone]):
            self.show_error("بيانات ناقصة", "يرجى ملء الحقول الإلزامية (الاسم، رقم الهوية، رقم الهاتف)")
            return

        try:
            # Connect to database
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Check if ID number already exists
                cursor.execute("SELECT id FROM customers WHERE national_id = %s", (id_number,))
                if cursor.fetchone():
                    self.show_error("خطأ", "رقم الهوية موجود مسبقاً")
                    return

                # Insert new customer
                cursor.execute("""
                    INSERT INTO customers (name, national_id, phone, email, address, license_number)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (name, id_number, phone, email, address, license_number))
                
                conn.commit()
                self.show_success("تمت إضافة العميل بنجاح")
                self.root.destroy()

        except mysql.connector.Error as err:
            self.show_error("خطأ في قاعدة البيانات", f"فشل إضافة العميل: {err}")
        except Exception as e:
            self.show_error("خطأ", f"حدث خطأ غير متوقع: {e}")

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
    app = AddCustomerWindow(root)
    root.mainloop()