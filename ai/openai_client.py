import streamlit as st
from openai import OpenAI



def get_openai_client():

    """
    Creates and returns OpenAI client
    using Streamlit secrets
    """



    try:


        api_key = st.secrets["OPENAI_API_KEY"]



        client = OpenAI(

            api_key=api_key

        )


        return client



    except Exception as e:


        raise Exception(

            """

OpenAI API key not found.


Please add your API key:


.streamlit/secrets.toml


Example:


OPENAI_API_KEY="your_api_key_here"


"""

        )