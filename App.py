# app.py — GenAI Gene Modification & Cross-Species Simulation
# Run:  streamlit run app.py
# Deps: pip install streamlit pandas matplotlib numpy

# ⚠️ DISCLAIMER: This is an educational simulation tool.
# All biology is simplified and NOT scientifically accurate.
# Do not use for real biological research.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random
import copy

# ─── Gene Data ────────────────────────────────────────────────────────────────
# Each gene has: function, expression_area, mutation_effect, knockout_effect,
# overexpress_effect, trait_impact (dict of trait → delta when mutated)

GENE_DB = {
    "MSTN": {
        "function":          "Myostatin — inhibits muscle growth",
        "expression_area":   "Muscle",
        "mutation_effect":   "Greatly increased muscle mass",
        "knockout_effect":   "Extreme muscle hypertrophy, reduced fat",
        "overexpress_effect": "Severe muscle wasting, weakness",
        "trait_impact": {
            "muscle_mass": +40, "strength": +35, "speed": +10,
            "aggression": +5,  "fat_ratio": -20, "survival": +0.05,
        },
    },
    "FOXP2": {
        "function":          "Forkhead box P2 — language and vocalization",
        "expression_area":   "Brain (Broca's area), Lungs",
        "mutation_effect":   "Altered vocalization patterns",
        "knockout_effect":   "Complete loss of complex vocalizations",
        "overexpress_effect": "Increased vocal complexity",
        "trait_impact": {
            "intelligence": +15, "communication": +30, "aggression": -10,
            "survival": +0.04,
        },
    },
    "MC1R": {
        "function":          "Melanocortin 1 receptor — pigmentation control",
        "expression_area":   "Skin, Hair follicles",
        "mutation_effect":   "Altered coat/skin color (red/yellow shift)",
        "knockout_effect":   "Loss of eumelanin → pale/albino phenotype",
        "overexpress_effect": "Darker pigmentation",
        "trait_impact": {
            "camouflage": -15, "uv_resistance": -10, "survival": -0.03,
        },
    },
    "IGF1": {
        "function":          "Insulin-like growth factor 1 — body size regulator",
        "expression_area":   "Liver, Muscle",
        "mutation_effect":   "Dwarfism or gigantism depending on variant",
        "knockout_effect":   "Severe growth retardation",
        "overexpress_effect": "Gigantism, increased organ size",
        "trait_impact": {
            "size": +35, "strength": +20, "lifespan": -10,
            "fat_ratio": +10, "survival": +0.03,
        },
    },
    "BRCA1": {
        "function":          "DNA repair — tumor suppressor",
        "expression_area":   "All tissues",
        "mutation_effect":   "Increased cancer susceptibility",
        "knockout_effect":   "Rapid tumor formation",
        "overexpress_effect": "Enhanced DNA repair efficiency",
        "trait_impact": {
            "lifespan": -20, "cancer_resistance": -30,
            "survival": -0.12,
        },
    },
    "EPAS1": {
        "function":          "Hypoxia-inducible factor — oxygen adaptation",
        "expression_area":   "Heart, Lung, Blood",
        "mutation_effect":   "High-altitude adaptation (Tibetan-like)",
        "knockout_effect":   "Oxygen deprivation sensitivity",
        "overexpress_effect": "Polycythemia — excess red blood cells",
        "trait_impact": {
            "endurance": +25, "altitude_tolerance": +40,
            "speed": +10, "survival": +0.06,
        },
    },
    "ACTN3": {
        "function":          "Alpha-actinin-3 — fast-twitch muscle fiber",
        "expression_area":   "Skeletal Muscle",
        "mutation_effect":   "Shift from power to endurance performance",
        "knockout_effect":   "Loss of explosive speed",
        "overexpress_effect": "Enhanced sprint performance",
        "trait_impact": {
            "speed": +30, "strength": +20, "endurance": -10,
            "survival": +0.02,
        },
    },
    "SLC24A5": {
        "function":          "Pigmentation — melanin transport",
        "expression_area":   "Skin",
        "mutation_effect":   "Lighter skin/coat pigmentation",
        "knockout_effect":   "Near-complete depigmentation",
        "overexpress_effect": "Darker pigmentation",
        "trait_impact": {
            "camouflage": -10, "uv_resistance": -15, "survival": -0.02,
        },
    },
    "DRD4": {
        "function":          "Dopamine receptor D4 — novelty seeking behavior",
        "expression_area":   "Brain (prefrontal cortex)",
        "mutation_effect":   "Increased risk-taking and exploratory behavior",
        "knockout_effect":   "Reduced dopamine signaling, apathy",
        "overexpress_effect": "Hyperactivity, impulsivity",
        "trait_impact": {
            "aggression": +15, "intelligence": +5,
            "communication": +10, "survival": -0.03,
        },
    },
    "EDAR": {
        "function":          "Ectodysplasin receptor — hair, teeth, sweat glands",
        "expression_area":   "Skin, Hair follicles, Teeth",
        "mutation_effect":   "Thicker hair, more sweat glands, shovel-shaped incisors",
        "knockout_effect":   "Ectodermal dysplasia — missing teeth/hair",
        "overexpress_effect": "Excessive hair density",
        "trait_impact": {
            "thermal_regulation": +15, "camouflage": +5, "survival": +0.02,
        },
    },
}

