self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open("gmc-cache-v1").then((cache) => {
      return cache.addAll([
        "./",
        "./index.html",
        "./main.pyz",
        "./logo.png"
      ]);
    })
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
