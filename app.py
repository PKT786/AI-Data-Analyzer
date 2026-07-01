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
# PART 2 FINAL
# PREMIUM CHART ENGINE + DASHBOARD
# =====================================================


import plotly.express as px
import random



# =====================================================
# SESSION STORAGE
# =====================================================


if "charts" not in st.session_state:

    st.session_state.charts = []



if "current_chart" not in st.session_state:

    st.session_state.current_chart = None






# =====================================================
# CHECK DATA
# =====================================================


if st.session_state.df is not None:


    df = st.session_state.df



    st.divider()


    st.subheader(
        "📊 AI Chart Builder"
    )





    # =================================================
    # SMART COLUMN DETECTION
    # =================================================


    usable_columns=[]


    for col in df.columns:


        name=col.lower()


        if (

            "id" in name

            or

            "code" in name

            or

            "number" in name

        ):


            continue



        usable_columns.append(col)




    numeric_columns = df[usable_columns].select_dtypes(

        include="number"

    ).columns.tolist()



    category_columns = df[usable_columns].select_dtypes(

        exclude="number"

    ).columns.tolist()





    if len(numeric_columns)==0:


        st.warning(

        "No numeric measure found for charts"

        )


        st.stop()






    # =================================================
    # USER OPTIONS
    # =================================================



    col1,col2,col3 = st.columns(3)



    with col1:


        chart_type = st.selectbox(

        "Choose Chart",

        [

        "Bar Chart",

        "Line Chart",

        "Area Chart",

        "Pie Chart",

        "Scatter Chart"

        ]

        )





    with col2:


        x_axis = st.selectbox(

        "Category",

        category_columns

        if category_columns

        else usable_columns

        )






    with col3:


        y_axis = st.selectbox(

        "Measure",

        numeric_columns

        )







    # =================================================
    # DATA AGGREGATION
    # =================================================



    chart_data = (

        df.groupby(x_axis)[y_axis]

        .sum()

        .reset_index()

        .sort_values(

            y_axis,

            ascending=False

        )

        .head(15)

    )





    st.info(

    "AI automatically summarizes top 15 categories for better visualization"

    )







    # =================================================
    # BUTTONS
    # =================================================


    c1,c2 = st.columns(2)




    with c1:


        create_chart = st.button(

        "🎨 Create Chart",

        use_container_width=True

        )




    with c2:


        add_dashboard = st.button(

        "➕ Add To Dashboard",

        use_container_width=True

        )






    # =================================================
    # CREATE CHART
    # =================================================



    if create_chart:



        if chart_type=="Bar Chart":



            fig = px.bar(

            chart_data,

            x=x_axis,

            y=y_axis,

            text_auto=True,

            color=y_axis,

            title=f"{y_axis} by {x_axis}"

            )





        elif chart_type=="Line Chart":



            fig = px.line(

            chart_data,

            x=x_axis,

            y=y_axis,

            markers=True,

            title=f"{y_axis} Trend"

            )






        elif chart_type=="Area Chart":



            fig = px.area(

            chart_data,

            x=x_axis,

            y=y_axis,

            title="Growth Analysis"

            )







        elif chart_type=="Pie Chart":



            fig = px.pie(

            chart_data,

            names=x_axis,

            values=y_axis,

            title="Contribution Analysis"

            )








        else:



            fig = px.scatter(

            chart_data,

            x=x_axis,

            y=y_axis,

            size=y_axis,

            title="Relationship Analysis"

            )







        # PROFESSIONAL STYLE


        fig.update_layout(

            template="plotly_white",

            height=450,

            title_font=dict(

            size=24

            ),

            margin=dict(

            l=40,

            r=40,

            t=80,

            b=40

            )

        )




        st.session_state.current_chart = fig




        st.plotly_chart(

        fig,

        use_container_width=True,

        key="preview_chart"

        )







    # =================================================
    # ADD DASHBOARD
    # =================================================


    if add_dashboard:



        if st.session_state.current_chart is not None:



            st.session_state.charts.append(

            st.session_state.current_chart

            )



            st.success(

            "Chart added to dashboard 🚀"

            )



        else:



            st.warning(

            "First create a chart"

            )







# =====================================================
# PREMIUM DASHBOARD
# =====================================================



if len(st.session_state.charts)>0:



    st.divider()



    st.subheader(

    "🚀 Punit AI Dashboard"

    )






    dashboard_colors=[


    "#020617",

    "#172554",

    "#312e81",

    "#064e3b",

    "#3f1d2e"


    ]



    selected_bg=random.choice(

    dashboard_colors

    )







    st.markdown(

    f"""

<div style="

background:{selected_bg};

padding:35px;

border-radius:30px;

margin-bottom:25px;

">


<h1 style="color:white">

📊 Business Intelligence Dashboard

</h1>


<p style="color:white">

Created by Punit AI Data Analyzer

</p>


</div>


""",

    unsafe_allow_html=True

    )








    # KPI AREA



    a,b,c,d = st.columns(4)



    a.metric(

    "Rows",

    df.shape[0]

    )


    b.metric(

    "Columns",

    df.shape[1]

    )


    c.metric(

    "Charts",

    len(st.session_state.charts)

    )


    d.metric(

    "Status",

    "Ready"

    )







    st.write("")





    # CHART GRID



    for i in range(

        0,

        len(st.session_state.charts),

        2

    ):



        left,right = st.columns(2)





        with left:



            st.plotly_chart(

            st.session_state.charts[i],

            use_container_width=True,

            key=f"dashboard_left_{i}"

            )





        if i+1 < len(st.session_state.charts):



            with right:



                st.plotly_chart(

                st.session_state.charts[i+1],

                use_container_width=True,

                key=f"dashboard_right_{i}"

                )







# =====================================================
# END PART 2
# =====================================================