# ─── Animal Data ──────────────────────────────────────────────────────────────
# Each animal: genes (list), base_traits (dict), dna_sequence (mock 20-char)
# Similarity is computed via sequence matching (mock Hamming distance)

ANIMALS = {
    "Lion": {
        "genes": ["MSTN","FOXP2","MC1R","IGF1","BRCA1",
                  "EPAS1","ACTN3","SLC24A5","DRD4","EDAR"],
        "base_traits": {
            "muscle_mass": 75, "strength": 80, "speed": 70,
            "aggression": 85, "intelligence": 55, "communication": 50,
            "endurance": 60, "size": 75, "camouflage": 40,
            "lifespan": 55, "fat_ratio": 30, "survival": 0.72,
            "cancer_resistance": 65, "altitude_tolerance": 30,
            "uv_resistance": 60, "thermal_regulation": 65,
        },
        "dna_sequence": "ATCGGCTATGCGATCGGCTA",
        "emoji": "🦁",
    },
    "Tiger": {
        "genes": ["MSTN","FOXP2","MC1R","IGF1","BRCA1",
                  "EPAS1","ACTN3","SLC24A5","DRD4","EDAR"],
        "base_traits": {
            "muscle_mass": 80, "strength": 85, "speed": 75,
            "aggression": 80, "intelligence": 60, "communication": 45,
            "endurance": 65, "size": 80, "camouflage": 75,
            "lifespan": 55, "fat_ratio": 28, "survival": 0.70,
            "cancer_resistance": 62, "altitude_tolerance": 35,
            "uv_resistance": 55, "thermal_regulation": 60,
        },
        "dna_sequence": "ATCGGCTATGCGATCGGCTG",
        "emoji": "🐯",
    },
    "Wolf": {
        "genes": ["MSTN","FOXP2","MC1R","IGF1","BRCA1",
                  "EPAS1","ACTN3","SLC24A5","DRD4","EDAR"],
        "base_traits": {
            "muscle_mass": 65, "strength": 65, "speed": 70,
            "aggression": 75, "intelligence": 75, "communication": 80,
            "endurance": 80, "size": 55, "camouflage": 65,
            "lifespan": 50, "fat_ratio": 25, "survival": 0.68,
            "cancer_resistance": 60, "altitude_tolerance": 50,
            "uv_resistance": 50, "thermal_regulation": 75,
        },
        "dna_sequence": "ATCGGCTAAGCGATCGGCTA",
        "emoji": "🐺",
    },
    "Cheetah": {
        "genes": ["MSTN","FOXP2","MC1R","IGF1","BRCA1",
                  "EPAS1","ACTN3","SLC24A5","DRD4","EDAR"],
        "base_traits": {
            "muscle_mass": 60, "strength": 55, "speed": 98,
            "aggression": 60, "intelligence": 60, "communication": 45,
            "endurance": 50, "size": 50, "camouflage": 55,
            "lifespan": 45, "fat_ratio": 15, "survival": 0.58,
            "cancer_resistance": 50, "altitude_tolerance": 30,
            "uv_resistance": 65, "thermal_regulation": 55,
        },
        "dna_sequence": "ATCGGCTATGCGATCAGCTA",
        "emoji": "🐆",
    },
    "Elephant": {
        "genes": ["MSTN","FOXP2","MC1R","IGF1","BRCA1",
                  "EPAS1","ACTN3","SLC24A5","DRD4","EDAR"],
        "base_traits": {
            "muscle_mass": 85, "strength": 95, "speed": 30,
            "aggression": 50, "intelligence": 85, "communication": 85,
            "endurance": 70, "size": 98, "camouflage": 20,
            "lifespan": 80, "fat_ratio": 40, "survival": 0.82,
            "cancer_resistance": 90, "altitude_tolerance": 25,
            "uv_resistance": 70, "thermal_regulation": 50,
        },
        "dna_sequence": "TTCGGCTATCCGATCGGCTA",
        "emoji": "🐘",
    },
    "Dolphin": {
        "genes": ["MSTN","FOXP2","MC1R","IGF1","BRCA1",
                  "EPAS1","ACTN3","SLC24A5","DRD4","EDAR"],
        "base_traits": {
            "muscle_mass": 55, "strength": 50, "speed": 65,
            "aggression": 30, "intelligence": 90, "communication": 95,
            "endurance": 75, "size": 45, "camouflage": 30,
            "lifespan": 60, "fat_ratio": 35, "survival": 0.78,
            "cancer_resistance": 65, "altitude_tolerance": 10,
            "uv_resistance": 40, "thermal_regulation": 70,
        },
        "dna_sequence": "GACGGCTATGCAATCGGCTA",
        "emoji": "🐬",
    },
    "Eagle": {
        "genes": ["MSTN","FOXP2","MC1R","IGF1","BRCA1",
                  "EPAS1","ACTN3","SLC24A5","DRD4","EDAR"],
        "base_traits": {
            "muscle_mass": 40, "strength": 45, "speed": 85,
            "aggression": 70, "intelligence": 65, "communication": 50,
            "endurance": 70, "size": 30, "camouflage": 50,
            "lifespan": 60, "fat_ratio": 10, "survival": 0.75,
            "cancer_resistance": 60, "altitude_tolerance": 95,
            "uv_resistance": 75, "thermal_regulation": 60,
        },
        "dna_sequence": "ATCGGCTATGCGATCGGCTT",
        "emoji": "🦅",
    },
    "Gorilla": {
        "genes": ["MSTN","FOXP2","MC1R","IGF1","BRCA1",
                  "EPAS1","ACTN3","SLC24A5","DRD4","EDAR"],
        "base_traits": {
            "muscle_mass": 88, "strength": 90, "speed": 35,
            "aggression": 65, "intelligence": 82, "communication": 70,
            "endurance": 60, "size": 80, "camouflage": 35,
            "lifespan": 60, "fat_ratio": 20, "survival": 0.70,
            "cancer_resistance": 68, "altitude_tolerance": 40,
            "uv_resistance": 55, "thermal_regulation": 60,
        },
        "dna_sequence": "ATCGGCTATGCGATCGGCCA",
        "emoji": "🦍",
    },
    "Snow Leopard": {
        "genes": ["MSTN","FOXP2","MC1R","IGF1","BRCA1",
                  "EPAS1","ACTN3","SLC24A5","DRD4","EDAR"],
        "base_traits": {
            "muscle_mass": 65, "strength": 70, "speed": 72,
            "aggression": 70, "intelligence": 65, "communication": 40,
            "endurance": 70, "size": 55, "camouflage": 85,
            "lifespan": 50, "fat_ratio": 25, "survival": 0.65,
            "cancer_resistance": 58, "altitude_tolerance": 90,
            "uv_resistance": 60, "thermal_regulation": 90,
        },
        "dna_sequence": "ATCGGCTATGCGATCGGCTC",
        "emoji": "🐱",
    },
    "Shark": {
        "genes": ["MSTN","FOXP2","MC1R","IGF1","BRCA1",
                  "EPAS1","ACTN3","SLC24A5","DRD4","EDAR"],
        "base_traits": {
            "muscle_mass": 70, "strength": 75, "speed": 80,
            "aggression": 88, "intelligence": 50, "communication": 30,
            "endurance": 85, "size": 70, "camouflage": 60,
            "lifespan": 70, "fat_ratio": 20, "survival": 0.80,
            "cancer_resistance": 85, "altitude_tolerance": 5,
            "uv_resistance": 50, "thermal_regulation": 45,
        },
        "dna_sequence": "CCCGGCTATGCGATCGGCTA",
        "emoji": "🦈",
    },
}

