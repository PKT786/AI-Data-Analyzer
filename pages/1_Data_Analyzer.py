import streamlit as st
import pandas as pd
import plotly.express as px


from utils.data_analyzer import analyze_data



st.set_page_config(

    page_title="AI Data Analyzer",

    page_icon="📊",

    layout="wide"

)



# -----------------------------
# Hero Section
# -----------------------------


col1,col2 = st.columns([1,1])


with col1:


    st.title(
        "📊 AI Data Analyzer"
    )


    st.write(

    """
    Analyze and visualize your data automatically using AI.

    Upload Excel/CSV files and get:

    ✔ Business Insights

    ✔ Charts

    ✔ Data Summary

    ✔ Recommendations

    """

    )



with col2:


    st.image(

        "assets/data_ai.png",

        use_container_width=True

    )



st.divider()



# -----------------------------
# Upload Data
# -----------------------------


st.header(

"📂 Upload Your Data"

)



file = st.file_uploader(

    "Upload CSV or Excel",

    type=[

        "csv",

        "xlsx"

    ]

)



if file:



    if file.name.endswith(".csv"):


        df = pd.read_csv(file)



    else:


        df = pd.read_excel(file)



    st.success(

        "Data uploaded successfully"

    )



    st.subheader(

        "Preview Data"

    )


    st.dataframe(

        df.head()

    )



    st.divider()



    question = st.text_input(

        "Ask AI about your data",

        placeholder=
        "Example: Find top selling products"

    )



    if st.button(

        "🤖 Analyze Data"

    ):



        with st.spinner(

            "AI analyzing your data..."

        ):



            result = analyze_data(

                df,

                question

            )



        st.subheader(

            "💡 AI Insights"

        )


        st.write(

            result["insight"]

        )



        st.divider()



        # Auto Chart


        if result["chart"]:


            chart=result["chart"]



            fig=px.bar(

                df,

                x=chart["x"],

                y=chart["y"],

                title=chart["title"]

            )



            st.plotly_chart(

                fig,

                use_container_width=True

            )



else:


    st.info(

    "Upload your dataset to start analysis"

    )