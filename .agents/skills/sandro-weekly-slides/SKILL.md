---
name: sandro-weekly-slides
description: 'Use when you make or update the slide deck for Liu Hao''s weekly meeting with Sandro, or when the message "weekly slides: summarise the past week in the Sandro deck" arrives. It gives all his slide preferences in his words, the Artifact calls in order, and the source of each fact on the detail slides.'
---

# Weekly slides for the meeting with Sandro

Written from two runs by the Astronomy lead. The run of 2026-11-25 (15:13 to 15:44 UTC) made the deck and rebuilt it one time. The run of 2026-11-26 (from 13:57 UTC) removed the cover. The record of the two runs is `~/.claude/projects/-Users-liuhao-Downloads-Astro-project/0e9cd474-3a15-4f3d-8102-ef966ca17496.jsonl`. No weekly update has run yet. The first weekly message is due on 2026-11-26.

The deck is "Chronometer: open questions": https://claude.ai/artifact/N1yaFvoNBaEzuEirFBFx9q. It is a claude.ai Slides artifact. It is private to Liu Hao. Sandro can open it only after Liu Hao shares it from the Share menu of the page.

Rules for figures, physical facts and browser pages are in `AGENTS.md` and `~/.claude/CLAUDE.md`. Read them there.

## His words

This section holds each slide preference that he gave, in date order (UTC). The lead wrote each question and each option. "Question" shows a question that the lead asked him. "Picked" shows the label of an option that he selected. "The option said" shows text of that option. Each of these is word for word from the record. All other text in quotation marks is his.

### 2026-11-19: figures

He said these words about figure previews. The record is `44a318fe-f8bc-458f-a1fc-c4c5cd719664.jsonl`, in the folder of the record of the runs. `~/.claude/CLAUDE.md` holds the rule that came from the second quote.

- **Simple.** "okay. that seems useful. but it should be simple and clear"
- **No explanations in a figure.** "just dont add explanations in figures please, they should speak for themselves. axes, titles, labels. no annoying explanations" Then: "for all future figures - save preference"
- **Fake galaxies in a figure.** "the mock truth stuff is very confusing. can you not mix it in with real data runs"
- **Physical meaning.** "also, theres no interesting physical trend here.. can you put t80 t50 t20 against age, or whatever is appropriate to look into downsizing. like the graphs should all have some physical intuition or grounding behind them"

### 2026-11-24: an explanation in the chat

- **Fake galaxies in an explanation.** "I don't like the over-reference to the fake galaxies". These words start a longer message. He said them about an explanation in the chat, not about the deck.

### 2026-11-25: the deck

- **Purpose.** "i need you to track these discussions and open questions somewhere clear. honestly, putting them into a slide would be good. for weekly discussions w sandro"
- **Style.** "use the write like me style for this please."
- **Schedule.** "this slide generation should run automatically weekly to summarise the past week's discussion"
- **Meeting day.** Question: "Which day is your weekly meeting with Sandro? The slides would be made the evening before." Answer: "friday"
- **Sources.** Question: "What should count as 'the past week's discussion' when the weekly slides are written?" Picked: "Chats with me (Recommended)", "New results", "Handwritten notes". He did not pick "Other Astro chats".
- **Deck.** Question: "How should each week's slides be kept?" Picked: "One running deck (Recommended)". The option said: "Same link every week. The new week's slides go first, the open-questions slide is updated, older weeks stay further back."
- **Review.** Question: "Should the weekly slides go live on their own, or wait for you to look first?" Picked: "Go live, tell me (Recommended)". The option said: "The deck updates on its own and I tell you in one line that it is ready."
- **Length.** Question: "How much should each week's update be?" Picked: "3 to 5 slides (Recommended)". The option said: "What was discussed, what was decided, any new result, and the updated open questions."
- **Figures.** Question: "When a result from that week has a figure, should the weekly slides show it?" Picked: "Yes, existing figures (Recommended)". The option said: "Use figures that already exist from that week's results. Nothing new is drawn or run."
- **Laptop asleep.** Question: "The slides are made on Thursday evening on this laptop. What if the laptop is asleep or off then?" Picked: "Run when it wakes (Recommended)".
- **Verdict on the first version** (8 slides, 7 open questions): "i have significant issues with this. too many open questions, not enough context (big issue!), too verbose"
- **Detail.** "more detail to include: wavelength ranges and lines per survey, what lines are masked, redshift ranges" and "also show the exact age ranges for bins"
- **Prior against posterior.** "i'd like a posterior plot showing how much exactly the sfh posterior has changed against the prior from our fits. ie plot both on same graph. maybe some stacked posterior versus original sfh prior. but explain how you stack the posterior"
- **Version of that figure.** Question: "Three versions of the prior against posterior figure are open in Preview (60 LEGA-C galaxies stacked, prior in grey, posterior in blue). Which one should go in the deck?" Picked: "Star formation rate (Recommended)". The first sentence of the option said: "Star formation rate against lookback time, relative to each galaxy's average." He did not pick "Mass fraction per bin" or "Cumulative mass".
- **Figure labels.** "do label the prior and posterior a bit more and add a short caption to the figure. explain age of universe is constrained by planck lambda cdm and circularity worries". He said this about the figure on the slide `stack`.
- **Order.** "organise the slides in a sensible coherent order"
- **Free parameters.** "carbon very important - this free parameter stuff is equally important to be tracked as compared to masks"
- **C and N.** "in skill and slides you need to explain how cn free works"

