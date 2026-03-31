import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

import json

with open("pipeline_state.json") as f:
    state = json.load(f)

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Statistical Arbitrage | Quant Research",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS (Institutional & Readable in ANY Mode)
# ==========================================
st.markdown("""
    <style>
    /* Main container width and font stack */
    .main { max-width: 1100px; margin: 0 auto; font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    
    /* Typography Upgrades using dynamic theme variables */
    h1 { text-align: center; font-size: 2.8rem !important; font-weight: 800 !important; margin-bottom: 0.5rem !important; line-height: 1.25 !important; color: var(--text-color) !important; letter-spacing: -0.02em !important; }
    .subtitle { text-align: center; font-size: 1.25rem !important; color: var(--text-color) !important; opacity: 0.75 !important; font-style: italic !important; margin-bottom: 2.5rem !important; font-weight: 400 !important; }
    
    h2 { font-weight: 700 !important; font-size: 2.0rem !important; margin-top: 3.5rem !important; border-bottom: 1px solid var(--secondary-background-color) !important; padding-bottom: 0.5rem !important; margin-bottom: 1.5rem !important; color: var(--text-color) !important; letter-spacing: -0.01em !important; }
    h3 { font-weight: 600 !important; font-size: 1.4rem !important; margin-top: 2rem !important; margin-bottom: 1rem !important; color: var(--text-color) !important; opacity: 0.9 !important; }
    
    /* Body text */
    /* Body text */
    div[data-testid="stMarkdownContainer"] p, 
    div[data-testid="stMarkdownContainer"] li { 
        font-size: 1.15rem !important; 
        line-height: 1.7 !important; 
        font-weight: 400 !important; 
        color: var(--text-color) !important; 
        opacity: 0.85 !important;
    } 
    div[data-testid="stMarkdownContainer"] li {
        margin-bottom: 0.5rem !important; /* Adds breathing room to bullet points */
    }
    div[data-testid="stMarkdownContainer"] strong { font-weight: 600 !important; color: var(--text-color) !important; opacity: 1.0 !important; }
    
    /* NEW: Visual Phase Badges for Headers */
    .section-badge {
        background-color: #3B82F6;
        color: #FFFFFF !important;
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 1.1rem;
        vertical-align: middle;
        margin-right: 14px;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        display: inline-block;
        transform: translateY(-3px);
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
    }

    /* NEW: Hero Box for Key Contributions */
    .hero-box {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 8px;
        padding: 25px 30px;
        margin: 1.5rem 0 2.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .hero-box-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #3B82F6;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* NEW: Math Framing */
    .math-box {
        text-align: center;
        font-size: 0.95rem;
        color: var(--text-color);
        opacity: 0.6;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: -10px;
        margin-top: 1.5rem;
        font-weight: 700;
    }
    
    /* NEW: Final Findings Box */
    .findings-box {
        border-left: 4px solid #10B981 !important; 
        padding: 1.5rem !important; 
        margin: 2rem 0 !important; 
        background-color: var(--secondary-background-color) !important;
        border-radius: 0 8px 8px 0 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .findings-title {
        font-size: 1.3rem;
        font-weight: 800;
        margin-bottom: 12px;
        color: #10B981;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Pipeline Process Blocks */
    .pipeline-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0;
        gap: 10px;
    }
    .pipeline-block {
        background-color: var(--secondary-background-color);
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        flex: 1;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    .pipeline-block-title {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 5px;
        color: #3B82F6;
    }
    .pipeline-block-desc {
        font-size: 0.95rem;
        opacity: 0.8;
    }
    .pipeline-arrow {
        font-size: 1.5rem;
        opacity: 0.3;
    }

    /* Callout Boxes for Technical Explanations */
    .mechanism-box { 
        border-left: 4px solid #3B82F6 !important; 
        padding: 1.25rem !important; 
        margin: 1.5rem 0 !important; 
        color: var(--text-color) !important; 
        font-size: 1.15rem !important; 
        background-color: var(--secondary-background-color) !important;
        border-radius: 0 8px 8px 0 !important;
    }
    
    .audit-box { 
        border-left: 4px solid #6B7280 !important; 
        padding: 1.25rem !important; 
        margin: 1.5rem 0 !important; 
        color: var(--text-color) !important; 
        font-size: 1.15rem !important;
        background-color: var(--secondary-background-color) !important;
        border-radius: 0 8px 8px 0 !important;
    }
    
    /* KPI Framing */
    .stat-box {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        border-radius: 8px !important;
        padding: 20px 15px !important;
        text-align: center !important;
        margin-bottom: 20px !important;
    }
    .stat-value { font-size: 2.2rem !important; font-weight: 700 !important; color: var(--text-color) !important; margin-bottom: 4px !important; line-height: 1 !important;}
    .stat-label { font-size: 0.9rem !important; font-weight: 600 !important; color: var(--text-color) !important; opacity: 0.7 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important;}
    
    /* Table of Contents Links */
    .toc-link { text-decoration: none !important; font-size: 1rem !important; display: block !important; padding: 6px 0 !important; font-weight: 500 !important; color: var(--text-color) !important; opacity: 0.8 !important; transition: all 0.2s ease-in-out !important; }
    .toc-link:hover { color: #3B82F6 !important; opacity: 1.0 !important; text-decoration: none !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# DATA RECONSTRUCTION (From Results output)
# ==========================================

@st.cache_data
def load_fracture_sweep():
    return pd.DataFrame({
        'Fracture Distance (Sigmas)': [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5],
        'Accepted Trades': [21, 21, 21, 21, 24, 27, 36, 36],
        'Blocked Trades': [18, 18, 18, 18, 15, 12, 3, 3],
        'Accepted EV': [0.0217, 0.0217, 0.0217, 0.0217, 0.0201, 0.0175, 0.0152, 0.0152],
        'Blocked EV': [0.0018, 0.0018, 0.0018, 0.0018, 0.0005, 0.0015, -0.0196, -0.0196]
    })


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.title("Research Outline")
    st.markdown("""
    <a href="#0-problem-setup" class="toc-link">0. Problem Setup & Approach</a>
    <a href="#1-dimensionality-stationarity" class="toc-link">1. Dimensionality & Stationarity</a>
    <a href="#2-extremal-dependence" class="toc-link">2. Extremal Dependence (Copulas)</a>
    <a href="#3-execution-friction" class="toc-link">3. Execution Friction & Bounds</a>
    <a href="#4-regime-risk" class="toc-link">4. Regime Risk Management</a>
    <a href="#5-production-roster" class="toc-link">5. Final Tradeable Pairs</a>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.info(
        "**Author:** Jayesh Chaudhary\n\n"
        "**Role:** Quantitative Researcher\n\n"
    )

# ==========================================
# MAIN DOCUMENT: TITLE & HERO
# ==========================================
st.markdown("<h1>Advanced Statistical Arbitrage: Copulas & Stochastic Control</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>A multi-stage statistical arbitrage pipeline combining clustering, copulas, and stochastic control for robust pair selection and execution.</p>", unsafe_allow_html=True)


st.markdown("""
<div class="hero-box">
    <div class="hero-box-title">Key Contributions</div>
    <ul>
        <li>Reduced the candidate universe using PCA + OPTICS clustering</li>
        <li>Filtered pairs using cointegration tests and Hurst exponent constraints</li>
        <li>Modeled dependence using multiple copula families with AIC-based selection</li>
        <li>Derived execution thresholds using an OU-based stochastic control framework</li>
        <li>Evaluated regime filtering empirically and retained it based on out-of-sample performance</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SECTION 0: INTUITION
# ==========================================
st.markdown("<h2 id='0-problem-setup'><span class='section-badge'>Phase 0</span> Problem Setup & Approach</h2>", unsafe_allow_html=True)


st.markdown("""
Traditional distance-based pairs trading strategies have shown declining robustness, particularly after accounting for transaction costs and unstable spread dynamics.

This work develops a pipeline to improve pair selection, dependence modeling, and execution by combining unsupervised learning, copula-based methods, and stochastic control.

### Limitation of Distance-Based Methods

Traditional approaches select pairs based on similarity in price paths. However, this often leads to spreads with weak and unstable mean-reversion properties, reducing their ability to generate consistent trading opportunities after costs.

### Research Workflow Architecture

**Dataset:** Daily adjusted close prices for S&P 500 constituents from January 2015 to January 2021. All modeling, filtering, and validation steps are conducted on this sample.


The workflow below shows how raw data is reduced into a final set of tradable pairs.
""")

# NEW: Modular Pipeline Blocks
st.markdown("""
<div class="pipeline-container">
    <div class="pipeline-block">
        <div class="pipeline-block-title">Step 1</div>
        <div class="pipeline-block-desc"><b>Ingestion</b><br>S&P 500 Universe</div>
    </div>
    <div class="pipeline-arrow">➔</div>
    <div class="pipeline-block">
        <div class="pipeline-block-title">Step 2</div>
        <div class="pipeline-block-desc"><b>Dimensionality</b><br>PCA + OPTICS</div>
    </div>
    <div class="pipeline-arrow">➔</div>
    <div class="pipeline-block">
        <div class="pipeline-block-title">Step 3</div>
        <div class="pipeline-block-desc"><b>Validation</b><br>Cointegration + Mean-Reversion</div>
    </div>
    <div class="pipeline-arrow">➔</div>
    <div class="pipeline-block">
        <div class="pipeline-block-title">Step 4</div>
        <div class="pipeline-block-desc"><b>Modeling</b><br>AIC Copulas</div>
    </div>
    <div class="pipeline-arrow">➔</div>
    <div class="pipeline-block">
        <div class="pipeline-block-title">Step 5</div>
        <div class="pipeline-block-desc"><b>Risk Control</b><br>OU + HMM</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### How the Universe Gets Filtered
Below is the exact reduction in the dataset at each step, based on the research logs.
""")


# Refined Funnel Chart
stages = ['Cleaned Universe', 'PCA Latent Factors', 'OPTICS Density Clusters', 'Cointegration & Mean-Reversion', 'OU Execution filtering', 'Final Pairs']
values = [459, 14, 38, 23, 20, 13]

st.markdown("""
<style>
/* Custom CSS for the Filtering Pipeline */
.filter-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    margin: 2rem 0;
}
.filter-step {
    background-color: var(--secondary-background-color);
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-left: 5px solid #3B82F6;
    padding: 15px 30px;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    max-width: 650px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    transition: transform 0.2s ease;
}
.filter-step:hover { transform: translateX(5px); }
.filter-label { font-size: 1.15rem; font-weight: 600; color: var(--text-color); }
.filter-desc { font-size: 0.9rem; color: var(--text-color); opacity: 0.7; margin-top: 4px; }
.filter-metric { font-size: 1.6rem; font-weight: 800; color: #3B82F6; text-align: right; line-height: 1; }
.filter-unit { font-size: 0.85rem; font-weight: 600; color: var(--text-color); opacity: 0.6; text-transform: uppercase; letter-spacing: 0.05em; }
.filter-arrow { color: var(--text-color); opacity: 0.3; font-size: 1.5rem; font-weight: bold; text-align: center; width: 100%; }
.filter-final { border-left: 5px solid #10B981; }
.filter-final .filter-metric { color: #10B981; }
</style>

<div class="filter-container">
<div class="filter-step">
<div><div class="filter-label">Cleaned Universe</div><div class="filter-desc">S&P 500 Equities</div></div>
<div><div class="filter-metric">459</div><div class="filter-unit">Assets</div></div>
</div>
<div class="filter-arrow">↓</div>
<div class="filter-step">
<div><div class="filter-label">Dimensionality Reduction</div><div class="filter-desc">PCA Latent Factors Retained</div></div>
<div><div class="filter-metric">14</div><div class="filter-unit">Factors</div></div>
</div>
<div class="filter-arrow">↓</div>
<div class="filter-step">
<div><div class="filter-label">Unsupervised Clustering</div><div class="filter-desc">OPTICS Density Cohorts</div></div>
<div><div class="filter-metric">38</div><div class="filter-unit">Clusters</div></div>
</div>
<div class="filter-arrow">↓</div>
<div class="filter-step">
<div><div class="filter-label">Cointegration & Mean-Reversion Filtering</div><div class="filter-desc">Engle-Granger & Hurst Validated</div></div>
<div><div class="filter-metric">23</div><div class="filter-unit">Pairs</div></div>
</div>
<div class="filter-arrow">↓</div>
<div class="filter-step">
<div><div class="filter-label">Stochastic Execution Filter</div><div class="filter-desc">OU Optimization (After 15bps Cost)</div></div>
<div><div class="filter-metric">20</div><div class="filter-unit">Pairs</div></div>
</div>
<div class="filter-arrow">↓</div>
<div class="filter-step filter-final">
<div><div class="filter-label">Final Tradable Pairs</div><div class="filter-desc">After Regime Filtering</div></div>
<div><div class="filter-metric">13</div><div class="filter-unit">Pairs</div></div>
</div>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="audit-box">
<strong>Interpretation:</strong> The pipeline reduced the search space from an unmanageable index of 459 assets to a highly refined, statistically valid execution roster of 13 pairs.
</div>
""", unsafe_allow_html=True)
st.divider()

# ==========================================
# SECTION 1: DIMENSIONALITY & STATIONARITY
# ==========================================
st.markdown("<h2 id='1-dimensionality-stationarity'><span class='section-badge'>Phase 1</span> Dimensionality & Stationarity</h2>", unsafe_allow_html=True)


st.markdown("""
Evaluating a large equity universe yields over 100,000 possible pairwise combinations. Exhaustive testing at this scale leads to a high rate of false discoveries.

To manage this, the pipeline utilizes unsupervised learning *prior* to any hypothesis testing. 
""")

col_pca_text, col_pca_plot = st.columns([1.2, 1])

with col_pca_text:
    st.markdown("""
    **The Mechanism:**
    1. The model extracts latent factors capturing >60% of the return variance via Principal Component Analysis (PCA). 
    2. It maps these factors into a multidimensional space and applies the density-based OPTICS algorithm to locate highly dense economic cohorts.
    3. Only pairs within the same cluster are considered for further statistical testing.
    
    This reduces the 459-dimensional space to 14 principal components, which are then grouped into **38 asset clusters** (e.g., Cluster 28 structurally isolating Energy components like `COP`, `EOG`, `HAL`, and `SLB`).
    """)
    
    st.markdown("""
    <div class="mechanism-box">
    <strong>Statistical Control</strong><br>
    Restricting hypothesis testing to pairs within the same OPTICS cluster reduces the effective search space, lowering the likelihood of spurious relationships without relying on overly conservative corrections.
    </div>
    """, unsafe_allow_html=True)

with col_pca_plot:
    # 3D PCA Visual
    pca_df = pd.read_csv("pca_embeddings.csv")
    fig_pca = px.scatter_3d(
        pca_df,
        x='PC1',
        y='PC2',
        z='PC3',
        color='Cluster',
        hover_name='Ticker',
        hover_data={
            'PC1': ':.2f',
            'PC2': ':.2f',
            'PC3': ':.2f'
        },
        opacity=0.75
    )

    fig_pca.update_traces(marker=dict(size=4))

    fig_pca.update_layout(
        title="PCA Factor Space: Asset Clustering",
        legend_title="Cluster",
        margin=dict(l=0, r=0, b=0, t=40),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    fig_pca.update_scenes(
        xaxis_title="PC1",
        yaxis_title="PC2",
        zaxis_title="PC3"
    )
    st.plotly_chart(fig_pca, use_container_width=True)
    st.markdown("""
    <div class="audit-box">
    <strong>Interpretation:</strong> <br>
    Each point represents an individual stock embedded in a low-dimensional factor space. Assets that cluster closely share similar return dynamics, allowing the model to restrict pair selection within economically coherent groups.
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
### Cointegration & Mean-Reversion Filtering

Pairs within each cluster are then tested for cointegration and mean-reversion strength.

Asset prices are inherently non-stationary **I(1) Series**. Cointegration ensures that a linear combination of two I(1) series ($X_t + \\beta Y_t$) results in an **I(0) Series**. An I(0) series exhibits weak-sense stationarity, defined by a finite and time-invariant mean and variance. 

A pair is retained only if it passes Engle-Granger cointegration tests ($p < 0.05$), ensuring a stationary spread, and exhibits sufficient mean-reversion (Hurst Exponent $< 0.45$).
""")

with st.expander("View Cointegration & Mean-Reversion Filtering Survivors (Phase 1 Output)"):
    arod_df = pd.DataFrame(state["validated_pairs"])
    arod_df = arod_df.rename(columns={
    "asset_x": "Asset X",
    "asset_y": "Asset Y",
    "cluster_id": "Cluster_ID",
    "hurst_exponent": "Hurst Exp.",
    "coint_p_value": "Cointegration p-value"
    })
    st.dataframe(arod_df, use_container_width=True, height=300, hide_index=True)
    
st.divider()

# ==========================================
# SECTION 2: COPULAS
# ==========================================
st.markdown("<h2 id='2-extremal-dependence'><span class='section-badge'>Phase 2</span> Extremal Dependence (Copulas)</h2>", unsafe_allow_html=True)


st.markdown("""
<div class="mechanism-box">
<strong>The Limits of Linear Correlation:</strong><br>
Pearson correlation only captures linear relationships. In practice, asset returns often exhibit asymmetric or tail dependence, which requires a more flexible modeling framework. Copulas address this limitation by separating marginal distributions from the dependence structure.
</div>
""", unsafe_allow_html=True)

st.markdown("""
### Dynamic Selection & The Mispricing Index (MPI)

To reduce computational cost, candidate pairs are first screened using a Pearson distance metric before fitting copula models.

For the survivors, returns are transformed into uniform marginals on the interval [0,1] via an empirical CDF before fitting multiple Copula families (Gaussian, Clayton for downside tail risk, Frank, and Gumbel for upside tail risk). The optimal structure for each pair is selected dynamically based on the Akaike Information Criterion (AIC). The Pearson distance is used purely as a computational pre-filter and does not determine the dependence structure.

**Signal Generation Mechanism:** Execution signals bypass standard deviation bands entirely. They are generated via a **Mispricing Index (MPI)**, calculating the conditional probability $P(U \le u | V=v)$. When this probability breaches extreme thresholds (e.g., drops below 0.05 or exceeds 0.95), the target asset is mathematically deemed under/overvalued relative to its partner's current state.


""")


copula_df = pd.DataFrame(state["copula_universe"])
copula_df = copula_df.rename(columns={
    "asset_x": "Asset X",
    "asset_y": "Asset Y",
    "cluster_id": "Cluster",
    "hedge_ratio": "Hedge Ratio",
    "hurst_exponent": "Hurst",
    "coint_p_value": "Cointegration p-value",
    "pearson_distance": "Pearson Distance",
    "optimal_copula": "Copula",
    "copula_theta": "Theta",
    "total_historical_trades": "Trades"
})
copula_df = copula_df.drop(columns=[
    "passes_dependence"
])

# Display authentic Copula scatter and signals generated from the research notebook
col_cop_text, col_cop_plot = st.columns([1.2, 1])

with col_cop_text:
    st.markdown("""
    ### Dynamic Selection & Cumulative Mispricing Index (CMPI)
    
    To reduce computational cost before expending resources on Maximum Likelihood Estimation (MLE), candidates are first screened using the **Pearson Distance Approach**. This calculates the sum of squared deviations (SSD) between normalized cumulative return indices; a lower distance mathematically validates tight historical co-movement.
    
    For the survivors, raw returns are mapped to strictly uniform marginals on the interval $[0, 1]$ via an Empirical Cumulative Distribution Function (ECDF). The model then fits these marginals to multiple Copula families (Gaussian, Clayton for lower-tail, Frank, and Gumbel). The optimal structure for each pair is selected dynamically based on the Akaike Information Criterion (AIC).
    
    **Signal Generation Mechanism:** Execution signals bypass standard deviation bands entirely. First, we calculate the raw **Mispricing Index (MPI)**—the conditional probability $P(U \le u \mid V=v)$. 
    
    Instead of trading raw MPI, the pipeline utilizes the **Cumulative Mispricing Index (CMPI)** following the Rad et al. (2016) doctrinal trigger. This captures cumulative mispricing over time rather than one-step probability shocks. Trades are triggered when CMPI breaches a `0.6` entry threshold, exit upon reversion to `0.0`, and feature a hard stop-loss limit of `2.0` to protect against structural breaks. Finally, pairs must pass an institutional dependence hurdle (e.g., Gaussian $\theta > 0.40$, Frank $\theta > 2.0$) to clear the filter.
    """)
    st.markdown("These thresholds are fixed instead of optimized to avoid overfitting and keep the results stable out-of-sample.")

with col_cop_plot:
    st.image("copula_scatter.png", caption="Copula Dependence Structure", use_container_width=True)
    st.markdown("<p style='font-size:0.85rem; opacity:0.7; text-align:center;'><em>Axes represent historical return percentiles (0.0 to 1.0). This isolates structural dependence by removing individual asset volatility.</em></p>", unsafe_allow_html=True)

st.markdown("""
<div class="audit-box">
<strong>Data Engineering Control: Term Structure Blindness</strong><br>
Fitting copulas directly to raw asset prices fails. Because equity prices generally drift upward over time, the empirical quantiles permanently skew towards 1.0, breaking the bounds of the copula. To preserve structural integrity, all marginal transformations via Empirical CDFs are executed strictly on daily returns.
</div>
""", unsafe_allow_html=True)

# Center the wide rectangular plot so it doesn't overwhelm the screen
col_pad1, col_sig, col_pad2 = st.columns([1, 4, 1])
with col_sig:
    st.image("copula_signals.png", caption="Trading Signals from Copula CMPI", use_container_width=True)

copula_df = pd.DataFrame(state["copula_universe"])
copula_df = copula_df.rename(columns={
    "asset_x": "Asset X",
    "asset_y": "Asset Y",
    "cluster_id": "Cluster",
    "hedge_ratio": "Hedge Ratio",
    "hurst_exponent": "Hurst",
    "coint_p_value": "Cointegration p-value",
    "pearson_distance": "Pearson Distance",
    "optimal_copula": "Copula",
    "copula_theta": "Theta",
    "total_historical_trades": "Trades"
})

if "passes_dependence" in copula_df.columns:
    copula_df = copula_df.drop(columns=["passes_dependence"])

with st.expander("View Copula Dependency Table (Phase 2 Output)"):
    st.dataframe(copula_df, use_container_width=True, hide_index=True)
    
st.divider()

# ==========================================
# SECTION 3: STOCHASTIC CONTROL
# ==========================================
st.markdown("<h2 id='3-execution-friction'><span class='section-badge'>Phase 3</span> Stochastic Execution Bounds</h2>", unsafe_allow_html=True)


st.markdown("""
Using fixed $\pm 2\sigma$ entry rules ignores an important factor: how long the spread takes to revert.

Holding a position requires capital and carries **Horizon Risk** (the uncertainty of exactly when the mispricing will correct) and **Divergence Risk** (the mathematical probability the spread widens further prior to converging). 

**The Mechanism:** The architecture explicitly models this spread as a continuous Ornstein-Uhlenbeck (OU) process:
""")

st.markdown("""
Optimal entry and exit thresholds are derived by maximizing expected profit relative to expected holding time under transaction costs.
""")

st.markdown("""
<div class="math-box">
<strong>Equation 1: Continuous Ornstein-Uhlenbeck (OU) Process</strong>
</div>
""", unsafe_allow_html=True)
st.latex(r"dX_t = \theta (\mu - X_t)dt + \sigma dW_t")

st.markdown("""
Instead of fixed entry bands, the model derives optimal thresholds from the underlying stochastic process. This transformation allows the optimizer to internalize a strict **15 basis point transaction cost**. 

If the model determines that the expected profit margin cannot clear the execution friction faster than the expected holding time, the trade is rejected.
""")

st.markdown("""
<div class="audit-box">
<strong>Empirical OU Fit (AEE vs CMS):</strong><br>
• Spread Half-Life (Horizon Risk): 6.18 Trading Days<br>
• Mean Reversion Speed (θ): 28.2635<br>
• Spread Volatility (σ): 0.2245<br>
• Dimensionless Entry: ±0.15 σ (incorporating 15 bps execution cost)
<br><br>
<strong>Implementation Note:</strong> Yield scores are used strictly for relative ranking of pairs and are not interpreted in absolute magnitude due to scaling sensitivity in the optimization.
</div>
""", unsafe_allow_html=True)

# --- NEW: Recreating your uploaded plots interactively ---
st.markdown("### Structural OU Parameters & Horizon Risk")
col_ou1, col_ou2 = st.columns(2)

with col_ou1:
    st.image("half_life_distribution.png", caption="Distribution of Spread Half-Lives", use_container_width=True)

with col_ou2:
    # Display authentic OU spread plot generated from the research notebook
    st.image("ou_spread.png", caption="OU Process Fit & Mean Reversion", use_container_width=True)

with st.expander("View Stochastic Execution Bounds (Phase 3 Output)"):
    ou_df = pd.DataFrame(state["final_execution_universe"])
    ou_df = ou_df.rename(columns={
        "asset_x": "Asset X", "asset_y": "Asset Y", "ou_half_life_days": "Half-Life (Days)",
        "dimensionless_entry_sigma": "Entry (σ)", "dimensionless_exit_sigma": "Exit (σ)", "ou_yield_score": "Yield Score"
    })
    # Drop only the boolean filter flags; keep the structural math parameters to showcase the research
    cols_to_drop = ["viable_after_costs", "passes_dependence"]
    ou_df = ou_df.drop(columns=[col for col in cols_to_drop if col in ou_df.columns])
    
    # Rename the remaining columns for UI professionalism
    ou_df = ou_df.rename(columns={
        "ou_mu": "Mean (μ)", 
        "ou_theta": "Reversion Speed (θ)", 
        "ou_sigma": "Volatility (σ)", 
        "expected_trade_length": "Expected Duration"
    })
    
    st.dataframe(ou_df, use_container_width=True, hide_index=True)
st.divider()

# ==========================================
# SECTION 4: REGIME RISK MANAGEMENT
# ==========================================
st.markdown("<h2 id='4-regime-risk'><span class='section-badge'>Phase 4</span> Regime Risk Management (HMM)</h2>", unsafe_allow_html=True)


st.markdown("""
Mean-reverting relationships are not stable over time. Structural shifts can change the equilibrium between assets. If the equilibrium between assets shifts, static models may generate persistent losses. 

**The Mechanism:** To prevent this, the model uses an out-of-sample Hidden Markov Model (HMM) featuring Skew-T emissions and Time-Varying Transition Probabilities (TVTP). The continuous estimation of the regime state ($s_t$) acts as a control mechanism to detect structural breaks in real time and stop trading when needed.

To prevent Lookahead Bias, the Expectation-Maximization (EM) algorithm is strictly trained on a rolling 252-day historical window and only predicts the state of the forward 63-day block. The model's clarity is audited using the formal Baele (2005) Regime Classification Measure (RCM).
Models with high RCM scores are treated as unreliable and excluded from decision-making.

### Institutional Hard Half-Life Filter
Before passing the universe to the heavy HMM compute engine, the pipeline applies a simple constraint: **Pairs must possess an OU half-life between 1.0 and 60.0 days.** Pairs reverting too quickly (< 1 day) are likely microstructure noise, while pairs taking too long (> 60 days) tie up capital and invite excessive horizon risk.
""")



# Display authentic regime classification and trading band plots from the research notebook
col_hmm1, col_hmm2 = st.columns(2)

with col_hmm1:
    st.image("regime_classification.png", caption="Out-of-Sample Regime Decoding", use_container_width=True)

with col_hmm2:
    st.image("bock_mestel_trading_bands.png", caption="Bock & Mestel Trading Bands", use_container_width=True)


st.markdown("""
<div class="audit-box">
<strong>Markov Transition Dynamics (AEE vs CMS):</strong><br>
Based on the empirical transition matrix, the <strong>Expected Duration of the Low Mean Regime is 57.8 Trading Days</strong>, providing sufficient time for the Ornstein-Uhlenbeck mean-reversion cycle (6.18 days half-life) to safely execute.<br><br>
<strong>Volatility Expansion:</strong> The HMM detected a <strong>2.12x Volatility Expansion Ratio</strong> during structural breaks (Regime 1), supporting the use of a hard-stop filter to preserve capital.
</div>
""", unsafe_allow_html=True)


st.markdown("""
### Empirical Audit: The Asymmetric Filter

We tested an asymmetric filter designed to automatically block trades during identified regime shifts. The goal was to protect capital when the model detected a transition from historical equilibrium to a structural break. 
""")

col4, col5 = st.columns(2)
with col4:
    st.markdown("##### Blocked Trades (Toxic Data Filtered)")
    st.write("**Total:** 15 Trades  |  **Hit Rate:** 60.00%")
    st.write("**Expected Value:** 0.000467 log-points")
with col5:
    st.markdown("##### Accepted Trades (Executed)")
    st.write("**Total:** 24 Trades  |  **Hit Rate:** 87.50%")
    st.write("**Expected Value:** 0.020102 log-points")
    
st.markdown("""
<div class="audit-box">
<strong>Empirical Result:</strong><br>
The regime filter improved trade quality by removing structurally unstable periods. While this reduced total trade count, it increased average expected value per trade, indicating a more selective but higher-quality execution set.
</div>
""", unsafe_allow_html=True)

st.markdown("""
### Fracture Distance Optimization
To determine the exact mathematical breakpoint of a falling knife, the algorithm executed a **Fracture Distance Sweep** across increasing standard deviations.
""")

with st.expander("View Fracture Distance Sweep Data"):
    st.dataframe(load_fracture_sweep(), use_container_width=True, hide_index=True)

st.markdown("""
**Conclusion:** Setting the asymmetric filter beyond $3.0 \sigma$ begins accepting extremely toxic trades with negative expected values ($-0.0196$), confirming that the strictly constrained filter correctly protects the portfolio.
""")
st.divider()

# ==========================================
# SECTION 5: CONCLUSION
# ==========================================
st.markdown("<h2 id='5-production-roster'><span class='section-badge'>Phase 5</span> Final Tradable Pairs</h2>", unsafe_allow_html=True)



st.markdown("""
The table below shows the final set of pairs after all selection and risk filters.

Each pair satisfies:
- statistically significant cointegration,
- stable dependence structure under copula modeling,
- positive expected value after transaction costs,
- and acceptable regime stability based on HMM diagnostics.
""")


final_df = pd.DataFrame(state["live_production_roster"])

# Isolate only the most critical production metrics to prevent horizontal UI scrolling
display_cols = [
    "asset_x", "asset_y", "optimal_copula", "ou_yield_score", 
    "ou_half_life_days", "hmm_rcm_score", "hmm_expected_safe_duration"
]
final_df = final_df[display_cols].copy()

# Rename to clean, institutional headers
final_df = final_df.rename(columns={
    "asset_x": "Asset X",
    "asset_y": "Asset Y",
    "optimal_copula": "Copula",
    "ou_yield_score": "Yield Score",
    "ou_half_life_days": "Half-Life (Days)",
    "hmm_rcm_score": "RCM Score",
    "hmm_expected_safe_duration": "Safe Duration (Days)"
})

st.dataframe(final_df, use_container_width=True, height=320, hide_index=True)

st.markdown("<p style='text-align: center; font-size: 1.05rem; opacity: 0.7; margin-top: 30px;'><em>Pipeline complete. Results reflect out-of-sample evaluation.</em></p>", unsafe_allow_html=True)

st.markdown("### Execution Summary")

sc1, sc2, sc3, sc4, sc5 = st.columns(5)
with sc1: st.markdown("<div class='stat-box'><div class='stat-value'>459</div><div class='stat-label'>Initial Universe</div></div>", unsafe_allow_html=True)
with sc2: st.markdown("<div class='stat-box'><div class='stat-value'>14</div><div class='stat-label'>PCA-reduced features</div></div>", unsafe_allow_html=True)
with sc3: st.markdown("<div class='stat-box'><div class='stat-value'>38</div><div class='stat-label'>Clustered cohorts</div></div>", unsafe_allow_html=True)
with sc4: st.markdown("<div class='stat-box'><div class='stat-value'>23</div><div class='stat-label'>Statistically validated pairs</div></div>", unsafe_allow_html=True)
with sc5: st.markdown("<div class='stat-box'><div class='stat-value'>13</div><div class='stat-label'>Final Pairs</div></div>", unsafe_allow_html=True)

st.markdown("""
<div class="findings-box">
<div class="findings-title">Key Findings</div>
<ul>
<li><strong>Copula Modeling:</strong> Dependence modeling via non-linear structures improves signal quality over traditional Euclidean distance methods.</li>
<li><strong>OU Execution Bounds:</strong> Transaction cost-aware optimization ensures trades only execute when mathematically viable, resolving the baseline model's alpha decay.</li>
<li><strong>HMM Risk Filtering:</strong> Utilizing a regime filter successfully blocked structural trap trades, preserving capital and actively improving the portfolio's hit rate to 87.5%.</li>
</ul>
</div>
""", unsafe_allow_html=True)
