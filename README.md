#Resume Reader (Uses Python and NLP)


#Project Goals:
This project was started to experiment with NLP models and PDF extraction. This was meant 
so that I could experiment with the behaviour of this NLP model and help me understand what the process
text classification is for them.


This helps extract key data from a resume, such as:
- Name
- Email
- Skills
- Graduation Year

Using PDF extraction and an NLP neural network to find these keywords in text.
As this is still experimental, accuracy can depend on the resume's format 

#How to run:
1: Install dependencies
- pip install PyMuPDF spacy
- python -m spacy download en_core_web_sm  #This is the neural network

2: Place the Resume in the same directory as the program

3: Run python Resume_reader.py

#Limitations and Future Work:
- uses word banks to look for these keywords, and if it is not in the word bank, it won't find it
- Find better support for all resume formatting types
- more accurate skill classification


-----------------------------------------------------------------------------------------------------------------------



#Stock Displayer (Streamlit and Yahoo Finance)


#Project Goals:

This project that I had in mind was to learn how to build an interactive app that explores these financial indicators and market behaviour. 
The current prototype mainly focused on data collection and moving averages, but in the future, I hope to implement more features, including
candlestick charts, and more predictive indicators.

An interactive dashboard that helps visualize stock price history over time. This includes:
- ticker name (eg. AAPL, TSLA)
- Stock Date Range
- Display Moving Average Line
- Ability to download the data as csv


#How to run:
1: Install dependencies
- pip install streamlit yfinance plotly pandas

2: Run on terminal: streamlit run financial_dashboard.py


#Future Improvements:
- fixing the graph to show the data and the moving average line
- adding candlesticks
- making the dashboard look better



-----------------------------------------------------------------------------------------------------------------------------



#Youtube Transcripter (YT API and Streamlit)


#Project Goals

This was a collaborative project, and it was just something simple so that I could get used to collaborating with others
on GitHub. It also improved my communication skills as we used Notion to brainstorm ideas and gave each of us tasks 
to accomplish.


Backend fetches transcripts using YouTube video IDs, using an API, and it combines the chunks to create the transcript. Frontend
uses Streamlit to provide a simple user interface where you can input the URL of the YouTube videos. 


#How to run: 
1: Install dependencies
pip install youtube-transcript-api, streamlit

2: In terminal: streamlit run frontend.py


#Future Improvements:
- making the interface look better
- add a button to summarize the transcript
- combine transcripts more efficiently





