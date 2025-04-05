# 📱 WhatsApp Chat Analyzer

A powerful Streamlit web application to analyze WhatsApp chat data. Gain insights into your or your group's messaging habits through detailed visualizations such as word clouds, emoji usage, user statistics, timelines, and more.

## 🚀 Features

- 📊 **Top Statistics**: Number of messages, words, media shared, and links.
- 👥 **Most Active Users**: Analyze who talks the most in the group.
- 🌐 **Word Cloud**: Visualize frequently used words.
- 🗣️ **Most Common Words**: Bar chart of the top 20 words (excluding stopwords).
- 😄 **Emoji Usage**: See which emojis are used the most.
- 📅 **Daily Timeline**: View chat activity over time.
- 📆 **Weekly & Monthly Activity Maps**: Understand day-wise and month-wise activity.
- 🔥 **Activity Heatmap**: Analyze chat behavior across times of day.
- 📏 **Message Length Distribution**: See how long your messages typically are.


## 🧠 How it Works

1. **Upload Chat File**: Export your WhatsApp chat from your phone (without media) and upload the `.txt` file.
2. **Preprocessing**: The chat file is cleaned and structured using `preprocessor.py`.
3. **Analysis**: Various helper functions from `helper.py` compute insights and generate plots using libraries like `matplotlib`, `seaborn`, and `plotly`.
4. **Visualization**: Streamlit renders everything on an interactive dashboard.

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
``` 

### 2. Install Dependencies
Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required packages 
```bash
pip install -r requirements.txt
```

Install requirements
```bash
pip install streamlit pandas matplotlib seaborn plotly wordcloud emoji urlextract
```

### 3. Run the application 
```bash
streamlit app.py
```


## 📂 How to Export WhatsApp Chat
Open the individual or group chat in WhatsApp.

Tap the three-dot menu > More > Export Chat.

Choose Without Media.

Send the .txt file to your computer or email.

## 📌 Notes
The app currently supports English chats only.

Stopwords can be customized via the stopwords.txt file.

Media messages are recognized via <Media omitted> tag (based on WhatsApp export format).


