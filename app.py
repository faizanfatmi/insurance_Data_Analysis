import textwrap
import pandas as pd
import joblib
import streamlit as st
import streamlit.components.v1 as components

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Insurance Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)


def render_html(content):
    st.markdown(textwrap.dedent(content), unsafe_allow_html=True)


# ==================================================
# GLOBAL CSS
# ==================================================
render_html("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    header[data-testid="stHeader"] {
        background-color: transparent;
        height: 3.5rem;
    }
    [data-testid="stToolbar"] {
        visibility: hidden;
    }
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999999 !important;
    }
    [data-testid="collapsedControl"] svg {
        fill: #F1EFF5 !important;
    }
    [data-testid="stSidebarCollapseButton"] button svg,
    [data-testid="baseButton-header"] svg {
        fill: #F1EFF5 !important;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    .stApp {
        background-color: #0D0C12;
        color: #F1EFF5;
    }

    section[data-testid="stSidebar"] {
        background-color: #111017;
        border-right: 1px solid #292733;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Sidebar brand */
    .sidebar-brand-title {
        color: #F1EFF5;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 0.1rem;
    }
    .sidebar-brand-sub {
        color: #777480;
        font-size: 0.78rem;
        margin-bottom: 1.6rem;
    }
    .sidebar-nav-label {
        color: #777480;
        font-size: 0.7rem;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin: 0.6rem 0 0.4rem 0;
    }

    .model-info-card {
        background-color: #15141C;
        border: 1px solid #292733;
        border-radius: 14px;
        padding: 16px 16px;
        margin-top: 1.8rem;
    }
    .model-info-title {
        color: #F1EFF5;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .model-info-row {
        color: #A9A6B2;
        font-size: 0.78rem;
        margin-bottom: 4px;
    }

    /* Sidebar radio styling as nav */
    div[role="radiogroup"] label {
        background-color: transparent;
        border-radius: 10px;
        padding: 6px 10px;
        margin-bottom: 2px;
        color: #C9C6D2;
        font-size: 0.88rem;
        transition: background-color 0.15s ease;
    }
    div[role="radiogroup"] label:hover {
        background-color: #181722;
    }
    div[role="radiogroup"] > label > div:first-child {
        display: none;
    }

    /* Header */
    .dashboard-header-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1.8rem;
        flex-wrap: wrap;
        gap: 12px;
    }
    .dashboard-title {
        font-size: 1.9rem;
        font-weight: 800;
        color: #F1EFF5;
        margin-bottom: 4px;
    }
    .dashboard-subtitle {
        color: #777480;
        font-size: 0.92rem;
    }
    .status-badge {
        background-color: rgba(103, 216, 209, 0.1);
        border: 1px solid rgba(103, 216, 209, 0.35);
        color: #67D8D1;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 7px 14px;
        border-radius: 999px;
        white-space: nowrap;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #67D8D1;
        display: inline-block;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(180deg, #181722 0%, #15141C 100%);
        border: 1px solid #292733;
        border-radius: 16px;
        padding: 18px 20px;
        height: 100%;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    }
    .metric-label {
        color: #777480;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        margin-bottom: 10px;
    }
    .metric-value {
        color: #F1EFF5;
        font-size: 1.55rem;
        font-weight: 800;
        margin-bottom: 6px;
    }
    .metric-desc {
        color: #777480;
        font-size: 0.78rem;
    }

    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #F1EFF5;
        margin-top: 1.4rem;
        margin-bottom: 2px;
    }
    .section-subtitle {
        color: #777480;
        font-size: 0.88rem;
        margin-bottom: 1.2rem;
    }

    .input-card {
        background-color: #15141C;
        border: 1px solid #292733;
        border-radius: 16px;
        padding: 22px 24px 6px 24px;
        margin-bottom: 1.4rem;
    }

    /* Streamlit widget overrides */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #181722 !important;
        border: 1px solid #292733 !important;
        color: #F1EFF5 !important;
        border-radius: 10px !important;
    }
    label, .stNumberInput label, .stSelectbox label {
        color: #A9A6B2 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] svg {
        fill: #777480;
    }

    /* Health profile card */
    .health-card {
        background: linear-gradient(135deg, rgba(232,117,50,0.10) 0%, rgba(21,20,28,0.6) 60%);
        border: 1px solid rgba(232,117,50,0.35);
        border-radius: 18px;
        padding: 22px 26px;
        margin-bottom: 1.6rem;
    }
    .health-title {
        color: #F1EFF5;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 2px;
    }
    .health-subtitle {
        color: #A9A6B2;
        font-size: 0.82rem;
        margin-bottom: 18px;
    }
    .health-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 18px;
    }
    .health-item-label {
        color: #C99A70;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        margin-bottom: 6px;
    }
    .health-item-value {
        color: #F1EFF5;
        font-size: 1.1rem;
        font-weight: 700;
    }
    .bmi-badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 700;
        background-color: rgba(232, 117, 50, 0.16);
        color: #E87532;
        border: 1px solid rgba(232, 117, 50, 0.4);
    }

    /* Predict button */
    div.stButton > button {
        background-color: #E87532;
        color: #0D0C12;
        border: none;
        border-radius: 12px;
        padding: 0.85rem 1.5rem;
        font-weight: 700;
        font-size: 1rem;
        width: 100%;
        transition: background-color 0.15s ease;
        box-shadow: 0 6px 18px rgba(232,117,50,0.25);
    }
    div.stButton > button:hover {
        background-color: #F08442;
        color: #0D0C12;
    }

    /* Result card */
    .result-card {
        background: linear-gradient(135deg, rgba(103,216,209,0.12) 0%, rgba(21,20,28,0.7) 65%);
        border: 1px solid rgba(103,216,209,0.4);
        border-radius: 18px;
        padding: 32px;
        text-align: center;
        margin-top: 1.6rem;
    }
    .result-label {
        color: #67D8D1;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        margin-bottom: 10px;
    }
    .result-value {
        color: #F1EFF5;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .result-subtitle {
        color: #A9A6B2;
        font-size: 0.85rem;
        max-width: 480px;
        margin: 0 auto;
    }

    /* Empty state */
    .empty-state-card {
        background-color: #15141C;
        border: 1px dashed #292733;
        border-radius: 16px;
        padding: 50px 20px;
        text-align: center;
        margin-top: 1rem;
    }
    .empty-state-title {
        color: #F1EFF5;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 6px;
        letter-spacing: 0.04em;
    }
    .empty-state-sub {
        color: #777480;
        font-size: 0.85rem;
    }

    .fi-row-wrap {
        background-color: #15141C;
        border: 1px solid #292733;
        border-radius: 16px;
        padding: 22px 26px;
        margin-top: 1rem;
    }
    .fi-row {
        margin-bottom: 14px;
    }
    .fi-row-top {
        display: flex;
        justify-content: space-between;
        margin-bottom: 6px;
        font-size: 0.85rem;
    }
    .fi-row-name {
        color: #C9C6D2;
        font-weight: 600;
    }
    .fi-row-val {
        color: #777480;
    }
    .fi-bar-bg {
        background-color: #181722;
        border-radius: 6px;
        height: 9px;
        width: 100%;
        overflow: hidden;
    }
    .fi-bar-fill {
        background: linear-gradient(90deg, #E87532, #F08442);
        height: 100%;
        border-radius: 6px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #292733;
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""")

# ==================================================
# CONSTANTS
# ==================================================
FEATURE_ORDER = [
    "age", "is_Female", "bmi", "children",
    "is_smoker", "region_southeast", "bmi_category_Obese"
]

R2_SCORE = 0.8670585555546673
MAE = 2868.836258987799
RMSE = 4942.549886434875


# ==================================================
# MODEL LOADING
# ==================================================
@st.cache_resource
def load_model():
    return joblib.load("insurance_model.pkl")


model = load_model()

# ==================================================
# SESSION STATE
# ==================================================
if "history" not in st.session_state:
    st.session_state.history = []
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None


def get_bmi_category(bmi_value):
    if bmi_value >= 30:
        return "Obese"
    elif bmi_value >= 25:
        return "Overweight"
    elif bmi_value >= 18.5:
        return "Normal"
    else:
        return "Underweight"


# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    render_html("""
    <div class="sidebar-brand-title">Insurance Predictor</div>
    <div class="sidebar-brand-sub">Medical Cost Prediction System</div>
    """)

    render_html('<div class="sidebar-nav-label">NAVIGATION</div>')
    page = st.radio(
        "Navigation",
        ["Dashboard", "Prediction History", "Model Analytics"],
        label_visibility="collapsed"
    )

    render_html(f"""
    <div class="model-info-card">
        <div class="model-info-title">Model Information</div>
        <div class="model-info-row">Random Forest Regressor</div>
        <div class="model-info-row">7 Input Features</div>
        <div class="model-info-row">R&sup2; Score: {R2_SCORE * 100:.2f}%</div>
    </div>
    """)

# ==================================================
# HEADER
# ==================================================
render_html(f"""
<div class="dashboard-header-row">
    <div>
        <div class="dashboard-title">Insurance Predictor</div>
        <div class="dashboard-subtitle">Estimate medical insurance charges from personal health information</div>
    </div>
</div>
""")

# ==================================================
# DASHBOARD PAGE
# ==================================================
if page == "Dashboard":

    # ---- Top metric cards ----
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_html("""
        <div class="metric-card">
            <div class="metric-label">BEST MODEL</div>
            <div class="metric-value">Random Forest</div>
            <div class="metric-desc">Selected regression model</div>
        </div>
        """)
    with c2:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-label">R&sup2; SCORE</div>
            <div class="metric-value">{R2_SCORE * 100:.2f}%</div>
            <div class="metric-desc">Test set performance</div>
        </div>
        """)
    with c3:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-label">MAE</div>
            <div class="metric-value">₹{MAE:,.2f}</div>
            <div class="metric-desc">Mean absolute error</div>
        </div>
        """)
    with c4:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-label">RMSE</div>
            <div class="metric-value">₹{RMSE:,.2f}</div>
            <div class="metric-desc">Root mean squared error</div>
        </div>
        """)

    # ---- Prediction section ----
    render_html("""
    <div class="section-title">Insurance Cost Prediction</div>
    <div class="section-subtitle">Enter the individual details below to estimate the insurance charge.</div>
    """)

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
        bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=28.5, step=0.1)
        smoking_status = st.selectbox("Smoking Status", ["No", "Yes"])
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        children = st.number_input("Number of Children", min_value=0, max_value=10, value=0, step=1)
        region = st.selectbox("Region", ["Northeast", "Northwest", "Southeast", "Southwest"])

    # ---- Derived values ----
    is_female = 1 if gender == "Female" else 0
    is_smoker = 1 if smoking_status == "Yes" else 0
    region_southeast = 1 if region == "Southeast" else 0
    bmi_category = get_bmi_category(bmi)
    bmi_obese = 1 if bmi >= 30 else 0
    smoker_label = "Smoker" if is_smoker == 1 else "Non-smoker"

    # ---- Health profile card ----
    render_html(f"""
    <div class="health-card">
        <div class="health-title">Health Profile</div>
        <div class="health-subtitle">Summary based on the entered information</div>
        <div class="health-grid">
            <div>
                <div class="health-item-label">AGE</div>
                <div class="health-item-value">{age} years</div>
            </div>
            <div>
                <div class="health-item-label">BMI</div>
                <div class="health-item-value">{bmi:.1f}</div>
            </div>
            <div>
                <div class="health-item-label">BMI CATEGORY</div>
                <div class="bmi-badge">{bmi_category}</div>
            </div>
            <div>
                <div class="health-item-label">SMOKING STATUS</div>
                <div class="health-item-value">{smoker_label}</div>
            </div>
        </div>
    </div>
    """)

    # ---- Predict button ----
    predict_clicked = st.button("Predict Insurance Charge")

    if predict_clicked:
        input_data = pd.DataFrame({
            "age": [age],
            "is_Female": [is_female],
            "bmi": [bmi],
            "children": [children],
            "is_smoker": [is_smoker],
            "region_southeast": [region_southeast],
            "bmi_category_Obese": [bmi_obese]
        })[FEATURE_ORDER]

        prediction = model.predict(input_data)[0]
        st.session_state.last_prediction = prediction

        st.session_state.history.append({
            "Age": age,
            "Gender": gender,
            "BMI": bmi,
            "Children": children,
            "Smoker": smoking_status,
            "Region": region,
            "Predicted Charge (₹)": round(float(prediction), 2)
        })

    if st.session_state.last_prediction is not None:
        render_html(f"""
        <div id="prediction-result" class="result-card">
            <div class="result-label">ESTIMATED INSURANCE CHARGE</div>
            <div class="result-value">₹{st.session_state.last_prediction:,.2f}</div>
            <div class="result-subtitle">Estimated medical insurance charge based on the information provided.</div>
        </div>
        """)

        if predict_clicked:
            components.html(
                """
                <script>
                    var doc = window.parent.document;
                    var target = doc.getElementById('prediction-result');
                    if (target) {
                        target.scrollIntoView({behavior: 'smooth', block: 'center'});
                    }
                </script>
                """,
                height=0,
            )

