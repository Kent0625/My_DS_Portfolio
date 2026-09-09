# SmartTripCDO

**Generative AI Case Study: Grounded Travel Assistant for Cagayan de Oro**

[![Live App](https://img.shields.io/badge/Live_App-Streamlit_on_HF_Spaces-FFD21E?style=flat-square&logo=huggingface&logoColor=black)](https://kent0625-smartrip-cdo.hf.space)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=flat-square&logo=github)](https://github.com/Kent0625/smartrip_cdo)
[![Architecture](https://img.shields.io/badge/Architecture-Static_RAG-green?style=flat-square)](https://github.com/Kent0625/smartrip_cdo)

A deployed Streamlit travel assistant for Cagayan de Oro City that leverages a curated local attractions dataset, deterministic constraint filtering, and static Retrieval-Augmented Generation (RAG) prompting to synthesize grounded, hallucination-free itineraries.

---

## Key Metrics at a Glance

| Metric / Attribute | Value / Specification |
| :--- | :--- |
| **Curated POI Database** | 47 Cagayan de Oro historical, eco-tourism, and culinary destinations |
| **Hallucination Rate** | 0.0% in controlled benchmark test prompts |
| **Clustering Efficiency** | 76.32% geographic proximity alignment |
| **Stack** | Python, Streamlit, Pandas, Google Gemini Flash API, Hugging Face Spaces |
| **Source Code** | [Kent0625/smartrip_cdo](https://github.com/Kent0625/smartrip_cdo) |

---

## Interactive Live Application

You can test the deployed SmartTripCDO itinerary generator below:

<iframe
    src="https://kent0625-smartrip-cdo.hf.space/?embed=true"
    frameborder="0"
    width="100%"
    height="650"
    style="border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);"
></iframe>

*(If the Hugging Face Space is asleep, please allow a few moments for the container to wake up, or open it directly in [Hugging Face Spaces](https://kent0625-smartrip-cdo.hf.space).)*

---

## Project Overview

```{image} ../assets/projects/smartrip-cdo-poster.png
:alt: SmartTripCDO static RAG travel assistant research poster
:align: center
:width: 85%
```

### 1. Problem Statement
Commercial AI travel assistants frequently hallucinate non-existent local routes, closed establishments, or geographically unrealistic multi-stop itineraries in regional Philippine cities. Furthermore, small local tourism offices lack the infrastructure or funding to maintain vector databases, live mapping APIs, or GPU-heavy LLM inference clusters. SmartTripCDO provides a lightweight, deterministic, and grounded alternative.

### 2. Curated Local Knowledge Base
- **Coverage:** 47 verified Cagayan de Oro points of interest (POIs) across heritage, eco-adventure, gastronomic, and urban leisure categories.
- **Attributes:** Opening hours, estimated admission costs, travel duration, geographic zones, and group suitability tags.

### 3. Static RAG Architecture
- **Stage 1 (User Parameter Extraction):** Collects duration (hours/days), budget constraints, group dynamics (solo, family, barkada), and primary interests.
- **Stage 2 (Deterministic Filtering):** Pandas-driven filtering isolates eligible candidate venues strictly meeting time, geographic proximity, and budget criteria.
- **Stage 3 (Grounded Itinerary Synthesis):** Passes candidate subsets into structured prompt templates powered by Google's Gemini Flash model, strictly constraining the LLM to verified venues.

### 4. Evaluation & Results
- **Zero Hallucinations:** In rigorous test trials, the system achieved 0% out-of-context venue generation by design.
- **High Geographic Clustering:** 76.32% clustering efficiency, ensuring tourist itineraries minimize unnecessary commuting across city zones.

### 5. Tools & Technologies
- **Framework & Libraries:** Python, Streamlit, Pandas, Gemini API
- **Hosting:** Hugging Face Spaces
- **Repository:** [Kent0625/smartrip_cdo](https://github.com/Kent0625/smartrip_cdo)
