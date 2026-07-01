import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from groq import Groq
from datetime import datetime
import os
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet



# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(

    page_title="Punit AI Data Analyzer",

    page_icon="📊",

    layout="wide"

)



# ===============================
# CUSTOM CSS
# ===============================


st.markdown("""

<style>


.main{

background:#0e1117;

}


.card{

background:#1c1f26;

padding:20px;

border-radius:15px;

border:1px solid #333;

}



h1{

color:white;

}


</style>


""",
unsafe_allow_html=True)




# ===============================
# GROQ
# ===============================


client = Groq(

api_key=st.secrets["GROQ_API_KEY"]

)




# ===============================
# LOGO
# ===============================


if os.path.exists(
"assets/punit_logo.png"
):

    st.image(

        "assets/punit_logo.png",

        width=220

    )



st.title(
"📊 Punit AI Data Analyzer"
)


st.caption(

"Transform your Excel & CSV files into AI powered business insights"

)



# ===============================
# SIDEBAR
# ===============================


with st.sidebar:


    st.header(
    "🚀 Punit AI Analytics"
    )


    st.write(

    """
    
    Features:

    📂 Upload Data

    🧹 Cleaning

    📊 Charts

    🤖 AI Insights

    📄 Reports

    """

    )


    st.divider()


    st.markdown(

    """

    Learn More:


    📊 Excel Tutorials

    🤖 AI Resources

    💻 Mainframe Guides


    """

    )





# ===============================
# UPLOAD
# ===============================


file = st.file_uploader(

"Upload Excel / CSV",

type=[
"csv",
"xlsx"
]

)



if file:



    if file.name.endswith(".csv"):


        df=pd.read_csv(file)


    else:


        df=pd.read_excel(file)



    original=df.copy()



    st.success(
    "Dataset Loaded Successfully"
    )



    # ===============================
    # KPI CARDS
    # ===============================


    st.subheader(
    "📌 Dataset Overview"
    )


    c1,c2,c3,c4=st.columns(4)



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

    "Missing",

    int(df.isna().sum().sum())

    )



    # ===============================
    # HEALTH SCORE
    # ===============================


    score=100


    score-=df.isna().sum().sum()*0.2


    score-=df.duplicated().sum()*0.1


    score=max(
    0,
    int(score)
    )



    st.info(

    f"""

    Dataset Health Score:

    ## {score}/100

    """

    )




    # ===============================
    # CLEAN DATA
    # ===============================


    st.divider()


    st.subheader(
    "🧹 Data Cleaning"
    )



    if st.button(
    "Clean Dataset"
    ):



        df=df.drop_duplicates()



        for col in df.columns:


            if df[col].isnull().sum()>0:


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
        "Cleaning Completed"
        )




    if "cleaned" in st.session_state:

        df=st.session_state.cleaned



    st.dataframe(
    df.head()
    )




    # ===============================
    # AI INSIGHTS
    # ===============================


    st.divider()


    st.subheader(
    "🤖 AI Business Insights"
    )



    if st.button(
    "Generate Insights"
    ):



        summary=df.describe(
        include="all"
        ).to_string()



        prompt=f"""


Act as senior data analyst.


Analyze:

{summary}


Give:

- Key findings

- Trends

- Recommendations


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



        st.success(

        response.choices[0].message.content

        )





    # ===============================
    # ASK YOUR DATA
    # ===============================


    st.divider()


    st.subheader(
    "💬 Ask Your Data"
    )


    question=st.text_input(

    "Example: Which product has highest sales?"

    )



    if question:



        prompt=f"""

Dataset:

{df.head(20).to_string()}


Question:

{question}


Answer clearly.

"""



        result=client.chat.completions.create(


        model="llama-3.1-8b-instant",


        messages=[

        {

        "role":"user",

        "content":prompt

        }

        ]


        )



        st.write(

        result.choices[0].message.content

        )





    # ===============================
    # CHART BUILDER
    # ===============================


    st.divider()


    st.subheader(
    "📊 Visualization Studio"
    )



    chart=st.selectbox(

    "Choose Chart",

    [

    "Bar",

    "Line",

    "Pie",

    "Scatter",

    "Histogram",

    "Box"

    ]

    )



    col1,col2=st.columns(2)


    x=col1.selectbox(

    "X Axis",

    df.columns

    )


    y=col2.selectbox(

    "Y Axis",

    df.columns

    )



    if st.button(
    "Create Chart"
    ):



        if chart=="Bar":

            fig=px.bar(
            df,
            x=x,
            y=y
            )


        elif chart=="Line":

            fig=px.line(
            df,
            x=x,
            y=y
            )


        elif chart=="Pie":

            fig=px.pie(
            df,
            names=x
            )


        elif chart=="Scatter":

            fig=px.scatter(
            df,
            x=x,
            y=y
            )


        elif chart=="Histogram":

            fig=px.histogram(
            df,
            x=x
            )


        else:

            fig=px.box(
            df,
            x=x,
            y=y
            )



        st.plotly_chart(

        fig,

        use_container_width=True

        )





    # ===============================
    # DOWNLOAD EXCEL
    # ===============================


    st.divider()


    output=BytesIO()



    with pd.ExcelWriter(
    output,
    engine="xlsxwriter"
    ):

        df.to_excel(
        output,
        index=False
        )



    st.download_button(

    "⬇ Download Excel Report",

    output.getvalue(),

    "Punit_AI_Report.xlsx"

    )





    # ===============================
    # PDF REPORT
    # ===============================


    st.subheader(
    "📄 PDF Report"
    )


    pdf=BytesIO()



    doc=SimpleDocTemplate(pdf)



    styles=getSampleStyleSheet()


    story=[]


    story.append(

    Paragraph(

    "Punit AI Data Analysis Report",

    styles["Heading1"]

    )

    )



    story.append(

    Paragraph(

    str(df.describe()),

    styles["Normal"]

    )

    )


    doc.build(story)



    st.download_button(

    "Download PDF",

    pdf.getvalue(),

    "Punit_AI_Report.pdf"

    )




else:


    st.info(

    "Upload a file to start AI analysis 🚀"

    )



st.divider()


st.caption(

"© Punit Tech Hub | AI Analytics Platform"

)
