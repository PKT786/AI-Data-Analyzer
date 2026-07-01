import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from groq import Groq
import os
from datetime import datetime



# ============================
# PAGE CONFIG
# ============================

st.set_page_config(
    page_title="Punit AI Data Analyzer",
    page_icon="📊",
    layout="wide"
)



# ============================
# GROQ
# ============================

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)



# ============================
# BRANDING
# ============================


if os.path.exists("assets/punit_logo.png"):

    st.image(
        "assets/punit_logo.png",
        width=180
    )


st.title(
    "📊 Punit AI Data Analyzer"
)


st.markdown(
"""
### Transform your Excel & CSV files into insights 🚀


Upload data → Clean → Analyze → Visualize → Generate AI Insights


Powered by **Punit Tech Hub**
"""
)



st.divider()




# ============================
# FILE UPLOAD
# ============================


uploaded_file = st.file_uploader(

    "Upload Excel or CSV file",

    type=[
        "csv",
        "xlsx"
    ]

)



if uploaded_file:



    # -------------------------
    # READ FILE
    # -------------------------


    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)


    else:

        df = pd.read_excel(uploaded_file)



    st.success(
        "File uploaded successfully"
    )



    original_df=df.copy()



    # ============================
    # DATA OVERVIEW
    # ============================


    st.subheader(
        "📌 Dataset Overview"
    )


    c1,c2,c3,c4 = st.columns(4)



    c1.metric(
        "Rows",
        df.shape[0]
    )


    c2.metric(
        "Columns",
        df.shape[1]
    )


    c3.metric(
        "Duplicates",
        df.duplicated().sum()
    )


    c4.metric(
        "Missing Values",
        df.isna().sum().sum()
    )





    # ============================
    # DATA CLEANING
    # ============================


    st.divider()


    st.subheader(
        "🧹 Data Cleaning"
    )



    if st.button(
        "Clean Data"
    ):



        df=df.drop_duplicates()



        for col in df.columns:


            if df[col].isna().sum()>0:


                if df[col].dtype=="object":

                    df[col]=df[col].fillna(
                        "Unknown"
                    )

                else:

                    df[col]=df[col].fillna(
                        df[col].median()
                    )



        st.session_state.cleaned=df



        st.success(
            "Data cleaned successfully"
        )





    if "cleaned" in st.session_state:


        df=st.session_state.cleaned



        st.dataframe(
            df.head(10)
        )






    # ============================
    # DATA TYPES
    # ============================


    st.divider()


    st.subheader(
        "🔍 Column Information"
    )


    info=pd.DataFrame(

    {

    "Column":df.columns,

    "Data Type":
    df.dtypes.astype(str),

    "Missing":
    df.isna().sum()

    }

    )


    st.dataframe(info)






    # ============================
    # AI INSIGHTS
    # ============================


    st.divider()


    st.subheader(
        "🤖 AI Data Insights"
    )



    if st.button(
        "Generate AI Insights"
    ):



        summary = df.describe(
            include="all"
        ).to_string()



        prompt=f"""

You are a senior data analyst.


Analyze this dataset:

{summary}


Provide:

1. Important patterns

2. Business insights

3. Recommendations


Keep it simple.


"""



        response=client.chat.completions.create(


            model=
            "llama-3.1-8b-instant",


            messages=[

            {

            "role":"user",

            "content":prompt

            }

            ]

        )


        st.info(

            response.choices[0].message.content

        )







    # ============================
    # CHART BUILDER
    # ============================


    st.divider()


    st.subheader(
        "📈 Interactive Chart Builder"
    )



    chart_type = st.selectbox(

        "Select Chart Type",

        [

        "Bar Chart",

        "Line Chart",

        "Pie Chart",

        "Scatter Plot",

        "Histogram",

        "Box Plot"

        ]

    )




    columns=list(df.columns)



    x_axis=st.selectbox(

        "Select X Axis",

        columns

    )



    y_axis=None



    if chart_type not in [

        "Pie Chart",

        "Histogram"

    ]:


        y_axis=st.selectbox(

            "Select Y Axis",

            columns

        )






    if st.button(
        "Create Chart"
    ):


        try:



            if chart_type=="Bar Chart":


                fig=px.bar(

                    df,

                    x=x_axis,

                    y=y_axis

                )



            elif chart_type=="Line Chart":


                fig=px.line(

                    df,

                    x=x_axis,

                    y=y_axis

                )



            elif chart_type=="Pie Chart":


                fig=px.pie(

                    df,

                    names=x_axis

                )



            elif chart_type=="Scatter Plot":


                fig=px.scatter(

                    df,

                    x=x_axis,

                    y=y_axis

                )



            elif chart_type=="Histogram":


                fig=px.histogram(

                    df,

                    x=x_axis

                )



            else:


                fig=px.box(

                    df,

                    x=x_axis,

                    y=y_axis

                )



            st.plotly_chart(

                fig,

                use_container_width=True

            )



        except Exception as e:


            st.error(
                str(e)
            )







    # ============================
    # DOWNLOAD
    # ============================


    st.divider()


    st.subheader(
        "⬇️ Download"
    )



    csv=df.to_csv(
        index=False
    ).encode()



    st.download_button(

        "Download Cleaned CSV",

        csv,

        "cleaned_data.csv",

        "text/csv"

    )



else:


    st.info(

    """
Upload a file to start analysis.

Supported:

✔ Excel

✔ CSV

"""
    )



# ============================
# FOOTER
# ============================


st.divider()


st.caption(

"🚀 Punit Tech Hub | AI Data Analytics Platform"

)
