import streamlit as st
import requests

st.title("GitHub Portfolio Analyzer")

username = st.text_input("Enter GitHub Username")

if username:
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        st.subheader("Profile Info")
        st.write("Public Repos:", data["public_repos"])
        st.write("Followers:", data["followers"])
        st.write("Following:", data["following"])

        score = min(data["public_repos"] * 2, 100)

        st.subheader("Portfolio Score")
        st.success(f"Score: {score}/100")

        st.subheader("Suggestions")
        if data["public_repos"] < 5:
            st.write("- Add more quality repositories.")
        if data["followers"] < 10:
            st.write("- Improve networking and collaboration.")
        if data["public_repos"] >= 5:
            st.write("- Good repo count. Focus on documentation.")
    else:
        st.error("User not found")
