import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from main_window import MainWindow

class LoginWindow:
    def __init__(self, root: tk.Tk):
        """Initialize the login window with modern UI."""
        self.root = root
        self.setup_window()
        self.create_styles()
        self.create_ui()

    def setup_window(self):
        """Set up the main window properties."""
        self.root.title("تسجيل الدخول - نظام تأجير السيارات")
        self.root.geometry("550x850")  # Increased height to show all elements
        
        # Center the window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 550) // 2
        y = (screen_height - 850) // 2
        self.root.geometry(f"550x850+{x}+{y}")
        
        # Modern color scheme
        self.colors = {
            'primary': '#6366F1',        # Modern indigo
            'primary_dark': '#4F46E5',   # Darker indigo
            'secondary': '#10B981',      # Fresh emerald
            'background': '#0F172A',     # Deep navy
            'surface': '#1E293B',        # Slate
            'surface_dark': '#334155',   # Darker slate
            'text': '#F8FAFC',           # Bright white
            'text_secondary': '#94A3B8',  # Cool gray
            'danger': '#EF4444',         # Modern red
            'success': '#10B981',        # Emerald
        }

        # Modern icons
        self.icons = {
            'user': '👨‍💼',           # Professional person
            'password': '🔐',         # Locked with key
            'login': '⤵️',           # Return arrow
            'error': '❌',           # Red X
            'success': '✅',         # Green checkmark
            'car': '🚙',            # Modern car
            'system': '⚙️',         # Gear/settings
            'security': '🔒',        # Lock
            'exit': '🚪',           # Door
            'warning': '⚠️',        # Warning triangle
            'info': 'ℹ️',           # Information
            'key': '🗝️',            # Old key
            'new': '✨',            # Sparkles
            'time': '⌛',           # Hourglass
            'save': '💾',           # Save
            'delete': '🗑️',         # Delete
            'edit': '✏️',           # Pencil
            'view': '👁️',           # Eye
            'search': '🔍',         # Magnifying glass
            'calendar': '📅',       # Calendar
            'notification': '🔔',    # Bell
            'settings': '⚙️',       # Gear
            'profile': '👤',        # User silhouette
            'home': '🏠',           # House
            'menu': '☰',           # Hamburger menu
            'close': '✖️',          # Close X
            'back': '⬅️',           # Back arrow
            'forward': '➡️',        # Forward arrow
            'up': '⬆️',             # Up arrow
            'down': '⬇️',           # Down arrow
            'refresh': '🔄',        # Refresh
            'link': '🔗',           # Link
            'star': '⭐',           # Star
            'heart': '❤️',          # Heart
            'mail': '📧',           # Email
            'phone': '📱',          # Mobile phone
            'location': '📍',       # Location pin
            'chat': '💬',           # Chat bubble
            'money': '💰',          # Money bag
            'chart': '📊',          # Bar chart
            'folder': '📁',         # Folder
            'file': '📄',           # File
            'cloud': '☁️',          # Cloud
            'download': '⬇️',       # Download arrow
            'upload': '⬆️',         # Upload arrow
        }
        
        self.root.configure(bg=self.colors['background'])
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_styles(self):
        """Create and configure widget styles."""
        style = ttk.Style()
        
        # Entry style
        style.configure(
            'Custom.TEntry',
            fieldbackground='white',  # Changed to white background
            foreground='black',       # Changed to black text
            borderwidth=1
        )
        
        # Configure the entry text color globally
        self.root.option_add('*TEntry*foreground', 'black')

    def create_ui(self):
        """Create the user interface elements."""
        # Main container with padding
        self.container = tk.Frame(self.root, bg=self.colors['background'])
        self.container.pack(expand=True, fill='both', padx=45, pady=40)  # Balanced padding

        # Welcome message
        self.create_welcome_section()
        
        # Login form card
        self.create_login_form()

    def create_welcome_section(self):
        """Create welcome section with logo and title."""
        welcome_frame = tk.Frame(self.container, bg=self.colors['background'])
        welcome_frame.pack(fill='x', pady=(0, 25))  # Reduced bottom padding
        
        # Modern car logo with sparkles
        logo_frame = tk.Frame(welcome_frame, bg=self.colors['background'])
        logo_frame.pack(pady=(0, 20))  # Reduced padding
        
        # Left sparkle
        tk.Label(
            logo_frame,
            text=self.icons['new'],
            font=("Segoe UI", 26),  # Optimized size
            fg=self.colors['primary'],
            bg=self.colors['background']
        ).pack(side='left', padx=6)
        
        # Car icon
        tk.Label(
            logo_frame,
            text=self.icons['car'],
            font=("Segoe UI", 56),  # Optimized size
            fg=self.colors['primary'],
            bg=self.colors['background']
        ).pack(side='left')
        
        # Right sparkle
        tk.Label(
            logo_frame,
            text=self.icons['new'],
            font=("Segoe UI", 26),  # Optimized size
            fg=self.colors['primary'],
            bg=self.colors['background']
        ).pack(side='left', padx=6)

        # Title with gear icon
        tk.Label(
            welcome_frame,
            text=f"{self.icons['system']} نظام تأجير السيارات",
            font=("Segoe UI", 28, "bold"),  # Optimized size
            fg=self.colors['text'],
            bg=self.colors['background']
        ).pack(pady=(0, 10))
        
        # Subtitle with security icon
        tk.Label(
            welcome_frame,
            text=f"{self.icons['security']} قم بتسجيل الدخول للمتابعة",
            font=("Segoe UI", 15),  # Optimized size
            fg=self.colors['text_secondary'],
            bg=self.colors['background']
        ).pack()

    def create_login_form(self):
        """Create login form elements."""
        # Form container with card styling
        form_card = tk.Frame(
            self.container,
            bg=self.colors['surface'],
            highlightbackground=self.colors['primary'],
            highlightthickness=1
        )
        form_card.pack(fill='x', pady=(0, 15))  # Reduced bottom padding

        # Inner form padding
        form_inner = tk.Frame(form_card, bg=self.colors['surface'])
        form_inner.pack(fill='both', expand=True, padx=35, pady=30)  # Reduced padding

        # Username field
        self.create_input_field(
            form_inner,
            "اسم المستخدم",
            self.icons['user'],
            'username'
        )

        # Password field
        self.create_input_field(
            form_inner,
            "كلمة المرور",
            self.icons['password'],
            'password',
            show="●"
        )

        # Button container
        button_container = tk.Frame(form_inner, bg=self.colors['surface'])
        button_container.pack(fill='x', pady=(20, 0))  # Reduced top padding

        # Login button
        self.login_button = tk.Button(
            button_container,
            text=f"تسجيل الدخول {self.icons['login']}",
            font=("Segoe UI", 13),
            fg=self.colors['text'],
            bg=self.colors['primary'],
            activebackground=self.colors['primary_dark'],
            activeforeground=self.colors['text'],
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2',
            command=self.login
        )
        self.login_button.pack(fill='x', pady=(0, 10))  # Reduced padding

        # Exit button
        self.exit_button = tk.Button(
            button_container,
            text=f"{self.icons['exit']} خروج",
            font=("Segoe UI", 13),
            fg=self.colors['text_secondary'],
            bg=self.colors['surface'],
            activebackground=self.colors['surface_dark'],
            activeforeground=self.colors['text'],
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2',
            command=self.on_closing
        )
        self.exit_button.pack(fill='x')

    def create_input_field(self, parent, label: str, icon: str, field_name: str, show: str = None):
        """Create a form input field with icon and label."""
        # Field container
        field_container = tk.Frame(parent, bg=self.colors['surface'])
        field_container.pack(fill='x', pady=10)  # Reduced vertical spacing

        # Label with icon
        label_frame = tk.Frame(field_container, bg=self.colors['surface'])
        label_frame.pack(fill='x', pady=(0, 5))  # Reduced padding

        # Label container for better RTL alignment
        label_container = tk.Frame(label_frame, bg=self.colors['surface'])
        label_container.pack(side='right')

        tk.Label(
            label_container,
            text=icon,
            font=("Segoe UI", 18),  # Optimized size
            fg=self.colors['primary'],
            bg=self.colors['surface']
        ).pack(side='right', padx=(0, 6))

        tk.Label(
            label_container,
            text=label,
            font=("Segoe UI", 13),  # Optimized size
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(side='right')

        # Input field
        field = ttk.Entry(
            field_container,
            font=("Segoe UI", 13),  # Optimized size
            style='Custom.TEntry',
            justify='right'
        )
        if show:
            field.configure(show=show)
        field.pack(fill='x', ipady=8)  # Optimized padding
        
        # Store field reference
        setattr(self, f"{field_name}_field", field)

    def login(self):
        """Handle login attempt."""
        username = self.username_field.get().strip()
        password = self.password_field.get().strip()

        if not username or not password:
            self.show_error("خطأ", "الرجاء إدخال اسم المستخدم وكلمة المرور")
            return

        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Check user credentials
                cursor.execute("""
                    SELECT id, username, role FROM users 
                    WHERE username = %s AND password = %s
                """, (username, password))
                
                user = cursor.fetchone()
                
                if user:
                    self.show_success("تم تسجيل الدخول بنجاح")
                    self.root.withdraw()  # Hide login window
                    
                    # Open main window
                    main_root = tk.Toplevel()
                    main_app = MainWindow(main_root)
                    main_root.protocol("WM_DELETE_WINDOW", self.on_main_closing)
                    
                    # Store references for proper cleanup
                    self.main_root = main_root
                    self.main_app = main_app
                else:
                    self.show_error("خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة")

        except mysql.connector.Error as err:
            self.show_error("خطأ في قاعدة البيانات", f"فشل تسجيل الدخول: {err}")
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
        messagebox.showerror(f"{self.icons['error']} {title}", message)

    def show_success(self, message: str):
        """Show success message with icon."""
        messagebox.showinfo(f"{self.icons['success']} نجاح", message)

    def on_main_closing(self):
        """Handle main window closing."""
        self.main_root.destroy()
        self.root.destroy()

    def on_closing(self):
        """Handle login window closing."""
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
