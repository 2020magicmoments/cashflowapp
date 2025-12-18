from datetime import datetime
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import TwoLineListItem
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.toast import toast
from kivy.utils import platform

# Import logic from other files
from database import db
from pdf_utils import create_pdf

# Set window size only if not on Android
if platform != 'android':
    Window.size = (360, 640)

# --- Screen Classes ---
class MenuScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.update_balance)

    def update_balance(self, dt):
        bal = db.get_balance()
        if 'balance_label' in self.ids:
            self.ids.balance_label.text = f"${bal:.2f}"
            
            # Always use Custom color mode so we can control it manually
            self.ids.balance_label.theme_text_color = "Custom"
            
            if bal < 0:
                # If negative, make it Light Red (readable on dark background)
                self.ids.balance_label.text_color = (1, 0.3, 0.3, 1)
            else:
                # If positive, FORCE WHITE
                self.ids.balance_label.text_color = (1, 1, 1, 1)

class AddScreen(Screen):
    pass

class ReportScreen(Screen):
    pass

# --- Main Application ---
class CashFlowApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray"  # <--- Change to Gray or BlueGray
        self.request_android_permissions()
        return Builder.load_file('layout.kv')

    def request_android_permissions(self):
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

    def get_today(self):
        return datetime.today().strftime('%Y-%m-%d')
    
    def get_first_of_month(self):
        return datetime.today().strftime('%Y-%m-01')

    def save_transaction(self, t_type):
        screen = self.root.get_screen('add')
        amount = screen.ids.amount.text
        category = screen.ids.category.text
        date = screen.ids.date_field.text

        if not amount or not date:
            toast("Please fill all fields")
            return 

        try:
            val_amount = float(amount)
        except ValueError:
            toast("Invalid Amount")
            return 

        db.add_transaction(t_type, val_amount, category, date)
        
        screen.ids.amount.text = ""
        screen.ids.category.text = ""
        toast("Saved!")
        self.root.current = 'menu'

    def generate_report(self):
        screen = self.root.get_screen('report')
        start = screen.ids.start_date.text
        end = screen.ids.end_date.text
        
        results = db.get_report(start, end)
        list_view = screen.ids.report_list
        list_view.clear_widgets()
        
        total_income = 0
        total_expense = 0

        for row in results:
            t_type, amount, category, date = row[1], row[2], row[3], row[4]
            
            if t_type == "Income":
                total_income += amount
            else:
                total_expense += amount

            item = TwoLineListItem(
                text=f"{category}: ${amount:.2f}",
                secondary_text=f"{date} | {t_type}",
            )
            list_view.add_widget(item)

        net = total_income - total_expense
        summary_item = TwoLineListItem(
            text=f"Total Net: ${net:.2f}",
            secondary_text=f"Income: ${total_income} | Expense: ${total_expense}",
            bg_color=(0.9, 0.9, 0.9, 1)
        )
        list_view.add_widget(summary_item)

    def generate_pdf_report(self):
        screen = self.root.get_screen('report')
        start = screen.ids.start_date.text
        end = screen.ids.end_date.text
        data = db.get_report(start, end)

        if not data:
            toast("No data to save")
            return

        # Call the utility function in pdf_utils.py
        saved_path = create_pdf(start, end, data)
        
        if saved_path:
            toast(f"Saved: {saved_path}")
        else:
            toast("Error generating PDF")

if __name__ == '__main__':
    CashFlowApp().run()