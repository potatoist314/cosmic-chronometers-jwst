/** Runs only against the disposable HTTP wiki started by test_direction_browser.py. */
import assert from 'node:assert/strict';
import { mkdir } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const { chromium } = await import(pathToFileURL(path.join(process.env.WIKI_PLAYWRIGHT, 'index.mjs')).href);
const browser = await chromium.launch({ headless: true, ...(process.env.WIKI_BROWSER ? { executablePath: process.env.WIKI_BROWSER } : {}) });
const context = await browser.newContext({ viewport: { width: 1200, height: 1100 } });
const page = await context.newPage();
const errors = [];
page.on('pageerror', error => errors.push(error.message));
const host = process.env.WIKI_TEST_URL;
assert.match(host, /^http:\/\/127\.0\.0\.1:\d+$/, 'A disposable loopback fixture is required');
const snapshot = async () => (await context.request.get(`${host}/api/direction`)).json();
const form = (p, name) => p.locator('form').filter({ has: p.getByRole('button', { name, exact: true }) });
const priorityForm = p => form(p, 'Save priority');
const directionForm = p => form(p, 'Save entry');
async function save(p, name) {
  const response = p.waitForResponse(r => r.url().endsWith('/api/direction') && r.request().method() === 'POST');
  await p.getByRole('button', { name, exact: true }).click();
  const result = await response;
  assert.equal(result.status(), 200, await result.text());
  await p.getByRole('button', { name, exact: true }).waitFor({ state: 'detached' });
}
async function editPriority(p, id) {
  await p.locator(`[data-edit-priority="${id}"]`).click();
  await priorityForm(p).waitFor();
}

