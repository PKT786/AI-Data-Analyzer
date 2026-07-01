# =====================================================
# PUNIT AI DATA ANALYZER V5
# PART 1 - UI + UPLOAD + DATA CLEANING
# =====================================================


import streamlit as st
import pandas as pd
import numpy as np
import os
import random
from datetime import datetime



# =====================================================
# PAGE CONFIG
# =====================================================


st.set_page_config(

    page_title="Punit AI Data Analyzer",

    page_icon="📊",

    layout="wide"

)



# =====================================================
# SESSION STORAGE
# =====================================================


if "df" not in st.session_state:

    st.session_state.df = None



if "clean_df" not in st.session_state:

    st.session_state.clean_df = None



if "charts" not in st.session_state:

    st.session_state.charts = []




# =====================================================
# CUSTOM CSS
# =====================================================


st.markdown(

"""

<style>


.main-title{

font-size:48px;

font-weight:800;

color:#1E293B;

}



.subtitle{

font-size:20px;

color:#475569;

}



.card{


background:white;

padding:25px;

border-radius:20px;

box-shadow:0px 5px 25px rgba(0,0,0,0.08);

}



.metric-card{


background:#F8FAFC;

padding:20px;

border-radius:15px;

text-align:center;

}



</style>


""",

unsafe_allow_html=True

)





# =====================================================
# HEADER
# =====================================================



col1,col2 = st.columns([1,5])



with col1:


    logo="assets/punit_logo.png"


    if os.path.exists(logo):

        st.image(

            logo,

            width=120

        )

    else:

        st.write("📊")



with col2:


    st.markdown(

    """

    <div class="main-title">

    Punit AI Data Analyzer 🚀

    </div>


    <div class="subtitle">

    Transform raw data into insights, charts and dashboards using AI

    </div>


    """,

    unsafe_allow_html=True

    )





st.divider()





# =====================================================
# HERO SECTION
# =====================================================


hero1,hero2 = st.columns([1,1])



with hero1:


    st.markdown(

    """

    <div class="card">


    <h2>

    Welcome to Punit AI Analyzer 🤖

    </h2>



    <p>

    Upload your Excel or CSV file and get:


    </p>


    <ul>


    <li>🧹 Automatic data cleaning</li>

    <li>📊 Professional charts</li>

    <li>📈 AI dashboard creation</li>

    <li>🤖 Business insights</li>

    <li>📄 Reports download</li>


    </ul>



    </div>


    """,

    unsafe_allow_html=True

    )





with hero2:


    st.info(

    """

    Supported:


    📊 Excel

    📄 CSV

    📈 Sales Reports

    💼 Business Data

    📉 Analytics Data


    """

    )





st.divider()






# =====================================================
# FILE UPLOAD
# =====================================================


st.subheader(

"📂 Upload Your Dataset"

)



uploaded_file = st.file_uploader(

"Upload Excel or CSV",

type=[

"xlsx",

"xls",

"csv"

]

)





if uploaded_file:



    try:



        if uploaded_file.name.endswith(".csv"):


            df=pd.read_csv(

                uploaded_file

            )


        else:


            df=pd.read_excel(

                uploaded_file

            )



        st.session_state.df=df



        st.success(

        "Dataset uploaded successfully 🚀"

        )



    except Exception as e:


        st.error(

        f"Upload error: {e}"

        )





# =====================================================
# DATA PREVIEW
# =====================================================



if st.session_state.df is not None:



    df=st.session_state.df



    st.subheader(

    "👀 Dataset Preview"

    )



    st.dataframe(

        df.head(),

        use_container_width=True

    )





    # Metrics


    c1,c2,c3=st.columns(3)



    with c1:


        st.metric(

        "Rows",

        df.shape[0]

        )



    with c2:


        st.metric(

        "Columns",

        df.shape[1]

        )



    with c3:


        missing=df.isnull().sum().sum()



        st.metric(

        "Missing Values",

        missing

        )





    st.divider()





    # =================================================
    # DATA CLEANING
    # =================================================


    st.subheader(

    "🧹 Data Cleaning Engine"

    )




    if st.button(

    "Clean My Data 🚀"

    ):



        clean=df.copy()



        # remove empty columns

        clean.dropna(

            axis=1,

            how="all",

            inplace=True

        )



        # remove duplicate rows

        clean.drop_duplicates(

            inplace=True

        )



        # fill missing values


        for col in clean.columns:


            if clean[col].dtype=="object":


                clean[col].fillna(

                    "Unknown",

                    inplace=True

                )


            else:


                clean[col].fillna(

                    clean[col].median(),

                    inplace=True

                )




        st.session_state.clean_df=clean



        st.session_state.df=clean



        st.success(

        "Data cleaned successfully ✅"

        )





    if st.session_state.clean_df is not None:



        clean=st.session_state.clean_df



        quality=round(

        (

        1 -

        (

        clean.isnull().sum().sum()

        /

        (clean.shape[0]*clean.shape[1])

        )

        )

        *

        100

        ,

        2

        )



        st.metric(

        "Data Quality Score",

        f"{quality}%"

        )





        st.dataframe(

        clean.head(),

        use_container_width=True

        )



# =====================================================
# END PART 1
# =====================================================
