# Maakt het bouwbestand voor de e-learning "Onderwijs opnieuw ontwerpen met AI".
# Het resultaat (../ai-didactisch-vaardig.json) open je in de E-learning Bouwer
# (Openen) om de inhoud verder te bewerken. Daarna is dat bouwbestand de bron,
# niet dit script.
#
# Gebruik: python _bron/maak_cursus.py
import base64, json, os


def beeld(naam):
    pad = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'beeld', naam)
    with open(pad, 'rb') as f:
        return 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('ascii')

HIER = os.path.dirname(os.path.abspath(__file__))
UIT = os.path.join(HIER, '..', 'ai-didactisch-vaardig.json')


def p(*alineas):
    return ''.join('<p>' + a + '</p>' for a in alineas)


def tekst(kop, *alineas):
    return {'t': 'text', 'heading': kop, 'body': p(*alineas)}


def lijst(items, geordend=False):
    return {'t': 'list', 'ordered': geordend, 'items': ['<p>' + i + '</p>' for i in items]}


def notitie(soort, body, titel=''):
    b = {'t': 'note', 'soort': soort, 'body': p(body) if not body.startswith('<') else body}
    if titel:
        b['title'] = titel
    return b


def plaatshouder(wat):
    return notitie('info', '<p><strong>Plaatshouder.</strong> ' + wat + '</p>', 'Nog invullen')


def doorgaan():
    return {'t': 'continue'}


def quiz(vraag, opties, multi=False):
    return {'t': 'quiz', 'multi': multi, 'question': vraag,
            'options': [{'text': t, 'correct': c, 'feedback': f} for t, c, f in opties]}


def open_vraag(vraag, hint='', voorbeeld=''):
    b = {'t': 'open', 'question': p(vraag), 'hint': hint}
    if voorbeeld:
        b['feedback'] = voorbeeld
    return b


def leerdoelen(*doelen):
    return [{'t': 'text', 'heading': 'Na deze module kun je',
             'body': '<ol>' + ''.join('<li>' + d + '</li>' for d in doelen) + '</ol>'}]


def competentie(nummers, minimum):
    return notitie('info', '<p><strong>Competentie ' + nummers + '.</strong> Aantoonbaar minimum: ' + minimum + '</p>',
                   'Koppeling met het competentieraamwerk')


# ------------------------------------------------------------------ schema's

SVG_LUS = '''<svg viewBox="0 0 640 220" xmlns="http://www.w3.org/2000/svg" font-family="inherit">
<defs><marker id="pijl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--go-groen-donker)"/></marker></defs>
<rect x="20" y="60" width="170" height="100" rx="14" fill="var(--go-groen-licht)" stroke="var(--go-groen)" stroke-width="2"/>
<text x="105" y="100" text-anchor="middle" font-size="20" font-weight="700" fill="var(--go-tekst)">1. Eerst zelf</text>
<text x="105" y="128" text-anchor="middle" font-size="14" fill="var(--go-tekst)">denken, weten, vragen</text>
<rect x="235" y="60" width="170" height="100" rx="14" fill="var(--go-kaart)" stroke="var(--go-rand)" stroke-width="2"/>
<text x="320" y="100" text-anchor="middle" font-size="20" font-weight="700" fill="var(--go-tekst)">2. Dan AI</text>
<text x="320" y="128" text-anchor="middle" font-size="14" fill="var(--go-tekst)">zoeken, maken, sparren</text>
<rect x="450" y="60" width="170" height="100" rx="14" fill="var(--go-groen-licht)" stroke="var(--go-groen)" stroke-width="2"/>
<text x="535" y="100" text-anchor="middle" font-size="20" font-weight="700" fill="var(--go-tekst)">3. Weer zelf</text>
<text x="535" y="128" text-anchor="middle" font-size="14" fill="var(--go-tekst)">checken, kiezen, uitleggen</text>
<line x1="192" y1="110" x2="231" y2="110" stroke="var(--go-groen-donker)" stroke-width="2.5" marker-end="url(#pijl)"/>
<line x1="407" y1="110" x2="446" y2="110" stroke="var(--go-groen-donker)" stroke-width="2.5" marker-end="url(#pijl)"/>
<path d="M535 162 C535 210 105 210 105 166" fill="none" stroke="var(--go-groen-donker)" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#pijl)"/>
<text x="320" y="204" text-anchor="middle" font-size="13" fill="var(--go-tekst)">verfijn en herhaal</text>
<text x="320" y="34" text-anchor="middle" font-size="15" font-weight="700" fill="var(--go-groen-donker)">Het denkwerk blijft bij de student</text>
</svg>'''

SVG_LAGEN = '''<svg viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg" font-family="inherit">
<rect x="20" y="170" width="600" height="60" rx="12" fill="var(--go-groen-licht)" stroke="var(--go-groen)" stroke-width="2"/>
<text x="40" y="198" font-size="18" font-weight="700" fill="var(--go-tekst)">AI-vaardig</text>
<text x="40" y="219" font-size="13" fill="var(--go-tekst)">Competenties 1 tot en met 4: begrijpen, gebruiken, controleren, verantwoord omgaan</text>
<rect x="70" y="95" width="500" height="60" rx="12" fill="var(--go-groen-medium)" stroke="var(--go-groen)" stroke-width="2"/>
<text x="90" y="123" font-size="18" font-weight="700" fill="var(--go-tekst)">AI-didactisch vaardig</text>
<text x="90" y="144" font-size="13" fill="var(--go-tekst)">Competenties 5 tot en met 7: ontwerpen, toetsen, begeleiden</text>
<rect x="120" y="20" width="400" height="60" rx="12" fill="var(--go-groen)" stroke="var(--go-groen-donker)" stroke-width="2"/>
<text x="140" y="48" font-size="18" font-weight="700" fill="var(--go-kaart)">Onderwijs opnieuw ontwerpen</text>
<text x="140" y="69" font-size="13" fill="var(--go-kaart)">Competentie 8: blijven leren, samen herontwerpen</text>
</svg>'''


# ------------------------------------------------------------------ modules

m0 = {'id': 'm0', 'title': 'Start: waarom deze e-learning?', 'deadline': '', 'blocks': [
    tekst('Welkom',
          'Bijna alle studenten gebruiken generatieve AI. Dat verandert wat een opdracht, een toets en een begeleidingsgesprek eigenlijk meten. Deze e-learning helpt je om AI niet alleen te <strong>bedienen</strong>, maar om je onderwijs er <strong>bewust op te ontwerpen</strong>.',
          'Het doel is niet dat je meer AI gaat gebruiken. Het doel is dat je AI-gebruik kunt <em>uitleggen, beoordelen, begrenzen en onderwijskundig verantwoorden</em>, ook als je kiest voor weinig of geen AI.'),
    {'t': 'svg', 'svg': SVG_LAGEN, 'alt': 'Drie lagen: AI-vaardig als fundament, daarop AI-didactisch vaardig, bovenaan onderwijs opnieuw ontwerpen.',
     'caption': 'De opbouw van deze e-learning: drie lagen, acht competenties.'},
    quiz('Schat eens: welk deel van de studenten gebruikt generatieve AI, volgens een grote Britse enquête uit 2026?', [
        ('Ongeveer de helft', False, 'Hoger. Volgens HEPI 2026 gebruikt 95% van de studenten AI. Kijk naar de grafiek hieronder.'),
        ('Ongeveer driekwart', False, 'Nog hoger. Volgens HEPI 2026 gebruikt 95% van de studenten AI. Kijk naar de grafiek hieronder.'),
        ('Bijna iedereen', True, 'Klopt: 95% volgens HEPI 2026. Kijk ook naar het tweede cijfer: maar 29% vindt docenten voorbereid.'),
    ]),
    {'t': 'chart', 'soort': 'staaf', 'title': 'Studenten en AI (Engelse en internationale enquêtes, 2026)', 'unit': '%', 'items': [
        {'label': 'Gebruikt AI (HEPI 2026)', 'value': 95},
        {'label': 'Gebruikt AI (DEC 2026)', 'value': 88},
        {'label': 'Vindt docenten voorbereid (DEC 2026)', 'value': 29},
        {'label': 'Plakt AI-tekst in beoordeeld werk (HEPI 2026)', 'value': 12},
    ]},
    notitie('let', 'Enquêtes meten wat studenten zeggen. Ze meten niet wat studenten leren. De cijfers laten zien dat AI er is, niet of het helpt. Daarover gaat module 4.'),
    doorgaan(),
    tekst('Hoe deze e-learning werkt',
          'Elke module volgt dezelfde lijn: je krijgt uitleg, ziet een voorbeeld, oefent meteen en past het toe op je eigen onderwijs. Dat laatste is het belangrijkste: wie oefent, leert meer dan wie alleen kijkt of leest.',
          'Je werkt de hele e-learning aan <strong>één eigen onderwijsactiviteit</strong>: een les, opdracht of toets die je echt geeft. Aan het eind heb je die herontworpen en verantwoord.'),
    {'t': 'steps', 'intro': {'title': 'De leerroute', 'body': 'Tien modules in drie lagen. Reken op ongeveer twaalf uur, inclusief praktijk.'},
     'steps': [
         {'title': 'Laag 1: AI-vaardig (modules 1 tot en met 3)', 'body': 'Begrijpen wat AI doet, doelgericht gebruiken, output controleren en verantwoord omgaan met gegevens.'},
         {'title': 'Laag 2: AI-didactisch vaardig (modules 4 tot en met 8)', 'body': 'Wat het onderzoek zegt, leeractiviteiten ontwerpen, de placemat-methode, toetsen en begeleiden.'},
         {'title': 'Laag 3: onderwijs opnieuw ontwerpen (module 9)', 'body': 'Je eigen herontwerp afronden, laten beoordelen door een collega en een plan om bij te blijven.'},
     ],
     'summary': {'title': 'Samen, niet alleen', 'body': 'Je volgt de e-learning het liefst in een groep collega\'s, met een gezamenlijk moment per twee weken en feedback van een collega op je praktijkopdrachten.'}},
    plaatshouder('Kennisclip van maximaal zes minuten: "Waarom dit nu?" Bijvoorbeeld een docent en een student over hoe AI een bestaande opdracht veranderde.'),
    doorgaan(),
    tekst('Instapopdracht: kies je eigen onderwijsactiviteit', 'Kies een les, opdracht of toets die je dit jaar geeft en die je wilt herontwerpen. Kies iets kleins en concreets: één opdracht, niet een heel vak.'),
    open_vraag('Welke onderwijsactiviteit neem je mee door deze e-learning? Beschrijf in een paar zinnen wat studenten nu doen, wat ze ervan moeten leren en wat je erin opvalt sinds studenten AI gebruiken.',
               'Bijvoorbeeld: "Verslag over een bedrijfscasus in jaar 2. Ze moeten leren een probleem te analyseren. Sinds dit jaar zijn de verslagen opvallend goed geschreven, maar in de bespreking kunnen ze hun keuzes slecht uitleggen."'),
    open_vraag('Zelfscan: hoe zeker voel je je nu over AI in je onderwijs? Noem één ding dat je al goed kunt en één ding waar je tegen opziet.', 'Je vergelijkt dit aan het eind met waar je dan staat.'),
]}

