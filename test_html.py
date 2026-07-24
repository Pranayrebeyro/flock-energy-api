import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://urja-ops.flockenergy.tech"

EMAIL = "operator@urja.local"
PASSWORD = "urja-ops-2026"

client = httpx.Client(
    follow_redirects=True,
    timeout=30.0,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

# -------------------------
# Login
# -------------------------
login = client.post(
    f"{BASE_URL}/login",
    data={
        "email": EMAIL,
        "password": PASSWORD,
    },
)

print("=" * 60)
print("LOGIN STATUS:", login.status_code)
print("=" * 60)

# -------------------------
# Fetch Meter HTML Page
# -------------------------
response = client.get(f"{BASE_URL}/meters/J100000")

print("METER PAGE STATUS:", response.status_code)

# -------------------------
# Save HTML
# -------------------------
with open("meter.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("meter.html created successfully")

# -------------------------
# Parse HTML
# -------------------------
soup = BeautifulSoup(response.text, "html.parser")

print("=" * 60)
print(soup.get_text(separator="\n"))
print("=" * 60)

client.close()