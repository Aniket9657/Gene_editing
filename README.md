# 🧬 Gene Modification & Cross-Species Simulation

> **Educational simulation tool** — Not scientifically accurate.
> Inspired by real genetics but heavily simplified for learning and exploration.

---

## 📌 Overview

An interactive Python + Streamlit application that simulates:

- **Gene editing** — mutate, knockout, or overexpress real genes in animals
- **Cross-species gene mixing** — transfer genes between animals based on genetic similarity
- **Trait prediction** — see how edits affect physical, behavioral, and survival traits
- **Genetic similarity mapping** — visualize how closely related 10 animals are

Built as an **educational prototype** demonstrating concepts from genomics, comparative biology, and synthetic biology.

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install streamlit pandas matplotlib numpy
```

### 2. Run the app

```bash
streamlit run app.py
```

### 3. Open in browser

```
http://localhost:8501
```

No API key required. Runs fully offline.

---

## 🖥️ Features

### Tab 1 — Gene Editing

- Select any of 10 animals
- Choose genes to edit (multi-select)
- Apply one of three actions:
  - **Mutate** — standard mutation effect
  - **Knockout** — complete gene silencing (stronger negative effect)
  - **Overexpress** — amplified gene activity (stronger positive effect)
- Adjust **biological uncertainty** (noise slider) to simulate real-world variability
- Output:
  - Trait delta table (color-coded ▲ ▼)
  - Composite scores (Physical, Behavioral, Survival Probability)
  - Bar chart comparison (original vs modified)
  - Radar chart of modified profile

### Tab 2 — Cross-Species Gene Mixing

- Select a **base animal** (recipient) and a **donor animal**
- System computes **genetic similarity** using mock DNA sequence comparison
- Gene transfer is **blocked if similarity < 85%** (biology-inspired constraint)
- Select which donor genes to transfer
- Output:
  - Side-by-side radar charts (original vs hybrid)
  - Full trait comparison bar chart
  - Composite scores for the hybrid

### Tab 3 — Animal Profiles

- Full trait table for any of the 10 animals
- Mock DNA sequence display
- Gene list with expression areas and functions
- Radar chart of base trait profile

### Tab 4 — Gene Library

- Searchable reference table for all 10 genes
- Shows: function, expression area, mutation / knockout / overexpress effects
- Trait impact map — which traits each gene affects and by how much

### Tab 5 — Similarity Map

- Heatmap of pairwise genetic similarity between all 10 animals
- Full similarity table sorted by score
- Visual indicator of which pairs are compatible for gene mixing (≥85%)

---

## 🐾 Animals Included

| Animal | Emoji |
|--------|-------|
| Lion | 🦁 |
| Tiger | 🐯 |
| Wolf | 🐺 |
| Cheetah | 🐆 |
| Elephant | 🐘 |
| Dolphin | 🐬 |
| Eagle | 🦅 |
| Gorilla | 🦍 |
| Snow Leopard | 🐱 |
| Shark | 🦈 |

---

## 🧪 Genes Used (Real Names, Simplified Functions)

| Gene | Real Function | Simulated Effect Area |
|------|--------------|----------------------|
| `MSTN` | Myostatin — inhibits muscle growth | Muscle mass, strength |
| `FOXP2` | Language and vocalization control | Intelligence, communication |
| `MC1R` | Melanocortin receptor — pigmentation | Coat color, UV resistance |
| `IGF1` | Insulin-like growth factor — body size | Size, strength, lifespan |
| `BRCA1` | DNA repair — tumor suppressor | Cancer resistance, lifespan |
| `EPAS1` | Hypoxia-inducible factor — oxygen | Altitude tolerance, endurance |
| `ACTN3` | Fast-twitch muscle fiber protein | Speed, explosive strength |
| `SLC24A5` | Melanin transport — pigmentation | Skin/coat color, UV resistance |
| `DRD4` | Dopamine receptor — behavior | Aggression, risk-taking |
| `EDAR` | Hair, teeth, sweat gland development | Thermal regulation, camouflage |

---

## 🏗️ Architecture

```
app.py
│
├── GENE_DB          — dict: 10 genes × functions, effects, trait impacts
├── ANIMALS          — dict: 10 animals × genes, base traits, DNA sequence
│
├── compute_similarity()   — Hamming distance on mock DNA sequences
├── apply_gene_edit()      — applies mutation/knockout/overexpress + noise
├── mix_genes()            — cross-species gene transfer (60% strength)
├── compute_scores()       — derives Physical, Behavioral, Survival scores
│
├── plot_trait_comparison() — bar chart: original vs modified
├── plot_radar()            — spider chart of trait profile
├── plot_similarity_heatmap() — pairwise similarity grid
│
└── Streamlit tabs
    ├── tab_gene_edit()
    ├── tab_cross_species()
    ├── tab_profiles()
    ├── tab_gene_library()
    └── tab_similarity()
