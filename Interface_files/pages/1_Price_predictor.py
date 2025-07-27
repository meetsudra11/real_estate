import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title = "Viz Demo")


# COLUMNS : property_type	sector	bedRoom	bathroom	balcony	agePossession	built_up_area	servant room	study room	furnishing_type	luxury_category	floor_category

with open('df.pkl','rb') as file: # read binary file
    df = pickle.load(file)

with open('pipeline.pkl','rb') as file: # read binary file
    pipeline = pickle.load(file)

st.header('Enter your requirements')

# property_type input
property_type = st.selectbox('property type', ['flat','house'])

# sector
sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))

# bedRoom
bedroom = float(st.selectbox('Number of Bedroom', sorted(df['bedRoom'].unique().tolist())))

# bathroom
bathroom = float(st.selectbox('Number of Bathroom', sorted(df['bathroom'].unique().tolist())))

# balcony
balcony = st.selectbox('Number of Balconies', sorted(df['balcony'].astype(str).unique().tolist()))


# agePossession
property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

# built_up_area
built_up_area = float(st.number_input('Built Up Area'))

# servant_room
servant_room = float(st.selectbox('Servant Room', [0.0,1.0]))

# study_room
study_room = float(st.selectbox('Study Room', [0.0,1.0]))

# furnishing_type
furnishing_type = st.selectbox('Furnishing type', sorted(df['furnishing_type'].unique().tolist()))

# luxury_category
luxury_category = st.selectbox('Luxury category', sorted(df['luxury_category'].unique().tolist()))

# floor_category
floor_category = st.selectbox('floor_category', sorted(df['floor_category'].unique().tolist()))
if st.button('Predict'):
    data = [[property_type, sector, bedroom, bathroom, balcony, property_age,
             built_up_area, servant_room, study_room, furnishing_type,
             luxury_category, floor_category]]

    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'study room',
               'furnishing_type', 'luxury_category', 'floor_category']

    one_df = pd.DataFrame(data, columns=columns)

    # ✅ Convert numeric columns to float
    one_df[['bedRoom', 'bathroom', 'built_up_area', 'servant room', 'study room']] = one_df[
        ['bedRoom', 'bathroom', 'built_up_area', 'servant room', 'study room']].astype(float)

    # ✅ Convert categorical columns to string
    cat_cols = ['property_type', 'sector', 'balcony', 'agePossession',
                'furnishing_type', 'luxury_category', 'floor_category']
    one_df[cat_cols] = one_df[cat_cols].astype(str)

    # ✅ Fill any NaNs
    one_df.fillna('Unknown', inplace=True)

    # Optional: show user inputs in a table
    st.write("Prediction Input:")
    st.dataframe(one_df)

    # ✅     Pre dict and show output
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22  # on considering that error is of 46 lacs

    # display
    st.text("The price of the flat is between {} and {} ".format(round(low,2),round(high,2)))

