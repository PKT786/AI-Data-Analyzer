import streamlit as st
import pandas as pd
import plotly.express as px
import random
import io
import os

from groq import Groq
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

if "df" not in st.session_state:
    st.session_state.df = None
# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Punit AI Data Analyzer",
    page_icon="📊",
    layout="wide"
)



# =====================================================
# PREMIUM CSS
# =====================================================

st.markdown("""

<style>


body{

background:#0b1120;

}


.main{

background:#0b1120;

}


.hero{

background:
linear-gradient(
135deg,
#111827,
#1e3a8a
);

padding:35px;

border-radius:25px;

color:white;

}


.hero h1{

font-size:45px;

}



.card{

background:#111827;

padding:20px;

border-radius:18px;

color:white;

box-shadow:
0px 8px 30px rgba(0,0,0,.4);

}


.metric-card{

background:#1f2937;

padding:20px;

border-radius:15px;

text-align:center;

color:white;

}



.stButton button{

background:#2563eb;

color:white;

border-radius:12px;

height:45px;

font-weight:bold;

}



</style>

""",
unsafe_allow_html=True)





# =====================================================
# LOGO + HEADER
# =====================================================


col1,col2=st.columns([1,5])


with col1:

    if os.path.exists(
        "assets/punit_logo.png"
    ):

        st.image(
            "assets/punit_logo.png",
            width=120
        )



with col2:

    st.markdown(
    """

<h1 style="color:white">

Punit AI Data Analyzer 🚀

</h1>


""",

unsafe_allow_html=True

)





# =====================================================
# HERO SECTION
# =====================================================


st.markdown(

"""

<div class="hero">


<h1>
Turn Your Data Into AI Powered Insights
</h1>


<p>

Upload Excel or CSV files.

Clean data.

Create charts.

Generate dashboards.

Get AI recommendations.

</p>


</div>


""",

unsafe_allow_html=True

)



st.write("")





# =====================================================
# UPLOAD
# =====================================================


uploaded_file = st.file_uploader(

"📂 Upload Excel / CSV Dataset",

type=[
"csv",
"xlsx"
]

)




# =====================================================
# LOAD DATA
# =====================================================


if uploaded_file:

    if uploaded_file.name.endswith(".csv"):

        st.session_state.df = pd.read_csv(uploaded_file)

    else:

        st.session_state.df = pd.read_excel(uploaded_file)


    df = st.session_state.df


    st.success(
        "Dataset uploaded successfully 🚀"
    )


    st.write(
        "Rows:",
        df.shape[0]
    )


    st.write(
        "Columns:",
        df.shape[1]
    )

    # =================================================
    # DATA SUMMARY
    # =================================================


    st.subheader(
    "📌 Dataset Overview"
    )


    missing=df.isnull().sum().sum()

    duplicate=df.duplicated().sum()


    quality=int(

        100 -

        (
        (missing+duplicate)
        /
        max(df.size,1)
        *
        100

        )

    )



    c1,c2,c3,c4=st.columns(4)



    c1.markdown(

    f"""

<div class="metric-card">

<h2>{df.shape[0]}</h2>

Rows

</div>

""",

unsafe_allow_html=True

)



    c2.markdown(

    f"""

<div class="metric-card">

<h2>{df.shape[1]}</h2>

Columns

</div>

""",

unsafe_allow_html=True

)



    c3.markdown(

    f"""

<div class="metric-card">

<h2>{quality}%</h2>

Data Quality

</div>

""",

unsafe_allow_html=True

)



    c4.markdown(

    f"""

<div class="metric-card">

<h2>{duplicate}</h2>

Duplicates

</div>

""",

unsafe_allow_html=True

)




    # =================================================
    # CLEAN DATA
    # =================================================


    st.divider()


    st.subheader(
    "🧹 AI Data Cleaning Engine"
    )



    if st.button(
    "✨ Clean My Dataset"
    ):


        clean=df.copy()



        # remove duplicates

        clean.drop_duplicates(
        inplace=True
        )



        # remove empty columns

        clean.dropna(
        axis=1,
        how="all",
        inplace=True
        )



        # fill missing

        for col in clean.columns:



            if clean[col].isnull().sum()>0:



                if clean[col].dtype=="object":


                    clean[col]=clean[col].fillna(
                    "Unknown"
                    )


                else:


                    clean[col]=clean[col].fillna(
                    clean[col].median()
                    )



        st.session_state.clean = clean
        st.session_state.df = clean



        st.success(

        "Data Cleaning Completed ✅"

        )



    if "clean" in st.session_state:


        df=st.session_state["clean"]




    st.subheader(
    "Clean Data Preview"
    )


    st.dataframe(

    df.head(20),

    use_container_width=True

    )


