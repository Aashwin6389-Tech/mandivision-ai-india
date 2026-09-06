
st = streamlit
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



/* Main content area */
.block-container {
    padding-top: 11rem !important;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* =========================================================
   🌾 FIXED PREMIUM HEADER - TITLE + SUBTITLE TOGETHER
   ========================================================= */

.mv-fixed-header {
    position: fixed;
    top: 2.75rem;
    left: 0;
    right: 0;
    width: 100%;
    z-index: 999999;
    text-align: center;
    padding: 8px 18px 10px 18px;
    box-sizing: border-box;
    background: linear-gradient(
        180deg,
        rgba(246, 252, 244, 0.99),
        rgba(255, 249, 226, 0.98)
    );
    border-bottom: 2px solid rgba(67, 111, 73, 0.16);
    box-shadow: 0 5px 18px rgba(50, 80, 45, 0.13);
    backdrop-filter: blur(12px);
}

.mv-fixed-header .main-title {
    position: static;
    width: auto;
    margin: 0;
    padding: 0;
    font-size: 42px;
    line-height: 1.08;
    font-weight: 900;
    color: #124b35 !important;
    letter-spacing: 0.2px;
    text-shadow: 0 1px 0 rgba(255,255,255,0.9);
}

.mv-fixed-header .subtitle {
    position: static;
    width: auto;
    margin: 5px 0 0 0;
    padding: 0;
    font-size: 17px;
    line-height: 1.25;
    font-weight: 800;
    color: #6b431f !important;
    background: transparent;
}

/* =========================================================
   🌾 CLEAN FARMER-FRIENDLY BACKGROUND
   ========================================================= */

.stApp {
    /* Clean, light agriculture-inspired background.
       No photograph is used, so text remains readable everywhere. */
    background:
        radial-gradient(circle at 12% 8%, rgba(214, 235, 199, 0.38) 0, rgba(214, 235, 199, 0) 24%),
        radial-gradient(circle at 88% 10%, rgba(250, 226, 177, 0.30) 0, rgba(250, 226, 177, 0) 25%),
        linear-gradient(135deg, #f7faf4 0%, #fbfaf3 50%, #fff8e9 100%) !important;
    background-attachment: fixed;
}

/* =========================================================
   🧑‍🌾 SECTION HEADERS
   ========================================================= */

h1, h2, h3 {
    font-weight: 900 !important;
    color: #124b35 !important;
    text-shadow: 0 1px 2px rgba(255,255,255,0.85);
}

[data-testid="stHeader"] {
    background: transparent;
}

/* Streamlit labels and normal text */
.stMarkdown, .stMarkdown *, .stText, label, [data-testid="stWidgetLabel"] {
    color: #163f2d !important;
}

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    color: #163f2d !important;
    font-weight: 800 !important;
}

/* Make success / warning / info text readable over the farm background */
div[data-testid="stAlert"] {
    background: rgba(255, 255, 255, 0.92) !important;
    border: 1px solid rgba(40, 90, 55, 0.16) !important;
    color: #174a32 !important;
}

div[data-testid="stAlert"] p,
div[data-testid="stAlert"] div,
div[data-testid="stAlert"] span {
    color: #174a32 !important;
}

/* =========================================================
   🧊 GLASS CARDS / CONTAINERS
   ========================================================= */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.78);
    border: 1px solid rgba(255, 255, 255, 0.75);
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(40, 70, 45, 0.10);
    backdrop-filter: blur(5px);
}

/* Horizontal blocks look more like sections */
div[data-testid="stHorizontalBlock"] {
    border-radius: 16px;
}

/* =========================================================
   🎛️ INPUT BOXES
   ========================================================= */

div[data-baseweb="select"] > div,
div[data-testid="stNumberInput"] > div {
    background: rgba(255, 255, 255, 0.96) !important;
    border: 2px solid rgba(22, 101, 52, 0.16);
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(30, 70, 40, 0.08);
}

div[data-baseweb="select"] *,
div[data-testid="stNumberInput"] * {
    color: #123f2b !important;
}

div[data-baseweb="select"] input {
    color: #123f2b !important;
}

div[role="listbox"] {
    background: #ffffff !important;
}

div[role="option"] {
    color: #123f2b !important;
    background: #ffffff !important;
}

div[role="option"]:hover {
    background: #eef7e9 !important;
}

/* =========================================================
   🚀 BUTTONS
   ========================================================= */

.stButton > button {
    width: 100%;
    min-height: 50px;
    border-radius: 13px;
    font-weight: 850;
    color: #123b2a !important;
    background: linear-gradient(135deg, #e8f5e9, #fff4d6) !important;
    border: 2px solid rgba(34, 139, 34, 0.20);
    box-shadow: 0 5px 15px rgba(30, 70, 40, 0.10);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 9px 22px rgba(30, 70, 40, 0.16);
    border-color: rgba(22, 101, 52, 0.35);
}

/* =========================================================
   💰 METRICS - ALWAYS HIGH CONTRAST
   ========================================================= */

[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.72) !important;
    border: 1px solid rgba(18, 75, 53, 0.10);
    border-radius: 16px;
    padding: 14px 16px !important;
    box-shadow: 0 5px 16px rgba(40, 70, 45, 0.06);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] * {
    color: #123f2b !important;
    opacity: 1 !important;
}

[data-testid="stMetricValue"] {
    font-weight: 900 !important;
    font-size: 2rem !important;
}