try {
  await page.goto(host);
  await page.getByRole('button', { name: 'Add priority', exact: true }).waitFor();
  const original = await snapshot();
  await page.getByRole('button', { name: 'Add priority', exact: true }).click();
  await priorityForm(page).getByLabel('Title', { exact: true }).fill('Cancelled priority');
  await priorityForm(page).getByRole('button', { name: 'Cancel', exact: true }).click();
  assert.deepEqual(await snapshot(), original, 'Cancel must not change the canonical source');
  await editPriority(page, 'metals');
  await save(page, 'Save priority');
  assert.deepEqual(await snapshot(), original, 'An unchanged save must not add history');

  await page.getByRole('button', { name: 'Add priority', exact: true }).click();
  const pf = priorityForm(page);
  await pf.getByRole('button', { name: 'Save priority', exact: true }).click();
  assert.deepEqual(await snapshot(), original);
  await pf.getByLabel('Title', { exact: true }).fill('word '.repeat(31));
  await pf.getByRole('button', { name: 'Save priority', exact: true }).click();
  assert.deepEqual(await snapshot(), original, 'Overlong wording must not save');
  await pf.getByLabel('Title', { exact: true }).fill('Browser priority');
  await pf.getByLabel('Details', { exact: true }).fill('An exact question?');
  await pf.getByLabel(/Difficulty/).fill('Small');
  await pf.locator('.score-strip label').filter({ hasText: /^7$/ }).click();
  assert.equal(await pf.getByRole('radio', { name: '7', exact: true }).isChecked(), true);
  await pf.locator('select').selectOption('metals');
  await save(page, 'Save priority');
  const created = await snapshot();
  const task = created.priorities.find(t => t.title === 'Browser priority');
  assert.equal(task.priority, 7);
  assert.equal(task.effort, 'Small');
  assert.deepEqual(task.depends_on, ['metals']);
  await page.reload();
  await page.locator(`[data-priority-id="${task.id}"]`).getByRole('link', { name: task.title, exact: true }).waitFor();
  await page.goto(`${host}/p/${task.id}/`);
  await page.getByRole('heading', { name: task.title, exact: true }).waitFor();
  await page.goto(host);

  await page.locator('[data-edit-direction="direction-0"]').click();
  let df = directionForm(page);
  assert.equal(await df.getByLabel('Text', { exact: true }).inputValue(), original.direction[0].text, 'Edit must open the original wording');
  await df.getByLabel(/Heading/).fill('My direction');
  const wording = 'Does this work?\n\n  I am still uncertain. ';
  await df.getByLabel('Text', { exact: true }).fill(wording);
  await save(page, 'Save entry');
  let current = await snapshot();
  assert.equal(current.direction[0].text, wording);
  assert.equal(current.history.at(-1).before.text, original.direction[0].text);
  assert.ok((await page.locator('#roadmap-amendments').textContent()).includes(original.direction[0].text), 'Earlier wording must remain available before a rebuild');
  await page.getByRole('button', { name: 'Add direction entry', exact: true }).click();
  df = directionForm(page);
  await df.getByLabel(/Heading/).fill('A second direction');
  await df.getByLabel('Text', { exact: true }).fill('Keep <script>literal text</script> and\n  spacing.');
  await save(page, 'Save entry');
  await page.reload();
  await page.getByRole('heading', { name: 'A second direction', exact: true }).waitFor();
  assert.equal((await snapshot()).direction.length, 2);

  const other = await context.newPage();
  other.on('pageerror', error => errors.push(error.message));
  await other.goto(host);
  await editPriority(page, task.id);
  await editPriority(other, task.id);
  await priorityForm(page).getByLabel('Title', { exact: true }).fill('First browser wording');
  await priorityForm(other).getByLabel('Title', { exact: true }).fill('Second browser wording');
  await save(page, 'Save priority');
  await page.locator(`[data-priority-id="${task.id}"]`).getByRole('link', { name: 'First browser wording', exact: true }).waitFor();
  const rejected = other.waitForResponse(r => r.url().endsWith('/api/direction') && r.request().method() === 'POST');
  await priorityForm(other).getByRole('button', { name: 'Save priority', exact: true }).click();
  assert.equal((await rejected).status(), 409);
  assert.equal(await priorityForm(other).getByLabel('Title', { exact: true }).inputValue(), 'Second browser wording');
  assert.equal((await snapshot()).priorities.find(t => t.id === task.id).title, 'First browser wording');
  await priorityForm(other).getByRole('button', { name: 'Cancel', exact: true }).click();
  await other.close();

  // Test the original resolution control after authoring replaces the table rows.
  const row = page.locator(`[data-priority-id="${task.id}"]`);
  const resolved = page.waitForResponse(r => r.url().includes(`/api/activity/priority/${task.id}`) && r.request().method() === 'POST');
  await row.getByRole('checkbox').check();
  assert.equal((await resolved).status(), 200);
  await page.reload();
  await page.locator('.resolved-priorities').getByText('First browser wording', { exact: true }).waitFor({ state: 'attached' });
  assert.equal((await snapshot()).states[task.id], 'resolved');

  for (const width of [1200, 820, 400]) {
    await page.setViewportSize({ width, height: 1100 });
    await page.getByRole('button', { name: 'Add priority', exact: true }).click();
    await priorityForm(page).getByLabel('Title', { exact: true }).fill('Responsive draft');
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, `No overflow at ${width}px`);
    const small = await priorityForm(page).locator('button,input,select,textarea').evaluateAll(nodes => nodes.filter(n => n.type !== 'radio' && n.type !== 'hidden' && n.getBoundingClientRect().height < 43).map(n => n.outerHTML));
    assert.deepEqual(small, [], `Touch target height at ${width}px`);
    if (process.env.WIKI_SCREENSHOTS) {
      await mkdir(process.env.WIKI_SCREENSHOTS, { recursive: true });
      await page.screenshot({ path: path.join(process.env.WIKI_SCREENSHOTS, `priority-${width}.png`), fullPage: true });
    }
    await priorityForm(page).getByRole('button', { name: 'Cancel', exact: true }).click();
    await page.locator('[data-edit-direction="direction-0"]').click();
    await directionForm(page).getByLabel('Text', { exact: true }).focus();
    if (process.env.WIKI_SCREENSHOTS) await page.screenshot({ path: path.join(process.env.WIKI_SCREENSHOTS, `direction-${width}.png`), fullPage: true });
    await page.keyboard.press('Escape');
    await directionForm(page).waitFor({ state: 'detached' });
  }
  assert.deepEqual(errors, [], 'No browser exceptions');
  console.log('PASS: create/edit, original wording, reload before build, cancel/no-op, validation, conflict retention, resolution, and 1200/820/400px forms.');
} finally {
  await browser.close();
}
