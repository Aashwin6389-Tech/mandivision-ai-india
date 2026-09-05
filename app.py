import streamlit as st
import pandas as pd
import numpy as np
import hashlib

from math import radians, sin, cos, sqrt, atan2
from sklearn.linear_model import LinearRegression
from streamlit_js_eval import get_geolocation
from deep_translator import GoogleTranslator
from streamlit_mic_recorder import speech_to_text


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MandiVision AI India",
    page_icon="🌾",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* =========================================================
   🌾 MANDIVISION AI - PREMIUM FARMER THEME
   ========================================================= */

/* Main agriculture background */
.stApp {
    background-image:
        linear-gradient(
            rgba(236, 248, 232, 0.48),
            rgba(236, 248, 232, 0.48)
        ),
        url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=2200&q=90");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}


/* Main content area */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}


/* =========================================================
   🌾 TITLE
   ========================================================= */

.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 900;
    color: #166534;
    letter-spacing: 0.5px;
    text-shadow: 1px 2px 4px rgba(255,255,255,0.9);
}


/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #374151;
    margin-bottom: 20px;
    font-weight: 600;
}


/* =========================================================
   🧊 GLASS EFFECT FOR STREAMLIT CONTENT
   ========================================================= */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.32);
    border-radius: 18px;
}


/* =========================================================
   🎛️ INPUT BOXES
   ========================================================= */

div[data-baseweb="select"] > div,
div[data-testid="stNumberInput"] > div {
    background: rgba(255, 255, 255, 0.92);
    border-radius: 10px;
}


/* =========================================================
   🚀 BUTTONS
   ========================================================= */

.stButton > button {
    width: 100%;
    border-radius: 12px;
    min-height: 46px;
    font-weight: 800;
    border: 1px solid rgba(34, 139, 34, 0.25);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 7px 18px rgba(0,0,0,0.13);
}


/* =========================================================
   📊 TABLES
   ========================================================= */

div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 4px 14px rgba(0,0,0,0.07);
}


/* =========================================================
   📈 CHART AREA
   ========================================================= */

div[data-testid="stArrowVegaLiteChart"],
div[data-testid="stVegaLiteChart"] {
    background: rgba(255,255,255,0.72);
    border-radius: 16px;
    padding: 10px;
}


/* =========================================================
   🧑‍🌾 HEADERS
   ========================================================= */

h1, h2, h3 {
    font-weight: 800;
    color: #14532d;
}


/* =========================================================
   📍 INFO / SUCCESS / WARNING BOXES
   ========================================================= */

div[data-testid="stAlert"] {
    border-radius: 14px;
}


/* =========================================================
   🌿 SIDEBAR - FARM IMAGE
   ========================================================= */

section[data-testid="stSidebar"] {
    background-image:
        linear-gradient(
            rgba(220, 245, 220, 0.55),
            rgba(220, 245, 220, 0.55)
        ),
        url("https://images.unsplash.com/photo-1499529112087-3cb3b73cec95?auto=format&fit=crop&w=1200&q=85");

    background-size: cover;
    background-position: center;
}


/* =========================================================
   📱 MOBILE RESPONSIVE
   ========================================================= */

