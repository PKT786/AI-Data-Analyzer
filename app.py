import streamlit as st


st.set_page_config(

    page_title="AI Data Analyzer",

    page_icon="📊",

    layout="wide"

)



st.title(
"📊 AI Data Analyzer"
)


st.write(

"""

Upload your Excel/CSV file and get:

✅ AI Insights

✅ Automatic Charts

✅ Business Recommendations


Go to the Data Analyzer page from sidebar.

"""

)


st.image(

"assets/data_ai.png",

use_container_width=True

)