TRAIT_LABELS = {
    "muscle_mass":        "Muscle Mass (%)",
    "strength":           "Strength (%)",
    "speed":              "Speed (%)",
    "aggression":         "Aggression (%)",
    "intelligence":       "Intelligence (%)",
    "communication":      "Communication (%)",
    "endurance":          "Endurance (%)",
    "size":               "Body Size (%)",
    "camouflage":         "Camouflage (%)",
    "lifespan":           "Lifespan (%)",
    "fat_ratio":          "Fat Ratio (%)",
    "cancer_resistance":  "Cancer Resistance (%)",
    "altitude_tolerance": "Altitude Tolerance (%)",
    "uv_resistance":      "UV Resistance (%)",
    "thermal_regulation": "Thermal Regulation (%)",
    "survival":           "Survival Probability",
}

# ─── Similarity ───────────────────────────────────────────────────────────────

def compute_similarity(animal_a: str, animal_b: str) -> float:
    """
    Mock genetic similarity using Hamming distance on DNA sequences.
    Returns percentage similarity (0–100).
    """
    seq_a = ANIMALS[animal_a]["dna_sequence"]
    seq_b = ANIMALS[animal_b]["dna_sequence"]
    matches = sum(a == b for a, b in zip(seq_a, seq_b))
    return round((matches / len(seq_a)) * 100, 1)


