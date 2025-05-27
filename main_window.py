import tkinter as tk
from tkinter import messagebox
from typing import List, Tuple, Callable, Dict
import sys
import mysql.connector
from tkinter import ttk

class MainWindow:
    def __init__(self, root: tk.Tk):
        """Initialize the main window with modern UI."""
        self.root = root
        self.setup_window()
        self.create_ui()

    def setup_window(self):
        """Set up the main window properties."""
        self.root.title("RentCars")
        self.root.geometry("1200x800")
        
        # Modern color scheme
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

        # Modern SVG-like icons using Unicode symbols
        self.icons = {
            'car': '🚗',           # Car icon
            'add_car': '🚙',       # Car with plus
            'customer': '👤',      # Person icon
            'rental': '📋',        # Clipboard
            'return': '↩️',        # Return arrow
            'reports': '📊',       # Chart
            'logout': '🔓',        # Power icon
            'stats': '📈',         # Stats icon
            'calendar': '📅',      # Calendar
            'time': '⏰',          # Clock
            'search': '🔍',        # Search
            'settings': '⚙️',      # Settings gear
            'help': '❔',          # Help icon
            'menu': '☰'           # Menu icon
        }
        
        self.root.configure(bg=self.colors['background'])
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_ui(self):
        """Create the user interface elements."""
        self.create_top_bar()
        
        # Main container
        container = tk.Frame(self.root, bg=self.colors['background'])
        container.pack(expand=True, fill='both', padx=40, pady=(0, 40))

        # Left sidebar (25% width)
        sidebar = self.create_sidebar(container)
        sidebar.pack(side='left', fill='y', padx=(0, 20))

        # Right content area (75% width)
        content = self.create_content_area(container)
        content.pack(side='right', fill='both', expand=True)

    def create_top_bar(self):
        """Create top navigation bar."""
        top_bar = tk.Frame(self.root, bg=self.colors['surface'])
        top_bar.pack(fill='x', pady=(0, 20))

        # Inner padding
        inner_top = tk.Frame(top_bar, bg=self.colors['surface'])
        inner_top.pack(fill='x', padx=40, pady=10)

        # Logo and title
        logo_frame = tk.Frame(inner_top, bg=self.colors['surface'])
        logo_frame.pack(side='left')

        tk.Label(
            logo_frame,
            text=self.icons['car'],
            font=("Segoe UI", 24),
            fg=self.colors['primary_light'],
            bg=self.colors['surface']
        ).pack(side='left', padx=(0, 10))

        tk.Label(
            logo_frame,
            text="RentCars",
            font=("Segoe UI", 18, "bold"),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(side='left')

        # Right-side actions
        actions_frame = tk.Frame(inner_top, bg=self.colors['surface'])
        actions_frame.pack(side='right')

        # Quick actions with better spacing and functionality
        quick_actions = [
            (self.icons['search'], "بحث", self.open_search),
            (self.icons['help'], "مساعدة", self.open_help),
            (self.icons['settings'], "إعدادات", self.open_settings)
        ]

        for icon, tooltip, command in quick_actions:
            action_frame = tk.Frame(actions_frame, bg=self.colors['surface'])
            action_frame.pack(side='left', padx=5)
            
            btn = tk.Label(
                action_frame,
                text=icon,
                font=("Segoe UI", 18),
                fg=self.colors['text_secondary'],
                bg=self.colors['surface'],
                cursor='hand2',
                padx=8,
                pady=4
            )
            btn.pack()
            
            # Add click event
            btn.bind('<Button-1>', lambda e, cmd=command: cmd())
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn: b.configure(fg=self.colors['primary_light']))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(fg=self.colors['text_secondary']))

    def create_sidebar(self, parent):
        """Create the sidebar with stats and quick actions."""
        sidebar = tk.Frame(parent, bg=self.colors['surface'], width=300)
        sidebar.pack_propagate(False)
        
        # Stats section
        stats_label = tk.Label(
            sidebar,
            text="نظرة عامة",
            font=("Segoe UI", 16, "bold"),
            fg=self.colors['text'],
            bg=self.colors['surface']
        )
        stats_label.pack(fill='x', pady=(20, 15), padx=20)

        # Stats cards with better icon display
        stats = [
            (self.icons['car'], "السيارات المتوفرة", "12", self.colors['info']),
            (self.icons['rental'], "الإيجارات النشطة", "8", self.colors['warning']),
            (self.icons['customer'], "العملاء", "45", self.colors['success'])
        ]

        for icon, label, value, color in stats:
            stat_card = tk.Frame(
                sidebar,
                bg=self.colors['surface_dark'],
                highlightbackground=color,
                highlightthickness=1
            )
            stat_card.pack(fill='x', padx=20, pady=5, ipady=10)

            # Icon with background and better sizing
            icon_frame = tk.Frame(stat_card, bg=color, width=45, height=45)
            icon_frame.pack(side='left', padx=15)
            icon_frame.pack_propagate(False)

            tk.Label(
                icon_frame,
                text=icon,
                font=("Segoe UI", 20),
                fg=self.colors['text'],
                bg=color
            ).place(relx=0.5, rely=0.5, anchor='center')

            # Text container
            text_frame = tk.Frame(stat_card, bg=self.colors['surface_dark'])
            text_frame.pack(side='left', fill='both', expand=True)

            tk.Label(
                text_frame,
                text=label,
                font=("Segoe UI", 11),
                fg=self.colors['text_secondary'],
                bg=self.colors['surface_dark']
            ).pack(anchor='w')

            tk.Label(
                text_frame,
                text=value,
                font=("Segoe UI", 16, "bold"),
                fg=self.colors['text'],
                bg=self.colors['surface_dark']
            ).pack(anchor='w')

        # Quick actions section
        actions_label = tk.Label(
            sidebar,
            text="وصول سريع",
            font=("Segoe UI", 16, "bold"),
            fg=self.colors['text'],
            bg=self.colors['surface']
        )
        actions_label.pack(fill='x', pady=(30, 15), padx=20)

        quick_actions = [
            (self.icons['calendar'], "حجوزات اليوم", self.colors['primary'], self.show_today_bookings),
            (self.icons['time'], "تأخر التسليم", self.colors['warning'], self.show_late_returns),
            (self.icons['stats'], "تقرير سريع", self.colors['info'], self.show_quick_report)
        ]

        for icon, label, color, command in quick_actions:
            action_btn = tk.Frame(
                sidebar,
                bg=self.colors['surface_dark'],
                cursor='hand2'
            )
            action_btn.pack(fill='x', padx=20, pady=5, ipady=8)

            tk.Label(
                action_btn,
                text=icon,
                font=("Segoe UI", 16),
                fg=color,
                bg=self.colors['surface_dark']
            ).pack(side='left', padx=15)

            tk.Label(
                action_btn,
                text=label,
                font=("Segoe UI", 11),
                fg=self.colors['text'],
                bg=self.colors['surface_dark']
            ).pack(side='left')

            # Add click event
            action_btn.bind('<Button-1>', lambda e, cmd=command: cmd())
            for widget in action_btn.winfo_children():
                widget.bind('<Button-1>', lambda e, cmd=command: cmd())

            # Hover effect
            action_btn.bind('<Enter>', lambda e, f=action_btn: self.on_quick_action_hover(f, True))
            action_btn.bind('<Leave>', lambda e, f=action_btn: self.on_quick_action_hover(f, False))

        return sidebar

    def create_content_area(self, parent):
        """Create the main content area with action cards."""
        content = tk.Frame(parent, bg=self.colors['background'])
        
        # Welcome section with emoji
        welcome_frame = tk.Frame(content, bg=self.colors['background'])
        welcome_frame.pack(fill='x', pady=(0, 30))
        
        tk.Label(
            welcome_frame,
            text="مرحباً بك 👋",
            font=("Segoe UI", 32, "bold"),
            fg=self.colors['text'],
            bg=self.colors['background']
        ).pack(anchor='w')
        
        tk.Label(
            welcome_frame,
            text="ماذا تريد أن تفعل اليوم؟",
            font=("Segoe UI", 16),
            fg=self.colors['text_secondary'],
            bg=self.colors['background']
        ).pack(anchor='w')

        # Action cards grid
        cards_frame = tk.Frame(content, bg=self.colors['background'])
        cards_frame.pack(fill='both', expand=True)
        
        # Configure grid
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(2, weight=1)

        # Main actions with updated icons
        actions = [
            {
                'icon': self.icons['add_car'],
                'title': 'إضافة سيارة',
                'description': 'إضافة سيارة جديدة للنظام',
                'color': self.colors['info'],
                'command': self.open_add_car
            },
            {
                'icon': self.icons['customer'],
                'title': 'إضافة عميل',
                'description': 'تسجيل عميل جديد',
                'color': self.colors['success'],
                'command': self.open_add_customer
            },
            {
                'icon': self.icons['rental'],
                'title': 'تأجير سيارة',
                'description': 'تسجيل عملية تأجير جديدة',
                'color': self.colors['primary'],
                'command': self.open_rent_car
            },
            {
                'icon': self.icons['return'],
                'title': 'إرجاع سيارة',
                'description': 'تسجيل عملية إرجاع سيارة',
                'color': self.colors['warning'],
                'command': self.open_return_car
            },
            {
                'icon': self.icons['reports'],
                'title': 'عرض الإيجارات',
                'description': 'عرض وإدارة الإيجارات',
                'color': self.colors['info'],
                'command': self.open_view_rentals
            },
            {
                'icon': self.icons['logout'],
                'title': 'تسجيل الخروج',
                'description': 'الخروج من النظام',
                'color': self.colors['danger'],
                'command': self.logout
            }
        ]

        for i, action in enumerate(actions):
            row = i // 3
            col = i % 3
            
            # Card container with glass effect
            card = tk.Frame(
                cards_frame,
                bg=self.colors['surface'],
                highlightbackground=action['color'],
                highlightthickness=1,
                bd=0
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # Icon container
            icon_frame = tk.Frame(
                card,
                bg=action['color'],
                width=50,
                height=50
            )
            icon_frame.pack(pady=(20, 15))
            icon_frame.pack_propagate(False)
            
            tk.Label(
                icon_frame,
                text=action['icon'],
                font=("Segoe UI", 20),
                fg=self.colors['text'],
                bg=action['color']
            ).place(relx=0.5, rely=0.5, anchor='center')

            # Title with larger font
            tk.Label(
                card,
                text=action['title'],
                font=("Segoe UI", 14, "bold"),
                fg=self.colors['text'],
                bg=self.colors['surface']
            ).pack(pady=(0, 5))

            # Description
            tk.Label(
                card,
                text=action['description'],
                font=("Segoe UI", 11),
                fg=self.colors['text_secondary'],
                bg=self.colors['surface']
            ).pack(pady=(0, 20))

            # Make card clickable
            for widget in card.winfo_children():
                widget.bind('<Button-1>', lambda e, cmd=action['command']: cmd())
            card.bind('<Button-1>', lambda e, cmd=action['command']: cmd())
            
            # Hover effects
            self.add_hover_effect(card, action['color'])

        return content

    def add_hover_effect(self, card, color):
        """Add hover effect to card."""
        def on_enter(e):
            card.configure(bg=self.colors['hover'])
            for widget in card.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=self.colors['hover'])

        def on_leave(e):
            card.configure(bg=self.colors['surface'])
            for widget in card.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=self.colors['surface'])

        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
        for widget in card.winfo_children():
            if not isinstance(widget, tk.Frame):  # Don't change icon background
                widget.bind('<Enter>', on_enter)
                widget.bind('<Leave>', on_leave)
            widget.configure(cursor='hand2')
        card.configure(cursor='hand2')

    def on_quick_action_hover(self, frame, is_hover: bool):
        """Handle quick action hover effect."""
        bg_color = self.colors['hover'] if is_hover else self.colors['surface_dark']
        frame.configure(bg=bg_color)
        for widget in frame.winfo_children():
            widget.configure(bg=bg_color)

    def open_window(self, window_class: str, module_name: str):
        """Generic method to open a new window."""
        try:
            module = __import__(module_name)
            window_class = getattr(module, window_class)
            new_window = tk.Toplevel(self.root)
            window_class(new_window)
        except ImportError:
            messagebox.showerror("خطأ", f"الملف {module_name}.py غير موجود!")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء فتح النافذة: {str(e)}")

    def open_add_car(self):
        """Open the add car window."""
        self.open_window("AddCarWindow", "add_car")

    def open_add_customer(self):
        """Open the add customer window."""
        self.open_window("AddCustomerWindow", "add_customer")

    def open_rent_car(self):
        """Open the rent car window."""
        self.open_window("RentCarWindow", "rent_car")

    def open_return_car(self):
        """Open the return car window."""
        self.open_window("ReturnCarWindow", "return_car")

    def open_view_rentals(self):
        """Open the view rentals window."""
        self.open_window("ViewRentalsWindow", "view_rentals")

    def logout(self):
        """Handle logout action."""
        if messagebox.askyesno("تأكيد", "هل أنت متأكد من تسجيل الخروج؟"):
            self.root.destroy()
            import login
            root = tk.Tk()
            login.LoginWindow(root)
            root.mainloop()

    def on_closing(self):
        """Handle window closing."""
        if messagebox.askyesno("تأكيد", "هل أنت متأكد من الخروج من البرنامج؟"):
            self.root.destroy()
            sys.exit()

    def open_search(self):
        """Open search window."""
        try:
            new_window = tk.Toplevel(self.root)
            from search_window import SearchWindow
            SearchWindow(new_window)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء فتح نافذة البحث: {str(e)}")

    def open_help(self):
        """Open help window."""
        help_text = """
        دليل استخدام النظام:
        
        1. إضافة سيارة: لإضافة سيارة جديدة للنظام
        2. إضافة عميل: لتسجيل عميل جديد
        3. تأجير سيارة: لتسجيل عملية تأجير جديدة
        4. إرجاع سيارة: لتسجيل عملية إرجاع سيارة
        5. عرض الإيجارات: لعرض وإدارة جميع الإيجارات
        
        للمساعدة الإضافية، يرجى التواصل مع الدعم الفني
        """
        messagebox.showinfo("مساعدة", help_text)

    def open_settings(self):
        """Open settings window."""
        try:
            new_window = tk.Toplevel(self.root)
            from settings_window import SettingsWindow
            SettingsWindow(new_window)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء فتح الإعدادات: {str(e)}")

    def show_today_bookings(self):
        """Show today's bookings."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        r.id,
                        CONCAT(c.brand, ' ', c.model) as car,
                        cu.name as customer,
                        DATE_FORMAT(r.rent_date, '%H:%i') as time
                    FROM rentals r
                    JOIN cars c ON r.car_id = c.id
                    JOIN customers cu ON r.customer_id = cu.id
                    WHERE DATE(r.rent_date) = CURDATE()
                    ORDER BY r.rent_date
                """)
                bookings = cursor.fetchall()
                
                if not bookings:
                    messagebox.showinfo("حجوزات اليوم", "لا توجد حجوزات لهذا اليوم")
                    return
                
                # Format bookings into a message
                message = "حجوزات اليوم:\n\n"
                for booking in bookings:
                    message += f"• {booking[1]} - {booking[2]} ({booking[3]})\n"
                
                messagebox.showinfo("حجوزات اليوم", message)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء جلب الحجوزات: {str(e)}")

    def show_late_returns(self):
        """Show late returns."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        r.id,
                        CONCAT(c.brand, ' ', c.model) as car,
                        cu.name as customer,
                        DATEDIFF(CURDATE(), r.return_date) as days_late
                    FROM rentals r
                    JOIN cars c ON r.car_id = c.id
                    JOIN customers cu ON r.customer_id = cu.id
                    WHERE r.returned_date IS NULL 
                    AND r.return_date < CURDATE()
                    ORDER BY r.return_date
                """)
                late_returns = cursor.fetchall()
                
                if not late_returns:
                    messagebox.showinfo("تأخر التسليم", "لا توجد سيارات متأخرة في التسليم")
                    return
                
                # Format late returns into a message
                message = "السيارات المتأخرة في التسليم:\n\n"
                for late in late_returns:
                    message += f"• {late[1]} - {late[2]} (متأخر {late[3]} يوم)\n"
                
                messagebox.showinfo("تأخر التسليم", message)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء جلب البيانات: {str(e)}")

    def show_quick_report(self):
        """Show quick report."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Get total revenue
                cursor.execute("""
                    SELECT COALESCE(SUM(c.price * DATEDIFF(r.return_date, r.rent_date)), 0) as total_revenue
                    FROM rentals r
                    JOIN cars c ON r.car_id = c.id
                    WHERE MONTH(r.rent_date) = MONTH(CURDATE())
                    AND YEAR(r.rent_date) = YEAR(CURDATE())
                """)
                revenue = cursor.fetchone()[0]
                
                # Get active rentals
                cursor.execute("""
                    SELECT COUNT(*) as active_rentals
                    FROM rentals
                    WHERE returned_date IS NULL
                """)
                active_rentals = cursor.fetchone()[0]
                
                # Get available cars
                cursor.execute("""
                    SELECT COUNT(*) as available_cars
                    FROM cars
                    WHERE available = TRUE
                """)
                available_cars = cursor.fetchone()[0]
                
                # Format report
                message = f"""
                تقرير سريع:
                
                الإيرادات الشهرية: {revenue:.2f} درهم
                الإيجارات النشطة: {active_rentals}
                السيارات المتوفرة: {available_cars}
                """
                
                messagebox.showinfo("تقرير سريع", message)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء إنشاء التقرير: {str(e)}")

    def get_db_connection(self):
        """Get database connection."""
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="car_rental"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("خطأ في الاتصال", "فشل الاتصال بقاعدة البيانات")
            raise

    def create_styles(self):
        style = ttk.Style()
        style.configure('Custom.TEntry', fieldbackground='white', foreground='black', borderwidth=1)
        style.configure('Custom.Treeview', background='#F3F4F6', foreground='black', fieldbackground='#F3F4F6', borderwidth=1)
        style.configure(
            'Custom.Treeview.Heading',
            background='#1E293B',  # Much darker for strong contrast
            foreground='white',
            font=('Segoe UI', 14, 'bold')
        )

if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()
