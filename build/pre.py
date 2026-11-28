# -*- coding: utf-8 -*-
p = '/home/sandbox/work/portfolio/index.html'
s = open(p, encoding='utf-8').read()

# --- Ausbildung section -> English source of truth ---
start = s.index('    <!-- ============ AUSBILDUNG ============ -->')
end = s.index('    <!-- ============ CONTACT ============ -->')
new = '''    <!-- ============ APPRENTICESHIP ============ -->
    <section class="section" id="ausbildung">
      <h2 class="section-title reveal"><span class="mono section-num">// 06</span>Apprenticeship 2027</h2>
      <div class="de-grid">
        <div class="de-copy reveal">
          <p class="de-lede">
            I am applying for an apprenticeship as Fachinformatiker für Anwendungsentwicklung, starting October 2027.
          </p>
          <p>
            I live in Cairo and have worked as a junior software developer at Digi-Sail since
            August 2026, building web and mobile applications with React, TypeScript and PHP.
            I learn best when something actually runs at the end: ChanceClub above is mine,
            from the database to the layout.
          </p>
          <p>
            I am learning German on my own and aim for B1 by mid-2027. I can relocate to
            North Rhine-Westphalia and start there in October 2027. My CV is available in
            German and English.
          </p>
          <div class="proj-links">
            <div class="cv-dl" role="group" aria-label="Download CV">
              <span class="cv-dl-label mono">CV</span>
              <a href="assets/Abdulaziz-Awal-CV-DE.pdf" download data-hover aria-label="Lebenslauf auf Deutsch herunterladen">DE</a>
              <a href="assets/Abdulaziz-Awal-CV.pdf" download data-hover aria-label="Download CV in English">EN</a>
            </div>
            <a class="proj-repo mono" href="mailto:zizoawal@icloud.com" data-hover>zizoawal@icloud.com</a>
          </div>
        </div>
        <ul class="de-facts reveal">
          <li><span>Target</span><strong>Fachinformatiker für Anwendungsentwicklung</strong></li>
          <li><span>Start</span><strong>October 2027</strong></li>
          <li><span>Location</span><strong>North Rhine-Westphalia, ready to move</strong></li>
          <li><span>German</span><strong>Self-study, B1 target by mid-2027</strong></li>
          <li><span>English</span><strong>Fluent</strong></li>
          <li><span>Arabic</span><strong>Native</strong></li>
          <li><span>Education</span><strong>IGCSE 2027: 8 O-Levels and A-Level Computer Science</strong></li>
          <li><span>Experience</span><strong>Junior Software Developer at Digi-Sail since August 2026</strong></li>
        </ul>
      </div>
    </section>

'''
s = s[:start] + new + s[end:]

# --- nav label + hero pill to English ---
s = s.replace('<span class="mono nav-num">05</span>Ausbildung', '<span class="mono nav-num">05</span>Apprenticeship')
s = s.replace("Open to a Fachinformatiker Ausbildung in Germany from October 2027",
              "Open to a Fachinformatiker apprenticeship in Germany from October 2027")

# --- arabic font ---
old_font = '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet" />'
new_font = '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:ital,wght@0,400;0,500;1,400&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet" />'
assert s.count(old_font) == 1
s = s.replace(old_font, new_font)

# --- language menu ---
old_nav = '''    <div class="nav-right">
      <div class="nav-socials">'''
new_nav = '''    <div class="nav-right">
      <div class="nav-lang">
        <button class="nav-lang-btn mono" type="button" aria-haspopup="true" aria-expanded="false" aria-label="Language">
          <span class="nav-lang-cur">EN</span>
        </button>
        <div class="nav-lang-menu" role="menu">
          <button type="button" role="menuitem" data-locale="en" lang="en">English</button>
          <button type="button" role="menuitem" data-locale="ar" lang="ar">العربية</button>
          <button type="button" role="menuitem" data-locale="de" lang="de">Deutsch</button>
        </div>
      </div>
      <div class="nav-socials">'''
assert s.count(old_nav) == 1
s = s.replace(old_nav, new_nav)

# --- scripts ---
old_js = '  <script src="js/main.js"></script>'
new_js = '  <script src="js/i18n.js"></script>\n  <script src="js/main.js"></script>\n  <script src="js/lang.js"></script>'
assert s.count(old_js) == 1
s = s.replace(old_js, new_js)

open(p, 'w', encoding='utf-8').write(s)
print('pre ok')