# ─── Simulation engine ────────────────────────────────────────────────────────

def apply_gene_edit(base_traits: dict, gene: str, action: str,
                    noise: float = 0.15) -> dict:
    """
    Apply a gene edit action (mutate/knockout/overexpress) to trait dict.
    Adds ±noise biological uncertainty.
    Returns updated trait dict.
    """
    traits  = copy.deepcopy(base_traits)
    impacts = GENE_DB[gene]["trait_impact"]
    sign    = {"mutate": 1.0, "knockout": -1.5, "overexpress": 1.8}[action]

    for trait, delta in impacts.items():
        if trait not in traits:
            continue
        # Add biological noise (random ±noise fraction)
        noisy_delta = delta * sign * (1 + random.uniform(-noise, noise))

        if trait == "survival":
            traits[trait] = round(
                max(0.0, min(1.0, traits[trait] + noisy_delta)), 3
            )
        else:
            traits[trait] = round(
                max(0, min(100, traits[trait] + noisy_delta)), 1
            )

    return traits


def mix_genes(animal_a: str, animal_b: str,
              selected_genes_b: list) -> dict:
    """
    Mix selected genes from animal_b INTO animal_a's base traits.
    Each gene from B applies its mutation effect at 60% strength
    (cross-species penalty).
    """
    base = copy.deepcopy(ANIMALS[animal_a]["base_traits"])
    for gene in selected_genes_b:
        impacts = GENE_DB[gene]["trait_impact"]
        for trait, delta in impacts.items():
            if trait not in base:
                continue
            cross_delta = delta * 0.6 * (1 + random.uniform(-0.1, 0.1))
            if trait == "survival":
                base[trait] = round(max(0.0, min(1.0, base[trait] + cross_delta)), 3)
            else:
                base[trait] = round(max(0, min(100, base[trait] + cross_delta)), 1)
    return base