m1 = {'id': 'm1', 'title': '1. AI begrijpen en bewust kiezen', 'deadline': '', 'blocks': [
    *leerdoelen('in gewone taal uitleggen waarom een overtuigend AI-antwoord geen bewijs van juistheid is;',
                'het verschil benoemen tussen genereren, zoeken in bronnen en redeneren controleren;',
                'voor een onderwijstaak kiezen tussen AI gebruiken, beperkt gebruiken of geen AI.'),
    doorgaan(),
    tekst('Wat een taalmodel eigenlijk doet',
          'Een generatief taalmodel voorspelt welke tekst waarschijnlijk volgt op jouw vraag. Het is getraind om <strong>plausibel</strong> te klinken, niet om <strong>waar</strong> te zijn. Meestal valt dat samen, maar niet altijd.',
          'Daarom kan een model met dezelfde stelligheid een correcte uitleg geven als een verzonnen bron. Jouw vakkennis blijft nodig om te zien welke van de twee je voor je hebt.'),
    {'t': 'cards', 'items': [
        {'front': '<p><strong>Genereren</strong></p>', 'back': '<p>Het model maakt nieuwe tekst op basis van patronen. Handig voor concepten, voorbeelden en variaties. Niet hetzelfde als opzoeken.</p>'},
        {'front': '<p><strong>Zoeken in bronnen</strong></p>', 'back': '<p>Sommige tools zoeken op het web of in je documenten en noemen bronnen. Een genoemde bron is pas betrouwbaar als je hem zelf opent en hij zegt wat er beweerd wordt.</p>'},
        {'front': '<p><strong>Redeneren controleren</strong></p>', 'back': '<p>AI kan een redenering laten zien, maar of die klopt beoordeel jij. Een stap-voor-stap-uitleg ziet er grondig uit, ook als een stap niet klopt.</p>'},
        {'front': '<p><strong>Hallucinatie</strong></p>', 'back': '<p>Inhoud die plausibel klinkt maar niet klopt, zoals een niet-bestaand artikel of een verzonnen cijfer.</p>'},
        {'front': '<p><strong>Agent</strong></p>', 'back': '<p>AI die zelfstandig meerdere stappen uitvoert, zoals documenten combineren of iets inleveren. Hoe meer een systeem zelf doet, hoe belangrijker afbakening en tussencontroles worden.</p>'},
    ]},
    quiz('Een collega vraagt een chatbot om drie wetenschappelijke bronnen over feedback in het hbo. Ze krijgt drie keurige APA-verwijzingen met DOI. Wat is de beste volgende stap?', [
        ('Ze gebruikt ze: de DOI\'s laten zien dat het echte artikelen zijn.', False, 'Een DOI kan net zo goed verzonnen zijn als de titel. Het model maakt de vorm van een bronverwijzing na, ook als de bron niet bestaat.'),
        ('Ze opent elke bron zelf en controleert of die bestaat en zegt wat beweerd wordt.', True, 'Precies. Een getoonde bron wordt afzonderlijk geopend en gecontroleerd. Pas dan weet je of hij bestaat én of hij de claim ondersteunt.'),
        ('Ze vraagt de chatbot of de bronnen echt bestaan.', False, 'Het model kan met dezelfde stelligheid bevestigen dat een verzonnen bron bestaat. Controleren doe je buiten het model, in de bron zelf.'),
    ]),
    doorgaan(),
    tekst('Gebruiken, beperkt gebruiken of geen AI',
          'Een goede AI-keuze begint niet bij de tool, maar bij de taak. Vraag je eerst af: <em>welk denkwerk moet de student (of ik) hier zelf doen?</em> Afzien van AI is ook een verdedigbare keuze, zolang je kunt uitleggen waarom.'),
    {'t': 'table', 'kop': True, 'zijkop': True, 'caption': 'Een eerste afweging per taak', 'rows': [
        ['Keuze', 'Wanneer', 'Voorbeeld'],
        ['AI gebruiken', 'De taak is ondersteunend en jij kunt de kwaliteit goed beoordelen.', 'Tien variaties op een oefencasus maken, die je daarna zelf controleert.'],
        ['Beperkt gebruiken', 'AI helpt, maar een deel van het denkwerk moet bij de student blijven.', 'Studenten schrijven eerst zelf een analyse en vragen daarna AI om tegenargumenten.'],
        ['Geen AI', 'Het denkwerk ís het leerdoel, of er zijn gegevens in het spel die niet in een AI-tool mogen.', 'Een eerste eigen probleemanalyse; feedback op een vertrouwelijk stageverslag.'],
    ]},
    {'t': 'sort', 'question': 'Sorteer deze docenttaken. Wat zou jij kiezen?', 'piles': ['AI gebruiken', 'Beperkt gebruiken', 'Geen AI'],
     'items': [
         {'text': 'Een concept-rubric opstellen die je daarna met collega\'s aanscherpt', 'pile': 0},
         {'text': 'Een studentverslag met naam en cijferlijst laten samenvatten in een gratis chatbot', 'pile': 2},
         {'text': 'Studenten laten oefenen met een AI-gesprekspartner, nadat ze eerst zelf een standpunt hebben geformuleerd', 'pile': 1},
         {'text': 'Meerkeuze-afleiders laten bedenken voor een oefentoets', 'pile': 0},
         {'text': 'Het eindoordeel over een afstudeerwerk', 'pile': 2},
     ],
     'feedback': 'Goed gesorteerd. Merk op dat het niet om de tool gaat, maar om wie het denkwerk doet en welke gegevens erin gaan.',
     'feedbackWrong': 'Kijk per taak naar twee dingen: wie moet hier het denkwerk doen, en zitten er persoons- of vertrouwelijke gegevens in? Het eindoordeel blijft altijd bij een mens.'},
    doorgaan(),
    notitie('opdracht', '<p><strong>Praktijk (20 minuten).</strong> Stel een AI-tool twee vakvragen uit je eigen onderwijs: één die je zelf makkelijk kunt beoordelen en één waarover je twijfelt. Vergelijk de antwoorden met je eigen lesmateriaal.</p>'),
    open_vraag('Wat was bruikbaar, wat bleef onzeker en wat zou je níet gebruiken? Kies voor je eigen onderwijsactiviteit (uit de start) tussen gebruiken, beperkt gebruiken of geen AI, en leg uit waarom.',
               'Noem minstens twee beperkingen die je zag.'),
    competentie('1 en 2', 'je verklaart bij twee voorbeelden waarom een overtuigend antwoord geen bewijs van juistheid is, en kiest met reden voor gebruik, beperkt gebruik of geen AI.'),
]}

