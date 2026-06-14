import streamlit as st
import os


image_path = os.path.join(
    "asset",
    "data_ai.jpg"
)


st.write("Checking image path:")
st.write(image_path)



if os.path.isfile(image_path):


    try:


        st.image(

            image_path,

            caption="AI Data Analyzer",

            use_container_width=True

        )


    except Exception as e:


        st.error(

            f"Image loading failed: {e}"

        )


else:


    st.error(

        "Image file not found"

    )

