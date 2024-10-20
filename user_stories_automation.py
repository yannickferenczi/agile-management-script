import gspread
from pprint import pprint
import os
from dotenv import load_dotenv


load_dotenv()

google_connection = gspread.service_account(filename=os.getenv("CREDENTIALS"))

spreadsheet = google_connection.open("User Stories")

issue_title = "USER STORY: " + spreadsheet.worksheet("Features").acell("H2").value

issue_body = spreadsheet.worksheet("Features").acell("G2").value

label_names = spreadsheet.worksheet("Labels").col_values(1)
label_descriptions = spreadsheet.worksheet("Labels").col_values(2)
label_colors = spreadsheet.worksheet("Labels").col_values(3)
