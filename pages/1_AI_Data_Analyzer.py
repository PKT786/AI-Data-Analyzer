import streamlit as st
import pandas as pd
import os


from utils.data_analyzer import analyze_data

from utils.chart_generator import generate_chart



# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(

    page_title="AI Data Analyzer",

    page_icon="📊",

    layout="wide"

)



# -----------------------------
# CSS Styling
# -----------------------------

st.markdown(

"""

<style>


.hero-title{

font-size:45px;

font-weight:800;

color:#111827;

}


.hero-text{

font-size:20px;

color:#4b5563;

}



.card{


padding:25px;

border-radius:15px;

background:#f8fafc;

border:1px solid #e5e7eb;

}



.metric-card{


padding:20px;

border-radius:15px;

background:#ffffff;

box-shadow:0px 4px 15px rgba(0,0,0,0.08);


}


</style>

""",

unsafe_allow_html=True

)





# -----------------------------
# Hero Section
# -----------------------------


col1,col2 = st.columns([1,1])



with col1:


    st.markdown(

    """

    <div class="hero-title">

    📊 AI Data Analyzer

    </div>

    """,

    unsafe_allow_html=True

    )


    st.markdown(

    """

    <div class="hero-text">


    Turn your Excel & CSV files into powerful business insights using Artificial Intelligence.


    <br><br>


    ✔ Automatic Data Analysis

    <br>

    ✔ AI Generated Insights

    <br>

    ✔ Interactive Charts

    <br>

    ✔ Business Recommendations


    </div>


    """,

    unsafe_allow_html=True

    )




with col2:


    image="assets/data_ai.png"


    if os.path.exists(image):


        st.image(

            image,

            use_container_width=True

        )





st.divider()



# -----------------------------
# Feature Cards
# -----------------------------


st.subheader(

"🚀 What AI Analyzer Can Do"

)



c1,c2,c3,c4 = st.columns(4)



with c1:

    st.markdown(

    """

    <div class="card">

    📂

    <h4>Upload Data</h4>

    Excel & CSV support

    </div>

    """,

    unsafe_allow_html=True

    )



with c2:

    st.markdown(

    """

    <div class="card">

    🤖

    <h4>AI Analysis</h4>

    Smart insights

    </div>

    """,

    unsafe_allow_html=True

    )



with c3:

    st.markdown(

    """

    <div class="card">

    📈

    <h4>Charts</h4>

    Auto visualization

    </div>

    """,

    unsafe_allow_html=True

    )



with c4:

    st.markdown(

    """

    <div class="card">

    💡

    <h4>Recommendations</h4>

    Business decisions

    </div>

    """,

    unsafe_allow_html=True

    )



st.divider()



# -----------------------------
# Upload Section
# -----------------------------


st.header(

"📂 Upload Your Dataset"

)



uploaded_file = st.file_uploader(

"Choose Excel or CSV file",

type=[

"csv",

"xlsx"

]

)




if uploaded_file:



    if uploaded_file.name.endswith(".csv"):


        df=pd.read_csv(uploaded_file)


    else:


        df=pd.read_excel(uploaded_file)



    st.success(

    "Dataset uploaded successfully"

    )



    # Dataset Metrics


    a,b,c = st.columns(3)



    with a:


        st.metric(

        "Rows",

        df.shape[0]

        )


    with b:


        st.metric(

        "Columns",

        df.shape[1]

        )



    with c:


        st.metric(

        "Missing Values",

        df.isnull().sum().sum()

        )




    st.divider()



    # Preview


    st.subheader(

    "👀 Data Preview"

    )


    st.dataframe(

        df.head(10),

        use_container_width=True

    )



    st.divider()



    # AI Question


    st.subheader(

    "🤖 Ask AI About Your Data"

    )


    question = st.text_input(

        "Example: Find top selling products",

        placeholder=

        "Ask anything about your dataset..."

    )



    if st.button(

        "✨ Analyze with AI"

    ):



        if question:



            with st.spinner(

            "AI analyzing your data..."

            ):


                result = analyze_data(

                    df,

                    question

                )



            st.session_state["result"]=result



        else:


            st.warning(

            "Please enter your question"

            )




# -----------------------------
# Result Dashboard
# -----------------------------


if "result" in st.session_state:



    result=st.session_state["result"]



    st.divider()



    st.header(

    "📊 AI Analysis Dashboard"

    )



    st.markdown(

    "### 💡 Insights"

    )


    st.info(

        result["insight"]

    )



    st.markdown(

    "### 📈 Visualization"

    )



    fig = generate_chart(

        df,

        result["chart"]

    )



    if fig:


        st.plotly_chart(

            fig,

            use_container_width=True

        )



else:


    st.info(

    """

Upload your dataset and ask AI:

Example:

"Analyze sales performance"

"Find trends"

"Identify problems"

"""

    )
