#!/usr/bin/env python3
"""Auto-Update für die 420-Joker-Seite (läuft in GitHub Actions).

- YouTube: neueste Videos -> clips.json (Vorschaubilder werden ins Repository geladen)
- Discord: Mitgliederzahl -> live.json ("stats" -> "discord")
- Twitch (optional): Live-Status -> live.json ("twitch"), nur mit Secrets
Alles ist fehlertolerant: Ein Fehler in einem Teil stoppt die anderen nicht.
"""
import json, os, re, sys, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
YT_HANDLE = os.environ.get("YT_HANDLE", "Real420Joker")
YT_CHANNEL_ID = os.environ.get("YT_CHANNEL_ID", "")
TWITCH_LOGIN = os.environ.get("TWITCH_LOGIN", "LeJoker3251")
DISCORD_INVITE = os.environ.get("DISCORD_INVITE", "5wPdtbftAr")
MAX_CLIPS, MAX_AUTO = 6, 4
UA = {"User-Agent": "Mozilla/5.0 (joker-auto-update)"}


def http_get(url, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()


def http_post(url, data, headers=None):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, headers={**UA, **(headers or {})}, method="POST")
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json_if_changed(path, obj):
    new = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    p = Path(path)
    if p.exists() and p.read_text(encoding="utf-8") == new:
        return False
    p.write_text(new, encoding="utf-8")
    return True


def resolve_channel_id():
    if YT_CHANNEL_ID:
        return YT_CHANNEL_ID
    page = http_get("https://www.youtube.com/@" + YT_HANDLE).decode("utf-8", "ignore")
    m = re.search(r'"channelId":"(UC[A-Za-z0-9_-]{22})"', page) or re.search(r"channel/(UC[A-Za-z0-9_-]{22})", page)
    if not m:
        raise RuntimeError("YouTube-Kanal-ID nicht gefunden")
    return m.group(1)


def update_clips():
    cid = resolve_channel_id()
    xml = http_get("https://www.youtube.com/feeds/videos.xml?channel_id=" + cid)
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
    root = ET.fromstring(xml)
    auto = []
    for e in root.findall("a:entry", ns)[:MAX_AUTO]:
        vid = e.findtext("yt:videoId", default="", namespaces=ns)
        title = (e.findtext("a:title", default="", namespaces=ns) or "").strip()[:80]
        if not re.fullmatch(r"[A-Za-z0-9_-]{6,20}", vid):
            continue
        thumb = ROOT / "clips" / ("yt-%s.jpg" % vid)
        if not thumb.exists():
            thumb.parent.mkdir(exist_ok=True)
            data = None
            for q in ("maxresdefault", "hqdefault"):
                try:
                    data = http_get("https://i.ytimg.com/vi/%s/%s.jpg" % (vid, q))
                    break
                except Exception:
                    continue
            if data:
                thumb.write_bytes(data)
        auto.append({"title": title, "platform": "youtube",
                     "url": "https://www.youtube.com/watch?v=" + vid,
                     "thumb": ("clips/yt-%s.jpg" % vid) if thumb.exists() else ""})
    manual = read_json(ROOT / "clips-manual.json", [])
    if not isinstance(manual, list):
        manual = []
    seen, clips = set(), []
    for c in manual + auto:
        if c.get("url") and c["url"] not in seen:
            seen.add(c["url"])
            clips.append(c)
    clips = clips[:MAX_CLIPS]
    changed = write_json_if_changed(ROOT / "clips.json", clips)
    keep = {Path(c.get("thumb", "")).name for c in clips}
    for old in (ROOT / "clips").glob("yt-*.jpg") if (ROOT / "clips").exists() else []:
        if old.name not in keep:
            old.unlink()
            changed = True
    return changed


def update_discord(live):
    raw = http_get("https://discord.com/api/v10/invites/%s?with_counts=true" % DISCORD_INVITE)
    n = int(json.loads(raw).get("approximate_member_count", 0))
    if n <= 0:
        return False
    stats = live.setdefault("stats", {})
    if stats.get("discord") == n:
        return False
    stats["discord"] = n
    return True


def update_twitch(live):
    cid, sec = os.environ.get("TWITCH_CLIENT_ID"), os.environ.get("TWITCH_CLIENT_SECRET")
    if not (cid and sec):
        return False
    tok = json.loads(http_post("https://id.twitch.tv/oauth2/token",
                               {"client_id": cid, "client_secret": sec, "grant_type": "client_credentials"}))["access_token"]
    raw = http_get("https://api.twitch.tv/helix/streams?user_login=" + urllib.parse.quote(TWITCH_LOGIN),
                   {"Client-Id": cid, "Authorization": "Bearer " + tok})
    is_live = len(json.loads(raw).get("data", [])) > 0
    if live.get("twitch") == is_live:
        return False
    live["twitch"] = is_live
    return True


def main():
    live_path = ROOT / "live.json"
    live = read_json(live_path, {})
    changed = False
    for name, fn in (("YouTube", lambda: update_clips()), ("Discord", lambda: update_discord(live)), ("Twitch", lambda: update_twitch(live))):
        try:
            if fn():
                changed = True
                print("aktualisiert:", name)
            else:
                print("unverändert:", name)
        except Exception as ex:
            print("übersprungen:", name, "-", ex)
    if changed and write_json_if_changed(live_path, live):
        print("live.json gespeichert")
    return 0


if __name__ == "__main__":
    sys.exit(main())