# ==================================================
# PREDICTION HISTORY PAGE
# ==================================================
elif page == "Prediction History":
    render_html("""
    <div class="section-title">Prediction History</div>
    <div class="section-subtitle">All predictions made during this session</div>
    """)

    if len(st.session_state.history) == 0:
        render_html("""
        <div class="empty-state-card">
            <div class="empty-state-title">NO PREDICTIONS YET</div>
            <div class="empty-state-sub">Make your first prediction from the Dashboard.</div>
        </div>
        """)
    else:
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df, use_container_width=True, hide_index=True)

# ==================================================
# MODEL ANALYTICS PAGE
# ==================================================
elif page == "Model Analytics":
    render_html("""
    <div class="section-title">Model Analytics</div>
    <div class="section-subtitle">Performance metrics and feature importance for the trained model</div>
    """)

    a1, a2, a3 = st.columns(3)
    with a1:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-label">R&sup2; SCORE</div>
            <div class="metric-value">{R2_SCORE * 100:.2f}%</div>
            <div class="metric-desc">Test set performance</div>
        </div>
        """)
    with a2:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-label">MAE</div>
            <div class="metric-value">₹{MAE:,.2f}</div>
            <div class="metric-desc">Mean absolute error</div>
        </div>
        """)
    with a3:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-label">RMSE</div>
            <div class="metric-value">₹{RMSE:,.2f}</div>
            <div class="metric-desc">Root mean squared error</div>
        </div>
        """)

    render_html("""
    <div class="section-title">Feature Importance</div>
    <div class="section-subtitle">Relative contribution of each feature to the model's predictions</div>
    """)

    importances = model.feature_importances_
    fi_df = pd.DataFrame({
        "feature": FEATURE_ORDER,
        "importance": importances
    }).sort_values("importance", ascending=False)

    max_importance = fi_df["importance"].max() if len(fi_df) > 0 else 1.0

    row_blocks = []
    for _, row in fi_df.iterrows():
        pct_of_max = (row["importance"] / max_importance) * 100 if max_importance > 0 else 0
        row_blocks.append(
            '<div class="fi-row">'
            '<div class="fi-row-top">'
            f'<span class="fi-row-name">{row["feature"]}</span>'
            f'<span class="fi-row-val">{row["importance"]:.4f}</span>'
            '</div>'
            '<div class="fi-bar-bg">'
            f'<div class="fi-bar-fill" style="width:{pct_of_max:.2f}%;"></div>'
            '</div>'
            '</div>'
        )
    rows_html = "".join(row_blocks)

    st.markdown(
        f'<div class="fi-row-wrap">{rows_html}</div>',
        unsafe_allow_html=True
    )
