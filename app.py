import streamlit as st
import pandas as pd
import plotly.express as px
import random
import io
import os
from datetime import datetime

from groq import Groq


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Punit AI Data Analyzer",
    page_icon="📊",
    layout="wide"
)


# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

.main {
background:#f7f9fc;
}

.hero {

padding:35px;
border-radius:20px;
background:linear-gradient(
135deg,#ffffff,#eef5ff
);

}


.title {

font-size:48px;
font-weight:800;

}


.card {

padding:20px;
border-radius:15px;
background:white;
box-shadow:0px 5px 20px #ddd;

}


button {

border-radius:10px!important;

}

</style>

""",unsafe_allow_html=True)



# -----------------------------
# LOGO
# -----------------------------

logo_path="assets/punit_logo.png"


col1,col2=st.columns([1,6])


with col1:

    if os.path.exists(logo_path):

        st.image(
            logo_path,
            width=100
        )


with col2:

    st.markdown(
    """
    <h1>
    Punit AI Data Analyzer 🚀
    </h1>
    """,
    unsafe_allow_html=True
    )



# -----------------------------
# HERO
# -----------------------------


st.markdown(
"""
<div class="hero">

<h2>
Analyze your Excel & CSV data using AI
</h2>


<p>
Upload → Clean → Analyze → Visualize → Create Dashboard
</p>


<ul>

<li>🧹 Automatic data cleaning</li>

<li>📊 Professional charts</li>

<li>🤖 AI business insights</li>

<li>🎨 Dynamic dashboards</li>

</ul>


</div>

""",
unsafe_allow_html=True
)



# -----------------------------
# FILE UPLOAD
# -----------------------------


st.divider()


uploaded_file = st.file_uploader(
"Upload Excel or CSV file",
type=["xlsx","csv"]
)



# -----------------------------
# LOAD DATA
# -----------------------------


if uploaded_file:


    if uploaded_file.name.endswith(".csv"):

        df=pd.read_csv(uploaded_file)

    else:

        df=pd.read_excel(uploaded_file)



    st.success(
    "File uploaded successfully"
    )



    # -------------------------
    # OVERVIEW
    # -------------------------

    st.subheader(
    "📌 Dataset Overview"
    )


    c1,c2,c3,c4=st.columns(4)



    quality = round(
        (1-(df.isnull().sum().sum()/(df.size)))*100
    )


    c1.metric(
    "Rows",
    df.shape[0]
    )


    c2.metric(
    "Columns",
    df.shape[1]
    )


    c3.metric(
    "Data Quality",
    f"{quality}%"
    )


    c4.metric(
    "Duplicates",
    df.duplicated().sum()
    )



    # -------------------------
    # CLEAN DATA
    # -------------------------


    st.divider()


    st.subheader(
    "🧹 AI Data Cleaning"
    )


    if st.button(
    "✨ Clean Dataset"
    ):


        clean=df.copy()


        clean.drop_duplicates(
            inplace=True
        )


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



        st.session_state["clean"]=clean


        st.success(
        "Dataset cleaned successfully"
        )



    if "clean" in st.session_state:


        df=st.session_state["clean"]



    # -------------------------
    # DATA PREVIEW
    # -------------------------


    st.subheader(
    "Preview"
    )

    st.dataframe(
        df.head(20),
        use_container_width=True
    )



    # -------------------------
    # CHART BUILDER
    # -------------------------


    st.divider()


    st.subheader(
    "📊 Chart Studio"
    )



    chart_type=st.selectbox(

    "Select Chart Type",

    [
    "Bar Chart",
    "Line Chart",
    "Pie Chart",
    "Scatter Chart"
    ]

    )



    cols=df.columns.tolist()



    x=st.selectbox(
    "Select X Axis",
    cols
    )



    y=st.selectbox(
    "Select Y Axis",
    cols
    )




    if st.button(
    "Generate Chart 🚀"
    ):


        if chart_type=="Bar Chart":


            fig=px.bar(
            df,
            x=x,
            y=y,
            template="plotly_dark"
            )


        elif chart_type=="Line Chart":


            fig=px.line(
            df,
            x=x,
            y=y,
            template="plotly_dark"
            )


        elif chart_type=="Pie Chart":


            fig=px.pie(
            df,
            names=x,
            values=y,
            template="plotly_dark"
            )


        else:


            fig=px.scatter(
            df,
            x=x,
            y=y,
            template="plotly_dark"
            )



        st.plotly_chart(
        fig,
        use_container_width=True
        )

        st.session_state["chart"]=fig



    # -------------------------
    # DASHBOARD BUILDER
    # -------------------------


    st.divider()


    st.subheader(
    "🎨 AI Dashboard Builder"
    )



    themes=[

    "plotly_dark",
    "ggplot2",
    "seaborn",
    "presentation"

    ]



    theme=random.choice(themes)



    if st.button(
    "🚀 Generate Dashboard"
    ):


        num=df.select_dtypes(
        include="number"
        ).columns



        if len(num)>0:


            fig=px.bar(

            df,

            x=df.columns[0],

            y=num[0],

            template=theme,

            title="Punit AI Dashboard"

            )


            st.plotly_chart(
            fig,
            use_container_width=True
            )


            st.session_state["dashboard"]=fig



        else:


            st.warning(
            "No numeric column available"
            )



    # -------------------------
    # AI INSIGHTS
    # -------------------------


    st.divider()


    st.subheader(
    "🤖 AI Business Insights"
    )



    if st.button(
    "Generate AI Insights"
    ):


        try:


            client=Groq(
            api_key=st.secrets["GROQ_API_KEY"]
            )



            prompt=f"""

Analyze this dataset:

Columns:
{list(df.columns)}

Give business insights,
trends and recommendations.

"""



            response=client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

            {
            "role":"user",
            "content":prompt
            }

            ]

            )



            st.write(

            response.choices[0].message.content

            )


        except Exception as e:


            st.error(
            "AI service unavailable"
            )



    # -------------------------
    # DOWNLOAD CLEAN FILE
    # -------------------------


    st.divider()


    output=io.BytesIO()


    df.to_excel(
    output,
    index=False
    )



    st.download_button(

    "⬇ Download Clean Excel",

    output.getvalue(),

    "clean_dataset.xlsx"

    )



else:


    st.info(
    "Upload your dataset to start analysis 🚀"
    )
