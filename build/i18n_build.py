# -*- coding: utf-8 -*-
import re, json, io

P = '/home/sandbox/work/portfolio/index.html'
html = open(P, encoding='utf-8').read()

# (key, english source text as it appears between tags, arabic, german)
T = [
 ("nav.work","Work","العمل","Arbeit"),
 ("nav.projects","Projects","المشاريع","Projekte"),
 ("nav.experience","Experience","الخبرة","Erfahrung"),
 ("nav.about","About","نبذة عني","Über mich"),
 ("nav.ausbildung","Apprenticeship","التدريب المهني","Ausbildung"),
 ("nav.contact","Contact","تواصل","Kontakt"),
 ("hero.eyebrow","// hello, world, I'm","// أهلاً، أنا","// hallo, ich bin"),
 ("hero.viewWork","View my work","شاهد أعمالي","Meine Arbeiten"),
 ("hero.avail","Open to a Fachinformatiker apprenticeship in Germany from October 2027","متاح للتدريب المهني (\u2066Fachinformatiker\u2069) في ألمانيا من أكتوبر 2027","Offen für eine Ausbildung als Fachinformatiker in Deutschland ab Oktober 2027"),
 ("hero.scroll","scroll","مرّر","scrollen"),
 ("mq.fullstack","Full-Stack Development","تطوير متكامل","Full-Stack-Entwicklung"),
 ("mq.design","Graphic Design","تصميم جرافيك","Grafikdesign"),
 ("work.title","Selected work","أعمال مختارة","Ausgewählte Arbeiten"),
 ("work.live","Live","مباشر","Live"),
 ("work.c1.title","Digi-Sail: Company Website","Digi-Sail: موقع الشركة","Digi-Sail: Firmenwebsite"),
 ("work.c1.body","Design and development of the Digi-Sail company website, end to end. Responsive front-end, PHP back-end, and the visual identity to match.","تصميم وتطوير موقع شركة Digi-Sail من الألف إلى الياء. واجهة أمامية متجاوبة، وخلفية بلغة PHP، وهوية بصرية متناسقة.","Design und Entwicklung der Digi-Sail-Website von Anfang bis Ende. Responsives Frontend, PHP-Backend und die passende visuelle Identität."),
 ("work.c2.title","Client Web Projects @ Digi-Sail","مشاريع ويب لعملاء في Digi-Sail","Kundenprojekte bei Digi-Sail"),
 ("work.c2.body","Full-stack features for client projects across industries: responsive interfaces in React.js and TypeScript, back-end logic in object-oriented PHP.","ميزات متكاملة لمشاريع عملاء في قطاعات مختلفة: واجهات متجاوبة بـ React.js وTypeScript، ومنطق خلفي بـ PHP كائني التوجه.","Full-Stack-Features für Kundenprojekte aus verschiedenen Branchen: responsive Interfaces mit React.js und TypeScript, Backend-Logik in objektorientiertem PHP."),
 ("work.c3.title","Mobile Features @ Digi-Sail","ميزات موبايل في Digi-Sail","Mobile-Features bei Digi-Sail"),
 ("work.c3.body","React Native features shipped as part of a small dev team, contributing to both web and mobile-facing products.","ميزات بـ React Native طُوّرت ضمن فريق صغير، تخدم منتجات ويب وموبايل في الوقت نفسه.","React-Native-Features, die im kleinen Team entstanden sind, für Web- und Mobile-Produkte."),
 ("proj.title","Projects","المشاريع","Projekte"),
 ("proj.prev","Previous project","المشروع السابق","Vorheriges Projekt"),
 ("proj.next","Next project","المشروع التالي","Nächstes Projekt"),
 ("proj.lede","Products I design, build and ship outside work. Everything here is live or open on GitHub.","منتجات أصممها وأبنيها وأشحنها خارج العمل. كل ما هنا حيّ أو مفتوح على GitHub.","Produkte, die ich außerhalb der Arbeit entwerfe, baue und ausliefere. Alles hier ist live oder offen auf GitHub."),
 ("proj.cc.body","A party-games platform for groups. One person opens a lobby, everyone else joins with a six-letter code, and the host picks a game from 17: Wordle, Word Bomb, Imposter, Two Truths and a Lie, Trivia, Draw &amp; Guess, Charades, and six deciders for the arguments.","منصة ألعاب جماعية للمجموعات. شخص واحد يفتح غرفة، والباقي ينضمون برمز من ستة أحرف، والمضيف يختار لعبة من 17: Wordle، قنبلة الكلمات، المحتال، حقيقتان وكذبة، معلومات، ارسم وخمّن، تمثيل، وستة أدوات قرار للخلافات.","Eine Partyspiel-Plattform für Gruppen. Eine Person öffnet eine Runde, alle anderen kommen mit einem sechsstelligen Code dazu, und der Host wählt eines von 17 Spielen: Wordle, Wortbombe, Bluffer, Zwei Wahrheiten und eine Lüge, Trivia, Draw &amp; Guess, Scharade und sechs Entscheider für die Diskussionen."),
 ("proj.cc.p1","Live lobbies with one scoreboard for the whole night, plus tournament mode with placement points.","غرف حيّة ولوحة نقاط واحدة للسهرة كلها، مع وضع بطولات ونقاط حسب المركز.","Live-Runden mit einer Punktetafel für den ganzen Abend, dazu ein Turniermodus mit Platzierungspunkten."),
 ("proj.cc.p2","Three languages: English, Arabic (Egyptian and Standard, full RTL) and German.","ثلاث لغات: الإنجليزية، والعربية (مصري وفصحى، بدعم RTL كامل)، والألمانية.","Drei Sprachen: Englisch, Arabisch (Ägyptisch und Standard, volles RTL) und Deutsch."),
 ("proj.cc.p3","Guests join by code with no account and play in seconds.","الضيوف يدخلون بالرمز من غير حساب ويلعبون في ثوانٍ.","Gäste kommen per Code ohne Konto dazu und spielen in Sekunden."),
 ("proj.cc.p4","Built end to end: front end, API, database, realtime rooms and deploy.","بنيته من الألف إلى الياء: الواجهة، والـAPI، وقاعدة البيانات، وغرف الريل تايم، والنشر.","Ende zu Ende gebaut: Frontend, API, Datenbank, Echtzeit-Räume und Deployment."),
 ("proj.play","Play ChanceClub","العب ChanceClub","ChanceClub spielen"),
 ("proj.source","source","الكود","Quellcode"),
 ("proj.pf.p1","Three locales, English, Arabic and German, with a full right-to-left layout for Arabic.","ثلاث لغات: الإنجليزية والعربية والألمانية، مع تخطيط كامل من اليمين إلى اليسار للعربية.","Drei Sprachen, Englisch, Arabisch und Deutsch, mit vollständigem Rechts-nach-links-Layout für Arabisch."),
 ("proj.pf.p2","A scroll-snap projects carousel driven by drag, arrows or keyboard, which mirrors itself in Arabic.","شريط مشاريع يعمل بالسحب أو بالأسهم أو بلوحة المفاتيح، وينعكس اتجاهه تلقائياً في العربية.","Ein Projekte-Karussell mit Scroll-Snap, bedienbar per Ziehen, Pfeilen oder Tastatur, das sich im Arabischen spiegelt."),
 ("proj.pf.p3","Print and no-JS fallbacks, so every section still shows up when the page is printed or scripting is off.","بدائل للطباعة ولحالة تعطّل JavaScript، فتظهر كل الأقسام عند الطباعة أو عند إيقاف السكربتات.","Fallbacks für Druck und für abgeschaltetes JavaScript, damit auch dann alle Abschnitte sichtbar bleiben."),
 ("proj.opensource","Open source","مفتوح المصدر","Open Source"),
 ("proj.aion.body","A local-first AI workspace that connects your devices, projects, files and AI tools in one place. Built for privacy and control: it runs on your own machines instead of handing everything to a cloud account.","مساحة عمل للذكاء الاصطناعي تعمل محلياً أولاً، تربط أجهزتك ومشاريعك وملفاتك وأدوات الذكاء الاصطناعي في مكان واحد. مبنية للخصوصية والتحكم: تعمل على أجهزتك بدل تسليم كل شيء إلى حساب سحابي.","Ein local-first KI-Arbeitsbereich, der Geräte, Projekte, Dateien und KI-Werkzeuge an einem Ort verbindet. Gebaut für Datenschutz und Kontrolle: läuft auf deinen eigenen Rechnern, statt alles an ein Cloud-Konto zu geben."),
 ("proj.localFirst","Local-first","محلي أولاً","Local-first"),
 ("proj.thisSite","This site","هذا الموقع","Diese Seite"),
 ("proj.pf.title","Portfolio","الموقع الشخصي","Portfolio"),
 ("proj.pf.body","The page you are reading. Hand-written HTML, CSS and vanilla JavaScript with no framework and no build step, kept small enough to load instantly on a phone.","الصفحة التي تقرأها الآن. HTML وCSS وJavaScript مكتوبة يدوياً، بلا إطار عمل وبلا خطوة بناء، وصغيرة بما يكفي لتفتح فوراً على الهاتف.","Die Seite, die du gerade liest. Handgeschriebenes HTML, CSS und Vanilla JavaScript, ohne Framework und ohne Build-Schritt, klein genug, um auf dem Handy sofort zu laden."),
 ("proj.noBuild","No build step","بلا خطوة بناء","Kein Build-Schritt"),
 ("exp.title","Experience","الخبرة","Erfahrung"),
 ("exp.present","Aug 2026 - Present","أغسطس 2026 - الآن","Aug 2026 - heute"),
 ("exp.r1","Junior Software Developer &amp; Graphic Designer","مطوّر برمجيات مبتدئ ومصمّم جرافيك","Junior Software Developer &amp; Grafikdesigner"),
 ("exp.r1.body","Full-stack development across front-end (HTML, CSS, JavaScript, TypeScript, React.js) and back-end (PHP, OOP), React Native mobile features, and design assets in Photoshop and Illustrator.","تطوير متكامل للواجهة الأمامية (HTML، CSS، JavaScript، TypeScript، React.js) والخلفية (PHP، OOP)، وميزات موبايل بـ React Native، وتصميم أصول بصرية بـ Photoshop وIllustrator.","Full-Stack-Entwicklung im Frontend (HTML, CSS, JavaScript, TypeScript, React.js) und Backend (PHP, OOP), React-Native-Features und Design-Assets in Photoshop und Illustrator."),
 ("exp.r2","English Assistant (OL English IGCSE)","مساعد لغة إنجليزية (IGCSE)","Englisch-Assistenz (IGCSE)"),
 ("exp.r2.body","Attendance and academic records for a cohort of 78 students, digitized handwritten logs and grade sheets with advanced spreadsheet work, and real-time administrative support during lessons.","الحضور والسجلات الأكاديمية لمجموعة من 78 طالباً، ورقمنة السجلات اليدوية وكشوف الدرجات بجداول بيانات متقدمة، ودعم إداري فوري أثناء الحصص.","Anwesenheit und akademische Unterlagen für eine Gruppe von 78 Schülern, Digitalisierung handschriftlicher Listen und Notenbögen mit fortgeschrittenen Tabellen, dazu administrative Soforthilfe im Unterricht."),
 ("exp.r3","Marketing Manager &amp; Specialist","مدير وأخصائي تسويق","Marketingmanager &amp; Spezialist"),
 ("exp.r3.body","Professional communication with leads, analysis of customer needs and local community trends, and streamlined digital workflows for academy members.","تواصل احترافي مع العملاء المحتملين، وتحليل احتياجاتهم واتجاهات المجتمع المحلي، وتبسيط سير العمل الرقمي لأعضاء الأكاديمية.","Professionelle Kommunikation mit Interessenten, Analyse von Kundenbedürfnissen und lokalen Trends, und verschlankte digitale Abläufe für die Mitglieder der Akademie."),
 ("exp.r4","Design &amp; Marketing Specialist","أخصائي تصميم وتسويق","Design- &amp; Marketing-Spezialist"),
 ("exp.r4.body","Promotional design and visual content that grew enrollment, social media management, and coordinated marketing campaigns reaching new students and parents.","تصميم ومحتوى بصري دعائي زاد التسجيل، وإدارة وسائل التواصل، وتنسيق حملات تسويقية وصلت إلى طلاب وأولياء أمور جدد.","Werbedesign und visuelle Inhalte, die die Anmeldungen steigerten, Social-Media-Betreuung und koordinierte Kampagnen, die neue Schüler und Eltern erreichten."),
 ("sk.title","Toolbox","الأدوات","Werkzeugkasten"),
 ("sk.languages","languages","اللغات","Sprachen"),
 ("sk.frameworks","frameworks","أطر العمل","Frameworks"),
 ("sk.development","development","التطوير","Entwicklung"),
 ("sk.design","design","التصميم","Design"),
 ("sk.fullstack","Full-stack","متكامل","Full-Stack"),
 ("sk.responsive","Responsive design","تصميم متجاوب","Responsives Design"),
 ("sk.troubleshooting","Troubleshooting","حل المشكلات","Fehlersuche"),
 ("sk.brand","Brand &amp; promo content","هوية ومحتوى دعائي","Marken- &amp; Werbeinhalte"),
 ("about.title","About","نبذة عني","Über mich"),
 ("about.lede","I'm Abdulaziz, a junior software developer and graphic designer based in Cairo, Egypt.","أنا عبدالعزيز، مطوّر برمجيات مبتدئ ومصمّم جرافيك مقيم في القاهرة، مصر.","Ich bin Abdulaziz, Junior Software Developer und Grafikdesigner in Kairo, Ägypten."),
 ("about.p1","By day I work across the stack at Digi-Sail, building web and mobile products and designing the visuals that go with them. Before code, I spent two years on marketing and design for two sports academies, and a year keeping academic operations running for a 78-student IGCSE English program.","أعمل نهاراً عبر الطبقات كلها في Digi-Sail، أبني منتجات ويب وموبايل وأصمّم الشكل البصري الذي يرافقها. قبل البرمجة، أمضيت عامين في التسويق والتصميم لأكاديميتين رياضيتين، وعاماً أدير فيه العمليات الأكاديمية لبرنامج إنجليزي لـ78 طالباً.","Tagsüber arbeite ich bei Digi-Sail über den ganzen Stack, baue Web- und Mobile-Produkte und gestalte die Visuals dazu. Vor dem Code war ich zwei Jahre in Marketing und Design für zwei Sportakademien und ein Jahr in der akademischen Organisation eines Englischprogramms mit 78 Schülern."),
 ("about.p2","I'm finishing my IGCSEs (8 O-Levels plus A-Level Computer Science) in 2027, fluent in Arabic and English, and currently teaching myself German.","أنهي شهادات IGCSE (ثماني مواد O-Level إضافة إلى A-Level في علوم الحاسوب) في 2027، وأتحدث العربية والإنجليزية بطلاقة، وأتعلّم الألمانية حالياً بنفسي.","Ich schließe 2027 meine IGCSEs ab (acht O-Levels plus A-Level Computer Science), spreche fließend Arabisch und Englisch und bringe mir gerade selbst Deutsch bei."),
 ("about.f1","location","الموقع","Standort"),
 ("about.f1v","Cairo, Egypt","القاهرة، مصر","Kairo, Ägypten"),
 ("about.f2v","Arabic (native), English (fluent), German (learning)","العربية (لغة أم)، الإنجليزية (بطلاقة)، الألمانية (قيد التعلّم)","Arabisch (Muttersprache), Englisch (fließend), Deutsch (lernend)"),
 ("about.f3","focus","التركيز","Fokus"),
 ("about.f3v","Full-stack web, mobile, design","ويب متكامل، موبايل، تصميم","Full-Stack-Web, Mobile, Design"),
 ("aus.title","Apprenticeship 2027","التدريب المهني 2027","Ausbildung 2027"),
 ("aus.lede","I am applying for an apprenticeship as Fachinformatiker für Anwendungsentwicklung, starting October 2027.","أتقدّم لتدريب مهني كـ \u2066Fachinformatiker für Anwendungsentwicklung\u2069 (تطوير التطبيقات)، بدءاً من أكتوبر 2027.","Ich suche eine Ausbildung als Fachinformatiker für Anwendungsentwicklung, Start Oktober 2027."),
 ("aus.p1","I live in Cairo and have worked as a junior software developer at Digi-Sail since August 2026, building web and mobile applications with React, TypeScript and PHP. I learn best when something actually runs at the end: ChanceClub above is mine, from the database to the layout.","أعيش في القاهرة وأعمل مطوّر برمجيات مبتدئاً في Digi-Sail منذ أغسطس 2026، أبني تطبيقات ويب وموبايل بـ React وTypeScript وPHP. أتعلّم أفضل حين يعمل شيء في النهاية فعلاً: ChanceClub أعلاه من عملي، من قاعدة البيانات إلى التصميم.","Ich lebe in Kairo und arbeite seit August 2026 als Junior Software Developer bei Digi-Sail. Dort baue ich Web- und Mobile-Anwendungen mit React, TypeScript und PHP. Am besten lerne ich, wenn am Ende etwas läuft: ChanceClub oben ist von mir, von der Datenbank bis zum Layout."),
 ("aus.p2","I am learning German on my own and aim for B1 by mid-2027. I can relocate to North Rhine-Westphalia and start there in October 2027. My CV is available in German and English.","أتعلّم الألمانية بنفسي وأستهدف مستوى B1 بحلول منتصف 2027. أستطيع الانتقال إلى شمال الراين-وستفاليا والبدء هناك في أكتوبر 2027. سيرتي الذاتية متاحة بالألمانية والإنجليزية.","Ich lerne Deutsch im Selbststudium und will bis Mitte 2027 Niveau B1 erreichen. Ich kann nach Nordrhein-Westfalen ziehen und dort im Oktober 2027 anfangen. Lebenslauf gibt es auf Deutsch und Englisch."),
 ("aus.fZiel","Target","الهدف","Ziel"),
 ("aus.fZielV","Fachinformatiker für Anwendungsentwicklung","Fachinformatiker für Anwendungsentwicklung (تطوير التطبيقات)","Fachinformatiker für Anwendungsentwicklung"),
 ("aus.fStart","Start","البداية","Start"),
 ("aus.fStartV","October 2027","أكتوبر 2027","Oktober 2027"),
 ("aus.fOrt","Location","المكان","Ort"),
 ("aus.fOrtV","North Rhine-Westphalia, ready to move","شمال الراين-وستفاليا، مستعد للانتقال","Nordrhein-Westfalen, umzugsbereit"),
 ("aus.fDe","German","الألمانية","Deutsch"),
 ("aus.fDeV","Self-study, B1 target by mid-2027","دراسة ذاتية، هدف B1 بحلول منتصف 2027","Selbststudium, Ziel B1 bis Mitte 2027"),
 ("aus.fEn","English","الإنجليزية","Englisch"),
 ("aus.fEnV","Fluent","بطلاقة","fließend"),
 ("aus.fAr","Arabic","العربية","Arabisch"),
 ("aus.fArV","Native","لغة أم","Muttersprache"),
 ("aus.fEdu","Education","التعليم","Abschluss"),
 ("aus.fEduV","IGCSE 2027: 8 O-Levels and A-Level Computer Science","IGCSE 2027: ثماني مواد O-Level وA-Level في علوم الحاسوب","IGCSE 2027: 8 O-Levels und A-Level Computer Science"),
 ("aus.fExp","Experience","الخبرة","Erfahrung"),
 ("aus.fExpV","Junior Software Developer at Digi-Sail since August 2026","مطوّر برمجيات مبتدئ في Digi-Sail منذ أغسطس 2026","Junior Software Developer bei Digi-Sail seit August 2026"),
 ("ct.eyebrow","// 07, say hello","// 07، قل مرحباً","// 07, sag hallo"),
 ("ct.cv","Download CV","حمّل السيرة الذاتية","Lebenslauf laden"),
 ("ct.also","also:","أيضاً:","außerdem:"),
 ("footer","&copy; 2026 Abdulaziz Awal. Hand-coded with HTML, CSS &amp; vanilla JS.","&copy; 2026 عبدالعزيز عوض. مكتوب يدوياً بـ HTML وCSS وJavaScript.","&copy; 2026 Abdulaziz Awal. Von Hand geschrieben mit HTML, CSS und Vanilla JS."),
]

