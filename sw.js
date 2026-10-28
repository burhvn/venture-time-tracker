/* Tracker service worker — offline app shell, live data always from network. */
const CACHE = 'tracker-v1';
const ASSETS = [
  './', './index.html', './manifest.webmanifest',
  './icon.svg', './icon-192.png', './icon-512.png',
  './icon-maskable-512.png', './apple-touch-icon.png'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(ASSETS))
      .catch(() => {})
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // Live data: never cache — let it go straight to the network.
  if (url.pathname.endsWith('/api/data') || /\/(time-data|timers)\.json$/.test(url.pathname)) return;

  // App shell / navigations: network-first so updates land, fall back to cache offline.
  if (req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html')) {
    e.respondWith(
      fetch(req)
        .then(r => { const cp = r.clone(); caches.open(CACHE).then(c => c.put('./index.html', cp)); return r; })
        .catch(() => caches.match('./index.html').then(m => m || caches.match('./')))
    );
    return;
  }

  // Static assets + CDN (Chart.js): cache-first, then network, caching what we fetch.
  e.respondWith(
    caches.match(req).then(hit => hit || fetch(req).then(r => {
      if (r && (r.ok || r.type === 'opaque')) {
        const cp = r.clone();
        caches.open(CACHE).then(c => c.put(req, cp));
      }
      return r;
    }).catch(() => hit))
  );
});
