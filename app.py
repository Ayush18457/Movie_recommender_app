import streamlit as st

st.title("My First App is Finally Working!")

st.write("This is my app.py file.")

name = st.text_input("Enter your name below:")

if name:
    st.success(f"Hello, {name}!")