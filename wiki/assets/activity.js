import { getStroke } from './vendor/perfect-freehand-1.2.3.mjs';

const base = new URL('.', import.meta.url).pathname.replace(/\/$/, '');
const api = async (path, payload) => {
  const response = await fetch(`${base}/api/${path}`, payload ? {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
  } : {});
  const result = await response.json();
  if (!response.ok) throw Object.assign(new Error(result.error || 'Request failed'), { status: response.status });
  return result;
};
const fileURL = path => `${base}/f/${path.split('/').map(encodeURIComponent).join('/')}`;
const catalogPromise = api('catalog');
// A rejected catalogue must remain retryable without an unhandled promise rejection.
catalogPromise.catch(() => {});

// Keep the Home lists current while a saved change waits for publication.
function revealPriorityAnchor() {
  const anchor = location.hash ? document.getElementById(decodeURIComponent(location.hash.slice(1))) : null;
  const resolved = document.querySelector('.resolved-priorities');
  if (anchor && resolved?.contains(anchor)) { resolved.open = true; anchor.scrollIntoView(); }
}
window.addEventListener('hashchange', revealPriorityAnchor);
revealPriorityAnchor();
async function refreshHome() {
  if (!document.querySelector('[data-priority-id]')) return;
  try {
    const catalog = await api('catalog');
    const tables = [...document.querySelectorAll('table.roadmap')];
    const active = tables[0]?.querySelector('tbody');
    const resolvedContainer = document.querySelector('.resolved-priorities');
    let resolved = resolvedContainer?.querySelector('tbody');
    if (!active || !resolvedContainer) return;
    if (!resolved) {
      const table = tables[0].cloneNode(true);
      table.querySelector('tbody').replaceChildren();
      resolvedContainer.querySelector('.empty')?.remove();
      resolvedContainer.append(table);
      resolved = table.querySelector('tbody');
    }
    for (const item of catalog.targets.filter(t => t.kind === 'priority')) {
      const row = document.querySelector(`[data-priority-id="${CSS.escape(item.id)}"]`);
      if (!row) continue;
      (item.state === 'resolved' ? resolved : active).append(row);
      row.querySelector('.roadmap-done input').checked = item.state === 'resolved';
    }
    // Sort after moving rows, preserving the original order for equal scores.
    for (const tbody of [active, resolved]) {
      const order = catalog.targets.map(t => t.id);
      [...tbody.children].sort((a, b) => {
        const score = row => parseInt(row.cells[0].textContent) || 0;
        return score(b) - score(a) || order.indexOf(a.dataset.priorityId) - order.indexOf(b.dataset.priorityId);
      }).forEach(row => tbody.append(row));
      const empty = tbody.closest('table').parentElement.querySelector(':scope > .empty');
      if (empty) empty.hidden = !!tbody.children.length;
    }
    revealPriorityAnchor();
  } catch { /* Static history remains readable when the server is unavailable. */ }
}
refreshHome();
window.addEventListener('pageshow', refreshHome);
// Ticking a priority's box resolves it; unticking in the resolved list reopens it.
document.addEventListener('change', async event => {
  const box = event.target;
  const row = box.closest('tr[data-priority-id]');
  if (!row || !box.matches('.roadmap-done input')) return;
  const status = row.closest('table').previousElementSibling;
  status.textContent = '';
  box.disabled = true;
  try {
    await api(`activity/priority/${row.dataset.priorityId}`, { id: crypto.randomUUID(), action: 'state',
      state: box.checked ? 'resolved' : 'open', expected_state: box.checked ? 'open' : 'resolved' });
    await refreshHome();
  } catch (error) {
    if (error.status === 409) await refreshHome();
    else {
      box.checked = !box.checked;
      status.textContent = error.status ? error.message : 'Connection unavailable';
    }
  } finally { box.disabled = false; }
});