```

---

## 🧠 How the Simulation Works

### Gene editing model

```
modified_trait = base_trait + (delta × action_multiplier × noise_factor)
```

| Action | Multiplier |
|--------|-----------|
| Mutate | 1.0× |
| Knockout | −1.5× |
| Overexpress | +1.8× |

Noise factor = `1 + random.uniform(-noise, +noise)`
Default noise = ±15% (adjustable via slider)

### Genetic similarity

Uses **Hamming distance** on 20-character mock DNA sequences:

```
similarity = (matching_positions / total_positions) × 100
```

Cross-species gene transfer is permitted only when `similarity ≥ 85%`.
Transferred genes apply at **60% strength** (cross-species penalty).

### Composite scores

```
Physical Score  = mean(muscle_mass, strength, speed, size)
Behavioral Score = mean(aggression, intelligence, communication)
Survival Probability = direct trait value (0.0 – 1.0)
```

---

## 📊 Traits Tracked

| Trait | Description |
|-------|-------------|
| Muscle Mass | Raw muscular development |
| Strength | Force output capability |
| Speed | Locomotion speed |
| Aggression | Territorial / predatory behavior |
| Intelligence | Problem-solving, learning |
| Communication | Vocalization, social signaling |
| Endurance | Sustained activity capacity |
| Body Size | Overall physical size |
| Camouflage | Environmental concealment |
| Lifespan | Expected longevity |
| Fat Ratio | Body fat percentage |
| Cancer Resistance | Tumor suppression efficiency |
| Altitude Tolerance | High-altitude oxygen adaptation |
| UV Resistance | Radiation tolerance |
| Thermal Regulation | Temperature management |
| Survival Probability | Overall survival score (0–1) |

---

## ⚠️ Scientific Disclaimers

1. **Polygenic traits** — Real traits like intelligence or size are controlled by hundreds or thousands of genes, not single edits.
2. **Similarity ≠ compatibility** — 85% DNA similarity does not guarantee functional gene transfer (e.g., humans and chimps share ~98.7% DNA but cannot exchange genes freely).
3. **Prediction is unsolved** — Accurately mapping gene → trait is one of the hardest open problems in biology.
4. **This is a simulation** — All outcomes are rule-based estimates, not biological predictions.

---

## 💡 Educational Use Cases

- Understanding gene function and expression
- Exploring concepts in comparative genomics
- Demonstrating CRISPR-style editing logic
- Teaching genetic similarity and phylogenetics
- Portfolio / interdisciplinary project in computational biology

---

## 🔮 Future Improvements

- [ ] Real DNA sequences from NCBI / Ensembl API
- [ ] Polygenic trait models (multiple genes → one trait)
- [ ] Evolutionary tree visualization
- [ ] ML-based trait prediction model
- [ ] Multi-language support
- [ ] Export simulation results as CSV / PDF
- [ ] Gene regulatory network graphs
- [ ] User-defined custom animals

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Streamlit | Interactive UI |
| Pandas | Data tables |
| Matplotlib | Charts (bar, radar, heatmap) |
| NumPy | Numerical computation |

---

## 📁 Project Structure

```
gene-simulation/
│
├── app.py          ← entire application (single file)
├── README.md       ← this file
└── requirements.txt
```

### requirements.txt

```
streamlit
pandas
matplotlib
numpy
```

---

## 🧪 Inspiration

Inspired by research in:

- **CRISPR-Cas9** gene editing
- **Genome-Wide Association Studies (GWAS)**
- **Comparative Genomics**
- How companies like **DeepMind (AlphaFold)** and **OpenAI** use AI to model biological systems

---

## 📌 Status

`MVP` — Minimum Viable Product.
Built for rapid prototyping, education, and portfolio demonstration.

---

## 📄 License

This project is for educational and non-commercial use only.
Gene names are real; all biological outcomes are fictional simulations.