Facts of the run. They are not his rules. After the verdict the lead rebuilt the deck with 6 slides and 3 questions. The lead added the slide `context` ("Where we are": goal, method, problem). Each slide got one grey line (`class="ctx"`) that tells what was done and on which galaxies. Each question got one line that tells why it is important (`class="qwhy"`). The slides `problem`, `slope`, `prior-us` and `decided` were removed. His next message asked for a skill "for making these slides". The two detail slides brought the deck to 8 slides: `cover`, `context`, `data`, `bins`, `evidence`, `why`, `prior`, `questions`.

### 2026-11-26: the deck

- **Cover.** "can you remove the front slide"
- **Text.** "can you humanise much of the text and give more context. i'm not sure how to best prompt you to accomplish this because the slides always read like slop"
- **New slides.** "add a slide showing mock vs real galaxies that demonstrated fixed systematic offset is okay as long as slope isn't affected. add a slide showing possible surveys, wavelength range, passive galaxy count, and how age slope error scales with these. add a slide on limitations of the ssp grid and explain how Ca masking, C/N free is an attempt to work around this."
- **Slop.** "i think a main issue i have with slop ness is that there's excessive inscrutable commentary that is only understood by the agent and not by people outside. maybe let figures speak for themselves, and give very simple context"
- **Figures, not tables.** "i prefer figures/graphs over tables. i don't really want explanations or commentary. no need for titles, or keep titles a handful of words"
- **This skill.** "save all slide preferences in a skill"

He said the next two quotes in one message at 14:17 UTC. They are about the version of the deck with figures. The message had one picture for each quote.

- **Surveys slide** (picture: the figure of the slide `surveys`). "this slide: no, i think just show expression you gave me where redshift range is linear and number of galaxies is square root and a graph showing how error changes for extra runs with these."
- **Age-bin figure, cosmology slide** (picture: the slide `bins`). "i don't quite understand the x axis on this age bin diagram, and i don't understand the two group things. add an extra slide diagram for cosmology independence"
- **Masked and free lines** (14:24 UTC, with the slide `data` open). "add very short physical explanation for why certain lines are masked or free on the data / model slides, maybe with excerpts from the original paper"
- **Cosmology slide, a slide to remove** (14:27 UTC, with a picture of the slide "Age offset and slope"). "for cosmology independence slide, add an excerpt from the borghi paper. show the results on age difference recovery with different age grids. show results before and after on lega c with different grids. i dont see the role of this attached slide it can go."
- **True and fitted history** (14:35 UTC, with the slide `agediff` open). "show sfh differences for age difference recovery -> the fake galaxy sfh vs recovered sfh"
- **Effect of the age differences** (14:39 UTC, with the slide `agediff` open and a picture of the figure of the slide `sfhrec`). "show effect of not recovering age differences super well here on this slide, the current diagram isn't so good"
- **Age-bin figure** (14:42 UTC, with a picture of the slide `bins`). "don't need the zoom, shorten the last vs before captions"
- **Which fit is which** (14:43 UTC, a comment on the figure of the slide `agediff`). "i don't understand which is which? which is planck and which is 15 gyr?"
- **Names of the two fits** (14:46 UTC, with a picture of the H(z) panel of the figure of the slide `agediff`). "dont need this. i think to shorten things just call everything planck or cosmology independent consistently through slides"

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
4. **Write the slides of the week.** Each slide is one file `project/slides/<id>.html` with one `<section id="<id>">`. Use the classes in `project/deck.css`. The deck has no cover slide (2026-11-26, **Cover**). Add each new id at the start of `order` in `project/deck.json` (2026-11-25, **Deck**). Update the slide `questions`. Keep each other key of `project/deck.json` as you read it.
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
| Galaxies fitted | LEGA-C DR3: line "Chain" of `results/dr3-more-galaxies-2026-11-16/REPORT.md`. SDSS DR17: the number of `targets` in `results/sdss-wide-range-2026-11-24/experiment.json` and in `results/sdss-mask-nad-2026-11-24/experiment.json` |
| Redshift | LEGA-C DR3: column `z` of `results/dr3-more-galaxies-2026-11-16/fits.csv`. SDSS DR17: row "Redshift" of `results/sdss-50-2026-11-24/t_481e53cf-detail.md`. The two wide SDSS runs fit the same 50 `targets` |
| Range fitted | `.agents/skills/chronometer-checklist/SKILL.md`, section "Masked pixels", line "Pixels outside the window are not fitted" |
| Lines fitted | Same skill, "Absorption features, rest 3600 to 7100 Å". Give the features that are in the range fitted and not masked |
| Lines masked | Same skill, table in the section "Masked pixels" (columns "Surveys" and "Physical reason") |
| Abundances free | Same skill, section "Free and fixed parameters": the table of parameters, and the table "C and N in each run". For each run on the slide, read `settings.abundance_response` of each fit in its `manifest.json`. Do not use the `priors` block of the manifest |

