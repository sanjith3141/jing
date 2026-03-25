import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="RegretAI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0B0F19 0%, #111827 100%);
        background-attachment: fixed;
        color: #F3F4F6;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: transparent;
    }
    
    .main {
        background-color: transparent;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* HERO CARD */
    .hero-card {
        background: linear-gradient(135deg, rgba(21, 27, 40, 0.8) 0%, rgba(11, 15, 25, 0.9) 100%);
        border: 1px solid rgba(0, 229, 255, 0.15);
        border-radius: 26px;
        padding: 42px 26px;
        text-align: center;
        margin: 42px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
    }
    
    .hero-title {
        font-size: 2.618em;
        font-weight: 700;
        color: #00E5FF;
        margin: 0;
        letter-spacing: -0.5px;
        text-shadow: 0 0 20px rgba(0, 229, 255, 0.3);
    }
    
    .hero-subtitle {
        font-size: 1em;
        color: #94A3B8;
        margin-top: 16px;
        font-weight: 400;
        letter-spacing: 0.5px;
    }

    /* STREAMLIT CONTAINERS */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #151B28 !important;
        border: 1px solid rgba(0, 229, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 26px !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(0, 229, 255, 0.3) !important;
        box-shadow: 0 8px 26px rgba(0, 229, 255, 0.08) !important;
    }
    
    /* SECTION HEADERS */
    .section-header {
        font-size: 1.618em;
        font-weight: 600;
        color: #F3F4F6;
        margin-bottom: 26px;
        margin-top: 0;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    /* INPUT LABELS & HINTS */
    .input-label {
        font-size: 0.85em;
        font-weight: 600;
        color: #00E5FF;
        margin-bottom: 12px;
        display: block;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .input-hint {
        font-size: 0.8em;
        color: #94A3B8;
        margin-top: 6px;
        display: block;
    }
    
    /* CUSTOM SLIDER STYLING */
    .slider-container {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .slider-wrapper {
        flex: 1;
    }
    
    .slider-value-box {
        background: rgba(0, 229, 255, 0.1);
        border: 1px solid rgba(0, 229, 255, 0.3);
        border-radius: 8px;
        padding: 8px 14px;
        min-width: 50px;
        text-align: center;
        font-weight: 600;
        color: #00E5FF;
        font-size: 0.95em;
    }
    
    /* Slider track styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(to right, rgba(148, 163, 184, 0.2), rgba(0, 229, 255, 0.4)) !important;
        height: 7px !important;
        border-radius: 4px !important;
    }
    
    /* Slider thumb (ball) styling */
    .stSlider > div > div > div > div > div {
        background: linear-gradient(135deg, #00E5FF 0%, #33EAFF 100%) !important;
        width: 18px !important;
        height: 18px !important;
        border-radius: 50% !important;
        box-shadow: 0 0 8px rgba(0, 229, 255, 0.5), inset 0 0 4px rgba(255, 255, 255, 0.2) !important;
        border: 2px solid rgba(0, 229, 255, 0.6) !important;
        transition: all 0.1s ease-out !important;
        cursor: grab !important;
    }
    
    /* Slider thumb on hover and active */
    .stSlider > div > div > div > div > div:hover,
    .stSlider > div > div > div > div > div:active {
        width: 22px !important;
        height: 22px !important;
        box-shadow: 0 0 16px rgba(0, 229, 255, 0.8), inset 0 0 6px rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Slider container */
    .stSlider {
        padding: 12px 0 !important;
    }
    
    /* CHOICE BUTTONS */
    .stButton > button {
        width: 100%;
        background: rgba(21, 27, 40, 0.8);
        color: #94A3B8;
        border: 1.5px solid rgba(0, 229, 255, 0.2);
        border-radius: 10px;
        padding: 14px 16px;
        font-size: 0.9em;
        font-weight: 600;
        letter-spacing: 0.3px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        white-space: normal;
        word-wrap: break-word;
        min-height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .stButton > button:hover {
        border-color: #00E5FF;
        color: #00E5FF;
        box-shadow: 0 0 12px rgba(0, 229, 255, 0.3);
        transform: translateY(-2px);
        background: rgba(0, 229, 255, 0.08);
    }
    
    .stButton > button:active {
        background: rgba(0, 229, 255, 0.25);
        border-color: #00E5FF;
        color: #00E5FF;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.5);
        animation: chosenPulse 0.5s ease-out;
    }
    
    /* MAIN CTA BUTTON */
    .cta-button > button {
        width: 100%;
        background: #00E5FF;
        color: #0B0F19;
        border: none;
        border-radius: 10px;
        padding: 16px 26px;
        font-size: 1.1em;
        font-weight: 700;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0, 229, 255, 0.3);
    }
    
    .cta-button > button:hover {
        background: #33EAFF;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 229, 255, 0.5);
    }
    
    /* NUMBER INPUT */
    .stNumberInput > div > div > input {
        background: #0B0F19 !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        color: #F3F4F6 !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #00E5FF !important;
        box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.2) !important;
    }
    
    /* DROPDOWN SELECT */
    .stSelectbox > div > div > select {
        background: #0B0F19 !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        color: #F3F4F6 !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #00E5FF !important;
        box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.2) !important;
    }
    
    /* RESULT BOXES */
    .result-box {
        border-radius: 16px;
        padding: 26px;
        margin: 26px 0;
        background: #0B0F19;
        border: 1px solid;
        animation: slideInUp 0.5s ease-out;
    }
    
    .result-safe { 
        border-color: rgba(0, 229, 255, 0.5); 
        box-shadow: inset 0 0 20px rgba(0, 229, 255, 0.05);
    }
    
    .result-warning { 
        border-color: rgba(251, 191, 36, 0.5); 
        box-shadow: inset 0 0 20px rgba(251, 191, 36, 0.05);
    }
    
    .result-danger { 
        border-color: rgba(239, 68, 68, 0.5); 
        box-shadow: inset 0 0 20px rgba(239, 68, 68, 0.05);
    }
    
    .result-title {
        font-weight: 700;
        font-size: 1.618em;
        margin: 0 0 10px 0;
    }
    
    .advice-box {
        background: rgba(11, 15, 25, 0.8);
        border-left: 3px solid #00E5FF;
        border-radius: 8px;
        padding: 16px 26px;
        margin: 16px 0;
        font-size: 1em;
        color: #E2E8F0;
        animation: slideInLeft 0.5s ease-out;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes chosenPulse {
        0% {
            transform: scale(1);
            box-shadow: 0 0 20px rgba(0, 229, 255, 0.5);
        }
        50% {
            transform: scale(1.02);
            box-shadow: 0 0 30px rgba(0, 229, 255, 0.7);
        }
        100% {
            transform: scale(1);
            box-shadow: 0 0 16px rgba(0, 229, 255, 0.4);
        }
    }
    
    /* HIDE STREAMLIT ELEMENTS */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Initialize session state for button selections
if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = None
if "selected_urgency" not in st.session_state:
    st.session_state.selected_urgency = None
if "selected_brand" not in st.session_state:
    st.session_state.selected_brand = None
if "selected_peer" not in st.session_state:
    st.session_state.selected_peer = None

# Load model
@st.cache_resource
def load_model():
    try:
        return joblib.load("regret_model.pkl")
    except:
        class DummyModel:
            def predict_proba(self, X): return [[0.2, 0.65]]
            @property
            def feature_importances_(self): return np.random.rand(11)
        return DummyModel()

model = load_model()

# CUSTOM SLIDER COMPONENT
def custom_slider(label, min_val, max_val, default_val, key_name):
    """
    Custom slider with value display box beside it
    """
    col1, col2 = st.columns([4, 0.8])
    
    with col1:
        st.markdown(f'<label class="input-label">{label}</label>', unsafe_allow_html=True)
        slider_value = st.slider(
            label,
            min_value=min_val,
            max_value=max_val,
            value=default_val,
            label_visibility="collapsed",
            key=key_name
        )
    
    with col2:
        st.markdown('<label class="input-label" style="visibility: hidden;">Value</label>', unsafe_allow_html=True)
        st.markdown(f'<div class="slider-value-box">{slider_value}</div>', unsafe_allow_html=True)
    
    return slider_value

# HERO SECTION
st.markdown("""
<div class="hero-card">
    <h1 class="hero-title">RegretAI</h1>
    <p class="hero-subtitle">Mindful purchase decisions powered by intelligence</p>
</div>
""", unsafe_allow_html=True)

# FINANCIAL DETAILS SECTION
with st.container(border=True):
    st.markdown('<h2 class="section-header">Financial Details</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<label class="input-label">Product Price</label>', unsafe_allow_html=True)
        price = st.number_input("Product Price", min_value=0, step=100, label_visibility="collapsed", placeholder="Amount")
        st.markdown('<span class="input-hint">Total cost of item</span>', unsafe_allow_html=True)

    with col2:
        st.markdown('<label class="input-label">Monthly Income</label>', unsafe_allow_html=True)
        income = st.number_input("Monthly Income", min_value=0, step=1000, label_visibility="collapsed", placeholder="Income")
        st.markdown('<span class="input-hint">Your monthly earnings</span>', unsafe_allow_html=True)

    with col3:
        savings = custom_slider("Savings Rate (%)", 0, 50, 20, "savings_slider")
        st.markdown('<span class="input-hint">% of income saved</span>', unsafe_allow_html=True)

# BEHAVIOR SECTION
with st.container(border=True):
    st.markdown('<h2 class="section-header">Shopping Behavior</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        impulse = custom_slider("Impulsiveness Level", 1, 10, 5, "impulse_slider")
        st.markdown('<span class="input-hint">1 = Deliberate, 10 = Impulse</span>', unsafe_allow_html=True)

    with col2:
        research = custom_slider("Research Time (min)", 0, 60, 15, "research_slider")
        st.markdown('<span class="input-hint">Minutes spent researching</span>', unsafe_allow_html=True)

    with col3:
        st.markdown('<label class="input-label">Current Mood</label>', unsafe_allow_html=True)
        mood_options = ["Neutral", "Happy", "Stressed", "Excited"]
        mood_cols = st.columns(len(mood_options), gap="small")
        for idx, option in enumerate(mood_options):
            with mood_cols[idx]:
                if st.button(option, key=f"mood_{option}", use_container_width=True):
                    st.session_state.selected_mood = option
                    st.rerun()
        
        # Display selected mood
        if st.session_state.selected_mood:
            st.markdown(f'<p style="text-align: center; color: #00E5FF; font-weight: 600; margin-top: 8px;">Selected: {st.session_state.selected_mood}</p>', unsafe_allow_html=True)
        
        mood = st.session_state.selected_mood if st.session_state.selected_mood else "Neutral"

# PURCHASE CONTEXT SECTION
with st.container(border=True):
    st.markdown('<h2 class="section-header">Purchase Context</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        discount = custom_slider("Discount Offered (%)", 0, 60, 10, "discount_slider")
        st.markdown('<span class="input-hint">Discount percentage</span>', unsafe_allow_html=True)

    with col2:
        st.markdown('<label class="input-label">Urgency Level</label>', unsafe_allow_html=True)
        urgency_options = ["Low", "Medium", "High"]
        urgency_cols = st.columns(len(urgency_options), gap="small")
        for idx, option in enumerate(urgency_options):
            with urgency_cols[idx]:
                if st.button(option, key=f"urgency_{option}", use_container_width=True):
                    st.session_state.selected_urgency = option
                    st.rerun()
        
        # Display selected urgency
        if st.session_state.selected_urgency:
            st.markdown(f'<p style="text-align: center; color: #00E5FF; font-weight: 600; margin-top: 8px;">Selected: {st.session_state.selected_urgency}</p>', unsafe_allow_html=True)
        
        urgency = st.session_state.selected_urgency if st.session_state.selected_urgency else "Low"
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<label class="input-label">Brand Familiarity</label>', unsafe_allow_html=True)
        brand_options = ["Low", "Medium", "High"]
        brand_cols = st.columns(len(brand_options), gap="small")
        for idx, option in enumerate(brand_options):
            with brand_cols[idx]:
                if st.button(option, key=f"brand_{option}", use_container_width=True):
                    st.session_state.selected_brand = option
                    st.rerun()
        
        # Display selected brand
        if st.session_state.selected_brand:
            st.markdown(f'<p style="text-align: center; color: #00E5FF; font-weight: 600; margin-top: 8px;">Selected: {st.session_state.selected_brand}</p>', unsafe_allow_html=True)
        
        brand = st.session_state.selected_brand if st.session_state.selected_brand else "Low"

    with col4:
        st.markdown('<label class="input-label">Product Category</label>', unsafe_allow_html=True)
        category = st.selectbox(
            "Product Category",
            ["Electronics", "Clothing", "Food", "Home", "Accessories"],
            label_visibility="collapsed"
        )
    
    col5, col6, col7 = st.columns([1, 1, 1])
    
    with col6:
        st.markdown('<label class="input-label">Peer Influence</label>', unsafe_allow_html=True)
        peer_options = ["None", "Low", "High"]
        peer_cols = st.columns(len(peer_options), gap="small")
        for idx, option in enumerate(peer_options):
            with peer_cols[idx]:
                if st.button(option, key=f"peer_{option}", use_container_width=True):
                    st.session_state.selected_peer = option
                    st.rerun()
        
        # Display selected peer
        if st.session_state.selected_peer:
            st.markdown(f'<p style="text-align: center; color: #00E5FF; font-weight: 600; margin-top: 8px;">Selected: {st.session_state.selected_peer}</p>', unsafe_allow_html=True)
        
        peer = st.session_state.selected_peer if st.session_state.selected_peer else "None"

# CTA BUTTON
st.markdown('<div style="margin: 42px 0;"></div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1.618, 1])

with col2:
    st.markdown('<div class="cta-button">', unsafe_allow_html=True)
    predict = st.button("Analyze Purchase Decision", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# RESULTS SECTION
if predict:
    # Prepare input data - USE ACTUAL TRAINING DATA RANGES

    
    # TRAINING DATA RANGES (from dataset analysis)
    # Price: 209 - 49,926 (avg ~24,500)
    # Income: 10,163 - 149,892 (avg ~80,000)
    # These are used to keep predictions in realistic bounds
    
    # Create dataframe from UI inputs
    row = pd.DataFrame([{
    "Price": price,
    "Monthly_Income": income,
    "Savings_Percentage": savings,
    "Discount_Percentage": discount,
    "Mood": mood,
    "Urgency_Level": urgency,
    "Research_Time_Minutes": research,
    "Brand_Familiarity": brand,
    "Purchase_Category": category,
    "Peer_Influence": np.nan if peer == "None" else peer,
    "Impulsiveness_Score": impulse,
}])

# Add missing features
    row["Price_Income_Ratio"] = np.where(
    row["Monthly_Income"] == 0,
    0,
    row["Price"] / row["Monthly_Income"]
)

    row["Log_Price"] = np.log1p(row["Price"])
    row["Log_Income"] = np.log1p(row["Monthly_Income"])

# Encode using trained encoders
    for col in ["Mood", "Urgency_Level", "Brand_Familiarity", "Purchase_Category", "Peer_Influence"]:
        row[col] = encoders[col].transform(row[col].astype(str))

# Ensure correct feature order
    row = row[[
    "Price", "Monthly_Income", "Savings_Percentage", "Discount_Percentage",
    "Mood", "Urgency_Level", "Research_Time_Minutes", "Brand_Familiarity",
    "Purchase_Category", "Peer_Influence", "Impulsiveness_Score",
    "Price_Income_Ratio", "Log_Price", "Log_Income"
]]

# Scale input
    row_scaled = scaler.transform(row)

# Predict
    prob = model.predict_proba(row_scaled)[0][1]
    
    # Smooth scroll to results
    st.markdown("""
    <script>
        setTimeout(function() {
            window.scrollBy({top: 800, behavior: 'smooth'});
        }, 100);
    </script>
    """, unsafe_allow_html=True)
    
    # Analysis Container
    with st.container(border=True):
        st.markdown('<h2 class="section-header">Mindful Analysis</h2>', unsafe_allow_html=True)
        
        # Color based on probability
        if prob < 0.3:
            color = "#00E5FF"
        elif prob < 0.6:
            color = "#FBBF24"
        else:
            color = "#EF4444"
            
        # Animated gauge
        gauge_placeholder = st.empty()
        
        target_value = int(prob * 100)
        
        # Easing function for smooth animation
        def ease_out_cubic(t):
            return 1 - pow(1 - t, 3)
        
        for step in range(101):
            progress = step / 100
            eased_progress = ease_out_cubic(progress)
            current_value = int(target_value * eased_progress)
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=current_value,
                title={'text': "Regret Probability", 'font': {'size': 16, 'color': '#F3F4F6'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#F3F4F6'},
                    'bar': {'color': color, 'thickness': 0.8},
                    'steps': [
                        {'range': [0, 33], 'color': 'rgba(0, 229, 255, 0.05)'},
                        {'range': [33, 66], 'color': 'rgba(251, 191, 36, 0.05)'},
                        {'range': [66, 100], 'color': 'rgba(239, 68, 68, 0.05)'},
                    ],
                },
                number={'font': {'size': 42, 'color': color}, 'suffix': '%'}
            ))
            
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'family': "-apple-system, BlinkMacSystemFont", 'color': '#F3F4F6'},
                height=350,
                margin=dict(l=20, r=20, t=60, b=20)
            )
            
            gauge_placeholder.plotly_chart(fig, use_container_width=True, key=f"gauge_{step}")
            time.sleep(0.012)
        
        # Risk Assessment
        if prob > 0.6:
            st.markdown(f"""
            <div class="result-box result-danger">
                <p class="result-title" style="color: {color}">High Regret Risk</p>
                <p style="margin: 0; color: #E2E8F0;">It is highly recommended to pause on this purchase. Take a day to evaluate if this aligns with your goals.</p>
            </div>
            """, unsafe_allow_html=True)
        elif prob > 0.3:
            st.markdown(f"""
            <div class="result-box result-warning">
                <p class="result-title" style="color: {color}">Moderate Risk</p>
                <p style="margin: 0; color: #E2E8F0;">Consider the mindful recommendations below before making your final decision.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-box result-safe">
                <p class="result-title" style="color: {color}">Safe to Purchase</p>
                <p style="margin: 0; color: #E2E8F0;">This appears to be a well-considered and balanced decision.</p>
            </div>
            """, unsafe_allow_html=True)

    # Recommendations Container
    with st.container(border=True):
        st.markdown('<h2 class="section-header">Gentle Reminders</h2>', unsafe_allow_html=True)
        
        advice = []
        if price > income * 0.3:
            advice.append("Consider a more budget-friendly alternative to maintain financial peace.")
        if research < 5:
            advice.append("Take a few more minutes to read reviews or find alternatives.")
        if impulse > 7:
            advice.append("Implement the '24-hour rule' before finalizing this transaction.")
        if discount < 10:
            advice.append("There might be better deals available. Consider waiting for a sale.")
        if urgency == "High":
            advice.append("Remember that 'limited time' offers are often designed to bypass logical decision-making.")
            
        if len(advice) == 0:
            st.markdown('<div class="advice-box" style="border-left-color: #00E5FF;">Your decision-making process is well-balanced. Trust your judgment.</div>', unsafe_allow_html=True)
        else:
            for suggestion in advice:
                st.markdown(f'<div class="advice-box">{suggestion}</div>', unsafe_allow_html=True)

    # Save history
    new_data = pd.DataFrame([{
        "Timestamp": pd.Timestamp.now(),
        "Price": price,
        "Income": income,
        "Savings": savings,
        "Discount": discount,
        "Research": research,
        "Impulse": impulse,
        "Regret_Probability": prob
    }])
    
    if not os.path.exists("history.csv"):
        new_data.to_csv("history.csv", index=False)
    else:
        new_data.to_csv("history.csv", mode='a', header=False, index=False)
