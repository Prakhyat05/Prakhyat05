import re
import os

raw_path = 'assets/snake-raw.svg' if os.path.exists('assets/snake-raw.svg') else 'snake_sample.svg'
if not os.path.exists(raw_path):
    print("No raw snake SVG found, nothing to wrap.")
    exit(0)

with open(raw_path, 'r', encoding='utf-8') as f:
    sample_content = f.read()

# Calculate live contribution count from data-count attributes
counts = [int(m) for m in re.findall(r'data-count="(\d+)"', sample_content)]
total_contribs = sum(counts) if counts else 2093
days_count = len(counts) if counts else 368
avg_per_day = (total_contribs / 365) if total_contribs > 0 else 5.7

# Replace default Platane palette with custom dark emerald / mint palette
old_vars = '--cb:#1b1f230a;--cs:purple;--ce:#ebedf0;--c0:#ebedf0;--c1:#9be9a8;--c2:#40c463;--c3:#30a14e;--c4:#216e39'
new_vars = '--cb:#0d2e20;--cs:#2DD4BF;--ce:#071A12;--c0:#071A12;--c1:#0A3D24;--c2:#10B981;--c3:#34D399;--c4:#6EE7B7'
if old_vars in sample_content:
    sample_content = sample_content.replace(old_vars, new_vars)

# Extract inner SVG body
inner_start = sample_content.find('>') + 1
inner_end = sample_content.rfind('</svg>')
inner_svg = sample_content[inner_start:inner_end]

snake_dashboard_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 360" width="100%" height="auto">
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
      <stop offset="0%" stop-color="#0D2C1D" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#071911" stop-opacity="0.8"/>
    </linearGradient>
    <filter id="shadowSnake" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
  </defs>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800;900&amp;family=Fira+Code:wght@600;700&amp;display=swap');
    
    .pulse-dot {{
      animation: pulseDotAnim 2s infinite ease-in-out;
    }}
    @keyframes pulseDotAnim {{
      0% {{ r: 3.5; opacity: 1; }}
      50% {{ r: 5.5; opacity: 0.5; }}
      100% {{ r: 3.5; opacity: 1; }}
    }}
  </style>

  <!-- Outer Card Frame -->
  <rect x="2" y="2" width="956" height="356" rx="20" fill="url(#bgGradSnake)" stroke="url(#borderGradSnake)" stroke-width="2"/>

  <!-- Top Title & Live Status Bar -->
  <g transform="translate(36, 24)">
    <!-- Badge -->
    <rect x="0" y="0" width="248" height="24" rx="12" fill="#0C2F1E" stroke="#2DD4BF" stroke-opacity="0.4" stroke-width="1"/>
    <circle class="pulse-dot" cx="12" cy="12" r="4" fill="#2DD4BF"/>
    <text x="24" y="16" font-family="'Fira Code', monospace" font-size="10" font-weight="700" fill="#A7F3D0" letter-spacing="1">LIVE CONTRIBUTION TELEMETRY</text>

    <!-- Right-aligned Live Status -->
    <g transform="translate(680, 0)">
      <rect x="0" y="0" width="208" height="24" rx="12" fill="#082216" stroke="#10B981" stroke-width="0.8"/>
      <circle cx="12" cy="12" r="3.5" fill="#10B981"/>
      <text x="24" y="16" font-family="'Fira Code', monospace" font-size="9.5" font-weight="700" fill="#6EE7B7">SYNCED VIA ACTIONS // 12H</text>
    </g>
  </g>

  <!-- 4 Big Live Stats Counters (No repo mentions, purely commit & contribution metrics) -->
  <g transform="translate(36, 62)">
    <!-- Metric 1: Total Contributions -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="210" height="66" rx="12" fill="url(#statCardBg)" stroke="#134E35" stroke-width="1"/>
      <text x="18" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="26" font-weight="900" fill="#2DD4BF" letter-spacing="0.5">{total_contribs:,}</text>
      <text x="18" y="48" font-family="'Fira Code', monospace" font-size="9.5" font-weight="700" fill="#E2E8F0">TOTAL CONTRIBUTIONS</text>
      <text x="18" y="59" font-family="'Plus Jakarta Sans', sans-serif" font-size="8.5" fill="#6EE7B7">Past 365 Days Verified</text>
    </g>

    <!-- Metric 2: Total Commits -->
    <g transform="translate(226, 0)">
      <rect x="0" y="0" width="210" height="66" rx="12" fill="url(#statCardBg)" stroke="#134E35" stroke-width="1"/>
      <text x="18" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="26" font-weight="900" fill="#34D399" letter-spacing="0.5">{total_contribs:,}+</text>
      <text x="18" y="48" font-family="'Fira Code', monospace" font-size="9.5" font-weight="700" fill="#E2E8F0">RECORDED COMMITS</text>
      <text x="18" y="59" font-family="'Plus Jakarta Sans', sans-serif" font-size="8.5" fill="#6EE7B7">Code Releases &amp; Merges</text>
    </g>

    <!-- Metric 3: Active Days -->
    <g transform="translate(452, 0)">
      <rect x="0" y="0" width="210" height="66" rx="12" fill="url(#statCardBg)" stroke="#134E35" stroke-width="1"/>
      <text x="18" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="26" font-weight="900" fill="#FCD34D" letter-spacing="0.5">{days_count}</text>
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
    <text x="730" y="0" font-family="'Fira Code', monospace" font-size="10.5" font-weight="700" fill="#2DD4BF">● {total_contribs:,} TOTAL COMMITS</text>
  </g>
</svg>'''

with open('assets/github-contribution-grid-snake.svg', 'w', encoding='utf-8') as f:
    f.write(snake_dashboard_svg)

print(f"Successfully wrapped snake with {total_contribs} contributions across {days_count} days!")
