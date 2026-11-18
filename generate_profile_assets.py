import os
import base64
import zipfile
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_base64_image(image_path, max_dim=700, crop_bbox=False):
    im = Image.open(image_path)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    
    if crop_bbox:
        bbox = im.getbbox()
        if bbox:
            im = im.crop(bbox)
            
    ratio = min(max_dim / im.width, max_dim / im.height, 1.0)
    if ratio < 1.0:
        new_size = (int(im.width * ratio), int(im.height * ratio))
        im = im.resize(new_size, Image.Resampling.LANCZOS)
    
    temp_path = os.path.join(BASE_DIR, '_temp_opt.png')
    im.save(temp_path, format='PNG', optimize=True)
    with open(temp_path, 'rb') as f:
        data = f.read()
    if os.path.exists(temp_path):
        os.remove(temp_path)
    return base64.b64encode(data).decode('utf-8')

print("Loading and encoding character images...")
# id.png is the high-res Lanczos portrait
b64_id = get_base64_image(os.path.join(BASE_DIR, 'id.png'), max_dim=600, crop_bbox=True)
b64_pointing = get_base64_image(os.path.join(BASE_DIR, 'right_pointing.png'), max_dim=500, crop_bbox=True)
b64_thumbs = get_base64_image(os.path.join(BASE_DIR, '02_thumbs_up.png'), max_dim=500, crop_bbox=True)
b64_laptop = get_base64_image(os.path.join(BASE_DIR, '04_laptop_ok.png'), max_dim=500, crop_bbox=True)
b64_thinking = get_base64_image(os.path.join(BASE_DIR, '05_thinking.png'), max_dim=500, crop_bbox=True)
b64_open_hands = get_base64_image(os.path.join(BASE_DIR, '06_open_hands.png'), max_dim=500, crop_bbox=True)
b64_waving = get_base64_image(os.path.join(BASE_DIR, 'Friendly Waving Man in Leather Jacket.png'), max_dim=500, crop_bbox=True)

print("All character images encoded successfully!")

