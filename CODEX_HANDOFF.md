# Codex Session Handoff

Exported: 2026-07-20 (Europe/London)

This is a structured history and continuation brief for moving the project from
the Codex desktop task into the VS Code Codex extension. It is not a verbatim
chat transcript; it preserves the decisions, scientific context, current state,
and exact next step needed to resume without repeating work.

## Resume instructions for Codex

1. Read `AGENTS.md` in full and follow it as the controlling project-specific
   coaching agreement.
2. Read this handoff before assigning another task.
3. Treat the project as a learning-first coaching exercise. Do not provide code
   or edit the scientific implementation unless the user explicitly relaxes
   that rule.
4. Continue from the deterministic integral benchmark described under
   **Current position and next step**. Do not repeat the derivation of the
   lookback-time relation; the user has demonstrated that they understand it.
5. During active coaching, explain the concept and give exactly one 5-10 minute
   task at a time.

A suitable first message in the new session is:

> Read `AGENTS.md` and `CODEX_HANDOFF.md`, then continue coaching from the
> recorded next step. Do not repeat material marked as understood.

## Project

**Title:** Stellar Ages of Massive Quiescent Galaxies with JWST: Testing the
Cosmic Chronometer Method

The larger goal is to assess whether improved stellar-population ages from
JWST can make the cosmic-chronometer method a robust and competitive probe of
the expansion history. Topics include age dating, metallicity and
star-formation-history degeneracies, progenitor bias, selection effects,
mock-data forecasts, and comparisons with Lambda-CDM and other cosmological
probes.

The primary purpose for the user is skill development: research practice,
physical and mathematical understanding, scientific programming, uncertainty
analysis, and Bayesian inference. Producing results quickly is secondary to the
user being able to explain and reproduce them independently.

## Time and scope

- Work began around 20 July 2026.
- The working horizon is the beginning of October 2026.
- The user can spend about half their working time on this project because a
  fusion project is running concurrently.
- The user expects to travel for two weeks near the end of August.
- This corresponds to roughly four full-time-equivalent research weeks.
- The basic published reproduction and mock/MCMC framework should ideally be
  supervisor-ready on GitHub before travel.

The agreed phase plan and must-have versus stretch scope are recorded in
`AGENTS.md`.

## Coaching agreement

The user supplied a tutoring prompt previously used successfully for a fusion
project. It was adapted and saved in `AGENTS.md`. The essential rules are:

- Explain the scientific concept before the practical operation.
- Do not provide code, copy-paste pseudocode, or a complete implementation
  unless the user explicitly asks to suspend this rule.
- The user writes and runs all scientific code.
- Give one manageable task at a time, normally taking 5-10 minutes.
- Use layered hints: concept, then inputs/outputs/shapes/units, then the type of
  operation, and only then exact syntax if explicitly requested.
- Check dimensions, units, ranges, boundary values, invariants, and physical
  plausibility.
- Identify errors directly and give one next correction.
- Do not accept a result because it merely looks plausible.
- Maintain continuity and prioritize scientific reasoning over cosmetic work.
- For requested live VS Code inspection, operate read-only and do not execute
  cells or modify the editor state.

Astronomy-specific distinctions that must remain explicit include stellar age
versus cosmic age, formation time versus formation redshift, lookback time
versus cosmic time, `H0` versus `H(z)`, absolute versus differential age
methods, likelihood versus prior information, and statistical versus systematic
uncertainty.

## First reproduction paper

The user confirmed that the first paper to reproduce is:

`Revisiting the Oldest Stars as Cosmological Probes.pdf`

This is Cimatti & Moresco (2023), *The Astrophysical Journal*, 953:149.

Important conceptual distinction: this paper is not a model-independent,
differential cosmic-chronometer measurement of `H(z)`. It constrains `H0` from
absolute stellar ages while assuming flat Lambda-CDM and priors on the matter
density and formation redshift. It is being used first because it provides a
clean introduction to cosmic-time integrals, priors, degeneracies, systematic
errors, and MCMC.

For an object formed at redshift `zf` and observed today,

\[
t_{\rm age}=\frac{1}{H_0}\int_0^{z_f}\frac{dz}{(1+z)E(z)},
\]

with flat-Lambda-CDM expansion function

\[
E(z)=\sqrt{\Omega_M(1+z)^3+(1-\Omega_M)}.
\]

When age is in Gyr and `H0` is in km/s/Mpc, the paper writes

\[
H_0=\frac{977.8}{t_{\rm age}/{\rm Gyr}}
\int_0^{z_f}\frac{dz}{(1+z)E(z)}.
\]

The redshift integral is dimensionless. At fixed `zf` and `Omega_m`, increasing
the stellar age decreases the inferred `H0`.

## First quantitative target