# =====================================================
# CHART STUDIO
# =====================================================
# Safety check

if st.session_state.df is None:

    st.warning(
    "Please upload a dataset first"
    )

    st.stop()


df = st.session_state.df

st.divider()


st.subheader(
"📊 Visualization Studio"
)



if "clean" in st.session_state:

    df = st.session_state.clean

else:

    df = st.session_state.df



numeric_cols = df.select_dtypes(
include=["int64","float64"]
).columns.tolist()



all_cols=df.columns.tolist()



chart_type = st.selectbox(

"Choose Chart Type",

[

"📊 Bar Chart",

"📈 Line Chart",

"🥧 Pie Chart",

"🌊 Area Chart",

"🔵 Scatter Plot",

"🔥 Heatmap"

]

)



col1,col2=st.columns(2)



with col1:

    x_axis=st.selectbox(

    "Select X Axis",

    all_cols

    )



with col2:

    y_axis=st.selectbox(

    "Select Y Axis",

    numeric_cols

    if len(numeric_cols)>0

    else all_cols

    )





# store charts

if "charts" not in st.session_state:

    st.session_state["charts"]=[]





if st.button(
"🚀 Create Chart"
):


    if chart_type=="📊 Bar Chart":


        fig=px.bar(

        df,

        x=x_axis,

        y=y_axis,

        template="plotly_dark",

        title=f"{y_axis} Analysis"

        )



    elif chart_type=="📈 Line Chart":


        fig=px.line(

        df,

        x=x_axis,

        y=y_axis,

        template="plotly_dark",

        title=f"{y_axis} Trend"

        )



    elif chart_type=="🥧 Pie Chart":


        fig=px.pie(

        df,

        names=x_axis,

        values=y_axis,

        template="plotly_dark"

        )



    elif chart_type=="🌊 Area Chart":


        fig=px.area(

        df,

        x=x_axis,

        y=y_axis,

        template="plotly_dark"

        )



    elif chart_type=="🔵 Scatter Plot":


        fig=px.scatter(

        df,

        x=x_axis,

        y=y_axis,

        template="plotly_dark"

        )



    else:


        corr=df.select_dtypes(
        include="number"
        ).corr()



        fig=px.imshow(

        corr,

        text_auto=True,

        template="plotly_dark"

        )





    st.session_state["charts"].append(fig)



    st.success(

    "Chart Added To Dashboard ✅"

    )



    st.plotly_chart(

    fig,

    use_container_width=True

    )





# =====================================================
# DASHBOARD BUILDER
# =====================================================


st.divider()



st.subheader(

"🎨 AI Dashboard Builder"

)





themes=[

{

"name":"Midnight Blue",

"bg":"#0F172A"

},

{

"name":"Fabric Dark",

"bg":"#111827"

},

{

"name":"Purple Glass",

"bg":"#3B0764"

},

{

"name":"Bloomberg",

"bg":"#050505"

},

{

"name":"Ocean",

"bg":"#082F49"

}

]



theme=random.choice(themes)



if st.button(

"✨ Generate Professional Dashboard"

):



    st.session_state["theme"]=theme



    st.success(

    f"Dashboard Theme Created: {theme['name']}"

    )





if "charts" in st.session_state and len(st.session_state["charts"])>0:



    selected_theme=st.session_state.get(

    "theme",

    theme

    )



    st.markdown(

    f"""

<div style="

background:{selected_theme['bg']};

padding:30px;

border-radius:25px;

">

<h1 style="color:white">

Punit AI Dashboard 🚀

</h1>


</div>


""",

    unsafe_allow_html=True

    )





    st.write("")



    # display all charts

    for i,chart in enumerate(
    st.session_state["charts"]
    ):


        st.plotly_chart(

        chart,

        use_container_width=True

        )





# =====================================================
# AUTO DASHBOARD GENERATOR
# =====================================================


st.divider()


st.subheader(

"🤖 Auto Generate Dashboard"

)



