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
# PART 2 PREMIUM
# CHART STUDIO + DASHBOARD
# =====================================================
# =====================================================
# PREMIUM CHART BUILDER
# =====================================================


import plotly.express as px
import random



if "charts" not in st.session_state:
    st.session_state.charts=[]




if "df" in st.session_state and st.session_state.df is not None:


    df=st.session_state.df



    st.divider()

    st.subheader("📊 AI Chart Studio")



    # remove useless columns


    ignore=[]


    for c in df.columns:


        if "id" in c.lower():

            ignore.append(c)



    usable_cols=[

        c for c in df.columns

        if c not in ignore

    ]



    numeric_cols=df[usable_cols].select_dtypes(

        include="number"

    ).columns.tolist()



    text_cols=df[usable_cols].select_dtypes(

        exclude="number"

    ).columns.tolist()




    c1,c2,c3=st.columns(3)



    with c1:


        chart_type=st.selectbox(

        "Select Chart",

        [

        "Bar Chart",

        "Line Chart",

        "Area Chart",

        "Pie Chart",

        "Scatter Chart"

        ]

        )



    with c2:


        x_col=st.selectbox(

        "Category",

        usable_cols

        )



    with c3:


        if numeric_cols:

            y_col=st.selectbox(

            "Measure",

            numeric_cols

            )

        else:

            y_col=None




    # aggregation


    if y_col:


        chart_df=(

        df.groupby(x_col)[y_col]

        .sum()

        .reset_index()

        .sort_values(

        y_col,

        ascending=False

        )

        .head(20)

        )



    else:


        chart_df=df.head(20)





    create,add=st.columns(2)




    with create:


        create_chart=st.button(

        "🎨 Create Chart",

        use_container_width=True

        )





    with add:


        add_dashboard=st.button(

        "➕ Add To Dashboard",

        use_container_width=True

        )






    if create_chart:



        if chart_type=="Bar Chart":


            fig=px.bar(

            chart_df,

            x=x_col,

            y=y_col,

            text_auto=True,

            color=y_col,

            title=f"{y_col} by {x_col}"

            )




        elif chart_type=="Line Chart":


            fig=px.line(

            chart_df,

            x=x_col,

            y=y_col,

            markers=True,

            title=f"{y_col} Trend"

            )




        elif chart_type=="Area Chart":


            fig=px.area(

            chart_df,

            x=x_col,

            y=y_col,

            title="Growth Analysis"

            )




        elif chart_type=="Pie Chart":


            fig=px.pie(

            chart_df,

            names=x_col,

            values=y_col,

            title="Contribution"

            )




        else:


            fig=px.scatter(

            chart_df,

            x=x_col,

            y=y_col,

            size=y_col,

            title="Relationship"

            )





        fig.update_layout(

        template="plotly_white",

        height=450,

        title_font_size=22

        )



        st.session_state.current_chart=fig



        st.plotly_chart(

        fig,

        use_container_width=True,

        key="preview_chart"

        )






    if add_dashboard:


        if "current_chart" in st.session_state:


            st.session_state.charts.append(

            st.session_state.current_chart

            )


            st.success(

            "Chart added to dashboard 🚀"

            )

        else:


            st.warning(

            "Create chart first"

            )






# =====================================================
# DASHBOARD
# =====================================================



if len(st.session_state.charts)>0:



    st.divider()


    st.subheader(

    "🚀 Punit AI Analytics Dashboard"

    )



    colors=[

    "#0f172a",

    "#1e293b",

    "#312e81",

    "#064e3b"

    ]


    bg=random.choice(colors)



    st.markdown(

    f"""

    <div style='

    background:{bg};

    padding:30px;

    border-radius:25px;

    '>


    <h1 style='color:white'>

    📊 Business Dashboard

    </h1>


    </div>

    """,

    unsafe_allow_html=True

    )




    for i in range(0,len(st.session_state.charts),2):


        col1,col2=st.columns(2)



        with col1:


            st.plotly_chart(

            st.session_state.charts[i],

            use_container_width=True,

            key=f"chart_{i}"

            )



        if i+1 < len(st.session_state.charts):


            with col2:


                st.plotly_chart(

                st.session_state.charts[i+1],

                use_container_width=True,

                key=f"chart_{i+1}"

                )
