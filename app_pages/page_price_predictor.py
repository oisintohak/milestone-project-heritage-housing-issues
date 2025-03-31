import streamlit as st
import pandas as pd
from src.data_management import load_house_data, load_pkl_file
from src.machine_learning.predictive_analysis_ui import (predict_sale_price)

def page_price_predictor_body():

    

    # load predict sale price files
    version = 'v1'
    sale_price_pipeline = load_pkl_file(
        f"outputs/ml_pipeline/predict_sale_price/{version}/regressor_pipeline.pkl")
    
    sale_price_features = (pd.read_csv(f"outputs/ml_pipeline/predict_sale_price/{version}/X_train.csv")
                       .columns
                       .to_list()
                       )
    # ['GrLivArea', 'TotalBsmtSF', 'YearBuilt']
    st.write("### Prospect Churnometer Interface")
    st.info(
        f"The client wants to be able to predict the sale price of a house "
    )
    st.write("---")
    df = pd.read_csv("inputs/datasets/raw/house_price_data/inherited_houses.csv")
    st.write('***inherited houses:***')
    print('df')

    print(df.info())
    print('enddf')
    # st.write(df.info())
    filtered_df = df.filter(sale_price_features)
    print(filtered_df.info())
    # print(df.loc[1])
    for i in range(len(filtered_df)):
        
        st.write(f'inherited house {i}:')
        test_data_set = pd.DataFrame(filtered_df.loc[i]).transpose()
        st.write(test_data_set)
        print(test_data_set)
        prediction = sale_price_pipeline.predict(test_data_set)
        st.write('prediction:')
        st.write(prediction)
            

    # Generate Live Data
    check_variables_for_UI(sale_price_features)
    st.write('enter values to predict a price:')
    X_live = DrawInputsWidgets()

    # predict on live data
    if st.button("Run Predictive Analysis"):
        # churn_prediction = predict_churn(
        #     X_live, churn_features, churn_pipe_dc_fe, churn_pipe_model)

        # if churn_prediction == 1:
        st.write('input data set:')
        st.write(X_live)
        st.write('predicted price:')
        predict_sale_price(X_live, sale_price_features,
                        sale_price_pipeline)
    




def check_variables_for_UI(sale_price_features):
    import itertools

    # The widgets inputs are the features used in all pipelines (tenure, churn, cluster)
    # We combine them only with unique values
    combined_features = set(
        list(
            itertools.chain(sale_price_features)
        )
    )
    st.write(
        f"* There are {len(combined_features)} features for the UI: \n\n {combined_features}")


def DrawInputsWidgets():

    # load dataset
    df = load_house_data()
    percentageMin, percentageMax = 0.4, 2.0

# we create input widgets only for 6 features
    col1, col2, col3 = st.beta_columns(3)

    # We are using these features to feed the ML pipeline - values copied from check_variables_for_UI() result

    # create an empty DataFrame, which will be the live data
    X_live = pd.DataFrame([], index=[0])

    # from here on we draw the widget based on the variable type (numerical or categorical)
    # and set initial values
    with col1:
        feature = "GrLivArea"
        st_widget = st.number_input(
            label=feature,
            min_value=df[feature].min()*percentageMin,
            max_value=df[feature].max()*percentageMax,
            value=df[feature].median()
        )
    X_live[feature] = st_widget

    with col2:
        feature = "TotalBsmtSF"
        st_widget = st.number_input(
            label=feature,
            min_value=df[feature].min()*percentageMin,
            max_value=df[feature].max()*percentageMax,
            value=df[feature].median()
        )
    X_live[feature] = st_widget

    with col3:
        feature = "YearBuilt"
        st_widget = st.number_input(
            label=feature,
            min_value=df[feature].min()*percentageMin,
            max_value=df[feature].max()*percentageMax,
            value=df[feature].median()
        )
    X_live[feature] = st_widget

    

    # st.write(X_live)

    return X_live
