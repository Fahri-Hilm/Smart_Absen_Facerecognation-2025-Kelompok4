/**
 * KAFEBASABASI - Service Worker
 * Offline Support & Caching v1.0
 */

const CACHE_NAME = 'kafebasabasi-v1.2';
const OFFLINE_URL = '/offline.html';

// Files to cache for offline functionality
const urlsToCache = [
    '/',
    '/static/css/modern-ui.css',
    '/static/js/attendance-optimized.js',
    '/static/bootstrap/css/bootstrap.min.css',
    '/static/bootstrap/js/bootstrap.bundle.min.js',
    '/static/bootstrap-icons/font/bootstrap-icons.css',
    '/static/face_recognition_model.pkl',
    '/offline.html'
];

// Install event - cache resources
self.addEventListener('install', event => {
    console.log('Service Worker: Installing...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Service Worker: Caching files...');
                return cache.addAll(urlsToCache);
            })
            .then(() => {
                console.log('Service Worker: All files cached');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('Service Worker: Cache failed', error);
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    console.log('Service Worker: Activating...');
    
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Service Worker: Deleting old cache', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            console.log('Service Worker: Activated');
            return self.clients.claim();
        })
    );
});

// Fetch event - serve cached content when offline
self.addEventListener('fetch', event => {
    const { request } = event;
    
    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }
    
    // Skip external requests
    if (!request.url.startsWith(self.location.origin)) {
        return;
    }
    
    // Handle attendance marking requests
    if (request.url.includes('/mark_attendance')) {
        event.respondWith(handleAttendanceRequest(request));
        return;
    }
    
    // Handle API requests
    if (request.url.includes('/api/') || request.url.includes('/get_')) {
        event.respondWith(handleApiRequest(request));
        return;
    }
    
    // Handle regular requests
    event.respondWith(
        caches.match(request)
            .then(response => {
                // Return cached version if available
                if (response) {
                    console.log('Service Worker: Serving from cache', request.url);
                    return response;
                }
                
                // Try to fetch from network
                return fetch(request)
                    .then(response => {
                        // Don't cache non-successful responses
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }
                        
                        // Clone the response for caching
                        const responseToCache = response.clone();
                        
                        // Cache static resources
                        if (shouldCache(request.url)) {
                            caches.open(CACHE_NAME)
                                .then(cache => {
                                    cache.put(request, responseToCache);
                                });
                        }
                        
                        return response;
                    })
                    .catch(() => {
                        // Network failed, try to serve offline page
                        if (request.destination === 'document') {
                            return caches.match(OFFLINE_URL);
                        }
                        
                        // For other resources, return empty response
                        return new Response('', {
                            status: 200,
                            statusText: 'OK'
                        });
                    });
            })
    );
});

