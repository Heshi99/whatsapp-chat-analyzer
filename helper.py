from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import numpy as np
from collections import Counter
import emoji

extractor=URLExtract()

def fetch_stats(selected_user,df):
    
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    #fetch the number of messages 
    num_messages = df.shape[0] 

    #fetch the total number of words
    words=[]  
    for message in df['message'] :
            words.extend(message.split())
    
    #fetch number of media messages 
    num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]

    #fetch number of links shareed
    links=[]
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_user(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percent'})
    return x,df

def create_wordccloud(selected_user,df):

    with open('stopwords.txt', 'r') as f:
        stop_words = f.read().splitlines() 
    
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    temp=df[df['user']!='group_notification']
    temp=temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_word(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return "".join(y)


    wc=WordCloud(width=500,height=500, min_font_size=10, background_color='white')
    temp['message']=temp['message'].apply(remove_stop_word)
    
    df_wc=wc.generate(temp['message'].str.cat(sep=""))
    return df_wc

def most_common_words(selected_user,df):
    
    with open('stopwords.txt', 'r') as f:
        stop_words = f.read().splitlines() 
    
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    temp=df[df['user']!='group_notification']
    temp=temp[temp['message'] != '<Media omitted>\n']

    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    most_common_df=pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]

    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])   
     
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def daily_timeline(user, df):
    if user != 'Overall':
        df = df[df['user'] == user]
    daily_timeline = df.groupby('date').count()['message'].reset_index()
    return daily_timeline

def week_activity(user, df):
    if user != 'Overall':
        df = df[df['user'] == user]
    week_df = df['day_name'].value_counts().reset_index()
    week_df.columns = ['day_name', 'message']
    return week_df

def month_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['month_year'] = df['date'].dt.to_period('M').astype(str)
    month_df = df.groupby('month_year').count()['message'].reset_index()
    month_df.rename(columns={'message': 'count'}, inplace=True)
    return month_df


def add_period_column(df):
    # Create 'period' column based on hour
    conditions = [
        (df['hour'] >= 5) & (df['hour'] < 12),  # Morning
        (df['hour'] >= 12) & (df['hour'] < 17), # Afternoon
        (df['hour'] >= 17) & (df['hour'] < 21), # Evening
        (df['hour'] >= 21) | (df['hour'] < 5)    # Night
    ]
    choices = ['Morning', 'Afternoon', 'Evening', 'Night']
    
    df['period'] = np.select(conditions, choices, default='Unknown')
    return df


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Add 'period' column to categorize hours into periods
    df = add_period_column(df)

    # Now, create the heatmap
    heatmap_data = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return heatmap_data


