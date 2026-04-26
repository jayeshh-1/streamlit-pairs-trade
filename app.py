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
# CUSTOM CSS (Institutional & Readable)
# ==========================================
st.markdown("""
    <style>
    /* Main container width and font stack */
    .main { max-width: 1100px; margin: 0 auto; font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    
    /* Typography Upgrades */
    h1 { text-align: center; font-size: 2.8rem !important; font-weight: 900 !important; margin-bottom: 0.5rem !important; line-height: 1.25 !important; color: var(--text-color) !important; opacity: 0.95 !important; letter-spacing: -0.02em !important; }
    .subtitle { text-align: center; font-size: 1.3rem !important; color: var(--text-color) !important; opacity: 0.75 !important; font-style: italic !important; margin-bottom: 1.8rem !important; font-weight: 400 !important; }
    
    /* Elegant section spacing */
    h2 { font-weight: 800 !important; font-size: 2.2rem !important; margin-top: 2.8rem !important; border-bottom: 1px solid rgba(128, 128, 128, 0.2) !important; padding-bottom: 0.5rem !important; margin-bottom: 1.5rem !important; color: var(--text-color) !important; opacity: 0.95 !important; letter-spacing: -0.01em !important; }
    h3 { font-weight: 700 !important; font-size: 1.6rem !important; margin-top: 2rem !important; margin-bottom: 1rem !important; color: var(--text-color) !important; opacity: 0.95 !important; }
    
    /* Body text */
    div[data-testid="stMarkdownContainer"] p, 
    div[data-testid="stMarkdownContainer"] li { font-size: 1.25rem !important; line-height: 1.6 !important; font-weight: 400 !important; color: var(--text-color) !important; opacity: 0.9 !important; } 
    div[data-testid="stMarkdownContainer"] li { margin-bottom: 0.5rem !important; }
    div[data-testid="stMarkdownContainer"] strong { font-weight: 700 !important; color: var(--text-color) !important; opacity: 1.0 !important; }
    
    /* Badges & Hero */
    .section-badge { background-color: #2563EB; color: #FFFFFF !important; padding: 8px 16px; border-radius: 8px; font-size: 1.25rem; font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase; display: inline-block; vertical-align: middle; margin-right: 12px; }
    .h2-text { position: relative; top: 3px; }
    
    .hero-box { background-color: var(--secondary-background-color); border: 1px solid rgba(128, 128, 128, 0.2); border-radius: 6px; padding: 20px 25px; margin: 1.5rem 0 2.5rem 0; }
    .hero-box-title { font-size: 1.2rem; font-weight: 700; color: #3B82F6; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.05em; }
    
    /* Math, Findings, Pipeline & Callouts */
    .math-box { text-align: center; font-size: 1.05rem; color: var(--text-color); opacity: 0.6; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: -10px; margin-top: 1.5rem; font-weight: 600; }
    .findings-box { border-left: 5px solid #10B981 !important; padding: 1.2rem !important; margin: 2rem 0 !important; background-color: var(--secondary-background-color) !important; border-radius: 0 6px 6px 0 !important; }
    .findings-title { font-size: 1.25rem; font-weight: 700; margin-bottom: 10px; color: #10B981; text-transform: uppercase; letter-spacing: 0.05em; }
    
    /* BIGGER PIPELINE BLOCKS */
    .pipeline-container { display: flex; justify-content: space-between; align-items: stretch; margin: 2.5rem 0; gap: 15px; }
    .pipeline-block { background-color: var(--secondary-background-color); padding: 20px 15px; border-radius: 8px; text-align: center; flex: 1; border: 1px solid rgba(128, 128, 128, 0.2); box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
    .pipeline-block-title { font-size: 1.25rem; font-weight: 800; text-transform: uppercase; margin-bottom: 8px; color: #3B82F6; }
    .pipeline-block-desc { font-size: 1.25rem; opacity: 0.9; line-height: 1.4; }
    .pipeline-arrow { font-size: 2.0rem; opacity: 0.3; display: flex; align-items: center; }

    /* BIGGER CALLOUT BOXES */
    .mechanism-box { border-left: 5px solid #3B82F6 !important; padding: 1.5rem 1.8rem !important; margin: 2rem 0 !important; background-color: var(--secondary-background-color) !important; color: var(--text-color) !important; border-radius: 0 8px 8px 0 !important; font-size: 1.3rem !important; line-height: 1.7 !important; }
    .audit-box { border-left: 5px solid #6B7280 !important; padding: 1.5rem 1.8rem !important; margin: 2rem 0 !important; color: var(--text-color) !important; background-color: var(--secondary-background-color) !important; border-radius: 0 8px 8px 0 !important; font-size: 1.3rem !important; line-height: 1.7 !important; }
    .callout { border-left: 5px solid #3B82F6 !important; padding-left: 1.25rem !important; margin: 1.4rem 0 !important; color: var(--text-color) !important; font-size: 1.25rem !important; background-color: transparent !important; }

    /* Stats Box */
    .stat-box { background-color: var(--secondary-background-color) !important; border: 1px solid rgba(128, 128, 128, 0.2) !important; border-radius: 6px !important; padding: 15px !important; text-align: center !important; margin-bottom: 15px !important; }
    .stat-value { font-size: 2.0rem !important; font-weight: 700 !important; color: var(--text-color) !important; margin-bottom: 2px !important; line-height: 1 !important;}
    .stat-label { font-size: 0.85rem !important; font-weight: 600 !important; color: var(--text-color) !important; opacity: 0.6 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important;}
    
    /* TOC Links */
    .toc-link { text-decoration: none !important; font-size: 1.2rem !important; text-align: center !important; display: block !important; padding: 12px 10px !important; font-weight: 500 !important; color: var(--text-color) !important; opacity: 0.8 !important; transition: opacity 0.2s ease-in-out !important; }
    .toc-link:hover { opacity: 1.0 !important; color: #FBBF24 !important; background-color: rgba(251, 191, 36, 0.05) !important; text-decoration: none !important; }

    /* Sidebar Brand Card */
    .author-card-fixed { background-color: #0F172A !important; border-top: 2px solid #FBBF24 !important; border-radius: 10px !important; padding: 12px 10px !important; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important; margin-bottom: 15px !important; text-align: center !important; }
    .sidebar-label-fixed { color: #FBBF24 !important; font-weight: 900 !important; letter-spacing: 0.15em !important; text-transform: uppercase !important; font-size: 1.03rem !important; display: block !important; margin-bottom: 2px !important; }
    .sidebar-author-fixed { color: #FFFFFF !important; font-weight: 800 !important; font-size: 1.34rem !important; display: block !important; line-height: 1.1 !important; }
    .sidebar-sub-fixed { color: rgba(255, 255, 255, 0.65) !important; font-style: italic !important; font-weight: 400 !important; font-size: 1.05rem !important; display: block !important; margin-top: 8px !important; border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 6px !important; }

    /* Mobile Overrides */
    .mobile-sidebar-hint { display: none; }
    .mobile-menu-badge { display: none; } 

    @media (max-width: 768px) {
        .mobile-sidebar-hint { display: block !important; background-color: rgba(59, 130, 246, 0.1); color: #3B82F6; padding: 12px; border-radius: 8px; text-align: center; font-weight: 500; font-size: 0.95rem; margin-top: 25px; border: 1px solid rgba(59, 130, 246, 0.3); line-height: 1.4; }
        .mobile-menu-badge { display: block !important; position: fixed; top: 14px; left: 55px; background-color: #2563EB; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem; font-weight: 800; letter-spacing: 0.05em; text-transform: uppercase; z-index: 999999 !important; box-shadow: 0 2px 5px rgba(0,0,0,0.2); animation: pulse 2s infinite; pointer-events: none; transition: opacity 0.2s ease-in-out, visibility 0.2s; }
        
        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(37, 99, 235, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
        }

        .stApp:has([data-testid="stSidebar"][aria-expanded="true"]) .mobile-menu-badge { opacity: 0 !important; visibility: hidden !important; }
    }
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
    <a href="#0-problem-setup" target="_self" class="toc-link">0. Problem Setup & Approach</a>
    <a href="#1-dimensionality-stationarity" target="_self" class="toc-link">1. Dimensionality & Stationarity</a>
    <a href="#2-extremal-dependence" target="_self" class="toc-link">2. Extremal Dependence (Copulas)</a>
    <a href="#3-execution-friction" target="_self" class="toc-link">3. Execution Friction & Bounds</a>
    <a href="#4-regime-risk" target="_self" class="toc-link">4. Regime Risk Management</a>
    <a href="#5-production-roster" target="_self" class="toc-link">5. Final Tradeable Pairs</a>
    <div class="mobile-sidebar-hint">
        <strong>Tap outside</strong> or <strong>swipe left</strong> to close menu.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="author-card-fixed">
        <span class="sidebar-label-fixed">AUTHOR</span>
        <span class="sidebar-author-fixed">Jayesh Chaudhary</span>
        <span class="sidebar-sub-fixed">Quantitative Researcher</span>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# MAIN DOCUMENT: TITLE & HERO
# ==========================================

# Mobile Tooltip pointing to the Sidebar
st.markdown('<div class="mobile-menu-badge">👈 Topics Menu</div>', unsafe_allow_html=True)

st.markdown("<h1>Advanced Statistical Arbitrage: Copulas & Stochastic Control</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>A multi-stage statistical arbitrage pipeline combining clustering, copulas, and stochastic control for pair selection and execution.</p>", unsafe_allow_html=True)

# Small, muted author line under the subtitle
st.markdown("""
    <div style='text-align: center; margin-top: -1.0rem; margin-bottom: 3rem;'>
        <span style='font-size: 1.0rem; color: var(--text-color); opacity: 0.5; font-weight: 400; letter-spacing: 0.15em; text-transform: uppercase;'>
            Research by <strong>Jayesh Chaudhary</strong>
        </span>
    </div>
""", unsafe_allow_html=True)

# Quick Stats Bar
col_a, col_b, col_c = st.columns(3)
box_css = "background-color: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 8px; padding: 20px 15px; text-align: center; margin-bottom: 20px;"
val_css = "font-size: 1.7rem; font-weight: 800; color: #10B981; margin-bottom: 6px; line-height: 1;"
lbl_css = "font-size: 0.90rem; font-weight: 600; color: var(--text-color); opacity: 0.7; text-transform: uppercase; letter-spacing: 0.05em;"

with col_a:
    st.markdown(f"<div style='{box_css}'><div style='{lbl_css}'>Data Source</div><div style='{val_css}'>S&P 500 (459 stocks)</div></div>", unsafe_allow_html=True)
with col_b:
    st.markdown(f"<div style='{box_css}'><div style='{lbl_css}'>Trading Years</div><div style='{val_css}'> 2015-2025 (10 years)</div></div>", unsafe_allow_html=True)
with col_c:
    st.markdown(f"<div style='{box_css}'><div style='{lbl_css}'>Timeframe</div><div style='{val_css}'>EOD (1D)</div></div>", unsafe_allow_html=True)


st.markdown("""
<div class="hero-box">
    <div class="hero-box-title">Key Contributions</div>
    <ul>
        <li><strong>Universe Reduction:</strong> Narrowed down the S&P 500 using PCA and OPTICS clustering to find stocks that actually move together.</li>
        <li><strong>Statistical Filtering:</strong> Kept only the pairs that proved to be strongly cointegrated and mean-reverting.</li>
        <li><strong>Copula Modeling:</strong> Replaced basic linear correlation with Copulas (auto-selected via AIC) to accurately map complex, non-linear price relationships.</li>
        <li><strong>Smart Execution:</strong> Built an Ornstein-Uhlenbeck (OU) stochastic model to calculate exact entry/exit thresholds that account for 15bps transaction costs.</li>
        <li><strong>Regime Risk Switch:</strong> Added a Hidden Markov Model (HMM) to detect structural market breaks and automatically halt trading to protect capital.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SECTION 0: INTUITION
# ==========================================
st.markdown("<h2 id='0-problem-setup'><span class='section-badge'>Phase 0</span><span class='h2-text'> Problem Setup & Approach</span></h2>", unsafe_allow_html=True)


st.markdown("""
Traditional pairs trading usually relies on basic distance metrics—finding two stocks with price paths that look similar. The problem? Once you factor in transaction costs and real-world market shifts, those simple spreads often fall apart and fail to mean-revert.
This project builds a more advanced approach. Instead of just looking at distance, it combines unsupervised learning, non-linear copula modeling, and stochastic control to find better pairs and execute them smarter.

### Research Workflow Architecture
**Dataset:** Daily adjusted close prices for S&P 500 constituents (Jan 2015 – Jan 2021). 

The workflow below shows exactly how we filter a massive universe of raw data down to a handful of highly profitable, structurally sound pairs.
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
values = [459, 14, 38, 23, 20, 20]

st.markdown("""
<style>
/* Custom CSS for the Filtering Pipeline */
.filter-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    margin: 3rem 0;
}
.filter-step {
    background-color: var(--secondary-background-color);
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-left: 6px solid #3B82F6;
    padding: 20px 40px; /* Increased padding */
    border-radius: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    max-width: 800px; /* Made the box wider */
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    transition: transform 0.2s ease;
}
.filter-step:hover { transform: translateX(5px); }
.filter-label { font-size: 1.43rem; font-weight: 700; color: var(--text-color); } /* Bigger label */
.filter-desc { font-size: 1.23rem; color: var(--text-color); opacity: 0.8; margin-top: 6px; } /* Bigger desc */
.filter-metric { font-size: 2.2rem; font-weight: 900; color: #3B82F6; text-align: right; line-height: 1; } /* Massive numbers */
.filter-unit { font-size: 1.2rem; font-weight: 700; color: var(--text-color); opacity: 0.6; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 4px; }
.filter-arrow { color: var(--text-color); opacity: 0.3; font-size: 2.0rem; font-weight: bold; text-align: center; width: 100%; }
.filter-final { border-left: 6px solid #10B981; }
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
<div><div class="filter-label">Final Tradable Pairs</div><div class="filter-desc">Active Ready Pairs</div></div>
<div><div class="filter-metric">20</div><div class="filter-unit">Pairs</div></div>
</div>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="audit-box">
<strong>Interpretation:</strong> The pipeline reduced the search space from an unmanageable index of 459 assets to a highly refined, statistically valid execution roster of 20 pairs.
</div>
""", unsafe_allow_html=True)
st.divider()

# ==========================================
# SECTION 1: DIMENSIONALITY & STATIONARITY
# ==========================================
st.markdown("<h2 id='1-dimensionality-stationarity'><span class='section-badge'>Phase 1</span><span class='h2-text'> Dimensionality & Stationarity</span></h2>", unsafe_allow_html=True)


st.markdown(r"""
Evaluating a 459-stock universe yields $C(459,2) = 105,111$ candidate pairs. Applying cointegration tests to all of them without pre-filtering creates a severe multiple testing problem: at a 5% significance level, approximately 5,255 pairs would appear cointegrated purely by chance (Type 1 error in Hypothesis Testing). 

To manage this, the pipeline imposes a structural prior using unsupervised learning before any hypothesis testing begins.
""")

with st.expander("Data Engineering Baseline: Log-Returns Framework"):
    st.markdown(r"""
    Raw price levels are integrated processes, $I(1)$, while PCA requires stationary inputs to produce meaningful factor loadings. Therefore, log-returns are used because they are approximately stationary, $I(0)$, additive across time ($log(P_T/P_0) = \Sigma log(P_t/P_{t-1})$), and they normalize across vastly different price levels[cite: 31, 32, 33]. The spread construction follows directly from this log-price framework: 
    """)
    st.latex(r"S_t = \log(P_t^A) - \beta \cdot \log(P_t^B)")
    st.markdown("This represents the log-ratio of a dollar-neutral portfolio[cite: 34].")

col_pca_text, col_pca_plot = st.columns([1.2, 1])

with col_pca_text:
    st.markdown("""
    **The Mechanism:**
    **1.** First, the model uses Principal Component Analysis (PCA) to distill the daily noise down to the core drivers of variance (retaining >60% of the variance). 
    
    **2.** It maps these latent factors into a 3D space and applies OPTICS clustering to group stocks that actually move together, adapting to local densities across different market sectors.
    
    **3.** We restrict all hypothesis testing strictly to pairs that belong to the exact same cluster.
    
    This quickly reduces our massive 459-stock universe down to 14 principal components, grouping them into **38 distinct asset clusters** (for example, Cluster 28 cleanly isolates energy sector stocks like `COP`, `EOG`, `HAL`, and `SLB`).
    """)
    
    with st.expander("View Formal PCA & OPTICS Mathematics"):
        st.markdown(r"""
        **1. PCA Factor Extraction:**
        We compute the sample covariance matrix $\Sigma = (1/T)R'R$ and solve the eigenvalue problem $\Sigma v_k = \lambda_k v_k$. We retain the minimum $K$ principal components such that the cumulative variance explained $\Sigma_{k=1}^{K} \lambda_k / \Sigma_j \lambda_j \geq 0.60$. The 0.60 threshold is the empirical inflection point; higher thresholds introduce idiosyncratic noise that destabilizes downstream clustering, while lower thresholds discard systematic variance.
        
        **2. OPTICS Density Clustering:**
        Traditional k-means assumes spherical clusters, failing in equity factor spaces. DBSCAN requires a global epsilon radius, failing because density varies across sectors. OPTICS computes a reachability distance adapting to local density. With `min_cluster_size = 3`, we ensure cross-validation of the cluster's economic coherence.
        """)
    
    st.markdown("""
    <div class="mechanism-box">
    <strong>Controlling the Math</strong><br>
    If you test every possible combination in the S&P 500, you will find accidental, meaningless correlations just by pure luck. By forcing the algorithm to only look for pairs <em>within</em> these tight, pre-calculated clusters, we massively cut down the search space and prevent the model from finding fake relationships.
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

Pairs within each cluster are then tested to see if they actually form a reliable spread.

Individual stock prices are inherently unpredictable and tend to drift over time (non-stationary). However, if two stocks are **cointegrated**, it means we can combine them mathematically to create a spread that *is* stationary, meaning it consistently snaps back to a predictable baseline. 

A pair is only retained if it proves this relationship mathematically: it must pass the Engle-Granger cointegration test ($p < 0.05$) and show a strong tendency to mean-revert rather than trend (Hurst Exponent $< 0.45$).
""")

with st.expander("Formal Statistical Disqualification Rules"):
    st.markdown(r"""
    Pairs undergo two sequential Rules of Disqualification. Failure at either stage results in immediate elimination to prevent borderline pair accumulation.

    * **Rule 1: Engle-Granger Cointegration:** We estimate the hedge ratio via OLS: P_t^Y = α + β·P_t^X + ε_t, the hedge ratio is $\beta = (X'X)^{-1}X'Y$, and apply an Augmented Dickey-Fuller (ADF) test to the spread $S_t$. The null hypothesis of a unit root must be rejected at $p < 0.05$.
    * **Rule 2: Hurst Exponent ($H$):** Using the variance-of-difference method where $Var(S_{t+\tau} - S_t) \propto \tau^{2H}$, we require $H < 0.45$. The random walk boundary is $0.5$; the $0.45$ threshold provides a strict mathematical margin of safety ensuring genuine mean-reversion.
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
st.markdown("<h2 id='2-extremal-dependence'><span class='section-badge'>Phase 2</span><span class='h2-text'> Extremal Dependence (Copulas)</span></h2>", unsafe_allow_html=True)


st.markdown("""
<div class="mechanism-box">
<strong>The Limits of Linear Correlation:</strong><br>
Pearson correlation only captures simple, linear relationships and assumes joint normality. In reality, equity returns exhibit excess kurtosis (fat tails) and asymmetric dependence (assets tend to crash together more strongly than they rally together). Copulas solve this by stripping away individual asset volatility, isolating the pure structural relationship.
</div>
""", unsafe_allow_html=True)



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
    """)
    
    with st.expander("View Copula MLE & CMPI Formulation"):
        st.markdown(r"""
        **Sklar's Theorem & Marginal Transformation:**
        Any joint distribution can be decomposed into its continuous marginals and a unique copula $C$: $F(x,y) = C(F_X(x), F_Y(y))$. We isolate this structure by mapping returns to uniform marginals via an ECDF. 
        
        *Crucial Engineering Step:* These marginals are strictly clipped to $[10^{-4}, 1-10^{-4}]$. Failing to do this causes numerical overflow in MLE estimation because inverse CDF functions (like $\Phi^{-1}(0)$) diverge to $-\infty$.
        
        **Cumulative Mispricing Index (CMPI):**
        We calculate the continuous conditional probability directly from the copula's distribution: 
        """)
        st.latex(r"MPI_{X|Y}(t) = P(U \leq u_t | V = v_t) = \frac{\partial C(u_t,v_t)}{\partial v_t}")
        st.markdown(r"""
        To smooth daily noise, we construct a rolling 21-day Cumulative Mispricing Index (CMPI):
        """)
        st.latex(r"CMPI_X(t) = \sum_{s=t-20}^{t} (MPI_{X|Y}(s) - 0.5)")
        st.markdown(r"""
        A long/short trade is initiated when directional disagreement occurs and $|CMPI| > 0.6$. A strict stop-loss and 'penalty box' mechanism is triggered if $|CMPI| > 2.0$.
        """)

with col_cop_plot:
    st.image("copula_scatter.png", caption="Copula Dependence Structure", use_container_width=True)
    st.markdown("<p style='font-size:0.85rem; opacity:0.7; text-align:center;'><em>Axes represent historical return percentiles (0.0 to 1.0). This isolates structural dependence by removing individual asset volatility.</em></p>", unsafe_allow_html=True)

st.markdown("""
<div class="audit-box">
<strong>Data Engineering Control: Term Structure Blindness</strong><br>
If you try to fit a copula directly to raw asset prices, the math breaks. Because equity prices generally drift upward over the years, the percentiles will permanently skew towards 1.0. To preserve the structural integrity of the model, all percentile transformations are executed strictly on daily returns, not absolute prices.
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
    "hurst_exponent": "Hurst EXP.",
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
st.markdown("<h2 id='3-execution-friction'><span class='section-badge'>Phase 3</span><span class='h2-text'> Stochastic Execution Bounds</span></h2>", unsafe_allow_html=True)


st.markdown("""
Holding a position ties up capital. It carries **Horizon Risk** (the uncertainty of exactly when the mispricing will correct) and **Divergence Risk** (the mathematical probability the spread widens further before converging). Standard pairs trading uses fixed $\pm 2\sigma$ entry bands. It ignores **the holding time**, fails to integrate transaction costs into the optimization objective, and is not derived from any rigorous optimality criterion. 

To solve this, the pipeline models the spread as a continuous Ornstein-Uhlenbeck (OU) process and applies the **Zeng & Lee (2014) Stochastic Control framework**. 
""")

st.markdown("""
<div class="math-box">
<strong>Equation 1: Continuous Ornstein-Uhlenbeck (OU) Process</strong>
</div>
""", unsafe_allow_html=True)
st.latex(r"dX_t = \theta (\mu - X_t)dt + \sigma dW_t")

st.markdown(r"""
Instead of guessing entry bands, the model solves a Hamilton-Jacobi-Bellman (HJB) optimal stopping problem[cite: 2173]. It mathematically derives the exact optimal entry and exit thresholds by maximizing the expected profit *per unit of time*[cite: 2175, 2178], embedding a strict **15 basis point transaction cost** directly into the objective function[cite: 2031, 2188].
""")


st.markdown("""
<div class="math-box">
<strong>Equation 1: Continuous Ornstein-Uhlenbeck (OU) Process</strong>
</div>
""", unsafe_allow_html=True)
st.latex(r"dX_t = \theta (\mu - X_t)dt + \sigma dW_t")

st.markdown("""
Instead of guessing entry bands, the model mathematically derives the exact optimal entry and exit thresholds. It does this by maximizing the expected profit against the expected holding time.

More importantly, this approach allows the optimizer to internalize a strict **15 basis point transaction cost**. If the math shows that the expected profit won't cover the execution friction faster than the expected holding time, the trade is automatically rejected.
""")

with st.expander("View Formal OU Discretization & MLE Estimation"):
    st.markdown(r"""
    **AR(1) Discretization:**
    The continuous OU SDE cannot be estimated directly from discrete daily data[cite: 2095]. We discretize it over interval $\Delta t = 1/252$ to obtain an AR(1) process[cite: 2096]:
    """)
    st.latex(r"X_t = \alpha + \beta X_{t-1} + \epsilon_t")
    st.markdown(r"""
    We run OLS regression to estimate $\alpha$ and $\beta$[cite: 2103]. Under Gaussian errors, OLS on an AR(1) process is mathematically equivalent to Maximum Likelihood Estimation (MLE)[cite: 2116]. 
    
    **Parameter Recovery & Stationarity:**
    We recover the continuous parameters via $\theta = -\ln(\beta)/\Delta t$ and $\mu = \alpha/(1-\beta)$[cite: 2108, 2109]. Crucially, $\beta$ is strictly clipped to $[10^{-4}, 0.9999]$[cite: 2105]. This enforces mean-reverting stationarity and prevents severe numerical instability (division by zero) for unit root processes[cite: 2114, 2115].
    """)

with st.expander("View Zeng-Lee HJB Dimensionless Optimization"):
    st.markdown(r"""
    **Dimensionless Transformation:**
    Raw OU parameters vary across pairs, making direct optimization impossible[cite: 2146]. We transform the spread into dimensionless coordinates: $x_d = (x-\mu)/\sigma_{OU}$, where $\sigma_{OU} = \sigma/\sqrt{2\theta}$ is the stationary standard deviation[cite: 2149]. The dimensionless transaction cost becomes $c_{dim} = c / \sigma_{OU}$[cite: 2152]. 
    
    *Hard Constraint:* If $c_{dim} \ge 1.0$, the round-trip execution cost exceeds the spread's entire natural fluctuation[cite: 2157]. The trade is mathematically impossible and immediately rejected[cite: 2155, 2159].
    
    **Log-Transformed HJB Objective:**
    The original objective maximizes Yield $= (a_d - b_d - c_{dim}) / \mathbb{E}[T]$[cite: 2195]. Because the numerator (profit margin) and denominator (expected first-passage time) are often tiny fractions, the exponential surface causes severe vanishing gradients and optimizer crashes (`max_fev`)[cite: 2199, 2200]. 
    
    We resolve this by minimizing the log-transformed objective, converting the exponential surface to a well-conditioned linear one[cite: 2204, 2206]:
    """)
    st.latex(r"\min \left[ \ln(\mathbb{E}[T]) - \ln(a_d - b_d - c_{dim}) \right]")

st.markdown("""
<div class="audit-box">
<strong>Empirical OU Fit (AEE vs CMS):</strong><br>
• <strong>Spread Half-Life (Horizon Risk):</strong> 6.18 Trading Days<br>
• <strong>Mean Reversion Speed (θ):</strong> 28.2635 (Exceptionally fast)<br>
• <strong>Dimensionless Cost Barrier ($c_{dim}$):</strong> 0.0502 (Highly tradable)<br>
• <strong>Optimal Entry Solution:</strong> ±0.15 $\sigma_{OU}$ (Incorporating 15 bps execution cost)
<br><br>
<strong>Interpretation:</strong> With transaction costs at only 5% of the natural spread fluctuation, the HJB optimizer mathematically proves that entering on very small deviations (0.15 $\sigma_{OU}$) is optimal given the extreme mean-reversion speed. Yield scores generated from this output are used strictly for relative portfolio ranking, not as absolute return forecasts.
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
st.markdown("<h2 id='4-regime-risk'><span class='section-badge'>Phase 4</span><span class='h2-text'> Regime Risk Management (HMM)</span></h2>", unsafe_allow_html=True)


st.markdown("""
Mean-reverting relationships are rarely stable forever. Structural market shifts can permanently alter the equilibrium between two assets—and if a static model keeps trying to trade a broken spread, it will generate persistent losses. 

**The Mechanism:** To prevent this, the pipeline uses an out-of-sample Hidden Markov Model (HMM) featuring Skew-T emissions and Time-Varying Transition Probabilities (TVTP). By continuously estimating the current regime state ($s_t$), the model acts as an emergency brake, detecting structural breaks in real-time and halting trading.

To absolutely prevent Lookahead Bias, the Expectation-Maximization (EM) algorithm is strictly trained on a rolling 252-day historical window to predict the forward 63-day block. Any model that fails the formal Baele (2005) Regime Classification Measure (RCM) is flagged as unreliable and excluded.

### The Baseline Constraint: The Half-Life Filter
Before feeding the universe into the heavy HMM compute engine, we apply a hard mathematical constraint: **Pairs must possess an OU half-life between 1.0 and 60.0 days.** Pairs reverting too quickly (< 1 day) are likely just microstructure noise, while pairs taking too long (> 60 days) tie up capital and invite unacceptable horizon risk.
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
Based on the empirical transition matrix, the <strong>Expected Duration of the High Mean Regime is 57.8 Trading Days</strong>, while the Low Mean Regime lasts only 11.4 days. This provides plenty of runway for the Ornstein-Uhlenbeck mean-reversion cycle (which has a 6.18-day half-life) to safely execute.<br><br>
<strong>Volatility Expansion:</strong> The HMM successfully separated a highly volatile state (21.2% annualized) from a stable state (9.7% annualized). By dynamically tracking these states, the asymmetric filter acts as a real-time risk overlay, mathematically isolating and blocking toxic trade entries.
</div>
""", unsafe_allow_html=True)


st.markdown("""
### Empirical Audit: The Asymmetric Filter

We backtested an asymmetric filter designed to automatically block trades the moment a structural break is detected. The goal was simple: protect capital when the historical equilibrium fails.
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
The regime filter actively improved trade quality by stripping out structurally unstable periods. While this reduced the total trade volume, it significantly increased the expected value per trade, yielding a highly selective, 87.5% hit-rate execution set.
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
st.markdown("<h2 id='5-production-roster'><span class='section-badge'>Phase 5</span><span class='h2-text'> Final Tradable Pairs</span></h2>", unsafe_allow_html=True)



st.markdown("""
This is the final production roster. After filtering a universe of over 100,000 potential combinations down to just 20, the pairs below represent the highest-conviction opportunities in the dataset.

To survive the pipeline, each pair mathematically proved:
- **Stationarity:** Statistically significant cointegration.
- **Structural Integrity:** A stable, non-linear dependence structure under AIC-selected Copula modeling.
- **Profitability:** A positive expected value *after* accounting for execution friction and holding time.
- **Safety:** Strong regime stability validated by Out-of-Sample HMM diagnostics.
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
with sc3: st.markdown("<div class='stat-box'><div class='stat-value'>38</div><div class='stat-label'>Asset Clusters</div></div>", unsafe_allow_html=True)
with sc4: st.markdown("<div class='stat-box'><div class='stat-value'>23</div><div class='stat-label'>Statistically Validated Pairs</div></div>", unsafe_allow_html=True)
with sc5: st.markdown("<div class='stat-box'><div class='stat-value'>20</div><div class='stat-label'>Execution Filtered Pairs</div></div>", unsafe_allow_html=True)

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


# ==========================================
# FOOTER
# ==========================================
st.markdown("""
<div style='text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid rgba(128, 128, 128, 0.2);'>
    <p style='font-size: 1.15rem; color: #6B7280; font-style: italic;'>
        If you made it all the way to the end, thank you for viewing my work.<br>
        I am always looking to refine these projects, so if you have critiques, suggestions, or just want to talk market dynamics, I'd love to hear them:
    </p>
    <a href='mailto:jayeshchaudharyofficial@gmail.com' style='font-size: 1.15rem; font-weight: 700; color: #FFFFFF; background-color: #3B82F6; padding: 10px 24px; border-radius: 6px; text-decoration: none; display: inline-block; transition: all 0.2s;'>
        ✉️ Email Me
    </a>
</div>
""", unsafe_allow_html=True)