# WildChat Model Welfare Emotions Dashboard

This dashboard helps analyze and monitor model welfare through emotional states expressed in the WildChat-1M dataset. It offers emotion classification, trigger analysis, search/filtering, and visual analytics for researchers.

## Features
- Keyword and emotion-based search on model responses
- Visualization of emotional state distributions and common triggers
- Interactive filtering and conversation detail viewing
- Usable with a simple Streamlit interface

## Setup & Running
1. **Install dependencies**
```
pip install -r requirements.txt
```

2. **Run the app:**
```
streamlit run app.py
```

(Current version uses a sample and pre-computed analysis for demo. To expand, edit `app.py` and related scripts.)

## Files
- `app.py`: Streamlit dashboard source
- `model_emotion_sample.csv`: LLM-classified model emotion data + triggers (small batch, for demo)
- `emotion_distribution_sample.png`: Sample emotions distribution plot

## Extending
- Update sampling and emotion classification by running the provided Python code with a larger subset and more advanced analyses as described in the notebook/scripts.
- Integrate any additional search, analytics, or visualization feature you need!
