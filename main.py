# impoting the required packages 
import streamlit as st


# to clear typed text 
def clear_input_field():
    st.session_state.user_question = st.session_state.user_input
    st.session_state.user_input = ""

# sending the input 
def set_send_input():
    st.session_state.send_input = True
    clear_input_field()

# main function 
def main():
    
    # for website name and icon 
    st.set_page_config(
        page_title="Chat With Docs",
        page_icon="📚"
    )

    # webpage title and description 
    st.markdown("<h1 style='text-align: center;'>Chat With Docs</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>You can collaborate with your data</p>", unsafe_allow_html=True)    
    
    # file upload 
    upload_file = st.file_uploader("Upload documents")
    
    # chatting container bot and user
    chat_container = st.container()

    # states of the text input to clear
    if 'send_input' not in st.session_state:
        st.session_state.send_input = False
        st.session_state.user_question = ""
        
    # buttons and text inputs
    user_input = st.text_input("Ask your queries", placeholder="enter your queries", on_change=set_send_input, key="user_input")
    sendButton = st.button("send", key="sendButton")

    # onclick event for button and put enter on text input
    if sendButton or set_send_input:
        if st.session_state.user_question != "":
            llm_response = "this is the response from the llm model"
            with chat_container:
                st.chat_message("user").write(st.session_state.user_question)
                st.chat_message("bot").write(llm_response)

if __name__ == '__main__':
    main()