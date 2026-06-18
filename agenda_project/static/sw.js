// Service Worker - Agenda Paola PWA
const CACHE_NAME = 'agenda-paola-v1';

// Archivos a guardar en caché para uso offline
const ASSETS_TO_CACHE = [
    '/',
    '/static/manifest.json',
    '/static/images/icono-192.png',
    '/static/images/icono-512.png',
];

// ── Instalación: guarda los archivos en caché ──
self.addEventListener('install', (event) => {
    console.log('[SW] Instalando Service Worker...');
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[SW] Guardando archivos en caché');
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
    self.skipWaiting();
});

// ── Activación: limpia cachés viejos ──
self.addEventListener('activate', (event) => {
    console.log('[SW] Activando Service Worker...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames
                    .filter((name) => name !== CACHE_NAME)
                    .map((name) => {
                        console.log('[SW] Eliminando caché antiguo:', name);
                        return caches.delete(name);
                    })
            );
        })
    );
    self.clients.claim();
});

// ── Fetch: responde con caché si está disponible, si no va a la red ──
self.addEventListener('fetch', (event) => {
    // Solo manejar peticiones GET
    if (event.request.method !== 'GET') return;

    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                return cachedResponse;
            }
            // No está en caché: va a la red
            return fetch(event.request).then((networkResponse) => {
                // Guarda en caché solo respuestas válidas de archivos estáticos
                if (
                    networkResponse.ok &&
                    event.request.url.includes('/static/')
                ) {
                    const responseClone = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseClone);
                    });
                }
                return networkResponse;
            }).catch(() => {
                // Sin conexión y sin caché: muestra página offline básica
                return new Response(
                    '<html><body><h1>Sin conexión</h1><p>Revisa tu conexión a internet.</p></body></html>',
                    { headers: { 'Content-Type': 'text/html' } }
                );
            });
        })
    );
});