Reproduce the Section 5 reference case before attempting individual objects or
sample averages:

- measured age: `13.5 +/- 0.5 Gyr`;
- `H0 ~ Uniform(50, 100) km/s/Mpc`;
- `zf ~ Uniform(11, 30)`;
- `Omega_m ~ Normal(0.30, 0.02)`;
- reported result:
  `H0 = 69.06 (+2.96, -2.77) km/s/Mpc`, subject to rounding and the paper's
  posterior-summary convention.

The deterministic cosmology calculation must be validated before introducing
`emcee`.

The printed Equation 4 appears to show the age uncertainty rather than its
square in the denominator. If `sigma_age` is a standard deviation, dimensional
analysis and the standard Gaussian likelihood require `sigma_age**2`. This
must be investigated explicitly rather than silently corrected.

## History of the session

1. The user supplied the overall JWST/cosmic-chronometer project description,
   literature list, supervisor roadmap, time horizon, travel constraint, and
   request for a learning-focused plan.
2. The repository was inspected. It was at a very early stage: no commits,
   empty README, a nearly empty notebook, and initial cosmology functions in
   `src/cosmology.py`.
3. A phased plan through early October was agreed, prioritizing physical
   understanding, one careful reproduction, a validated mock/MCMC framework,
   controlled systematics, and a high-redshift forecast.
4. The user confirmed that coaching and pair programming are preferred and
   supplied the fusion-project tutoring prompt.
5. The prompt was adapted for astronomy and saved as `AGENTS.md`.
6. The user identified *Revisiting the Oldest Stars as Cosmological Probes* as
   the first reproduction target and wanted to complete its first stage on
   20 July.
7. The initial coaching task was to derive the lookback-time relation. The user
   shared a handwritten derivation showing `a=1/(1+z)`,
   `dt=-dz/[(1+z)H(z)]`, and the positive integral from `z=0` to `zf`.
8. The derivation was accepted as understood. The user explicitly asked to move
   past it.
9. The next assigned step was the fixed-parameter deterministic numerical
   benchmark described below. The user has not yet reported its result in this
   exported session.

## Current position and next step

Do not repeat the derivation. The immediate objective is to test the numerical
integral and unit conversion independently of MCMC.

The fixed benchmark is:

- `Omega_m = 0.3`;
- `zf = 20`;
- `t_age = 13.5 Gyr`.

The user was asked to calculate

\[
I=\int_0^{20}\frac{dz}{(1+z)E(z)}
\]

and then

\[
H_0=\frac{977.8}{13.5}I.
\]

Expected checks:

- `I` is dimensionless and approximately `0.95`;
- `H0` is approximately `69 km/s/Mpc`;
- no MCMC should be started until these two values are understood and checked.

The next Codex response should first ask whether the user has implemented this
benchmark in the VS Code notebook. If not, explain only the numerical purpose
and assign that single task. If it has been implemented, inspect the visible
code and output read-only, following `AGENTS.md`, and give one next correction
or progression.

## Saved repository state at export

The following observations are from the saved filesystem at export time and
may lag unsaved VS Code content:

- Git repository exists on branch `main` but has no commits yet.
- All current project files are untracked.
- `README.md` is empty.
- `AGENTS.md` contains the complete coaching contract and project plan.
- `notebooks/01_age_of_universe.ipynb` contains one code cell whose saved source
  is the incomplete text `### Sign disapp`, with no saved output. Do not assume
  this reflects the current live editor state.
- `src/cosmology.py` currently defines `E(z, omega_m)`, `H(z, H0, omega_m)`, and
  `age_integrand(z, H0, omega_m)` and imports NumPy, Astropy units, and SciPy's
  quadrature function.
- The numerical integration and reference posterior have not been confirmed in
  the exported session.

## Locally available literature

- `Revisiting the Oldest Stars as Cosmological Probes.pdf`
- `Implications for the Hubble Tension from the Ages of the Oldest Astrophysical Objects.pdf`
- `Toward a Better Understanding of Cosmic Chronometers - A New Measurement of H(z) at z 0.7.pdf`
- `Cosmic Chronometers with Photometry - A New Path to H(z).pdf`
- `Setting the Stage for Cosmic Chronometers I - Young Stellar Populations.pdf`
- `Setting the Stage for Cosmic Chronometers II - SPS Systematics and Full Covariance Matrix.pdf`

The later differential-age reproduction will likely use the Borghi et al.
`z ~ 0.7` paper, but that is not the immediate task.

## Files to open first in VS Code

- `AGENTS.md`
- `CODEX_HANDOFF.md`
- `notebooks/01_age_of_universe.ipynb`
- `src/cosmology.py`
- `Revisiting the Oldest Stars as Cosmological Probes.pdf`
