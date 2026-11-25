---
name: sandro-weekly-slides
description: Use when you make or update the slide deck for Liu Hao's weekly meeting with Sandro, or when the message "weekly slides: summarise the past week in the Sandro deck" arrives. It gives his words about the deck, the Artifact calls in order, and the source of each fact on the two detail slides.
---

# Weekly slides for the meeting with Sandro

Written from the run of 2026-11-25 by the Astronomy lead. That run made the deck and rebuilt it one time. Its record is `~/.claude/projects/-Users-liuhao-Downloads-Astro-project/0e9cd474-3a15-4f3d-8102-ef966ca17496.jsonl`, 15:13 to 15:44 UTC. No weekly update has run yet. The first weekly message is due on 2026-11-26.

The deck is "Chronometer: open questions": https://claude.ai/artifact/N1yaFvoNBaEzuEirFBFx9q. It is a claude.ai Slides artifact. It is private to Liu Hao. Sandro can open it only after Liu Hao shares it from the Share menu of the page.

Rules for figures, physical facts and browser pages are in `AGENTS.md` and `~/.claude/CLAUDE.md`. Read them there.

## His words

All words are from 2026-11-25. Text in quotation marks is his. "Picked" shows an option that he selected from a list.

- **Purpose.** "i need you to track these discussions and open questions somewhere clear. honestly, putting them into a slide would be good. for weekly discussions w sandro"
- **Style.** "use the write like me style for this please."
- **Schedule.** "this slide generation should run automatically weekly to summarise the past week's discussion". Meeting day: "friday". The slides are made on the evening before. Picked: "Run when it wakes".
- **Sources.** Picked: "Chats with me", "New results", "Handwritten notes". He did not pick "Other Astro chats".
- **Deck.** Picked: "One running deck". The option said: "Same link every week. The new week's slides go first, the open-questions slide is updated, older weeks stay further back."
- **Review.** Picked: "Go live, tell me". The option said: "The deck updates on its own and I tell you in one line that it is ready."
- **Length.** Picked: "3 to 5 slides". The option said: "What was discussed, what was decided, any new result, and the updated open questions."
- **Figures.** Picked: "Yes, existing figures". The option said: "Use figures that already exist from that week's results. Nothing new is drawn or run."
- **Verdict on the first version** (8 slides, 7 open questions): "i have significant issues with this. too many open questions, not enough context (big issue!), too verbose"
- **Detail.** "more detail to include: wavelength ranges and lines per survey, what lines are masked, redshift ranges" and "also show the exact age ranges for bins"

Facts of the run. They are not his rules. After the verdict the lead rebuilt the deck with 6 slides and 3 questions. The lead added the slide `context` ("Where we are": goal, method, problem). Each slide got one grey line (`class="ctx"`) that tells what was done and on which galaxies. Each question got one line that tells why it is important (`class="qwhy"`). The slides `problem`, `slope`, `prior-us` and `decided` were removed. His next message asked for a skill "for making these slides". The two detail slides brought the deck to 8 slides: `cover`, `context`, `data`, `bins`, `evidence`, `why`, `prior`, `questions`.

## Steps

1. **Start.** The job `com.liuhao.weekly-slides` sends the message on Thursday at 20:00, or at the next wake or login. A second copy in one week is possible. Update the deck one time for each week. Read `~/.claude/projects/-Users-liuhao-Downloads-Astro-project/memory/sandro-open-questions-deck.md` for words that he said after 2026-11-25.
2. **Collect the week.** Use only the three sources that he picked.
   - Chats: the session files `~/.claude/projects/-Users-liuhao-Downloads-Astro-project/*.jsonl` of the Astronomy lead. A worker session starts with the message "Read your brief at". Do not use a worker session.
   - New results: the entries of the week in `wiki/log.md`, and the pages that they name.
   - Handwritten notes: the `notes` tools, folder `Research`. Read "Liu Hao's handwritten notes are searchable" in `~/.claude/CLAUDE.md`.
3. **Get the deck files.** Read the index, then each slide that you will change:
   ```
   Artifact {"action": "read", "url": "https://claude.ai/artifact/N1yaFvoNBaEzuEirFBFx9q", "path": "project/deck.json"}
   Artifact {"action": "read", "url": "https://claude.ai/artifact/N1yaFvoNBaEzuEirFBFx9q", "path": "project/slides/<id>.html"}
   ```
   The result gives the location of each saved file. The artifact is the master copy. The files of the run are in `/private/tmp/claude-501/-Users-liuhao-Downloads-Astro-project/0e9cd474-3a15-4f3d-8102-ef966ca17496/scratchpad/deck/project/`. A restart can clear that folder.
