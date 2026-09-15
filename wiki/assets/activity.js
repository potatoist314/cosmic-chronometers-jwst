import { getStroke } from './vendor/perfect-freehand-1.2.3.mjs';

const base = new URL('.', import.meta.url).pathname.replace(/\/$/, '');
const api = async (path, payload) => {
  const response = await fetch(`${base}/api/${path}`, payload ? {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
  } : {});
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || 'Request failed');
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
      if (row) (item.state === 'resolved' ? resolved : active).append(row);
    }
    // Sort after moving rows, preserving the original order for equal scores.
    for (const tbody of [active, resolved]) {
      const order = catalog.targets.map(t => t.id);
      [...tbody.children].sort((a, b) => {
        const score = row => parseInt(row.cells[0].textContent) || 0;
        return score(b) - score(a) || order.indexOf(a.dataset.priorityId) - order.indexOf(b.dataset.priorityId);
      }).forEach(row => tbody.append(row));
      const empty = tbody.closest('table').previousElementSibling;
      if (empty?.classList.contains('empty')) empty.hidden = !!tbody.children.length;
    }
    revealPriorityAnchor();
  } catch { /* Static history remains readable when the server is unavailable. */ }
}
refreshHome();
window.addEventListener('pageshow', refreshHome);

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
  const canvas = $('.ink-canvas');
  const ctx = canvas.getContext('2d');
  const viewport = $('.ink-viewport');
  const status = $('[data-save-status]');
  const draftStatus = $('[data-draft-status]');
  const key = `${location.origin}:${path}`;
  const emptyPage = () => ({ width: 1000, height: 1300, strokes: [] });
  const fresh = () => ({ pages: [emptyPage()], text: '', evidence: '', page: 0, requestId: crypto.randomUUID() });
  let draft = fresh(), currentState = 'open', entries = [], busy = false, active = null;
  let storage, storageFailed = false, restoring = true, undo = [], redo = [], figures = [];
  const backgrounds = new Map();
  let imageEpoch = 0;

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
    if (restoring) return;
    try {
      await transaction('readwrite', store => store.put(structuredClone(draft), key));
      draftStatus.textContent = 'Draft on this device';
      storageFailed = false;
    } catch {
      storageFailed = true;
      draftStatus.textContent = 'Draft storage unavailable — save before closing';
    }
  }
  function hasContent() {
    return draft.text.trim() || draft.evidence.trim() || draft.pages.some(p => p.strokes.length);
  }
  function changed() {
    draft.requestId = crypto.randomUUID();
    draft.dirty = true;
    persist();
  }
  function captureUndo() {
    undo.push(structuredClone(draft.pages));
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
  function paint(context, page, image) {
    context.fillStyle = '#fff';
    context.fillRect(0, 0, page.width, page.height);
    if (image) context.drawImage(image, 0, 0, page.width, page.height);
    for (const stroke of page.strokes) {
      context.fillStyle = stroke.color;
      context.fill(strokePath(stroke));
    }
  }
  let renderedBackground = null;
  function draw() {
    const page = draft.pages[draft.page];
    ctx.setTransform(canvas.width / page.width, 0, 0, canvas.height / page.height, 0, 0);
    paint(ctx, page, renderedBackground);
  }
  function resize() {
    if (!dialog.open) return;
    const page = draft.pages[draft.page];
    const zoom = Number($('[data-zoom]').value);
    const width = Math.max(100, viewport.clientWidth - 24) * zoom;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${width * page.height / page.width}px`;
    canvas.width = Math.round(width * devicePixelRatio);
    canvas.height = Math.round(width * page.height / page.width * devicePixelRatio);
    draw();
  }
  async function showPage() {
    const epoch = ++imageEpoch;
    renderedBackground = null;
    $('[data-sheet]').replaceChildren(...draft.pages.map((_, i) => new Option(String(i + 1), String(i))));
    $('[data-sheet]').value = String(draft.page);
    resize();
    try {
      const image = await background(draft.pages[draft.page]);
      if (imageEpoch === epoch) { renderedBackground = image; draw(); }
    } catch (error) { draftStatus.textContent = error.message; }
  }
  async function openWriter() {
    if (busy || restoring) return;
    syncText();
    if (!dialog.open) dialog.showModal();
    showPage();
  }
  $('[data-open-writer]').addEventListener('click', openWriter);
  $('[data-close-writer]').addEventListener('click', () => { persist(); dialog.close(); });
  dialog.addEventListener('cancel', event => {
    if (busy) event.preventDefault();
    else persist();
  });
  dialog.addEventListener('close', () => {
    if (active) finishStroke();
    persist();
  });
  new ResizeObserver(resize).observe(viewport);
  $('[data-zoom]').addEventListener('change', resize);
  $('[data-sheet]').addEventListener('change', event => {
    draft.page = Number(event.target.value); showPage(); persist();
  });
  $('[data-add-sheet]').addEventListener('click', () => {
    captureUndo(); draft.pages.push(emptyPage()); draft.page = draft.pages.length - 1;
    changed(); showPage();
  });
  $('[data-add-figure]').addEventListener('click', async () => {
    const key = $('[data-background]').value;
    if (!key) return;
    try {
      const page = { ...emptyPage(), background: key };
      const image = await background(page);
      const ratio = image.naturalHeight / image.naturalWidth;
      page.width = Math.min(2000, image.naturalWidth);
      page.height = Math.round(page.width * ratio);
      captureUndo(); draft.pages.push(page); draft.page = draft.pages.length - 1;
      changed(); showPage();
    } catch (error) { draftStatus.textContent = error.message; }
  });
  $('[data-undo]').addEventListener('click', () => {
    if (!undo.length) return;
    redo.push(structuredClone(draft.pages)); draft.pages = undo.pop();
    draft.page = Math.min(draft.page, draft.pages.length - 1); changed(); showPage();
  });
  $('[data-redo]').addEventListener('click', () => {
    if (!redo.length) return;
    undo.push(structuredClone(draft.pages)); draft.pages = redo.pop();
    draft.page = Math.min(draft.page, draft.pages.length - 1); changed(); showPage();
  });
  $('[data-tool]').addEventListener('change', () => {
    viewport.classList.toggle('ink-move', $('[data-tool]').value === 'move');
  });
  function point(event) {
    const rect = canvas.getBoundingClientRect(), page = draft.pages[draft.page];
    return [Math.max(0, Math.min(page.width, (event.clientX - rect.left) / rect.width * page.width)),
      Math.max(0, Math.min(page.height, (event.clientY - rect.top) / rect.height * page.height)),
      event.pressure > 0 ? event.pressure : 0.5];
  }
  function erase(p) {
    const page = draft.pages[draft.page];
    // Hit-test the rendered stroke rather than erasing unrelated neighbouring ink.
    for (let i = page.strokes.length - 1; i >= 0; i--) {
      ctx.save(); ctx.resetTransform();
      const hit = ctx.isPointInPath(strokePath(page.strokes[i]), p[0], p[1]);
      ctx.restore();
      if (hit) { page.strokes.splice(i, 1); break; }
    }
  }
  canvas.addEventListener('pointerdown', event => {
    if (busy || restoring || active || event.pointerType === 'touch' || $('[data-tool]').value === 'move') return;
    if (event.button !== 0) return;
    event.preventDefault();
    canvas.setPointerCapture(event.pointerId);
    captureUndo();
    active = { pointerId: event.pointerId, tool: $('[data-tool]').value };
    if (active.tool === 'pen') draft.pages[draft.page].strokes.push({ color: $('[data-color]').value,
      size: Number($('[data-width]').value), points: [point(event)] });
    else erase(point(event));
    draw();
  });
  canvas.addEventListener('pointermove', event => {
    if (!active || active.pointerId !== event.pointerId) return;
    event.preventDefault();
    for (const sample of event.getCoalescedEvents?.().length ? event.getCoalescedEvents() : [event]) {
      if (active.tool === 'pen') draft.pages[draft.page].strokes.at(-1).points.push(point(sample));
      else erase(point(sample));
    }
    draw();
  });
  function finishStroke() {
    if (!active) return;
    active = null; changed();
  }
  for (const event of ['pointerup', 'pointercancel', 'lostpointercapture']) canvas.addEventListener(event, finishStroke);
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
      for (const page of draft.pages) {
        if (!page.strokes.length && !page.background) continue;
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
        // Match saved pages to the non-empty editor sheets.
        const editorPages = draft.pages.filter(p => p.strokes.length || p.background);
        if (page.background_path) Object.assign(editorPages[i], {
          background: `saved:${payload.id}:${i}`, background_path: page.background_path });
      });
      await persist();
      draftStatus.textContent = 'Saved';
      publicationStatus();
    } catch (error) {
      status.textContent = error.message;
      draftStatus.textContent = `${error.message} · draft retained`;
    } finally { saving(false); }
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
    draft = fresh(); undo = []; redo = []; syncText(); persist(); showPage();
  });
  $('.activity-actions').append(newNote);

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