m2 = {'id': 'm2', 'title': '2. Instructies geven en resultaten controleren', 'deadline': '', 'blocks': [
    *leerdoelen('een prompt opbouwen uit rol, context, opdracht en output;',
                'een resultaat in twee rondes verbeteren en vastleggen wat je zelf aanpaste;',
                'fouten en verzonnen bronnen in AI-output opsporen en corrigeren.'),
    doorgaan(),
    tekst('Een prompt heeft vier delen',
          'Hoe meer context de AI krijgt, hoe gerichter het resultaat. Zonder context krijg je een algemeen verhaal dat bij elke opdracht past. Het context-deel is bijna altijd te kort.'),
    {'t': 'tabs', 'items': [
        {'title': 'Rol', 'body': p('Wie moet de AI zijn? <em>Je bent een onderwijsontwerper die korte oefencasussen maakt voor tweedejaars hbo-studenten bedrijfskunde.</em>')},
        {'title': 'Context', 'body': p('Alles wat de AI moet weten: doelgroep, leerdoel, wat studenten al kennen, je eigen bronmateriaal. Hier zit het meeste werk, en dat werk doe jij vooraf zelf.')},
        {'title': 'Opdracht', 'body': p('Wat moet er precies gebeuren? Eén duidelijke taak, met criteria. <em>Maak drie casussen van maximaal 150 woorden, elk met een ander dilemma.</em>')},
        {'title': 'Output', 'body': p('In welke vorm? <em>Als genummerde lijst in platte tekst. Verzin geen cijfers; gebruik alleen mijn bronmateriaal.</em>')},
    ]},
    {'t': 'match', 'question': 'Welk deel van de prompt is dit?', 'pairs': [
        {'left': '"Je bent een ervaren docent verpleegkunde."', 'right': 'Rol'},
        {'left': '"De studenten zitten in jaar 1 en kennen het begrip klinisch redeneren nog niet."', 'right': 'Context'},
        {'left': '"Schrijf vijf toetsvragen over het leerdoel hieronder."', 'right': 'Opdracht'},
        {'left': '"Geef een tabel met vraag, juist antwoord en de denkfout achter elke afleider."', 'right': 'Output'},
    ], 'feedback': 'Goed. Merk op dat de context het enige deel is waarvoor je zelf moet nadenken over je studenten.',
     'feedbackWrong': 'Rol is wie de AI is, context is wat de AI moet weten, opdracht is wat er moet gebeuren en output is de vorm.'},
    doorgaan(),
    tekst('Verfijnen: één ding per ronde',
          'Het eerste resultaat is een concept. Verbeter het in rondes, en verander per ronde één ding. Zo zie je wat effect heeft. Leg vast wat de AI deed en wat jij zelf aanpaste: dat is je verantwoording.',
          'Loop je na twee rondes nog vast? Dan zit het probleem meestal niet in de prompt, maar in je eigen voorwerk: je doel of context is nog niet scherp.'),
    notitie('tip', '<p><strong>De metaprompt.</strong> Laat de AI jou eerst vragen stellen voordat die iets maakt: <em>"Ik wil een [product] maken over [onderwerp] voor [doelgroep]. Hieronder staat wat ik al heb bedacht. Stel me eerst vragen, één voor één. Begin pas met maken als ik START typ."</em> Gebruik dit pas als je zelf hebt nagedacht, niet als vervanging daarvan.</p>', 'Tip uit de AI-placemats'),
    doorgaan(),
    tekst('Controleren: de foutenjacht',
          'Hieronder staat een AI-tekst over feedback geven. Er zitten bewust fouten in. Lees hem als een kritische collega.'),
    {'t': 'quote', 'body': '"Uit de meta-analyse van Hattie (2009) blijkt dat feedback een effectgrootte van 0,73 heeft, het hoogste van alle interventies. Recent onderzoek van De Vries en Bakker (2024, Tijdschrift voor Hoger Onderwijs, 42(3)) bevestigt dat AI-feedback in het hbo even effectief is als feedback van docenten."'},
    quiz('Wat zou jij controleren voordat je deze tekst gebruikt? Kies alles wat van toepassing is.', [
        ('Of de studie van De Vries en Bakker (2024) bestaat en dit zegt.', True, 'Ja. Deze bron is voor deze oefening verzonnen. Een keurige verwijzing met jaargang en nummer zegt niets over of hij bestaat.'),
        ('Of "het hoogste van alle interventies" klopt.', True, 'Ja. Absolute claims ("het hoogste", "altijd") zijn een signaal om na te gaan. In Hatties overzichten scoren andere invloeden hoger.'),
        ('Of de tekst grammaticaal correct is.', False, 'Grammatica is zelden het probleem bij AI-tekst. De tekst is juist vlot en overtuigend, en dat maakt fouten lastig te zien.'),
        ('Of "even effectief als docenten" past bij wat het onderzoek over AI-feedback zegt.', True, 'Ja. Zo\'n algemene claim gaat verder dan het beschikbare bewijs. Effecten hangen af van taak, tool en context.'),
    ], multi=True),
    plaatshouder('Vervang dit foutvoorbeeld door een voorbeeld uit een eigen vakgebied of opleiding, met vooraf aangebrachte fouten en één niet-bestaande bron.'),
    doorgaan(),
    notitie('opdracht', '<p><strong>Praktijk (40 minuten).</strong> Laat AI voor je eigen onderwijsactiviteit een uitleg of oefencasus maken. Gebruik de vier delen. Verbeter het resultaat in twee rondes en controleer daarna elke claim.</p>'),
    open_vraag('Plak je eerste prompt, beschrijf je twee verbeterrondes en noem wat je zelf hebt aangepast of gecorrigeerd. Welke claim heb je nagetrokken, en waar?',
               'Beginversie, ronde 1, ronde 2, controle.'),
    competentie('2 en 3', 'je maakt een bruikbaar concept voor een eigen taak, documenteert twee verbeterstappen en corrigeert een voorbeeld met fouten en een niet-bestaande bron.'),
]}

m3 = {'id': 'm3', 'title': '3. Gegevens, ethiek en gelijke toegang', 'deadline': '', 'blocks': [
    *leerdoelen('persoonsgegevens en vertrouwelijk materiaal herkennen voordat het een AI-tool in gaat;',
                'bepalen wanneer je moet aanpassen, stoppen of iets moet voorleggen aan een deskundige;',
                'auteurschap, transparantie en gelijke toegang bespreken met studenten en collega\'s.'),
    doorgaan(),
    tekst('Wat mag een AI-tool in?',
          'De vuistregel van de placemats geldt ook voor docenten: <strong>geen persoonsgegevens en geen vertrouwelijke informatie in een open AI-tool.</strong> Gebruik de omgeving die je instelling heeft goedgekeurd en zet modeltraining uit waar dat kan.',
          'Let op: alleen namen weghalen maakt een tekst niet anoniem. Een stageverslag over "de enige vrouwelijke teamleider bij een kleine zorginstelling in Arnhem" is nog steeds herleidbaar.'),
    {'t': 'accordion', 'items': [
        {'title': 'Privacy en herleidbaarheid', 'body': p('Studentwerk, cijfers, gezondheidsinformatie en stageverslagen bevatten vaak persoonsgegevens. Vraag je af: kan iemand hieruit opmaken over wie het gaat? Twijfel je, leg het dan voor aan de privacy-ondersteuning van je instelling.')},
        {'title': 'Auteurschap en transparantie', 'body': p('Spreek af hoe jij en je studenten vermelden waar AI is gebruikt. Wees zelf het voorbeeld: vertel studenten waarvoor jij AI gebruikte bij het maken van het lesmateriaal.')},
        {'title': 'Gelijke toegang', 'body': p('Niet elke student heeft een betaald abonnement. Een opdracht die alleen goed te doen is met een betaalde tool, is niet eerlijk. Ontwerp zo dat een gratis of door de instelling geleverde tool volstaat.')},
        {'title': 'Afhankelijkheid van leveranciers', 'body': p('Critici wijzen op afhankelijkheid van commerciële partijen en op energiegebruik. Open alternatieven, zoals die van SURF, zijn het verkennen waard. Je onderwijs moet blijven werken als een specifieke tool wegvalt.')},
    ]},
    tekst('Waar vind je de afspraken?',
          'Bij de HAN staan het AI-kader, de AI-tools die binnen de HAN beschikbaar zijn en de ondersteuning op één pagina. Met vragen kun je terecht bij de AI-desk (ai-desk@han.nl). Werk je bij een andere instelling, zoek dan de vergelijkbare pagina op.'),
    {'t': 'links', 'items': [
        {'label': 'HAN: Onderwijs met AI', 'href': 'https://www.han.nl/onderwijsondersteuning/leren-werken-met-ict/artificial-intelligence/ai-in-je-onderwijs/'},
        {'label': 'HAN: Integraal AI-kader (pdf)', 'href': 'https://www.han.nl/onderwijsondersteuning/leren-werken-met-ict/artificial-intelligence/ai-in-je-onderwijs/Integraal-AI-kader-HAN-1.0-27062025.pdf'},
        {'label': 'HAN: AI-tools als bron vermelden (APA)', 'href': 'https://www.han.nl/artikelen/2024/10/apa-bronnenlijst-ai-tools/'},
    ]},
    doorgaan(),
    {'t': 'scenario', 'persoon': 'Sanne', 'rol': 'Collega-docent, tweedejaars', 'intro': p('Sanne heeft het druk met nakijken en wil AI inzetten. Help haar een verantwoorde keuze te maken.'),
     'scenes': [
         {'id': 's1', 'text': 'Ik heb 60 stageverslagen liggen. Ik wil ze in ChatGPT plakken voor een eerste feedbackronde. Ik haal de namen eruit, dus dat is toch prima?',
          'choices': [
              {'text': 'Ja, zonder namen zijn ze anoniem.', 'reactie': 'Fijn, dan begin ik meteen.', 'uitleg': 'Niet zo snel. Stageverslagen bevatten vaak herleidbare details over de student, de stageplek en cliënten. Namen weghalen is geen anonimisering.', 'naar': 's2'},
              {'text': 'Wacht even: wat staat er nog meer in die verslagen?', 'reactie': 'Hm, nu je het zegt: namen van de stageplek, situaties met cliënten, soms ook persoonlijke reflecties.', 'uitleg': 'Goede vraag. Je laat Sanne zelf zien waarom de verslagen herleidbaar blijven.', 'naar': 's2'},
          ]},
         {'id': 's2', 'text': 'Oké, dus niet zomaar plakken. Maar ik wil wel sneller kunnen nakijken. Wat kan dan wél?',
          'choices': [
              {'text': 'Gebruik AI voor een feedbackbank: laat het veelvoorkomende sterke punten en valkuilen per criterium formuleren op basis van je rubric, zonder studentwerk.', 'reactie': 'Dat is slim. Dan gebruik ik mijn eigen rubric als context en schrijf ik per student zelf de feedback.', 'uitleg': 'Sterk alternatief: de AI krijgt geen persoonsgegevens en jij houdt het oordeel.', 'naar': 's3'},
              {'text': 'Gebruik een betaalde tool, die zijn veiliger.', 'reactie': 'Is dat zo? En wie betaalt dat?', 'uitleg': 'Betaald is niet automatisch toegestaan. Wat telt is of je instelling de omgeving heeft goedgekeurd en er een verwerkersovereenkomst is.', 'naar': 's3'},
          ]},
         {'id': 's3', 'text': 'Laatste vraag: moet ik mijn studenten vertellen dat ik AI gebruik voor de feedback?',
          'choices': [
              {'text': 'Ja. Vertel wat je ermee deed en dat het oordeel van jou is.', 'reactie': 'Dan doe ik wat ik van hen ook vraag. Klinkt eerlijk.', 'uitleg': 'Transparantie werkt twee kanten op en maakt het makkelijker om met studenten over hun eigen AI-gebruik te praten.'},
              {'text': 'Nee, het is maar een hulpmiddel.', 'reactie': 'Maar ik vraag van hen wel dat ze het vermelden...', 'uitleg': 'Als je van studenten transparantie vraagt, is het geloofwaardig om dat zelf ook te doen.'},
          ]},
     ], 'slot': p('Kern: geen studentwerk met herleidbare gegevens in een open tool, zoek een alternatief waarin AI zonder persoonsgegevens helpt, en wees transparant.')},
    doorgaan(),
    notitie('opdracht', '<p><strong>Praktijk.</strong> Beoordeel drie situaties uit je eigen werk. Eén: feedback op studentwerk. Twee: een vertrouwelijk document. Drie: een betaalde AI-tool die niet iedereen heeft.</p>'),
    open_vraag('Kies per situatie: gebruiken, aanpassen, stoppen of voorleggen. Geef een reden en een bruikbaar alternatief. Bij wie in je instelling kun je terecht met twijfel?'),
    competentie('4', 'je bepaalt bij een fictieve studentcasus welke informatie je mag gebruiken en welke eerst weg moet. Je weet wanneer je het voorlegt aan een deskundige.'),
]}