if st.button(

"Generate AI Dashboard Automatically"

):


    nums=df.select_dtypes(

    include="number"

    ).columns



    if len(nums)>0:


        auto1=px.line(

        df,

        y=nums[0],

        title="Performance Trend",

        template="plotly_dark"

        )


        auto2=px.bar(

        df,

        x=df.columns[0],

        y=nums[0],

        title="Category Performance",

        template="plotly_dark"

        )


        auto3=px.histogram(

        df,

        x=nums[0],

        title="Distribution",

        template="plotly_dark"

        )



        st.session_state["charts"]=[

        auto1,

        auto2,

        auto3

        ]



        st.success(

        "AI Dashboard Generated Successfully 🚀"

        )


        for c in st.session_state["charts"]:

            st.plotly_chart(

            c,

            use_container_width=True

            )


    else:


        st.warning(

        "No numeric columns detected"

        )
        # =====================================================
# AI DATA INSIGHTS (GROQ)
# =====================================================


st.divider()


st.subheader(
"🤖 AI Business Insights"
)



if st.button(
"Generate AI Insights 🚀"
):


    try:


        client=Groq(

        api_key=st.secrets["GROQ_API_KEY"]

        )



        sample=df.head(50).to_string()



        prompt=f"""

You are a senior data analyst.


Analyze this dataset:


{sample}



Provide:

1. Important trends

2. Business insights

3. Data problems

4. Recommendations



Answer in simple business language.

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



        st.markdown(

        response.choices[0].message.content

        )



    except Exception as e:


        st.error(

        "AI service unavailable"

        )




# =====================================================
# ASK YOUR DATA
# =====================================================


st.divider()


st.subheader(

"💬 Ask Questions From Your Data"

)



question=st.text_input(

"Example: Which product has highest sales?"

)



if question:


    try:



        client=Groq(

        api_key=st.secrets["GROQ_API_KEY"]

        )



        context=df.head(100).to_string()



        prompt=f"""


Dataset:


{context}



User Question:


{question}



Answer like a data analyst.

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



        st.success(

        result.choices[0].message.content

        )



    except:


        st.error(

        "Unable to analyze question"

        )





# =====================================================
# DOWNLOAD CLEAN EXCEL
# =====================================================


st.divider()


st.subheader(

"⬇ Export Reports"

)



excel_buffer=io.BytesIO()



df.to_excel(

excel_buffer,

index=False,

engine="openpyxl"

)



st.download_button(


"📊 Download Clean Excel",


excel_buffer.getvalue(),


"punit_clean_dataset.xlsx"



)





# =====================================================
# PDF REPORT
# =====================================================


pdf_buffer=io.BytesIO()



doc=SimpleDocTemplate(

pdf_buffer

)



styles=getSampleStyleSheet()



content=[]



content.append(

Paragraph(

"Punit AI Data Analyzer Report",

styles["Heading1"]

)

)



content.append(

Paragraph(

f"""

Created Date:

{datetime.now()}



Rows:

{df.shape[0]}



Columns:

{df.shape[1]}



Data Quality:

{quality}%



Summary:



{df.describe().to_string()}


""",

styles["Normal"]

)

)



doc.build(

content

)



st.download_button(

"📄 Download PDF Report",

pdf_buffer.getvalue(),

"punit_ai_report.pdf"

)





# =====================================================
# DASHBOARD IMAGE EXPORT
# =====================================================


if "charts" in st.session_state and len(st.session_state["charts"])>0:


    st.subheader(

    "🖼 Download Dashboard Image"

    )



    if st.button(

    "Create Dashboard Snapshot"

    ):



        try:


            image=st.session_state["charts"][0].to_image(

            format="png"

            )



            st.download_button(

            "⬇ Download PNG",

            image,

            "punit_dashboard.png",

            "image/png"

            )


        except:


            st.warning(

            "Install kaleido package for image export"

            )





# =====================================================
# RESOURCE SECTION
# =====================================================


st.divider()



st.markdown(

"""

## 🚀 Explore Punit Tech Hub


📊 Excel Tutorials

🤖 AI Resources

💻 Mainframe Learning

📄 Interview Preparation



www.punittechhub.com


"""

)




# =====================================================
# FOOTER
# =====================================================


st.divider()



st.caption(

"""

© Punit Tech Hub | Punit AI Data Analyzer


Built with AI + Data Analytics 🚀

"""

)
