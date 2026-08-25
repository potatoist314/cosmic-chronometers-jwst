# Papers

Local reference PDFs are stored here and excluded from version control, so this
index is the only in-repo record of which literature the project is working
from. Keep it current when a paper is added or removed.

Root-level PDFs cover cosmic chronometers; topic subdirectories group related
literature. Every paper remains listed in this table.

Full citations are recorded only where they have actually been confirmed. Do
not fill in the unrecorded ones by guessing — check the PDF.

| File | Citation | Role |
| --- | --- | --- |
| `Toward a Better Understanding of Cosmic Chronometers - A New Measurement of H(z) at z 0.7.pdf` | Borghi et al. (2022b) | **Current target** (brief steps 1–2): differential ages → `H(z)` at `z ~ 0.7`. Table 1 and Eq. 2 are the numbers to match; §3.1 is the uncertainty budget |
| `Toward a Better Understanding of Cosmic Chronometers - Stellar Population Properties of Passive Galaxies at Intermediate Redshift.pdf` | Borghi et al. (2022a), "Paper I" | Companion paper for the same sample; source of the Lick index sets and the age–redshift relations |
| `Revisiting the Oldest Stars as Cosmological Probes.pdf` | Cimatti & Moresco (2023), ApJ 953:149 | Parked. Absolute stellar ages → `H0` in flat ΛCDM. Its printed Eq. 4 appears to omit the square on `sigma_age`; a standard Gaussian log-likelihood needs `sigma_age**2` |
| `Implications for the Hubble Tension from the Ages of the Oldest Astrophysical Objects.pdf` | not recorded | Background on absolute-age constraints and the Hubble tension |
| `Cosmic Chronometers with Photometry - A New Path to H(z).pdf` | not recorded | Alternative route to `H(z)`; background |
| `Setting the Stage for Cosmic Chronometers I - Young Stellar Populations.pdf` | not recorded | Cosmic-chronometer sample selection and contamination |
| `Setting the Stage for Cosmic Chronometers II - SPS Systematics and Full Covariance Matrix.pdf` | not recorded | SPS systematics and the covariance treatment implemented in `external/CCcovariance/` |
| `spectral fitting/Alpha-MC - Self-consistent Alpha-enhanced Stellar Population Models Covering a Wide Range of Age, Metallicity, and Wavelength.pdf` | Park et al. (2025), ApJ 994:165, arXiv:2410.21375 | Self-consistent alpha-enhanced isochrones and stellar spectra for age, abundance, and full-spectrum modelling |
| `spectral fitting/Fast, Slow, Early, Late - Quenching Massive Galaxies at z 0.8.pdf` | Tacchella et al. (2022), ApJ 926:134, arXiv:2102.12494 | Prospector fits to spectra plus photometry; constrains diverse star-formation and quenching histories |
| `spectral fitting/Decoding the Variability in the Star Formation Histories of z 0.8 Galaxies.pdf` | Wan et al. (2025), MNRAS 539:2891–2909, arXiv:2504.05281 | Stochastic SFH fits to 1,928 LEGA-C galaxies; measures long- and short-timescale SFMS scatter |
| `spectral fitting/Stochastic Prior for Non-parametric Star-formation Histories.pdf` | Wan et al. (2024), MNRAS 532:4002–4025, arXiv:2404.14494 | Defines and validates the Prospector stochastic SFH prior used by Wan et al. (2025) |
| `spectral fitting/A Census of Star Formation Histories of Massive Galaxies at z 0.6-1 with Bagpipes and Prospector.pdf` | Kaushal et al. (2024), ApJ 961:118, arXiv:2307.03725 | Fits the full LEGA-C sample with Prospector and Bagpipes; exposes SFH-model dependence |
| `spectral fitting/More Is Better - Strong Constraints on LEGA-C Stellar Properties with Prospector.pdf` | Nersesian et al. (2025), A&amp;A 695:A86, arXiv:2502.03021 | Joint Prospector fits constrain LEGA-C ages, metallicities, dust, and stellar masses |
| `spectral fitting/Less Is Less - Photometry Alone Cannot Predict LEGA-C Spectral Indices.pdf` | Nersesian et al. (2024), A&amp;A 681:A94, arXiv:2310.18000 | Shows photometry-only Prospector fits cannot recover detailed age- and metallicity-sensitive spectra |

The "role" column records why each paper is here, not an agreed plan to use it.

See the [concise stellar-population fitting review](spectral%20fitting/README.md).