m4 = {'id': 'm4', 'title': '4. Wat weten we echt? Het onderzoek', 'deadline': '', 'blocks': [
    *leerdoelen('uitleggen waarom het ontwerp, niet de tool, bepaalt of AI leren helpt of schaadt;',
                'het verschil tussen presteren mét AI en leren door AI herkennen;',
                'populaire maar onbetrouwbare claims over AI in het onderwijs herkennen.'),
    doorgaan(),
    {'t': 'quote', 'body': 'Ontwerp beslist: AI binnen een didactische structuur helpt, een open chatbot als antwoordmachine schaadt.'},
    tekst('Drie studies, drie uitkomsten',
          'Het causale bewijs over AI en leren is nog klein: een handvol studies, vaak kortdurend en buiten het hbo. Toch is er een patroon.'),
    {'t': 'tabs', 'items': [
        {'title': 'Kestin e.a. (2025)', 'body': p('<strong>Positief.</strong> In een natuurkundevak met 194 Harvard-studenten leverde een <em>didactisch ontworpen</em> AI-tutor betere directe leerresultaten op dan de klassikale vergelijkingsconditie.', '<em>Beperking:</em> kort, één vak. Geen bewijs dat docenten vervangbaar zijn.')},
        {'title': 'Bastani e.a. (2025)', 'body': p('<strong>Negatief.</strong> Bij bijna 1.000 scholieren wiskunde presteerden leerlingen met een algemene GPT-interface beter tijdens het oefenen, maar slechter op de latere toets zonder AI (circa 17% lager). Een begrensde tutor-versie verminderde die schade.', '<em>Beperking:</em> voortgezet onderwijs, wiskunde.')},
        {'title': 'Fischer e.a. (2025)', 'body': p('<strong>Genuanceerd.</strong> Bij 334 universiteitsstudenten verbeterde AI-tutoring de testprestaties, en presteerde onbeperkte toegang beter dan de onderzochte beperking vooraf.', '<em>Beperking:</em> working paper, specifieke toetscontext. Een tegenwicht tegen "eerst zonder AI is altijd beter".')},
    ]},
    notitie('info', 'Vermijd beide uitersten: "AI helpt altijd" en "AI schaadt altijd" zijn allebei niet onderbouwd. Effecten hangen af van taak, tool en context.', 'Wat je hieruit meeneemt'),
    quiz('Studenten die een algemene chatbot gebruikten, scoorden in Bastani e.a. beter tijdens het oefenen en slechter op de toets zonder AI. Wat betekent dat voor jouw onderwijs?', [
        ('Een beter product met AI bewijst niet dat een student meer geleerd heeft.', True, 'Precies. Taakprestatie en leerresultaat zijn twee verschillende dingen. Ontwerp daarom altijd een controle op begrip die verder gaat dan het eindproduct.'),
        ('AI moet verboden worden bij oefenopdrachten.', False, 'Dat gaat verder dan het bewijs. In dezelfde studie verminderde een begrensde tutor-versie de schade, en Fischer e.a. vond juist voordelen. Het gaat om het ontwerp.'),
        ('Het effect geldt alleen voor wiskunde en is dus niet relevant.', False, 'De context verschilt inderdaad, maar het mechanisme, dat AI het denkwerk overneemt, is in elk vak een risico om rekening mee te houden.'),
    ]),
    doorgaan(),
    tekst('Claimcheck: wat je beter niet gebruikt',
          'Over AI in het onderwijs circuleren claims die steviger klinken dan ze zijn. Weet welke dat zijn, zodat je ze niet doorvertelt in een les, beleidsstuk of presentatie.'),
    {'t': 'accordion', 'items': [
        {'title': '"AI levert bijna een standaarddeviatie leerwinst op"', 'body': p('Dit komt uit een meta-analyse (Wang &amp; Fan) die in april 2026 is ingetrokken, maar nog steeds veel wordt geciteerd. Niet gebruiken.')},
        {'title': '"Met een AI-detector kun je fraude aantonen"', 'body': p('AI-detectors zijn onvoldoende nauwkeurig (onder de 80%) om op te sanctioneren. Een detectorscore is nooit een zelfstandig fraudeoordeel.')},
        {'title': '"20% van de masterscripties is door AI geschreven"', 'body': p('Dit is een signaal uit een detectortool, geen meting. De foutmarge van de detector is onbekend.')},
        {'title': '"AI veroorzaakt cognitive debt"', 'body': p('De bekende MIT-studie had 54 deelnemers en is (nog) niet peer reviewed. Een interessante aanwijzing, geen vaststaand feit.')},
    ]},
    {'t': 'fill', 'question': 'Vul aan.', 'text': 'Een AI-detectorscore is geen zelfstandig [fraudeoordeel|bewijs]. Wat studenten met AI maken zegt iets over hun taakprestatie, maar niet automatisch over hun [leerresultaat|leren|begrip].',
     'feedback': 'Goed. Detectors zijn te onnauwkeurig voor een oordeel, en een goed product is nog geen bewijs van leren.',
     'feedbackWrong': 'Een detector is te onnauwkeurig om op te sanctioneren. En presteren met AI is iets anders dan zelf iets geleerd hebben: dat heet het leerresultaat.'},
    doorgaan(),
    tekst('Wat dit betekent voor ontwerpen',
          'Uit het onderzoek volgen vier ontwerpprincipes die in de rest van deze e-learning terugkomen:'),
    lijst(['<strong>Basis eerst.</strong> Wie de basis niet beheerst, kan AI-output niet beoordelen.',
           '<strong>Kalibratie als leerdoel.</strong> Geef taken waarin AI soms bewust fout zit, zodat studenten leren wanneer ze AI kunnen vertrouwen.',
           '<strong>Docent in de lus.</strong> AI binnen een structuur die jij ontwerpt, met jouw oordeel aan het eind.',
           '<strong>Van product naar persoon.</strong> Toets meer het denkproces en de beslissingen, minder alleen het eindproduct.'], True),
    plaatshouder('Kennisclip of interview met een onderzoeker of kritische stem (bijvoorbeeld over de drie kampen: integrators, pragmatici en critici).'),
    open_vraag('Welk van de vier principes is voor jouw onderwijsactiviteit het belangrijkst, en waarom?'),
]}