The memory file `~/.claude/projects/-Users-liuhao-Downloads-Astro-project/memory/current-samples-and-spectral-window.md` names the result folder of each sample. Read it first. The folders in the table are those that it names on 2026-11-25.

The slide of the run gives the reason for the masks in one line below the table (`class="src"`).

Slide `cnfree`, "How free C and N work". The deck holds this slide after the slide `data` in `order` of `project/deck.json`. Its file is `project/slides/cnfree.html`. The lead added it on 2026-11-25. The source of each statement on it is the section "How free C and N work" of `.agents/skills/chronometer-checklist/SKILL.md`. That section gives the lines of `ceridwen/ceridwen/ssps/abundance_response.py` and the alf files.

Slide `bins`, "Age bins of the star formation history". It shows each bin edge in Gyr.

- The rule for our grid is in `notebooks/ceridwen_integrated_photometry_spectra.ipynb`: `sfh_nbins` in `SETTINGS` (cell 2) and the lines at `sfh_tbinmax_yr` (cell 8). Read the rule there.
- The grid length of a run is `sfh_grid_age` in its `experiment.json` (Gyr, the same for each galaxy). When `sfh_grid_age` is `None`, the grid length is the age of the Universe at the redshift of the galaxy.
- The rule for the grid of the group is the function `zred_to_agebins_extra_young` in `~/Downloads/age bin definition.rtf`. It gives 12 bins. The edges are 0, 3 Myr, 5 Myr and 10 Myr, then 9 more log-spaced edges to `tbinmax`. To read the file: `textutil -convert txt -stdout ~/Downloads/"age bin definition.rtf"`.
- The file does not give the constants `Z_LIMIT_SFH` and `TBINMAX_FLOOR_YR`. Thus the slide uses the age of the Universe for `tbinmax`. The slide says that this is an assumption.
- The command of the run. Run it in `/Users/liuhao/Downloads/Astro project`. `ours` is the notebook rule for 14 bins. `grp` is the function of the group with `tbinmax` equal to the age of the Universe. Change a function if its rule is different.
  ```
  ceridwen/.venv/bin/python - <<'EOF'
  import numpy as np
  from astropy.cosmology import Planck18
  def ours(T): return np.concatenate([[0,0.03],np.logspace(np.log10(0.1),np.log10(0.85*T),12),[T]])
  def grp(T):
      e=np.append([0,np.log10(3e6),np.log10(5e6),7],np.linspace(7,np.log10(T*1e9),10)[1:]); return np.concatenate([[0],10**e[1:]/1e9])
  np.set_printoptions(precision=3,suppress=True,linewidth=250)
  print('15',ours(15.0))
  for z in (0.1,0.7):
      T=Planck18.age(z).value; print(z,round(T,3)); print(' ours',ours(T)); print(' grp ',grp(T))
  EOF
  ```
- The slide of the run has two rows for our grid. One row is the 15 Gyr grid. The other row ends at the age of the Universe at z = 0.7.
- The slide of the run also has two rows for the grid of the group: z = 0.7 and z = 0.1.

## How the deck started

The deck has one link. These calls of 2026-11-25 are the record.

1. `Artifact {"action": "quickstart", "intent": "slides"}`. The result gave the Slides type.
2. `Artifact {"type_url": "https://claude.ai/artifact/8jTsAFQMFDb2oA8MsPJ2eL", "title": "Chronometer: open questions", "auto_open": "after_first_write"}`. No files. The result gave the link and the file rules.
3. The lead wrote `project/deck.json` first, with each slide id in `order`. Then `project/deck.css` and `project/slides/cover.html`. One call published the three files: `url`, `root`, `file_path` of `project/deck.json`, the other two files in `files`.
4. The lead wrote the other slides. One more call with the same `url` and `root` published them.
