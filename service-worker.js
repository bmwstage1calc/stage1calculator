const CACHE_NAME = "bmw-stage1-calculator-v1";

const FILES_TO_CACHE = [
  "./",
  "./index.html",
  "./bmw_database.csv",
  "./bmw_logo.png"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(FILES_TO_CACHE);
    })
  );
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});