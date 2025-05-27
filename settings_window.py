import tkinter as tk
from tkinter import messagebox, filedialog
import mysql.connector
from tkinter import ttk
from password_change_window import PasswordChangeWindow
import os
import shutil
from datetime import datetime
import subprocess

class SettingsWindow:
    def __init__(self, root: tk.Tk):
        """Initialize the settings window."""
        self.root = root
        self.setup_window()
        self.create_ui()

    def setup_window(self):
        """Set up the main window properties."""
        self.root.title("الإعدادات")
        self.root.geometry("500x850")
        
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 850) // 2
        self.root.geometry(f"500x850+{x}+{y}")
        
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
            'settings': '⚙️',
            'database': '💾',
            'backup': '📦',
            'restore': '↩️',
            'password': '🔑',
            'account': '👤',
            'notification': '🔔',
            'rental': '🚗',
            'return': '↩️'
        }
        
        self.root.configure(bg=self.colors['background'])
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_ui(self):
        """Create the user interface elements."""
        # Create settings container
        container = tk.Frame(self.root, bg=self.colors['background'])
        container.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Settings title
        tk.Label(
            container,
            text=f"{self.icons['settings']} الإعدادات",
            font=("Segoe UI", 20, "bold"),
            fg=self.colors['text'],
            bg=self.colors['background']
        ).pack(pady=(0, 20))
        
        # Create settings sections
        sections = [
            ("إعدادات النظام", [
                (self.icons['database'], "تحديث قاعدة البيانات", "update_database", self.colors['info']),
                (self.icons['backup'], "النسخ الاحتياطي", "backup_database", self.colors['success']),
                (self.icons['restore'], "استعادة النسخة الاحتياطية", "restore_database", self.colors['warning'])
            ]),
            ("إعدادات الحساب", [
                (self.icons['password'], "تغيير كلمة المرور", "change_password", self.colors['primary']),
                (self.icons['account'], "تحديث معلومات الحساب", "update_account", self.colors['primary_light'])
            ]),
            ("إعدادات الإشعارات", [
                (self.icons['rental'], "إشعارات التأجير", "rental_notifications", self.colors['info']),
                (self.icons['return'], "إشعارات التسليم", "return_notifications", self.colors['warning'])
            ])
        ]
        
        for section_title, options in sections:
            # Section frame
            section_frame = tk.Frame(container, bg=self.colors['surface'])
            section_frame.pack(fill='x', pady=(0, 15))
            
            # Section title
            tk.Label(
                section_frame,
                text=section_title,
                font=("Segoe UI", 14, "bold"),
                fg=self.colors['text'],
                bg=self.colors['surface']
            ).pack(fill='x', padx=15, pady=10)
            
            # Options container with padding
            options_container = tk.Frame(section_frame, bg=self.colors['surface'])
            options_container.pack(fill='x', padx=15, pady=(0, 10))
            
            # Options
            for icon, option_text, command_name, color in options:
                # Create button with custom style
                btn = tk.Button(
                    options_container,
                    text=f"{icon} {option_text}",
                    font=("Segoe UI", 12),
                    fg=self.colors['text'],
                    bg=self.colors['surface_dark'],
                    activebackground=self.colors['hover'],
                    activeforeground=self.colors['text'],
                    bd=0,
                    padx=15,
                    pady=10,
                    cursor='hand2',
                    command=lambda cmd=command_name: self.execute_command(cmd),
                    anchor='e',
                    justify='right'
                )
                btn.pack(fill='x', pady=5)
                
                # Add hover effect
                def on_enter(e, button=btn):
                    button.configure(bg=self.colors['hover'])
                
                def on_leave(e, button=btn):
                    button.configure(bg=self.colors['surface_dark'])
                
                btn.bind('<Enter>', on_enter)
                btn.bind('<Leave>', on_leave)

    def execute_command(self, command_name):
        """Execute the appropriate command based on the command name."""
        commands = {
            'update_database': self.update_database,
            'backup_database': self.backup_database,
            'restore_database': self.restore_database,
            'change_password': self.change_password,
            'update_account': self.update_account,
            'rental_notifications': self.rental_notifications,
            'return_notifications': self.return_notifications
        }
        
        if command_name in commands:
            commands[command_name]()
        else:
            messagebox.showerror("خطأ", "الوظيفة غير موجودة")

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

    def update_database(self):
        """Update database structure."""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Create notification_settings table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS notification_settings (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        setting_name VARCHAR(50) UNIQUE NOT NULL,
                        enabled BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    )
                """)
                
                # Create users table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        email VARCHAR(100),
                        role VARCHAR(20) DEFAULT 'user',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    )
                """)
                
                # Add notes column to rentals table if it doesn't exist
                cursor.execute("""
                    ALTER TABLE rentals 
                    ADD COLUMN IF NOT EXISTS notes TEXT,
                    ADD COLUMN IF NOT EXISTS notification_sent BOOLEAN DEFAULT FALSE
                """)
                
                # Insert default notification settings if they don't exist
                default_settings = [
                    ('new_rental', True),
                    ('rental_expiry', True),
                    ('daily_report', True),
                    ('return_notification', True),
                    ('late_return', True),
                    ('daily_return_report', True)
                ]
                
                for setting_name, enabled in default_settings:
                    cursor.execute("""
                        INSERT IGNORE INTO notification_settings (setting_name, enabled)
                        VALUES (%s, %s)
                    """, (setting_name, enabled))
                
                # Insert default admin user if it doesn't exist
                cursor.execute("""
                    INSERT IGNORE INTO users (username, password, role)
                    VALUES ('admin', 'admin123', 'admin')
                """)
                
                conn.commit()
                messagebox.showinfo("تحديث قاعدة البيانات", "تم تحديث قاعدة البيانات بنجاح")
                
        except mysql.connector.Error as err:
            messagebox.showerror("خطأ", f"فشل تحديث قاعدة البيانات: {err}")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء تحديث قاعدة البيانات: {str(e)}")

    def backup_database(self):
        """Create database backup."""
        try:
            # Create backups directory if it doesn't exist
            backup_dir = "backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"car_rental_backup_{timestamp}.sql")
            
            # Create backup using mysqldump
            try:
                # Check if mysqldump is available
                if not shutil.which('mysqldump'):
                    messagebox.showerror("خطأ", "لم يتم العثور على mysqldump. يرجى التأكد من تثبيت MySQL")
                    return
                
                subprocess.run([
                    "mysqldump",
                    "-u", "root",
                    "--password=",
                    "car_rental",
                    f"--result-file={backup_file}"
                ], check=True)
                
                if os.path.exists(backup_file) and os.path.getsize(backup_file) > 0:
                    messagebox.showinfo("النسخ الاحتياطي", f"تم إنشاء نسخة احتياطية بنجاح\nتم حفظ النسخة في: {backup_file}")
                else:
                    messagebox.showerror("خطأ", "فشل إنشاء النسخة الاحتياطية: الملف فارغ أو غير موجود")
                    
            except subprocess.CalledProcessError as e:
                messagebox.showerror("خطأ", f"فشل إنشاء النسخة الاحتياطية: {str(e)}")
                
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء إنشاء النسخة الاحتياطية: {str(e)}")

    def restore_database(self):
        """Restore database from backup."""
        try:
            # Open file dialog to select backup file
            backup_file = filedialog.askopenfilename(
                title="اختر ملف النسخة الاحتياطية",
                filetypes=[("SQL files", "*.sql"), ("All files", "*.*")],
                initialdir="backups"
            )
            
            if not backup_file:
                return
            
            # Confirm restoration
            if not messagebox.askyesno("تأكيد", "هل أنت متأكد من استعادة النسخة الاحتياطية؟\nسيتم استبدال جميع البيانات الحالية."):
                return
            
            # Check if mysql is available
            if not shutil.which('mysql'):
                messagebox.showerror("خطأ", "لم يتم العثور على mysql. يرجى التأكد من تثبيت MySQL")
                return
            
            # Restore database using mysql command
            try:
                subprocess.run([
                    "mysql",
                    "-u", "root",
                    "--password=",
                    "car_rental",
                    f"--execute=source {backup_file}"
                ], check=True)
                
                messagebox.showinfo("استعادة النسخة الاحتياطية", "تم استعادة النسخة الاحتياطية بنجاح")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("خطأ", f"فشل استعادة النسخة الاحتياطية: {str(e)}")
                
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء استعادة النسخة الاحتياطية: {str(e)}")

    def change_password(self):
        """Change user password."""
        PasswordChangeWindow(self.root)

    def update_account(self):
        """Update account information."""
        try:
            # Create account update dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("تحديث معلومات الحساب")
            dialog.geometry("400x300")
            dialog.configure(bg=self.colors['background'])
            
            # Center dialog
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Get current user info
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT username, email FROM users WHERE id = 1")
                user_info = cursor.fetchone()
                
                if not user_info:
                    messagebox.showerror("خطأ", "لم يتم العثور على معلومات المستخدم")
                    return
            
            # Create form
            form_frame = tk.Frame(dialog, bg=self.colors['background'])
            form_frame.pack(expand=True, fill='both', padx=20, pady=20)
            
            # Username field
            tk.Label(
                form_frame,
                text="اسم المستخدم:",
                font=("Segoe UI", 12),
                fg=self.colors['text'],
                bg=self.colors['background']
            ).pack(fill='x', pady=(0, 5))
            
            username_entry = tk.Entry(
                form_frame,
                font=("Segoe UI", 12),
                bg=self.colors['surface'],
                fg=self.colors['text'],
                insertbackground=self.colors['text']
            )
            username_entry.pack(fill='x', pady=(0, 15))
            username_entry.insert(0, user_info[0])
            
            # Email field
            tk.Label(
                form_frame,
                text="البريد الإلكتروني:",
                font=("Segoe UI", 12),
                fg=self.colors['text'],
                bg=self.colors['background']
            ).pack(fill='x', pady=(0, 5))
            
            email_entry = tk.Entry(
                form_frame,
                font=("Segoe UI", 12),
                bg=self.colors['surface'],
                fg=self.colors['text'],
                insertbackground=self.colors['text']
            )
            email_entry.pack(fill='x', pady=(0, 15))
            email_entry.insert(0, user_info[1] or "")
            
            # Save button
            def save_changes():
                new_username = username_entry.get().strip()
                new_email = email_entry.get().strip()
                
                if not new_username:
                    messagebox.showerror("خطأ", "يرجى إدخال اسم المستخدم")
                    return
                
                try:
                    with self.get_db_connection() as conn:
                        cursor = conn.cursor()
                        
                        # Check if username is already taken
                        cursor.execute("SELECT id FROM users WHERE username = %s AND id != 1", (new_username,))
                        if cursor.fetchone():
                            messagebox.showerror("خطأ", "اسم المستخدم موجود مسبقاً")
                            return
                        
                        cursor.execute(
                            "UPDATE users SET username = %s, email = %s WHERE id = 1",
                            (new_username, new_email)
                        )
                        conn.commit()
                        messagebox.showinfo("نجاح", "تم تحديث معلومات الحساب بنجاح")
                        dialog.destroy()
                except Exception as e:
                    messagebox.showerror("خطأ", f"فشل تحديث معلومات الحساب: {str(e)}")
            
            tk.Button(
                form_frame,
                text="حفظ التغييرات",
                font=("Segoe UI", 12),
                fg=self.colors['text'],
                bg=self.colors['success'],
                activebackground=self.colors['hover'],
                activeforeground=self.colors['text'],
                bd=0,
                padx=20,
                pady=10,
                cursor='hand2',
                command=save_changes
            ).pack(fill='x', pady=(20, 0))
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء تحديث معلومات الحساب: {str(e)}")

    def rental_notifications(self):
        """Configure rental notifications."""
        try:
            # Create notifications dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("إعدادات إشعارات التأجير")
            dialog.geometry("400x300")
            dialog.configure(bg=self.colors['background'])
            
            # Center dialog
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Create form
            form_frame = tk.Frame(dialog, bg=self.colors['background'])
            form_frame.pack(expand=True, fill='both', padx=20, pady=20)
            
            # Get current settings
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT setting_name, enabled FROM notification_settings WHERE setting_name LIKE 'rental%'")
                current_settings = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Notification options
            options = [
                ("إشعارات التأجير الجديدة", "new_rental"),
                ("تذكير قبل انتهاء التأجير", "rental_expiry"),
                ("تقرير التأجيرات اليومي", "daily_report")
            ]
            
            # Create checkboxes
            vars = {}
            for text, var_name in options:
                var = tk.BooleanVar(value=current_settings.get(var_name, True))
                vars[var_name] = var
                
                tk.Checkbutton(
                    form_frame,
                    text=text,
                    font=("Segoe UI", 12),
                    fg=self.colors['text'],
                    bg=self.colors['background'],
                    selectcolor=self.colors['surface'],
                    activebackground=self.colors['background'],
                    activeforeground=self.colors['text'],
                    variable=var
                ).pack(fill='x', pady=5)
            
            # Save button
            def save_settings():
                try:
                    with self.get_db_connection() as conn:
                        cursor = conn.cursor()
                        
                        # Update notification settings
                        for var_name, var in vars.items():
                            cursor.execute("""
                                INSERT INTO notification_settings (setting_name, enabled) 
                                VALUES (%s, %s) 
                                ON DUPLICATE KEY UPDATE enabled = %s
                            """, (var_name, var.get(), var.get()))
                        
                        conn.commit()
                        messagebox.showinfo("نجاح", "تم حفظ إعدادات الإشعارات بنجاح")
                        dialog.destroy()
                except Exception as e:
                    messagebox.showerror("خطأ", f"فشل حفظ الإعدادات: {str(e)}")
            
            tk.Button(
                form_frame,
                text="حفظ الإعدادات",
                font=("Segoe UI", 12),
                fg=self.colors['text'],
                bg=self.colors['success'],
                activebackground=self.colors['hover'],
                activeforeground=self.colors['text'],
                bd=0,
                padx=20,
                pady=10,
                cursor='hand2',
                command=save_settings
            ).pack(fill='x', pady=(20, 0))
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء إعداد الإشعارات: {str(e)}")

    def return_notifications(self):
        """Configure return notifications."""
        try:
            # Create notifications dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("إعدادات إشعارات التسليم")
            dialog.geometry("400x300")
            dialog.configure(bg=self.colors['background'])
            
            # Center dialog
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Create form
            form_frame = tk.Frame(dialog, bg=self.colors['background'])
            form_frame.pack(expand=True, fill='both', padx=20, pady=20)
            
            # Get current settings
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT setting_name, enabled FROM notification_settings WHERE setting_name LIKE 'return%'")
                current_settings = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Notification options
            options = [
                ("إشعارات التسليم", "return_notification"),
                ("تذكير بالتأخير", "late_return"),
                ("تقرير التسليم اليومي", "daily_return_report")
            ]
            
            # Create checkboxes
            vars = {}
            for text, var_name in options:
                var = tk.BooleanVar(value=current_settings.get(var_name, True))
                vars[var_name] = var
                
                tk.Checkbutton(
                    form_frame,
                    text=text,
                    font=("Segoe UI", 12),
                    fg=self.colors['text'],
                    bg=self.colors['background'],
                    selectcolor=self.colors['surface'],
                    activebackground=self.colors['background'],
                    activeforeground=self.colors['text'],
                    variable=var
                ).pack(fill='x', pady=5)
            
            # Save button
            def save_settings():
                try:
                    with self.get_db_connection() as conn:
                        cursor = conn.cursor()
                        
                        # Update notification settings
                        for var_name, var in vars.items():
                            cursor.execute("""
                                INSERT INTO notification_settings (setting_name, enabled) 
                                VALUES (%s, %s) 
                                ON DUPLICATE KEY UPDATE enabled = %s
                            """, (var_name, var.get(), var.get()))
                        
                        conn.commit()
                        messagebox.showinfo("نجاح", "تم حفظ إعدادات الإشعارات بنجاح")
                        dialog.destroy()
                except Exception as e:
                    messagebox.showerror("خطأ", f"فشل حفظ الإعدادات: {str(e)}")
            
            tk.Button(
                form_frame,
                text="حفظ الإعدادات",
                font=("Segoe UI", 12),
                fg=self.colors['text'],
                bg=self.colors['success'],
                activebackground=self.colors['hover'],
                activeforeground=self.colors['text'],
                bd=0,
                padx=20,
                pady=10,
                cursor='hand2',
                command=save_settings
            ).pack(fill='x', pady=(20, 0))
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء إعداد الإشعارات: {str(e)}")

    def on_closing(self):
        """Handle window closing."""
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsWindow(root)
    root.mainloop() 