m5 = {'id': 'm5', 'title': '5. Leeractiviteiten ontwerpen met AI', 'deadline': '', 'blocks': [
    *leerdoelen('bepalen welk denkwerk de student zelf moet doen;',
                'een leeractiviteit ontwerpen waarin leerdoel, AI-keuze en begripscontrole kloppen;',
                'kiezen welke rol AI in een leeractiviteit krijgt.'),
    doorgaan(),
    tekst('Begin bij het denkwerk',
          'Elke leeractiviteit draait om een denkhandeling, zoals analyseren of onderbouwen. De vraag is dus niet "mag AI?". De vraag is: <strong>welk denkwerk moet de student zelf doen om het leerdoel te halen?</strong>',
          'Een handige test: kan een student de opdracht afmaken zonder het leerdoel te oefenen? Dan is je ontwerp kwetsbaar. Dat geldt met en zonder AI.'),
    {'t': 'svg', 'svg': SVG_LUS, 'alt': 'Cyclus: eerst zelf, dan AI, dan weer zelf, met een pijl terug voor verfijnen en herhalen.',
     'caption': 'Eerst zelf, dan AI, dan weer zelf: het patroon uit de AI-placemats.'},
    notitie('let', 'Dit is een mogelijk ontwerp, geen vaste regel. Soms is AI juist aan het begin nuttig. Bijvoorbeeld om een onbekend onderwerp te verkennen. Kies bewust.'),
    quiz('Een student kan je opdracht helemaal afronden door alles aan AI te vragen, zonder het leerdoel te oefenen. Wat zegt dat?', [
        ('Het ontwerp is kwetsbaar: pas de opdracht aan zodat het denkwerk bij de student ligt.', True, 'Ja. Het probleem zit in het ontwerp, niet bij de student of de tool.'),
        ('De student fraudeert.', False, 'Niet per se. Als de afspraken niet helder zijn en de opdracht het toelaat, ligt het eerst aan het ontwerp.'),
        ('Er is niets aan de hand zolang het product goed is.', False, 'Een goed product zegt dan niets over wat de student kan. Taakprestatie is geen leerresultaat.'),
    ]),
    doorgaan(),
    tekst('Rollen die AI kan spelen',
          'Mollick &amp; Mollick (2023) beschrijven zeven rollen die AI in een opdracht kan hebben. Elke rol heeft een ander leerdoel en een ander risico. In alle rollen blijft de student de mens in de lus: die controleert de output.'),
    {'t': 'cards', 'items': [
        {'front': '<p><strong>Mentor</strong></p>', 'back': '<p>Geeft doorlopend feedback op werk in uitvoering. Risico: de student neemt feedback over zonder te beoordelen of die klopt.</p>'},
        {'front': '<p><strong>Tutor</strong></p>', 'back': '<p>Legt uit en stelt vragen, bij voorkeur hints in plaats van antwoorden. Risico: de student vraagt toch om het antwoord.</p>'},
        {'front': '<p><strong>Coach</strong></p>', 'back': '<p>Helpt reflecteren op het eigen leerproces en plannen. Risico: oppervlakkige reflectie die mooi klinkt.</p>'},
        {'front': '<p><strong>Teamgenoot</strong></p>', 'back': '<p>Denkt mee in een project en brengt andere perspectieven of tegenargumenten in. Risico: de student neemt ideeën over zonder ze te wegen.</p>'},
        {'front': '<p><strong>Student</strong></p>', 'back': '<p>De student legt iets uit aan de AI en verbetert de fouten van de AI. Risico: de AI maakt geen realistische fouten.</p>'},
        {'front': '<p><strong>Simulator</strong></p>', 'back': '<p>Speelt een klant, patiënt of stakeholder in een oefengesprek. Risico: onrealistische reacties.</p>'},
        {'front': '<p><strong>Gereedschap</strong></p>', 'back': '<p>Voert een afgebakende taak uit, zoals tekst ordenen of samenvatten. Risico: de student begrijpt niet wat er gebeurde.</p>'},
    ]},
    quiz('Een docent wil dat studenten leren een beleidsadvies te onderbouwen. Welk ontwerp past het best bij dat leerdoel?', [
        ('Studenten laten AI een advies schrijven en dat inleveren met bronvermelding.', False, 'Dan doet de AI het onderbouwen, terwijl dat juist het leerdoel is. Het product zegt weinig over wat de student kan.'),
        ('Studenten schrijven eerst zelf een kernadvies met drie argumenten, laten AI tegenargumenten geven en verantwoorden welke ze verwerkten en waarom.', True, 'Ja. De student doet het onderbouwen en wegen zelf; AI is teamgenoot die tegenargumenten inbrengt. De verantwoording maakt het denkwerk zichtbaar.'),
        ('Studenten mogen geen AI gebruiken en schrijven het advies thuis.', False, 'Dat kan een verdedigbare keuze zijn, maar thuis valt AI-gebruik niet te controleren. Je mist ook de kans om kritisch AI-gebruik te oefenen.'),
    ]),
    doorgaan(),
    tekst('Taakprestatie of leerresultaat?',
          'Ontwerp altijd een <strong>begripscontrole</strong> die verder gaat dan het eindproduct. Denk aan een korte uitleg aan een medestudent. Of een nieuwe casus zonder AI. Of een gesprek over de keuzes.'),
    {'t': 'match', 'question': 'Koppel elk leerdoel aan een passende begripscontrole.', 'pairs': [
        {'left': 'Een analyse kunnen maken', 'right': 'Een nieuwe, vergelijkbare casus live analyseren zonder AI'},
        {'left': 'Keuzes kunnen verantwoorden', 'right': 'Een kort gesprek: welke AI-suggestie heb je verworpen en waarom?'},
        {'left': 'Een begrip kunnen uitleggen', 'right': 'Het begrip in eigen woorden uitleggen aan een medestudent'},
    ], 'feedback': 'Goed. Elke controle maakt zichtbaar wat de student zelf kan.',
     'feedbackWrong': 'Kijk welke controle precies de denkhandeling uit het leerdoel zichtbaar maakt.'},
    doorgaan(),
    notitie('opdracht', '<p><strong>Praktijk (40 minuten).</strong> Herontwerp je eigen onderwijsactiviteit. Laat daarna een collega nagaan of een student de opdracht kan afronden zonder het leerdoel te oefenen.</p>'),
    open_vraag('Beschrijf je herontwerp: het leerdoel, welk denkwerk de student zelf doet, welke rol AI krijgt (of waarom geen AI), de begripscontrole en een alternatief zonder AI.',
               'Leerdoel / denkwerk student / rol AI / begripscontrole / alternatief'),
    competentie('5', 'je ontwerpt één activiteit met een leerdoel en een onderbouwde AI-keuze. Je controleert het begrip van de student, niet alleen het eindproduct.'),
]}

