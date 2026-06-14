from ai.openai_client import get_openai_client

import pandas as pd
import json
import streamlit as st



def analyze_data(df, user_question):


    try:


        client = get_openai_client()



        # -----------------------------
        # Prepare dataset information
        # -----------------------------


        columns = list(df.columns)



        sample_data = df.head(10).to_string()



        data_summary = f"""

Dataset Columns:

{columns}


Sample Data:

{sample_data}

"""



        # -----------------------------
        # AI Request
        # -----------------------------


        response = client.chat.completions.create(


            model="gpt-4.1-mini",


            messages=[


            {


            "role":"system",


            "content":

            """

You are an expert Data Analyst AI.


Analyze uploaded datasets.


Your job:


1. Understand user question

2. Find useful business insights

3. Suggest best visualization


Return ONLY JSON.


Required format:


{

"insight":"Explain findings here",


"chart":

{

"type":"bar",

"x":"column name",

"y":"column name",

"title":"chart title"

}

}



Chart type options:

bar

line

pie

scatter



Rules:

- Use existing column names only
- Never create fake columns
- Keep insights simple

"""

            },



            {


            "role":"user",


            "content":


            f"""

Dataset:

{data_summary}



User Question:

{user_question}


"""

            }



            ],


            temperature=0.2


        )



        result = response.choices[0].message.content



        # remove markdown


        result = result.replace(

            "```json",

            ""

        ).replace(

            "```",

            ""

        ).strip()



        analysis = json.loads(

            result

        )



        return analysis




    except Exception as e:



        st.warning(

        """

AI analysis unavailable.

Generating basic analysis.

"""

        )



        return basic_analysis(

            df,

            user_question

        )






# ----------------------------------
# Backup Analyzer (No AI)
# ----------------------------------


def basic_analysis(df, question):


    numeric_columns = list(

        df.select_dtypes(

            include="number"

        ).columns

    )



    text_columns = list(

        df.select_dtypes(

            include="object"

        ).columns

    )



    chart = None



    insight = (

        "Dataset contains "

        + str(len(df))

        + " records."

    )



    if len(numeric_columns) > 0 and len(text_columns) > 0:



        chart = {


        "type":

        "bar",


        "x":

        text_columns[0],


        "y":

        numeric_columns[0],


        "title":

        "Data Overview"


        }




        insight += (


        f"""

The column

{numeric_columns[0]}

contains numeric values.

The chart shows comparison by

{text_columns[0]}.

"""

        )



    elif len(numeric_columns) > 0:



        chart = {


        "type":

        "line",


        "x":

        df.index.name or "index",


        "y":

        numeric_columns[0],


        "title":

        "Trend Analysis"


        }



    return {


    "insight":

    insight,


    "chart":

    chart


    }