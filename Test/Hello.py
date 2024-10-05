import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


st.write("# Welcome to my first Web-Application! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Please select a page from the sidebar to get started. Up till now, we have the following pages:
    - **📈 Plotting Demo**: In this section one can find different (interactive) plots of the US population
    - **📊 LLM**: In this section one can find an implemented LLM model.

    This Web-Application is my playroom to try out different functionalities of Streamlit.

    You can find the code for this Web-Application on my [GitHub](https://github.com/EliValLoc/CS-Project)
    For furter information about streamlit visit the [Streamlit Website](https://streamlit.io)

    **Have fun!** 😊
    
    **Note:** This Web-Application is still under construction.
    """
    )