def compute_scores(traits: dict) -> dict:
    """Derive composite scores from trait values."""
    physical  = np.mean([traits.get("muscle_mass", 50),
                         traits.get("strength", 50),
                         traits.get("speed", 50),
                         traits.get("size", 50)])
    behavioral = np.mean([traits.get("aggression", 50),
                          traits.get("intelligence", 50),
                          traits.get("communication", 50)])
    return {
        "Physical Score":  round(physical, 1),
        "Behavioral Score": round(behavioral, 1),
        "Survival Probability": traits.get("survival", 0.5),
    }


# ─── Plotting ─────────────────────────────────────────────────────────────────

def plot_trait_comparison(original: dict, modified: dict,
                          title: str = "Trait Comparison"):
    """Bar chart comparing original vs modified traits."""
    common = [k for k in original if k != "survival" and k in modified]
    x      = np.arange(len(common))
    width  = 0.35

    fig, ax = plt.subplots(figsize=(12, 5))
    bars1 = ax.bar(x - width/2,
                   [original[k] for k in common],
                   width, label="Original", color="#4A90D9", alpha=0.85)
    bars2 = ax.bar(x + width/2,
                   [modified[k] for k in common],
                   width, label="Modified", color="#E85D2F", alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(
        [TRAIT_LABELS.get(k, k).replace(" (%)", "") for k in common],
        rotation=45, ha="right", fontsize=9,
    )
    ax.set_ylabel("Score (0–100)")
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.legend()
    ax.set_ylim(0, 110)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    # Delta annotations
    for b1, b2, k in zip(bars1, bars2, common):
        delta = modified[k] - original[k]
        color = "green" if delta >= 0 else "red"
        ax.annotate(
            f"{delta:+.0f}",
            xy=(b2.get_x() + b2.get_width() / 2, b2.get_height()),
            xytext=(0, 3), textcoords="offset points",
            ha="center", fontsize=7, color=color,
        )

    fig.tight_layout()
    return fig


def plot_radar(traits: dict, label: str, color: str):
    """Radar / spider chart for a single animal's traits."""
    keys   = [k for k in traits if k != "survival"]
    values = [traits[k] for k in keys]
    N      = len(keys)

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    values_plot = values + values[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"polar": True})
    ax.plot(angles, values_plot, color=color, linewidth=2)
    ax.fill(angles, values_plot, color=color, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(
        [k.replace("_", "\n") for k in keys], fontsize=7
    )
    ax.set_ylim(0, 100)
    ax.set_title(label, size=12, fontweight="bold", pad=15)
    return fig


def plot_similarity_heatmap():
    """Heatmap of pairwise genetic similarity between all animals."""
    names = list(ANIMALS.keys())
    n     = len(names)
    matrix = np.zeros((n, n))

    for i, a in enumerate(names):
        for j, b in enumerate(names):
            matrix[i][j] = compute_similarity(a, b)

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(matrix, cmap="YlOrRd", vmin=60, vmax=100)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(names, fontsize=9)
    plt.colorbar(im, ax=ax, label="Similarity (%)")
    ax.set_title("Genetic Similarity Matrix", fontsize=13, fontweight="bold")

    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{matrix[i][j]:.0f}",
                    ha="center", va="center", fontsize=8,
                    color="black" if matrix[i][j] < 88 else "white")
    fig.tight_layout()
    return fig


# ─── UI: Gene Editing Tab ─────────────────────────────────────────────────────

