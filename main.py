from flask import Flask, render_template_string, request

app = Flask(__name__)

# -------------------- DATA --------------------
teams = [
    {
        "name": "Team Vitality",
        "country": "France",
        "founded": 2013,
        "coach": "XTQZZZ",
        "ranking": "#1-3 a világranglistán",
        "achievements": [
            "IEM Rio 2023 győzelem",
            "BLAST Premier Finals bajnok",
            "Rendszeres playoff résztvevő minden nagyobb LAN-on"
        ],
        "players": ["ZywOo", "flameZ", "apEX", "mezii", "spinX"]
    },
    {
        "name": "FaZe Clan",
        "country": "International",
        "founded": 2010,
        "coach": "RobbaN",
        "ranking": "Stabil TOP5",
        "achievements": [
            "Intel Grand Slam győzelem",
            "PGL Antwerp 2022 Major bajnok",
            "HLTV #1 csapat több hónapon át"
        ],
        "players": ["karrigan", "broky", "rain", "frozen", "ropz"]
    },
    {
        "name": "Natus Vincere",
        "country": "Ukraine",
        "founded": 2009,
        "coach": "b1ad3",
        "ranking": "TOP8-as csapat",
        "achievements": [
            "PGL Major Stockholm 2021 bajnok",
            "PGL CS2 Major Copenhagen 2024 bajnok",
            "S1mple MVP címek sorozata"
        ],
        "players": ["Aleksib", "b1t", "iM", "JL", "w0nderful"]
    },
    {
        "name": "G2 Esports",
        "country": "Europe",
        "founded": 2014,
        "coach": "TaZ",
        "ranking": "TOP10",
        "achievements": [
            "IEM Katowice 2023 bajnok",
            "BLAST World Final győzelem",
            "NiKo & m0NESY ikonikus párosa"
        ],
        "players": ["NiKo", "huNter-", "HooXi", "nexa", "m0NESY"]
    },
]

players = [
    {
        "name": "ZywOo",
        "team": "Team Vitality",
        "role": "AWPer / Carry",
        "rating": 1.31,
        "age": 24,
        "country": "France",
        "bio": "ZywOo az egyik legkomplettebb játékos a CS történetében. hihetetlen clutchek, stabil aim, és nagyon kevés hiba."
    },
    {
        "name": "NiKo",
        "team": "G2 Esports",
        "role": "Rifler / Star player",
        "rating": 1.20,
        "age": 27,
        "country": "Bosnia and Herzegovina",
        "bio": "NiKo híres entry fragjeiről és brutális AK-47 kontrolljáról. Sokszor ő nyitja meg a kört a csapata számára."
    },
    {
        "name": "ropz",
        "team": "FaZe Clan",
        "role": "Lurker",
        "rating": 1.18,
        "age": 24,
        "country": "Estonia",
        "bio": "Ropz a világ egyik legokosabb lurkere. Türelemmel, jó pozicionálással és időzítéssel szedi szét az ellenfelet."
    },
    {
        "name": "b1t",
        "team": "Natus Vincere",
        "role": "Rifler / Anchor",
        "rating": 1.12,
        "age": 21,
        "country": "Ukraine",
        "bio": "b1t híres a headshot százalékáról és erős defensív pozíciófogásáról CT oldalon."
    },
]

events = [
    {
        "name": "PGL CS2 Major Copenhagen 2024",
        "winner": "Natus Vincere",
        "location": "Copenhagen",
        "prize_pool": "$1,250,000+",
        "mvp": "b1t",
        "highlights": [
            "Első CS2 Major a történelemben",
            "Új MR12 rendszer bevezetése",
            "Meta alakulása: utility még fontosabb lett"
        ]
    },
    {
        "name": "IEM Katowice",
        "winner": "Team Vitality",
        "location": "Katowice, Spodek Aréna",
        "prize_pool": "$1,000,000",
        "mvp": "ZywOo",
        "highlights": [
            "Az egyik legrangosabb nem-Major torna",
            "Spodek legendás atmoszférája",
            "A playoff meccsek szinte mindig teltház előtt mennek"
        ]
    },
    {
        "name": "BLAST Premier World Final",
        "winner": "FaZe Clan",
        "location": "Abu Dhabi",
        "prize_pool": "$1,000,000",
        "mvp": "ropz",
        "highlights": [
            "Szezon lezáró csúcstorna",
            "Csak a legjobb, meghívott csapatok indulhatnak",
            "FaZe domináns playoff futása"
        ]
    },
]