const attach = document.querySelector('.figure-attach');
if (attach) {
  let selectedFigure;
  document.querySelectorAll('[data-annotate-figure]').forEach(button => button.addEventListener('click', async () => {
    try {
      const catalog = await catalogPromise;
      const select = attach.querySelector('[data-attach-target]');
      select.replaceChildren(...catalog.targets.map(t => new Option(t.title, t.url)));
      selectedFigure = button.dataset.annotateFigure;
      attach.showModal();
    } catch { button.textContent = 'Connection unavailable'; }
  }));
  attach.querySelector('[data-attach-go]').addEventListener('click', () => {
    const target = attach.querySelector('[data-attach-target]').value;
    if (target) location.href = `${target}?figure=${encodeURIComponent(selectedFigure)}#notes`;
  });
}

const root = document.querySelector('.research-activity');
if (root) await setupEditor(root);

async function setupEditor(root) {
  const $ = selector => root.querySelector(selector);
  const path = `activity/${root.dataset.kind}/${root.dataset.id}`;
  const dialog = $('.ink-dialog');
  const sheets = $('.ink-sheets');
  let slots = [];
  const touches = new Map();
  let scrollFrame = 0, inkFrame = 0, draftTimer = 0;
  const dirtySlots = new Set();
  const viewport = $('.ink-viewport');
  const status = $('[data-save-status]');
  const draftStatus = $('[data-draft-status]');
  const key = `${location.origin}:${path}`;
  const emptyPage = () => ({ width: 1000, height: 1300, strokes: [] });
  const fresh = () => ({ pages: [emptyPage()], text: '', evidence: '', page: 0, requestId: crypto.randomUUID() });
  let draft = fresh(), currentState = 'open', entries = [], busy = false, active = null;
  let storage, storageFailed = false, restoring = true, undo = [], redo = [], figures = [];
  const backgrounds = new Map();


  // IndexedDB keeps ink drafts larger than localStorage's small string quota.
  const database = new Promise((resolve, reject) => {
    const request = indexedDB.open('astro-research-drafts', 1);
    request.onupgradeneeded = () => request.result.createObjectStore('drafts');
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
  async function transaction(mode, run) {
    storage ||= await database;
    return new Promise((resolve, reject) => {
      const tx = storage.transaction('drafts', mode);
      const request = run(tx.objectStore('drafts'));
      tx.oncomplete = () => resolve(request.result);
      tx.onerror = tx.onabort = () => reject(tx.error || new Error('Draft storage unavailable'));
    });
  }
  async function persist() {
    clearTimeout(draftTimer);
    if (restoring) return;
    try {
      await transaction('readwrite', store => store.put(draft, key));
      if (draftStatus.textContent !== 'Draft on this device') draftStatus.textContent = 'Draft on this device';
      storageFailed = false;
    } catch {
      storageFailed = true;
      draftStatus.textContent = 'Draft storage unavailable — save before closing';
    }
  }
  function hasContent() {
    return draft.text.trim() || draft.evidence.trim() || draft.pages.some(p => p.strokes.length);
  }
  function schedulePersist() {
    clearTimeout(draftTimer);
    draftTimer = setTimeout(() => { if (!active) persist(); }, 150);
  }
  function pageSnapshot() {
    // Finished strokes are immutable; only copy the arrays that editing changes.
    return draft.pages.map(page => ({ ...page, strokes: page.strokes.slice() }));
  }
  function changed() {
    draft.requestId = crypto.randomUUID();
    draft.dirty = true;
    schedulePersist();
  }
  function captureUndo() {
    undo.push(pageSnapshot());
    if (undo.length > 60) undo.shift();
    redo = [];
  }
  function syncText() {
    for (const selector of ['[data-note-text]', '[data-ink-text]']) $(selector).value = draft.text;
    for (const selector of ['[data-note-evidence]', '[data-ink-evidence]']) $(selector).value = draft.evidence;
  }
  for (const selector of ['[data-note-text]', '[data-ink-text]', '[data-note-evidence]', '[data-ink-evidence]']) {
    $(selector).addEventListener('input', event => {
      if (selector.includes('evidence')) draft.evidence = event.target.value;
      else draft.text = event.target.value;
      syncText();
      changed();
    });
  }
  function updateHistory(result) {
    entries = result.entries;
    currentState = result.state;
    // This HTML is produced by the same escaped server renderer as the static page.
    $('[data-activity-history]').innerHTML = result.html;
    if ($('[data-current-state]')) {
      $('[data-current-state]').textContent = currentState === 'resolved' ? 'Resolved' : 'Open';
      $('[data-change-state]').textContent = currentState === 'resolved' ? 'Reopen' : 'Mark resolved';
    }
  }
  async function refresh() { updateHistory(await api(path)); }
  function saving(value) {
    busy = value;
    root.querySelectorAll('button, textarea, select').forEach(el => { el.disabled = value; });
  }
  async function publicationStatus() {
    try {
      let result = await api('publication');
      if (result.state === 'pending') {
        status.textContent = 'Saved · publishing';
        setTimeout(publicationStatus, 2000);
      } else status.textContent = result.state === 'failed' ? 'Saved · publication failed' : 'Saved';
    } catch { status.textContent = 'Saved · publication unavailable'; }
  }
  $('[data-change-state]')?.addEventListener('click', async () => {
    saving(true);
    try {
      const result = await api(path, { id: crypto.randomUUID(), action: 'state',
        state: currentState === 'resolved' ? 'open' : 'resolved', expected_state: currentState });
      updateHistory(result);
      publicationStatus();
    } catch (error) {
      status.textContent = error.message;
      try { await refresh(); } catch { /* Retain the rendered history. */ }
    } finally { saving(false); }
  });

  function backgroundURL(page) {
    if (page.background_path) return fileURL(page.background_path);
    return figures.find(f => f.key === page.background)?.url;
  }
  async function background(page) {
    const url = backgroundURL(page);
    if (!url) return null;
    if (!backgrounds.has(url)) {
      backgrounds.set(url, new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = () => { backgrounds.delete(url); reject(new Error('Figure unavailable')); };
        img.src = url;
      }));
    }
    return backgrounds.get(url);
  }
  function strokePath(stroke) {
    const points = getStroke(stroke.points, { size: stroke.size, thinning: 0.5, smoothing: 0.5,
      streamline: 0.3, simulatePressure: false, last: true });
    const path = new Path2D();
    if (points.length) {
      path.moveTo(...points[0]);
      for (const point of points.slice(1)) path.lineTo(...point);
      path.closePath();
    }
    return path;
  }
  function pointBounds(points) {
    let left = Infinity, top = Infinity, right = -Infinity, bottom = -Infinity;
    for (const [x, y] of points) {
      left = Math.min(left, x); right = Math.max(right, x);
      top = Math.min(top, y); bottom = Math.max(bottom, y);
    }
    return [left, top, right - left, bottom - top];
  }
  function scribbleBounds(stroke) {
    const [x, y, width, height] = pointBounds(stroke.points);
    return [x - stroke.size / 2, y - stroke.size / 2, width + stroke.size, height + stroke.size];
  }
  function isScribble(points) {
    if (points.length < 6) return false;
    const spans = pointBounds(points).slice(2);
    const axis = spans[0] >= spans[1] ? 0 : 1, span = spans[axis];
    if (span < 24 || span < spans[1 - axis] * 1.2) return false;
    let length = 0;
    for (let i = 1; i < points.length; i++) length += Math.hypot(points[i][0] - points[i-1][0], points[i][1] - points[i-1][1]);
    if (length < span * 3.5) return false;
    const turn = span * 0.35;
    let direction = 0, extreme = points[0][axis], sweeps = 0;
    for (const point of points) {
      const distance = point[axis] - extreme;
      if (!direction && Math.abs(distance) >= turn) {
        direction = Math.sign(distance); extreme = point[axis]; sweeps = 1;
      } else if (direction * distance > 0) extreme = point[axis];
      else if (direction * distance <= -turn) {
        direction = -direction; extreme = point[axis]; sweeps++;
      }
    }
    return sweeps >= 5;
  }
  function overlapsInk(slot, stroke) {
    if (!slot?.before) return false;
    const scale = slot.before.width / slot.page.width;
    const [x, y, width, height] = scribbleBounds({ ...stroke, size: 24 });
    const left = Math.max(0, Math.floor(x * scale)), top = Math.max(0, Math.floor(y * scale));
    const right = Math.min(slot.before.width, Math.ceil((x + width) * scale));
    const bottom = Math.min(slot.before.height, Math.ceil((y + height) * scale));
    if (right <= left || bottom <= top) return false;
    const pixels = slot.before.getContext('2d').getImageData(left, top, right - left, bottom - top).data;
    for (let i = 3; i < pixels.length; i += 4) if (pixels[i]) return true;
    return false;
  }
  function paintStroke(layer, stroke) {
    if (stroke.tool === 'eraser') {
      layer.globalCompositeOperation = 'destination-out';
      if (stroke.gesture === 'scribble') {
        const [x, y, width, height] = scribbleBounds(stroke);
        layer.fillRect(x, y, width, height);
        return;
      }
      layer.lineWidth = stroke.size;
      layer.lineCap = layer.lineJoin = 'round';
      layer.beginPath();
      layer.moveTo(stroke.points[0][0], stroke.points[0][1]);
      for (const [x, y] of stroke.points) layer.lineTo(x, y);
      layer.stroke();
      layer.beginPath();
      layer.arc(stroke.points[0][0], stroke.points[0][1], stroke.size / 2, 0, Math.PI * 2);
      layer.fill();
    } else {
      layer.globalCompositeOperation = 'source-over';
      layer.fillStyle = stroke.color;
      layer.fill(strokePath(stroke));
    }
  }
  function present(context, image, ink) {
    context.resetTransform();
    context.fillStyle = '#fff';
    context.fillRect(0, 0, context.canvas.width, context.canvas.height);
    if (image) context.drawImage(image, 0, 0, context.canvas.width, context.canvas.height);
    context.drawImage(ink, 0, 0);
  }
  function paint(context, page, image, ink = document.createElement('canvas')) {
    ink.width = context.canvas.width; ink.height = context.canvas.height;
    const layer = ink.getContext('2d');
    layer.scale(ink.width / page.width, ink.height / page.height);
    for (const stroke of page.strokes) paintStroke(layer, stroke);
    present(context, image, ink);
  }
  function draw() {
    inkFrame = 0;
    for (const slot of dirtySlots) {
      if (!slot.canvas || !slot.before) continue;
      const layer = slot.ink.getContext('2d');
      layer.resetTransform();
      layer.globalCompositeOperation = 'source-over';
      layer.clearRect(0, 0, slot.ink.width, slot.ink.height);
      layer.drawImage(slot.before, 0, 0);
      layer.scale(slot.ink.width / slot.page.width, slot.ink.height / slot.page.height);
      for (const stroke of active.drawings.get(slot.page) || []) paintStroke(layer, stroke);
      present(slot.canvas.getContext('2d'), slot.image, slot.ink);
    }
    dirtySlots.clear();
  }
  function scheduleDraw(slot) {
    dirtySlots.add(slot);
    if (!inkFrame) inkFrame = requestAnimationFrame(draw);
  }
  function baseline(slot) {
    if (!slot.canvas || slot.before) return;
    slot.before = document.createElement('canvas');
    slot.before.width = slot.ink.width; slot.before.height = slot.ink.height;
    slot.before.getContext('2d').drawImage(slot.ink, 0, 0);
  }
  function renderVisible() {
    if (!dialog.open) return;
    const top = viewport.scrollTop, bottom = top + viewport.clientHeight;
    for (const slot of slots) {
      const visible = slot.top + slot.height >= top - viewport.clientHeight &&
        slot.top <= bottom + viewport.clientHeight;
      if (visible && !slot.canvas) {
        slot.canvas = document.createElement('canvas');
        slot.canvas.className = 'ink-canvas';
        slot.canvas.setAttribute('aria-label', `Handwriting sheet ${slots.indexOf(slot) + 1}`);
        slot.canvas.width = Math.round(slot.width * Math.min(devicePixelRatio, 2));
        slot.canvas.height = Math.round(slot.height * Math.min(devicePixelRatio, 2));
        slot.ink = document.createElement('canvas');
        slot.element.append(slot.canvas);
        paint(slot.canvas.getContext('2d'), slot.page, slot.image, slot.ink);
        background(slot.page).then(image => {
          slot.image = image;
          if (slot.canvas) present(slot.canvas.getContext('2d'), image, slot.ink);
        }).catch(error => { draftStatus.textContent = error.message; });
      } else if (!visible && slot.canvas) {
        slot.canvas.width = slot.canvas.height = slot.ink.width = slot.ink.height = 0;
        slot.canvas.remove(); slot.canvas = slot.ink = null;
        if (slot.before) { slot.before.width = slot.before.height = 0; slot.before = null; }
      }
    }
    const current = slots.findIndex(slot => slot.top + slot.height > top + 12);
    if (current >= 0) {
      draft.page = current;
      $('[data-sheet]').value = String(current);
    }
  }
  function releaseCanvases() {
    for (const slot of slots) {
      if (slot.canvas) {
        slot.canvas.width = slot.canvas.height = slot.ink.width = slot.ink.height = 0;
        slot.canvas = slot.ink = null;
      }
    }
  }
  function resize() {
    if (!dialog.open) return;
    finishStroke();
    const old = slots.find(slot => slot.top + slot.height > viewport.scrollTop);
    const fraction = old ? (viewport.scrollTop - old.top) / old.height : 0;
    const index = Math.max(0, slots.indexOf(old));
    releaseCanvases();
    const width = Math.max(100, viewport.clientWidth - 24) * Number($('[data-zoom]').value);
    let top = 12;
    slots = draft.pages.map(page => {
      const element = document.createElement('div');
      element.className = 'ink-sheet';
      const height = width * page.height / page.width;
      element.style.width = `${width}px`; element.style.height = `${height}px`;
      const slot = { element, page, top, width, height, image: null, canvas: null };
      top += height;
      return slot;
    });
    sheets.replaceChildren(...slots.map(slot => slot.element));
    viewport.scrollTop = slots[index] ? slots[index].top + fraction * slots[index].height : 0;
    renderVisible();
  }
  function updateSheetControls() {
    $('[data-sheet]').replaceChildren(...draft.pages.map((_, i) => new Option(String(i + 1), String(i))));
    $('[data-sheet]').value = String(draft.page);
    const full = draft.pages.length >= 30;
    $('[data-add-sheet]').disabled = busy || full;
    $('[data-add-figure]').disabled = busy || full;
    $('[data-sheet-limit]').textContent = full ? '30 sheets · save before starting a new note' : '';
    $('[data-new-ink]').hidden = !full;
  }
  function showPage(jump = false) {
    const target = draft.page;
    updateSheetControls(); resize();
    if (jump && slots[target]) {
      viewport.scrollTop = slots[target].top - 12;
      renderVisible();
    }
  }
  function appendSpace() {
    if (busy || restoring || draft.pages.length >= 30) return;
    const last = slots.at(-1);
    if (!last || viewport.scrollTop + viewport.clientHeight < last.top + last.height - viewport.clientHeight / 2) return;
    // Layout alone does not extend the notebook. Navigation and writing can.
    const page = emptyPage(), element = document.createElement('div');
    element.className = 'ink-sheet';
    const height = last.width * page.height / page.width;
    element.style.width = `${last.width}px`; element.style.height = `${height}px`;
    draft.pages.push(page);
    slots.push({ element, page, top: last.top + last.height, width: last.width, height, image: null, canvas: null });
    sheets.append(element);
    updateSheetControls(); schedulePersist(); renderVisible();
  }
  function scrollNotebook(dx, dy) {
    viewport.scrollLeft += dx; viewport.scrollTop += dy;
    appendSpace(); renderVisible();
  }
  viewport.addEventListener('scroll', () => {
    cancelAnimationFrame(scrollFrame);
    scrollFrame = requestAnimationFrame(() => { renderVisible(); appendSpace(); });
  });
  viewport.addEventListener('wheel', event => {
    if (active) { event.preventDefault(); return; }
    appendSpace();
    requestAnimationFrame(() => { appendSpace(); renderVisible(); });
  }, { passive: false });
  async function openWriter() {
    if (busy || restoring) return;
    syncText();
    if (!dialog.open) dialog.showModal();
    showPage(true);
  }
  $('[data-open-writer]').addEventListener('click', openWriter);
  $('[data-close-writer]').addEventListener('click', () => { finishStroke(); persist(); dialog.close(); });
  dialog.addEventListener('cancel', event => {
    if (busy) event.preventDefault();
    else persist();
  });
  dialog.addEventListener('close', () => {
    finishStroke(); touches.clear(); persist(); releaseCanvases(); slots = []; sheets.replaceChildren();
  });
  let observedWidth = 0;
  new ResizeObserver(() => {
    if (viewport.clientWidth !== observedWidth) {
      observedWidth = viewport.clientWidth;
      resize();
    } else renderVisible();
  }).observe(viewport);
  $('[data-zoom]').addEventListener('change', resize);
  $('[data-sheet]').addEventListener('change', event => {
    finishStroke(); draft.page = Number(event.target.value); showPage(true); persist();
  });
  $('[data-add-sheet]').addEventListener('click', () => {
    if (draft.pages.length >= 30) return;
    finishStroke(); captureUndo(); draft.pages.push(emptyPage()); draft.page = draft.pages.length - 1;
    changed(); showPage(true);
  });
  $('[data-add-figure]').addEventListener('click', async () => {
    const key = $('[data-background]').value;
    if (!key || draft.pages.length >= 30) return;
    try {
      const page = { ...emptyPage(), background: key };
      const image = await background(page);
      const ratio = image.naturalHeight / image.naturalWidth;
      page.width = Math.min(2000, image.naturalWidth);
      page.height = Math.round(page.width * ratio);
      finishStroke(); captureUndo(); draft.pages.push(page); draft.page = draft.pages.length - 1;
      changed(); showPage(true);
    } catch (error) { draftStatus.textContent = error.message; }
  });
  $('[data-undo]').addEventListener('click', () => {
    finishStroke();
    if (!undo.length) return;
    redo.push(pageSnapshot()); draft.pages = undo.pop();
    draft.page = Math.min(draft.page, draft.pages.length - 1); changed(); showPage();
  });
  $('[data-redo]').addEventListener('click', () => {
    finishStroke();
    if (!redo.length) return;
    undo.push(pageSnapshot()); draft.pages = redo.pop();
    draft.page = Math.min(draft.page, draft.pages.length - 1); changed(); showPage();
  });
  function point(event) {
    const rect = sheets.getBoundingClientRect();
    return [event.clientX - rect.left, event.clientY - rect.top + 12, event.pressure > 0 ? event.pressure : 0.5];
  }
  function addSegment(from, to) {
    const touched = new Map();
    for (const [index, slot] of slots.entries()) {
      const low = slot.top, high = low + slot.height;
      if (Math.max(from[1], to[1]) < low || Math.min(from[1], to[1]) > high) continue;
      const delta = to[1] - from[1];
      let start = 0, end = 1;
      if (delta) {
        const a = (low - from[1]) / delta, b = (high - from[1]) / delta;
        start = Math.max(0, Math.min(a, b)); end = Math.min(1, Math.max(a, b));
      }
      const local = t => {
        const scale = slot.page.width / slot.width;
        return [Math.max(0, Math.min(slot.page.width, (from[0] + (to[0] - from[0]) * t) * scale)),
          Math.max(0, Math.min(slot.page.height, (from[1] + delta * t - low) * scale)),
          from[2] + (to[2] - from[2]) * t];
      };
      baseline(slot);
      let stroke = active.fragments.get(index);
      if (!stroke) {
        stroke = { tool: active.tool, size: active.size, points: [local(start)],
          ...(active.tool === 'pen' ? { color: active.color } : {}) };
        slot.page.strokes.push(stroke);
        if (!active.drawings.has(slot.page)) active.drawings.set(slot.page, []);
        active.drawings.get(slot.page).push(stroke);
      }
      stroke.points.push(local(end)); touched.set(index, stroke);
      scheduleDraw(slot);
    }
    active.fragments = touched;
    active.last = to;
    active.gesturePoints.push(to);
  }
  viewport.addEventListener('pointerdown', event => {
    if (busy || restoring) return;
    if (event.pointerType === 'touch') {
      event.preventDefault();
      touches.set(event.pointerId, { x: event.clientX, y: event.clientY, blocked: !!active });
      viewport.setPointerCapture(event.pointerId);
      return;
    }
    if (active || event.button !== 0 || !event.target.closest('.ink-sheet')) return;
    event.preventDefault(); viewport.setPointerCapture(event.pointerId);
    for (const touch of touches.values()) touch.blocked = true;
    clearTimeout(draftTimer);
    captureUndo();
    active = { pointerId: event.pointerId, tool: 'pen', fragments: new Map(), drawings: new Map(), gesturePoints: [],
      color: $('[data-color]').value, size: Number($('[data-width]').value) };
    addSegment(point(event), point(event)); appendSpace();
  });
  viewport.addEventListener('pointermove', event => {
    const touch = touches.get(event.pointerId);
    if (touch) {
      event.preventDefault();
      if (!active && !touch.blocked && touches.size === 1) scrollNotebook(touch.x - event.clientX, touch.y - event.clientY);
      touch.x = event.clientX; touch.y = event.clientY;
      return;
    }
    if (!active || active.pointerId !== event.pointerId) return;
    event.preventDefault();
    const samples = event.getCoalescedEvents?.();
    for (const sample of samples?.length ? samples : [event]) {
      addSegment(active.last, point(sample));
    }
    appendSpace();
  });
  function finishStroke() {
    if (!active) return;
    if (isScribble(active.gesturePoints) && [...active.drawings].some(([page, strokes]) =>
      strokes.some(stroke => overlapsInk(slots.find(slot => slot.page === page), stroke)))) {
      for (const [page, strokes] of active.drawings) {
        for (const stroke of strokes) Object.assign(stroke, { tool: 'eraser', gesture: 'scribble', size: 24 });
        const slot = slots.find(slot => slot.page === page);
        if (slot) dirtySlots.add(slot);
      }
    }
    cancelAnimationFrame(inkFrame); draw();
    const pointerId = active.pointerId;
    active = null;
    if (viewport.hasPointerCapture(pointerId)) viewport.releasePointerCapture(pointerId);
    for (const slot of slots) {
      if (slot.before) { slot.before.width = slot.before.height = 0; slot.before = null; }
    }
    changed();
  }
  for (const name of ['pointerup', 'pointercancel', 'lostpointercapture']) viewport.addEventListener(name, event => {
    touches.delete(event.pointerId);
    if (active?.pointerId === event.pointerId) {
      if (name === 'pointerup') addSegment(active.last, point(event));
      finishStroke();
    }
    schedulePersist();
  });
  window.addEventListener('pagehide', () => { finishStroke(); persist(); });
  window.addEventListener('beforeunload', event => {
    if (storageFailed && draft.dirty) { event.preventDefault(); event.returnValue = ''; }
  });

  async function saveNote() {
    if (busy || restoring) return;
    finishStroke(); saving(true);
    draftStatus.textContent = 'Saving'; status.textContent = 'Saving';
    try {
      const pages = [];
      // Preserve interior blank sheets; omit only the unused trailing space.
      const lastUsed = draft.pages.findLastIndex(page => page.strokes.length || page.background);
      for (const page of draft.pages.slice(0, lastUsed + 1)) {
        const output = document.createElement('canvas');
        output.width = page.width; output.height = page.height;
        paint(output.getContext('2d'), page, await background(page));
        pages.push({ width: page.width, height: page.height, strokes: page.strokes,
          ...(page.background ? { background: page.background } : {}), preview: output.toDataURL('image/png') });
      }
      const payload = { id: draft.requestId, action: 'note', text: draft.text,
        evidence: draft.evidence.split('\n').map(s => s.trim()).filter(Boolean), pages,
        ...(draft.supersedes ? { supersedes: draft.supersedes } : {}) };
      await persist();
      const result = await api(path, payload);
      updateHistory(result);
      // Keep the written sheet open. Further edits create a new immutable revision.
      draft.supersedes = payload.id;
      draft.requestId = crypto.randomUUID(); draft.dirty = false;
      result.entries.find(e => e.id === payload.id)?.pages.forEach((page, i) => {
        // Saved pages retain their original positions, including blank sheets.
        const editorPages = draft.pages;
        if (page.background_path) Object.assign(editorPages[i], {
          background: `saved:${payload.id}:${i}`, background_path: page.background_path });
      });
      await persist();
      draftStatus.textContent = 'Saved';
      publicationStatus();
    } catch (error) {
      status.textContent = error.message;
      draftStatus.textContent = `${error.message} · draft retained`;
    } finally { saving(false); updateSheetControls(); }
  }
  $('[data-save-ink]').addEventListener('click', saveNote);
  $('[data-save-text]').addEventListener('click', saveNote);
  $('[data-activity-history]').addEventListener('click', async event => {
    const button = event.target.closest('[data-edit-note]');
    if (!button) return;
    if (draft.dirty && hasContent()) { status.textContent = 'Save current draft first'; return; }
    const entry = entries.find(e => e.id === button.dataset.editNote);
    if (!entry) return;
    draft = { ...fresh(), text: entry.text || '', evidence: (entry.evidence || []).join('\n'), supersedes: entry.id,
      pages: entry.pages.length ? entry.pages.map((p, i) => ({ ...structuredClone(p),
        ...(p.background_path ? { background: `saved:${entry.id}:${i}` } : {}) })) : [emptyPage()] };
    undo = []; redo = []; syncText(); persist(); openWriter();
  });
  // A fresh note leaves the saved history intact; explicit revision is available above.
  const newNote = document.createElement('button');
  newNote.type = 'button'; newNote.textContent = 'New note';
  newNote.addEventListener('click', () => {
    if (draft.dirty && hasContent()) { status.textContent = 'Save current draft first'; return; }
    finishStroke(); draft = fresh(); undo = []; redo = []; syncText(); persist(); showPage(true);
  });
  $('.activity-actions').append(newNote);
  $('[data-new-ink]').addEventListener('click', () => {
    if (draft.dirty && hasContent()) { draftStatus.textContent = 'Save current draft first'; return; }
    newNote.click();
  });

  $('[data-context-title]').textContent = document.querySelector('h1').textContent;
  const context = $('[data-context-content]');
  // Copy only the item's introduction, not its history or interactive controls.
  for (const sibling of [...root.parentElement.children]) {
    if (sibling === root) break;
    if (sibling.matches('p, .record-meta') || (root.dataset.kind === 'question' && sibling.querySelector('#context'))) {
      const copy = sibling.cloneNode(true);
      copy.removeAttribute('id');
      copy.querySelectorAll('[id]').forEach(el => el.removeAttribute('id'));
      context.append(copy);
    }
  }
  try {
    const saved = await transaction('readonly', store => store.get(key));
    if (saved) { draft = saved; draftStatus.textContent = saved.dirty ? 'Draft recovered' : (saved.supersedes ? 'Saved notes' : ''); }
  } catch { storageFailed = true; draftStatus.textContent = 'Draft storage unavailable'; }
  restoring = false; syncText();
  try { await refresh(); } catch { status.textContent = 'Connection unavailable · local drafts available'; }
  try {
    const catalog = await catalogPromise;
    figures = catalog.figures;
    function filterFigures() {
      const query = $('[data-figure-search]').value.toLowerCase();
      const matches = figures.filter(f => f.title.toLowerCase().includes(query)).slice(0, 100);
      $('[data-background]').replaceChildren(new Option('Choose figure', ''), ...matches.map(f => new Option(f.title, f.key)));
    }
    $('[data-figure-search]').addEventListener('input', filterFigures);
    filterFigures();
    const requested = new URLSearchParams(location.search).get('figure');
    if (requested && figures.some(f => f.key === requested)) {
      const selected = figures.find(f => f.key === requested);
      $('[data-background]').append(new Option(selected.title, selected.key));
      $('[data-background]').value = requested;
      openWriter();
      $('[data-add-figure]').click();
      history.replaceState(null, '', location.pathname + '#notes');
    }
  } catch { /* Writing without a figure still works. */ }
}