[data-testid="stMetricLabel"] {
    font-weight: 800 !important;
}

/* =========================================================
   📊 TABLES
   ========================================================= */

div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 7px 20px rgba(30, 70, 40, 0.10);
    background: rgba(255,255,255,0.90);
}

/* =========================================================
   📈 CHART AREA
   ========================================================= */

div[data-testid="stArrowVegaLiteChart"],
div[data-testid="stVegaLiteChart"] {
    background: rgba(255,255,255,0.88);
    border-radius: 16px;
    padding: 10px;
    box-shadow: 0 7px 20px rgba(30, 70, 40, 0.08);
}

/* =========================================================
   📍 INFO / SUCCESS / WARNING BOXES
   ========================================================= */

div[data-testid="stAlert"] {
    border-radius: 14px;
    box-shadow: 0 5px 16px rgba(30, 70, 40, 0.07);
}

/* =========================================================
   🌿 SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #eef7e8 0%, #fff7e5 100%) !important;
}

/* =========================================================
   ✨ DIVIDERS
   ========================================================= */

hr {
    border: 0;
    height: 2px;
    background: rgba(22, 101, 52, 0.15);
    margin: 1.4rem 0;
}

/* =========================================================
   📱 MOBILE RESPONSIVE
   ========================================================= */

@media (max-width: 768px) {

    .block-container {
        padding-top: 8.5rem !important;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    .mv-fixed-header {
        top: 2.65rem;
        padding: 7px 8px 9px 8px;
    }

    .mv-fixed-header .main-title {
        font-size: 27px;
    }

    .mv-fixed-header .subtitle {
        font-size: 13px;
        margin-top: 4px;
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

# Speech-recognition locales are kept separate from translation codes.
# This prevents the microphone component from receiving an unsupported locale.
SPEECH_LOCALES = {
    "en": "en-IN",
    "hi": "hi-IN",
    "bn": "bn-IN",
    "te": "te-IN",
    "mr": "mr-IN",
    "ta": "ta-IN",
    "gu": "gu-IN",
    "kn": "kn-IN",
    "ml": "ml-IN",
    "pa": "pa-IN",
    "or": "or-IN",
    "as": "as-IN",
    "ur": "ur-IN",
    "ne": "ne-NP"
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
        list(LANGUAGES.keys()),
        key="language_selector"
    )
    language_code = LANGUAGES[selected_language]
    speech_locale = SPEECH_LOCALES.get(language_code, "en-IN")

with top2:
    st.write("### 🎤 Voice Input")

    # Use a language-specific key so Streamlit fully resets the microphone
    # component when the user changes language.
    try:
        voice_text = speech_to_text(
            language=speech_locale,
            start_prompt="🎤 Speak",
            stop_prompt="⏹ Stop",
            just_once=True,
            use_container_width=True,
            key=f"voice_input_{language_code}"
        )
    except Exception:
        # A microphone/locale problem should never break the language selector
        # or the rest of the MandiVision app.
        voice_text = None
        st.caption("🎤 Voice input is temporarily unavailable for this language. The rest of the app will continue to work.")


# =========================================================
# TRANSLATION
# =========================================================

# Local UI translations keep the app usable even when Google's translation
# endpoint returns an HTTP 500 page. Online translation is used only for
# phrases that are not in this safe fallback dictionary.
LOCAL_TRANSLATIONS = {
    "hi": {
        "Smart Mandi Price and Farmer Decision Support System": "स्मार्ट मंडी मूल्य और किसान निर्णय सहायता प्रणाली",
        "👨‍🌾 Farmer Details": "👨‍🌾 किसान विवरण",
        "🌾 Select Your Crop": "🌾 अपनी फसल चुनें",
        "📦 Quantity (Quintal)": "📦 मात्रा (क्विंटल)",
        "📍 Your Location": "📍 आपका स्थान",
        "Click the button and allow browser location permission.": "बटन पर क्लिक करें और ब्राउज़र में लोकेशन की अनुमति दें।",
        "📍 Enable My Current Location": "📍 मेरी वर्तमान लोकेशन सक्षम करें",
        "Please allow location permission and try again.": "कृपया लोकेशन की अनुमति दें और फिर प्रयास करें।",
        "Please allow location permission in your browser.": "कृपया अपने ब्राउज़र में लोकेशन की अनुमति दें।",
        "🟢 Live location is ready!": "🟢 लाइव लोकेशन तैयार है!",
        "🔴 Enable location before analyzing nearby mandis.": "🔴 आसपास की मंडियों का विश्लेषण करने से पहले लोकेशन सक्षम करें।",
        "🚀 ANALYZE NEARBY MANDIS": "🚀 आसपास की मंडियों का विश्लेषण करें",
        "❌ Please enable your current location first.": "❌ पहले अपनी वर्तमान लोकेशन सक्षम करें।",
        "📊 Smart Mandi Comparison": "📊 स्मार्ट मंडी तुलना",
        "📊 Price Comparison": "📊 मूल्य तुलना",
        "📈 Price Trend Dashboard": "📈 मूल्य ट्रेंड डैशबोर्ड",
        "📈 Historical Price Trend": "📈 ऐतिहासिक मूल्य ट्रेंड",
        "🌾 Select Crop for Trend Analysis": "🌾 ट्रेंड विश्लेषण के लिए फसल चुनें",
        "📅 Select Time Period": "📅 समय अवधि चुनें",
        "📊 Market Price Statistics": "📊 बाजार मूल्य आंकड़े",
        "📋 Historical Price Data": "📋 ऐतिहासिक मूल्य डेटा",
        "📍 Nearest Mandis": "📍 निकटतम मंडियां",
        "🏆 Top 3 Recommended Mandis": "🏆 शीर्ष 3 अनुशंसित मंडियां",
        "🤖 FINAL AI RECOMMENDATION": "🤖 अंतिम AI सिफारिश",
        "🧠 Smart Market Insight": "🧠 स्मार्ट बाजार जानकारी",
        "🤖 Trend Status": "🤖 ट्रेंड स्थिति",
        "Current Price": "वर्तमान मूल्य",
        "Predicted Price": "अनुमानित मूल्य",
        "Expected Return": "अपेक्षित रिटर्न",
        "Expected Net Return": "अपेक्षित शुद्ध रिटर्न",
        "Transport Cost": "परिवहन लागत",
        "Distance": "दूरी",
        "State": "राज्य",
        "Crop": "फसल",
        "Price": "मूल्य",
        "Price Change": "मूल्य परिवर्तन",
        "Average Price": "औसत मूल्य",
        "⬆️ Highest Price": "⬆️ सबसे अधिक मूल्य",
        "⬇️ Lowest Price": "⬇️ सबसे कम मूल्य",
        "AI Reason": "AI कारण",
        "Market Insight": "बाजार जानकारी",
        "PRICE TREND: INCREASING": "मूल्य ट्रेंड: बढ़ रहा है",
        "PRICE TREND: DECREASING": "मूल्य ट्रेंड: घट रहा है",
        "PRICE TREND: STABLE": "मूल्य ट्रेंड: स्थिर है",
        "✅ Location enabled successfully!": "✅ लोकेशन सफलतापूर्वक सक्षम हो गई!",
    },
    "bn": {
        "Smart Mandi Price and Farmer Decision Support System": "স্মার্ট মান্ডি মূল্য ও কৃষক সিদ্ধান্ত সহায়তা ব্যবস্থা",
        "👨‍🌾 Farmer Details": "👨‍🌾 কৃষকের বিবরণ",
        "🌾 Select Your Crop": "🌾 আপনার ফসল নির্বাচন করুন",
        "📦 Quantity (Quintal)": "📦 পরিমাণ (কুইন্টাল)",
        "📍 Your Location": "📍 আপনার অবস্থান",
        "📍 Enable My Current Location": "📍 আমার বর্তমান অবস্থান চালু করুন",
        "🚀 ANALYZE NEARBY MANDIS": "🚀 কাছের মান্ডি বিশ্লেষণ করুন",
        "🟢 Live location is ready!": "🟢 লাইভ অবস্থান প্রস্তুত!",
        "🔴 Enable location before analyzing nearby mandis.": "🔴 কাছের মান্ডি বিশ্লেষণের আগে অবস্থান চালু করুন।",
        "📊 Smart Mandi Comparison": "📊 স্মার্ট মান্ডি তুলনা",
        "📈 Price Trend Dashboard": "📈 মূল্য প্রবণতা ড্যাশবোর্ড",
        "📍 Nearest Mandis": "📍 নিকটতম মান্ডি",
        "🏆 Top 3 Recommended Mandis": "🏆 সেরা ৩টি প্রস্তাবিত মান্ডি",
        "Current Price": "বর্তমান মূল্য",
        "Predicted Price": "পূর্বাভাসিত মূল্য",
        "Expected Return": "প্রত্যাশিত রিটার্ন",
        "Transport Cost": "পরিবহন খরচ",
        "Distance": "দূরত্ব",
        "State": "রাজ্য",
        "Crop": "ফসল",
        "Price": "মূল্য",
        "Average Price": "গড় মূল্য",
    },
    "te": {
        "Smart Mandi Price and Farmer Decision Support System": "స్మార్ట్ మండీ ధర మరియు రైతు నిర్ణయ సహాయ వ్యవస్థ",
        "👨‍🌾 Farmer Details": "👨‍🌾 రైతు వివరాలు",
        "🌾 Select Your Crop": "🌾 మీ పంటను ఎంచుకోండి",
        "📦 Quantity (Quintal)": "📦 పరిమాణం (క్వింటాల్)",
        "📍 Your Location": "📍 మీ స్థానం",
        "📍 Enable My Current Location": "📍 నా ప్రస్తుత స్థానాన్ని ప్రారంభించండి",
        "🚀 ANALYZE NEARBY MANDIS": "🚀 సమీప మండీలను విశ్లేషించండి",
        "🟢 Live location is ready!": "🟢 లైవ్ లొకేషన్ సిద్ధంగా ఉంది!",
        "🔴 Enable location before analyzing nearby mandis.": "🔴 సమీప మండీలను విశ్లేషించే ముందు స్థానాన్ని ప్రారంభించండి.",
        "📊 Smart Mandi Comparison": "📊 స్మార్ట్ మండీ పోలిక",
        "📈 Price Trend Dashboard": "📈 ధర ట్రెండ్ డ్యాష్‌బోర్డ్",
        "📍 Nearest Mandis": "📍 సమీప మండీలు",
        "🏆 Top 3 Recommended Mandis": "🏆 సిఫార్సు చేసిన టాప్ 3 మండీలు",
        "Current Price": "ప్రస్తుత ధర",
        "Predicted Price": "అంచనా ధర",
        "Expected Return": "అంచనా రాబడి",
        "Transport Cost": "రవాణా ఖర్చు",
        "Distance": "దూరం",
        "State": "రాష్ట్రం",
        "Crop": "పంట",
        "Price": "ధర",
        "Average Price": "సగటు ధర",
    },
    "mr": {
        "Smart Mandi Price and Farmer Decision Support System": "स्मार्ट मंडी किंमत आणि शेतकरी निर्णय सहाय्य प्रणाली",
        "👨‍🌾 Farmer Details": "👨‍🌾 शेतकरी तपशील",
        "🌾 Select Your Crop": "🌾 तुमचे पीक निवडा",
        "📦 Quantity (Quintal)": "📦 प्रमाण (क्विंटल)",
        "📍 Your Location": "📍 तुमचे स्थान",
        "📍 Enable My Current Location": "📍 माझे वर्तमान स्थान सुरू करा",
        "🚀 ANALYZE NEARBY MANDIS": "🚀 जवळच्या मंड्यांचे विश्लेषण करा",
        "🟢 Live location is ready!": "🟢 लाइव्ह स्थान तयार आहे!",
        "🔴 Enable location before analyzing nearby mandis.": "🔴 जवळच्या मंड्यांचे विश्लेषण करण्यापूर्वी स्थान सुरू करा.",
        "📊 Smart Mandi Comparison": "📊 स्मार्ट मंडी तुलना",
        "📈 Price Trend Dashboard": "📈 किंमत ट्रेंड डॅशबोर्ड",
        "📍 Nearest Mandis": "📍 जवळच्या मंड्या",
        "🏆 Top 3 Recommended Mandis": "🏆 शिफारस केलेल्या टॉप 3 मंड्या",
        "Current Price": "सध्याची किंमत",
        "Predicted Price": "अंदाजित किंमत",
        "Expected Return": "अपेक्षित परतावा",
        "Transport Cost": "वाहतूक खर्च",
        "Distance": "अंतर",
        "State": "राज्य",
        "Crop": "पीक",
        "Price": "किंमत",
        "Average Price": "सरासरी किंमत",
    },
    "ta": {
        "Smart Mandi Price and Farmer Decision Support System": "ஸ்மார்ட் மண்டி விலை மற்றும் விவசாயி முடிவு ஆதரவு அமைப்பு",
        "👨‍🌾 Farmer Details": "👨‍🌾 விவசாயி விவரங்கள்",
        "🌾 Select Your Crop": "🌾 உங்கள் பயிரைத் தேர்ந்தெடுக்கவும்",
        "📦 Quantity (Quintal)": "📦 அளவு (குவிண்டால்)",
        "📍 Your Location": "📍 உங்கள் இருப்பிடம்",
        "📍 Enable My Current Location": "📍 எனது தற்போதைய இருப்பிடத்தை இயக்கவும்",
        "🚀 ANALYZE NEARBY MANDIS": "🚀 அருகிலுள்ள மண்டிகளை பகுப்பாய்வு செய்யவும்",
        "🟢 Live location is ready!": "🟢 நேரடி இருப்பிடம் தயாராக உள்ளது!",
        "🔴 Enable location before analyzing nearby mandis.": "🔴 அருகிலுள்ள மண்டிகளை பகுப்பாய்வு செய்வதற்கு முன் இருப்பிடத்தை இயக்கவும்.",
        "📊 Smart Mandi Comparison": "📊 ஸ்மார்ட் மண்டி ஒப்பீடு",
        "📈 Price Trend Dashboard": "📈 விலை போக்கு டாஷ்போர்டு",
        "📍 Nearest Mandis": "📍 அருகிலுள்ள மண்டிகள்",
        "🏆 Top 3 Recommended Mandis": "🏆 பரிந்துரைக்கப்பட்ட சிறந்த 3 மண்டிகள்",
        "Current Price": "தற்போதைய விலை",
        "Predicted Price": "கணிக்கப்பட்ட விலை",
        "Expected Return": "எதிர்பார்க்கப்படும் வருமானம்",
        "Transport Cost": "போக்குவரத்து செலவு",
        "Distance": "தூரம்",
        "State": "மாநிலம்",
        "Crop": "பயிர்",
        "Price": "விலை",
        "Average Price": "சராசரி விலை",
    },
    "gu": {
        "Smart Mandi Price and Farmer Decision Support System": "સ્માર્ટ મંડી ભાવ અને ખેડૂત નિર્ણય સહાય પ્રણાલી",
        "👨‍🌾 Farmer Details": "👨‍🌾 ખેડૂત વિગતો",
        "🌾 Select Your Crop": "🌾 તમારો પાક પસંદ કરો",
        "📦 Quantity (Quintal)": "📦 જથ્થો (ક્વિન્ટલ)",
        "📍 Your Location": "📍 તમારું સ્થાન",
        "📍 Enable My Current Location": "📍 મારું વર્તમાન સ્થાન સક્ષમ કરો",
        "🚀 ANALYZE NEARBY MANDIS": "🚀 નજીકની મંડીનું વિશ્લેષણ કરો",
        "🟢 Live location is ready!": "🟢 લાઇવ સ્થાન તૈયાર છે!",
        "🔴 Enable location before analyzing nearby mandis.": "🔴 નજીકની મંડીનું વિશ્લેષણ કરતા પહેલાં સ્થાન સક્ષમ કરો.",
        "📊 Smart Mandi Comparison": "📊 સ્માર્ટ મંડી સરખામણી",
        "📈 Price Trend Dashboard": "📈 ભાવ ટ્રેન્ડ ડેશબોર્ડ",
        "📍 Nearest Mandis": "📍 નજીકની મંડીઓ",
        "🏆 Top 3 Recommended Mandis": "🏆 ભલામણ કરેલી ટોચની 3 મંડીઓ",
        "Current Price": "વર્તમાન ભાવ",
        "Predicted Price": "અંદાજિત ભાવ",
        "Expected Return": "અપેક્ષિત વળતર",
        "Transport Cost": "પરિવહન ખર્ચ",
        "Distance": "અંતર",
        "State": "રાજ્ય",
        "Crop": "પાક",
        "Price": "ભાવ",
        "Average Price": "સરેરાશ ભાવ",
    },
    "kn": {
        "Smart Mandi Price and Farmer Decision Support System": "ಸ್ಮಾರ್ಟ್ ಮಂಡಿ ಬೆಲೆ ಮತ್ತು ರೈತ ನಿರ್ಧಾರ ಸಹಾಯ ವ್ಯವಸ್ಥೆ",
        "👨‍🌾 Farmer Details": "👨‍🌾 ರೈತ ವಿವರಗಳು",
        "🌾 Select Your Crop": "🌾 ನಿಮ್ಮ ಬೆಳೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "📦 Quantity (Quintal)": "📦 ಪ್ರಮಾಣ (ಕ್ವಿಂಟಲ್)",
        "📍 Your Location": "📍 ನಿಮ್ಮ ಸ್ಥಳ",
        "📍 Enable My Current Location": "📍 ನನ್ನ ಪ್ರಸ್ತುತ ಸ್ಥಳವನ್ನು ಸಕ್ರಿಯಗೊಳಿಸಿ",
        "🚀 ANALYZE NEARBY MANDIS": "🚀 ಹತ್ತಿರದ ಮಂಡಿಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಿ",
        "🟢 Live location is ready!": "🟢 ಲೈವ್ ಸ್ಥಳ ಸಿದ್ಧವಾಗಿದೆ!",
        "🔴 Enable location before analyzing nearby mandis.": "🔴 ಹತ್ತಿರದ ಮಂಡಿಗಳನ್ನು ವಿಶ್ಲೇಷಿಸುವ ಮೊದಲು ಸ್ಥಳವನ್ನು ಸಕ್ರಿಯಗೊಳಿಸಿ.",
        "📊 Smart Mandi Comparison": "📊 ಸ್ಮಾರ್ಟ್ ಮಂಡಿ ಹೋಲಿಕೆ",
        "📈 Price Trend Dashboard": "📈 ಬೆಲೆ ಟ್ರೆಂಡ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "📍 Nearest Mandis": "📍 ಹತ್ತಿರದ ಮಂಡಿಗಳು",
        "🏆 Top 3 Recommended Mandis": "🏆 ಶಿಫಾರಸು ಮಾಡಿದ ಟಾಪ್ 3 ಮಂಡಿಗಳು",
        "Current Price": "ಪ್ರಸ್ತುತ ಬೆಲೆ",
        "Predicted Price": "ಅಂದಾಜು ಬೆಲೆ",
        "Expected Return": "ನಿರೀಕ್ಷಿತ ಆದಾಯ",
        "Transport Cost": "ಸಾರಿಗೆ ವೆಚ್ಚ",
        "Distance": "ದೂರ",
        "State": "ರಾಜ್ಯ",
        "Crop": "ಬೆಳೆ",
        "Price": "ಬೆಲೆ",
        "Average Price": "ಸರಾಸರಿ ಬೆಲೆ",
    },
    "ml": {
        "Smart Mandi Price and Farmer Decision Support System": "സ്മാർട്ട് മണ്ഡി വിലയും കർഷക തീരുമാന സഹായ സംവിധാനവും",
        "👨‍🌾 Farmer Details": "👨‍🌾 കർഷക വിവരങ്ങൾ",
        "🌾 Select Your Crop": "🌾 നിങ്ങളുടെ വിള തിരഞ്ഞെടുക്കുക",
        "📦 Quantity (Quintal)": "📦 അളവ് (ക്വിന്റൽ)",
        "📍 Your Location": "📍 നിങ്ങളുടെ സ്ഥലം",
        "📍 Enable My Current Location": "📍 എന്റെ നിലവിലെ സ്ഥലം പ്രവർത്തനക്ഷമമാക്കുക",
        "🚀 ANALYZE NEARBY MANDIS": "🚀 സമീപ മണ്ഡികൾ വിശകലനം ചെയ്യുക",
        "🟢 Live location is ready!": "🟢 ലൈവ് ലൊക്കേഷൻ തയ്യാറാണ്!",
        "🔴 Enable location before analyzing nearby mandis.": "🔴 സമീപ മണ്ഡികൾ വിശകലനം ചെയ്യുന്നതിന് മുമ്പ് ലൊക്കേഷൻ പ്രവർത്തനക്ഷമമാക്കുക.",
        "📊 Smart Mandi Comparison": "📊 സ്മാർട്ട് മണ്ഡി താരതമ്യം",
        "📈 Price Trend Dashboard": "📈 വില ട്രെൻഡ് ഡാഷ്ബോർഡ്",
        "📍 Nearest Mandis": "📍 സമീപ മണ്ഡികൾ",
        "🏆 Top 3 Recommended Mandis": "🏆 ശുപാർശ ചെയ്ത മികച്ച 3 മണ്ഡികൾ",
        "Current Price": "നിലവിലെ വില",
        "Predicted Price": "പ്രവചിച്ച വില",
        "Expected Return": "പ്രതീക്ഷിക്കുന്ന വരുമാനം",
        "Transport Cost": "ഗതാഗത ചെലവ്",
        "Distance": "ദൂരം",
        "State": "സംസ്ഥാനം",
        "Crop": "വിള",
        "Price": "വില",
        "Average Price": "ശരാശരി വില",
    },
    "pa": {
        "Smart Mandi Price and Farmer Decision Support System": "ਸਮਾਰਟ ਮੰਡੀ ਕੀਮਤ ਅਤੇ ਕਿਸਾਨ ਫੈਸਲਾ ਸਹਾਇਤਾ ਪ੍ਰਣਾਲੀ",
        "👨‍🌾 Farmer Details": "👨‍🌾 ਕਿਸਾਨ ਵੇਰਵੇ",
        "🌾 Select Your Crop": "🌾 ਆਪਣੀ ਫਸਲ ਚੁਣੋ",
        "📦 Quantity (Quintal)": "📦 ਮਾਤਰਾ (ਕੁਇੰਟਲ)",
        "📍 Your Location": "📍 ਤੁਹਾਡਾ ਟਿਕਾਣਾ",
        "📍 Enable My Current Location": "📍 ਮੇਰਾ ਮੌਜੂਦਾ ਟਿਕਾਣਾ ਚਾਲੂ ਕਰੋ",
        "🚀 ANALYZE NEARBY MANDIS": "🚀 ਨੇੜਲੀਆਂ ਮੰਡੀਆਂ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ",
        "🟢 Live location is ready!": "🟢 ਲਾਈਵ ਟਿਕਾਣਾ ਤਿਆਰ ਹੈ!",
        "🔴 Enable location before analyzing nearby mandis.": "🔴 ਨੇੜਲੀਆਂ ਮੰਡੀਆਂ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ ਟਿਕਾਣਾ ਚਾਲੂ ਕਰੋ।",
        "📊 Smart Mandi Comparison": "📊 ਸਮਾਰਟ ਮੰਡੀ ਤੁਲਨਾ",
        "📈 Price Trend Dashboard": "📈 ਕੀਮਤ ਰੁਝਾਨ ਡੈਸ਼ਬੋਰਡ",
        "📍 Nearest Mandis": "📍 ਨੇੜਲੀਆਂ ਮੰਡੀਆਂ",
        "🏆 Top 3 Recommended Mandis": "🏆 ਸਿਫਾਰਸ਼ ਕੀਤੀਆਂ ਚੋਟੀ ਦੀਆਂ 3 ਮੰਡੀਆਂ",
        "Current Price": "ਮੌਜੂਦਾ ਕੀਮਤ",
        "Predicted Price": "ਅਨੁਮਾਨਿਤ ਕੀਮਤ",
        "Expected Return": "ਉਮੀਦ ਕੀਤੀ ਵਾਪਸੀ",
        "Transport Cost": "ਢੋਆ-ਢੁਆਈ ਖਰਚ",
        "Distance": "ਦੂਰੀ",
        "State": "ਰਾਜ",
        "Crop": "ਫਸਲ",
        "Price": "ਕੀਮਤ",
        "Average Price": "ਔਸਤ ਕੀਮਤ",
    },
    "or": {
        "Smart Mandi Price and Farmer Decision Support System": "ସ୍ମାର୍ଟ ମଣ୍ଡି ମୂଲ୍ୟ ଏବଂ କୃଷକ ନିଷ୍ପତ୍ତି ସହାୟତା ପ୍ରଣାଳୀ",
        "👨‍🌾 Farmer Details": "👨‍🌾 କୃଷକ ବିବରଣୀ",
        "🌾 Select Your Crop": "🌾 ଆପଣଙ୍କ ଫସଲ ବାଛନ୍ତୁ",
        "📦 Quantity (Quintal)": "📦 ପରିମାଣ (କ୍ୱିଣ୍ଟାଲ)",
        "📍 Your Location": "📍 ଆପଣଙ୍କ ସ୍ଥାନ",
        "📍 Enable My Current Location": "📍 ମୋର ବର୍ତ୍ତମାନ ସ୍ଥାନ ସକ୍ରିୟ କରନ୍ତୁ",
        "🚀 ANALYZE NEARBY MANDIS": "🚀 ନିକଟସ୍ଥ ମଣ୍ଡି ବିଶ୍ଳେଷଣ କରନ୍ତୁ",
        "🟢 Live location is ready!": "🟢 ଲାଇଭ୍ ସ୍ଥାନ ପ୍ରସ୍ତୁତ!",
        "🔴 Enable location before analyzing nearby mandis.": "🔴 ନିକଟସ୍ଥ ମଣ୍ଡି ବିଶ୍ଳେଷଣ ପୂର୍ବରୁ ସ୍ଥାନ ସକ୍ରିୟ କରନ୍ତୁ।",
        "📊 Smart Mandi Comparison": "📊 ସ୍ମାର୍ଟ ମଣ୍ଡି ତୁଳନା",
        "📈 Price Trend Dashboard": "📈 ମୂଲ୍ୟ ଟ୍ରେଣ୍ଡ ଡ୍ୟାସବୋର୍ଡ",
        "📍 Nearest Mandis": "📍 ନିକଟସ୍ଥ ମଣ୍ଡି",
        "🏆 Top 3 Recommended Mandis": "🏆 ସୁପାରିଶ କରାଯାଇଥିବା ଶ୍ରେଷ୍ଠ 3 ମଣ୍ଡି",
        "Current Price": "ବର୍ତ୍ତମାନ ମୂଲ୍ୟ",
        "Predicted Price": "ଅନୁମାନିତ ମୂଲ୍ୟ",
        "Expected Return": "ଆଶାକରାଯାଇଥିବା ରିଟର୍ନ",
        "Transport Cost": "ପରିବହନ ଖର୍ଚ୍ଚ",
        "Distance": "ଦୂରତା",
        "State": "ରାଜ୍ୟ",
        "Crop": "ଫସଲ",
        "Price": "ମୂଲ୍ୟ",
        "Average Price": "ହାରାହାରି ମୂଲ୍ୟ",
    },
    "as": {
        "Smart Mandi Price and Farmer Decision Support System": "স্মাৰ্ট মাণ্ডী মূল্য আৰু কৃষক সিদ্ধান্ত সহায়তা ব্যৱস্থা",
        "👨‍🌾 Farmer Details": "👨‍🌾 কৃষকৰ বিৱৰণ",
        "🌾 Select Your Crop": "🌾 আপোনাৰ শস্য বাছনি কৰক",
        "📦 Quantity (Quintal)": "📦 পৰিমাণ (কুইণ্টাল)",
        "📍 Your Location": "📍 আপোনাৰ অৱস্থান",
        "📍 Enable My Current Location": "📍 মোৰ বৰ্তমান অৱস্থান সক্ৰিয় কৰক",
        "🚀 ANALYZE NEARBY MANDIS": "🚀 ওচৰৰ মাণ্ডী বিশ্লেষণ কৰক",
        "🟢 Live location is ready!": "🟢 লাইভ অৱস্থান সাজু!",
        "🔴 Enable location before analyzing nearby mandis.": "🔴 ওচৰৰ মাণ্ডী বিশ্লেষণ কৰাৰ আগতে অৱস্থান সক্ৰিয় কৰক।",
        "📊 Smart Mandi Comparison": "📊 স্মাৰ্ট মাণ্ডী তুলনা",
        "📈 Price Trend Dashboard": "📈 মূল্য ট্ৰেণ্ড ডেশ্বব'ৰ্ড",
        "📍 Nearest Mandis": "📍 ওচৰৰ মাণ্ডী",
        "🏆 Top 3 Recommended Mandis": "🏆 পৰামৰ্শ দিয়া শীৰ্ষ ৩ মাণ্ডী",
        "Current Price": "বৰ্তমান মূল্য",
        "Predicted Price": "অনুমানিত মূল্য",
        "Expected Return": "প্ৰত্যাশিত ৰিটাৰ্ণ",
        "Transport Cost": "পৰিবহণ খৰচ",
        "Distance": "দূৰত্ব",
        "State": "ৰাজ্য",
        "Crop": "শস্য",
        "Price": "মূল্য",
        "Average Price": "গড় মূল্য",
    },
    "ur": {
        "Smart Mandi Price and Farmer Decision Support System": "اسمارٹ منڈی قیمت اور کسان فیصلہ معاون نظام",
        "👨‍🌾 Farmer Details": "👨‍🌾 کسان کی تفصیلات",
        "🌾 Select Your Crop": "🌾 اپنی فصل منتخب کریں",
        "📦 Quantity (Quintal)": "📦 مقدار (کوئنٹل)",
        "📍 Your Location": "📍 آپ کا مقام",
        "📍 Enable My Current Location": "📍 میری موجودہ لوکیشن فعال کریں",
        "🚀 ANALYZE NEARBY MANDIS": "🚀 قریبی منڈیوں کا تجزیہ کریں",
        "🟢 Live location is ready!": "🟢 لائیو لوکیشن تیار ہے!",
        "🔴 Enable location before analyzing nearby mandis.": "🔴 قریبی منڈیوں کا تجزیہ کرنے سے پہلے لوکیشن فعال کریں۔",
        "📊 Smart Mandi Comparison": "📊 اسمارٹ منڈی موازنہ",
        "📈 Price Trend Dashboard": "📈 قیمت رجحان ڈیش بورڈ",
        "📍 Nearest Mandis": "📍 قریبی منڈیاں",
        "🏆 Top 3 Recommended Mandis": "🏆 تجویز کردہ ٹاپ 3 منڈیاں",
        "Current Price": "موجودہ قیمت",
        "Predicted Price": "متوقع قیمت",
        "Expected Return": "متوقع منافع",
        "Transport Cost": "نقل و حمل کی لاگت",
        "Distance": "فاصلہ",
        "State": "ریاست",
        "Crop": "فصل",
        "Price": "قیمت",
        "Average Price": "اوسط قیمت",
    },
    "ne": {
        "Smart Mandi Price and Farmer Decision Support System": "स्मार्ट मन्डी मूल्य तथा किसान निर्णय सहयोग प्रणाली",
        "👨‍🌾 Farmer Details": "👨‍🌾 किसान विवरण",
        "🌾 Select Your Crop": "🌾 आफ्नो बाली छान्नुहोस्",
        "📦 Quantity (Quintal)": "📦 मात्रा (क्विन्टल)",
        "📍 Your Location": "📍 तपाईंको स्थान",
        "📍 Enable My Current Location": "📍 मेरो हालको स्थान सक्षम गर्नुहोस्",
        "🚀 ANALYZE NEARBY MANDIS": "🚀 नजिकका मन्डी विश्लेषण गर्नुहोस्",
        "🟢 Live location is ready!": "🟢 लाइभ स्थान तयार छ!",
        "🔴 Enable location before analyzing nearby mandis.": "🔴 नजिकका मन्डी विश्लेषण गर्नु अघि स्थान सक्षम गर्नुहोस्।",
        "📊 Smart Mandi Comparison": "📊 स्मार्ट मन्डी तुलना",
        "📈 Price Trend Dashboard": "📈 मूल्य प्रवृत्ति ड्यासबोर्ड",
        "📍 Nearest Mandis": "📍 नजिकका मन्डी",
        "🏆 Top 3 Recommended Mandis": "🏆 सिफारिस गरिएका शीर्ष ३ मन्डी",
        "Current Price": "हालको मूल्य",
        "Predicted Price": "अनुमानित मूल्य",
        "Expected Return": "अपेक्षित आम्दानी",
        "Transport Cost": "ढुवानी लागत",
        "Distance": "दूरी",
        "State": "राज्य",
        "Crop": "बाली",
        "Price": "मूल्य",
        "Average Price": "औसत मूल्य",
    },
}


@st.cache_data(show_spinner=False, ttl=86400)
def translate_text(text, lang):

    if lang == "en" or not text:
        return text

    # First use local translations for important UI strings.
    local = LOCAL_TRANSLATIONS.get(lang, {})
    if text in local:
        return local[text]

    try:
        translated = GoogleTranslator(source="auto", target=lang).translate(text)
        if not translated:
            return text

        # Google can occasionally return its own HTTP 500 error page as text.
        # Never show that server message inside the app UI.
        bad_markers = (
            "error 500",
            "500 (server error)",
            "that's an error",
            "there was an error",
            "please try again later",
            "server error",
        )
        translated_lower = str(translated).lower()
        if any(marker in translated_lower for marker in bad_markers):
            return text

        # Guard against an unexpectedly huge HTML/error response.
        if len(str(translated)) > max(500, len(str(text)) * 12):
            return text

        return translated

    except Exception:
        return text


def T(text):
    return translate_text(text, language_code)

    # English is already the source language, so do not make a network call.
    if lang == "en" or not text:
        return text

    try:
        translated = GoogleTranslator(
            source="auto",
            target=lang
        ).translate(text)

        # Never replace working UI text with an empty/invalid translation.
        return translated if translated else text

    except Exception:
        # Translation service can occasionally be unavailable or rate-limited.
        # Keep the English text as a safe fallback instead of showing an error.
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
    f'''<div class="mv-fixed-header">
        <div class="main-title">🌾 MandiVision AI India 🇮🇳</div>
        <div class="subtitle">{T("Smart Mandi Price and Farmer Decision Support System")}</div>
    </div>''',
    unsafe_allow_html=True
)

st.divider()


st.markdown("""
<div style="
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:12px;
    margin:8px 0 20px 0;
">
  <div style="background:rgba(255,255,255,.78);padding:14px;border-radius:15px;text-align:center;box-shadow:0 5px 15px rgba(30,70,40,.08);">
    <div style="font-size:25px;">🌾</div>
    <b style="color:#173f2b;">Crop Prices</b><br>
    <span style="color:#5b3a1f;font-size:13px;">Smart mandi insights</span>
  </div>
  <div style="background:rgba(255,255,255,.78);padding:14px;border-radius:15px;text-align:center;box-shadow:0 5px 15px rgba(30,70,40,.08);">
    <div style="font-size:25px;">📍</div>
    <b style="color:#173f2b;">Nearby Mandis</b><br>
    <span style="color:#5b3a1f;font-size:13px;">Find better options</span>
  </div>
  <div style="background:rgba(255,255,255,.78);padding:14px;border-radius:15px;text-align:center;box-shadow:0 5px 15px rgba(30,70,40,.08);">
    <div style="font-size:25px;">🤖</div>
    <b style="color:#173f2b;">AI Prediction</b><br>
    <span style="color:#5b3a1f;font-size:13px;">Price trend support</span>
  </div>
  <div style="background:rgba(255,255,255,.78);padding:14px;border-radius:15px;text-align:center;box-shadow:0 5px 15px rgba(30,70,40,.08);">
    <div style="font-size:25px;">💰</div>
    <b style="color:#173f2b;">Net Return</b><br>
    <span style="color:#5b3a1f;font-size:13px;">Compare earnings</span>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# FARMER DETAILS
# =========================================================

st.header(T("👨‍🌾 Farmer Details"))

col1, col2 = st.columns(2)

with col1:

    crop = st.selectbox(
        T("🌾 Select Your Crop"),
        CROPS,
        index=CROPS.index(st.session_state.selected_crop),
        key="main_crop_selector"
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
    use_container_width=True,
    key="enable_location_button"
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
    use_container_width=True,
    key="analyze_nearby_mandis_button"
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

