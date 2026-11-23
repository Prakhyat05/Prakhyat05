import urllib.request
import re
import datetime

print("=== Building Custom Dark Emerald 365-Day Contribution Calendar SVG ===")

url = "https://github.com/users/Prakhyat05/contributions"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8')

# Parse total contributions
total_contribs = 2267
h2_m = re.search(r'([0-9,]+)\s+contributions\s+in\s+the\s+last\s+year', html)
if h2_m:
    total_contribs = int(h2_m.group(1).replace(',', ''))
print(f"Total Contributions: {total_contribs:,}")

# Parse cells
cells = re.findall(r'<td[^>]*data-date="([^"]+)"[^>]*data-level="([^"]+)"[^>]*>', html)
print(f"Total cells parsed: {len(cells)}")

if not cells:
    print("Error: Could not parse cells!")
    exit(1)

# Active days
active_days = sum(1 for c in cells if c[1] != '0')
print(f"Active days: {active_days}")

# Cell colors matching our dark emerald theme
level_colors = {
    '0': '#082216',  # Deep muted dark emerald (empty)
    '1': '#0E4B2B',  # Low activity
    '2': '#10B981',  # Medium activity (Emerald)
    '3': '#34D399',  # High activity (Mint)
    '4': '#6EE7B7'   # Peak activity (Vibrant light mint)
}

# Grid parameters
cell_size = 11
gap = 3.5
step = cell_size + gap  # 14.5px per week
start_x = 55
start_y = 65

# Group cells by week
# Each column is a week from Sun (row 0) to Sat (row 6)
# First cell date determines day of week
first_date_str = cells[0][0]
first_date = datetime.date.fromisoformat(first_date_str)
# weekday(): Monday is 0, Sunday is 6. In GitHub, Sunday is row 0.
first_day_of_week = (first_date.weekday() + 1) % 7

rects_svg = []
month_labels = []
current_month = None

col = 0
row = first_day_of_week

for i, (date_str, level) in enumerate(cells):
    d = datetime.date.fromisoformat(date_str)
    
    # Check for month transition
    if d.day <= 7 and d.month != current_month and col > 0:
        current_month = d.month
        month_name = d.strftime("%b")
        month_x = start_x + (col * step)
        month_labels.append(f'<text x="{month_x:.1f}" y="{start_y - 10}" font-family="\'Fira Code\', monospace" font-size="10" font-weight="600" fill="#A7F3D0">{month_name}</text>')
    elif current_month is None:
        current_month = d.month
        month_name = d.strftime("%b")
        month_x = start_x + (col * step)
        month_labels.append(f'<text x="{month_x:.1f}" y="{start_y - 10}" font-family="\'Fira Code\', monospace" font-size="10" font-weight="600" fill="#A7F3D0">{month_name}</text>')

    x = start_x + (col * step)
    y = start_y + (row * step)
    fill = level_colors.get(level, level_colors['0'])
    stroke = '#10B981' if level in ['3', '4'] else '#134E35' if level in ['1', '2'] else '#0C2C1D'
    stroke_w = '0.75' if level in ['3', '4'] else '0.5'

    rects_svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" rx="2.5" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>')

    row += 1
    if row > 6:
        row = 0
        col += 1

# Weekday labels
day_labels = [
    f'<text x="{start_x - 12}" y="{start_y + (1 * step) + 9}" text-anchor="end" font-family="\'Fira Code\', monospace" font-size="9" fill="#64748B">Mon</text>',
    f'<text x="{start_x - 12}" y="{start_y + (3 * step) + 9}" text-anchor="end" font-family="\'Fira Code\', monospace" font-size="9" fill="#64748B">Wed</text>',
    f'<text x="{start_x - 12}" y="{start_y + (5 * step) + 9}" text-anchor="end" font-family="\'Fira Code\', monospace" font-size="9" fill="#64748B">Fri</text>'
]

