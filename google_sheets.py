import gspread
from google.oauth2.service_account import Credentials

# === Setup Google Sheets ===
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Ganti dengan ID Google Sheet kamu
SHEET_ID = "1xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
sheet = client.open_by_key(SHEET_ID).sheet1

def get_account():
    """Ambil akun pertama yang masih Ready, lalu update jadi Sold."""
    rows = sheet.get_all_records()
    for idx, row in enumerate(rows, start=2):  # Row ke-1 biasanya header
        if row["Status"].lower() == "ready":
            email = row["Email"]
            passwd = row["Password"]
            # Update status
            sheet.update_cell(idx, 3, "Sold")
            return f"📧 Email: `{email}`\n🔑 Password: `{passwd}`\n✅ Status: Sold"
    return "❌ Tidak ada akun Ready lagi."