@media (max-width: 768px) {

    .main-title {
        font-size: 30px;
    }

    .subtitle {
        font-size: 15px;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LANGUAGES
# =========================================================

LANGUAGES = {
    "🇬🇧 English": "en",
    "🇮🇳 हिन्दी (Hindi)": "hi",
    "বাংলা (Bengali)": "bn",
    "తెలుగు (Telugu)": "te",
    "मराठी (Marathi)": "mr",
    "தமிழ் (Tamil)": "ta",
    "ગુજરાતી (Gujarati)": "gu",
    "ಕನ್ನಡ (Kannada)": "kn",
    "മലയാളം (Malayalam)": "ml",
    "ਪੰਜਾਬੀ (Punjabi)": "pa",
    "ଓଡ଼ିଆ (Odia)": "or",
    "অসমীয়া (Assamese)": "as",
    "اردو (Urdu)": "ur",
    "नेपाली (Nepali)": "ne"
}


# =========================================================
# SESSION STATE
# =========================================================

if "selected_crop" not in st.session_state:
    st.session_state.selected_crop = "Wheat"

if "farmer_lat" not in st.session_state:
    st.session_state.farmer_lat = None

if "farmer_lon" not in st.session_state:
    st.session_state.farmer_lon = None


# =========================================================
# LANGUAGE + VOICE
# =========================================================

top1, top2 = st.columns([2, 1])

with top1:
    selected_language = st.selectbox(
        "🌐 Language / भाषा",
        list(LANGUAGES.keys())
    )
    language_code = LANGUAGES[selected_language]

with top2:
    st.write("### 🎤 Voice Input")

    voice_text = speech_to_text(
        language=language_code,
        start_prompt="🎤 Speak",
        stop_prompt="⏹ Stop",
        just_once=True,
        use_container_width=True,
        key="voice_input"
    )


# =========================================================
# TRANSLATION
# =========================================================

@st.cache_data(show_spinner=False)
def translate_text(text, lang):

    if lang == "en":
        return text

    try:
        return GoogleTranslator(
            source="auto",
            target=lang
        ).translate(text)

    except Exception:
        return text


def T(text):
    return translate_text(text, language_code)


# =========================================================
# CROPS
# =========================================================

CROPS = [
    "Wheat",
    "Rice",
    "Maize",
    "Potato",
    "Tomato",
    "Onion",
    "Soybean",
    "Mustard",
    "Cotton"
]


# =========================================================
# VOICE CROP DETECTION
# =========================================================

if voice_text:

    st.success(f"🎤 You said: {voice_text}")

    voice_lower = voice_text.lower()

    crop_keywords = {
        "wheat": "Wheat",
        "गेहूं": "Wheat",
        "गेहूँ": "Wheat",

        "rice": "Rice",
        "धान": "Rice",
        "चावल": "Rice",

        "maize": "Maize",
        "corn": "Maize",
        "मक्का": "Maize",

        "potato": "Potato",
        "आलू": "Potato",

        "tomato": "Tomato",
        "टमाटर": "Tomato",

        "onion": "Onion",
        "प्याज": "Onion",

        "soybean": "Soybean",
        "सोयाबीन": "Soybean",

        "mustard": "Mustard",
        "सरसों": "Mustard",

        "cotton": "Cotton",
        "कपास": "Cotton"
    }

    for keyword, detected_crop in crop_keywords.items():
        if keyword.lower() in voice_lower:
            st.session_state.selected_crop = detected_crop
            break


# =========================================================
# INDIA MANDI DATABASE
# =========================================================

@st.cache_data
def create_india_mandi_data():

    data = [

        ["Lucknow Mandi", "Uttar Pradesh", 26.8467, 80.9462],
        ["Kanpur Mandi", "Uttar Pradesh", 26.4499, 80.3319],
        ["Varanasi Mandi", "Uttar Pradesh", 25.3176, 82.9739],
        ["Agra Mandi", "Uttar Pradesh", 27.1767, 78.0081],
        ["Meerut Mandi", "Uttar Pradesh", 28.9845, 77.7064],
        ["Prayagraj Mandi", "Uttar Pradesh", 25.4358, 81.8463],
        ["Gorakhpur Mandi", "Uttar Pradesh", 26.7606, 83.3732],

        ["Azadpur Mandi", "Delhi", 28.7041, 77.1025],

        ["Karnal Mandi", "Haryana", 29.6857, 76.9905],
        ["Hisar Mandi", "Haryana", 29.1492, 75.7217],

        ["Amritsar Mandi", "Punjab", 31.6340, 74.8723],
        ["Ludhiana Mandi", "Punjab", 30.9010, 75.8573],
        ["Patiala Mandi", "Punjab", 30.3398, 76.3869],

        ["Jaipur Mandi", "Rajasthan", 26.9124, 75.7873],
        ["Kota Mandi", "Rajasthan", 25.2138, 75.8648],
        ["Jodhpur Mandi", "Rajasthan", 26.2389, 73.0243],

        ["Indore Mandi", "Madhya Pradesh", 22.7196, 75.8577],
        ["Bhopal Mandi", "Madhya Pradesh", 23.2599, 77.4126],
        ["Jabalpur Mandi", "Madhya Pradesh", 23.1815, 79.9864],

        ["Mumbai APMC", "Maharashtra", 19.0760, 72.8777],
        ["Pune Mandi", "Maharashtra", 18.5204, 73.8567],
        ["Nagpur Mandi", "Maharashtra", 21.1458, 79.0882],
        ["Nashik Mandi", "Maharashtra", 19.9975, 73.7898],

        ["Ahmedabad Mandi", "Gujarat", 23.0225, 72.5714],
        ["Surat Mandi", "Gujarat", 21.1702, 72.8311],

        ["Patna Mandi", "Bihar", 25.5941, 85.1376],
        ["Gaya Mandi", "Bihar", 24.7914, 84.9994],

        ["Kolkata Market", "West Bengal", 22.5726, 88.3639],
        ["Siliguri Mandi", "West Bengal", 26.7271, 88.3953],

        ["Ranchi Mandi", "Jharkhand", 23.3441, 85.3096],
        ["Bhubaneswar Mandi", "Odisha", 20.2961, 85.8245],
        ["Raipur Mandi", "Chhattisgarh", 21.2514, 81.6296],

        ["Bengaluru Mandi", "Karnataka", 12.9716, 77.5946],
        ["Mysuru Mandi", "Karnataka", 12.2958, 76.6394],

        ["Chennai Market", "Tamil Nadu", 13.0827, 80.2707],
        ["Coimbatore Mandi", "Tamil Nadu", 11.0168, 76.9558],

        ["Hyderabad Mandi", "Telangana", 17.3850, 78.4867],
        ["Vijayawada Mandi", "Andhra Pradesh", 16.5062, 80.6480],

        ["Kochi Market", "Kerala", 9.9312, 76.2673],
        ["Guwahati Mandi", "Assam", 26.1445, 91.7362],
        ["Dehradun Mandi", "Uttarakhand", 30.3165, 78.0322]
    ]

    return pd.DataFrame(
        data,
        columns=["Mandi", "State", "Latitude", "Longitude"]
    )


# =========================================================
# DEMO BASE PRICES
# =========================================================

BASE_PRICES = {
    "Wheat": 2600,
    "Rice": 3200,
    "Maize": 2300,
    "Potato": 1800,
    "Tomato": 2500,
    "Onion": 2200,
    "Soybean": 4500,
    "Mustard": 5500,
    "Cotton": 6800
}


# =========================================================
# DISTANCE FUNCTION
# =========================================================

def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


# =========================================================
# DEMO PRICE GENERATION
# =========================================================

def generate_market_price(crop, mandi):

    base = BASE_PRICES[crop]

    text = crop + "_" + mandi

    hash_value = hashlib.md5(text.encode()).hexdigest()

    number = int(hash_value[:8], 16)

    variation = (number % 700) - 350

    return round(base + variation, 2)


# =========================================================
# AI PRICE PREDICTION
# =========================================================

def predict_price(current_price):

    days = np.arange(1, 31)

    np.random.seed(int(current_price) % 1000)

    trend = np.linspace(-40, 60, 30)
    noise = np.random.normal(0, 50, 30)

    prices = current_price + trend + noise

    X = pd.DataFrame({"Day": days})

    model = LinearRegression()
    model.fit(X, prices)

    future = pd.DataFrame({"Day": [37]})

    prediction = model.predict(future)[0]

    return round(prediction, 2)



# =========================================================
# PRICE TREND DATA GENERATION
# =========================================================

@st.cache_data
def generate_price_history(crop, days_count):

    base_price = BASE_PRICES[crop]

    # Consistent demo historical data for each crop and period
    seed_value = sum(ord(char) for char in crop) + days_count
    rng = np.random.default_rng(seed_value)

    dates = pd.date_range(
        end=pd.Timestamp.today().normalize(),
        periods=days_count
    )

    trend_strength = {
        "Wheat": 80,
        "Rice": 50,
        "Maize": -30,
        "Potato": 40,
        "Tomato": 120,
        "Onion": -70,
        "Soybean": 60,
        "Mustard": 90,
        "Cotton": 30
    }

    trend = trend_strength.get(crop, 40)

    price_trend = np.linspace(
        -trend / 2,
        trend / 2,
        days_count
    )

    noise = rng.normal(
        0,
        base_price * 0.025,
        days_count
    )

    prices = base_price + price_trend + noise

    return pd.DataFrame({
        "Date": dates,
        "Price": prices.round(2)
    })


# =========================================================
# PRICE TREND ANALYSIS
# =========================================================

def analyze_price_trend(history_df):

    first_price = history_df["Price"].iloc[0]
    current_price = history_df["Price"].iloc[-1]

    change = current_price - first_price
    change_percent = (change / first_price) * 100

    if change_percent > 2:
        trend_status = "📈 Increasing"
        advice = (
            "Prices are showing an upward trend. If you do not need "
            "immediate cash, monitoring the market for a better selling "
            "opportunity may be useful."
        )

    elif change_percent < -2:
        trend_status = "📉 Decreasing"
        advice = (
            "Prices are showing a downward trend. Consider selling sooner "
            "if the downward trend continues."
        )

    else:
        trend_status = "➖ Stable"
        advice = (
            "Prices are relatively stable. Compare nearby mandis before "
            "making a selling decision."
        )

    return trend_status, change, change_percent, advice


# =========================================================
# HEADER
# =========================================================

st.markdown(
    f'<div class="main-title">🌾 MandiVision AI India 🇮🇳</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">{T("Smart Mandi Price and Farmer Decision Support System")}</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# FARMER DETAILS
# =========================================================

st.header(T("👨‍🌾 Farmer Details"))

col1, col2 = st.columns(2)

with col1:

    crop = st.selectbox(
        T("🌾 Select Your Crop"),
        CROPS,
        index=CROPS.index(st.session_state.selected_crop)
    )

with col2:

    quantity = st.number_input(
        T("📦 Quantity (Quintal)"),
        min_value=1,
        value=10,
        step=1
    )


# =========================================================
# LOCATION
# =========================================================

st.divider()

st.header(T("📍 Your Location"))

st.info(
    T("Click the button and allow browser location permission.")
)

location = get_geolocation()


if st.button(
    T("📍 Enable My Current Location"),
    use_container_width=True
):

    if location:

        try:
            st.session_state.farmer_lat = location["coords"]["latitude"]
            st.session_state.farmer_lon = location["coords"]["longitude"]

            st.success(T("✅ Location enabled successfully!"))

        except Exception:
            st.warning(T("Please allow location permission and try again."))

    else:
        st.warning(T("Please allow location permission in your browser."))


# =========================================================
# LOCATION STATUS
# =========================================================

if (
    st.session_state.farmer_lat is not None
    and st.session_state.farmer_lon is not None
):

    st.success(T("🟢 Live location is ready!"))

else:

    st.warning(
        T("🔴 Enable location before analyzing nearby mandis.")
    )


# =========================================================
# ANALYZE BUTTON
# =========================================================

st.divider()

analyze = st.button(
    T("🚀 ANALYZE NEARBY MANDIS"),
    use_container_width=True
)


if analyze:

    farmer_lat = st.session_state.farmer_lat
    farmer_lon = st.session_state.farmer_lon


    if farmer_lat is None or farmer_lon is None:

        st.error(T("❌ Please enable your current location first."))
        st.stop()


    mandi_df = create_india_mandi_data().copy()


    mandi_df["Distance_km"] = mandi_df.apply(
        lambda row: calculate_distance(
            farmer_lat,
            farmer_lon,
            row["Latitude"],
            row["Longitude"]
        ),
        axis=1
    )


    nearby = mandi_df.sort_values("Distance_km").head(10).copy()


    results = []


    for _, row in nearby.iterrows():

        mandi = row["Mandi"]

        current_price = generate_market_price(crop, mandi)

        predicted_price = predict_price(current_price)

        transport_cost = row["Distance_km"] * quantity * 0.50

        predicted_revenue = predicted_price * quantity

        net_return = predicted_revenue - transport_cost


        results.append({

            "Mandi": mandi,
            "State": row["State"],
            "Distance_km": row["Distance_km"],
            "Current_Price": current_price,
            "Predicted_Price": predicted_price,
            "Transport_Cost": transport_cost,
            "Expected_Net_Return": net_return

        })


    result = pd.DataFrame(results)


    result = result.sort_values(
        "Expected_Net_Return",
        ascending=False
    ).reset_index(drop=True)


    # =====================================================
    # NEAREST MANDIS
    # =====================================================

    st.divider()

    st.header(T("📍 Nearest Mandis"))

    nearest_display = nearby[
        ["Mandi", "State", "Distance_km"]
    ].copy()

    nearest_display["Distance_km"] = (
        nearest_display["Distance_km"].round(2)
    )

    st.dataframe(
        nearest_display,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # MANDI COMPARISON
    # =====================================================

    st.divider()

    st.header(T("📊 Smart Mandi Comparison"))

    display_result = result.copy()

    for col in [
        "Distance_km",
        "Current_Price",
        "Predicted_Price",
        "Transport_Cost",
        "Expected_Net_Return"
    ]:
        display_result[col] = display_result[col].round(2)


    st.dataframe(
        display_result,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # CHART
    # =====================================================

    st.divider()

    st.header(T("📊 Price Comparison"))

    chart_data = result.set_index("Mandi")[
        ["Current_Price", "Predicted_Price"]
    ]

    st.bar_chart(chart_data)


    # =====================================================
    # TOP 3
    # =====================================================

    st.divider()

    st.header(T("🏆 Top 3 Recommended Mandis"))

    medals = ["🥇", "🥈", "🥉"]

    for i, (_, row) in enumerate(result.head(3).iterrows()):

        st.subheader(f"{medals[i]} {row['Mandi']}")

        a, b, c = st.columns(3)

        a.metric(
            T("Distance"),
            f"{row['Distance_km']:.1f} km"
        )

        b.metric(
            T("Price"),
            f"₹{row['Current_Price']:,.0f}"
        )

        c.metric(
            T("Expected Return"),
            f"₹{row['Expected_Net_Return']:,.0f}"
        )


    # =====================================================
    # FINAL AI RECOMMENDATION
    # =====================================================

    best = result.iloc[0]

    difference = (
        best["Predicted_Price"]
        - best["Current_Price"]
    )


    if difference > 50:

        decision = "WAIT FOR BETTER PRICE"
        reason = "AI predicts that the market price may increase."

    else:

        decision = "SELL NOW"
        reason = "Current market conditions are favorable."


    st.divider()

    st.header(T("🤖 FINAL AI RECOMMENDATION"))


    st.success(f"""
### 🌾 {T(decision)}

## 🏪 {best["Mandi"]}

📍 **{T("State")}:** {best["State"]}

📏 **{T("Distance")}:** {best["Distance_km"]:.1f} km

🌾 **{T("Crop")}:** {crop}

📦 **{T("Quantity")}:** {quantity} Quintal

💰 **{T("Current Price")}:** ₹{best["Current_Price"]:,.0f} / Quintal

🤖 **{T("Predicted Price")}:** ₹{best["Predicted_Price"]:,.0f} / Quintal

🚛 **{T("Transport Cost")}:** ₹{best["Transport_Cost"]:,.0f}

🏆 **{T("Expected Net Return")}:** ₹{best["Expected_Net_Return"]:,.0f}

---

🧠 **{T("AI Reason")}**

{T(reason)}
""")



# =========================================================
# PRICE TREND DASHBOARD
# =========================================================

st.divider()

st.header(T("📈 Price Trend Dashboard"))

st.info(
    T(
        "Track historical price trends and understand whether market prices "
        "are increasing, decreasing or stable."
    )
)

trend_col1, trend_col2 = st.columns(2)

with trend_col1:
    trend_crop = st.selectbox(
        T("🌾 Select Crop for Trend Analysis"),
        CROPS,
        index=CROPS.index(crop),
        key="trend_crop"
    )

with trend_col2:
    trend_period = st.selectbox(
        T("📅 Select Time Period"),
        [7, 15, 30],
        format_func=lambda x: f"Last {x} Days",
        key="trend_period"
    )

history_df = generate_price_history(
    trend_crop,
    trend_period
)

(
    trend_status,
    price_change,
    change_percent,
    trend_advice
) = analyze_price_trend(history_df)

current_trend_price = history_df["Price"].iloc[-1]
highest_price = history_df["Price"].max()
lowest_price = history_df["Price"].min()
average_price = history_df["Price"].mean()

st.subheader(T("📊 Market Price Statistics"))

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    T("💰 Current Price"),
    f"₹{current_trend_price:,.0f}"
)

metric2.metric(
    T("⬆️ Highest Price"),
    f"₹{highest_price:,.0f}"
)

metric3.metric(
    T("⬇️ Lowest Price"),
    f"₹{lowest_price:,.0f}"
)

metric4.metric(
    T("📊 Average Price"),
    f"₹{average_price:,.0f}"
)

st.divider()

change_col1, change_col2 = st.columns(2)

with change_col1:
    st.metric(
        T("📈 Price Change"),
        f"₹{price_change:,.2f}",
        f"{change_percent:.2f}%"
    )

with change_col2:
    st.metric(
        T("🤖 Trend Status"),
        trend_status
    )

st.divider()

st.subheader(T("📈 Historical Price Trend"))

chart_df = history_df.set_index("Date")
st.line_chart(
    chart_df["Price"],
    use_container_width=True
)

st.divider()

st.subheader(T("📋 Historical Price Data"))

display_history = history_df.copy()
display_history["Date"] = (
    display_history["Date"].dt.strftime("%d %b %Y")
)
display_history["Price"] = display_history["Price"].round(2)

st.dataframe(
    display_history,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader(T("🧠 Smart Market Insight"))

if change_percent > 2:
    st.success(f"""
### 📈 {T("PRICE TREND: INCREASING")}

🌾 **{trend_crop}**

💰 **{T("Current Price")}:** ₹{current_trend_price:,.0f} / Quintal

📊 **{T("Price Change")}:** {change_percent:.2f}%

💡 **{T("Market Insight")}**

{T(trend_advice)}
""")

elif change_percent < -2:
    st.warning(f"""
### 📉 {T("PRICE TREND: DECREASING")}

🌾 **{trend_crop}**

💰 **{T("Current Price")}:** ₹{current_trend_price:,.0f} / Quintal

📊 **{T("Price Change")}:** {change_percent:.2f}%

💡 **{T("Market Insight")}**

{T(trend_advice)}
""")

else:
    st.info(f"""
### ➖ {T("PRICE TREND: STABLE")}

🌾 **{trend_crop}**

💰 **{T("Current Price")}:** ₹{current_trend_price:,.0f} / Quintal

📊 **{T("Price Change")}:** {change_percent:.2f}%

💡 **{T("Market Insight")}**

{T(trend_advice)}
""")


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🇮🇳 MandiVision AI | Smart Agriculture Decision Support System"
)

