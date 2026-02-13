import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

st.set_page_config(page_title="GitHub Portfolio Analyzer", layout="wide")


st.markdown("""
<style>
html, body, [class*="css"]  {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

.big-title {
    font-size: 40px;
    font-weight: 700;
}

.glass-card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    margin-bottom: 15px;
    border: 1px solid rgba(255,255,255,0.1);
}

.repo-card {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 15px;
    transition: 0.3s;
    border: 1px solid rgba(255,255,255,0.08);
}

.repo-card:hover {
    transform: scale(1.02);
    background: rgba(255,255,255,0.08);
}

a {
    text-decoration: none;
    color: #58a6ff;
}

a:hover {
    text-decoration: underline;
}

.score-box {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    padding: 15px;
    border-radius: 12px;
    font-size: 20px;
    text-align: center;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🚀 GitHub Portfolio Analyzer</p>', unsafe_allow_html=True)
st.caption("AI-powered recruiter style GitHub evaluation")

username = st.text_input("Enter GitHub Username")

if username:

    user_url = f"https://api.github.com/users/{username}"
    user = requests.get(user_url).json()

    if "message" not in user:

        col1, col2 = st.columns([1,3])

        with col1:
            st.image(user["avatar_url"], width=160)

        with col2:
            st.markdown(f"## {user.get('name', username)}")
            st.write(user.get("bio", "No bio available"))
            st.write("📍", user.get("location", "Not specified"))
            st.markdown(f"[🔗 Visit GitHub Profile]({user['html_url']})")

        st.markdown("---")

        m1, m2, m3 = st.columns(3)
        m1.metric("📦 Public Repos", user["public_repos"])
        m2.metric("👥 Followers", user["followers"])
        m3.metric("🔄 Following", user["following"])

        
        repo_url = f"https://api.github.com/users/{username}/repos"
        repos = requests.get(repo_url).json()

        total_stars = sum(r["stargazers_count"] for r in repos)
        languages = [r["language"] for r in repos if r["language"]]
        lang_count = Counter(languages)

        
        score = 0
        score += min(user["public_repos"], 30)
        score += min(user["followers"] * 2, 20)
        score += min(total_stars * 2, 20)
        score += min(len(lang_count) * 5, 20)
        score = min(score, 100)

        
        st.subheader("🎯 Portfolio Score")
        st.progress(score / 100)
        st.markdown(f'<div class="score-box">Final Score: {score}/100</div>', unsafe_allow_html=True)

        if score >= 75:
            st.success("🔥 Strong GitHub Presence – Recruiter Ready!")
        elif score >= 50:
            st.info("👍 Good profile – Improve impact projects.")
        else:
            st.warning("⚠ Needs improvement – Focus on quality & consistency.")

        st.markdown("---")

        
        st.subheader("🏆 Highlighted Repositories")

        sorted_repos = sorted(repos, key=lambda x: x["updated_at"], reverse=True)[:5]

        for repo in sorted_repos:
            st.markdown(f"""
            <div class="repo-card">
                <h4><a href="{repo['html_url']}" target="_blank">{repo['name']}</a></h4>
                <p>{repo['description'] or "No description provided"}</p>
                ⭐ {repo['stargazers_count']} &nbsp; | &nbsp;
                🍴 {repo['forks_count']} &nbsp; | &nbsp;
                💻 {repo['language'] or "None"}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        
        if lang_count:
            st.subheader("📊 Languages Used")

            fig1, ax1 = plt.subplots(figsize=(6,3))
            ax1.bar(lang_count.keys(), lang_count.values(), color="#00c6ff")
            ax1.set_facecolor("#0f2027")
            fig1.patch.set_facecolor("#0f2027")
            ax1.tick_params(colors="white")
            plt.xticks(rotation=45)
            st.pyplot(fig1)

        
        st.subheader("📈 Developer Strength Radar")

        categories = ["Repos", "Followers", "Stars", "Languages"]
        values = [
            min(user["public_repos"], 30),
            min(user["followers"], 30),
            min(total_stars, 30),
            min(len(lang_count)*5, 30)
        ]

        values += values[:1]
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        fig2, ax2 = plt.subplots(figsize=(4,4), subplot_kw=dict(polar=True))
        ax2.plot(angles, values, color="#00c6ff")
        ax2.fill(angles, values, alpha=0.25, color="#0072ff")
        ax2.set_xticks(angles[:-1])
        ax2.set_xticklabels(categories)
        ax2.set_facecolor("#0f2027")
        fig2.patch.set_facecolor("#0f2027")

        st.pyplot(fig2)

        st.markdown("---")
        st.caption("Built with ❤️ using Streamlit + GitHub API")

    else:
        st.error("User not found ❌")