def tab_gene_edit():
    st.subheader("Gene Editing Simulation")
    st.caption(
        "Select an animal, choose genes to edit, and apply mutations, "
        "knockouts, or overexpression. Results show predicted trait changes."
    )

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        animal = st.selectbox(
            "Select animal",
            list(ANIMALS.keys()),
            format_func=lambda a: f"{ANIMALS[a]['emoji']} {a}",
        )

        genes_to_edit = st.multiselect(
            "Select genes to edit",
            ANIMALS[animal]["genes"],
            default=["MSTN"],
        )

        action = st.radio(
            "Edit action",
            ["mutate", "knockout", "overexpress"],
            format_func=lambda x: x.capitalize(),
            horizontal=True,
        )

        noise_level = st.slider(
            "Biological uncertainty (noise)",
            min_value=0.0, max_value=0.5, value=0.15, step=0.05,
            help="Simulates biological variability. Higher = more random outcomes.",
        )

        run = st.button("Run Simulation", type="primary", use_container_width=True)

    with col2:
        # Gene info table
        st.markdown("**Selected gene details**")
        if genes_to_edit:
            gene_rows = []
            for g in genes_to_edit:
                gd = GENE_DB[g]
                gene_rows.append({
                    "Gene":      g,
                    "Function":  gd["function"],
                    "Location":  gd["expression_area"],
                    "Effect": gd.get("effects", {}).get(action, "No known effect"),
                })
            st.dataframe(pd.DataFrame(gene_rows), use_container_width=True,
                         hide_index=True)
        else:
            st.info("Select at least one gene.")

    if run and genes_to_edit:
        st.divider()
        st.markdown(f"### Results: {ANIMALS[animal]['emoji']} {animal} — {action.capitalize()}")

        base_traits     = ANIMALS[animal]["base_traits"]
        modified_traits = copy.deepcopy(base_traits)

        for gene in genes_to_edit:
            modified_traits = apply_gene_edit(
                modified_traits, gene, action, noise=noise_level
            )

        # Delta table
        deltas = []
        for trait, label in TRAIT_LABELS.items():
            orig = base_traits.get(trait, 0)
            mod  = modified_traits.get(trait, 0)
            delta = round(mod - orig, 3)
            deltas.append({
                "Trait":    label,
                "Original": orig,
                "Modified": mod,
                "Change":   f"{delta:+.3f}",
                "Signal":   "▲" if delta > 0 else ("▼" if delta < 0 else "—"),
            })

        delta_df = pd.DataFrame(deltas)
        changed  = delta_df[delta_df["Change"] != "+0.000"]
        st.dataframe(
            changed.style.apply(
                lambda row: [
                    "color: green" if row["Signal"] == "▲"
                    else "color: red" if row["Signal"] == "▼"
                    else ""
                ] * len(row),
                axis=1,
            ),
            use_container_width=True,
            hide_index=True,
        )

        # Composite scores
        scores = compute_scores(modified_traits)
        s1, s2, s3 = st.columns(3)
        s1.metric("Physical Score",       f"{scores['Physical Score']:.1f} / 100")
        s2.metric("Behavioral Score",     f"{scores['Behavioral Score']:.1f} / 100")
        s3.metric("Survival Probability", f"{scores['Survival Probability']:.3f}")

        # Charts
        ch1, ch2 = st.columns([2, 1])
        with ch1:
            st.pyplot(
                plot_trait_comparison(
                    base_traits, modified_traits,
                    title=f"{animal} — Trait Changes after {action.capitalize()}",
                ),
                use_container_width=True,
            )
        with ch2:
            st.pyplot(
                plot_radar(modified_traits, f"{animal} (Modified)", "#E85D2F"),
                use_container_width=True,
            )


# ─── UI: Cross-Species Tab ────────────────────────────────────────────────────

