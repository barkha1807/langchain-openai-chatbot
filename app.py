import streamlit as st
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_openai import ChatOpenAI

# load environemnt variables
load_dotenv()

# initialize chat history session variable
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# initialize UI parameters
st.set_page_config(page_title = "Streaming Bot", page_icon = "")
st.title("Streaming Bot")


# function to create prompt and call openAI to receive response
def get_response(query, chat_history):
    template = """
    You are a helpful assistant. Amswer the following questions considering the history of the conversation:
    
    Chat history : {chat_history}
    
    User question: {user_question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI()

    chain = prompt | llm | StrOutputParser()

    return chain.invoke(
        {
            "chat_history" : chat_history,
            "user_question" : query
        }
    )

# display converation history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

# new user input
user_query = st.chat_input("Your message")

# process new user query
if user_query is not None and user_query != '':
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = get_response(user_query, st.session_state.chat_history)
        st.markdown(ai_response)
    
    st.session_state.chat_history.append(AIMessage(ai_response))