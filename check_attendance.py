import pandas as pd

EXCEL_FILE = "attendance.xlsx"

try:
    df = pd.read_excel(EXCEL_FILE)
    print(df)
except FileNotFoundError:
    print("Attendance file not found!")
