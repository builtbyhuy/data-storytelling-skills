// Optional PNG export. SVG creation/viewing requires no dependency.
// Requires the sharp package in your Node environment: node examples/render_previews.cjs
const sharp = require('sharp');
const path = require('node:path');
(async () => {
  for (const file of ['01-profit-decision/decision', '02-fair-comparison/comparison', '03-join-audit/join']) {
    const base = path.join(__dirname, file);
    await sharp(base + '.svg', { density: 144 }).resize(1800).png().toFile(base + '.png');
    process.stdout.write('Rendered ' + file + '.png\n');
  }
})().catch(err => { process.stderr.write(err.message + '\n'); process.exitCode = 1; });