// Handle attendance marking with offline queueing
async function handleAttendanceRequest(request) {
    try {
        // Try network first
        const response = await fetch(request);
        
        if (response.ok) {
            // Clear any queued requests on success
            await clearOfflineQueue();
            return response;
        }
        
        throw new Error('Network response not ok');
        
    } catch (error) {
        console.log('Service Worker: Queueing attendance request for later');
        
        // Queue the request for when network is available
        await queueOfflineRequest(request);
        
        // Return pending response
        return new Response(JSON.stringify({
            status: 'pending',
            message: 'Absensi sedang diproses. Data akan tersimpan saat koneksi tersedia.'
        }), {
            status: 202,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}

// Handle API requests with cache fallback
async function handleApiRequest(request) {
    try {
        // Try network first for API requests
        const response = await fetch(request);
        
        if (response.ok) {
            // Cache successful API responses for short time
            const cache = await caches.open(CACHE_NAME);
            const responseToCache = response.clone();
            
            // Set expiration for API cache (5 minutes)
            const expiresAt = new Date(Date.now() + 5 * 60 * 1000).toISOString();
            responseToCache.headers.set('SW-Cache-Expires', expiresAt);
            
            await cache.put(request, responseToCache);
            return response;
        }
        
        throw new Error('API response not ok');
        
    } catch (error) {
        // Try to serve from cache
        const cachedResponse = await caches.match(request);
        
        if (cachedResponse) {
            // Check if cache is still valid
            const expiresAt = cachedResponse.headers.get('SW-Cache-Expires');
            if (expiresAt && new Date(expiresAt) > new Date()) {
                console.log('Service Worker: Serving API from cache', request.url);
                return cachedResponse;
            }
        }
        
        // Return empty data response for API failures
        return new Response(JSON.stringify({
            status: 'offline',
            message: 'Data tidak tersedia saat offline',
            data: []
        }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}

// Queue offline requests
async function queueOfflineRequest(request) {
    try {
        const requestData = {
            url: request.url,
            method: request.method,
            headers: Object.fromEntries(request.headers.entries()),
            body: await request.text(),
            timestamp: Date.now()
        };
        
        // Get existing queue
        const queue = await getOfflineQueue();
        queue.push(requestData);
        
        // Store updated queue
        await setOfflineQueue(queue);
        
    } catch (error) {
        console.error('Service Worker: Failed to queue request', error);
    }
}

// Get offline queue from storage
async function getOfflineQueue() {
    try {
        const cache = await caches.open(CACHE_NAME);
        const response = await cache.match('/offline-queue');
        
        if (response) {
            const data = await response.json();
            return data.queue || [];
        }
        
        return [];
    } catch (error) {
        console.error('Service Worker: Failed to get offline queue', error);
        return [];
    }
}

// Set offline queue in storage
async function setOfflineQueue(queue) {
    try {
        const cache = await caches.open(CACHE_NAME);
        const response = new Response(JSON.stringify({ queue }), {
            headers: { 'Content-Type': 'application/json' }
        });
        
        await cache.put('/offline-queue', response);
    } catch (error) {
        console.error('Service Worker: Failed to set offline queue', error);
    }
}

// Clear offline queue
async function clearOfflineQueue() {
    try {
        const cache = await caches.open(CACHE_NAME);
        await cache.delete('/offline-queue');
    } catch (error) {
        console.error('Service Worker: Failed to clear offline queue', error);
    }
}

// Process offline queue when network is available
async function processOfflineQueue() {
    try {
        const queue = await getOfflineQueue();
        
        if (queue.length === 0) {
            return;
        }
        
        console.log(`Service Worker: Processing ${queue.length} queued requests`);
        
        const processedQueue = [];
        
        for (const requestData of queue) {
            try {
                // Skip requests older than 24 hours
                if (Date.now() - requestData.timestamp > 24 * 60 * 60 * 1000) {
                    continue;
                }
                
                const response = await fetch(requestData.url, {
                    method: requestData.method,
                    headers: requestData.headers,
                    body: requestData.body
                });
                
                if (!response.ok) {
                    // Keep failed requests in queue for retry
                    processedQueue.push(requestData);
                }
                
            } catch (error) {
                // Keep failed requests in queue for retry
                processedQueue.push(requestData);
            }
        }
        
        // Update queue with only failed requests
        await setOfflineQueue(processedQueue);
        
        // Notify client about processed requests
        if (queue.length > processedQueue.length) {
            const clients = await self.clients.matchAll();
            clients.forEach(client => {
                client.postMessage({
                    type: 'offline-queue-processed',
                    processed: queue.length - processedQueue.length,
                    remaining: processedQueue.length
                });
            });
        }
        
    } catch (error) {
        console.error('Service Worker: Failed to process offline queue', error);
    }
}

// Monitor network status
self.addEventListener('online', () => {
    console.log('Service Worker: Network available, processing offline queue');
    processOfflineQueue();
});

// Background sync for offline requests
self.addEventListener('sync', event => {
    if (event.tag === 'attendance-sync') {
        console.log('Service Worker: Background sync triggered');
        event.waitUntil(processOfflineQueue());
    }
});

// Message handling from clients
self.addEventListener('message', event => {
    const { data } = event;
    
    if (data.type === 'skip-waiting') {
        self.skipWaiting();
    } else if (data.type === 'check-offline-queue') {
        getOfflineQueue().then(queue => {
            event.ports[0].postMessage({
                type: 'offline-queue-status',
                count: queue.length
            });
        });
    }
});

// Determine if URL should be cached
function shouldCache(url) {
    // Cache static resources
    if (url.includes('/static/')) {
        return true;
    }
    
    // Cache main pages
    if (url === self.location.origin + '/' || 
        url === self.location.origin + '/qr_auth') {
        return true;
    }
    
    return false;
}

// Periodic cache cleanup
setInterval(() => {
    caches.open(CACHE_NAME).then(cache => {
        cache.keys().then(requests => {
            requests.forEach(request => {
                cache.match(request).then(response => {
                    if (response) {
                        const expiresAt = response.headers.get('SW-Cache-Expires');
                        if (expiresAt && new Date(expiresAt) < new Date()) {
                            console.log('Service Worker: Removing expired cache', request.url);
                            cache.delete(request);
                        }
                    }
                });
            });
        });
    });
}, 10 * 60 * 1000); // Every 10 minutes

console.log('Service Worker: Loaded and ready');