maps_data = [
    {
        "name": "Mirage",
        "type": "Balanced",
        "difficulty": "Közepes",
        "description": "Mirage az egyik legikonikusabb pálya. T és CT oldal is rengeteg lehetőséget ad taktikázásra.",
        "tips_t": [
            "Alap smoke execute A-ra: Jungle, Stairs, CT smokes",
            "B split: B apartments + Short kontroll midről",
            "Mid kontroll korai roundban – smoke top mid, flash ablakra"
        ],
        "tips_ct": [
            "Ne add fel könnyen a mide-t, használj agresszív ablak/jungle pozikat",
            "A site-on gyakori setup: CT + Stairs + Under balcony crossfire",
            "B site-on fontos az információ visszahúzódás után is (rádió, utility)"
        ]
    },
    {
        "name": "Inferno",
        "type": "CT-sided",
        "difficulty": "Közepes–nehéz",
        "description": "Inferno híres a szűk chokepointokról, főleg Banana és Apartments környékén.",
        "tips_t": [
            "Banana kontroll kör elején molotov + flash kombóval",
            "Fake executes – utility elköltése egy site-ra, majd gyors rotate",
            "Apps + Short + Long triplaszorítás A-ra"
        ],
        "tips_ct": [
            "Banana dupla HE és molotov T oldali rush ellen",
            "Rotáció gyors B és A között – jó kommunikáció szükséges",
            "Pit játékos kulcsfontosságú A site védésénél"
        ]
    },
    {
        "name": "Nuke",
        "type": "CT-sided",
        "difficulty": "Nehéz",
        "description": "Vertikális pálya, két szinttel (A és B). Sok boost, szög és taktika.",
        "tips_t": [
            "Yard smokes: Secret smoke, Red smoke, Garage smoke",
            "Outside kontroll után lejutás Secretre és B execute",
            "A site-ra gyors vent dive strat, ha az ellenfél nem figyel rá"
        ],
        "tips_ct": [
            "Yard információ: agresszív push vagy opció AWPerrel",
            "Ramp játékos rotáljon gyorsan B-re, ha nagy nyomás van rajta",
            "Ajtó és Hut kontroll A-n – molotovokkal törjük meg a gyors T pusht"
        ]
    },
    {
        "name": "Anubis",
        "type": "T-sided",
        "difficulty": "Közepes",
        "description": "Anubis újabb pálya, vízzel, hidakkal és sok átlőhető fallal.",
        "tips_t": [
            "Korai mid kontroll nagy előnyt ad",
            "A hosszú (A Long) smoke + flash kombóval vehető át biztonságosan",
            "B site on executes: smokes a fő bejáratokra, egy lurker midről"
        ],
        "tips_ct": [
            "Aggresszív mid push meglepheti a T-ket",
            "Rotációk lerövidítése: középső útvonalak figyelése",
            "Utility fontos a site belépések lassításához"
        ]
    },
]

tactics = {
    "t_side": [
        "Fast A exec Mirage-on: két ember Palace, három Ramp, egyszerre kifutás full utility-vel.",
        "Banana kontroll Infernon: két molotov, két HE, egy deep smoke és utána agresszív felpush.",
        "Nuke yard smoke wall + Secret creep, majd B site exec flashes-szel és molotovval a fontos pozikra.",
    ],
    "ct_side": [
        "Double AWP setup Mirage-on: egy mid, egy B – nagy mapkontroll, de drága.",
        "Inferno tripla A setup: Pit + Site + Library, miközben B-n csak egy anchor és egy rotáló.",
        "Aggresszív ramp push Nuke-on, ha tudod, hogy az ellenfél lassan játszik.",
    ],
    "utility": [
        "Popflash: olyan flash, ami az ellenfél feje felett robban, de téged nem vakít.",
        "Lineup: pontos pozíció + irány, ahonnan/ahová dobod a gránátot, hogy mindig ugyanoda essen.",
        "Anti-rush utility: korai molotovok és HE-k, hogy megállítsd a gyors T támadást."
    ]
}

facts = [
    "A CS 1999-ben jelent meg Half-Life modként, a CS2 pedig 2023-ban váltotta a CS:GO-t.",
    "A Major tornák a CS legnagyobb presztízsű eseményei, Valve szponzorációval.",
    "Egy profi CS2 meccs során a játékosok gyakran több mint 8 órát is gyakorolnak naponta.",
    "A kommunikáció legalább annyira fontos, mint az aim – a top csapatok rengeteget gyakorolják a callokat.",
    "Az első nagyobb LAN-tornákat netkávézókban, viszonylag kis pénzdíjazással rendezték.",
    "HLTV rating 2.0 egy komplex mutató, ami figyelembe veszi a kill/death arányt, hatást, clutchokat és sok mást.",
    "Sok profi játékos edzővel, pszichológussal és dietetikussal is dolgozik.",
    "A modern CS2 meta nagyon utility-központú – smoke, molotov és flash nélkül nehéz köröket nyerni.",
    "A legtöbb profi játékos 800–1200 eDPI környékén játszik.",
    "LAN környezetben teljesen más a hangulat: nincs ping, de ott a közönség nyomása."
]