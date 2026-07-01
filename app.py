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

# =====================================================
# PUNIT AI DATA ANALYZER V5
# PART 2
# CHART STUDIO + DASHBOARD BUILDER
# =====================================================


import plotly.express as px
import random




# =====================================================
# CHECK DATA
# =====================================================


if st.session_state.df is not None:


    df = st.session_state.df



    st.divider()



    # =================================================
    # CHART STUDIO
    # =================================================


    st.subheader(

    "📊 Chart Studio"

    )



    numeric_columns = df.select_dtypes(

        include=["number"]

    ).columns.tolist()



    all_columns = df.columns.tolist()





    chart_type = st.selectbox(

    "Choose Chart Type",

    [

    "📊 Bar Chart",

    "📈 Line Chart",

    "🥧 Pie Chart",

    "🌊 Area Chart",

    "🔵 Scatter Chart",

    "🔥 Heatmap"

    ]

    )





    col1,col2 = st.columns(2)



    with col1:


        x_column = st.selectbox(

        "Select X Axis",

        all_columns

        )



    with col2:


        if len(numeric_columns)>0:


            y_column = st.selectbox(

            "Select Y Axis",

            numeric_columns

            )

        else:


            y_column = st.selectbox(

            "Select Y Axis",

            all_columns

            )





    if st.button(

    "🚀 Create Chart"

    ):



        try:



            if chart_type=="📊 Bar Chart":



                fig = px.bar(

                df,

                x=x_column,

                y=y_column,

                template="plotly_dark",

                title=f"{y_column} Analysis"

                )





            elif chart_type=="📈 Line Chart":



                fig = px.line(

                df,

                x=x_column,

                y=y_column,

                template="plotly_dark",

                title=f"{y_column} Trend"

                )





            elif chart_type=="🥧 Pie Chart":



                fig = px.pie(

                df,

                names=x_column,

                values=y_column,

                template="plotly_dark"

                )





            elif chart_type=="🌊 Area Chart":



                fig = px.area(

                df,

                x=x_column,

                y=y_column,

                template="plotly_dark"

                )





            elif chart_type=="🔵 Scatter Chart":



                fig = px.scatter(

                df,

                x=x_column,

                y=y_column,

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





            st.session_state.charts.append(fig)



            st.success(

            "Chart added to dashboard ✅"

            )



            st.plotly_chart(

            fig,

            use_container_width=True,

            key=f"created_chart_{len(st.session_state.charts)}"

            )





        except Exception as e:



            st.error(

            f"Chart error: {e}"

            )







    # =================================================
    # DASHBOARD BUILDER
    # =================================================



    st.divider()



    st.subheader(

    "🎨 AI Dashboard Builder"

    )





    themes=[



    {

    "name":"Bloomberg Dark",

    "color":"#050505"

    },



    {

    "name":"Fabric Blue",

    "color":"#0f172a"

    },



    {

    "name":"Purple AI",

    "color":"#3b0764"

    },



    {

    "name":"Ocean Analytics",

    "color":"#082f49"

    }



    ]





    if st.button(

    "✨ Generate Dashboard"

    ):



        selected_theme=random.choice(

        themes

        )



        st.session_state.dashboard_theme = selected_theme



        st.success(

        f"Dashboard Theme: {selected_theme['name']}"

        )







    # =================================================
    # DISPLAY DASHBOARD
    # =================================================



    if len(st.session_state.charts)>0:



        theme = st.session_state.get(

        "dashboard_theme",

        {

        "color":"#0f172a",

        "name":"Default"

        }

        )





        st.markdown(

        f"""

<div style="

background:{theme['color']};

padding:30px;

border-radius:25px;


">


<h1 style="color:white">

Punit AI Dashboard 🚀

</h1>



<p style="color:white">

Interactive Business Analytics Dashboard

</p>



</div>


""",

        unsafe_allow_html=True

        )





        st.write("")





        for index,chart in enumerate(

            st.session_state.charts

        ):



            st.plotly_chart(

            chart,

            use_container_width=True,

            key=f"dashboard_chart_{index}"

            )







    # =================================================
    # AUTO DASHBOARD
    # =================================================


    st.divider()



    st.subheader(

    "🤖 Auto Dashboard Generator"

    )





    if st.button(

    "Generate Automatic Dashboard 🚀"

    ):



        numeric=numeric_columns



        if len(numeric)>0:



            auto_charts=[]





            auto_charts.append(

            px.line(

            df,

            y=numeric[0],

            title="Performance Trend",

            template="plotly_dark"

            )

            )





            auto_charts.append(

            px.bar(

            df,

            x=df.columns[0],

            y=numeric[0],

            title="Category Performance",

            template="plotly_dark"

            )

            )





            auto_charts.append(

            px.histogram(

            df,

            x=numeric[0],

            title="Data Distribution",

            template="plotly_dark"

            )

            )





            st.session_state.charts = auto_charts





            st.success(

            "AI Dashboard Created Successfully 🚀"

            )



            for i,c in enumerate(auto_charts):


                st.plotly_chart(

                c,

                use_container_width=True,

                key=f"auto_dashboard_{i}"

                )



        else:



            st.warning(

            "No numeric columns found"

            )





# =====================================================
# END PART 2
# =====================================================
