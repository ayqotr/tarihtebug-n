import requests
from bs4 import BeautifulSoup

URL = "https://www.tarihtebugun.org/tarihte-bugun"
OUT_HTML = "tarih.html"

html = requests.get(URL, timeout=20, headers={"User-Agent": "Mozilla/5.0"}).text
soup = BeautifulSoup(html, "html.parser")

rows = soup.select("table#myTable tbody tr")
items = []

for r in rows:
    # YIL (2. sütun)
    year_td = r.select_one("td:nth-of-type(2)")
    year = year_td.get_text(" ", strip=True).split()[-1] if year_td else ""

    # AY (3. sütun)
    month_td = r.select_one("td:nth-of-type(3)")
    month = month_td.get_text(strip=True) if month_td else ""

    # GÜN (4. sütun)
    day_td = r.select_one("td:nth-of-type(4)")
    day = day_td.get_text(strip=True) if day_td else ""

    full_date = f"{day} {month} {year}".strip()

    # SADECE AÇIKLAMA (6. sütun, <br/> sonrası)
    td6 = r.select_one("td:nth-of-type(6)")
    if not td6:
        continue

    parts = [p.strip() for p in td6.get_text("\n", strip=True).split("\n") if p.strip()]
    desc = parts[1] if len(parts) >= 2 else ""

    if full_date and desc:
        items.append((full_date, desc))

# HTML oluştur
rows_html = "\n".join(
    f"<div class='item'><span class='date'>{d}</span> – <span class='desc'>{t}</span></div>"
    for d, t in items
)

html_out = f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tarihte Bugün</title>
<style>
body {{
  margin: 0;
  font: 14px Arial, sans-serif;
  background: #fff;
  color: #111;
}}
.wrap {{
  padding: 10px;
}}
.item {{
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}}
.date {{
  font-weight: 700;
}}
</style>
</head>
<body>
<div class="wrap">
{rows_html}
</div>
</body>
</html>
"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_out)

print(f"{len(items)} kayıt ile tarihli {OUT_HTML} oluşturuldu.")
