
import streamlit as st
import pandas as pd

st.title('WildChat Model Welfare Emotions Dashboard')

df = pd.read_csv('model_emotion_sample.csv')
st.write('Sample data:')
st.dataframe(df.head(20))

st.image('emotion_distribution_sample.png', caption='Distribution of Model Emotional States (Sample)')
