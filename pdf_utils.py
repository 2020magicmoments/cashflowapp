from fpdf import FPDF
from kivy.utils import platform
import os

def create_pdf(start_date, end_date, data):
    """
    Generates a PDF and returns the path where it was saved, 
    or raises an Exception if it fails.
    """
    if not data:
        return None

    # 1. Create PDF Object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # 2. Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"Cash Flow Report", ln=1, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"From {start_date} to {end_date}", ln=1, align="C")
    pdf.ln(10)

    # 3. Table Header
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, "Date", 1)
    pdf.cell(60, 10, "Category", 1)
    pdf.cell(40, 10, "Type", 1)
    pdf.cell(40, 10, "Amount", 1)
    pdf.ln()

    # 4. Table Body
    pdf.set_font("Arial", size=12)
    total_income = 0
    total_expense = 0

    for row in data:
        # row: id, type, amount, category, date
        t_type = row[1]
        amount = row[2]
        category = row[3]
        date = row[4]

        if t_type == "Income":
            total_income += amount
        else:
            total_expense += amount

        pdf.cell(40, 10, str(date), 1)
        pdf.cell(60, 10, str(category), 1)
        pdf.cell(40, 10, str(t_type), 1)
        pdf.cell(40, 10, f"${amount:.2f}", 1)
        pdf.ln()

    pdf.ln(10)
    
    # 5. Summary
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Total Income: ${total_income:.2f}", ln=1)
    pdf.cell(0, 10, f"Total Expense: ${total_expense:.2f}", ln=1)
    pdf.cell(0, 10, f"Net Balance: ${total_income - total_expense:.2f}", ln=1)

    # 6. Save File Logic
    file_name = f"Report_{start_date}_to_{end_date}.pdf"
    
    if platform == "android":
        # Try standard download folder
        save_path = f"/sdcard/Download/{file_name}"
    else:
        save_path = file_name

    try:
        pdf.output(save_path)
        return save_path
    except Exception as e:
        # Fallback for Android permissions issues
        if platform == "android":
            from android.storage import app_storage_path
            fallback = os.path.join(app_storage_path(), file_name)
            pdf.output(fallback)
            return fallback
        else:
            raise e