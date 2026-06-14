const http = require('http');
const fs = require('fs');
const path = require('path');
const root = 'D:\\OPENCODE_0621\\tamsui-new-town-water-electric-site';
const server = http.createServer((req, res) => {
  // Decode URL (handle Chinese filenames)
  const decoded = decodeURIComponent(req.url);
  let f = path.join(root, decoded === '/' ? 'index.html' : decoded);
  f = path.normalize(f);
  if (!f.startsWith(root)) { res.writeHead(403); res.end('Forbidden'); return; }
  const ext = path.extname(f);
  const ct = { '.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.png':'image/png','.jpg':'image/jpeg','.json':'application/json','.svg':'image/svg+xml','.ico':'image/x-icon','.md':'text/plain' }[ext] || 'text/plain';
  fs.readFile(f, (err, data) => {
    if (err) { res.writeHead(404); res.end('Not Found: ' + f); return; }
    res.writeHead(200, { 'Content-Type': ct, 'Access-Control-Allow-Origin': '*' });
    res.end(data);
  });
});
server.listen(8002, () => console.log('Server at http://localhost:8002'));