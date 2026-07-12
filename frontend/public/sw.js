// Service Worker basique pour le cache hors-ligne
const CACHE_NAME = 'footgolf-cache-v2'; // Bump version
const OFFLINE_URL = '/offline.html';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      // Pré-cache des assets de base et de la page hors-ligne
      return cache.addAll([
        '/',
        OFFLINE_URL,
        '/manifest.webmanifest',
      ]);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Ignore Next.js dev server and specific internal files
  if (
    url.pathname.startsWith('/_next/') ||
    url.pathname.includes('webpack') ||
    url.pathname === '/__nextjs_original-stack-frame' ||
    event.request.headers.get('accept')?.includes('text/event-stream')
  ) {
    return; // Ne pas intercepter
  }

  // Stratégie Network First pour l'API
  if (url.pathname.startsWith('/api/v1/')) {
    event.respondWith(
      fetch(event.request).catch(() => {
        return caches.match(event.request);
      })
    );
    return;
  }

  // Stale-While-Revalidate pour le reste
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      const fetchPromise = fetch(event.request).then((networkResponse) => {
        if (
          event.request.method === 'GET' &&
          networkResponse.status === 200 &&
          (url.protocol === 'http:' || url.protocol === 'https:')
        ) {
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, networkResponse.clone());
          });
        }
        return networkResponse;
      }).catch(() => {
        if (event.request.mode === 'navigate') {
          return caches.match(OFFLINE_URL);
        }
      });

      return cachedResponse || fetchPromise;
    })
  );
});