def tab_cross_species():
    st.subheader("Cross-Species Gene Mixing")
    st.caption(
        "Mix genes between two animals. Gene transfer is only allowed "
        "when genetic similarity ≥ 85%. Inspired by comparative genomics."
    )

    col1, col2 = st.columns(2)
    with col1:
        animal_a = st.selectbox(
            "Base animal (recipient)",
            list(ANIMALS.keys()),
            format_func=lambda a: f"{ANIMALS[a]['emoji']} {a}",
            key="cs_a",
        )
    with col2:
        animal_b = st.selectbox(
            "Donor animal",
            [a for a in ANIMALS if a != animal_a],
            format_func=lambda a: f"{ANIMALS[a]['emoji']} {a}",
            key="cs_b",
        )

    similarity = compute_similarity(animal_a, animal_b)
    threshold  = 85.0
    compatible = similarity >= threshold

    sim_col1, sim_col2 = st.columns(2)
    sim_col1.metric("Genetic Similarity", f"{similarity}%")
    sim_col2.metric(
        "Compatibility",
        "✅ Compatible" if compatible else "❌ Incompatible",
    )

    if not compatible:
        st.error(
            f"❌ Genetic similarity is {similarity}% — below the 85% threshold. "
            f"Gene transfer blocked. "
            f"Select a more closely related donor animal."
        )
        return

    st.success(f"✅ {similarity}% similarity — gene transfer permitted.")

    genes_to_transfer = st.multiselect(
        f"Select genes to transfer from {animal_b} → {animal_a}",
        ANIMALS[animal_b]["genes"],
        default=["MSTN", "ACTN3"],
    )

    if st.button("Run Cross-Species Mix", type="primary", use_container_width=True):
        if not genes_to_transfer:
            st.warning("Select at least one gene to transfer.")
            return

        st.divider()
        st.markdown(
            f"### Result: {ANIMALS[animal_a]['emoji']} {animal_a} + "
            f"{ANIMALS[animal_b]['emoji']} {animal_b} genes"
        )

        base_traits     = ANIMALS[animal_a]["base_traits"]
        hybrid_traits   = mix_genes(animal_a, animal_b, genes_to_transfer)

        # Side-by-side radar
        r1, r2 = st.columns(2)
        with r1:
            st.pyplot(
                plot_radar(base_traits, f"{animal_a} (Original)", "#4A90D9"),
                use_container_width=True,
            )
        with r2:
            st.pyplot(
                plot_radar(hybrid_traits, f"{animal_a} + {animal_b} genes (Hybrid)", "#E85D2F"),
                use_container_width=True,
            )

        st.pyplot(
            plot_trait_comparison(
                base_traits, hybrid_traits,
                title=f"Trait Changes: {animal_a} after receiving {animal_b} genes",
            ),
            use_container_width=True,
        )

        # Scores
        scores = compute_scores(hybrid_traits)
        s1, s2, s3 = st.columns(3)
        s1.metric("Physical Score",       f"{scores['Physical Score']:.1f} / 100")
        s2.metric("Behavioral Score",     f"{scores['Behavioral Score']:.1f} / 100")
        s3.metric("Survival Probability", f"{scores['Survival Probability']:.3f}")


# ─── UI: Gene Library Tab ─────────────────────────────────────────────────────

def tab_gene_library():
    st.subheader("Gene Reference Library")
    st.caption("Real gene names, simplified functions, and simulated effects.")

    search = st.text_input("Search genes", placeholder="e.g. muscle, brain, MSTN...")

    rows = []
    for gene, info in GENE_DB.items():
        rows.append({
            "Gene":               gene,
            "Function":           info["function"],
            "Expression Area":    info["expression_area"],
            "Mutation Effect":    info["mutation_effect"],
            "Knockout Effect":    info["knockout_effect"],
            "Overexpress Effect": info["overexpress_effect"],
        })

    df = pd.DataFrame(rows)
    if search.strip():
        mask = df.apply(
            lambda row: search.lower() in row.to_string().lower(), axis=1
        )
        df = df[mask]

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("**Gene trait impact map**")
    impact_rows = []
    for gene, info in GENE_DB.items():
        for trait, delta in info["trait_impact"].items():
            impact_rows.append({
                "Gene": gene,
                "Trait": TRAIT_LABELS.get(trait, trait),
                "Mutation Impact": f"{delta:+}",
            })

    impact_df = pd.DataFrame(impact_rows)
    st.dataframe(impact_df, use_container_width=True, hide_index=True)