4. **Write the slides of the week.** Each slide is one file `project/slides/<id>.html` with one `<section id="<id>">`. Use the classes in `project/deck.css`. Add each new id to `order` in `project/deck.json`, after `cover`. Update the slide `questions`. Update the date on `cover`. Keep each other key of `project/deck.json` as you read it.
5. **Write the slide text in his style.** Start the `write-like-liu-hao` skill. Use his own phrases from the chats of the week.
6. **Use only figures that exist.** Take a figure from the results of that week. Draw nothing. Run nothing. The run of 2026-11-25 put no figure on a slide. The file `artifact-type/reference/images.md` of the Slides type is about images.
7. **Update the two detail slides.** See "Detail slides". Read each source again each week. Do not copy a number from this skill or from an old slide.
8. **Publish to the same link.** Send only the changed files:
   ```
   Artifact {"url": "https://claude.ai/artifact/N1yaFvoNBaEzuEirFBFx9q", "root": "<folder that contains project/>", "file_path": "<root>/project/deck.json", "files": {"project/slides/<id>.html": "project/slides/<id>.html"}}
   ```
   - `file_path` is the absolute path of one changed file. `files` holds the other changed files.
   - Send `project/deck.json` only when the title, `order`, `sections` or `faces` change.
   - To remove a slide, delete its id from `order` and set `"project/slides/<id>.html": null` in `files`.
   - Obey the instructions that the Artifact tool returns. They can change.
9. **Tell him.** Write one line with the link.

## Detail slides

Slide `data`, "Data and what is fitted". One column for each survey. Wavelengths are rest-frame, vacuum, in Å.

| Row | Source |
|---|---|
| Galaxies fitted | `~/.claude/projects/-Users-liuhao-Downloads-Astro-project/memory/current-samples-and-spectral-window.md`, then the report that it names for the current sample |
| Redshift | The fits of the current sample. On 2026-11-25: column `z` of `results/dr3-more-galaxies-2026-11-16/fits.csv` (LEGA-C DR3) and row "Redshift" of `results/sdss-50-2026-11-24/t_481e53cf-detail.md` (SDSS DR17) |
| Range fitted | `rest_range` in the `experiment.json` of the run |
| Lines fitted | `.agents/skills/chronometer-checklist/SKILL.md`, "Absorption features, rest 3600 to 7100 Å". Give the features that are in `rest_range` and not masked |
| Lines masked | Same skill, table "Masked pixels" (columns "Surveys" and "Physical reason"), and `masked_absorption_features` in the `experiment.json` of the run |

The slide of the run gives the reason for the masks in one line below the table (`class="src"`).

Slide `bins`, "Age bins of the star formation history". It shows each bin edge in Gyr.

- The rule is in `notebooks/ceridwen_integrated_photometry_spectra.ipynb`: `sfh_nbins` in `SETTINGS` (cell 2) and the lines at `sfh_tbinmax_yr` (cell 8). Read the rule there.
- The grid length of a run is `sfh_grid_age` in its `experiment.json` (Gyr, the same for each galaxy). When `sfh_grid_age` is `None`, the grid length is the age of the Universe at the redshift of the galaxy.
- The command of the run, without the grid of the group. Run it in `/Users/liuhao/Downloads/Astro project`. `ours` is the notebook rule for 14 bins. Change `ours` if the notebook rule is different.
  ```
  ceridwen/.venv/bin/python - <<'EOF'
  import numpy as np
  from astropy.cosmology import Planck18
  def ours(T): return np.concatenate([[0,0.03],np.logspace(np.log10(0.1),np.log10(0.85*T),12),[T]])
  np.set_printoptions(precision=3,suppress=True,linewidth=250)
  print('15',ours(15.0))
  for z in (0.1,0.7):
      T=Planck18.age(z).value; print(z,round(T,3),ours(T))
  EOF
  ```
- The slide of the run has two rows for our grid. One row is the 15 Gyr grid. The other row ends at the age of the Universe at z = 0.7.
- The slide of the run also has the 12-bin SFMS grid of the group at z = 0.7 and z = 0.1. The run did not record the file that gives that rule. The slide tells that the oldest edge of that grid is an assumption.

## How the deck started

The deck has one link. These calls of 2026-11-25 are the record.

1. `Artifact {"action": "quickstart", "intent": "slides"}`. The result gave the Slides type.
2. `Artifact {"type_url": "https://claude.ai/artifact/8jTsAFQMFDb2oA8MsPJ2eL", "title": "Chronometer: open questions", "auto_open": "after_first_write"}`. No files. The result gave the link and the file rules.
3. The lead wrote `project/deck.json` first, with each slide id in `order`. Then `project/deck.css` and `project/slides/cover.html`. One call published the three files: `url`, `root`, `file_path` of `project/deck.json`, the other two files in `files`.
4. The lead wrote the other slides. One more call with the same `url` and `root` published them.
