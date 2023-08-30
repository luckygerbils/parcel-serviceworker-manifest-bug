# Reproducing

```
$ git clone https://github.com/luckygerbils/parcel-serviceworker-manifest-bug
$ cd parcel-serviceworker-manifest-bug
$ npm install
$ npx parcel build src/index.html
```

Note the output includes two `index.{hash}.js` files, both of which are referenced by the built `dist/index.html`:

```
✨ Built in 1.75s

dist/index.html              256 B    643ms
dist/index.086234c1.js    98.88 KB    236ms
dist/service-worker.js       183 B    593ms
dist/index.881f056f.js     1.07 KB    236ms
```

`dist/index.html` (manually formatted for this readme)
```
<!doctype html><html lang="en">
<head>
  <meta charset="utf-8">
  <script type="module" src="/index.881f056f.js"></script>
  <script type="module" src="/index.086234c1.js"></script>
</head>
<body> <h1>Hello, World!</h1> </body>
</html>
```

However only one of these index.js files is included in the generated service worker manifest:

```
$ grep 'Service Worker manifest is' dist/service-worker.js
console.log("Service Worker manifest is",["/index.html","/index.086234c1.js"]);//# sourceMappingURL=service-worker.js.map
```

Since the other file isn't included, it isn't cached by a service worker using this manifest to prepopulate the cache ([as in the docs here](https://parceljs.org/languages/javascript/#service-workers)) and so this file will be missing if the website is reloaded offline.

This appears to only happen if the bundle size is greater than ~100KB (presumably code splitting is coming into effect then)
