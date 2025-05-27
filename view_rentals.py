import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class ViewRentalsWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.setup_window()
        self.create_styles()
        self.create_ui()
        self.load_rentals()

    def setup_window(self):
        self.root.title("عرض التأجيرات")
        self.root.geometry("1200x800")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2
        self.root.geometry(f"1200x800+{x}+{y}")
        self.colors = {
            'primary': '#6366F1',
            'primary_dark': '#4F46E5',
            'secondary': '#10B981',
            'background': '#0F172A',
            'surface': '#1E293B',
            'surface_dark': '#334155',
            'card': '#1E293B',
            'text': '#F8FAFC',
            'text_secondary': '#94A3B8',
            'danger': '#EF4444',
            'warning': '#F59E0B',
            'success': '#10B981',
            'info': '#3B82F6'
        }
        self.icons = {
            'car': '🚗',
            'calendar': '📅',
            'search': '🔍',
            'refresh': '🔄',
            'status': '🔄'
        }
        self.root.configure(bg=self.colors['background'])

    def create_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TEntry', fieldbackground='white', foreground='black', borderwidth=1)
        style.configure('Custom.Treeview', background='#F3F4F6', foreground='black', fieldbackground='#F3F4F6', borderwidth=1)
        style.configure(
            'Custom.Treeview.Heading',
            background='#6B7280',
            foreground='white',
            font=('Segoe UI', 12, 'bold'),
            relief='raised'
        )

    def create_ui(self):
        self.create_top_bar()
        self.container = tk.Frame(self.root, bg=self.colors['background'])
        self.container.pack(expand=True, fill='both', padx=40, pady=(0, 40))
        self.create_search_section()
        self.create_table_section()

    def create_top_bar(self):
        top_bar = tk.Frame(self.root, bg=self.colors['surface'])
        top_bar.pack(fill='x', pady=(0, 15))
        inner_top = tk.Frame(top_bar, bg=self.colors['surface'])
        inner_top.pack(fill='x', padx=30, pady=8)
        title_frame = tk.Frame(inner_top, bg=self.colors['surface'])
        title_frame.pack(side='left')
        tk.Label(
            title_frame,
            text=self.icons['car'],
            font=("Segoe UI", 20),
            fg=self.colors['primary'],
            bg=self.colors['surface']
        ).pack(side='left', padx=(0, 8))
        tk.Label(
            title_frame,
            text="عرض التأجيرات",
            font=("Segoe UI", 16, "bold"),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(side='left')

    def create_search_section(self):
        search_frame = tk.Frame(self.container, bg=self.colors['card'])
        search_frame.pack(fill='x', pady=(0, 20))
        inner = tk.Frame(search_frame, bg=self.colors['card'])
        inner.pack(padx=20, pady=15, fill='x')
        tk.Label(inner, text=f"{self.icons['search']} بحث", font=("Segoe UI", 13, "bold"), fg=self.colors['text'], bg=self.colors['card']).pack(side='left', padx=(0, 10))
        self.search_entry = ttk.Entry(inner, font=("Segoe UI", 12), style='Custom.TEntry', width=30)
        self.search_entry.pack(side='left')
        self.search_entry.bind('<KeyRelease>', self.filter_rentals)
        filter_frame = tk.Frame(inner, bg=self.colors['card'])
        filter_frame.pack(side='right')
        self.filter_buttons = {}
        for text, key in [("الكل", 'all'), ("قيد التأجير", 'active'), ("منتهية", 'completed'), ("ملغية", 'cancelled')]:
            btn = tk.Button(filter_frame, text=text, font=("Segoe UI", 12, "bold"), fg=self.colors['text'], bg=self.colors['primary'] if key=='all' else self.colors['surface'], activebackground=self.colors['primary'], bd=0, padx=20, pady=8, cursor='hand2', command=lambda k=key: self.apply_filter(k))
            btn.pack(side='left', padx=5)
            self.filter_buttons[key] = btn
        self.current_filter = 'all'

    def create_table_section(self):
        table_frame = tk.Frame(self.container, bg=self.colors['card'], highlightbackground=self.colors['primary'], highlightthickness=1)
        table_frame.pack(fill='both', expand=True)
        columns = ('rental_id', 'car_info', 'customer', 'start_date', 'end_date', 'status')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', style='Custom.Treeview', height=20, selectmode='browse')
        headings = {
            'rental_id': ('رقم التأجير', 100),
            'car_info': ('السيارة', 250),
            'customer': ('العميل', 200),
            'start_date': ('تاريخ البداية', 150),
            'end_date': ('تاريخ النهاية', 150),
            'status': ('الحالة', 150)
        }
        for col, (heading, width) in headings.items():
            self.tree.heading(col, text=heading, anchor='center')
            self.tree.column(col, width=width, anchor='center', stretch=False)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.tree.xview)
        h_scrollbar.pack(side='bottom', fill='x')
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        v_scrollbar.pack(side='right', fill='y')
        self.tree.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

    def apply_filter(self, filter_type):
        for k, btn in self.filter_buttons.items():
            btn.configure(bg=self.colors['primary'] if k == filter_type else self.colors['surface'])
        self.current_filter = filter_type
        self.filter_rentals()

    def filter_rentals(self, event=None):
        search_text = self.search_entry.get().strip().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = '''
                SELECT r.id, CONCAT(car.brand, ' ', car.model, ' - ', car.plate) as car_info,
                       c.name as customer, r.rent_date, r.return_date, r.status
                FROM rentals r
                JOIN customers c ON r.customer_id = c.id
                JOIN cars car ON r.car_id = car.id
                WHERE 1=1
            '''
            params = []
            if self.current_filter == 'active':
                query += " AND r.status = 'قيد التأجير'"
            elif self.current_filter == 'completed':
                query += " AND r.status = 'منتهية'"
            elif self.current_filter == 'cancelled':
                query += " AND r.status = 'ملغية'"
            if search_text:
                query += ''' AND (
                    c.name LIKE %s OR 
                    car.model LIKE %s OR 
                    car.plate LIKE %s OR 
                    car.brand LIKE %s OR
                    CAST(r.id AS CHAR) LIKE %s
                )'''
                search_pattern = f"%{search_text}%"
                params.extend([search_pattern] * 5)
            query += " ORDER BY r.rent_date DESC"
            cursor.execute(query, params)
            rentals = cursor.fetchall()
            for rental in rentals:
                self.tree.insert('', 'end', values=(
                    rental['id'],
                    rental['car_info'],
                    rental['customer'],
                    rental['rent_date'].strftime('%Y-%m-%d') if rental['rent_date'] else '',
                    rental['return_date'].strftime('%Y-%m-%d') if rental['return_date'] else '',
                    rental['status']
                ))
        except Exception as e:
            self.show_error("خطأ", f"حدث خطأ أثناء البحث: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def load_rentals(self):
        self.current_filter = 'all'
        self.filter_rentals()

    def get_db_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="car_rental"
        )

    def show_error(self, title, message):
        messagebox.showerror(title, message)

if __name__ == "__main__":
    root = tk.Tk()
    ViewRentalsWindow(root)
    root.mainloop()
