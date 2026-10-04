"""Generate a standalone cyberpunk header banner SVG for GitHub profile README.
Ensures 100% visual consistency in both GitHub Light and Dark modes.
"""
W, H = 960, 190

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Amir Elfalw - AI Engineer">
<defs>
  <radialGradient id="bgGlow" cx="50%" cy="50%" r="65%">
    <stop offset="0%" stop-color="#1E0B36"/>
    <stop offset="60%" stop-color="#0D0221"/>
    <stop offset="100%" stop-color="#06010F"/>
  </radialGradient>
  <linearGradient id="neonTitle" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#05D9E8"/>
    <stop offset="40%" stop-color="#F8FAFC"/>
    <stop offset="70%" stop-color="#FF2A6D"/>
    <stop offset="100%" stop-color="#B967FF"/>
  </linearGradient>
  <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#05D9E8"/>
    <stop offset="50%" stop-color="#B967FF"/>
    <stop offset="100%" stop-color="#FF2A6D"/>
  </linearGradient>
  <pattern id="bannerGrid" width="30" height="30" patternUnits="userSpaceOnUse">
    <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#B967FF" stroke-width="0.7" stroke-opacity="0.12"/>
  </pattern>
  <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
    <feMerge>
      <feMergeNode in="coloredBlur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
</defs>

<!-- Background Base & Grid -->
<rect width="{W}" height="{H}" rx="14" fill="url(#bgGlow)"/>
<rect width="{W}" height="{H}" rx="14" fill="url(#bannerGrid)"/>

<!-- Cyber Frame & Outer Border -->
<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="13" fill="none" stroke="url(#borderGrad)" stroke-width="1.8" stroke-opacity="0.85"/>

<!-- Cyber Corner Accents -->
<path d="M 12 28 L 12 12 L 28 12" fill="none" stroke="#05D9E8" stroke-width="3"/>
<path d="M {W-28} 12 L {W-12} 12 L {W-12} 28" fill="none" stroke="#FF2A6D" stroke-width="3"/>
<path d="M 12 {H-28} L 12 {H-12} L 28 {H-12}" fill="none" stroke="#B967FF" stroke-width="3"/>
<path d="M {W-28} {H-12} L {W-12} {H-12} L {W-12} {H-28}" fill="none" stroke="#05D9E8" stroke-width="3"/>

<!-- Top Meta / System Status -->
<g font-family="'JetBrains Mono', 'Fira Code', 'Courier New', monospace" font-size="11">
  <text x="36" y="32" fill="#05D9E8" letter-spacing="2">SYSTEM://INITIALIZED</text>
  <rect x="{W-235}" y="20" width="195" height="22" rx="4" fill="#120A2B" stroke="#05D9E8" stroke-opacity="0.4" stroke-width="1"/>
  <circle cx="{W-222}" cy="31" r="4" fill="#00FF66">
    <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="{W-210}" y="35" fill="#E2E8F0" font-weight="600" letter-spacing="1">STATUS: OPEN TO ROLES</text>
</g>

<!-- Main Name / Title -->
<g text-anchor="middle">
  <text x="{W/2}" y="100" font-family="'Impact', 'Arial Black', sans-serif" font-size="54" font-weight="900" fill="url(#neonTitle)" letter-spacing="4" filter="url(#neonGlow)">AMIR ELFALW</text>
  
  <!-- Subtitle Badge -->
  <rect x="{W/2 - 270}" y="122" width="540" height="28" rx="6" fill="#120A2B" stroke="#B967FF" stroke-opacity="0.5" stroke-width="1.2"/>
  <text x="{W/2}" y="141" font-family="'JetBrains Mono', 'Segoe UI', monospace" font-size="13" font-weight="700" fill="#05D9E8" letter-spacing="2.5">AI ENGINEER · GENAI &amp; RAG · COMPUTER VISION</text>
  
  <!-- Lower scanline decor -->
  <line x1="{W/2 - 340}" y1="164" x2="{W/2 + 340}" y2="164" stroke="#FF2A6D" stroke-opacity="0.35" stroke-width="1" stroke-dasharray="8 6"/>
</g>
</svg>'''

with open("assets/banner.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("Generated assets/banner.svg successfully")
