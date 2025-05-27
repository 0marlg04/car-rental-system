import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

class PasswordChangeWindow:
    def __init__(self, parent):
        """Initialize the password change window."""
        self.parent = parent
        
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
            'info': '#3B82F6',           # Blue
            'hover': '#2D3B55'           # Hover color
        }

        # Modern icons
        self.icons = {
            'password': '🔑'
        }
        
        self.setup_window()
        self.create_ui()

    def setup_window(self):
        """Set up the main window properties."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("تغيير كلمة المرور")
        self.dialog.geometry("500x800")
        self.dialog.configure(bg=self.colors['background'])
        self.dialog.resizable(False, False)
        
        # Center the dialog
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 800) // 2
        self.dialog.geometry(f"500x800+{x}+{y}")

    def create_ui(self):
        """Create the user interface elements."""
        # Container with card-like appearance
        container = tk.Frame(
            self.dialog,
            bg=self.colors['surface'],
            highlightbackground=self.colors['primary'],
            highlightthickness=1
        )
        container.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Title with larger font and icon
        title_frame = tk.Frame(container, bg=self.colors['surface'])
        title_frame.pack(fill='x', pady=(30, 30))
        
        tk.Label(
            title_frame,
            text=self.icons['password'],
            font=("Segoe UI", 32),
            fg=self.colors['primary'],
            bg=self.colors['surface']
        ).pack()
        
        tk.Label(
            title_frame,
            text="تغيير كلمة المرور",
            font=("Segoe UI", 20, "bold"),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(pady=(10, 0))
        
        # Form container
        form_frame = tk.Frame(container, bg=self.colors['surface'])
        form_frame.pack(fill='x', padx=40, pady=(0, 30))
        
        # Current password
        tk.Label(
            form_frame,
            text="كلمة المرور الحالية",
            font=("Segoe UI", 12),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(anchor='e', pady=(0, 5))
        
        self.current_password = ttk.Entry(
            form_frame,
            font=("Segoe UI", 12),
            show="•",
            width=40
        )
        self.current_password.pack(fill='x', pady=(0, 20))
        
        # New password
        tk.Label(
            form_frame,
            text="كلمة المرور الجديدة",
            font=("Segoe UI", 12),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(anchor='e', pady=(0, 5))
        
        self.new_password = ttk.Entry(
            form_frame,
            font=("Segoe UI", 12),
            show="•",
            width=40
        )
        self.new_password.pack(fill='x', pady=(0, 20))
        
        # Confirm new password
        tk.Label(
            form_frame,
            text="تأكيد كلمة المرور الجديدة",
            font=("Segoe UI", 12),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(anchor='e', pady=(0, 5))
        
        self.confirm_password = ttk.Entry(
            form_frame,
            font=("Segoe UI", 12),
            show="•",
            width=40
        )
        self.confirm_password.pack(fill='x', pady=(0, 20))
        
        # Password requirements
        requirements_frame = tk.Frame(form_frame, bg=self.colors['surface_dark'])
        requirements_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            requirements_frame,
            text="متطلبات كلمة المرور:",
            font=("Segoe UI", 11, "bold"),
            fg=self.colors['text'],
            bg=self.colors['surface_dark']
        ).pack(anchor='e', padx=15, pady=(10, 5))
        
        requirements = [
            "• يجب أن تكون 8 أحرف على الأقل",
            "• يجب أن تحتوي على حرف كبير",
            "• يجب أن تحتوي على رقم",
            "• يجب أن تحتوي على رمز خاص"
        ]
        
        for req in requirements:
            tk.Label(
                requirements_frame,
                text=req,
                font=("Segoe UI", 10),
                fg=self.colors['text_secondary'],
                bg=self.colors['surface_dark']
            ).pack(anchor='e', padx=15, pady=2)
        
        # Buttons container
        button_frame = tk.Frame(container, bg=self.colors['surface'])
        button_frame.pack(fill='x', padx=40, pady=(0, 30))
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="إلغاء",
            font=("Segoe UI", 12),
            fg=self.colors['text'],
            bg=self.colors['surface_dark'],
            activebackground=self.colors['hover'],
            activeforeground=self.colors['text'],
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2',
            command=self.dialog.destroy
        )
        cancel_btn.pack(side='left', padx=5)
        
        # Save button
        save_btn = tk.Button(
            button_frame,
            text="حفظ",
            font=("Segoe UI", 12),
            fg=self.colors['text'],
            bg=self.colors['success'],
            activebackground=self.colors['hover'],
            activeforeground=self.colors['text'],
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2',
            command=self.save_password
        )
        save_btn.pack(side='right', padx=5)
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.parent.wait_window(self.dialog)

    def get_db_connection(self):
        """Get database connection."""
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="car_rental"
        )

    def save_password(self):
        """Save the new password."""
        current = self.current_password.get().strip()
        new = self.new_password.get().strip()
        confirm = self.confirm_password.get().strip()
        
        if not all([current, new, confirm]):
            messagebox.showerror("خطأ", "يرجى ملء جميع الحقول")
            return
        
        if new != confirm:
            messagebox.showerror("خطأ", "كلمة المرور الجديدة غير متطابقة")
            return
        
        # Password validation
        if len(new) < 8:
            messagebox.showerror("خطأ", "كلمة المرور يجب أن تكون 8 أحرف على الأقل")
            return
        
        if not any(c.isupper() for c in new):
            messagebox.showerror("خطأ", "كلمة المرور يجب أن تحتوي على حرف كبير")
            return
        
        if not any(c.isdigit() for c in new):
            messagebox.showerror("خطأ", "كلمة المرور يجب أن تحتوي على رقم")
            return
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in new):
            messagebox.showerror("خطأ", "كلمة المرور يجب أن تحتوي على رمز خاص")
            return
        
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Verify current password
                cursor.execute("SELECT password FROM users WHERE id = 1")
                stored_password = cursor.fetchone()
                
                if not stored_password or stored_password[0] != current:
                    messagebox.showerror("خطأ", "كلمة المرور الحالية غير صحيحة")
                    return
                
                # Update password
                cursor.execute("UPDATE users SET password = %s WHERE id = 1", (new,))
                conn.commit()
                
                messagebox.showinfo("نجاح", "تم تغيير كلمة المرور بنجاح")
                self.dialog.destroy()
                
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء تغيير كلمة المرور: {str(e)}") 