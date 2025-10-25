# 💬 WhatsApp Chat Analyzer

A *Streamlit-based Machine Learning Dashboard* that analyzes WhatsApp chats to extract deep conversational insights — including message statistics, user behavior, sentiment, and predictive analytics.  
The app integrates *Cohere’s NLP API* to provide an *AI-powered chatbot* for dynamic insights and contextual question answering.

---

## 🚀 Key Features

### 📊 Chat Data Analysis
- Parses and cleans WhatsApp exported chat text into a structured CSV/Excel file.  
- Displays total messages, active days, average messages/day, and sender activity.

### 🧠 Machine Learning Insights
- Trains ML models (using *Scikit-learn*) to:
  - Predict message reply times.
  - Identify probable “love” or “regular” messages.
  - Analyze message sentiment using *TextBlob*.

### 🤖 Cohere AI Chatbot
- Integrates *Cohere’s “command-light”* LLM model to interpret chat data.
- Users can ask natural language questions about their chats, e.g.:
  - “Who talks more during weekends?”
  - “When are we most active?”
  - “What’s the tone of our conversations?”

### 📈 Visualization & Reports
- Interactive *Streamlit dashboard* with:
  - Word clouds
  - Time-based message frequency plots
  - Message length distributions
  - Keyword trends
- Generates a full *analytical report* summarizing behavioral insights.

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| Frontend | Streamlit |
| Backend | Python |
| Data Processing | Pandas, NumPy, re, openpyxl, BytesIO |
| Machine Learning | scikit-learn, TextBlob |
| Visualization | Matplotlib, Seaborn, WordCloud |
| NLP & LLM Integration | Cohere API (Command-Light model) |

---

## 🧠 Project Architecture



WhatsApp Chat Analyzer
│
├── 📄 WhatsAppChat to csv.py      # Converts raw WhatsApp .txt to structured CSV/Excel
├── 📄 ChatAnalyzer.py             # Streamlit dashboard with ML and Cohere integration
│
├── 📊 cleaned_messages.csv        # Output data after preprocessing
│
├── 📁 assets/                     # (Optional) images, wordclouds, icons
│
├── requirements.txt               # Python dependencies
└── README.md





## ⚙️ Installation & Setup

1. *Clone the repository*
   bash
   git clone https://github.com/<your-username>/whatsapp-chat-analyzer.git
   cd whatsapp-chat-analyzer


2. **Create a virtual environment**

   bash
   python -m venv venv
   source venv/bin/activate       # For Linux/Mac
   venv\Scripts\activate          # For Windows
   

3. **Install dependencies**

   bash
   pip install -r requirements.txt
   

4. **Add your Cohere API key**

   * Open `ChatAnalyzer.py`
   * Replace `"your-api-key-here"` with your **Cohere API key**
     *(get it from [https://dashboard.cohere.com](https://dashboard.cohere.com))*

5. **Run the Streamlit App**

   bash
   streamlit run ChatAnalyzer.py
   

---

## 🧮 How It Works

1. **Convert Chat → CSV**

   * Use `WhatsAppChat to csv.py` to convert your exported WhatsApp `.txt` file.
   * The script automatically extracts `Date`, `Time`, `Name`, and `Message` fields and saves:

     * `cleaned_messages.csv`
     * `cleaned_messages.xlsx`

2. **Analyze in Dashboard**

   * Upload or place the CSV in the same directory as `ChatAnalyzer.py`
   * Run the Streamlit app to view dashboards such as:

     * Message distribution
     * Keyword frequency
     * Sentiment trends
     * Temporal activity (hourly, weekly)
     * Word clouds and ML predictions

3. **Chat with AI**

   * Navigate to **AI Chat** section in sidebar.
   * Ask natural questions about communication patterns — Cohere’s LLM generates insights in real time.

---

## 📊 Example Insights

| Metric             | Example Output          |
| ------------------ | ----------------------- |
| Most Active User   | Alice                   |
| Average Reply Time | 12.6 minutes            |
| Common Words       | love, night, miss, good |
| Peak Chat Hour     | 22:00 hrs               |
| Sentiment Score    | +0.43 (Positive)        |

---

## 🧾 Sample Commands

bash
# Convert WhatsApp chat to CSV
python "WhatsAppChat to csv.py"

# Launch the analyzer dashboard
streamlit run ChatAnalyzer.py


---

## 🧰 Dependencies


streamlit==1.39.0
pandas==2.2.2
numpy==1.26.4
scikit-learn==1.5.2
textblob==0.18.0.post0
matplotlib==3.9.2
seaborn==0.13.2
wordcloud==1.9.3
openpyxl==3.1.5
cohere==5.5.8
```

---

## 🧑‍💻 Author

*Developed by:* Love Mathur
*Email:* love.mathur@outlook.com
*Cohere Model Used:* command-light
*License:* MIT

---

## 🧾 Future Enhancements

* Integration with OpenAI GPT models.
* Advanced clustering of chat topics using sentence embeddings.
* Sentiment-over-time trend visualization.
* Real-time chat ingestion and dashboard auto-refresh.
