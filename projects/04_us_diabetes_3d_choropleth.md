# U.S. Diabetes 3D Choropleth & Spatial Analytics

**Spatial Data Science Case Study: 3D Rayshader Cartography & Interactive County-Level Risk Modeling**

[![Live 3D Map](https://img.shields.io/badge/Live_App-Interactive_3D_WebGL-ef3b2c?style=flat-square&logo=google-earth&logoColor=white)](https://kent0625.github.io/Data_Viz_Project/)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=flat-square&logo=github)](https://github.com/Kent0625/Data_Viz_Project)
[![Language](https://img.shields.io/badge/Language-R-276DC3?style=flat-square&logo=r)](https://www.r-project.org/)
[![Engine](https://img.shields.io/badge/3D_Engine-rayshader-orange?style=flat-square)](https://www.rayshader.com/)
[![Client](https://img.shields.io/badge/Web_Client-Three.js_WebGL-black?style=flat-square&logo=threedotjs)](https://threejs.org/)

An interactive 3D spatial data visualization and rayshader mapping of adult diabetes prevalence across all 3,108 contiguous United States counties using CDC PLACES epidemiological data and U.S. Census Bureau cartographic boundaries.

---

## Key Metrics at a Glance

| Metric / Attribute | Value / Specification |
| :--- | :--- |
| **Geographic Coverage** | 3,108 Contiguous U.S. Counties (excluding AK, HI, & territories) |
| **Data Sources** | CDC Diabetes Atlas 2021 & U.S. Census Bureau TIGER/Line County Boundaries |
| **National County Median** | 8.3% adult diabetes prevalence |
| **Peak Prevalence Rate** | 17.9% (Todd County; concentrated Southern clusters) |
| **Count-to-Rate Correlation** | $r = 0.12$ (revealing distinct rural prevalence clusters obscured by raw totals) |
| **Spatial Projection** | NAD83 / Conus Albers (`EPSG:5070`) with topology-preserving polygon simplification |
| **Interactive Client** | Three.js WebGL real-time extrusion mesh, dynamic raycasting, lighting presets & camera controls |
| **Deployment** | GitHub Pages ([Live Demo](https://kent0625.github.io/Data_Viz_Project/)) |
| **Source Code** | [Kent0625/Data_Viz_Project](https://github.com/Kent0625/Data_Viz_Project) |

---

## Interactive Live Application

Experience the real-time 3D county-level visualization directly in your browser below:

<iframe
    src="https://kent0625.github.io/Data_Viz_Project/"
    frameborder="0"
    width="100%"
    height="650"
    style="border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid rgba(226, 232, 240, 0.8);"
></iframe>

*(If viewing on mobile, rotate to landscape mode or open full-screen directly in [GitHub Pages](https://kent0625.github.io/Data_Viz_Project/).)*

---

## Project Overview

```{image} ../assets/projects/us-diabetes-3d-map.png
:alt: 3D Rayshader photorealistic county-level diabetes prevalence map
:align: center
:width: 85%
```

### 1. Problem Statement & Spatial Motivation
Standard 2D thematic maps (choropleths) often distort epidemiological reality. In traditional 2D visualizations, large geographic counties dominate viewer perception regardless of population density, while high-risk urban or rural micro-clusters with smaller land area disappear. Furthermore, raw case count maps simply highlight population centers, obscuring areas where disproportionate percentages of the population suffer from chronic health conditions.

This project solves these visualization hurdles by implementing a **dual-encoding 3D choropleth landscape**:
1. **Vertical Elevation ($\Delta z$):** Extrudes county geometry proportional to adult diabetes prevalence rates.
2. **Color Chroma & Value:** Mapped continuously across a clinical health-alert palette (`#FFF5F0` light blush to `#5A0009` deep blood crimson).

This dual encoding transforms the United States map into an intuitive topographic landscape where regional clusters of high disease burden visually erupt above the national baseline.

---

### 2. Dataset, Spatial Boundaries & Data Pipeline
The analysis merges federal health records with high-resolution cartographic boundary definitions:

- **Epidemiological Records:** CDC Diabetes Atlas / PLACES county-level data containing diagnosed adult diabetes prevalence (percentage) and total diagnosed cases.
- **Geographic Boundaries:** U.S. Census Bureau TIGER/Line county shapefiles converted to an optimized GeoPackage (`.gpkg`).
- **Standardized Spatial Joins:** 5-digit Federal Information Processing Standard (FIPS / GEOID) keys joined across tables, filtering non-contiguous states and territories (`02` Alaska, `15` Hawaii, `72` Puerto Rico, etc.).
- **Map Projection:** Reprojected from unprojected WGS84 geographic coordinates to **NAD83 / Conus Albers (`EPSG:5070`)**, preserving accurate area and shape proportions across the continental United States.
- **Topology-Preserving Simplification:** Douglas-Peucker simplification (`dTolerance = 11,000m`) applied via `sf::st_simplify` to compress complex boundary coastlines into lightweight vector coordinates suitable for low-latency WebGL rendering.

```{image} ../assets/projects/us-diabetes-2d-map.png
:alt: 2D Baseline county-level diabetes prevalence choropleth
:align: center
:width: 85%
```

---

### 3. Cartographic & 3D Rayshader Pipeline
The publication-quality raytraced visualization was engineered in **R** using `rayshader`, `ggplot2`, and `stars`:

- **Raster Surface Generation:** County prevalence polygons were rasterized into a high-resolution matrix elevation grid representing normalized diabetes rates.
- **Raymarched Shadows & Illumination:** Using `rayshader::render_highquality()`, physical ray tracing simulated realistic sunlight angles, ambient occlusion, and soft shadow falloff across county boundaries.
- **Sequential Clinical Palette:** Designed with a high-contrast sequential scale starting from low prevalence (cream `#FFF5F0`) transitioning through moderate risk (terracotta `#EF3B2C`) to critical risk (deep burgundy `#5A0009`).

---

### 4. Interactive WebGL Client & Real-Time Engine
To provide an interactive experience without requiring users to install R or wait for raytracing compute runs, an interactive web client was developed with **HTML5, CSS3, and Three.js**:

- **Pre-Projected Vector Engine:** Lightweight JSON data coordinates (`data/us_counties_preprojected.json`) are centered and scaled directly into Three.js 3D world space.
- **Real-Time Extrusion:** County polygons are dynamically triangulated with `THREE.ExtrudeGeometry`, mapping prevalence percentage to mesh height in real time.
- **Camera & POV Presets:** Orbit controls enable free 360° pan, tilt, and zoom, complemented by presets (*Rayshader 3D*, *Top-Down 2D*, *Cinematic Horizon*, and *South Clusters*).
- **Sun Lighting & Shadow Controls:** Sliders control live sun azimuth (0°–360°), elevation angle (15°–85°), and soft directional shadow intensity.
- **Interactive Raycasting:** Mouse hover tooltips highlight individual counties, displaying exact prevalence percentages, state names, and risk classifications.
- **Snapshot Exporter:** Built-in canvas export allows users to download customized high-resolution camera angles instantly.

---

### 5. Key Epidemiological Findings & Spatial Insights

1. **National Distribution:** Median county prevalence sits at **8.3%**, but the national distribution exhibits severe regional inequality.
2. **The "Diabetes Belt" Clustering:** The highest prevalence rates cluster heavily in the rural South, peaking at **17.9% in Todd County**, followed by Williamsburg County (17.5%), Portsmouth City (16.8%), Gadsden County (15.9%), and Holmes County (15.5%).
3. **Weak Correlation Between Volume & Rate ($r = 0.12$):** High raw case counts are concentrated in populous urban centers (e.g., Los Angeles, Cook, Harris counties), whereas high percentage rates are concentrated in rural counties with limited healthcare access. A flat 2D count map obscures these critical vulnerable communities.

---

### 6. Tools & Technologies

- **Data Processing & Cartography:** R (`sf`, `stars`, `raster`, `dplyr`, `readr`, `stringr`, `ggplot2`)
- **3D Raytracing Engine:** `rayshader`
- **Interactive Web App:** JavaScript (ES6+), Three.js (WebGL), HTML5, CSS3
- **Data Formats:** GeoPackage (`.gpkg`), GeoJSON / Simplified JSON, CSV
- **Deployment & Hosting:** GitHub Pages
- **Repository:** [Kent0625/Data_Viz_Project](https://github.com/Kent0625/Data_Viz_Project)
