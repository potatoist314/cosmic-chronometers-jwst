/** Regression checks for the editor's drawing budget and immutable stroke history. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';
import test from 'node:test';
import { getStroke } from '../assets/vendor/perfect-freehand-1.2.3.mjs';

const source = readFileSync(new URL('../assets/activity.js', import.meta.url), 'utf8');
// Exercise the actual private functions without loading a browser or a database.
function definition(name) {
  const regular = source.indexOf(`  function ${name}(`);
  const start = regular >= 0 ? regular : source.indexOf(`  async function ${name}(`);
  assert.ok(start >= 0, `Missing function ${name}`);
  let end = source.indexOf('{', start), depth = 1;
  for (end++; depth; end++) {
    if (source[end] === '{') depth++;
    if (source[end] === '}') depth--;
  }
  return source.slice(start, end);
}
function harness() {
  const metrics = { outlines: 0, resizes: 0, frames: [], inkPresent: true };
  function canvas() {
    const c = { _width: 1000, _height: 1300 };
    for (const key of ['width', 'height']) Object.defineProperty(c, key, {
      get: () => c[`_${key}`], set: value => { metrics.resizes++; c[`_${key}`] = value; },
    });
    const context = { canvas: c };
    for (const name of ['scale', 'resetTransform', 'fillRect', 'clearRect', 'drawImage',
      'beginPath', 'moveTo', 'lineTo', 'stroke', 'arc', 'fill']) context[name] = () => {};
    context.getImageData = () => ({ data: new Uint8ClampedArray([0, 0, 0, metrics.inkPresent ? 255 : 0]) });
    c.getContext = () => context;
    return c;
  }
  const page = { width: 1000, height: 1300, strokes: Array.from({ length: 500 }, (_, i) => ({
    color: '#17212b', size: 4, points: Array.from({ length: 24 }, (_, j) => [j * 3, i, 0.5]),
  })) };
  const slot = { page, top: 12, width: 1000, height: 1300, canvas: canvas(), ink: canvas(), image: null };
  const env = {
    document: { createElement: canvas },
    Path2D: class { moveTo() {} lineTo() {} closePath() {} },
    getStroke: (...args) => { metrics.outlines++; return getStroke(...args); },
    slots: [slot], active: { fragments: new Map(), drawings: new Map(), tool: 'pen', color: '#17212b', size: 4, gesturePoints: [] },
    cancelAnimationFrame() {}, viewport: { hasPointerCapture: () => false }, changed() {},
    inkFrame: 0, dirtySlots: new Set(), requestAnimationFrame: fn => { metrics.frames.push(fn); return metrics.frames.length; },
  };
  runInNewContext(['pointBounds', 'scribbleBounds', 'isScribble', 'overlapsInk', 'finishStroke', 'strokePath', 'paintStroke', 'present', 'paint', 'draw', 'scheduleDraw', 'baseline', 'addSegment']
    .map(definition).join('\n'), env);
  env.paint(slot.canvas.getContext('2d'), page, null, slot.ink);
  metrics.outlines = metrics.resizes = 0;
  return { env, metrics, slot, canvas };
}

test('128 coalesced samples schedule one frame and do not replay 500 finished strokes', () => {
  const { env, metrics, slot } = harness();
  let from = [100, 100, 0.5];
  for (let i = 1; i <= 128; i++) {
    const to = [100 + i, 100 + i / 2, 0.5];
    env.addSegment(from, to); from = to;
  }
  assert.equal(metrics.outlines, 0);
  assert.equal(metrics.frames.length, 1);
  const allocations = metrics.resizes;
  metrics.frames.shift()();
  assert.equal(metrics.outlines, 1);
  assert.equal(metrics.resizes, allocations, 'Drawing must not reset canvas dimensions');
  assert.equal(slot.page.strokes.at(-1).points.length, 129);
  for (let i = 0; i < 10; i++) {
    const to = [from[0] + 1, from[1] + 1, 0.5];
    env.addSegment(from, to); from = to;
    metrics.frames.shift()();
  }
  assert.equal(metrics.outlines, 11);
  assert.equal(metrics.resizes, allocations);
});

test('eraser updates do not rebuild finished pen outlines', () => {
  const { env, metrics } = harness();
  env.active.tool = 'eraser'; env.active.size = 24;
  env.addSegment([100, 100, 0.5], [200, 200, 0.5]);
  metrics.frames.shift()();
  assert.equal(metrics.outlines, 0);
});

test('cross-sheet samples preserve both sides without redrawing an untouched sheet', () => {
  const { env, metrics, canvas } = harness();
  const second = { page: { width: 1000, height: 1300, strokes: [] }, top: 1312, width: 1000,
    height: 1300, canvas: canvas(), ink: canvas() };
  env.slots.push(second);
  env.addSegment([300, 1300, 0.4], [300, 1330, 0.8]);
  metrics.frames.shift()();
  assert.equal(env.slots[0].page.strokes.at(-1).points.at(-1)[1], 1300);
  assert.equal(second.page.strokes[0].points[0][1], 0);
  assert.equal(second.page.strokes[0].points.at(-1)[1], 18);
  assert.equal(metrics.outlines, 2);
});

test('undo snapshots share immutable points but isolate mutable stroke arrays', () => {
  const page = { width: 1000, height: 1300, strokes: [{ points: [[1, 2, 0.5]] }] };
  const env = { draft: { pages: [page] } };
  runInNewContext(definition('pageSnapshot'), env);
  const snapshot = env.pageSnapshot();
  assert.equal(snapshot[0].strokes[0], page.strokes[0]);
  page.strokes.push({ points: [[3, 4, 0.5]] });
  assert.equal(snapshot[0].strokes.length, 1);
});


test('repeated back-and-forth scribbles are recognized at different scales', () => {
  const { env } = harness();
  const points = [[0,0], [100,5], [0,10], [100,15], [0,20], [100,25]];
  for (const scale of [0.5, 1, 2]) assert.ok(env.isScribble(points.map(([x,y]) => [x*scale,y*scale,0.5])));
  assert.ok(env.isScribble(points.map(([x,y]) => [y,x,0.5])));
});

test('ordinary lines, cursive-like progress, short crossings and tiny jitter are not erasures', () => {
  const { env } = harness();
  const normal = [
    [[0,0],[100,0]],
    [[0,0],[10,20],[20,0],[30,20],[40,0],[50,20],[60,0]],
    [[0,0],[100,5],[0,10],[100,15]],
    [[0,0],[4,1],[0,2],[4,3],[0,4],[4,5]],
  ];
  for (const points of normal) assert.equal(env.isScribble(points), false);
});

test('scribble erasure retains original gesture points and uses its covered area', () => {
  const { env } = harness();
  const points = [[0,0],[100,5],[0,10],[100,15],[0,20],[100,25]];
  const stroke = { tool: 'eraser', gesture: 'scribble', size: 24, points };
  assert.deepEqual(Array.from(env.scribbleBounds(stroke)), [-12,-12,124,49]);
  const layer = { fillRect(...bounds) { this.bounds = bounds; } };
  env.paintStroke(layer, stroke);
  assert.deepEqual(layer.bounds, [-12,-12,124,49]);
  assert.equal(layer.globalCompositeOperation, 'destination-out');
  assert.equal(stroke.points, points);
});

test('finishing a scribble converts it to erasure only over existing ink', () => {
  for (const inkPresent of [true, false]) {
    const { env, metrics, slot } = harness();
    metrics.inkPresent = inkPresent;
    const points = [[100,220],[200,225],[100,230],[200,235],[100,240],[200,245]];
    for (let i = 0; i < points.length; i++) env.addSegment(points[Math.max(0,i-1)], points[i]);
    env.finishStroke();
    const stroke = slot.page.strokes.at(-1);
    assert.equal(stroke.tool, inkPresent ? 'eraser' : 'pen');
    assert.equal(stroke.gesture, inkPresent ? 'scribble' : undefined);
    assert.equal(env.active, null);
  }
});


test('Done saves changed notes before closing and retains the editor on failure', async () => {
  for (const success of [true, false]) {
    const calls = [];
    const env = { busy: false, restoring: false, draft: { dirty: true },
      finishStroke: () => calls.push('finish'), hasContent: () => true,
      saveNote: async () => { calls.push('save'); return success; },
      persist: async () => calls.push('persist'), dialog: { close: () => calls.push('close') } };
    runInNewContext(definition('doneWriting'), env);
    await env.doneWriting();
    assert.deepEqual(calls, success ? ['finish', 'save', 'persist', 'close'] : ['finish', 'save']);
  }
});

test('Done does not create another revision for unchanged notes', async () => {
  const calls = [];
  const env = { busy: false, restoring: false, draft: { dirty: false }, finishStroke() {},
    hasContent: () => true, saveNote: () => assert.fail('Unchanged notes must not be saved again'),
    persist: async () => calls.push('persist'), dialog: { close: () => calls.push('close') } };
  runInNewContext(definition('doneWriting'), env);
  await env.doneWriting();
  assert.deepEqual(calls, ['persist', 'close']);
});

test('save status distinguishes local drafts from server saves and history controls follow available actions', () => {
  const controls = { '[data-undo]': {}, '[data-redo]': {} };
  const env = { draft: { dirty: true }, draftStatus: {}, busy: false, undo: [], redo: [], $: key => controls[key] };
  runInNewContext(['updateDraftStatus', 'updateUndoControls'].map(definition).join('\n'), env);
  env.updateDraftStatus();
  assert.match(env.draftStatus.textContent, /not yet synced/);
  env.draft = { dirty: false, supersedes: 'saved-note' }; env.updateDraftStatus();
  assert.equal(env.draftStatus.textContent, 'Saved');
  env.updateUndoControls();
  assert.equal(controls['[data-undo]'].disabled, true);
  env.undo.push({}); env.updateUndoControls();
  assert.equal(controls['[data-undo]'].disabled, false);
  assert.equal(controls['[data-redo]'].disabled, true);
  env.busy = true; env.updateUndoControls();
  assert.equal(controls['[data-undo]'].disabled, true);
});


test('failed server save retains the draft and reports local storage failure accurately', async () => {
  for (const storageFailed of [false, true]) {
    const draft = { dirty: true, pages: [], text: 'Keep these notes', evidence: '', requestId: 'retry-id' };
    const env = { busy: false, restoring: false, storageFailed, draft, draftStatus: {}, status: {}, path: 'fixture',
      finishStroke() {}, hasContent: () => true, saving: value => { env.busy = value; },
      persist: async () => {}, updateSheetControls() {},
      api: async () => { throw new Error('Connection unavailable'); } };
    runInNewContext(definition('saveNote'), env);
    assert.equal(await env.saveNote(), false);
    assert.equal(env.draft, draft);
    assert.equal(draft.dirty, true);
    assert.equal(draft.requestId, 'retry-id');
    assert.equal(env.busy, false);
    assert.match(env.draftStatus.textContent, /Connection unavailable/);
    assert.match(env.draftStatus.textContent, storageFailed ? /keep this page open/ : /notes kept on this device/);
  }
});
