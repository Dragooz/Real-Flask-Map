import pandas as pd
import os
import plotly
import plotly.graph_objs as go

# Load data that we will use.
articleData = pd.read_csv(
    os.getcwd() + "/articles/articleInfo.csv")
# information about timesData
articleData.info()
articleData.head() 

# prepare data frames
dfArticle = articleData.iloc[:, :]
print(dfArticle)

# create trace1
trace1 = go.Bar(
    x=dfArticle.articles,
    y=dfArticle.word_count,
    name="Word Count after removing stop words",
    marker=dict(color='white',
                line=dict(color='grey', width=1.5)),
    text='Word Count after removing stop words')
# create trace2 
trace2 = go.Bar(
    x=dfArticle.articles,
    y=dfArticle.negative_words,
    name="Negative words",
    marker=dict(color='white',
                line=dict(color='red', width=1.5)),
    text='Negative words')

trace3 = go.Bar(
    x=dfArticle.articles,
    y=dfArticle.positive_words,
    name="Positive words",
    marker=dict(color='white',
                line=dict(color='green', width=1.5)),
    text='Positive words')

data = [trace1, trace2, trace3]
layout = go.Layout(
    barmode="group",
    title="Sentiment Analysis",
    xaxis=dict(title='Related Articles'),
    yaxis=dict(title='Word Count'),

)
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='sentiment_analysis.html')