calendar_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 215" width="100%" height="auto">
  <defs>
    <radialGradient id="bgGradCal" cx="50%" cy="30%" r="80%">
      <stop offset="0%" stop-color="#143D28"/>
      <stop offset="45%" stop-color="#0A2417"/>
      <stop offset="85%" stop-color="#04120C"/>
      <stop offset="100%" stop-color="#020805"/>
    </radialGradient>
    <linearGradient id="borderGradCal" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF" stop-opacity="0.8"/>
      <stop offset="30%" stop-color="#10B981" stop-opacity="0.4"/>
      <stop offset="70%" stop-color="#059669" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#2DD4BF" stop-opacity="0.75"/>
    </linearGradient>
    <filter id="shadowCal" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
  </defs>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800;900&amp;family=Fira+Code:wght@600;700&amp;display=swap');
    .radar-pulse {{
      animation: radarRing 2.4s infinite cubic-bezier(0.215, 0.61, 0.355, 1);
      transform-origin: 14px 12px;
    }}
    @keyframes radarRing {{
      0% {{ r: 3; opacity: 1; }}
      50% {{ r: 9; opacity: 0; }}
      100% {{ r: 3; opacity: 0; }}
    }}
    .live-dot-glow {{
      animation: dotGlow 1.8s infinite ease-in-out alternate;
    }}
    @keyframes dotGlow {{
      0% {{ fill: #10B981; filter: drop-shadow(0 0 1px #10B981); }}
      100% {{ fill: #34D399; filter: drop-shadow(0 0 6px #2DD4BF); }}
    }}
  </style>

  <!-- Outer Card Frame -->
  <rect x="2" y="2" width="956" height="211" rx="16" fill="url(#bgGradCal)" stroke="url(#borderGradCal)" stroke-width="1.8" filter="url(#shadowCal)"/>

  <!-- Top Title Bar -->
  <g transform="translate(32, 18)">
    <!-- Badge -->
    <rect x="0" y="0" width="260" height="24" rx="12" fill="#0C2F1E" stroke="#2DD4BF" stroke-opacity="0.4" stroke-width="1"/>
    <circle class="live-dot-glow" cx="12" cy="12" r="4"/>
    <text x="24" y="16" font-family="'Fira Code', monospace" font-size="10" font-weight="700" fill="#A7F3D0" letter-spacing="1">365-DAY COMMIT HEATMAP</text>

    <!-- Right Live Counter & Radar -->
    <g transform="translate(565, 0)">
      <rect x="0" y="0" width="330" height="24" rx="12" fill="#082216" stroke="#10B981" stroke-width="0.8"/>
      <circle class="radar-pulse" cx="14" cy="12" r="4" fill="none" stroke="#2DD4BF" stroke-width="1"/>
      <circle class="live-dot-glow" cx="14" cy="12" r="3.5"/>
      <text x="26" y="16" font-family="'Fira Code', monospace" font-size="9.5" font-weight="700" fill="#6EE7B7">{total_contribs:,} CONTRIBUTIONS • {active_days} ACTIVE DAYS</text>
    </g>
  </g>

  <!-- Month Labels -->
  <g>
    {''.join(month_labels)}
  </g>

  <!-- Weekday Labels -->
  <g>
    {''.join(day_labels)}
  </g>

  <!-- Heatmap Day Squares -->
  <g>
    {''.join(rects_svg)}
  </g>

  <!-- Bottom Legend Bar -->
  <g transform="translate(32, 186)">
    <text x="0" y="10" font-family="'Fira Code', monospace" font-size="9" fill="#64748B">Less</text>
    <rect x="30" y="1" width="10" height="10" rx="2" fill="#082216" stroke="#0C2C1D" stroke-width="0.5"/>
    <rect x="43" y="1" width="10" height="10" rx="2" fill="#0E4B2B" stroke="#134E35" stroke-width="0.5"/>
    <rect x="56" y="1" width="10" height="10" rx="2" fill="#10B981" stroke="#134E35" stroke-width="0.5"/>
    <rect x="69" y="1" width="10" height="10" rx="2" fill="#34D399" stroke="#10B981" stroke-width="0.5"/>
    <rect x="82" y="1" width="10" height="10" rx="2" fill="#6EE7B7" stroke="#2DD4BF" stroke-width="0.5"/>
    <text x="98" y="10" font-family="'Fira Code', monospace" font-size="9" fill="#64748B">More</text>

    <text x="565" y="10" font-family="'Fira Code', monospace" font-size="9" font-weight="700" fill="#2DD4BF">● REAL-TIME DIRECT GITHUB SYNC (LAST 365 DAYS)</text>
  </g>
</svg>
'''

output_path = "assets/contribution-calendar.svg"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(calendar_svg)

print(f"Successfully generated {output_path} with {len(rects_svg)} day squares!")

# Synchronize README.md with the latest version tag
readme_path = 'README.md'
import os
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_text = f.read()
    updated_readme = re.sub(
        r'(contribution-calendar\.svg\?v=)[^\"]*',
        rf'\g<1>{total_contribs}',
        readme_text
    )
    if updated_readme != readme_text:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(updated_readme)
        print(f"Synchronized README.md calendar cache buster with ?v={total_contribs}")