# ─── UI: Similarity Tab ───────────────────────────────────────────────────────

def tab_similarity():
    st.subheader("Genetic Similarity Explorer")
    st.caption(
        "Pairwise genetic similarity between all 10 animals, "
        "computed via mock DNA sequence comparison."
    )

    st.pyplot(plot_similarity_heatmap(), use_container_width=True)

    st.divider()
    st.markdown("**Pairwise similarity table**")
    names = list(ANIMALS.keys())
    rows  = []
    for a in names:
        for b in names:
            if a < b:
                sim = compute_similarity(a, b)
                rows.append({
                    "Animal A": f"{ANIMALS[a]['emoji']} {a}",
                    "Animal B": f"{ANIMALS[b]['emoji']} {b}",
                    "Similarity (%)": sim,
                    "Compatible (≥85%)": "✅" if sim >= 85 else "❌",
                })

    sim_df = pd.DataFrame(rows).sort_values("Similarity (%)", ascending=False)
    st.dataframe(sim_df, use_container_width=True, hide_index=True)


# ─── UI: Animal Profiles Tab ──────────────────────────────────────────────────

def tab_profiles():
    st.subheader("Animal Profiles")

    animal = st.selectbox(
        "Select animal",
        list(ANIMALS.keys()),
        format_func=lambda a: f"{ANIMALS[a]['emoji']} {a}",
        key="profile_select",
    )

    info = ANIMALS[animal]

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"## {info['emoji']} {animal}")
        st.markdown(f"**DNA sequence (mock):** `{info['dna_sequence']}`")
        st.markdown("**Genes:**")
        for g in info["genes"]:
            st.markdown(
                f"- **{g}** — {GENE_DB[g]['expression_area']}: "
                f"{GENE_DB[g]['function'].split('—')[-1].strip()}"
            )

    with col2:
        st.markdown("**Base trait profile**")
        trait_df = pd.DataFrame([
            {"Trait": TRAIT_LABELS.get(k, k), "Value": v}
            for k, v in info["base_traits"].items()
        ])
        st.dataframe(trait_df, use_container_width=True, hide_index=True)

    st.divider()
    st.pyplot(
        plot_radar(info["base_traits"], f"{animal} — Base Profile", "#4A90D9"),
        use_container_width=True,
    )


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="Gene Simulation Engine",
        page_icon="🧬",
        layout="wide",
    )

    st.title("🧬 Gene Modification & Cross-Species Simulation")
    st.caption(
        "⚠️ Educational simulation only — not scientifically accurate. "
        "Inspired by real genetics but heavily simplified."
    )

    with st.sidebar:
        st.header("About")
        st.markdown(
            "**What this simulates:**\n"
            "- Gene mutations, knockouts, overexpression\n"
            "- Cross-species gene mixing (similarity-gated)\n"
            "- Trait prediction with uncertainty\n"
            "- Genetic similarity between 10 animals\n\n"
            "**Real genes used:**\n"
            "MSTN, FOXP2, MC1R, IGF1, BRCA1,\n"
            "EPAS1, ACTN3, SLC24A5, DRD4, EDAR\n\n"
            "**Animals:**\n"
        )
        for name, data in ANIMALS.items():
            st.markdown(f"- {data['emoji']} {name}")

        st.divider()
        st.caption(
            "Similarity threshold for gene mixing: **85%**\n\n"
            "Noise model: uniform random ±noise × delta"
        )

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Gene Editing",
        "Cross-Species Mix",
        "Animal Profiles",
        "Gene Library",
        "Similarity Map",
    ])

    with tab1:
        tab_gene_edit()
    with tab2:
        tab_cross_species()
    with tab3:
        tab_profiles()
    with tab4:
        tab_gene_library()
    with tab5:
        tab_similarity()


if __name__ == "__main__":
    main()