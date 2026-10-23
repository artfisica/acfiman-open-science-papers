// Run with node --test tests/portal.cjs; no browser dependencies required.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');

test('resize preserves PDF until paper or breakpoint changes', async () => {
  const elements = new Map();
  let assignments = 0;
  let desktop = true;
  const viewer = {
    source: 'pdf/comunidades.pdf#view=FitH',
    getAttribute() { return this.source; },
    hasAttribute() { return this.source !== null; },
    setAttribute(name, value) { this.source = value; assignments++; },
    removeAttribute() { this.source = null; },
  };
  const listeners = {};
  const location = { hash: '' };
  const paper = { label: '01', title: 'Title', authors: 'Author', directory: 'example',
    manifest: { source_date: '2026-10-22', source_commit: '1234567890', pdf_sha256: 'abc' } };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../web/app.js'), 'utf8'), {
    document: { querySelectorAll: () => [], getElementById(id) {
      if (id === 'pdf-viewer') return viewer;
      if (!elements.has(id)) elements.set(id, { textContent: '' });
      return elements.get(id);
    } },
    window: { matchMedia: () => ({ matches: desktop }),
      addEventListener: (name, fn) => { listeners[name] = fn; } },
    location,
    fetch: async () => ({ ok: true, json: async () => ({ comunidades: paper, computacion: paper }) }),
  });
  await new Promise(resolve => setImmediate(resolve));
  listeners.resize();
  listeners.resize();
  assert.equal(assignments, 0);
  location.hash = '#computacion';
  listeners.hashchange();
  assert.equal(viewer.source, 'pdf/computacion.pdf#view=FitH');
  assert.equal(assignments, 1);
  desktop = false;
  listeners.resize();
  assert.equal(viewer.source, null);
  desktop = true;
  listeners.resize();
  assert.equal(assignments, 2);
  listeners.resize();
  assert.equal(assignments, 2);
});