# english values are the source text itself
en = {k: s for (k, s, a, d) in T}
ar = {k: a for (k, s, a, d) in T}
de = {k: d for (k, s, a, d) in T}

missing = []
for (k, s, a, d) in T:
    pat = re.compile(r'>(\s*)' + r'\s+'.join(re.escape(w) for w in s.split()) + r'(\s*)<')
    n = len(pat.findall(html))
    if n == 0:
        missing.append((k, s[:50]))
        continue
    def repl(m, key=k, text=s):
        start = m.start()
        # is the tag that owns this text a closing tag?
        lt = html.rfind('<', 0, start + 1)
        if 'data-i18n' in html[lt:start + 1]:
            return m.group(0)
        closing = html[lt:lt + 2] == '</'
        if closing:
            return '><span data-i18n="%s">%s%s%s</span><' % (key, m.group(1), text, m.group(2))
        return ' data-i18n="%s">%s%s%s<' % (key, m.group(1), text, m.group(2))
    html = pat.sub(repl, html)

# html-mode blocks
html = html.replace('<p class="hero-sub reveal">', '<p class="hero-sub reveal" data-i18n-html="hero.sub">')
html = html.replace('<h2 class="contact-title reveal">', '<h2 class="contact-title reveal" data-i18n-html="ct.title">')

