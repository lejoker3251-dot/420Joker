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
- `karte-rot.webp`, `karte-dame-lila.webp`, `karte-dame-rot.webp` – große Karten für Quiz-Ergebnis und Teilen-Bild
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

## Showreel (optional)
Lege `hero.mp4` (oder `hero.webm`) neben die `index.html`: 5 bis 8 Sekunden, stumm, unter 5 MB. Der Clip läuft hinter der Headline und als Fenster auf der 3D-Hero-Karte. Ohne Datei bleibt alles wie bisher.

## Einstellungen und Leistung
Im Footer unter "Einstellungen" schalten Besucher Ton, Vibration, 3D-Szene und weiches Scrollen. Läuft ein Gerät zu langsam, schaltet die Seite die 3D-Szene selbst ab und weist darauf hin.

## Quiz
Die Fragen stehen in `index.html`. Suche nach `var DQ=` (Tages-Quiz, je Frage: Text, drei Antworten, Nummer der richtigen Antwort ab 0) und `var TQ=` (Quiz "Welcher Joker bist du?"). Pro Tag erscheint eine Frage aus `DQ`.

## App (PWA)
Die Seite ist als App installierbar: `manifest.webmanifest`, `sw.js` (Offline-Speicher), `icon-*.png`, `screenshot-*.jpg`.
- Android/Chrome: Knopf "App installieren" im Album oder Footer. iPhone: Safari, Teilen, "Zum Home-Bildschirm" (die Seite zeigt eine Anleitung).
- Nach Änderungen an Bildern musst du nichts tun. Die Seite und `live.json`/`clips.json` kommen immer frisch aus dem Netz, Bilder werden im Hintergrund erneuert.
- Willst du alle Besucher zur Neuladung zwingen, erhöhe in `sw.js` die Zahl bei `const V = "joker-v1"`.
- `qr-420joker.png` ist der QR-Code zur Seite. Ändert sich die Adresse, muss er neu erzeugt werden.
- `stream-kalender.ics` ist der abonnierbare Stream-Kalender. Die Automatik (`AUTOMATIK`) füllt ihn aus `live.json`.

## Stream-Plan (`live.json`)
```json
"plan": [
  { "day": "Mi", "time": "19:00", "title": "Fortnite mit der Community", "platform": "twitch", "dur": 120 },
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