m6 = {'id': 'm6', 'title': '6. Onderwijs herontwerpen: de placemat-methode', 'deadline': '', 'blocks': [
    *leerdoelen('de zeven stappen van de AI-placemat uitleggen en toepassen in je eigen vak;',
                'studenten coachen op het denkwerk in plaats van op de tool;',
                'signalen herkennen dat een student het denkwerk aan de AI overlaat.'),
    doorgaan(),
    tekst('Wat is een AI-placemat?',
          'Een AI-placemat is een A3-werkblad dat studenten in zeven stappen van een leeg vel naar een eigen product brengt, bijvoorbeeld een infographic, website, e-learning of spel. De voorkant is denken en zoeken, de achterkant is maken.',
          'De kern in één zin: <strong>eerst zelf, dan AI, dan weer zelf.</strong> Wat een student in stap 1 opschrijft, wordt in stap 2 de prompt. Niets vul je voor niets in.'),
    {'t': 'timeline', 'items': [
        {'date': 'Stap 1', 'title': 'Zelf eerst', 'body': p('Zonder AI: wat weet ik al, wat is mijn verwachting, drie echte onderzoeksvragen, twee bronnen.')},
        {'date': 'Stap 2', 'title': 'Deep research', 'body': p('De prompt schrijven uit het denkwerk van stap 1: rol, context, opdracht, output.')},
        {'date': 'Stap 3', 'title': 'Zelf analyseren', 'body': p('Het rapport lezen, twee claims natrekken in de bron, afwijkingen van de eigen verwachting noteren.')},
        {'date': 'Stap 4', 'title': 'Sorteren', 'body': p('Kiezen wat erin komt. Wat de student niet kiest, kiest de AI.')},
        {'date': 'Stap 5', 'title': 'Uittekenen', 'body': p('Het product op papier schetsen. Wie het kan tekenen, snapt het.')},
        {'date': 'Stap 6', 'title': 'Maken', 'body': p('De AI bouwt wat de student bedacht. Pas hier eventueel een metaprompt.')},
        {'date': 'Stap 7', 'title': 'Checken', 'body': p('Testen met een ander groepje, controleren en verantwoorden wat AI deed en wat de student zelf deed.')},
    ]},
    {'t': 'hotspots', 'src': beeld('placemat5-voor.jpg'),
     'alt': 'Voorkant van AI-placemat 5 (E-learning) van Food & Business: bovenin een strook met zeven stappen, daaronder drie kolommen voor stap 1 Zelf eerst, stap 2 Deep research met AI en stap 3 Zelf analyseren, onderaan vier vuistregels.',
     'intro': 'Een voorbeeld: de voorkant van placemat 5 (E-learning) uit Food & Business. Klik op de nummers.',
     'points': [
         {'x': 50, 'y': 5, 'title': 'De zeven stappen', 'body': p('De strook laat zien waar de student is. Stap 1 tot en met 3 staan op de voorkant (onderzoeken), stap 4 tot en met 7 op de achterkant (maken). Tussen 6 en 7 zit een lus: verfijn en herhaal.')},
         {'x': 4, 'y': 17, 'title': 'Stap 1: Zelf eerst', 'body': p('Laptop dicht. De student noteert wat die al weet, een eigen verwachting, drie echte onderzoeksvragen en twee bronnen. Hier gaat de meeste begeleidingstijd naartoe.')},
         {'x': 36.2, 'y': 17, 'title': 'Stap 2: Deep research', 'body': p('De prompt komt uit stap 1: rol, context, opdracht, output. Vraag: "Waar op je placemat komt dit deel van je prompt vandaan?"')},
         {'x': 47, 'y': 38, 'title': 'Context is bijna altijd te kort', 'body': p('De student neemt het onderwerp, de vragen en de bronnen uit stap 1 over. Hoe meer context, hoe gerichter de AI zoekt.')},
         {'x': 68.3, 'y': 17, 'title': 'Stap 3: Zelf analyseren', 'body': p('Het rapport naast je, pen in de hand. Drie inzichten in eigen woorden en wat afwijkt van de eigen verwachting.')},
         {'x': 88, 'y': 54, 'title': 'Twee claims natrekken', 'body': p('De student opent de bron die de AI noemt: bestaat hij, en staat het er echt? Een gevonden fout is bewijs van kritisch denken.')},
         {'x': 11, 'y': 92.5, 'title': 'Vuistregels', 'body': p('Werk in .md of .txt, geen persoonsgegevens in een open tool, een cijfer zonder geziene bron gebruik je niet, en: jij blijft de denker.')},
     ]},
    {'t': 'image', 'src': beeld('placemat5-achter.jpg'),
     'alt': 'Achterkant van AI-placemat 5 (E-learning): stap 4 Sorteren, stap 5 Uittekenen, stap 6 Maken en stap 7 Checken, met een checklist en een overzicht van het eigen AI-gebruik.',
     'caption': 'De achterkant: sorteren, uittekenen, maken en checken. Die kant verschilt per product.'},
    plaatshouder('Kies of je de placemats van Food &amp; Business als voorbeeld houdt, of een placemat uit een ander domein laat zien.'),
    doorgaan(),
    tekst('Jouw rol: didactisch coach, geen AI-expert',
          'Je stuurt op het denkwerk, niet op de tool. Vraag niet "laat je scherm zien", maar "wijs het aan op je placemat". Het zwaarste moment is het begin: van een leeg vel naar goede vragen. Daar gaat het grootste deel van je begeleidingstijd naartoe.'),
    {'t': 'table', 'kop': True, 'caption': 'Eén coachvraag per stap', 'rows': [
        ['Stap', 'Jouw vraag'],
        ['1 Zelf eerst', 'Welke vraag wil je beantwoorden?'],
        ['2 Deep research', 'Waar op je placemat komt dit deel van je prompt vandaan?'],
        ['3 Analyseren', 'Laat zien waar deze claim in de bron staat.'],
        ['4 Sorteren', 'Wat laat je weg, en waarom?'],
        ['5 Uittekenen', 'Leg je product uit aan de hand van je schets.'],
        ['6 Maken', 'Als jij de AI was, wat zou je met deze prompt maken?'],
        ['7 Checken', 'Kun je uitleggen wat je gemaakt hebt, zonder de AI erbij?'],
    ]},
    quiz('Een groepje heeft een prachtige website gemaakt, maar de voorkant van de placemat is bijna leeg. Wat doe je?', [
        ('Je beoordeelt de website: het product is goed.', False, 'Een mooi product met een lege voorkant zegt weinig over wat de studenten geleerd hebben. Het denkwerk is overgeslagen.'),
        ('Je stuurt ze terug naar stap 1: een eenvoudig product met een volle voorkant is meer waard.', True, 'Ja. Zo maak je duidelijk dat het denkwerk telt, niet de glans van het product.'),
        ('Je laat ze een tweede website maken met een betere prompt.', False, 'Het probleem zit niet in de prompt maar in het ontbrekende voorwerk. Een betere prompt lost dat niet op.'),
    ]),
    {'t': 'sort', 'question': 'Signaal of geen zorg? Sorteer wat je ziet tijdens het rondlopen.', 'piles': ['Signaal: ingrijpen', 'Geen zorg'],
     'items': [
         {'text': 'De student plakt het hele rapport in de chat', 'pile': 0},
         {'text': 'De AI verzint cijfers in het product', 'pile': 0},
         {'text': 'Een student vindt een fout in het AI-rapport', 'pile': 1},
         {'text': 'Na twee rondes is het product nog steeds mis', 'pile': 0},
         {'text': 'Een groepje start de deep research vóór de pauze', 'pile': 1},
     ],
     'feedback': 'Goed. En vergeet niet: een gevonden fout van de AI is bewijs van kritisch denken, geen mislukking. Zeg dat hardop.',
     'feedbackWrong': 'Een gevonden fout is juist goed nieuws. Rapport plakken, verzonnen cijfers en vastlopen na twee rondes wijzen op ontbrekend voorwerk in stap 4 of 5.'},
    doorgaan(),
    notitie('opdracht', '<p><strong>Praktijk.</strong> Probeer het één keer zelf: doorloop stap 1 tot en met 3 met een onderwerp uit je eigen vak. Een half uur is genoeg om te weten waar studenten tegenaan lopen.</p>'),
    {'t': 'links', 'items': [
        {'label': 'AI-placemats en docentinstructie', 'href': 'https://fabianb88.github.io/war-room/'},
    ]},
    plaatshouder('Vervang de link hierboven door de juiste downloadlocatie van de placemats, de docentinstructie en de extra uitleg voor studenten.'),
    open_vraag('Hoe zou de placemat-aanpak eruitzien in jouw vak? Welke stap zou voor jouw studenten het moeilijkst zijn, en welke coachvraag stel je dan?'),
]}

m7 = {'id': 'm7', 'title': '7. Toetsing en bewijs van beheersing', 'deadline': '', 'blocks': [
    *leerdoelen('vooraf duidelijke AI-afspraken formuleren bij een opdracht of toets;',
                'uitleggen wat een AI-ondersteund product wel en niet aantoont over individuele beheersing;',
                'een passende aanvullende bewijsvorm toevoegen, met oog voor toegankelijkheid.'),
    doorgaan(),
    tekst('Van product naar persoon',
          'AI-agents kunnen steeds meer stappen zelfstandig uitvoeren, tot het inleveren van huiswerk toe. Een product dat zonder toezicht is gemaakt, verliest daarmee waarde als bewijs van wat een student kan. Toetsing verschuift naar wat <strong>live, mondeling en traceerbaar</strong> is.',
          'Dat betekent niet: alles mondeling. Een gesprek is niet vanzelf geldig of voor iedereen even toegankelijk. Het gaat om een <em>combinatie</em> van producten, gesprekken en observaties (Lodge e.a., 2023).'),
    {'t': 'steps', 'intro': {'title': 'AI-afspraken per opdracht', 'body': 'De vijf niveaus van de herziene AI Assessment Scale (Perkins e.a., 2024). Het zijn geen treden van slecht naar goed: je kiest per opdracht het niveau dat bij het leerdoel past.'},
     'steps': [
         {'title': 'Geen AI', 'body': 'De opdracht wordt onder toezicht gemaakt; het denkwerk is het leerdoel.'},
         {'title': 'AI voor voorbereiding', 'body': 'AI mag helpen bij verkennen en plannen; het product maakt de student zelf.'},
         {'title': 'AI als samenwerkingspartner', 'body': 'AI mag meeschrijven; de student verantwoordt wat AI deed en wat zelf.'},
         {'title': 'Volledig met AI', 'body': 'AI mag overal; de beoordeling richt zich op keuzes, controle en eindoordeel.'},
         {'title': 'AI verkennen', 'body': 'Studenten onderzoeken AI zelf of gebruiken het op een nieuwe manier.'},
     ],
     'summary': {'title': 'Let op', 'body': 'Een afspraak is geen controle. Alleen wat je onder toezicht toetst, kan zelfstandig bewijs van individuele beheersing zijn. Spreek vooraf af wat er beoordeeld wordt.'}},
    notitie('info', 'De University of Sydney werkt met een tweesporenaanpak. Spoor 1: beveiligde toetsmomenten waar AI-gebruik controleerbaar is. Dat betekent niet per se "geen AI". Spoor 2: open opdrachten waar AI-gebruik bij het leren hoort en niet verboden wordt. Kijk welk kader je eigen instelling hanteert.'),
    tekst('Het kader van je eigen instelling',
          'Bij de HAN staan het Integraal AI-kader en de Toolkit AI-bestendig toetsen op de pagina Onderwijs met AI. Werk je bij een andere instelling, zoek dan de vergelijkbare stukken op.'),
    {'t': 'links', 'items': [
        {'label': 'HAN: Toolkit AI-bestendig toetsen (pdf)', 'href': 'https://www.han.nl/onderwijsondersteuning/leren-werken-met-ict/artificial-intelligence/Toolkit-AI-bestendig-toetsen-Versie-2-maart-2025.pdf'},
        {'label': 'HAN: Integraal AI-kader (pdf)', 'href': 'https://www.han.nl/onderwijsondersteuning/leren-werken-met-ict/artificial-intelligence/ai-in-je-onderwijs/Integraal-AI-kader-HAN-1.0-27062025.pdf'},
        {'label': 'AI Assessment Scale', 'href': 'https://aiassessmentscale.com/'},
    ]},
    doorgaan(),
    {'t': 'scenario', 'persoon': 'Mehmet', 'rol': 'Examencommissielid', 'intro': p('Je hebt het vermoeden dat een student een verslag grotendeels met AI heeft geschreven, terwijl dat niet mocht. Mehmet vraagt hoe je dit aanpakt.'),
     'scenes': [
         {'id': 'a', 'text': 'Waar baseer je je vermoeden op?',
          'choices': [
              {'text': 'De AI-detector gaf 87% AI-tekst.', 'reactie': 'Dat alleen is voor ons geen grond voor een fraudeoordeel.', 'uitleg': 'Klopt: detectors zijn daarvoor niet nauwkeurig genoeg. Een score kan aanleiding zijn voor een gesprek, nooit voor een oordeel.', 'naar': 'b'},
              {'text': 'De student kon in de bespreking de eigen keuzes niet uitleggen en citeerde een bron die niet bestaat.', 'reactie': 'Dat zijn concrete, controleerbare observaties. Goed vastgelegd?', 'uitleg': 'Sterk: je baseert je op wat de student wel en niet kan laten zien, plus een verifieerbare fout.', 'naar': 'b'},
          ]},
         {'id': 'b', 'text': 'Hoe kun je voorkomen dat je hier volgende keer weer staat?',
          'choices': [
              {'text': 'Vooraf duidelijke AI-afspraken en een kort gesprek over de keuzes als vast onderdeel van de beoordeling.', 'reactie': 'Dat maakt het voor de student ook helder wat er telt.', 'uitleg': 'Ja: je ontwerpt de beoordeling zo dat individuele beheersing zichtbaar wordt, in plaats van achteraf te speuren.'},
              {'text': 'Alle opdrachten door een betere detector halen.', 'reactie': 'Daar ben ik niet zo zeker van.', 'uitleg': 'Een betere detector lost het onderliggende probleem niet op: het product alleen is geen betrouwbaar bewijs meer.'},
          ]},
     ], 'slot': p('Kern: een detectorscore is geen fraudeoordeel. Ontwerp de toets zo dat je individuele beheersing kunt laten zien.')},
    doorgaan(),
    notitie('opdracht', '<p><strong>Praktijk.</strong> Test je eigen opdracht met AI: hoe ver komt een student als die alles door AI laat doen? Beschrijf wat het resultaat dan nog wel en niet aantoont.</p>'),
    open_vraag('Herschrijf je opdracht met (1) duidelijke AI-afspraken, (2) beoordelingscriteria die het denkwerk van de student zichtbaar maken en (3) een aanvullende bewijsvorm. Hoe zorg je dat die bewijsvorm voor alle studenten toegankelijk is?'),
    competentie('6', 'je past een bestaande opdracht aan met duidelijke AI-afspraken en een onderbouwde manier om individuele beheersing te beoordelen.'),
]}

