import urllib.request
import re
import os

print("=== Starting Dynamic Live Snake & Telemetry Sync ===")

# 1. Fetch real-time live contribution count from GitHub
total_contribs = 2113
active_days = 324
avg_per_day = 5.8

try:
    url = "https://github.com/users/Prakhyat05/contributions"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8')
        
        # Parse total from header (e.g. '2,113 contributions in the last year')
        h2_m = re.search(r'([0-9,]+)\s+contributions\s+in\s+the\s+last\s+year', html)
        if h2_m:
            total_contribs = int(h2_m.group(1).replace(',', ''))
            print(f"Fetched live total contributions: {total_contribs:,}")
        
        # Parse active days from tooltips
        tips = re.findall(r'<tool-tip[^>]*>(.*?)</tool-tip>', html)
        if tips:
            act = sum(1 for t in tips if 'contribution' in t and 'No contributions' not in t)
            if act > 0:
                active_days = act
                print(f"Fetched live active days: {active_days}")
        
        avg_per_day = total_contribs / 365.0
        print(f"Calculated average velocity: {avg_per_day:.1f} commits/day")
except Exception as e:
    print(f"Warning: Could not fetch live html from GitHub ({e}), using fallback: {total_contribs}")

# 2. Prepare 4-step rolling count animation values
s1_val = f"{total_contribs - 3:,}"
s2_val = f"{total_contribs - 2:,}"
s3_val = f"{total_contribs - 1:,}"
s4_val = f"{total_contribs:,}"

s1_val_plus = f"{total_contribs - 3:,}+"
s2_val_plus = f"{total_contribs - 2:,}+"
s3_val_plus = f"{total_contribs - 1:,}+"
s4_val_plus = f"{total_contribs:,}+"

# 3. Locate raw snake SVG
raw_path = None
for candidate in ['assets/snake-raw.svg', 'assets/github-contribution-grid-snake.svg', 'snake_sample.svg']:
    if os.path.exists(candidate):
        raw_path = candidate
        break

if not raw_path:
    print("Error: No snake SVG found to wrap!")
    exit(1)

print(f"Using snake source: {raw_path}")
with open(raw_path, 'r', encoding='utf-8') as f:
    sample_content = f.read()

# Replace default Platane palette with custom dark emerald / mint palette
old_vars = '--cb:#1b1f230a;--cs:purple;--ce:#ebedf0;--c0:#ebedf0;--c1:#9be9a8;--c2:#40c463;--c3:#30a14e;--c4:#216e39'
new_vars = '--cb:#0d2e20;--cs:#2DD4BF;--ce:#071A12;--c0:#071A12;--c1:#0A3D24;--c2:#10B981;--c3:#34D399;--c4:#6EE7B7'
if old_vars in sample_content:
    sample_content = sample_content.replace(old_vars, new_vars)

# Extract inner snake canvas
start_tag = '<svg x="0" y="0" width="880" height="150" viewBox="-16 -32 880 192">'
if start_tag in sample_content:
    start_idx = sample_content.find(start_tag) + len(start_tag)
    end_idx = sample_content.find('</svg>', start_idx)
    inner_svg = sample_content[start_idx:end_idx].strip()
else:
    inner_start = sample_content.find('>') + 1
    inner_end = sample_content.rfind('</svg>')
    inner_svg = sample_content[inner_start:inner_end].strip()

