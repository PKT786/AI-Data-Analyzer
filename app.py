# =====================================================
# PUNIT AI DATA ANALYZER V5
# PART 1
# UI + UPLOAD + CLEANING ENGINE
# =====================================================


import streamlit as st
import pandas as pd
import numpy as np
import os



# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Punit AI Data Analyzer",

    page_icon="📊",

    layout="wide"

)



# =====================================================
# SESSION STATE
# =====================================================


if "df" not in st.session_state:

    st.session_state.df = None



if "clean_df" not in st.session_state:

    st.session_state.clean_df = None



if "charts" not in st.session_state:

    st.session_state.charts = []




# =====================================================
# PREMIUM CSS
# =====================================================


st.markdown(

"""

<style>


.main-title{

font-size:45px;

font-weight:800;

}



.sub-title{

font-size:20px;

color:#64748b;

}



.hero{


background:

linear-gradient(

135deg,

#0f172a,

#2563eb

);


padding:35px;

border-radius:25px;

color:white;


}



.card{


background:white;

padding:25px;

border-radius:18px;

box-shadow:

0px 5px 25px rgba(0,0,0,0.12);


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


    <div class="sub-title">

    AI powered Excel & CSV analytics platform

    </div>


    """,

    unsafe_allow_html=True

    )





st.divider()





# =====================================================
# HERO SECTION
# =====================================================


st.markdown(

"""

<div class="hero">


<h1>

Transform Data Into Decisions 🤖

</h1>


<p>


Upload your data → Clean → Analyze → Create Charts → Build Dashboard


</p>


</div>


""",

unsafe_allow_html=True

)





st.write("")





# =====================================================
# FILE UPLOAD
# =====================================================


st.subheader(

"📂 Upload Dataset"

)



uploaded_file = st.file_uploader(

"Upload Excel or CSV file",

type=[

"csv",

"xlsx",

"xls"

]

)





if uploaded_file:



    try:



        if uploaded_file.name.endswith(".csv"):


            data = pd.read_csv(

                uploaded_file

            )


        else:


            data = pd.read_excel(

                uploaded_file

            )



        st.session_state.df = data



        st.success(

        "Dataset uploaded successfully 🚀"

        )



    except Exception as e:



        st.error(

        f"File loading error: {e}"

        )





# =====================================================
# DATA ANALYSIS
# =====================================================



if st.session_state.df is not None:



    df = st.session_state.df



    st.subheader(

    "📌 Dataset Overview"

    )



    col1,col2,col3,col4 = st.columns(4)



    col1.metric(

    "Rows",

    df.shape[0]

    )



    col2.metric(

    "Columns",

    df.shape[1]

    )



    col3.metric(

    "Duplicate Rows",

    df.duplicated().sum()

    )



    col4.metric(

    "Missing Values",

    int(df.isnull().sum().sum())

    )





    st.subheader(

    "Preview"

    )



    st.dataframe(

    df.head(20),

    use_container_width=True

    )





    st.divider()






    # =================================================
    # CLEANING ENGINE
    # =================================================



    st.subheader(

    "🧹 AI Data Cleaning Engine"

    )





    if st.button(

    "✨ Clean My Data"

    ):



        clean = df.copy()



        # remove empty columns


        clean.dropna(

            axis=1,

            how="all",

            inplace=True

        )



        # remove duplicates


        clean.drop_duplicates(

            inplace=True

        )





        # handle missing values safely


        for col in clean.columns:



            if pd.api.types.is_numeric_dtype(

                clean[col]

            ):



                clean[col] = clean[col].fillna(

                    clean[col].median()

                )



            else:



                clean[col] = clean[col].fillna(

                    "Unknown"

                )





        # convert numeric text columns


        for col in clean.columns:



            try:



                converted = pd.to_numeric(

                    clean[col]

                )



                clean[col] = converted



            except:



                pass





        st.session_state.clean_df = clean


        st.session_state.df = clean





        st.success(

        "Cleaning completed successfully ✅"

        )







    # =================================================
    # CLEAN RESULT
    # =================================================


    if st.session_state.clean_df is not None:



        clean = st.session_state.clean_df



        quality = round(

            (

            1 -

            (

            clean.isnull().sum().sum()

            /

            max(clean.size,1)

            )

            )

            *

            100,

            2

        )



        st.metric(

        "Data Quality Score",

        f"{quality}%"

        )



        st.dataframe(

        clean.head(20),

        use_container_width=True

        )



else:


    st.info(

    "Please upload a file to start analysis 🚀"

    )



# =====================================================
# END PART 1
# =====================================================