en['hero.sub'] = 'I build full-stack web and mobile products, and design the visuals that ship with them. Based in Cairo, building at <a href="https://digi-sail.com" target="_blank" rel="noopener" data-hover>Digi-Sail</a>.'
ar['hero.sub'] = 'أبني منتجات ويب وموبايل متكاملة، وأصمّم الهوية البصرية التي تُشحن معها. مقرّي القاهرة، وأعمل في <a href="https://digi-sail.com" target="_blank" rel="noopener" data-hover>Digi-Sail</a>.'
de['hero.sub'] = 'Ich baue Full-Stack-Web- und Mobile-Produkte und gestalte die Visuals, die mit ihnen ausgeliefert werden. Ich lebe in Kairo und arbeite bei <a href="https://digi-sail.com" target="_blank" rel="noopener" data-hover>Digi-Sail</a>.'
en['ct.title'] = "Let's build something<br /><span class=\"accent-outline\">worth scrolling.</span>"
ar['ct.title'] = 'لنبنِ شيئاً<br /><span class="accent-outline">يستحق التمرير.</span>'
de['ct.title'] = 'Lass uns etwas bauen,<br /><span class="accent-outline">das sich zu scrollen lohnt.</span>'

open(P, 'w', encoding='utf-8').write(html)

out = io.StringIO()
out.write("/* aawal portfolio: translations. The English markup in index.html is the source of truth;\n   switching a language rewrites every [data-i18n] node from this table. */\n")
out.write("window.AAWAL_I18N = {\n")
for name, d in (("en", en), ("ar", ar), ("de", de)):
    out.write('  %s: %s,\n' % (name, json.dumps(d, ensure_ascii=False, indent=2).replace('\n', '\n  ')))
out.write("};\n\nwindow.AAWAL_ROLES = {\n")
out.write('  en: ["Junior Software Developer", "Graphic Designer", "Full-Stack Web Developer", "React Native Developer"],\n')
out.write('  ar: ["مطوّر برمجيات مبتدئ", "مصمّم جرافيك", "مطوّر ويب متكامل", "مطوّر React Native"],\n')
out.write('  de: ["Junior Software Developer", "Grafikdesigner", "Full-Stack-Webentwickler", "React-Native-Entwickler"]\n};\n')
open('/home/sandbox/work/portfolio/js/i18n.js', 'w', encoding='utf-8').write(out.getvalue())

print('annotated keys:', len(T), 'missing:', missing)
print('data-i18n count:', html.count('data-i18n'))
