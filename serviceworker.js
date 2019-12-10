const assetCacheName = 'assets';
const pageCacheName = 'pages';

addEventListener( 'install', installEvent => {
  skipWaiting();
  installEvent.waitUntil(
    caches.open( assetCacheName )
    .then( assetCache => {
      return assetCache.add('/offline');
    })
  );
});

addEventListener( 'activate', activateEvent => {
  clients.claim();
});

addEventListener( 'fetch', fetchEvent => {
  const request = fetchEvent.request;

  // Ignore non-GET requests
  if ( request.method !== 'GET' ) {
    return;
  }

  // Ignore video requests because of Safari's range bug https://philna.sh/blog/2018/10/23/service-workers-beware-safaris-range-request/
  if ( request.url.match(/\.(mp4)$/) ) {
    return;
  }

  // For pages, try the network first, then the cache
  if ( request.mode === 'navigate' ) {
    fetchEvent.respondWith(
      fetch( request )
      .then( responseFromFetch => {
        // Cache a copy of any pages you fetch
        if ( responseFromFetch.status < 400 ) {
          let copy = responseFromFetch.clone();
          fetchEvent.waitUntil(
            caches.open( pageCacheName )
            .then( pageCache => {
              return pageCache.put( request, copy );
            })
          );
        }
        return responseFromFetch;
      })
      .catch( error => {
        return caches.match( request )
        .then( responseFromCache => {
          if ( responseFromCache ) {
            return responseFromCache;
          }
          // As a last resort, show an offline page
          return caches.match('/offline/');
        })
      })
    );
    return;
  }

  // For everything else, try the cache first, then the network
  fetchEvent.respondWith(
    caches.match( request )
    .then( responseFromCache => {
      if ( responseFromCache ) {
        // Refresh the cache with a fresh version of this file from the network
        fetchEvent.waitUntil(
          fetch( request )
          .then( responseFromFetch => {
            caches.open( assetCacheName )
            .then( assetCache => {
              return assetCache.put( request, responseFromFetch );
            })
          })
        );
        return responseFromCache;
      }
      return fetch( request )
      .then( responseFromFetch => {
        // Cache any files you fetch
        let copy = responseFromFetch.clone();
        fetchEvent.waitUntil(
          caches.open( assetCacheName )
          .then( assetCache => {
            return assetCache.put( request, copy );
          })
        );
        return responseFromFetch;
      })
      .catch( error => {
        // As a last resort, show an offline image (if the request if for an image)
        if ( request.url.match(/\.(jpe?g|png|gif|svg)$/) ) {
          return new Response(`
            <svg role="img" aria-labelledby="offline-title" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
              <title id="offline-title">Offline</title>
              <g fill="none" fill-rule="evenodd">
                <path fill="#D8D8D8" d="M0 0h400v300H0z"/>
                <text fill="#9B9B9B" font-family="Helvetica Neue,Arial,Helvetica,sans-serif" font-size="72" font-weight="bold">
                  <tspan x="93" y="172">offline</tspan>
                </text>
              </g>
            </svg>`,
            {
              headers: {
                'Content-Type': 'image/svg+xml',
                'Cache-Control': 'no-store'
              }
            }
          );
        }
      })
    })
  );

});
