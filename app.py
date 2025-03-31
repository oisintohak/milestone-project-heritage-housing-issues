import streamlit as st
from app_pages.multipage import MultiPage

# load pages scripts
from app_pages.page_summary import page_summary_body
from page_price_predictor import page_price_predictor_body

app = MultiPage(app_name= "Sale Price Predictor") # Create an instance of the app 

# Add your app pages here using .add_page()
app.add_page("Quick Project Summary", page_summary_body)
app.add_page("Sale Price Predictor", page_price_predictor_body)

app.run() # Run the  app
