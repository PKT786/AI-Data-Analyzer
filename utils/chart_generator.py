import plotly.express as px



def generate_chart(df, chart_info):

    """
    Creates charts dynamically
    based on AI recommendation
    """



    if not chart_info:


        return None



    chart_type = chart_info.get(

        "type",

        "bar"

    )



    x_column = chart_info.get(

        "x"

    )


    y_column = chart_info.get(

        "y"

    )


    title = chart_info.get(

        "title",

        "Data Analysis"

    )



    if x_column not in df.columns:


        return None



    if y_column and y_column not in df.columns:


        return None



    # -------------------------
    # Bar Chart
    # -------------------------


    if chart_type == "bar":


        fig = px.bar(

            df,

            x=x_column,

            y=y_column,

            title=title

        )



    # -------------------------
    # Line Chart
    # -------------------------


    elif chart_type == "line":


        fig = px.line(

            df,

            x=x_column,

            y=y_column,

            title=title

        )



    # -------------------------
    # Pie Chart
    # -------------------------


    elif chart_type == "pie":


        fig = px.pie(

            df,

            names=x_column,

            values=y_column,

            title=title

        )



    # -------------------------
    # Scatter Chart
    # -------------------------


    elif chart_type == "scatter":


        fig = px.scatter(

            df,

            x=x_column,

            y=y_column,

            title=title

        )



    else:


        fig = px.bar(

            df,

            x=x_column,

            y=y_column,

            title=title

        )



    return fig