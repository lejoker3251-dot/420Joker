/* 420 Joker – Service Worker
   Strategie: Seiten und Daten zuerst aus dem Netz (immer frisch), Bilder und Schrift aus dem Speicher
   und im Hintergrund erneuert. Ohne Netz läuft die Seite aus dem Speicher weiter. */
const V = "joker-v1";
const CORE = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "apple-touch-icon.png",
  "karte-lila.webp", "karte-lila-klein.webp", "karte-rot-klein.webp", "karte-rot2-klein.webp", "karte-dame-lila-klein.webp",
  "thumb-youtube.webp", "thumb-twitch.webp", "thumb-tiktok.webp", "AgentOrange.woff", "qr-420joker.png",
  "impressum.html", "datenschutz.html"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(V).then(c => Promise.allSettled(CORE.map(u => c.add(new Request(u, { cache: "reload" }))))).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

const isData = u => /\.(json|ics)$/.test(u.pathname);

async function networkFirst(req, fallbackUrl) {
  const c = await caches.open(V);
  try {
    const r = await fetch(req);
    if (r && r.ok) c.put(req, r.clone());
    return r;
  } catch (err) {
    const hit = await c.match(req, { ignoreSearch: true }) || (fallbackUrl && await c.match(fallbackUrl));
    if (hit) return hit;
    throw err;
  }
}
async function staleWhileRevalidate(req) {
  const c = await caches.open(V);
  const hit = await c.match(req);
  const net = fetch(req).then(r => { if (r && r.ok) c.put(req, r.clone()); return r; }).catch(() => null);
  return hit || (await net) || Response.error();
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const u = new URL(req.url);
  if (u.origin !== location.origin) return;
  if (req.mode === "navigate") { e.respondWith(networkFirst(req, "index.html")); return; }
  if (isData(u)) { e.respondWith(networkFirst(req)); return; }
  e.respondWith(staleWhileRevalidate(req));
});