m8 = {'id': 'm8', 'title': '8. Studenten begeleiden bij zelfstandig oordelen', 'deadline': '', 'blocks': [
    *leerdoelen('een gesprek over AI-gebruik voeren zonder automatisch van fraude uit te gaan;',
                'vragen stellen die de redenering, controle en verantwoordelijkheid van de student zichtbaar maken;',
                'herkennen wanneer AI het eigen leerproces van een student belemmert.'),
    doorgaan(),
    tekst('Het gesprek gaat over denken, niet over de tool',
          'Studenten gebruiken AI toch. Het gesprek verschuift daarom van "heb je AI gebruikt?" naar "hoe heb je het gebruikt, en wat deed je zelf?". Dat is ook het moment waarop een student leert kalibreren: wanneer kan ik AI vertrouwen, en wanneer niet?'),
    {'t': 'cards', 'items': [
        {'front': '<p>Welke suggestie van de AI heb je verworpen?</p>', 'back': '<p>Laat zien of de student kritisch heeft gekozen of alles heeft overgenomen.</p>'},
        {'front': '<p>Welke claim heb je nagetrokken, en waar?</p>', 'back': '<p>Laat zien of de student de output heeft gecontroleerd.</p>'},
        {'front': '<p>Kun je dit uitleggen zonder de AI erbij?</p>', 'back': '<p>Laat zien of de kennis van de student is.</p>'},
        {'front': '<p>Wanneer hielp AI je niet?</p>', 'back': '<p>Helpt de student herkennen wanneer ondersteuning het eigen leren in de weg zit.</p>'},
    ]},
    doorgaan(),
    {'t': 'scenario', 'persoon': 'Lisa', 'rol': 'Tweedejaars student', 'intro': p('Lisa leverde een sterke analyse in. In het begeleidingsgesprek merk je dat ze de kern lastig kan uitleggen.'),
     'scenes': [
         {'id': 'l1', 'text': 'Ik heb het wel echt zelf gedaan hoor. Nou ja, ik heb ChatGPT gebruikt om het netjes te maken.',
          'choices': [
              {'text': 'Dat mocht niet. Ik moet dit melden.', 'reactie': 'Maar... dat stond nergens. Iedereen doet het.', 'uitleg': 'Je begint bij fraude en sluit het gesprek af. Als de afspraken niet helder waren, ligt een deel van het probleem bij het ontwerp.', 'naar': 'l2'},
              {'text': 'Fijn dat je dat vertelt. Kun je me laten zien wat je eerst zelf had, en wat de AI veranderde?', 'reactie': 'Eh, ik had vooral wat steekwoorden. De structuur kwam eigenlijk van ChatGPT.', 'uitleg': 'Goed: je maakt het gesprek veilig en richt je op het denkproces.', 'naar': 'l2'},
          ]},
         {'id': 'l2', 'text': 'Dus... is het nu niet goed?',
          'choices': [
              {'text': 'Leg me in je eigen woorden uit waarom je tot deze conclusie komt. Welk argument vind jij het sterkst?', 'reactie': 'Hm. Ik denk het tweede, omdat... eigenlijk weet ik niet zeker of dat klopt.', 'uitleg': 'Je laat de student een keuze uitleggen. Ze ontdekt zelf waar haar begrip ophoudt.', 'naar': 'l3'},
              {'text': 'Het is goed geschreven, dus prima.', 'reactie': 'Oké, top!', 'uitleg': 'Dan beoordeel je de taakprestatie, niet het leren. Lisa leert niets van dit gesprek.', 'naar': 'l3'},
          ]},
         {'id': 'l3', 'text': 'Wat moet ik nu doen?',
          'choices': [
              {'text': 'Controleer die ene claim in de bron en schrijf in vijf zinnen je eigen redenering op. Dan bespreken we het volgende week.', 'reactie': 'Dat is te doen. En dan weet ik ook beter wat ik eigenlijk vind.', 'uitleg': 'Een concrete vervolgstap: claim controleren en de redenering eigen maken.'},
              {'text': 'Volgende keer gewoon geen AI gebruiken.', 'reactie': 'Oké... maar dan weet ik nog steeds niet hoe het wel moet.', 'uitleg': 'Een verbod helpt Lisa niet om te leren hoe ze AI verstandig gebruikt.'},
          ]},
     ], 'slot': p('Kern: veilig gesprek, focus op de redenering, de student een keuze laten uitleggen, een claim laten controleren en een vervolgstap laten formuleren.')},
    notitie('let', 'Herken ook wanneer een vraag niet over AI gaat. Soms zit achter overmatig AI-gebruik tijdsdruk, onzekerheid of een persoonlijk probleem. Dan is menselijke ondersteuning nodig, bijvoorbeeld van een studentbegeleider.'),
    doorgaan(),
    notitie('opdracht', '<p><strong>Praktijk (in drietallen).</strong> Voer een begeleidingsgesprek: één docent, één student, één observator. Gebruik je eigen onderwijsactiviteit als casus. Wissel daarna van rol.</p>'),
    open_vraag('Welke vraag werkte het best in het gesprek, en waarom? Wat zou je in een echt gesprek anders doen?'),
    competentie('7', 'je voert een gesimuleerd begeleidingsgesprek waarin de student een keuze uitlegt, een claim controleert en een vervolgstap formuleert.'),
]}

