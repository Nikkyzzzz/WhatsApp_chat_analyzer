import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from textblob import TextBlob
import cohere
from sklearn.linear_model import LinearRegression, LogisticRegression

# ===============================
# Streamlit Config
# ===============================
st.set_page_config(
    page_title="Chat Analysis Dashboard", 
    page_icon="💬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# Enhanced Professional Theme
# ===============================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap');
    
    :root {
        --primary-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-bg: rgba(255, 255, 255, 0.95);
        --text-primary: #2d3748;
        --text-secondary: #4a5568;
        --text-light: #718096;
        --accent-primary: #667eea;
        --accent-secondary: #764ba2;
        --border-light: rgba(226, 232, 240, 0.8);
        --shadow-soft: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-medium: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --border-radius: 12px;
        --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        --bg-color1:#000B58;
        --bg-color2:#003161;

    }
    
    .stApp {
        background: linear-gradient(135deg, var(--bg-color1), var(--bg-color2));
        color: #FFFFFF !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Ensure all text elements have proper color */
    .stApp * {
        color: var(--text-primary) !important;
    }
    
    /* Override for specific elements that should remain white */
    .stButton > button {
        color: white !important;
    }
    
    /* Typography - General styling */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.025em;
        line-height: 1.2;
    }
    
    /* Override ALL headers except sidebar */
    .stApp h1:not([data-testid="stSidebar"] h1):not(.css-1d391kg h1):not(.css-17lntkn h1),
    .stApp h2:not([data-testid="stSidebar"] h2):not(.css-1d391kg h2):not(.css-17lntkn h2),
    .stApp h3:not([data-testid="stSidebar"] h3):not(.css-1d391kg h3):not(.css-17lntkn h3),
    h1:not([data-testid="stSidebar"] h1),
    h2:not([data-testid="stSidebar"] h2),
    h3:not([data-testid="stSidebar"] h3) {
        color: #006A67 !important;
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 1.5rem 2rem !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        margin: 1rem 0 !important;
        display: block !important;
        width: calc(100% - 4rem) !important;
        box-sizing: content-box !important;
    }
    
    h1 { font-size: 2.5rem; margin-bottom: 1rem; }
    h2 { font-size: 2rem; margin-bottom: 0.75rem; }
    h3 { font-size: 1.5rem; margin-bottom: 0.5rem; }
    
    /* Custom Content Header Div */
    .content-header {
        background: linear-gradient(135deg, rgba(255, 194, 155, 0.35), rgba(255, 194, 155, 0.15)) !important;
        border: 2px solid #006A67 !important;
        border-radius: 16px !important;
        padding: 2rem 2.5rem !important;
        margin: 2rem 0 !important;
        box-shadow: 
            0 8px 25px -5px rgba(0, 106, 103, 0.2),
            0 10px 10px -5px rgba(0, 106, 103, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .content-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #006A67, #FFC29B, #006A67) !important;
        border-radius: 16px 16px 0 0;
    }
    
    .content-header h1,
    .content-header h2,
    .content-header h3 {
        color: #FFFFFF !important;
        margin: 0 !important;
        padding: 0 !important;
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        width: 100% !important;
        box-sizing: border-box !important;
        text-align: center !important;
        font-weight: 800 !important;
        text-shadow: 0 3px 8px rgba(0, 0, 0, 0.5), 0 1px 3px rgba(0, 0, 0, 0.3) !important;
    }
    
    .content-header h1 { font-size: 2.8rem !important; }
    .content-header h2 { font-size: 2.2rem !important; }
    .content-header h3 { font-size: 1.8rem !important; }
    
    .content-header p,
    .content-header pre,
    .content-header pre * {
        color: #F7FAFC !important;
        font-size: 1.1rem !important;
        text-align: center !important;
        margin: 1rem 0 0 0 !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        white-space: pre-wrap !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        display: block !important;
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 0 !important;
        background: none !important;
        border: none !important;
    }
    .content-pre {
        color: #F7FAFC !important;
        font-size: 1.1rem !important;
        text-align: center !important;
        margin: 1rem 0 0 0 !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        white-space: pre-wrap !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        display: block !important;
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 0 !important;
        background: none !important;
        border: none !important;
    }

    /* Specific pink text class to override global styles */
    .pink-text {
        color: #F39F9F !important;
        font-weight: 600 !important;
    }
    
    /* Main Content Area */
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 1200px;
    }
    
    /* Sidebar Styling */
    .css-1d391kg,
    .css-17lntkn,
    .css-1lcbmhc,
    .css-1y4p8pa,
    .stSidebar,
    [data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {
        background: rgba(253, 235, 158, 0.5) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid var(--border-light);
    }
    
    .sidebar .sidebar-content {
        background: transparent;
        padding: 1.5rem 1rem;
    }
    
    /* Radio Button Styling */
    .stRadio > label {
        font-weight: 500;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .stRadio > div > label {
        display: flex;
        align-items: center;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: var(--border-radius);
        background: rgba(255, 255, 255, 0.3);
        border: 1px solid transparent;
        transition: var(--transition);
        cursor: pointer;
        color: var(--text-primary) !important;
    }
    
    .stRadio > div > label:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: var(--border-light);
        transform: translateY(-1px);
    }
    
    /* Cards and Containers */
    .metric-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-soft);
        border: 1px solid var(--border-light);
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    .stMetric {
        background: var(--card-bg);
        padding: 1rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-soft);
        border: 1px solid var(--border-light);
        color: var(--text-primary) !important;
    }
    
    /* Charts and Data */
    .stDataFrame {
        background: var(--card-bg);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-soft);
        border: 1px solid var(--border-light);
        overflow: hidden;
    }
    
    .stPlotlyChart, .stPyplot {
        background: var(--card-bg);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-soft);
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 2rem;
        font-weight: 600;
        letter-spacing: 0.025em;
        transition: var(--transition);
        box-shadow: var(--shadow-soft);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
        background: linear-gradient(135deg, var(--accent-secondary), var(--accent-primary));
    }
    
    /* Form Elements */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stSlider > div {
        border-radius: var(--border-radius);
        border: 1px solid var(--border-light);
        background: rgba(253, 235, 158, 0.8); !important;
        transition: var(--transition);
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        border-color: var(--accent-primary);
    }
    
    /* Success/Info Messages */
    .stSuccess, .stInfo {
        background: var(--card-bg);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-soft);
        border-left: 4px solid var(--accent-primary);
    }
    
    /* Custom Classes */
    .love-header {
        text-align: center;
        background: var(--card-bg);
        padding: 2rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-soft);
        margin-bottom: 2rem;
    }
    
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .award-item {
        background: var(--card-bg);
        padding: 1rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-soft);
        border-left: 4px solid var(--accent-primary);
        margin: 0.5rem 0;
    }
    
    /* Footer styling */
    .stApp .footer-text,
    .stApp .footer-text em,
    .stApp .footer-text * {
        color: white !important;
        font-style: italic !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ===============================
# Sidebar Navigation
# ===============================
with st.sidebar:
    st.markdown("# 📊 Chat Analysis")
    st.markdown("---")
    
    menu = st.radio(
        "Navigate:",
        [
            "Overview",
            "Basic Stats", 
            "Keyword Analysis",
            "Temporal Patterns",
            "Conversation Flow",
            "Word Clouds",
            "Awards & Metrics",
            "ML Predictions",
            "AI Chat",
            "Report"
        ],
        key="navigation"
    )
    
    st.markdown("---")
    st.markdown("### 📁 Project Info")
    st.markdown("*Key sections to navigate through the dashboard*")

# ===============================
# Data Loading & Processing
# ===============================
@st.cache_data(show_spinner=False)
def load_and_process_data(path: str) -> pd.DataFrame:
    try:
        df_local = pd.read_csv(path)
    except:
        # Create sample data if file doesn't exist
        dates = pd.date_range('2023-01-01', '2023-12-31', freq='4H')
        df_local = pd.DataFrame({
            'DateTime': dates,
            'Name': np.random.choice(['Alice', 'Bob'], len(dates)),
            'Message': ['I love you', 'Miss you', 'Good morning baby', 'How was your day?'] * (len(dates)//4)
        })
    
    # Data cleaning and feature engineering
    if "Message" not in df_local.columns:
        df_local["Message"] = ""
    df_local["Message"] = df_local["Message"].fillna("").astype(str)
    
    if "Name" not in df_local.columns:
        df_local["Name"] = "Unknown"
    
    # Handle datetime parsing
    if "DateTime" in df_local.columns:
        df_local["DateTime"] = pd.to_datetime(df_local["DateTime"], errors="coerce")
    elif {"Date", "Time"}.issubset(df_local.columns):
        df_local["DateTime"] = pd.to_datetime(
            df_local["Date"].astype(str) + " " + df_local["Time"].astype(str),
            errors="coerce"
        )
    else:
        df_local["DateTime"] = pd.date_range('2023-01-01', periods=len(df_local), freq='H')
    
    # Feature engineering
    df_local["Hour"] = df_local["DateTime"].dt.hour
    df_local["WeekdayName"] = df_local["DateTime"].dt.day_name()
    df_local["WeekdayNum"] = df_local["DateTime"].dt.weekday
    df_local["MsgLength"] = df_local["Message"].str.len()
    df_local["Sentiment"] = df_local["Message"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    
    # Reply time calculation
    df_local = df_local.sort_values("DateTime").reset_index(drop=True)
    df_local["PrevName"] = df_local["Name"].shift(1)
    df_local["PrevDateTime"] = df_local["DateTime"].shift(1)
    deltas = (df_local["DateTime"] - df_local["PrevDateTime"]).dt.total_seconds() / 60
    df_local["ReplyTimeMin"] = np.where(df_local["Name"] != df_local["PrevName"], deltas, np.nan)
    
    return df_local

# Load data
df = load_and_process_data("HuyeHuye.csv")
non_system = df[df["Name"] != "System"].copy() if "System" in df["Name"].values else df.copy()

# ===============================
# Page Content
# ===============================

if menu == "Overview":
    st.markdown("""
    <div class="content-header">
        <h1>Chat Analysis Dashboard</h1>
        <p>An executive overview of communication patterns and key insights derived from chat data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Messages", value=f"{len(non_system):,}")
    with col2:
        unique_days = df['DateTime'].dt.date.nunique()
        st.metric("Active Days", value=unique_days)
    with col3:
        avg_daily = len(non_system) / max(unique_days, 1)
        st.metric("Avg Messages / Day", value=f"{avg_daily:.1f}")

    st.markdown("""
    <div class="content-header">
        <h2>Key Findings</h2>
        <p>
        Summary of key metrics, trends, and actionable insights derived from the chat dataset. Use these highlights to guide next steps and discussion points during the presentation.
        </p><p style="text-align: left;">
        It includes: <br>
                1. Most active participants <br>
                2. Peak communication times <br>
                3. Common keywords and sentiments <br>
                4. Conversation dynamics and reply patterns, and several other metrics
        </p>
    </div>
    """, unsafe_allow_html=True)

elif menu == "Basic Stats":
    st.header("📊 Communication Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Message Distribution")
        msg_counts = non_system['Name'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = ['#667eea', '#764ba2']
        bars = ax.bar(msg_counts.index, msg_counts.values, color=colors[:len(msg_counts)])
        ax.set_title('Who Texts More?', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Number of Messages')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                   f'{int(height):,}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Message Length Analysis")
        fig, ax = plt.subplots(figsize=(8, 6))
        non_system.boxplot(column='MsgLength', by='Name', ax=ax)
        ax.set_title('Message Length Distribution')
        ax.set_xlabel('Person')
        ax.set_ylabel('Characters per Message')
        plt.suptitle('')
        plt.tight_layout()
        st.pyplot(fig)

elif menu == "Keyword Analysis":
    st.header("Keyword & Sentiment Analysis")
    
    # Define keywords of interest
    keywords = {
        "hello": "",
        "good morning": "",
        "good night": "",
        "meeting": "",
        "project": "",
        "thanks": ""
    }
    
    # Calculate keyword frequencies
    keyword_data = []
    for person in non_system['Name'].unique():
        person_msgs = non_system[non_system['Name'] == person]['Message'].str.lower()
        person_data = {'Name': person}
        for keyword, emoji in keywords.items():
            count = person_msgs.str.contains(keyword, na=False).sum()
            person_data[f"{keyword} {emoji}"] = count
        keyword_data.append(person_data)
    
    keyword_df = pd.DataFrame(keyword_data)
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Keyword Overview")
        st.dataframe(keyword_df.set_index('Name'), use_container_width=True)

    with col2:
        st.subheader("Keyword Frequency")
        # Use a representative keyword for plot example if present
        rep_keyword = list(keywords.keys())[0]
        rep_col = f"{rep_keyword}"
        keyword_counts = keyword_df.set_index('Name').get(rep_col, pd.Series(dtype=int))
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(keyword_counts.index, keyword_counts.values, color=['#4c78a8', '#f58518'][:len(keyword_counts)])
        ax.set_title(f'Frequency of "{rep_keyword}"')
        ax.set_ylabel('Frequency')

        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom', fontweight='bold')

        plt.tight_layout()
        st.pyplot(fig)

elif menu == "Temporal Patterns":
    st.header("⏰ Temporal Activity")
    
    # Hourly activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Activity by Hour")
        hourly = df.groupby('Hour').size()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(hourly.index, hourly.values, marker='o', linewidth=3, markersize=8, color='#667eea')
        ax.fill_between(hourly.index, hourly.values, alpha=0.3, color='#667eea')
        ax.set_title('Messages Throughout the Day')
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Message Count')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Weekly Pattern")
        weekly = df['WeekdayName'].value_counts()
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly = weekly.reindex(days_order)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(range(len(weekly)), weekly.values, color='#764ba2')
        ax.set_title('Messages by Day of Week')
        ax.set_xlabel('Day')
        ax.set_ylabel('Message Count')
        ax.set_xticks(range(len(weekly)))
        ax.set_xticklabels([day[:3] for day in days_order], rotation=45)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)

elif menu == "Conversation Flow":
    st.header("📖 How We Communicate")
    
    # Reply time analysis
    non_system = df[df["Name"].ne("System")].copy()
    reply_times = non_system.dropna(subset=['ReplyTimeMin'])
    if not reply_times.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Reply Time Distribution")
            avg_reply = reply_times.groupby('Name')['ReplyTimeMin'].mean()
            fig, ax = plt.subplots(figsize=(8, 6))
            bars = ax.bar(avg_reply.index, avg_reply.values, color=['#ff9a9e', '#fecfef'])
            ax.set_title('Average Reply Time')
            ax.set_ylabel('Minutes')
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}m', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.subheader("Conversation Starters")
            # Messages after long gaps (>60 min) could be conversation starters
            starters = reply_times[reply_times['ReplyTimeMin'] > 60]['Name'].value_counts()
            if not starters.empty:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.pie(starters.values, labels=starters.index, autopct='%1.1f%%', 
                      colors=['#a8edea', '#fed6e3'])
                ax.set_title('Who Starts Conversations More?')
                st.pyplot(fig)
    else:
        st.info("Reply time analysis requires timestamp data.")

elif menu == "Word Clouds":
    st.header("☁️ Word Clouds")
    
    # Create word clouds for each person
    names = non_system['Name'].unique()
    
    cols = st.columns(len(names))
    
    for i, name in enumerate(names):
        person_text = " ".join(non_system[non_system['Name'] == name]['Message'].astype(str))
        person_text = person_text.replace('<Media omitted>', '').replace('This message was deleted', '')
        
        if person_text.strip():
            wordcloud = WordCloud(
                width=400, height=300, 
                background_color='white',
                colormap='viridis',
                max_words=100,
                relative_scaling=0.5
            ).generate(person_text)
            
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            ax.set_title(f"{name}'s Words", fontsize=16, fontweight='bold')
            
            with cols[i]:
                st.pyplot(fig)

elif menu == "Awards & Metrics":
    st.header("🏆 Special Recognition")
    
    # Calculate various metrics for awards
    metrics = {}
    
    # Romance metrics
    love_counts = non_system[non_system['Message'].str.contains('i love you', case=False, na=False)]['Name'].value_counts()
    miss_counts = non_system[non_system['Message'].str.contains('i miss you', case=False, na=False)]['Name'].value_counts()
    
    # Communication metrics
    msg_lengths = non_system.groupby('Name')['MsgLength'].mean()
    total_messages = non_system['Name'].value_counts()
    
    # Awards
    awards = []
    
    if not love_counts.empty:
        awards.append(("💕 Most Romantic", love_counts.index[0], f"{love_counts.iloc[0]} love declarations"))
    
    if not miss_counts.empty:
        awards.append(("🥺 Biggest Misser", miss_counts.index[0], f"{miss_counts.iloc[0]} miss you messages"))
    
    if not msg_lengths.empty:
        storyteller = msg_lengths.idxmax()
        awards.append(("📚 The Storyteller", storyteller, f"{msg_lengths[storyteller]:.0f} chars/message"))
    
    if not total_messages.empty:
        chatterbox = total_messages.index[0]
        awards.append(("💬 The Chatterbox", chatterbox, f"{total_messages.iloc[0]:,} total messages"))
    
    # Display awards
    for award, winner, description in awards:
        st.markdown(f"""
        <div class="award-item">
            <h3>{award}</h3>
            <h4>🏆 {winner}</h4>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Summary statistics
    st.subheader("📊 Award Statistics")
    award_data = {
        'Person': non_system['Name'].unique(),
        'Total Messages': [total_messages.get(name, 0) for name in non_system['Name'].unique()],
        'Avg Message Length': [msg_lengths.get(name, 0) for name in non_system['Name'].unique()],
        'Love Declarations': [love_counts.get(name, 0) for name in non_system['Name'].unique()],
        'Miss You Count': [miss_counts.get(name, 0) for name in non_system['Name'].unique()]
    }
    st.dataframe(pd.DataFrame(award_data).set_index('Person'))

elif menu == "ML Predictions":
    st.header("🤖 AI Insights About Our Love")
    
    # Prepare features for ML
    feature_cols = ['Hour', 'WeekdayNum', 'MsgLength', 'Sentiment']
    df_ml = df.dropna(subset=feature_cols).copy()
    
    if len(df_ml) > 10:  # Need sufficient data
        # Love message prediction
        df_ml['LoveMsg'] = df_ml['Message'].str.contains('i love you', case=False, na=False).astype(int)
        
        if df_ml['LoveMsg'].sum() > 0:  # Need some positive examples
            X = df_ml[feature_cols]
            y = df_ml['LoveMsg']
            
            # Train model
            model = LogisticRegression(random_state=42)
            model.fit(X, y)
            
            st.subheader("Love Message Predictor")
            
            with st.form("prediction_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    hour = st.slider("Hour of day", 0, 23, 20)
                    day = st.selectbox("Day of week", 
                                     ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                                      'Friday', 'Saturday', 'Sunday'], index=5)
                
                with col2:
                    message = st.text_area("Sample message", 
                                         "Good night", height=100)
                
                predict_btn = st.form_submit_button("🔮 Predict", use_container_width=True)
                
                if predict_btn:
                    # Calculate features
                    msg_length = len(message)
                    sentiment = TextBlob(message).sentiment.polarity
                    weekday_num = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                                  'Friday', 'Saturday', 'Sunday'].index(day)
                    
                    # Make prediction
                    features = np.array([[hour, weekday_num, msg_length, sentiment]])
                    prob = model.predict_proba(features)[0][1]
                    prediction = "This looks like a love message!" if prob > 0.5 else "This seems like a regular message."

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Love Probability", f"{prob:.1%}")
                    with col2:
                        st.metric("Prediction", prediction)
        else:
            st.info("Not enough love messages in the data for prediction modeling.")
    else:
        st.info("Insufficient data for machine learning predictions.")

elif menu == "AI Chat":
    st.header("🤖 AI Chat Data Analyzer")
    
    st.markdown("""
    <div class="content-header">
        <h2>Cohere AI Analysis</h2>
        <p>Ask questions about your chat data and get AI-powered insights based on the conversation patterns, statistics, and trends.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize Cohere client
    try:
        co = cohere.Client("8mbLFQr0Vv21emvY4tI3DEy8YNlpO8e7Y5SAzpqU")

        # Prepare chat data summary for context
        chat_summary = f"""
        Chat Data Summary:
        - Total Messages: {len(non_system):,}
        - Active Days: {df['DateTime'].dt.date.nunique()}
        - Participants: {', '.join(non_system['Name'].unique())}
        - Date Range: {df['DateTime'].min().strftime('%Y-%m-%d')} to {df['DateTime'].max().strftime('%Y-%m-%d')}
        - Average Messages per Day: {len(non_system) / max(df['DateTime'].dt.date.nunique(), 1):.1f}
        - Most Active Hour: {df.groupby('Hour').size().idxmax()}:00
        - Message Length Stats: Min {non_system['MsgLength'].min()}, Max {non_system['MsgLength'].max()}, Avg {non_system['MsgLength'].mean():.1f} characters
        - Participants Message Count: {dict(non_system['Name'].value_counts())}
        """
        
        # User input for AI query
        user_question = st.text_area(
            "Ask AI about your chat data:",
            placeholder="Examples:\n- What are the communication patterns?\n- Who is more active in conversations?\n- What are the peak activity times?\n- Analyze the conversation dynamics\n- What insights can you provide about this chat data?",
            height=100
        )
        
        if st.button("🤖 Analyze with AI", use_container_width=True):
            if user_question.strip():
                with st.spinner("AI is analyzing your chat data..."):
                    try:
                        # Create comprehensive prompt for Cohere
                        prompt = f"""
                        You are a data analyst expert. Based on the following chat dataset summary, please answer the user's question with detailed insights and professional analysis.

                        {chat_summary}

                        Additional Context:
                        - This is a chat conversation dataset
                        - Data includes timestamps, participants, message content, and derived metrics
                        - Focus on communication patterns, behavioral insights, and data-driven observations

                        User Question: {user_question}

                        Please provide a comprehensive, professional analysis addressing the user's question. Include specific numbers and insights from the data summary provided above.
                        """
                        
                        # Generate response using Cohere Chat API with model fallback
                        models_to_try = ['command-r-plus', 'command-r-08-2024', 'command', 'command-light']
                        response = None
                        
                        for model in models_to_try:
                            try:
                                response = co.chat(
                                    model=model,
                                    message=prompt,
                                    max_tokens=500,
                                    temperature=0.3,
                                    preamble="You are a professional data analyst expert specializing in communication pattern analysis."
                                )
                                break  # If successful, break out of the loop
                            except Exception as model_error:
                                if "404" in str(model_error) or "not found" in str(model_error).lower():
                                    continue  # Try next model
                                else:
                                    raise model_error  # Re-raise if it's not a model availability issue
                        
                        if response is None:
                            raise Exception("All available models failed. Cohere API may have changed.")
                        
                        # Display AI response
                        st.markdown("### 🤖 AI Analysis Results")
                        
                        with st.container():
                            st.markdown(f"""
                            <div class = "metric-card">
                                <p>{response.text.strip().replace('\n', '<br>')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Show data context used
                        with st.expander("📊 Data Context Used by AI"):
                             st.text(chat_summary)

                    except Exception as e:
                        st.error(f"AI Analysis Error: {str(e)}")
                        st.info("Please check your Cohere API key configuration in Streamlit secrets.")
            else:
                st.warning("Please enter a question for AI analysis.")
                
    except Exception as e:
        st.error("Cohere AI configuration error. Please set up your API key.")
        
        # Fallback: Show basic statistics
        st.markdown("### 📊 Basic Chat Statistics (Fallback)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Messages", f"{len(non_system):,}")
        with col2:
            most_active = non_system['Name'].value_counts().index[0]
            st.metric("Most Active", most_active)
        with col3:
            peak_hour = df.groupby('Hour').size().idxmax()
            st.metric("Peak Hour", f"{peak_hour}:00")

elif menu == "Report":
    st.markdown("""
    <div class="content-header">
        <h1>Project Report</h1>
        <p>Executive summary and recommended next steps based on chat data analysis.</p>
    </div>
    """, unsafe_allow_html=True)

    # Key summary metrics
    total_days = df['DateTime'].dt.date.nunique()
    total_messages = len(non_system)
    avg_daily = total_messages / max(total_days, 1)
    peak_hour = int(df['Hour'].mode()[0]) if not df['Hour'].mode().empty else None
    top_sender = non_system['Name'].value_counts().idxmax() if not non_system['Name'].empty else 'N/A'

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Days", f"{total_days}")
    with col2:
        st.metric("💬 Total Messages", f"{total_messages:,}")
    with col3:
        st.metric("📊 Daily Average", f"{avg_daily:.1f}")
    with col4:
        st.metric("Top Sender", top_sender)

    st.markdown("---")

    st.subheader("Executive Summary")
    st.markdown("""
    <div class="content-header">
    <p>
    - The dataset contains an estimated {msgs:,} messages collected over {days} days.
    - Peak messaging activity typically occurs around hour {peak}.
    - The analysis includes keyword frequency, temporal patterns, and a demonstration ML model for illustrative purposes.
    </p>
    </div>
    """.format(msgs=total_messages, days=total_days, peak=peak_hour), unsafe_allow_html=True)

    st.subheader("Recommendations")
    st.markdown("""
    <div class="content-header">
    <p>
    1. Consider segmenting conversations by topic to identify actionable categories (e.g., project, scheduling, support).
    2. Use keyword-driven alerts to highlight urgent or high-priority messages.
    3. If further modeling is required, enrich the dataset with labeled categories and conversational context.
    4. Schedule a follow-up meeting to review these insights and determine priorities for next steps.
    </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<p class="footer-text"><em>Prepared by Love Mathur</em></p>', unsafe_allow_html=True)