# ==========================================
# 1. INTRO.SVG
# ==========================================
intro_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 420" width="100%" height="auto">
  <defs>
    <radialGradient id="bgGrad1" cx="72%" cy="45%" r="75%">
      <stop offset="0%" stop-color="#1B4630"/>
      <stop offset="45%" stop-color="#0F2A1C"/>
      <stop offset="100%" stop-color="#06140D"/>
    </radialGradient>

    <linearGradient id="borderGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF" stop-opacity="0.8"/>
      <stop offset="35%" stop-color="#10B981" stop-opacity="0.3"/>
      <stop offset="70%" stop-color="#059669" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#2DD4BF" stop-opacity="0.6"/>
    </linearGradient>

    <linearGradient id="pillGrad1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#133824" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#1E4D34" stop-opacity="0.9"/>
    </linearGradient>

    <pattern id="techDots1" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="#2DD4BF" opacity="0.08"/>
    </pattern>

    <filter id="softGlow1" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="16" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>

    <filter id="cardShadow1" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.6"/>
    </filter>

    <style>
      .bg-rect1 {{ fill: url(#bgGrad1); }}
      .pattern-layer1 {{ fill: url(#techDots1); }}

      .font-sans {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
      .font-mono {{ font-family: 'Fira Code', 'SF Mono', Consolas, Menlo, Monaco, monospace; }}
      .font-condensed {{ font-family: 'Impact', 'Bebas Neue', 'Oswald', 'Plus Jakarta Sans', sans-serif; }}
      .font-script {{ font-family: 'Brush Script MT', 'Reenie Beanie', 'Segoe Script', cursive, sans-serif; }}

      .big-watermark1 {{
        font-size: 145px;
        font-weight: 900;
        letter-spacing: 5px;
        fill: #FFFFFF;
        opacity: 0.12;
      }}

      .script-overlay1 {{
        font-size: 38px;
        fill: #2DD4BF;
        filter: drop-shadow(0 2px 8px rgba(45, 212, 191, 0.4));
      }}

      .typewriter-cursor1 {{
        animation: blinkCursor 0.85s steps(2, start) infinite;
      }}
      @keyframes blinkCursor {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0; }}
      }}

      .name-letter {{
        opacity: 1;
        animation: letterReveal 0.4s ease forwards;
      }}
      @keyframes letterReveal {{
        0% {{ opacity: 0; transform: translateY(4px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}

      .role-track {{
        animation: cycleRoles 8s cubic-bezier(0.77, 0, 0.175, 1) infinite;
      }}
      @keyframes cycleRoles {{
        0%, 20% {{ transform: translateY(0px); }}
        25%, 45% {{ transform: translateY(-38px); }}
        50%, 70% {{ transform: translateY(-76px); }}
        75%, 95% {{ transform: translateY(-114px); }}
        100% {{ transform: translateY(0px); }}
      }}

      .portrait-float {{
        animation: floatPortrait 6s ease-in-out infinite alternate;
      }}
      @keyframes floatPortrait {{
        0% {{ transform: translateY(0px); }}
        100% {{ transform: translateY(-6px); }}
      }}

      .live-dot {{
        animation: pulseLive 2s infinite;
      }}
      @keyframes pulseLive {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.4; transform: scale(0.85); }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        .role-track, .portrait-float, .typewriter-cursor1, .live-dot, .name-letter {{
          animation: none !important;
          transform: none !important;
          opacity: 1 !important;
        }}
      }}
    </style>
  </defs>

  <rect class="bg-rect1" x="1" y="1" width="958" height="418" rx="20" stroke="url(#borderGrad1)" stroke-width="2"/>
  <rect class="pattern-layer1" x="1" y="1" width="958" height="418" rx="20"/>

  <g transform="translate(48, 142)">
    <text class="font-condensed big-watermark1" x="0" y="0">BUILDER</text>
  </g>

  <g transform="translate(48, 42)">
    <rect x="0" y="0" width="224" height="26" rx="13" fill="url(#pillGrad1)" stroke="#2DD4BF" stroke-opacity="0.4" stroke-width="1"/>
    <circle class="live-dot" cx="14" cy="13" r="4.5" fill="#10B981"/>
    <circle cx="14" cy="13" r="8" fill="none" stroke="#10B981" stroke-width="1" opacity="0.4"/>
    <text x="27" y="17" class="font-mono" font-size="11" font-weight="600" fill="#6EE7B7" letter-spacing="1">OPEN TO OPPORTUNITIES</text>
  </g>

  <g transform="translate(48, 92)">
    <text x="0" y="32" class="font-script script-overlay1">Hey there, I am</text>
  </g>

  <g transform="translate(48, 172)">
    <text class="font-condensed" font-size="52" font-weight="900" fill="#FFFFFF" letter-spacing="2">
      <tspan class="name-letter" style="animation-delay: 0.05s;">P</tspan>
      <tspan class="name-letter" style="animation-delay: 0.10s;">R</tspan>
      <tspan class="name-letter" style="animation-delay: 0.15s;">A</tspan>
      <tspan class="name-letter" style="animation-delay: 0.20s;">K</tspan>
      <tspan class="name-letter" style="animation-delay: 0.25s;">H</tspan>
      <tspan class="name-letter" style="animation-delay: 0.30s;">Y</tspan>
      <tspan class="name-letter" style="animation-delay: 0.35s;">A</tspan>
      <tspan class="name-letter" style="animation-delay: 0.40s;">T</tspan>
      <tspan dx="14" class="name-letter" style="animation-delay: 0.48s;">P</tspan>
      <tspan class="name-letter" style="animation-delay: 0.53s;">R</tspan>
      <tspan class="name-letter" style="animation-delay: 0.58s;">A</tspan>
      <tspan class="name-letter" style="animation-delay: 0.63s;">K</tspan>
      <tspan class="name-letter" style="animation-delay: 0.68s;">H</tspan>
      <tspan class="name-letter" style="animation-delay: 0.73s;">A</tspan>
      <tspan class="name-letter" style="animation-delay: 0.78s;">R</tspan>
    </text>
    <rect class="typewriter-cursor1" x="515" y="-38" width="4" height="46" fill="#2DD4BF" rx="2"/>
  </g>

  <g transform="translate(48, 206)">
    <text x="0" y="24" class="font-mono" font-size="16" font-weight="700" fill="#2DD4BF">&gt;</text>
    <g transform="translate(20, 0)">
      <clipPath id="roleClip1">
        <rect x="0" y="0" width="480" height="36"/>
      </clipPath>
      <g clip-path="url(#roleClip1)">
        <g class="role-track">
          <text x="0" y="26" class="font-sans" font-size="20" font-weight="700" fill="#34D399" letter-spacing="0.5">Full Stack Developer</text>
          <text x="0" y="64" class="font-sans" font-size="20" font-weight="700" fill="#2DD4BF" letter-spacing="0.5">AI &amp; ML Integrations</text>
          <text x="0" y="102" class="font-sans" font-size="20" font-weight="700" fill="#6EE7B7" letter-spacing="0.5">Mobile App Engineer</text>
          <text x="0" y="140" class="font-sans" font-size="20" font-weight="700" fill="#A7F3D0" letter-spacing="0.5">System Architect</text>
        </g>
      </g>
    </g>
  </g>

  <g transform="translate(48, 268)">
    <text class="font-sans" font-size="14.5" fill="#D1D5DB" line-height="1.5">
      <tspan x="0" y="0">Architecting resilient distributed systems, production LLM pipelines &amp; responsive</tspan>
      <tspan x="0" y="24">mobile apps. Turning complex engineering challenges into elegant high-throughput code.</tspan>
    </text>
  </g>

  <g transform="translate(48, 335)">
    <g transform="translate(0, 0)">
      <rect width="138" height="28" rx="7" fill="#133824" stroke="#2DD4BF" stroke-opacity="0.3" stroke-width="0.8"/>
      <text x="14" y="18" class="font-mono" font-size="11.5" font-weight="600" fill="#A7F3D0">📍 India (Worldwide)</text>
    </g>
    <g transform="translate(150, 0)">
      <rect width="132" height="28" rx="7" fill="#133824" stroke="#2DD4BF" stroke-opacity="0.3" stroke-width="0.8"/>
      <text x="14" y="18" class="font-mono" font-size="11.5" font-weight="600" fill="#A7F3D0">🎓 SLIET Longowal</text>
    </g>
    <g transform="translate(294, 0)">
      <rect width="170" height="28" rx="7" fill="#133824" stroke="#2DD4BF" stroke-opacity="0.3" stroke-width="0.8"/>
      <text x="14" y="18" class="font-mono" font-size="11.5" font-weight="600" fill="#A7F3D0">⚡ CycleOne &amp; LuminAI</text>
    </g>
  </g>

  <!-- High-Res ID Portrait Frame -->
  <g transform="translate(565, 18)">
    <rect x="0" y="0" width="355" height="385" rx="18" fill="#0C2417" stroke="#2DD4BF" stroke-width="1.5" stroke-opacity="0.6" filter="url(#cardShadow1)"/>
    <rect x="10" y="10" width="335" height="365" rx="12" fill="#07180F" stroke="#10B981" stroke-width="0.8" stroke-opacity="0.3"/>
    
    <!-- Lanyard tab -->
    <rect x="135" y="-8" width="85" height="14" rx="4" fill="#04100A" stroke="#2DD4BF" stroke-width="1"/>
    <rect x="160" y="-3" width="35" height="4" rx="2" fill="#2DD4BF"/>
    
    <g class="portrait-float">
      <image href="data:image/png;base64,{b64_id}" x="12" y="14" width="331" height="357" preserveAspectRatio="xMidYMid meet"/>
    </g>
    
    <!-- ID HUD Tag -->
    <rect x="22" y="338" width="165" height="24" rx="6" fill="#04100D" stroke="#2DD4BF" stroke-width="1" opacity="0.95"/>
    <circle cx="34" cy="350" r="4" fill="#10B981"/>
    <text x="44" y="354" class="font-mono" font-size="10.5" font-weight="700" fill="#A7F3D0">VERIFIED DEV // ID.01</text>
  </g>
</svg>'''

with open(os.path.join(BASE_DIR, 'intro.svg'), 'w', encoding='utf-8') as f:
    f.write(intro_svg)
print("Saved intro.svg!")

# ==========================================
# 2. RIGHT-NOW.SVG
# ==========================================
right_now_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 360" width="100%" height="auto">
  <defs>
    <radialGradient id="bgGrad2" cx="30%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#1B4630"/>
      <stop offset="60%" stop-color="#0F2A1C"/>
      <stop offset="100%" stop-color="#06140D"/>
    </radialGradient>

    <linearGradient id="borderGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#10B981" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#2DD4BF" stop-opacity="0.7"/>
    </linearGradient>

    <linearGradient id="cardGrad2" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#153E28"/>
      <stop offset="100%" stop-color="#0D2719"/>
    </linearGradient>

    <pattern id="techDots2" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="#2DD4BF" opacity="0.08"/>
    </pattern>

    <filter id="cardShadow2" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000000" flood-opacity="0.5"/>
    </filter>

    <style>
      .bg-rect2 {{ fill: url(#bgGrad2); }}
      .pattern-layer2 {{ fill: url(#techDots2); }}

      .font-sans {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
      .font-mono {{ font-family: 'Fira Code', 'SF Mono', Consolas, Menlo, Monaco, monospace; }}

      .fade-card {{
        opacity: 1;
        animation: cardSlideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      }}
      .card-c1 {{ animation-delay: 0.15s; }}
      .card-c2 {{ animation-delay: 0.45s; }}
      .card-c3 {{ animation-delay: 0.75s; }}

      @keyframes cardSlideUp {{
        0% {{ opacity: 0; transform: translateY(18px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}

      .pulse-beacon {{
        animation: beaconGlow 2.5s infinite;
      }}
      @keyframes beaconGlow {{
        0%, 100% {{ transform: scale(1); opacity: 0.9; }}
        50% {{ transform: scale(1.4); opacity: 0.2; }}
      }}

      .thumbs-float {{
        animation: floatThumbs 5s ease-in-out infinite alternate;
      }}
      @keyframes floatThumbs {{
        0% {{ transform: translateY(0); }}
        100% {{ transform: translateY(-6px); }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        .fade-card, .pulse-beacon, .thumbs-float {{
          animation: none !important;
          transform: none !important;
          opacity: 1 !important;
        }}
      }}
    </style>
  </defs>

  <rect class="bg-rect2" x="1" y="1" width="958" height="358" rx="18" stroke="url(#borderGrad2)" stroke-width="2"/>
  <rect class="pattern-layer2" x="1" y="1" width="958" height="358" rx="18"/>

  <g transform="translate(36, 32)">
    <rect x="0" y="0" width="135" height="22" rx="11" fill="#133824" stroke="#2DD4BF" stroke-opacity="0.3" stroke-width="0.8"/>
    <circle cx="12" cy="11" r="3.5" fill="#2DD4BF"/>
    <text x="22" y="15" class="font-mono" font-size="10.5" font-weight="600" fill="#A7F3D0" letter-spacing="1">RADAR // NOW</text>

    <text x="0" y="46" class="font-sans" font-size="24" font-weight="800" fill="#FFFFFF" letter-spacing="0.3">What I'm Focused On Right Now</text>
    <text x="0" y="66" class="font-sans" font-size="13" fill="#9CA3AF">Active engineering pursuits, research spikes, and continuous learning streams</text>
  </g>

  <!-- 3 CARDS COLUMN -->
  <g transform="translate(36, 115)">
    <!-- CARD 1: BUILDING -->
    <g class="fade-card card-c1" transform="translate(0, 0)">
      <rect width="640" height="66" rx="12" fill="url(#cardGrad2)" stroke="#2DD4BF" stroke-width="1" stroke-opacity="0.5" filter="url(#cardShadow2)"/>
      <circle cx="34" cy="33" r="16" fill="#10B981" fill-opacity="0.15"/>
      <text x="34" y="39" font-size="16" text-anchor="middle">🛠️</text>
      <text x="64" y="27" class="font-mono" font-size="10.5" font-weight="700" fill="#2DD4BF" letter-spacing="1">BUILDING</text>
      <text x="64" y="47" class="font-sans" font-size="14.5" font-weight="700" fill="#FFFFFF">CycleOne SLIET, LuminAI Fitness &amp; OmniMark OMR Evaluator</text>
      
      <rect x="530" y="20" width="94" height="24" rx="6" fill="#0A2216" stroke="#2DD4BF" stroke-width="0.8"/>
      <circle class="pulse-beacon" cx="542" cy="32" r="3.5" fill="#10B981"/>
      <text x="552" y="36" class="font-mono" font-size="9.5" font-weight="600" fill="#6EE7B7">ACTIVE DEV</text>
    </g>

    <!-- CARD 2: LEARNING -->
    <g class="fade-card card-c2" transform="translate(0, 78)">
      <rect width="640" height="66" rx="12" fill="url(#cardGrad2)" stroke="#10B981" stroke-width="1" stroke-opacity="0.4" filter="url(#cardShadow2)"/>
      <circle cx="34" cy="33" r="16" fill="#10B981" fill-opacity="0.15"/>
      <text x="34" y="39" font-size="16" text-anchor="middle">🧠</text>
      <text x="64" y="27" class="font-mono" font-size="10.5" font-weight="700" fill="#34D399" letter-spacing="1">LEARNING</text>
      <text x="64" y="47" class="font-sans" font-size="14.5" font-weight="700" fill="#FFFFFF">Agentic Workflows, LangGraph Orchestration &amp; Deep Learning</text>
      
      <rect x="530" y="20" width="94" height="24" rx="6" fill="#0A2216" stroke="#10B981" stroke-width="0.8"/>
      <circle class="pulse-beacon" cx="542" cy="32" r="3.5" fill="#34D399"/>
      <text x="552" y="36" class="font-mono" font-size="9.5" font-weight="600" fill="#A7F3D0">EXPANDING</text>
    </g>

    <!-- CARD 3: READING -->
    <g class="fade-card card-c3" transform="translate(0, 156)">
      <rect width="640" height="66" rx="12" fill="url(#cardGrad2)" stroke="#059669" stroke-width="1" stroke-opacity="0.4" filter="url(#cardShadow2)"/>
      <circle cx="34" cy="33" r="16" fill="#10B981" fill-opacity="0.15"/>
      <text x="34" y="39" font-size="16" text-anchor="middle">📖</text>
      <text x="64" y="27" class="font-mono" font-size="10.5" font-weight="700" fill="#6EE7B7" letter-spacing="1">READING</text>
      <text x="64" y="47" class="font-sans" font-size="14.5" font-weight="700" fill="#FFFFFF">Designing Data-Intensive Applications — Martin Kleppmann</text>
      
      <rect x="530" y="20" width="94" height="24" rx="6" fill="#0A2216" stroke="#059669" stroke-width="0.8"/>
      <circle class="pulse-beacon" cx="542" cy="32" r="3.5" fill="#6EE7B7"/>
      <text x="552" y="36" class="font-mono" font-size="9.5" font-weight="600" fill="#D1FAE5">READING</text>
    </g>
  </g>

  <!-- Character Accent: 02_thumbs_up.png -->
  <g transform="translate(695, 20)">
    <circle cx="120" cy="165" r="115" fill="#2DD4BF" opacity="0.08" filter="url(#cardShadow2)"/>
    <g class="thumbs-float">
      <image href="data:image/png;base64,{b64_thumbs}" x="0" y="0" width="245" height="340" preserveAspectRatio="xMidYMid meet"/>
    </g>
  </g>
</svg>'''

with open(os.path.join(BASE_DIR, 'right-now.svg'), 'w', encoding='utf-8') as f:
    f.write(right_now_svg)
print("Saved right-now.svg!")

# ==========================================
# 3. TOOLKIT.SVG (3D Keyboard Keys)
# ==========================================
toolkit_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 420" width="100%" height="auto">
  <defs>
    <radialGradient id="bgGrad3" cx="70%" cy="40%" r="80%">
      <stop offset="0%" stop-color="#1B4630"/>
      <stop offset="50%" stop-color="#0F2A1C"/>
      <stop offset="100%" stop-color="#06140D"/>
    </radialGradient>

    <linearGradient id="borderGrad3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#10B981" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#2DD4BF" stop-opacity="0.7"/>
    </linearGradient>

    <linearGradient id="keyTopGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#194D33"/>
      <stop offset="100%" stop-color="#0E2F1E"/>
    </linearGradient>

    <pattern id="techDots3" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="#2DD4BF" opacity="0.08"/>
    </pattern>

    <filter id="keyShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feDropShadow dx="0" dy="4" stdDeviation="3" flood-color="#000000" flood-opacity="0.7"/>
    </filter>

    <style>
      .bg-rect3 {{ fill: url(#bgGrad3); }}
      .pattern-layer3 {{ fill: url(#techDots3); }}

      .font-sans {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
      .font-mono {{ font-family: 'Fira Code', 'SF Mono', Consolas, Menlo, Monaco, monospace; }}

      .key-press {{
        transform-origin: center;
        animation: pressMotion 5s ease-in-out infinite;
      }}
      @keyframes pressMotion {{
        0%, 100% {{ transform: translateY(0); }}
        8% {{ transform: translateY(3.5px); }}
        16% {{ transform: translateY(0); }}
      }}

      .k-1  {{ animation-delay: 0.1s; }}
      .k-2  {{ animation-delay: 0.35s; }}
      .k-3  {{ animation-delay: 0.6s; }}
      .k-4  {{ animation-delay: 0.85s; }}
      .k-5  {{ animation-delay: 1.1s; }}
      .k-6  {{ animation-delay: 1.35s; }}
      .k-7  {{ animation-delay: 1.6s; }}
      .k-8  {{ animation-delay: 1.85s; }}
      .k-9  {{ animation-delay: 2.1s; }}
      .k-10 {{ animation-delay: 2.35s; }}
      .k-11 {{ animation-delay: 2.6s; }}
      .k-12 {{ animation-delay: 2.85s; }}
      .k-13 {{ animation-delay: 3.1s; }}
      .k-14 {{ animation-delay: 3.35s; }}
      .k-15 {{ animation-delay: 3.6s; }}
      .k-16 {{ animation-delay: 3.85s; }}
      .k-17 {{ animation-delay: 4.1s; }}
      .k-18 {{ animation-delay: 4.35s; }}
      .k-19 {{ animation-delay: 4.6s; }}
      .k-20 {{ animation-delay: 4.85s; }}

      .thinking-float {{
        animation: floatThinking 6s ease-in-out infinite alternate;
      }}
      @keyframes floatThinking {{
        0% {{ transform: translateY(0); }}
        100% {{ transform: translateY(-6px); }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        .key-press, .thinking-float {{
          animation: none !important;
          transform: none !important;
        }}
      }}
    </style>
  </defs>

  <rect class="bg-rect3" x="1" y="1" width="958" height="418" rx="18" stroke="url(#borderGrad3)" stroke-width="2"/>
  <rect class="pattern-layer3" x="1" y="1" width="958" height="418" rx="18"/>

  <!-- Section Header -->
  <g transform="translate(36, 30)">
    <rect x="0" y="0" width="130" height="22" rx="11" fill="#133824" stroke="#2DD4BF" stroke-opacity="0.3" stroke-width="0.8"/>
    <circle cx="12" cy="11" r="3.5" fill="#2DD4BF"/>
    <text x="22" y="15" class="font-mono" font-size="10.5" font-weight="600" fill="#A7F3D0" letter-spacing="1">ARSENAL // 2026</text>

    <text x="0" y="46" class="font-sans" font-size="24" font-weight="800" fill="#FFFFFF" letter-spacing="0.3">Developer Toolkit &amp; Tech Stack</text>
    <text x="0" y="66" class="font-sans" font-size="13" fill="#9CA3AF">Engineered as physical mechanical keys — battle-tested across production applications</text>
  </g>

  <!-- KEYBOARD RACKS (X=36, Y=115) -->
  <g transform="translate(36, 115)">

    <!-- ROW 1: Languages & Core -->
    <g transform="translate(0, 0)">
      <text x="0" y="16" class="font-mono" font-size="11" font-weight="700" fill="#2DD4BF" letter-spacing="1">CORE</text>
      
      <g transform="translate(145, -6)">
        <g class="key-press k-1">
          <rect width="105" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="101" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="52.5" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">TypeScript</text>
        </g>
      </g>
      
      <g transform="translate(258, -6)">
        <g class="key-press k-2">
          <rect width="82" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="78" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="41" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">Python</text>
        </g>
      </g>

      <g transform="translate(348, -6)">
        <g class="key-press k-3">
          <rect width="68" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="64" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="34" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">Dart</text>
        </g>
      </g>

      <g transform="translate(424, -6)">
        <g class="key-press k-4">
          <rect width="78" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="74" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="39" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">C / C++</text>
        </g>
      </g>

      <g transform="translate(510, -6)">
        <g class="key-press k-5">
          <rect width="66" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="62" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="33" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">SQL</text>
        </g>
      </g>

      <g transform="translate(584, -6)">
        <g class="key-press k-6">
          <rect width="74" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="70" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="37" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">Kotlin</text>
        </g>
      </g>
    </g>

    <!-- ROW 2: Frontend & Mobile -->
    <g transform="translate(0, 68)">
      <text x="0" y="16" class="font-mono" font-size="11" font-weight="700" fill="#34D399" letter-spacing="1">UI &amp; APP</text>
      <g transform="translate(145, -6)">
        <g class="key-press k-7">
          <rect width="80" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="76" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="40" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">Flutter</text>
        </g>
      </g>
      <g transform="translate(233, -6)">
        <g class="key-press k-8">
          <rect width="78" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="74" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="39" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">React</text>
        </g>
      </g>
      <g transform="translate(319, -6)">
        <g class="key-press k-9">
          <rect width="82" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="78" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="41" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">Next.js</text>
        </g>
      </g>
      <g transform="translate(409, -6)">
        <g class="key-press k-10">
          <rect width="105" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="101" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="52.5" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">TailwindCSS</text>
        </g>
      </g>
      <g transform="translate(522, -6)">
        <g class="key-press k-11">
          <rect width="68" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="64" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="34" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">Vite</text>
        </g>
      </g>
    </g>

    <!-- ROW 3: Backend & Cloud -->
    <g transform="translate(0, 136)">
      <text x="0" y="16" class="font-mono" font-size="11" font-weight="700" fill="#6EE7B7" letter-spacing="1">BACKEND</text>
      <g transform="translate(145, -6)">
        <g class="key-press k-12">
          <rect width="82" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="78" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="41" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">Node.js</text>
        </g>
      </g>
      <g transform="translate(235, -6)">
        <g class="key-press k-13">
          <rect width="86" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="82" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="43" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">Firebase</text>
        </g>
      </g>
      <g transform="translate(329, -6)">
        <g class="key-press k-14">
          <rect width="92" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="88" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="46" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">Supabase</text>
        </g>
      </g>
      <g transform="translate(429, -6)">
        <g class="key-press k-15">
          <rect width="95" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="91" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="47.5" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">FastAPI</text>
        </g>
      </g>
      <g transform="translate(532, -6)">
        <g class="key-press k-16">
          <rect width="78" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="74" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="39" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">Docker</text>
        </g>
      </g>
    </g>

    <!-- ROW 4: AI & Computer Vision -->
    <g transform="translate(0, 204)">
      <text x="0" y="16" class="font-mono" font-size="11" font-weight="700" fill="#A7F3D0" letter-spacing="1">AI &amp; VISION</text>
      <g transform="translate(145, -6)">
        <g class="key-press k-17">
          <rect width="102" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="98" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="51" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">ML Kit / Vision</text>
        </g>
      </g>
      <g transform="translate(255, -6)">
        <g class="key-press k-18">
          <rect width="90" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="86" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="45" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">PyTorch</text>
        </g>
      </g>
      <g transform="translate(353, -6)">
        <g class="key-press k-19">
          <rect width="92" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="88" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="46" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">OpenCV</text>
        </g>
      </g>
      <g transform="translate(453, -6)">
        <g class="key-press k-20">
          <rect width="102" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="98" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="51" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">Gemini API</text>
        </g>
      </g>
      <g transform="translate(563, -6)">
        <g class="key-press k-1">
          <rect width="84" height="34" rx="6" fill="#0C2417" stroke="#05120B" stroke-width="1.5" filter="url(#keyShadow)"/>
          <rect x="2" y="2" width="80" height="26" rx="4" fill="url(#keyTopGrad)" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.6"/>
          <text x="42" y="19" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5" text-anchor="middle">MediaPipe</text>
        </g>
      </g>
    </g>
  </g>

  <!-- Character Accent: 05_thinking.png -->
  <g transform="translate(710, 35)">
    <circle cx="120" cy="170" r="120" fill="#2DD4BF" opacity="0.08" filter="url(#keyShadow)"/>
    <g class="thinking-float">
      <image href="data:image/png;base64,{b64_thinking}" x="0" y="0" width="245" height="350" preserveAspectRatio="xMidYMid meet"/>
    </g>
  </g>
</svg>'''

with open(os.path.join(BASE_DIR, 'toolkit.svg'), 'w', encoding='utf-8') as f:
    f.write(toolkit_svg)
print("Saved toolkit.svg!")

# ==========================================
# 4. CONTRIBUTIONS.SVG (Animated Sankey Flow)
# ==========================================
# Generate 4 rows x 34 cols of contribution heatmap cells
heatmap_cells_svg = []
import random
random.seed(42)
colors = ['#064E3B', '#047857', '#10B981', '#34D399', '#6EE7B7']
weights = [0.15, 0.25, 0.35, 0.15, 0.10]

for c in range(35):
    for r in range(4):
        x = c * 15
        y = r * 15
        color = random.choices(colors, weights)[0]
        delay = round((c * 0.08 + r * 0.04), 2)
        cell = f'<rect x="{x}" y="{y}" width="11" height="11" rx="2.5" fill="{color}" class="heat-cell" style="animation-delay: {delay}s;"/>'
        heatmap_cells_svg.append(cell)

heatmap_cells_str = "\n      ".join(heatmap_cells_svg)

contributions_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" width="100%" height="auto">
  <defs>
    <radialGradient id="bgGradContrib" cx="50%" cy="35%" r="75%">
      <stop offset="0%" stop-color="#1B4630"/>
      <stop offset="50%" stop-color="#0F2A1C"/>
      <stop offset="100%" stop-color="#04100D"/>
    </radialGradient>

    <linearGradient id="borderGradContrib" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF" stop-opacity="0.8"/>
      <stop offset="35%" stop-color="#10B981" stop-opacity="0.3"/>
      <stop offset="70%" stop-color="#059669" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#2DD4BF" stop-opacity="0.7"/>
    </linearGradient>

    <linearGradient id="ribbonGrad1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10B981" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#2DD4BF" stop-opacity="0.6"/>
    </linearGradient>

    <linearGradient id="ribbonGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#34D399" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#10B981" stop-opacity="0.6"/>
    </linearGradient>

    <linearGradient id="ribbonGrad3" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2DD4BF" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#6EE7B7" stop-opacity="0.6"/>
    </linearGradient>

    <pattern id="techDotsContrib" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="#2DD4BF" opacity="0.08"/>
    </pattern>

    <filter id="contribGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>

    <filter id="shadowContrib" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000000" flood-opacity="0.55"/>
    </filter>

    <style>
      .bg-rect-contrib {{ fill: url(#bgGradContrib); }}
      .pattern-layer-contrib {{ fill: url(#techDotsContrib); }}

      .font-sans {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
      .font-mono {{ font-family: 'Fira Code', 'SF Mono', Consolas, Menlo, Monaco, monospace; }}

      /* Sankey Flow Energy Dashes */
      .flow-stream-1 {{
        stroke-dasharray: 10 22;
        animation: flowSankey1 2.8s linear infinite;
      }}
      @keyframes flowSankey1 {{
        from {{ stroke-dashoffset: 0; }}
        to {{ stroke-dashoffset: -128; }}
      }}

      .flow-stream-2 {{
        stroke-dasharray: 12 24;
        animation: flowSankey2 3.4s linear infinite;
      }}
      @keyframes flowSankey2 {{
        from {{ stroke-dashoffset: 0; }}
        to {{ stroke-dashoffset: -144; }}
      }}

      .flow-stream-3 {{
        stroke-dasharray: 8 20;
        animation: flowSankey3 2.5s linear infinite;
      }}
      @keyframes flowSankey3 {{
        from {{ stroke-dashoffset: 0; }}
        to {{ stroke-dashoffset: -112; }}
      }}

      /* Node Junction Pulse */
      .pulse-node {{
        animation: pulseJunction 2.2s ease-in-out infinite;
      }}
      @keyframes pulseJunction {{
        0%, 100% {{ r: 4.5; opacity: 0.8; }}
        50% {{ r: 6.5; opacity: 1; filter: drop-shadow(0 0 5px #2DD4BF); }}
      }}

      /* Heatmap Wave */
      .heat-cell {{
        animation: heatPulse 4.5s ease-in-out infinite;
      }}
      @keyframes heatPulse {{
        0%, 100% {{ opacity: 0.6; }}
        50% {{ opacity: 1; filter: drop-shadow(0 0 3px #34D399); }}
      }}

      .stat-badge-pulse {{
        animation: statPulse 3s ease-in-out infinite alternate;
      }}
      @keyframes statPulse {{
        0% {{ stroke-opacity: 0.3; }}
        100% {{ stroke-opacity: 0.9; }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        .flow-stream-1, .flow-stream-2, .flow-stream-3, .pulse-node, .heat-cell, .stat-badge-pulse {{
          animation: none !important;
          stroke-dashoffset: 0 !important;
          opacity: 1 !important;
        }}
      }}
    </style>
  </defs>

  <rect class="bg-rect-contrib" x="1" y="1" width="958" height="538" rx="20" stroke="url(#borderGradContrib)" stroke-width="2"/>
  <rect class="pattern-layer-contrib" x="1" y="1" width="958" height="538" rx="20"/>

  <!-- Top Header Section -->
  <g transform="translate(36, 28)">
    <rect x="0" y="0" width="220" height="22" rx="11" fill="#133824" stroke="#2DD4BF" stroke-opacity="0.3" stroke-width="0.8"/>
    <circle cx="12" cy="11" r="3.5" fill="#2DD4BF"/>
    <text x="22" y="15" class="font-mono" font-size="10" font-weight="600" fill="#A7F3D0" letter-spacing="1">GIT CONTRIBUTION PIPELINE</text>

    <text x="0" y="46" class="font-sans" font-size="23" font-weight="800" fill="#FFFFFF" letter-spacing="0.3">Commit Lifecycle &amp; Sankey Contribution Stream</text>
    <text x="0" y="66" class="font-sans" font-size="12.5" fill="#9CA3AF">Active commits flowing through computer vision kinematics, microservices, and verified deployments</text>
  </g>

  <!-- ==========================================
       SANKEY FLOW DIAGRAM
       Col 1 (Repos): X = 36 to 220
       Col 2 (Pipelines): X = 370 to 580
       Col 3 (Deliverables): X = 730 to 924
       ========================================== -->

  <!-- Flow Ribbons Layer (Under nodes) -->
  <g fill="none">
    <!-- REPO 1: CycleOne -> Pipes 1 & 3 -->
    <path d="M 220,126 C 295,126 295,135 370,135" stroke="url(#ribbonGrad1)" stroke-width="10" opacity="0.25"/>
    <path d="M 220,126 C 295,126 295,135 370,135" stroke="#2DD4BF" stroke-width="2.5" class="flow-stream-1"/>

    <path d="M 220,126 C 295,126 295,235 370,235" stroke="url(#ribbonGrad2)" stroke-width="8" opacity="0.2"/>
    <path d="M 220,126 C 295,126 295,235 370,235" stroke="#34D399" stroke-width="2" class="flow-stream-2"/>

    <!-- REPO 2: LuminAI -> Pipes 2 & 1 -->
    <path d="M 220,174 C 295,174 295,185 370,185" stroke="url(#ribbonGrad3)" stroke-width="12" opacity="0.3"/>
    <path d="M 220,174 C 295,174 295,185 370,185" stroke="#6EE7B7" stroke-width="2.8" class="flow-stream-3"/>

    <path d="M 220,174 C 295,174 295,135 370,135" stroke="url(#ribbonGrad1)" stroke-width="8" opacity="0.2"/>
    <path d="M 220,174 C 295,174 295,135 370,135" stroke="#2DD4BF" stroke-width="2" class="flow-stream-1"/>

    <!-- REPO 3: OmniMark -> Pipes 2 & 3 -->
    <path d="M 220,222 C 295,222 295,185 370,185" stroke="url(#ribbonGrad2)" stroke-width="10" opacity="0.25"/>
    <path d="M 220,222 C 295,222 295,185 370,185" stroke="#34D399" stroke-width="2.5" class="flow-stream-2"/>

    <path d="M 220,222 C 295,222 295,235 370,235" stroke="url(#ribbonGrad1)" stroke-width="8" opacity="0.2"/>
    <path d="M 220,222 C 295,222 295,235 370,235" stroke="#2DD4BF" stroke-width="2" class="flow-stream-1"/>

    <!-- REPO 4: IESSD-26 -> Pipes 1 & 4 -->
    <path d="M 220,270 C 295,270 295,135 370,135" stroke="url(#ribbonGrad3)" stroke-width="8" opacity="0.2"/>
    <path d="M 220,270 C 295,270 295,135 370,135" stroke="#6EE7B7" stroke-width="2" class="flow-stream-3"/>

    <path d="M 220,270 C 295,270 295,285 370,285" stroke="url(#ribbonGrad2)" stroke-width="10" opacity="0.25"/>
    <path d="M 220,270 C 295,270 295,285 370,285" stroke="#34D399" stroke-width="2.5" class="flow-stream-2"/>

    <!-- REPO 5: rapsapp -> Pipes 3 & 4 -->
    <path d="M 220,318 C 295,318 295,235 370,235" stroke="url(#ribbonGrad1)" stroke-width="8" opacity="0.2"/>
    <path d="M 220,318 C 295,318 295,235 370,235" stroke="#2DD4BF" stroke-width="2" class="flow-stream-1"/>

    <path d="M 220,318 C 295,318 295,285 370,285" stroke="url(#ribbonGrad3)" stroke-width="10" opacity="0.25"/>
    <path d="M 220,318 C 295,318 295,285 370,285" stroke="#6EE7B7" stroke-width="2.5" class="flow-stream-3"/>

    <!-- MIDDLE TO DELIVERABLES -->
    <!-- Pipe 1 -> Deliverable 1 -->
    <path d="M 580,135 C 655,135 655,135 730,135" stroke="url(#ribbonGrad1)" stroke-width="11" opacity="0.3"/>
    <path d="M 580,135 C 655,135 655,135 730,135" stroke="#2DD4BF" stroke-width="2.6" class="flow-stream-1"/>

    <!-- Pipe 2 -> Deliverable 2 -->
    <path d="M 580,185 C 655,185 655,185 730,185" stroke="url(#ribbonGrad3)" stroke-width="11" opacity="0.3"/>
    <path d="M 580,185 C 655,185 655,185 730,185" stroke="#6EE7B7" stroke-width="2.6" class="flow-stream-3"/>

    <!-- Pipe 3 -> Deliverable 3 -->
    <path d="M 580,235 C 655,235 655,235 730,235" stroke="url(#ribbonGrad2)" stroke-width="11" opacity="0.3"/>
    <path d="M 580,235 C 655,235 655,235 730,235" stroke="#34D399" stroke-width="2.6" class="flow-stream-2"/>

    <!-- Pipe 4 -> Deliverable 4 -->
    <path d="M 580,285 C 655,285 655,285 730,285" stroke="url(#ribbonGrad1)" stroke-width="11" opacity="0.3"/>
    <path d="M 580,285 C 655,285 655,285 730,285" stroke="#2DD4BF" stroke-width="2.6" class="flow-stream-1"/>
  </g>

  <!-- COLUMN 1: SOURCE REPOSITORIES -->
  <g transform="translate(36, 105)">
    <!-- Node 1: CycleOne -->
    <g transform="translate(0, 0)">
      <rect width="184" height="38" rx="8" fill="#0C2518" stroke="#10B981" stroke-width="1" filter="url(#shadowContrib)"/>
      <circle cx="16" cy="19" r="6" fill="#10B981" fill-opacity="0.3"/>
      <circle class="pulse-node" cx="16" cy="19" r="4.5" fill="#34D399"/>
      <text x="30" y="17" class="font-mono" font-size="10.5" font-weight="700" fill="#FFFFFF">CycleOne-Sliet/App</text>
      <text x="30" y="29" class="font-mono" font-size="8.5" fill="#6EE7B7">Kotlin • Fleet Mobility</text>
      <circle cx="184" cy="19" r="4" fill="#2DD4BF"/>
    </g>

    <!-- Node 2: LuminAI -->
    <g transform="translate(0, 48)">
      <rect width="184" height="38" rx="8" fill="#0C2518" stroke="#2DD4BF" stroke-width="1" filter="url(#shadowContrib)"/>
      <circle cx="16" cy="19" r="6" fill="#2DD4BF" fill-opacity="0.3"/>
      <circle class="pulse-node" cx="16" cy="19" r="4.5" fill="#2DD4BF"/>
      <text x="30" y="17" class="font-mono" font-size="10.5" font-weight="700" fill="#FFFFFF">Prakhyat05/LuminAI</text>
      <text x="30" y="29" class="font-mono" font-size="8.5" fill="#2DD4BF">Flutter • 30 FPS Pose</text>
      <circle cx="184" cy="19" r="4" fill="#2DD4BF"/>
    </g>

    <!-- Node 3: OmniMark -->
    <g transform="translate(0, 96)">
      <rect width="184" height="38" rx="8" fill="#0C2518" stroke="#34D399" stroke-width="1" filter="url(#shadowContrib)"/>
      <circle cx="16" cy="19" r="6" fill="#34D399" fill-opacity="0.3"/>
      <circle class="pulse-node" cx="16" cy="19" r="4.5" fill="#34D399"/>
      <text x="30" y="17" class="font-mono" font-size="10.5" font-weight="700" fill="#FFFFFF">OmniMark Evaluator</text>
      <text x="30" y="29" class="font-mono" font-size="8.5" fill="#A7F3D0">PyTorch • Micro-CNN</text>
      <circle cx="184" cy="19" r="4" fill="#34D399"/>
    </g>

    <!-- Node 4: IESSD-26 -->
    <g transform="translate(0, 144)">
      <rect width="184" height="38" rx="8" fill="#0C2518" stroke="#10B981" stroke-width="1" filter="url(#shadowContrib)"/>
      <circle cx="16" cy="19" r="6" fill="#10B981" fill-opacity="0.3"/>
      <circle class="pulse-node" cx="16" cy="19" r="4.5" fill="#10B981"/>
      <text x="30" y="17" class="font-mono" font-size="10.5" font-weight="700" fill="#FFFFFF">Prakhyat05/IESSD-26</text>
      <text x="30" y="29" class="font-mono" font-size="8.5" fill="#6EE7B7">React • TypeScript Portal</text>
      <circle cx="184" cy="19" r="4" fill="#10B981"/>
    </g>

    <!-- Node 5: rapsapp -->
    <g transform="translate(0, 192)">
      <rect width="184" height="38" rx="8" fill="#0C2518" stroke="#2DD4BF" stroke-width="1" filter="url(#shadowContrib)"/>
      <circle cx="16" cy="19" r="6" fill="#2DD4BF" fill-opacity="0.3"/>
      <circle class="pulse-node" cx="16" cy="19" r="4.5" fill="#2DD4BF"/>
      <text x="30" y="17" class="font-mono" font-size="10.5" font-weight="700" fill="#FFFFFF">Prakhyat05/rapsapp</text>
      <text x="30" y="29" class="font-mono" font-size="8.5" fill="#2DD4BF">Dart • Marketplace</text>
      <circle cx="184" cy="19" r="4" fill="#2DD4BF"/>
    </g>
  </g>

  <!-- COLUMN 2: COMMIT & ENGINEERING STREAMS -->
  <g transform="translate(370, 115)">
    <!-- Stream 1 -->
    <g transform="translate(0, 0)">
      <rect width="210" height="40" rx="9" fill="#123824" stroke="#2DD4BF" stroke-width="1" filter="url(#shadowContrib)"/>
      <text x="14" y="18" class="font-mono" font-size="10" font-weight="700" fill="#2DD4BF">STREAM 01 // CORE STATE</text>
      <text x="14" y="32" class="font-sans" font-size="12" font-weight="700" fill="#FFFFFF">Reactive State &amp; Architecture</text>
      <circle cx="0" cy="20" r="3.5" fill="#2DD4BF"/>
      <circle cx="210" cy="20" r="3.5" fill="#2DD4BF"/>
    </g>

    <!-- Stream 2 -->
    <g transform="translate(0, 50)">
      <rect width="210" height="40" rx="9" fill="#123824" stroke="#6EE7B7" stroke-width="1" filter="url(#shadowContrib)"/>
      <text x="14" y="18" class="font-mono" font-size="10" font-weight="700" fill="#6EE7B7">STREAM 02 // ON-DEVICE AI</text>
      <text x="14" y="32" class="font-sans" font-size="12" font-weight="700" fill="#FFFFFF">Vision Kinematics &amp; Micro-CNN</text>
      <circle cx="0" cy="20" r="3.5" fill="#6EE7B7"/>
      <circle cx="210" cy="20" r="3.5" fill="#6EE7B7"/>
    </g>

    <!-- Stream 3 -->
    <g transform="translate(0, 100)">
      <rect width="210" height="40" rx="9" fill="#123824" stroke="#34D399" stroke-width="1" filter="url(#shadowContrib)"/>
      <text x="14" y="18" class="font-mono" font-size="10" font-weight="700" fill="#34D399">STREAM 03 // CLOUD APIS</text>
      <text x="14" y="32" class="font-sans" font-size="12" font-weight="700" fill="#FFFFFF">Serverless &amp; Offline Sync</text>
      <circle cx="0" cy="20" r="3.5" fill="#34D399"/>
      <circle cx="210" cy="20" r="3.5" fill="#34D399"/>
    </g>

    <!-- Stream 4 -->
    <g transform="translate(0, 150)">
      <rect width="210" height="40" rx="9" fill="#123824" stroke="#10B981" stroke-width="1" filter="url(#shadowContrib)"/>
      <text x="14" y="18" class="font-mono" font-size="10" font-weight="700" fill="#10B981">STREAM 04 // PERFORMANCE</text>
      <text x="14" y="32" class="font-sans" font-size="12" font-weight="700" fill="#FFFFFF">CI/CD, Speed &amp; 60 Hz UX</text>
      <circle cx="0" cy="20" r="3.5" fill="#10B981"/>
      <circle cx="210" cy="20" r="3.5" fill="#10B981"/>
    </g>
  </g>

  <!-- COLUMN 3: IMPACT & DELIVERABLES -->
  <g transform="translate(730, 115)">
    <!-- Deliverable 1 -->
    <g transform="translate(0, 0)">
      <rect width="194" height="40" rx="9" fill="#0E2D1D" stroke="#2DD4BF" stroke-width="1" filter="url(#shadowContrib)"/>
      <circle cx="0" cy="20" r="3.5" fill="#2DD4BF"/>
      <text x="14" y="17" class="font-mono" font-size="9" font-weight="700" fill="#34D399">FLEET MOBILITY</text>
      <text x="14" y="31" class="font-sans" font-size="12" font-weight="800" fill="#FFFFFF">500+ Commuters • 99.5%</text>
    </g>

    <!-- Deliverable 2 -->
    <g transform="translate(0, 50)">
      <rect width="194" height="40" rx="9" fill="#0E2D1D" stroke="#6EE7B7" stroke-width="1" filter="url(#shadowContrib)"/>
      <circle cx="0" cy="20" r="3.5" fill="#6EE7B7"/>
      <text x="14" y="17" class="font-mono" font-size="9" font-weight="700" fill="#2DD4BF">AI BIOMECHANICS</text>
      <text x="14" y="31" class="font-sans" font-size="12" font-weight="800" fill="#FFFFFF">30+ FPS Pose Detection</text>
    </g>

    <!-- Deliverable 3 -->
    <g transform="translate(0, 100)">
      <rect width="194" height="40" rx="9" fill="#0E2D1D" stroke="#34D399" stroke-width="1" filter="url(#shadowContrib)"/>
      <circle cx="0" cy="20" r="3.5" fill="#34D399"/>
      <text x="14" y="17" class="font-mono" font-size="9" font-weight="700" fill="#A7F3D0">OMR ENGINE</text>
      <text x="14" y="31" class="font-sans" font-size="12" font-weight="800" fill="#FFFFFF">Automated Mobile Grading</text>
    </g>

    <!-- Deliverable 4 -->
    <g transform="translate(0, 150)">
      <rect width="194" height="40" rx="9" fill="#0E2D1D" stroke="#10B981" stroke-width="1" filter="url(#shadowContrib)"/>
      <circle cx="0" cy="20" r="3.5" fill="#10B981"/>
      <text x="14" y="17" class="font-mono" font-size="9" font-weight="700" fill="#6EE7B7">ACADEMIC &amp; SERVICES</text>
      <text x="14" y="31" class="font-sans" font-size="12" font-weight="800" fill="#FFFFFF">Global IEEE 2026 Portal</text>
    </g>
  </g>

  <!-- ==========================================
       BOTTOM TELEMETRY & CONTRIBUTION HEATMAP
       ========================================== -->
  <g transform="translate(36, 385)">
    <rect width="888" height="125" rx="14" fill="#0A2216" stroke="#2DD4BF" stroke-width="1" stroke-opacity="0.4" filter="url(#shadowContrib)"/>

    <!-- Heatmap Grid Title & Indicators -->
    <g transform="translate(20, 18)">
      <text x="0" y="0" class="font-mono" font-size="10.5" font-weight="700" fill="#A7F3D0" letter-spacing="1">ACTIVITY DENSITY &amp; COMMITS HEATMAP</text>
      <text x="400" y="0" class="font-mono" font-size="9.5" fill="#9CA3AF">Less</text>
      <rect x="432" y="-9" width="10" height="10" rx="2" fill="#064E3B"/>
      <rect x="446" y="-9" width="10" height="10" rx="2" fill="#047857"/>
      <rect x="460" y="-9" width="10" height="10" rx="2" fill="#10B981"/>
      <rect x="474" y="-9" width="10" height="10" rx="2" fill="#34D399"/>
      <rect x="488" y="-9" width="10" height="10" rx="2" fill="#6EE7B7"/>
      <text x="506" y="0" class="font-mono" font-size="9.5" fill="#9CA3AF">More</text>

      <!-- The 4x35 Matrix -->
      <g transform="translate(0, 15)">
        {heatmap_cells_str}
      </g>
    </g>

    <!-- Right Side HUD Metrics -->
    <g transform="translate(585, 20)">
      <line x1="0" y1="0" x2="0" y2="85" stroke="#2DD4BF" stroke-opacity="0.2" stroke-width="1"/>
      
      <g transform="translate(24, 6)">
        <text x="0" y="16" class="font-mono" font-size="10" font-weight="700" fill="#34D399">TOTAL REPO COMMITS</text>
        <text x="0" y="38" class="font-sans" font-size="24" font-weight="900" fill="#FFFFFF">850+</text>
      </g>

      <g transform="translate(160, 6)">
        <text x="0" y="16" class="font-mono" font-size="10" font-weight="700" fill="#2DD4BF">SYSTEM UPTIME</text>
        <text x="0" y="38" class="font-sans" font-size="24" font-weight="900" fill="#FFFFFF">99.5%</text>
      </g>

      <g transform="translate(24, 52)">
        <text x="0" y="16" class="font-mono" font-size="9.5" font-weight="600" fill="#A7F3D0">PR MERGE ACCURACY</text>
        <text x="0" y="32" class="font-sans" font-size="16" font-weight="800" fill="#6EE7B7">100% Verified</text>
      </g>

      <g transform="translate(160, 52)">
        <text x="0" y="16" class="font-mono" font-size="9.5" font-weight="600" fill="#A7F3D0">CONCURRENCY BUGS</text>
        <text x="0" y="32" class="font-sans" font-size="16" font-weight="800" fill="#34D399">0 Failures</text>
      </g>
    </g>
  </g>
</svg>'''

with open(os.path.join(BASE_DIR, 'contributions.svg'), 'w', encoding='utf-8') as f:
    f.write(contributions_svg)
print("Saved contributions.svg!")

# ==========================================
# 5. PROJECTS.SVG (Showcasing the 5 Repositories)
# ==========================================
projects_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" width="100%" height="auto">
  <defs>
    <radialGradient id="bgGradProjects" cx="70%" cy="40%" r="80%">
      <stop offset="0%" stop-color="#19422C"/>
      <stop offset="50%" stop-color="#0F2A1C"/>
      <stop offset="100%" stop-color="#06140D"/>
    </radialGradient>

    <linearGradient id="borderGradProjects" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#10B981" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#2DD4BF" stop-opacity="0.7"/>
    </linearGradient>

    <pattern id="techDotsProjects" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="#2DD4BF" opacity="0.08"/>
    </pattern>

    <filter id="shadowProjects" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000000" flood-opacity="0.5"/>
    </filter>

    <style>
      .bg-rect-projects {{ fill: url(#bgGradProjects); }}
      .pattern-layer-projects {{ fill: url(#techDotsProjects); }}

      .font-sans {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
      .font-mono {{ font-family: 'Fira Code', 'SF Mono', Consolas, Menlo, Monaco, monospace; }}

      .laptop-float {{
        animation: floatLaptop 5.5s ease-in-out infinite alternate;
      }}
      @keyframes floatLaptop {{
        0% {{ transform: translateY(0); }}
        100% {{ transform: translateY(-6px); }}
      }}

      .badge-glow {{
        animation: badgePulse 3s ease-in-out infinite alternate;
      }}
      @keyframes badgePulse {{
        0% {{ stroke-opacity: 0.3; }}
        100% {{ stroke-opacity: 0.8; }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        .laptop-float, .badge-glow {{
          animation: none !important;
          transform: none !important;
        }}
      }}
    </style>
  </defs>

  <rect class="bg-rect-projects" x="1" y="1" width="958" height="518" rx="20" stroke="url(#borderGradProjects)" stroke-width="2"/>
  <rect class="pattern-layer-projects" x="1" y="1" width="958" height="518" rx="20"/>

  <!-- Section Header -->
  <g transform="translate(36, 28)">
    <rect x="0" y="0" width="185" height="22" rx="11" fill="#133824" stroke="#2DD4BF" stroke-opacity="0.3" stroke-width="0.8"/>
    <circle cx="12" cy="11" r="3.5" fill="#2DD4BF"/>
    <text x="22" y="15" class="font-mono" font-size="10.5" font-weight="600" fill="#A7F3D0" letter-spacing="1">FEATURED REPOSITORIES</text>

    <text x="0" y="46" class="font-sans" font-size="23" font-weight="800" fill="#FFFFFF" letter-spacing="0.3">Production Repositories &amp; Architecture</text>
    <text x="0" y="66" class="font-sans" font-size="12.5" fill="#9CA3AF">Open-source mobile platforms, on-device AI kinematics, and high-concurrency systems</text>
  </g>

  <!-- CARDS GRID: 5 Repositories -->
  <g transform="translate(36, 105)">

    <!-- CARD 1: CycleOne SLIET (Top Left) -->
    <g transform="translate(0, 0)">
      <rect width="320" height="118" rx="12" fill="#113120" stroke="#2DD4BF" stroke-width="1" class="badge-glow" filter="url(#shadowProjects)"/>
      <circle cx="28" cy="28" r="14" fill="#0A1F14"/>
      <text x="28" y="34" font-size="15" text-anchor="middle">🚲</text>
      <text x="52" y="24" class="font-mono" font-size="10" font-weight="700" fill="#34D399">CYCLEONE-SLIET / APP</text>
      <text x="52" y="42" class="font-sans" font-size="16" font-weight="800" fill="#FFFFFF">500+ Commuters • 99.5%</text>
      <text x="14" y="74" class="font-sans" font-size="11" fill="#CBD5E1">Smart campus bicycle fleet • Zero concurrency failures</text>
      <text x="14" y="92" class="font-mono" font-size="9.5" fill="#2DD4BF">Kotlin • Flutter • Firebase • NHPC CSR</text>
      <text x="14" y="108" class="font-mono" font-size="9" fill="#6EE7B7">github.com/CycleOne-Sliet/App</text>
    </g>

    <!-- CARD 2: LuminAI (Top Middle) -->
    <g transform="translate(338, 0)">
      <rect width="320" height="118" rx="12" fill="#113120" stroke="#2DD4BF" stroke-width="1" class="badge-glow" filter="url(#shadowProjects)"/>
      <circle cx="28" cy="28" r="14" fill="#0A1F14"/>
      <text x="28" y="34" font-size="15" text-anchor="middle">🧠</text>
      <text x="52" y="24" class="font-mono" font-size="10" font-weight="700" fill="#2DD4BF">PRAKHYAT05 / LUMINAI</text>
      <text x="52" y="42" class="font-sans" font-size="16" font-weight="800" fill="#FFFFFF">30+ FPS Pose Kinematics</text>
      <text x="14" y="74" class="font-sans" font-size="11" fill="#CBD5E1">On-device ML Kit joint tracking &amp; &lt;1.2s Gemini workouts</text>
      <text x="14" y="92" class="font-mono" font-size="9.5" fill="#2DD4BF">Flutter • MediaPipe • Gemini API • SQLite</text>
      <text x="14" y="108" class="font-mono" font-size="9" fill="#6EE7B7">github.com/Prakhyat05/LuminAI</text>
    </g>

    <!-- CARD 3: OmniMark OMR Evaluator (Bottom Left) -->
    <g transform="translate(0, 134)">
      <rect width="320" height="118" rx="12" fill="#113120" stroke="#34D399" stroke-width="1" class="badge-glow" filter="url(#shadowProjects)"/>
      <circle cx="28" cy="28" r="14" fill="#0A1F14"/>
      <text x="28" y="34" font-size="15" text-anchor="middle">📝</text>
      <text x="52" y="24" class="font-mono" font-size="10" font-weight="700" fill="#A7F3D0">OMNIMARK-OMR_SCAN</text>
      <text x="52" y="42" class="font-sans" font-size="16" font-weight="800" fill="#FFFFFF">PyTorch Micro-CNN</text>
      <text x="14" y="74" class="font-sans" font-size="11" fill="#CBD5E1">High-precision mobile OMR scanner &amp; test grading</text>
      <text x="14" y="92" class="font-mono" font-size="9.5" fill="#2DD4BF">Dart • OpenCV • PyTorch • Supabase</text>
      <text x="14" y="108" class="font-mono" font-size="9" fill="#6EE7B7">github.com/Prakhyat05/OmniMark...</text>
    </g>

    <!-- CARD 4: IESSD-26 (Bottom Middle) -->
    <g transform="translate(338, 134)">
      <rect width="320" height="118" rx="12" fill="#113120" stroke="#10B981" stroke-width="1" class="badge-glow" filter="url(#shadowProjects)"/>
      <circle cx="28" cy="28" r="14" fill="#0A1F14"/>
      <text x="28" y="34" font-size="15" text-anchor="middle">🌐</text>
      <text x="52" y="24" class="font-mono" font-size="10" font-weight="700" fill="#6EE7B7">PRAKHYAT05 / IESSD-26</text>
      <text x="52" y="42" class="font-sans" font-size="16" font-weight="800" fill="#FFFFFF">IEEE Conference Portal</text>
      <text x="14" y="74" class="font-sans" font-size="11" fill="#CBD5E1">Official web portal for SLIET International Conference</text>
      <text x="14" y="92" class="font-mono" font-size="9.5" fill="#2DD4BF">React • TypeScript • Tailwind CSS • Vite</text>
      <text x="14" y="108" class="font-mono" font-size="9" fill="#6EE7B7">github.com/Prakhyat05/IESSD-26</text>
    </g>

    <!-- CARD 5: RapsApp (Bottom Row Wide) -->
    <g transform="translate(0, 268)">
      <rect width="658" height="105" rx="12" fill="#113120" stroke="#2DD4BF" stroke-width="1" class="badge-glow" filter="url(#shadowProjects)"/>
      <circle cx="28" cy="28" r="14" fill="#0A1F14"/>
      <text x="28" y="34" font-size="15" text-anchor="middle">🛠️</text>
      <text x="52" y="24" class="font-mono" font-size="10" font-weight="700" fill="#34D399">PRAKHYAT05 / RAPSAPP</text>
      <text x="52" y="42" class="font-sans" font-size="16" font-weight="800" fill="#FFFFFF">Hyperlocal On-Demand Service &amp; Handyman Marketplace</text>
      <text x="14" y="70" class="font-sans" font-size="11.5" fill="#CBD5E1">Full-stack mobile app with live interactive web demo, real-time service booking &amp; geo-scheduling</text>
      <text x="14" y="88" class="font-mono" font-size="9.5" fill="#2DD4BF">Flutter • Dart • Cloud Architecture • Web Demo</text>
      <text x="440" y="88" class="font-mono" font-size="9" fill="#6EE7B7">github.com/Prakhyat05/rapsapp</text>
    </g>
  </g>

  <!-- Character Accent: 04_laptop_ok.png -->
  <g transform="translate(685, 45)">
    <circle cx="130" cy="200" r="125" fill="#2DD4BF" opacity="0.08" filter="url(#shadowProjects)"/>
    <g class="laptop-float">
      <image href="data:image/png;base64,{b64_laptop}" x="0" y="0" width="270" height="420" preserveAspectRatio="xMidYMid meet"/>
    </g>
  </g>
</svg>'''

with open(os.path.join(BASE_DIR, 'projects.svg'), 'w', encoding='utf-8') as f:
    f.write(projects_svg)
print("Saved projects.svg!")

# ==========================================
# 6. CARD.SVG (Collectible Trading Card)
# ==========================================
card_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" width="100%" height="auto">
  <defs>
    <radialGradient id="bgGrad5" cx="50%" cy="50%" r="75%">
      <stop offset="0%" stop-color="#1A422D"/>
      <stop offset="50%" stop-color="#0F2A1C"/>
      <stop offset="100%" stop-color="#06140D"/>
    </radialGradient>

    <!-- Holographic Foil Gradient Border -->
    <linearGradient id="holoBorder" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF"/>
      <stop offset="25%" stop-color="#F59E0B"/>
      <stop offset="50%" stop-color="#EC4899"/>
      <stop offset="75%" stop-color="#10B981"/>
      <stop offset="100%" stop-color="#2DD4BF"/>
    </linearGradient>

    <!-- Sweeping Foil Beam -->
    <linearGradient id="foilSheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="45%" stop-color="#FFFFFF" stop-opacity="0.05"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.45"/>
      <stop offset="55%" stop-color="#2DD4BF" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <pattern id="techDots5" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="#2DD4BF" opacity="0.08"/>
    </pattern>

    <filter id="holoGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>

    <filter id="cardShadow5" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#000000" flood-opacity="0.6"/>
    </filter>

    <clipPath id="cardClip">
      <rect x="0" y="0" width="370" height="465" rx="18"/>
    </clipPath>

    <clipPath id="portraitWindowClip">
      <rect x="18" y="68" width="334" height="195" rx="10"/>
    </clipPath>

    <style>
      .bg-rect5 {{ fill: url(#bgGrad5); }}
      .pattern-layer5 {{ fill: url(#techDots5); }}

      .font-sans {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
      .font-mono {{ font-family: 'Fira Code', 'SF Mono', Consolas, Menlo, Monaco, monospace; }}
      .font-condensed {{ font-family: 'Impact', 'Bebas Neue', 'Oswald', 'Plus Jakarta Sans', sans-serif; }}

      /* Shiny Foil Sweep Animation across the card */
      .shine-beam {{
        animation: foilSweep 4.5s ease-in-out infinite;
      }}
      @keyframes foilSweep {{
        0% {{ transform: translateX(-550px) rotate(25deg); opacity: 0; }}
        20% {{ opacity: 0.85; }}
        50% {{ transform: translateX(550px) rotate(25deg); opacity: 0; }}
        100% {{ transform: translateX(550px) rotate(25deg); opacity: 0; }}
      }}

      .card-float {{
        animation: floatCard 6s ease-in-out infinite alternate;
      }}
      @keyframes floatCard {{
        0% {{ transform: translateY(0); }}
        100% {{ transform: translateY(-8px); }}
      }}

      .sparkle-pulse {{
        animation: sparkleStar 2.5s ease-in-out infinite alternate;
      }}
      @keyframes sparkleStar {{
        0% {{ transform: scale(0.85); opacity: 0.5; }}
        100% {{ transform: scale(1.2); opacity: 1; filter: drop-shadow(0 0 6px #2DD4BF); }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        .shine-beam, .card-float, .sparkle-pulse {{
          animation: none !important;
          transform: none !important;
          opacity: 1 !important;
        }}
      }}
    </style>
  </defs>

  <rect class="bg-rect5" x="1" y="1" width="958" height="518" rx="20" stroke="url(#holoBorder)" stroke-width="2"/>
  <rect class="pattern-layer5" x="1" y="1" width="958" height="518" rx="20"/>

  <!-- Left: Trading Card Container (X=40, Y=26) -->
  <g transform="translate(42, 26)">
    <g class="card-float">
      <!-- Outer Holographic Trading Card -->
      <rect x="0" y="0" width="370" height="465" rx="18" fill="#0A1F15" stroke="url(#holoBorder)" stroke-width="2.5" filter="url(#cardShadow5)"/>
      <rect x="6" y="6" width="358" height="453" rx="14" fill="#05140D" stroke="#2DD4BF" stroke-width="1" stroke-opacity="0.4"/>

      <!-- CARD HEADER: Name & Rarity -->
      <g transform="translate(18, 22)">
        <text class="font-condensed" font-size="20" font-weight="900" fill="#FFFFFF" letter-spacing="1">PRAKHYAT PRAKHAR</text>
        <text x="0" y="18" class="font-mono" font-size="9" font-weight="700" fill="#34D399" letter-spacing="1">LEGENDARY DEV • EDITION #001</text>
        
        <!-- Stars Rating -->
        <g transform="translate(265, -8)">
          <text class="sparkle-pulse" font-size="14">★★★★★</text>
        </g>
      </g>

      <!-- PORTRAIT FRAME -->
      <g transform="translate(18, 54)">
        <rect width="334" height="205" rx="10" fill="#020B07" stroke="#2DD4BF" stroke-width="1.2" stroke-opacity="0.6"/>
        <g clip-path="url(#portraitWindowClip)" transform="translate(-18, -68)">
          <image href="data:image/png;base64,{b64_id}" x="30" y="58" width="310" height="215" preserveAspectRatio="xMidYMid meet"/>
        </g>
        <!-- Overlay HUD stats on image bottom -->
        <rect x="8" y="172" width="138" height="24" rx="6" fill="#06180E" stroke="#10B981" stroke-width="0.8" opacity="0.95"/>
        <text x="16" y="188" class="font-mono" font-size="9" font-weight="700" fill="#A7F3D0">HP 9999 • MANA ∞</text>
      </g>

      <!-- CARD CORE STATS BARS -->
      <g transform="translate(18, 274)">
        <!-- Stat 1: Distributed Architecture -->
        <text x="0" y="12" class="font-mono" font-size="10" font-weight="600" fill="#CBD5E1">Distributed Systems</text>
        <rect x="150" y="4" width="184" height="8" rx="4" fill="#0A2216"/>
        <rect x="150" y="4" width="176" height="8" rx="4" fill="#10B981"/>

        <!-- Stat 2: AI & Kinematics -->
        <text x="0" y="30" class="font-mono" font-size="10" font-weight="600" fill="#CBD5E1">Computer Vision &amp; AI</text>
        <rect x="150" y="22" width="184" height="8" rx="4" fill="#0A2216"/>
        <rect x="150" y="22" width="170" height="8" rx="4" fill="#2DD4BF"/>

        <!-- Stat 3: Mobile & Frontend -->
        <text x="0" y="48" class="font-mono" font-size="10" font-weight="600" fill="#CBD5E1">Mobile Engineering</text>
        <rect x="150" y="40" width="184" height="8" rx="4" fill="#0A2216"/>
        <rect x="150" y="40" width="178" height="8" rx="4" fill="#34D399"/>

        <!-- Stat 4: Speed & Execution -->
        <text x="0" y="66" class="font-mono" font-size="10" font-weight="600" fill="#CBD5E1">Sub-800ms Latency</text>
        <rect x="150" y="58" width="184" height="8" rx="4" fill="#0A2216"/>
        <rect x="150" y="58" width="174" height="8" rx="4" fill="#6EE7B7"/>
      </g>

      <!-- CARD FOOTER FLAVOR TEXT -->
      <g transform="translate(18, 362)">
        <rect width="334" height="85" rx="8" fill="#0B2317" stroke="#2DD4BF" stroke-width="0.8" stroke-opacity="0.4"/>
        <text x="12" y="22" class="font-mono" font-size="10" font-weight="700" fill="#34D399">&lt;SPECIAL ABILITY: ZERO BREAKING CHANGES/&gt;</text>
        <text x="12" y="42" class="font-sans" font-size="11" fill="#E2E8F0">
          <tspan x="12" y="42">Specializes in turning ambiguous requirements into 30+ FPS</tspan>
          <tspan x="12" y="58">on-device intelligence and fault-tolerant mobile backends.</tspan>
          <tspan x="12" y="74" class="font-mono" font-size="9" fill="#2DD4BF">SLIET Longowal • 8.57 CGPA • Tech Lead</tspan>
        </text>
      </g>

      <!-- Shiny Foil Sweep Masked over Card -->
      <g clip-path="url(#cardClip)">
        <rect class="shine-beam" x="-200" y="-100" width="180" height="700" fill="url(#foilSheen)" pointer-events="none"/>
      </g>
    </g>
  </g>

  <!-- Right: 3 Fun Facts / Developer Lore (X=440, Y=30) -->
  <g transform="translate(440, 28)">
    <rect x="0" y="0" width="145" height="22" rx="11" fill="#133824" stroke="#2DD4BF" stroke-opacity="0.3" stroke-width="0.8"/>
    <circle cx="12" cy="11" r="3.5" fill="#2DD4BF"/>
    <text x="22" y="15" class="font-mono" font-size="10.5" font-weight="600" fill="#A7F3D0" letter-spacing="1">DEV LORE &amp; TRIVIA</text>

    <text x="0" y="48" class="font-sans" font-size="24" font-weight="800" fill="#FFFFFF" letter-spacing="0.3">3 Fun Facts &amp; Engineering Truths</text>
    <text x="0" y="68" class="font-sans" font-size="13" fill="#9CA3AF">A few things that fuel my code, architecture decisions, and daily drive</text>

    <!-- FACT 1 -->
    <g transform="translate(0, 92)">
      <rect width="310" height="96" rx="12" fill="#113120" stroke="#2DD4BF" stroke-width="1" stroke-opacity="0.5" filter="url(#cardShadow5)"/>
      <circle cx="28" cy="28" r="14" fill="#0A1F14"/>
      <text x="28" y="34" font-size="15" text-anchor="middle">⚡</text>
      <text x="52" y="24" class="font-mono" font-size="10.5" font-weight="700" fill="#2DD4BF">FACT 01 // LATENCY OBSESSED</text>
      <text x="52" y="42" class="font-sans" font-size="14.5" font-weight="700" fill="#FFFFFF">Sub-800ms Latency Hunter</text>
      <text x="14" y="66" class="font-sans" font-size="11" fill="#CBD5E1">I believe speed is a core feature. From SQLite offline</text>
      <text x="14" y="82" class="font-sans" font-size="11" fill="#CBD5E1">outboxes to frame budget profiling, every millisecond counts.</text>
    </g>

    <!-- FACT 2 -->
    <g transform="translate(0, 202)">
      <rect width="310" height="96" rx="12" fill="#113120" stroke="#10B981" stroke-width="1" stroke-opacity="0.5" filter="url(#cardShadow5)"/>
      <circle cx="28" cy="28" r="14" fill="#0A1F14"/>
      <text x="28" y="34" font-size="15" text-anchor="middle">🚲</text>
      <text x="52" y="24" class="font-mono" font-size="10.5" font-weight="700" fill="#34D399">FACT 02 // MOBILITY ARCHITECT</text>
      <text x="52" y="42" class="font-sans" font-size="14.5" font-weight="700" fill="#FFFFFF">500+ Daily Commuters</text>
      <text x="14" y="66" class="font-sans" font-size="11" fill="#CBD5E1">Architected CycleOne SLIET bicycle sharing fleet with</text>
      <text x="14" y="82" class="font-sans" font-size="11" fill="#CBD5E1">zero concurrency check-in bugs and 99.5% uptime.</text>
    </g>

    <!-- FACT 3 -->
    <g transform="translate(0, 312)">
      <rect width="310" height="96" rx="12" fill="#113120" stroke="#059669" stroke-width="1" stroke-opacity="0.5" filter="url(#cardShadow5)"/>
      <circle cx="28" cy="28" r="14" fill="#0A1F14"/>
      <text x="28" y="34" font-size="15" text-anchor="middle">🎯</text>
      <text x="52" y="24" class="font-mono" font-size="10.5" font-weight="700" fill="#6EE7B7">FACT 03 // VISION PIONEER</text>
      <text x="52" y="42" class="font-sans" font-size="14.5" font-weight="700" fill="#FFFFFF">30+ FPS On-Device Pose ML</text>
      <text x="14" y="66" class="font-sans" font-size="11" fill="#CBD5E1">Extracted multi-joint biomechanical kinematics on-device</text>
      <text x="14" y="82" class="font-sans" font-size="11" fill="#CBD5E1">for LuminAI &amp; PyTorch Micro-CNNs for OmniMark.</text>
    </g>
  </g>

  <!-- Open Hands Accent Character: 06_open_hands.png -->
  <g transform="translate(760, 100)">
    <circle cx="95" cy="190" r="105" fill="#2DD4BF" opacity="0.08" filter="url(#cardShadow5)"/>
    <g class="card-float">
      <image href="data:image/png;base64,{b64_open_hands}" x="0" y="0" width="190" height="380" preserveAspectRatio="xMidYMid meet"/>
    </g>
  </g>
</svg>'''

with open(os.path.join(BASE_DIR, 'card.svg'), 'w', encoding='utf-8') as f:
    f.write(card_svg)
print("Saved card.svg!")

# ==========================================
# 7. CONTACT.SVG (Terminal Call to Collaborate)
# ==========================================
contact_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 360" width="100%" height="auto">
  <defs>
    <radialGradient id="bgGrad6" cx="25%" cy="50%" r="75%">
      <stop offset="0%" stop-color="#1B4630"/>
      <stop offset="50%" stop-color="#0F2A1C"/>
      <stop offset="100%" stop-color="#06140D"/>
    </radialGradient>

    <linearGradient id="borderGrad6" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#10B981" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#2DD4BF" stop-opacity="0.7"/>
    </linearGradient>

    <linearGradient id="terminalGrad6" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0A2216"/>
      <stop offset="100%" stop-color="#05140D"/>
    </linearGradient>

    <pattern id="techDots6" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="#2DD4BF" opacity="0.08"/>
    </pattern>

    <filter id="cardShadow6" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000000" flood-opacity="0.5"/>
    </filter>

    <style>
      .bg-rect6 {{ fill: url(#bgGrad6); }}
      .pattern-layer6 {{ fill: url(#techDots6); }}

      .font-sans {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
      .font-mono {{ font-family: 'Fira Code', 'SF Mono', Consolas, Menlo, Monaco, monospace; }}

      .pointer-pulse {{
        animation: pointBounce 2.5s ease-in-out infinite;
      }}
      @keyframes pointBounce {{
        0%, 100% {{ transform: translateX(0); }}
        50% {{ transform: translateX(8px); }}
      }}

      .term-cursor {{
        animation: cursorFlash 1s steps(2, start) infinite;
      }}
      @keyframes cursorFlash {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0; }}
      }}

      .pulse-ring {{
        animation: ringPulse 2s infinite;
      }}
      @keyframes ringPulse {{
        0% {{ transform: scale(1); opacity: 0.8; }}
        100% {{ transform: scale(1.6); opacity: 0; }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        .pointer-pulse, .term-cursor, .pulse-ring {{
          animation: none !important;
          transform: none !important;
          opacity: 1 !important;
        }}
      }}
    </style>
  </defs>

  <rect class="bg-rect6" x="1" y="1" width="958" height="358" rx="18" stroke="url(#borderGrad6)" stroke-width="2"/>
  <rect class="pattern-layer6" x="1" y="1" width="958" height="358" rx="18"/>

  <!-- Character: right_pointing.png on Left -->
  <g transform="translate(20, 20)">
    <circle cx="160" cy="160" r="130" fill="#2DD4BF" opacity="0.08" filter="url(#cardShadow6)"/>
    <g class="pointer-pulse">
      <image href="data:image/png;base64,{b64_pointing}" x="0" y="0" width="315" height="320" preserveAspectRatio="xMidYMid meet"/>
    </g>
  </g>

  <!-- Collaboration Action Terminal on Right -->
  <g transform="translate(345, 30)">
    <rect width="575" height="295" rx="14" fill="url(#terminalGrad6)" stroke="#2DD4BF" stroke-width="1.2" stroke-opacity="0.6" filter="url(#cardShadow6)"/>
    
    <!-- Terminal Title Bar -->
    <rect x="0" y="0" width="575" height="34" rx="14" fill="#0C2619"/>
    <circle cx="18" cy="17" r="5" fill="#EF4444"/>
    <circle cx="34" cy="17" r="5" fill="#F59E0B"/>
    <circle cx="50" cy="17" r="5" fill="#10B981"/>
    <text x="70" y="21" class="font-mono" font-size="11" font-weight="600" fill="#9CA3AF">bash — collaboration_session.sh — 80x24</text>

    <!-- Terminal Content Body -->
    <g transform="translate(24, 52)">
      <text class="font-mono" font-size="13" font-weight="600" fill="#2DD4BF">$ ./collaborate_with_prakhyat.sh --status</text>
      
      <!-- Output 1: Availability -->
      <g transform="translate(0, 26)">
        <text class="font-mono" font-size="12" fill="#E2E8F0">
          <tspan fill="#34D399">&gt; AVAILABILITY:</tspan> Open for Full-Time SWE, Full Stack &amp; AI Roles
        </text>
      </g>

      <!-- Output 2: Response SLA -->
      <g transform="translate(0, 50)">
        <text class="font-mono" font-size="12" fill="#E2E8F0">
          <tspan fill="#34D399">&gt; RESPONSE TIME:</tspan> &lt; 24 hours (Prompt &amp; Direct)
        </text>
      </g>

      <!-- Output 3: Preferred Stack -->
      <g transform="translate(0, 74)">
        <text class="font-mono" font-size="12" fill="#E2E8F0">
          <tspan fill="#34D399">&gt; CORE EXPERTISE:</tspan> Flutter, React, Next.js, Python, Node, CV/AI
        </text>
      </g>

      <line x1="0" y1="94" x2="525" y2="94" stroke="#2DD4BF" stroke-opacity="0.2" stroke-width="1"/>

      <!-- Contact Actions Box -->
      <g transform="translate(0, 110)">
        <text class="font-mono" font-size="12" font-weight="700" fill="#A7F3D0">DIRECT CHANNELS READY FOR DISPATCH:</text>
        
        <!-- Email Pill -->
        <g transform="translate(0, 18)">
          <rect width="250" height="34" rx="8" fill="#133824" stroke="#10B981" stroke-width="0.8"/>
          <text x="12" y="21" class="font-sans" font-size="11.5" font-weight="600" fill="#ECFDF5">✉️ prakhyatprakhar2004@gmail.com</text>
        </g>

        <!-- LinkedIn Pill -->
        <g transform="translate(265, 18)">
          <rect width="260" height="34" rx="8" fill="#133824" stroke="#2DD4BF" stroke-width="0.8"/>
          <text x="12" y="21" class="font-mono" font-size="11.5" font-weight="600" fill="#ECFDF5">💼 in/prakhyat-prakhar</text>
        </g>
      </g>

      <!-- Blinking Terminal Prompt -->
      <g transform="translate(0, 198)">
        <text class="font-mono" font-size="13" font-weight="600" fill="#2DD4BF">prakhyat@production:~$ connect --instant</text>
        <rect class="term-cursor" x="305" y="-12" width="8" height="16" fill="#34D399"/>
      </g>
    </g>
  </g>
</svg>'''

with open(os.path.join(BASE_DIR, 'contact.svg'), 'w', encoding='utf-8') as f:
    f.write(contact_svg)
print("Saved contact.svg!")

# ==========================================
# 8. SAY-HI.SVG (Waving character on left, social cards on right)
# ==========================================
say_hi_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 380" width="100%" height="auto">
  <defs>
    <radialGradient id="bgGrad7" cx="20%" cy="50%" r="75%">
      <stop offset="0%" stop-color="#1B4630"/>
      <stop offset="50%" stop-color="#0F2A1C"/>
      <stop offset="100%" stop-color="#06140D"/>
    </radialGradient>

    <linearGradient id="borderGrad7" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#10B981" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#2DD4BF" stop-opacity="0.7"/>
    </linearGradient>

    <linearGradient id="cardGrad7" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#143B25"/>
      <stop offset="100%" stop-color="#0C2518"/>
    </linearGradient>

    <pattern id="techDots7" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="#2DD4BF" opacity="0.08"/>
    </pattern>

    <filter id="cardShadow7" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000000" flood-opacity="0.5"/>
    </filter>

    <style>
      .bg-rect7 {{ fill: url(#bgGrad7); }}
      .pattern-layer7 {{ fill: url(#techDots7); }}

      .font-sans {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
      .font-mono {{ font-family: 'Fira Code', 'SF Mono', Consolas, Menlo, Monaco, monospace; }}

      .waving-float {{
        animation: floatWaving 5s ease-in-out infinite alternate;
      }}
      @keyframes floatWaving {{
        0% {{ transform: translateY(0); }}
        100% {{ transform: translateY(-7px); }}
      }}

      .wave-ring {{
        animation: expandRing 2.4s cubic-bezier(0.2, 0.8, 0.4, 1) infinite;
        transform-origin: 85px 115px;
      }}
      @keyframes expandRing {{
        0% {{ transform: scale(0.6); opacity: 0.9; }}
        100% {{ transform: scale(2.2); opacity: 0; }}
      }}

      .social-card-pulse {{
        animation: socialGlow 4s ease-in-out infinite alternate;
      }}
      @keyframes socialGlow {{
        0% {{ stroke-opacity: 0.4; }}
        100% {{ stroke-opacity: 0.85; }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        .waving-float, .wave-ring, .social-card-pulse {{
          animation: none !important;
          transform: none !important;
        }}
      }}
    </style>
  </defs>

  <rect class="bg-rect7" x="1" y="1" width="958" height="378" rx="18" stroke="url(#borderGrad7)" stroke-width="2"/>
  <rect class="pattern-layer7" x="1" y="1" width="958" height="378" rx="18"/>

  <!-- Friendly Waving Character on Left -->
  <g transform="translate(10, 15)">
    <circle cx="160" cy="180" r="140" fill="#2DD4BF" opacity="0.09" filter="url(#cardShadow7)"/>
    <circle cx="85" cy="115" r="10" fill="none" stroke="#2DD4BF" stroke-width="1.5" class="wave-ring"/>
    <circle cx="85" cy="115" r="10" fill="none" stroke="#34D399" stroke-width="1.5" class="wave-ring" style="animation-delay: 1.2s;"/>
    <g class="waving-float">
      <image href="data:image/png;base64,{b64_waving}" x="0" y="0" width="345" height="350" preserveAspectRatio="xMidYMid meet"/>
    </g>
  </g>

  <!-- Right Side: Header and Social Cards (x=380, y=28) -->
  <g transform="translate(380, 28)">
    <rect x="0" y="0" width="120" height="22" rx="11" fill="#133824" stroke="#2DD4BF" stroke-opacity="0.3" stroke-width="0.8"/>
    <circle cx="12" cy="11" r="3.5" fill="#2DD4BF"/>
    <text x="22" y="15" class="font-mono" font-size="10.5" font-weight="600" fill="#A7F3D0" letter-spacing="1">SAY HELLO</text>

    <text x="0" y="48" class="font-sans" font-size="24" font-weight="800" fill="#FFFFFF" letter-spacing="0.3">Let's Connect &amp; Collaborate</text>
    <text x="0" y="68" class="font-sans" font-size="13" fill="#9CA3AF">Whether you have a role, a bold idea, or just want to talk tech — my inbox is open!</text>

    <!-- Social Link Cards Grid (2 columns x 2 rows) -->
    <g transform="translate(0, 92)">

      <!-- CARD 1: LINKEDIN -->
      <g transform="translate(0, 0)">
        <rect width="265" height="96" rx="12" fill="url(#cardGrad7)" stroke="#2DD4BF" stroke-width="1" class="social-card-pulse" filter="url(#cardShadow7)"/>
        <rect x="14" y="14" width="36" height="36" rx="8" fill="#0A66C2"/>
        <text x="32" y="38" font-family="sans-serif" font-size="20" font-weight="900" fill="#FFFFFF" text-anchor="middle">in</text>
        <text x="60" y="28" class="font-sans" font-size="14.5" font-weight="700" fill="#FFFFFF">LinkedIn</text>
        <text x="60" y="44" class="font-mono" font-size="10" font-weight="600" fill="#38BDF8">/in/prakhyat-prakhar</text>
        <text x="14" y="74" class="font-sans" font-size="11" fill="#9CA3AF">Professional network &amp; career updates</text>
      </g>

      <!-- CARD 2: GITHUB -->
      <g transform="translate(280, 0)">
        <rect width="265" height="96" rx="12" fill="url(#cardGrad7)" stroke="#2DD4BF" stroke-width="1" class="social-card-pulse" filter="url(#cardShadow7)"/>
        <rect x="14" y="14" width="36" height="36" rx="8" fill="#24292F" stroke="#4B5563" stroke-width="1"/>
        <text x="32" y="38" font-size="18" text-anchor="middle">🐙</text>
        <text x="60" y="28" class="font-sans" font-size="14.5" font-weight="700" fill="#FFFFFF">GitHub</text>
        <text x="60" y="44" class="font-mono" font-size="10" font-weight="600" fill="#34D399">@Prakhyat05</text>
        <text x="14" y="74" class="font-sans" font-size="11" fill="#9CA3AF">Repositories, contributions &amp; builds</text>
      </g>

      <!-- CARD 3: EMAIL -->
      <g transform="translate(0, 110)">
        <rect width="265" height="96" rx="12" fill="url(#cardGrad7)" stroke="#2DD4BF" stroke-width="1" class="social-card-pulse" filter="url(#cardShadow7)"/>
        <rect x="14" y="14" width="36" height="36" rx="8" fill="#881337" stroke="#BE123C" stroke-width="1"/>
        <text x="32" y="38" font-size="18" text-anchor="middle">✉️</text>
        <text x="60" y="28" class="font-sans" font-size="14.5" font-weight="700" fill="#FFFFFF">Email</text>
        <text x="60" y="44" class="font-sans" font-size="10" font-weight="600" fill="#FDA4AF">prakhyatprakhar2004@gmail.com</text>
        <text x="14" y="74" class="font-sans" font-size="11" fill="#9CA3AF">Direct inbox for offers &amp; collaborations</text>
      </g>

      <!-- CARD 4: RESUME DOWNLOAD -->
      <g transform="translate(280, 110)">
        <rect width="265" height="96" rx="12" fill="url(#cardGrad7)" stroke="#2DD4BF" stroke-width="1" class="social-card-pulse" filter="url(#cardShadow7)"/>
        <rect x="14" y="14" width="36" height="36" rx="8" fill="#14532D" stroke="#16A34A" stroke-width="1"/>
        <text x="32" y="38" font-size="18" text-anchor="middle">📄</text>
        <text x="60" y="28" class="font-sans" font-size="14.5" font-weight="700" fill="#FFFFFF">Resume (PDF)</text>
        <text x="60" y="44" class="font-mono" font-size="10" font-weight="600" fill="#A7F3D0">Prakhyat-Prakhar-Resume.pdf</text>
        <text x="14" y="74" class="font-sans" font-size="11" fill="#9CA3AF">Instant download &amp; verified credentials</text>
      </g>
    </g>

    <!-- Interactive Hint -->
    <text x="2" y="324" class="font-mono" font-size="11.5" fill="#2DD4BF">⚡ Click the direct markdown links below to connect instantly</text>
  </g>
</svg>'''

with open(os.path.join(BASE_DIR, 'say-hi.svg'), 'w', encoding='utf-8') as f:
    f.write(say_hi_svg)
print("Saved say-hi.svg!")


# ==========================================
# 9. README.MD GENERATION
# ==========================================
readme_content = '''# <p align="center">✦ PRAKHYAT PRAKHAR ✦</p>

<p align="center">
  <b>Full Stack Developer • AI Integrations • Scalable Web &amp; Mobile Platforms</b>
</p>

<p align="center">
  <a href="https://raw.githubusercontent.com/Prakhyat05/Prakhyat05/main/Prakhyat-Prakhar-Resume.pdf"><img src="https://img.shields.io/badge/📄_Curriculum_Vitae-Download_Resume_PDF-10B981?style=for-the-badge&logo=adobe-acrobat-reader&logoColor=white" alt="Download Resume" /></a>
  <a href="https://www.linkedin.com/in/prakhyat-prakhar/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="https://github.com/Prakhyat05"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>
  <a href="mailto:prakhyatprakhar2004@gmail.com"><img src="https://img.shields.io/badge/Email-prakhyatprakhar2004%40gmail.com-2DD4BF?style=for-the-badge&logo=gmail&logoColor=black" alt="Email" /></a>
</p>

> 📥 **Quick Resume Download**: Looking for my credentials? **[Click here to Download Prakhyat's Resume (PDF)](https://raw.githubusercontent.com/Prakhyat05/Prakhyat05/main/Prakhyat-Prakhar-Resume.pdf)** or access [`Prakhyat-Prakhar-Resume.pdf`](Prakhyat-Prakhar-Resume.pdf) directly.

---

## ⚡ 1. Introduction &amp; Core Identity

<p align="center">
  <img src="intro.svg?v=1" alt="Prakhyat Prakhar Intro Banner" width="100%" />
</p>

---

## 🚀 2. Currently Focused On (Building • Learning • Reading)

<p align="center">
  <img src="right-now.svg?v=1" alt="What I'm Doing Right Now" width="100%" />
</p>

---

## ⌨️ 3. Developer Arsenal &amp; Mechanical Keyboard Stack

<p align="center">
  <img src="toolkit.svg?v=1" alt="Prakhyat's Developer Toolkit as Keyboard Keys" width="100%" />
</p>

---

## 🌊 4. Git Contributions &amp; Commit Flow Architecture

<p align="center">
  <img src="contributions.svg?v=1" alt="Prakhyat's Git Commit Lifecycle and Sankey Contribution Stream" width="100%" />
</p>

---

## 💼 5. Production Repositories &amp; Engineering Deployments

<p align="center">
  <img src="projects.svg?v=1" alt="Featured Repositories &amp; Architecture Highlights" width="100%" />
</p>

### 🛠️ Key Featured Repositories

| Repository | Tech Stack &amp; Architecture | Engineering Highlights &amp; Metrics | Links |
| :--- | :--- | :--- | :--- |
| **[CycleOne-Sliet/App](https://github.com/CycleOne-Sliet/App)** <br><sub>Smart Campus Bicycle Sharing</sub> | `Kotlin` • `Flutter` • `Firebase Cloud Functions` • `Serverless` | • Architected distributed campus mobility platform serving **500+ student commuters** across SLIET docking stations (**CSR funded by NHPC**).<br>• Engineered automated station checkouts/check-ins with **zero concurrency failures** and **99.5%+ uptime**. | [🐙 GitHub Repository](https://github.com/CycleOne-Sliet/App) |
| **[Prakhyat05/LuminAI](https://github.com/Prakhyat05/LuminAI)** <br><sub>Elite AI Personal Fitness Trainer</sub> | `Flutter` • `Google ML Kit` • `MediaPipe` • `Gemini API` • `SQLite` | • Real-time cross-platform pose detection and biomechanical multi-joint coordinate extraction at **30+ FPS** on-device.<br>• Integrated **Gemini API** with structured prompt engineering and asynchronous thread isolation in Flutter, generating dynamic workouts in **under 1.2s** at **60 Hz** UI rendering. | [🐙 GitHub Repository](https://github.com/Prakhyat05/LuminAI) |
| **[Prakhyat05/OmniMark-OMR_Scan_Evaluator](https://github.com/Prakhyat05/OmniMark-OMR_Scan_Evaluator)** <br><sub>High-Precision Mobile OMR Evaluator</sub> | `Dart` • `Flutter` • `OpenCV` • `PyTorch Micro-CNN` • `FastAPI` • `Supabase` | • Mobile Optical Mark Recognition (OMR) scanner with edge-computed computer vision and PyTorch Micro-CNN bubble classification.<br>• Offline-first SQLite outbox synchronization pipeline with automated Supabase cloud exam grading reporting. | [🐙 GitHub Repository](https://github.com/Prakhyat05/OmniMark-OMR_Scan_Evaluator) |
| **[Prakhyat05/IESSD-26](https://github.com/Prakhyat05/IESSD-26)** <br><sub>International Conference Web Portal</sub> | `React` • `TypeScript` • `Tailwind CSS` • `Vite` | • Official web portal for **IESSD'26** (*International Conference on Innovative Engineering Solutions for Sustainable Development* at SLIET Longowal).<br>• High-speed responsive registration, speaker schedule, and paper submission portal. | [🐙 GitHub Repository](https://github.com/Prakhyat05/IESSD-26) |
| **[Prakhyat05/rapsapp](https://github.com/Prakhyat05/rapsapp)** <br><sub>Hyperlocal On-Demand Service App</sub> | `Dart` • `Flutter` • `Firebase` • `Geolocation` • `Interactive Web Demo` | • Full-featured on-demand service and handyman marketplace application with real-time technician discovery and instant booking.<br>• Includes live interactive web simulation and reactive state management. | [🐙 GitHub Repository](https://github.com/Prakhyat05/rapsapp) |

---

## 🃏 6. Collectible Player Card &amp; Engineering Lore

<p align="center">
  <img src="card.svg?v=1" alt="Prakhyat Prakhar Collectible Holographic Trading Card" width="100%" />
</p>

---

## 🤝 7. Collaboration &amp; Opportunities Terminal

<p align="center">
  <img src="contact.svg?v=1" alt="Call to Collaborate with Prakhyat" width="100%" />
</p>

---

## 👋 8. Say Hi &amp; Connect

<p align="center">
  <img src="say-hi.svg?v=1" alt="Say Hi to Prakhyat" width="100%" />
</p>

### 📬 Quick Direct Connect Links
- 📄 **Curriculum Vitae**: **[Download Resume PDF](https://raw.githubusercontent.com/Prakhyat05/Prakhyat05/main/Prakhyat-Prakhar-Resume.pdf)** (or view local [`Prakhyat-Prakhar-Resume.pdf`](Prakhyat-Prakhar-Resume.pdf))
- 💼 **LinkedIn Profile**: [linkedin.com/in/prakhyat-prakhar](https://www.linkedin.com/in/prakhyat-prakhar/)
- 🐙 **GitHub Profile**: [github.com/Prakhyat05](https://github.com/Prakhyat05)
- ✉️ **Direct Email**: [prakhyatprakhar2004@gmail.com](mailto:prakhyatprakhar2004@gmail.com)
- 📱 **Phone / WhatsApp**: [+91 9199008357](tel:+919199008357)
- 📍 **Location**: Bhagalpur, Bihar &amp; Longowal, Punjab, India *(Open to worldwide remote, hybrid, &amp; on-site roles)*

---

<p align="center">
  <i>Crafted with precision • Animated with 100% pure CSS • Self-contained vector engineering</i>
</p>
'''

with open(os.path.join(BASE_DIR, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme_content)
print("Saved README.md!")

# ==========================================
# 10. ZIP PACKAGING
# ==========================================
zip_path = os.path.join(BASE_DIR, 'github-profile-prakhyat.zip')
files_to_zip = [
    'README.md',
    'intro.svg',
    'right-now.svg',
    'toolkit.svg',
    'contributions.svg',
    'projects.svg',
    'card.svg',
    'contact.svg',
    'say-hi.svg',
    'id.png',
    'right_pointing.png',
    '02_thumbs_up.png',
    '04_laptop_ok.png',
    '05_thinking.png',
    '06_open_hands.png',
    'Friendly Waving Man in Leather Jacket.png',
    'Prakhyat-Prakhar-Resume.pdf'
]

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for filename in files_to_zip:
        file_full_path = os.path.join(BASE_DIR, filename)
        if os.path.exists(file_full_path):
            zipf.write(file_full_path, arcname=filename)
            print(f"Added to ZIP: {filename}")

print(f"Created ZIP bundle: {zip_path} (size: {os.path.getsize(zip_path)/1024:.1f} KB)")