dynamic_snake_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 360" width="100%" height="auto">
  <defs>
    <radialGradient id="bgGradSnake" cx="50%" cy="30%" r="80%">
      <stop offset="0%" stop-color="#143D28"/>
      <stop offset="45%" stop-color="#0A2417"/>
      <stop offset="85%" stop-color="#04120C"/>
      <stop offset="100%" stop-color="#020805"/>
    </radialGradient>
    <linearGradient id="borderGradSnake" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF" stop-opacity="0.8"/>
      <stop offset="25%" stop-color="#10B981" stop-opacity="0.4"/>
      <stop offset="75%" stop-color="#059669" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#2DD4BF" stop-opacity="0.75"/>
    </linearGradient>
    <linearGradient id="statCardBg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0D2C1D" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#071911" stop-opacity="0.85"/>
    </linearGradient>
    <filter id="shadowSnake" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
  </defs>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800;900&amp;family=Fira+Code:wght@600;700&amp;display=swap');
    
    /* Live Status Radar Ping */
    .radar-pulse {{
      animation: radarRing 2.4s infinite cubic-bezier(0.215, 0.61, 0.355, 1);
      transform-origin: 12px 12px;
    }}
    @keyframes radarRing {{
      0% {{ r: 3; opacity: 1; }}
      50% {{ r: 8; opacity: 0; }}
      100% {{ r: 3; opacity: 0; }}
    }}

    .live-dot-glow {{
      animation: dotGlow 1.8s infinite ease-in-out alternate;
    }}
    @keyframes dotGlow {{
      0% {{ fill: #10B981; filter: drop-shadow(0 0 1px #10B981); }}
      100% {{ fill: #34D399; filter: drop-shadow(0 0 6px #2DD4BF); }}
    }}

    /* Dynamic Digital Counter Step Animation */
    .step-num {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 26px;
      font-weight: 900;
      letter-spacing: 0.5px;
    }}

    /* Staggered transition revealing live increments */
    .c-s1 {{ animation: animS1 2.8s forwards; }}
    .c-s2 {{ animation: animS2 2.8s forwards; }}
    .c-s3 {{ animation: animS3 2.8s forwards; }}
    .c-s4 {{ animation: animS4 2.8s forwards; }}

    @keyframes animS1 {{
      0% {{ opacity: 1; transform: translateY(0); }}
      24% {{ opacity: 1; transform: translateY(0); }}
      25% {{ opacity: 0; transform: translateY(-8px); }}
      100% {{ opacity: 0; transform: translateY(-8px); }}
    }}
    @keyframes animS2 {{
      0% {{ opacity: 0; transform: translateY(8px); }}
      24% {{ opacity: 0; transform: translateY(8px); }}
      25% {{ opacity: 1; transform: translateY(0); }}
      49% {{ opacity: 1; transform: translateY(0); }}
      50% {{ opacity: 0; transform: translateY(-8px); }}
      100% {{ opacity: 0; transform: translateY(-8px); }}
    }}
    @keyframes animS3 {{
      0% {{ opacity: 0; transform: translateY(8px); }}
      49% {{ opacity: 0; transform: translateY(8px); }}
      50% {{ opacity: 1; transform: translateY(0); }}
      74% {{ opacity: 1; transform: translateY(0); }}
      75% {{ opacity: 0; transform: translateY(-8px); }}
      100% {{ opacity: 0; transform: translateY(-8px); }}
    }}
    @keyframes animS4 {{
      0% {{ opacity: 0; transform: translateY(8px); }}
      74% {{ opacity: 0; transform: translateY(8px); }}
      75% {{ opacity: 1; transform: translateY(0); filter: drop-shadow(0 0 8px #2DD4BF); }}
      88% {{ filter: drop-shadow(0 0 12px #34D399); }}
      100% {{ opacity: 1; transform: translateY(0); filter: none; }}
    }}

    /* Floating "+1" Commit Indicator Particle */
    .particle-float {{
      animation: floatUp 3.2s infinite ease-out;
      font-family: 'Fira Code', monospace;
      font-size: 11px;
      font-weight: 700;
      fill: #34D399;
    }}
    @keyframes floatUp {{
      0% {{ opacity: 0; transform: translateY(0); }}
      40% {{ opacity: 1; }}
      80% {{ opacity: 0.8; transform: translateY(-16px); }}
      100% {{ opacity: 0; transform: translateY(-22px); }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      .c-s1, .c-s2, .c-s3 {{ display: none !important; }}
      .c-s4 {{ opacity: 1 !important; transform: none !important; }}
      .particle-float, .radar-pulse {{ animation: none !important; }}
    }}
  </style>

  <!-- Outer Card Frame -->
  <rect x="2" y="2" width="956" height="356" rx="20" fill="url(#bgGradSnake)" stroke="url(#borderGradSnake)" stroke-width="2"/>

  <!-- Top Title & Live Status Bar -->
  <g transform="translate(36, 24)">
    <!-- Badge -->
    <rect x="0" y="0" width="248" height="24" rx="12" fill="#0C2F1E" stroke="#2DD4BF" stroke-opacity="0.4" stroke-width="1"/>
    <circle class="live-dot-glow" cx="12" cy="12" r="4"/>
    <text x="24" y="16" font-family="'Fira Code', monospace" font-size="10" font-weight="700" fill="#A7F3D0" letter-spacing="1">LIVE CONTRIBUTION TELEMETRY</text>

    <!-- Right-aligned Live Status with Radar Ping -->
    <g transform="translate(670, 0)">
      <rect x="0" y="0" width="218" height="24" rx="12" fill="#082216" stroke="#10B981" stroke-width="0.8"/>
      <!-- Radar Wave Ring -->
      <circle class="radar-pulse" cx="14" cy="12" r="4" fill="none" stroke="#2DD4BF" stroke-width="1"/>
      <circle class="live-dot-glow" cx="14" cy="12" r="3.5"/>
      <text x="26" y="16" font-family="'Fira Code', monospace" font-size="9.5" font-weight="700" fill="#6EE7B7">DYNAMIC REAL-TIME SYNC</text>
    </g>
  </g>

  <!-- 4 Big Live Stats Counters (Dynamic Step-Animated Odometer) -->
  <g transform="translate(36, 62)">
    <!-- Metric 1: Total Contributions with Dynamic Step Counter -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="210" height="66" rx="12" fill="url(#statCardBg)" stroke="#134E35" stroke-width="1"/>
      
      <!-- Counter Animation Sequence -->
      <g>
        <text class="step-num c-s1" x="18" y="32" fill="#2DD4BF">{s1_val}</text>
        <text class="step-num c-s2" x="18" y="32" fill="#2DD4BF">{s2_val}</text>
        <text class="step-num c-s3" x="18" y="32" fill="#2DD4BF">{s3_val}</text>
        <text class="step-num c-s4" x="18" y="32" fill="#2DD4BF">{s4_val}</text>
      </g>

      <!-- Floating particle indicating live delta -->
      <g transform="translate(142, 28)">
        <text class="particle-float">+1 ✦</text>
      </g>

      <text x="18" y="48" font-family="'Fira Code', monospace" font-size="9.5" font-weight="700" fill="#E2E8F0">TOTAL CONTRIBUTIONS</text>
      <text x="18" y="59" font-family="'Plus Jakarta Sans', sans-serif" font-size="8.5" fill="#6EE7B7">● Real-time Live Tracked</text>
    </g>

    <!-- Metric 2: Total Commits & Merges with Dynamic Step Counter -->
    <g transform="translate(226, 0)">
      <rect x="0" y="0" width="210" height="66" rx="12" fill="url(#statCardBg)" stroke="#134E35" stroke-width="1"/>
      
      <!-- Counter Animation Sequence -->
      <g>
        <text class="step-num c-s1" x="18" y="32" fill="#34D399">{s1_val_plus}</text>
        <text class="step-num c-s2" x="18" y="32" fill="#34D399">{s2_val_plus}</text>
        <text class="step-num c-s3" x="18" y="32" fill="#34D399">{s3_val_plus}</text>
        <text class="step-num c-s4" x="18" y="32" fill="#34D399">{s4_val_plus}</text>
      </g>

      <text x="18" y="48" font-family="'Fira Code', monospace" font-size="9.5" font-weight="700" fill="#E2E8F0">RECORDED COMMITS</text>
      <text x="18" y="59" font-family="'Plus Jakarta Sans', sans-serif" font-size="8.5" fill="#6EE7B7">Production Code Merges</text>
    </g>

    <!-- Metric 3: Active Days -->
    <g transform="translate(452, 0)">
      <rect x="0" y="0" width="210" height="66" rx="12" fill="url(#statCardBg)" stroke="#134E35" stroke-width="1"/>
      <text x="18" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="26" font-weight="900" fill="#FCD34D" letter-spacing="0.5">{active_days}</text>
      <text x="18" y="48" font-family="'Fira Code', monospace" font-size="9.5" font-weight="700" fill="#E2E8F0">DAYS MONITORED</text>
      <text x="18" y="59" font-family="'Plus Jakarta Sans', sans-serif" font-size="8.5" fill="#FDE68A">Continuous Engineering</text>
    </g>

    <!-- Metric 4: Consistency / Velocity Tier -->
    <g transform="translate(678, 0)">
      <rect x="0" y="0" width="210" height="66" rx="12" fill="url(#statCardBg)" stroke="#134E35" stroke-width="1"/>
      <text x="18" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="26" font-weight="900" fill="#F472B6" letter-spacing="0.5">TOP 1%</text>
      <text x="18" y="48" font-family="'Fira Code', monospace" font-size="9.5" font-weight="700" fill="#E2E8F0">COMMIT VELOCITY</text>
      <text x="18" y="59" font-family="'Plus Jakarta Sans', sans-serif" font-size="8.5" fill="#FBCFE8">{avg_per_day:.1f} Commits / Day Avg</text>
    </g>
  </g>

  <!-- Snake Grid Viewport -->
  <g transform="translate(40, 148)" filter="url(#shadowSnake)">
    <!-- Inner Snake Canvas -->
    <svg x="0" y="0" width="880" height="150" viewBox="-16 -32 880 192">
      {inner_svg}
    </svg>
  </g>

  <!-- Bottom Legend & Live Telemetry Note -->
  <g transform="translate(40, 332)">
    <text x="0" y="0" font-family="'Fira Code', monospace" font-size="10" fill="#9CA3AF">Less</text>
    <rect x="35" y="-9" width="10" height="10" rx="2" fill="#071A12" stroke="#0D2E20" stroke-width="0.8"/>
    <rect x="49" y="-9" width="10" height="10" rx="2" fill="#0A3D24"/>
    <rect x="63" y="-9" width="10" height="10" rx="2" fill="#10B981"/>
    <rect x="77" y="-9" width="10" height="10" rx="2" fill="#34D399"/>
    <rect x="91" y="-9" width="10" height="10" rx="2" fill="#6EE7B7"/>
    <text x="108" y="0" font-family="'Fira Code', monospace" font-size="10" fill="#9CA3AF">More</text>

    <text x="320" y="0" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" fill="#94A3B8">Autonomous snake slithering across real-time 365-day commit history</text>
    <text x="730" y="0" font-family="'Fira Code', monospace" font-size="10.5" font-weight="700" fill="#2DD4BF">● {s4_val} TOTAL COMMITS</text>
  </g>
</svg>'''

with open('assets/github-contribution-grid-snake.svg', 'w', encoding='utf-8') as f:
    f.write(dynamic_snake_svg)

print(f"Successfully generated dynamic assets/github-contribution-grid-snake.svg with {s4_val} contributions across {active_days} active days!")

# 4. Synchronize README.md with the latest live version tag to guarantee zero cache lag
readme_path = 'README.md'
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_text = f.read()
    
    updated_readme = re.sub(
        r'(github-contribution-grid-snake\.svg\?v=)[^\"]*',
        rf'\g<1>{total_contribs}',
        readme_text
    )
    if updated_readme != readme_text:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(updated_readme)
        print(f"Synchronized README.md cache buster with ?v={total_contribs}")
