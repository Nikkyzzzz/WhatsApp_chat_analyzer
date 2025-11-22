# 📊 WhatsApp Chat Analyzer Dashboard

A powerful **Streamlit-based dashboard** to analyze WhatsApp chat exports — uncovering communication trends, sentiment insights, keyword usage, relationship dynamics, and more!

This project includes automated chat parsing + an interactive data analytics dashboard.
It supports word clouds, reply-time analysis, conversation flow, temporal behavior, and even basic ML-based insights.

---

## 🚀 Features

### ✔ WhatsApp Chat → Structured Data

Convert raw `.txt` chat exports into CSV/Excel format using the script


### ✔ Analytics & Visualizations Dashboard

Built with Streamlit, offering:

| Module             | Insights                                       |
| ------------------ | ---------------------------------------------- |
| Overview           | Total messages, active days, chat highlights   |
| Basic Stats        | Who texts more? Message length distribution    |
| Keyword Analysis   | Common phrases usage count                     |
| Temporal Patterns  | Hourly + weekday communication patterns        |
| Conversation Flow  | Reply-time analysis, conversation starters     |
| Word Clouds        | Personalized clouds for each participant       |
| Awards & Metrics   | Fun badges like *Chatterbox* & *Most Romantic* |
| ML Predictions     | Love message probability (demo model)          |
| AI Chat *(Cohere)* | Ask AI questions about your chat insights      |

Dashboard source:


---

## 🏗 Tech Stack

| Category             | Tools                          |
| -------------------- | ------------------------------ |
| Frontend UI          | Streamlit                      |
| Data Processing      | pandas, numpy                  |
| Visualization        | matplotlib, seaborn, wordcloud |
| Sentiment Analysis   | TextBlob                       |
| ML Models            | scikit-learn                   |
| Optional AI Querying | Cohere                         |

All dependencies:


---

## 📥 Installation & Setup

### 1️⃣ Clone repo

```bash
git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔄 Convert WhatsApp Chat File

Export your WhatsApp chat as `.txt`, name it `WhatsApp.txt`, then run:

```bash
python "WhatsappChat to csv.py"
```

This will generate:

```
cleaned_messages.csv
cleaned_messages.xlsx
```

---

## ▶ Run the Dashboard

Inside the project folder:

```bash
streamlit run "ChatAnalyzer.py"
```

Once launched, upload/ensure `cleaned_messages.csv` is available — analytics begin instantly!

---

## 🔐 Optional: AI Analysis Setup

To use Cohere-powered AI insights:

1. Create an API key → [https://dashboard.cohere.com](https://dashboard.cohere.com)
2. Add it to your Streamlit secrets:

```
.streamlit/secrets.toml
```

```toml
cohere_api_key="YOUR_API_KEY"
```

Or edit directly in the script.

---

## 📈 Example Insights You’ll Get

* Who initiates conversations more?
* Emotional positivity vs negativity over time
* Most active communication hours & days
* Keyword heatmap (Good morning / Sorry / Love etc.)
* Reply behavior — faster responder?
* Personalized word clouds
* Fun couple analytics 🥰

---

## 📌 Future Enhancements (Planned)

* More robust chat parser supporting multiple date formats
* Topic clustering using NLP
* Advanced sentiment trend forecasting
* Multi-chat comparison

---

## 👩‍💻 Author

**Love Mathur**
*Data Analyst & ML Developer*

---

If you'd like, I can also:

✨ Add screenshots to README
🧩 Bundle this as a deployable Streamlit Cloud app
🎨 Add a project logo & banner
🐳 Create Docker support
📦 Improve folder structure

