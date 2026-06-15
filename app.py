import streamlit as st
import os



# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(

    page_title="AI Data Analyzer",

    page_icon="📊",

    layout="wide"

)



# -----------------------------
# Custom CSS
# -----------------------------

st.markdown(

"""

<style>


.hero-title{

font-size:55px;

font-weight:900;

line-height:1.1;

color:#111827;

}


.hero-subtitle{

font-size:22px;

color:#4b5563;

}



.feature-card{


padding:25px;

border-radius:18px;

background:#ffffff;

border:1px solid #e5e7eb;

box-shadow:0px 8px 25px rgba(0,0,0,0.08);

height:170px;


}



.section-title{

font-size:32px;

font-weight:800;

text-align:center;

}



.cta{


padding:35px;

border-radius:20px;

background:#f1f5f9;

text-align:center;

}


</style>


""",

unsafe_allow_html=True

)



# -----------------------------
# Hero Section
# -----------------------------


left,right = st.columns(

[1,1]

)



with left:


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

    <div class="hero-subtitle">


    Transform your Excel & CSV data into meaningful insights using Artificial Intelligence.


    <br><br>


    Analyze trends, discover patterns and generate business recommendations automatically.


    </div>


    """,

    unsafe_allow_html=True

    )



    st.write("")


    if st.button(

        "🚀 Start Analyzing Data"

    ):


        st.switch_page(

            "pages/1_Data_Analyzer.py"

        )



with right:


    image_path = "assets/data_ai.png"



    if os.path.exists(image_path):


        st.image(

            image_path,

            use_container_width=True

        )



st.divider()



# -----------------------------
# Feature Section
# -----------------------------


st.markdown(

"""

<div class="section-title">

Why Use AI Data Analyzer?

</div>


""",

unsafe_allow_html=True

)


st.write("")



c1,c2,c3 = st.columns(3)



with c1:


    st.markdown(

    """

    <div class="feature-card">


    <h2>🤖 AI Insights</h2>


    Understand your data with natural language questions.


    </div>


    """,

    unsafe_allow_html=True

    )




with c2:


    st.markdown(

    """

    <div class="feature-card">


    <h2>📈 Smart Charts</h2>


    Automatically generate meaningful visualizations.


    </div>


    """,

    unsafe_allow_html=True

    )




with c3:


    st.markdown(

    """

    <div class="feature-card">


    <h2>💡 Business Decisions</h2>


    Convert raw data into actionable recommendations.


    </div>


    """,

    unsafe_allow_html=True

    )




st.divider()



# -----------------------------
# How it works
# -----------------------------


st.markdown(

"""

<div class="section-title">

How It Works

</div>

""",

unsafe_allow_html=True

)


a,b,c,d = st.columns(4)



steps=[

("1️⃣","Upload","Upload Excel/CSV"),

("2️⃣","Ask","Ask questions"),

("3️⃣","Analyze","AI finds insights"),

("4️⃣","Decide","Take action")

]



for col,step in zip(

[a,b,c,d],

steps

):


    with col:


        st.info(

        f"""

{step[0]}

### {step[1]}


{step[2]}

"""

        )



st.divider()



# -----------------------------
# Use Cases
# -----------------------------


st.markdown(

"""

<div class="section-title">

Built For

</div>


""",

unsafe_allow_html=True

)



x,y,z = st.columns(3)



with x:


    st.success(

    """

📊 Business Analysts


Sales & KPI analysis

"""

    )



with y:


    st.success(

    """

📁 Excel Users


Automated reporting

"""

    )



with z:


    st.success(

    """

🚀 Companies


Data-driven decisions

"""

    )



st.divider()



# -----------------------------
# CTA
# -----------------------------


st.markdown(

"""

<div class="cta">


<h2>Ready to unlock your data?</h2>


Upload your dataset and let AI discover insights.


</div>

""",

unsafe_allow_html=True

)



st.write("")


if st.button(

"✨ Analyze Your First Dataset"

):


    st.switch_page(

        "pages/1_Data_Analyzer.py"

    )



st.caption(

"AI Data Analyzer | Built with Streamlit + OpenAI + Python"

)