m9 = {'id': 'm9', 'title': '9. Blijven leren en je herontwerp afronden', 'deadline': '', 'blocks': [
    *leerdoelen('je herontwerp afronden en laten beoordelen door een collega;',
                'verschillende toekomstscenario\'s gebruiken om je ontwerp robuust te maken;',
                'een persoonlijk onderhoudsplan maken.'),
    doorgaan(),
    tekst('Drie scenario\'s richting 2030',
          'Niemand weet hoe snel AI verandert. Daarom ontwerp je onderwijs dat werkt in meerdere toekomsten. Dit zijn verkenningen, geen voorspellingen.'),
    {'t': 'tabs', 'items': [
        {'title': 'AI blijft assistent', 'body': p('Tools verbeteren, maar docenten en studenten doen veel stappen zelf. Leerdoelen, broncontrole, feedback en verantwoording blijven centraal.')},
        {'title': 'AI doet meer zelf', 'body': p('Systemen combineren documenten, plannen en voeren handelingen uit. Afbakening, tussencontroles en zichtbaarheid van de bijdrage van de student worden belangrijker.')},
        {'title': 'AI wordt begrensd', 'body': p('Kosten, privacy of beleid beperken toepassingen. Alternatieven, inclusieve opdrachten en uitleg over beperkingen blijven essentieel.')},
    ]},
    quiz('Welk onderdeel van je herontwerp blijft in alle drie de scenario\'s waardevol?', [
        ('Een begripscontrole die laat zien wat de student zelf kan.', True, 'Ja. Hoe AI zich ook ontwikkelt, je wilt weten wat de student zelf beheerst.'),
        ('Een opdracht die alleen werkt met één specifieke tool.', False, 'Die is kwetsbaar: in het derde scenario kan de tool wegvallen, in het tweede kan hij de opdracht helemaal overnemen.'),
    ]),
    doorgaan(),
    tekst('Je portfolio afronden',
          'Je eindportfolio laat in je eigen beroepspraktijk zien dat je de acht competenties beheerst. Een collega beoordeelt het met een rubric. Een onopgeloste kritieke fout, zoals vertrouwelijke gegevens in een open tool, een verzonnen bron of onbewezen beheersing, vraagt eerst herstel.'),
    {'t': 'list', 'ordered': False, 'items': [
        '<p>Een gecontroleerd AI-resultaat met je verbeterrondes (module 2)</p>',
        '<p>Een uitgewerkte gegevenscasus (module 3)</p>',
        '<p>Je herontworpen leeractiviteit (modules 5 en 6)</p>',
        '<p>Je aangepaste opdracht met AI-afspraken (module 7)</p>',
        '<p>Een reflectie op een begeleidingsgesprek (module 8)</p>',
        '<p>Je onderhoudsplan (deze module)</p>',
    ]},
    {'t': 'table', 'kop': True, 'zijkop': True, 'caption': 'Conceptrubric voor de collegiale beoordeling. Voldoende is het aantoonbare minimum per competentie.', 'rows': [
        ['Competentie', 'Nog niet', 'Voldoende', 'Goed', 'Voorbeeldig'],
        ['1 Grenzen begrijpen', 'Neemt AI-antwoorden over als feit', 'Legt bij twee voorbeelden uit waarom overtuigend niet juist betekent', 'Benoemt ook wanneer een bron of specialist nodig is', 'Helpt collega\'s deze grenzen te zien'],
        ['2 Doelgericht gebruiken', 'Gebruikt AI zonder doel of context', 'Concept voor een eigen taak, twee verbeterstappen vastgelegd', 'Verantwoordt ook waarom AI wel of niet past', 'Werkwijze werkt ook met een andere tool'],
        ['3 Output controleren', 'Mist fouten of de verzonnen bron', 'Corrigeert fouten en verzonnen bron met controleerbare informatie', 'Ziet ook eenzijdigheid en ontbrekende perspectieven', 'Maakt er een oefening voor studenten van'],
        ['4 Gegevens en gevolgen', 'Kritieke fout: herleidbare gegevens in een open tool', 'Kiest per casus wat mag, wat weg moet en wanneer voorleggen', 'Biedt een bruikbaar alternatief', 'Bespreekt toegang en auteurschap met studenten'],
        ['5 Leeractiviteit ontwerpen', 'Opdracht is af te ronden zonder het leerdoel', 'Leerdoel, onderbouwde AI-keuze en begripscontrole', 'Met een alternatief zonder AI', 'Getest met studenten en bijgesteld'],
        ['6 Toetsing en afspraken', 'Geen of vage AI-afspraken, of leunt op een detector', 'Duidelijke afspraken en een manier om individuele beheersing te zien', 'Met oog voor toegankelijkheid', 'Ingebed in het toetsprogramma'],
        ['7 Begeleiden', 'Gaat uit van fraude of kijkt alleen naar het product', 'Student legt keuze uit, controleert claim, formuleert vervolgstap', 'Herkent wanneer menselijke ondersteuning nodig is', 'Studenten verwoorden zelf hun AI-gebruik'],
        ['8 Blijven leren', 'Geen verbetering of plan', 'Eén verbetering na feedback en een controlemoment gepland', 'Deelt het voorbeeld met het team', 'Zet een cyclus op met collega\'s'],
    ]},
    notitie('let', 'Een onopgeloste kritieke fout vraagt eerst herstel. Denk aan herleidbare gegevens in een open tool, een verzonnen bron of onbewezen beheersing. Deze rubric is een concept: kalibreer hem vooraf met docenten en deskundigen.'),
    plaatshouder('Informatie over de edubadge (SURF) en hoe je je portfolio inlevert.'),
    doorgaan(),
    notitie('opdracht', '<p><strong>Praktijk.</strong> Bespreek je herontwerp met een collega. Verbeter het op basis van de feedback en geef het daarna in je les.</p>'),
    open_vraag('Welke verbetering bracht je aan na de feedback van je collega? Wanneer kijk je opnieuw naar dit ontwerp, en wat check je dan (tools, voorbeelden, afspraken van je instelling)?',
               'Bijvoorbeeld: elk semester tools en voorbeelden controleren, jaarlijks de leerdoelen herzien.'),
    open_vraag('Kijk terug naar je zelfscan uit de start. Wat kun je nu dat je toen nog niet kon? Waar wil je verder in groeien?'),
    competentie('8', 'je beschrijft één verbetering na collegiale feedback en plant wanneer je het voorbeeld opnieuw controleert.'),
    {'t': 'quote', 'body': 'Meer AI-gebruik is geen doel op zich. Goed onderwijs is het doel; AI is één van de keuzes.'},
]}

bronnen = {'id': 'bronnen', 'title': 'Bronnen en verantwoording', 'deadline': '', 'blocks': [
    tekst('Waar deze e-learning op is gebaseerd',
          'Deze e-learning bouwt op het onderzoek van de challenge "de revolutie van AI in het onderwijs" (Creator &amp; Development, november 2026). Het gaat om drie stukken: het rapport <em>Minimale AI-competenties voor hbo-docenten</em>, de <em>bewijs- en expertkaart AI in het hoger onderwijs</em> en het <em>advies online docentprofessionalisering op schaal</em>. De werkwijze in module 6 komt uit de AI-placemats en de docentinstructie daarbij.',
          'De acht competenties, de lesopzet en de beoordelingscriteria zijn een ontwerpvoorstel. Ze zijn nog niet gevalideerd en worden in een pilot getoetst.'),
    {'t': 'accordion', 'items': [
        {'title': 'Competentiekaders', 'body': p('Miao, F., &amp; Cukurova, M. (2024). <em>AI competency framework for teachers</em>. UNESCO.', 'Renkema, M., e.a. (2025). <em>AI-GO! Een raamwerk voor AI-geletterdheid in het onderwijs</em>. Npuls.', 'Theelen, H., e.a. (2026). <em>AI-GO in actie: Handreiking voor AI-geletterdheid in het onderwijs</em>. Npuls.', 'OECD. (2026). <em>OECD digital education outlook 2026</em>.')},
        {'title': 'Studies naar AI en leren', 'body': p('Kestin, G., e.a. (2025). AI tutoring outperforms in-class active learning. <em>Scientific Reports, 15</em>, 17458.', 'Bastani, H., e.a. (2025). Generative AI without guardrails can harm learning. <em>PNAS, 122</em>(26).', 'Fischer, M., Rau, H. A., &amp; Rilke, R. M. (2025). AI tutoring enhances student learning without crowding out reading effort. IZA Discussion Paper 18338.')},
        {'title': 'Toetsing', 'body': p('Lodge, J. M., Howard, S., Bearman, M., &amp; Dawson, P. (2023). <em>Assessment reform for the age of artificial intelligence</em>. TEQSA.', 'Perkins, M., Roe, J., Furze, L., e.a. (2024). The AI Assessment Scale revisited: A framework for educational assessment. arXiv:2412.09029. Zie ook aiassessmentscale.com.', 'Liu, D., &amp; Bridgeman, A. (2023-2025). Artikelen over de tweesporenaanpak (two-lane approach). Teaching@Sydney, University of Sydney.', 'HAN. (2025). <em>Toolkit AI-bestendig toetsen</em> (versie 2) en <em>Integraal AI-kader HAN 1.0</em>.')},
        {'title': 'Didactiek en professionalisering', 'body': p('Mollick, E., &amp; Mollick, L. (2023). <em>Assigning AI: Seven approaches for students, with prompts</em>. SSRN.', 'Sims, S., Fletcher-Wood, H., e.a. (2021). <em>What are the characteristics of effective teacher professional development?</em> EEF.', 'Kraft, M. A., Blazar, D., &amp; Hogan, D. (2018). The effect of teacher coaching on instruction and achievement. <em>Review of Educational Research, 88</em>(4).')},
    ]},
    notitie('let', 'Enquêtecijfers (HEPI 2026, DEC 2026) meten percepties, geen leereffect. De meta-analyse van Wang &amp; Fan is in april 2026 ingetrokken en wordt hier bewust niet als bewijs gebruikt. Controleer bij het invullen van echte content alle bronnen opnieuw.'),
]}

cursus = {
    'id': 'ai-didactisch-vaardig',
    'title': 'Onderwijs opnieuw ontwerpen met AI',
    'subtitle': 'Van AI-vaardig naar AI-didactisch vaardig: een basisprogramma voor hbo-docenten',
    'author': 'Creator & Development, challenge AI in het onderwijs (concept)',
    'intro': 'In tien korte modules leer je AI begrijpen en verantwoord gebruiken, en vooral: je onderwijs er bewust op ontwerpen. Je werkt de hele e-learning aan één eigen les, opdracht of toets. Reken op ongeveer twaalf uur, inclusief praktijk.',
    'ontwerp': {'sjabloon': 'han', 'boven': 'verloop', 'koppen': 'lijn'},
    'lessons': [m0, m1, m2, m3, m4, m5, m6, m7, m8, m9, bronnen],
}

with open(UIT, 'w', encoding='utf-8') as f:
    json.dump(cursus, f, ensure_ascii=False, indent=2)
n = sum(len(l['blocks']) for l in cursus['lessons'])
print('geschreven:', os.path.normpath(UIT), '-', len(cursus['lessons']), 'modules,', n, 'blokken')
