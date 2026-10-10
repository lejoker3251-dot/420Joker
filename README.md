# 420 Joker – Webseite

Fortnite Creator: Gaming auf TikTok, YouTube und Twitch. Creator-Code: **420 Joker**.

Statische Seite ohne Build-Schritt, läuft direkt auf GitHub Pages: https://lejoker3251-dot.github.io/420Joker/

## Dateien
- `index.html` – die Seite
- `impressum.html`, `datenschutz.html` – Pflichtseiten (vor dem Livegang ausfüllen)
- `live.json` – Live-Schalter und Stream-Plan
- `clips.json` – Clip-Liste
- `og-image.jpg`, `apple-touch-icon.png` – Vorschaubild für geteilte Links und App-Symbol
- `404.html`, `sitemap.xml` – Fehlerseite und Suchmaschinen-Angabe
- `thumb-*.webp` – Bilder der drei Kanal-Kacheln
- `wallpaper-*.jpg` – Handy-Hintergründe als Belohnung im Spiel
- `karte-*.webp`, `AgentOrange.woff` – Bilder und Schrift
- optional: `hero.mp4` – kurzer, stummer Loop (5 bis 8 Sekunden) für den Hero

## Live schalten (`live.json`)
```json
{ "twitch": true, "youtube": false, "tiktok": false, "plan": [] }
```
`true` setzen, speichern (Commit). Nach 1 bis 2 Minuten zeigt die Seite „LIVE“. Danach wieder auf `false`.

## Banner und Zahlen (`live.json`)
```json
"banner": { "text": "Neue Season: Code 420 Joker", "url": "#creator-code" },
"stats": { "tiktok": 2886, "youtube": 1, "twitch": 0 }
```
- Der Banner erscheint oben. Mit `"banner": {}` oder leerem Text verschwindet er.
- Zahlen unter 100 zeigt die Seite nicht an. Trage sie trotzdem ein, sie erscheinen von selbst, sobald sie die Schwelle erreichen.

## Wochen-Challenge und Shop-Link (`live.json`)
```json
"challenge": { "title": "Diese Woche: 10 Siege", "current": 4, "goal": 10 },
"shopUrl": "https://www.fortnite.com/item-shop/offers/..."
```
- Die Challenge erscheint im Community-Band mit Fortschrittsbalken. Ohne `challenge` bleibt sie unsichtbar.
- `shopUrl` ist der Epic-Shop-Link mit deinem Code (Fortnite.com, Item-Shop, Teilen-Symbol). Nur Adressen von fortnite.com werden akzeptiert.

## Stream-Plan (`live.json`)
```json
"plan": [
  { "day": "Mi", "time": "19:00", "title": "Fortnite mit der Community", "platform": "twitch" },
  { "day": "Fr", "time": "20:00", "title": "Ranked-Session", "platform": "twitch" }
]
```
Solange kein Eintrag da ist, zeigt die Seite „Coming soon“. Plattformen: `twitch`, `youtube`, `tiktok`.

## Clips (`clips.json`)
```json
[
  { "title": "Mein bester Clip", "platform": "youtube", "url": "https://www.youtube.com/watch?v=...", "thumb": "clip1.jpg" }
]
```
Das Vorschaubild (`thumb`) als Datei im Repository ablegen. Bis zu 6 Clips.
