import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class SearchWindow:
    def __init__(self, root: tk.Tk):
        """Initialize the search window."""
        self.root = root
        self.setup_window()
        self.create_ui()

    def setup_window(self):
        """Set up the main window properties."""
        self.root.title("بحث")
        self.root.geometry("600x400")
        
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 400) // 2
        self.root.geometry(f"600x400+{x}+{y}")
        
        # Modern color scheme
        self.colors = {
            'primary': '#4F46E5',        # Deep indigo
            'primary_light': '#818CF8',   # Light indigo
            'primary_dark': '#4338CA',    # Darker indigo
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
            'info': '#3B82F6'            # Blue
        }

        # Modern icons
        self.icons = {
            'search': '🔍',
            'car': '🚗',
            'customer': '👤',
            'rental': '📋'
        }
        
        self.root.configure(bg=self.colors['background'])
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_ui(self):
        """Create the user interface elements."""
        # Create search container
        container = tk.Frame(self.root, bg=self.colors['background'])
        container.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Search title
        tk.Label(
            container,
            text=f"{self.icons['search']} البحث",
            font=("Segoe UI", 20, "bold"),
            fg=self.colors['text'],
            bg=self.colors['background']
        ).pack(pady=(0, 20))
        
        # Search type selection
        search_type_frame = tk.Frame(container, bg=self.colors['background'])
        search_type_frame.pack(fill='x', pady=(0, 15))
        
        self.search_type = tk.StringVar(value="cars")
        
        types = [
            (self.icons['car'], "السيارات", "cars"),
            (self.icons['customer'], "العملاء", "customers"),
            (self.icons['rental'], "الإيجارات", "rentals")
        ]
        
        for icon, text, value in types:
            tk.Radiobutton(
                search_type_frame,
                text=f"{icon} {text}",
                value=value,
                variable=self.search_type,
                font=("Segoe UI", 12),
                fg=self.colors['text'],
                bg=self.colors['background'],
                selectcolor=self.colors['surface'],
                activebackground=self.colors['background'],
                activeforeground=self.colors['text']
            ).pack(side='left', padx=10)
        
        # Search input
        search_frame = tk.Frame(container, bg=self.colors['surface'])
        search_frame.pack(fill='x', pady=(0, 20))
        
        self.search_entry = ttk.Entry(
            search_frame,
            font=("Segoe UI", 12),
            style='Custom.TEntry'
        )
        self.search_entry.pack(side='left', fill='x', expand=True, padx=10, pady=10)
        
        # Search button
        search_btn = tk.Button(
            search_frame,
            text="بحث",
            font=("Segoe UI", 12),
            fg=self.colors['text'],
            bg=self.colors['primary'],
            activebackground=self.colors['primary_dark'],
            activeforeground=self.colors['text'],
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.perform_search
        )
        search_btn.pack(side='right', padx=10)
        
        # Results area
        results_frame = tk.Frame(container, bg=self.colors['surface'])
        results_frame.pack(fill='both', expand=True)
        
        # Create Treeview for results
        columns = ('id', 'name', 'details')
        self.results_tree = ttk.Treeview(
            results_frame,
            columns=columns,
            show='headings',
            style='Custom.Treeview'
        )
        
        # Configure columns
        self.results_tree.heading('id', text='الرقم')
        self.results_tree.heading('name', text='الاسم')
        self.results_tree.heading('details', text='التفاصيل')
        
        self.results_tree.column('id', width=50)
        self.results_tree.column('name', width=150)
        self.results_tree.column('details', width=300)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.results_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind enter key to search
        self.search_entry.bind('<Return>', lambda e: self.perform_search())

    def perform_search(self):
        """Perform search based on selected type and query."""
        try:
            search_type = self.search_type.get()
            query = self.search_entry.get().strip()
            
            if not query:
                messagebox.showwarning("تنبيه", "الرجاء إدخال نص للبحث")
                return
            
            # Clear previous results
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                if search_type == "cars":
                    cursor.execute("""
                        SELECT id, CONCAT(brand, ' ', model) as name, 
                               CONCAT('اللون: ', color, ' | السعر: ', price, ' درهم') as details
                        FROM cars
                        WHERE brand LIKE %s OR model LIKE %s OR plate LIKE %s
                    """, (f'%{query}%', f'%{query}%', f'%{query}%'))
                
                elif search_type == "customers":
                    cursor.execute("""
                        SELECT id, name, CONCAT('الهاتف: ', phone) as details
                        FROM customers
                        WHERE name LIKE %s OR phone LIKE %s
                    """, (f'%{query}%', f'%{query}%'))
                
                else:  # rentals
                    cursor.execute("""
                        SELECT r.id, 
                               CONCAT(c.name, ' - ', car.brand, ' ', car.model) as name,
                               CONCAT('من: ', DATE_FORMAT(r.rent_date, '%Y-%m-%d'), 
                                     ' | إلى: ', DATE_FORMAT(r.return_date, '%Y-%m-%d')) as details
                        FROM rentals r
                        JOIN customers c ON r.customer_id = c.id
                        JOIN cars car ON r.car_id = car.id
                        WHERE c.name LIKE %s OR car.brand LIKE %s OR car.model LIKE %s
                    """, (f'%{query}%', f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                
                if not results:
                    messagebox.showinfo("نتائج البحث", "لم يتم العثور على نتائج")
                    return
                
                # Insert results
                for result in results:
                    self.results_tree.insert('', 'end', values=result)
                
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء البحث: {str(e)}")

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

    def on_closing(self):
        """Handle window closing."""
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchWindow(root)
    root.mainloop() 