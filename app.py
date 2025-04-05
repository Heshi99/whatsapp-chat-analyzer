import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")
st.markdown("<h1 style='text-align: center; color: #3A6EA5;'>📱 WhatsApp Chat Analyzer</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.title("🔍 Analyze Your Chat")
    uploaded_file = st.file_uploader("📂 Upload your WhatsApp chat file")

if uploaded_file:
    data = uploaded_file.getvalue().decode("utf-8")
    df = preprocessor.preprocess(data)
    st.success("✅ Chat file successfully processed!")

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("📌 Select user to analyze", user_list)

    if st.sidebar.button("Show Analysis"):
        st.markdown("## ✨ Top Statistics")
        num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Messages", num_messages)
        col2.metric("Words", words)
        col3.metric("Media Shared", num_media)
        col4.metric("Links Shared", num_links)

        st.markdown("---")

        if selected_user == "Overall":
            st.subheader("👥 Most Active Users")
            x, new_df = helper.most_busy_user(df)
            fig1, ax1 = plt.subplots()
            ax1.bar(x.index, x.values, color='green')
            plt.xticks(rotation='vertical')
            col1, col2 = st.columns(2)
            col1.pyplot(fig1)
            col2.dataframe(new_df)

        st.markdown("---")

        st.subheader("🌐 Word Cloud")
        wc = helper.create_wordccloud(selected_user, df)
        fig2, ax2 = plt.subplots()
        ax2.imshow(wc)
        ax2.axis("off")
        st.pyplot(fig2)

        st.subheader("🗣️ Most Common Words")
        common_words_df = helper.most_common_words(selected_user, df)
        fig3 = px.bar(common_words_df, x=0, y=1, labels={'0': 'Word', '1': 'Count'}, color=1, color_continuous_scale='Agsunset')
        st.plotly_chart(fig3)

        st.markdown("---")

        st.subheader("😄 Emoji Usage")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        col1.dataframe(emoji_df)
        col2.plotly_chart(px.pie(emoji_df, names=0, values=1, title='Emoji Distribution'))

        st.markdown("---")

        st.subheader("📅 Daily Activity Timeline")
        daily_df = helper.daily_timeline(selected_user, df)
        st.line_chart(daily_df.set_index('date')['message'])

        st.subheader("📆 Weekly Activity Map")
        st.plotly_chart(px.bar(helper.week_activity(selected_user, df), x='day_name', y='message', title='Weekly Activity'))

        st.subheader("📆 Monthly Activity Map")
        st.plotly_chart(px.bar(helper.month_activity(selected_user, df), x='month_year', y='count', title='Monthly Activity'))

        st.subheader("📊 Activity Heatmap")
        fig4 = plt.figure(figsize=(10, 6))
        sns.heatmap(helper.activity_heatmap(selected_user, df), cmap="YlGnBu")
        st.pyplot(fig4)

        st.subheader("📏 Message Length Distribution")
        fig5 = px.histogram(df[df['user'] == selected_user]['message'].str.len(), nbins=30)
        st.plotly_chart(fig5)
