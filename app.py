"""
Premium ATS Resume Builder — Streamlit app
--------------------------------------------
- Hero section: your logo (left) + title/tagline + premium hero image (right)
- Choose a resume tier: Simple / Professional / Premium
    -> app randomly picks one of that tier's 5 templates at generation time
- Fill the resume manually OR upload an existing resume to auto-fill the form
- Generate a polished, ATS-friendly .docx and download it
- Check the ATS-friendliness score of the generated resume (0-100)

Run locally:
    streamlit run app.py

Deploy on Streamlit Community Cloud:
    1. Push this folder to a GitHub repo (app.py, resume_builder.py,
       resume_parser.py, ats_scorer.py, requirements.txt, assets/).
    2. On share.streamlit.io, create a new app pointing at app.py.

Branding:
    Replace assets/logo.png with your real logo and assets/hero.png with
    your own hero image at any time — same filenames, any reasonable size.
"""

import base64
import os
import random

import streamlit as st
from resume_builder import build_resume, TEMPLATES, pick_random_template
from resume_parser import parse_resume
from ats_scorer import score_resume
import auth

st.set_page_config(page_title="Premium ATS Resume Builder", page_icon="📄", layout="centered")

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")
HERO_PATH = os.path.join(ASSETS_DIR, "hero.png")


# ========================================================== AUTHENTICATION ==
def _complete_oauth_callback():
    """If Google/Facebook just redirected back here with ?code=&state=,
    finish the login and clear the URL before rendering anything else."""
    if st.session_state.get("auth_user"):
        return

    params = st.query_params
    code = params.get("code")
    state = params.get("state")
    if not code or state not in ("google", "facebook"):
        return

    profile = auth.complete_google_login(code) if state == "google" else auth.complete_facebook_login(code)
    st.query_params.clear()

    if profile and profile.get("email"):
        user = auth.login_or_signup_via_social(profile["name"], profile["email"], provider=state)
        st.session_state["auth_user"] = user
        st.session_state["auth_flash"] = f"Signed in with {state.title()} as {profile['email']}."
    else:
        st.session_state["auth_error"] = f"{state.title()} sign-in failed or was cancelled. Please try again."

    st.rerun()


def render_auth_page():
    """Login / Sign up gate shown before the resume builder unlocks."""

    st.markdown(
        """
        <style>
        .auth-card {
            background: #FFFFFF;
            border: 1px solid #E7EAF0;
            border-radius: 16px;
            padding: 28px 30px 8px;
            box-shadow: 0 8px 24px rgba(13,27,42,0.08);
            margin-bottom: 20px;
        }
        .auth-divider {
            display: flex; align-items: center; gap: 12px;
            margin: 18px 0 14px; color: #9AA4B2; font-size: 12.5px;
            text-transform: uppercase; letter-spacing: 1px;
        }
        .auth-divider::before, .auth-divider::after {
            content: ""; flex: 1; height: 1px; background: #E7EAF0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.get("auth_flash"):
        st.success(st.session_state.pop("auth_flash"))
    if st.session_state.get("auth_error"):
        st.error(st.session_state.pop("auth_error"))

    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    tab_login, tab_signup = st.tabs(["🔐 Log In", "📝 Sign Up"])

    with tab_login:
        with st.form("login_form"):
            login_email = st.text_input("Email (User ID)", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Log In", type="primary", use_container_width=True)
        if submitted:
            success, message, user = auth.login_user(login_email, login_password)
            if success:
                st.session_state["auth_user"] = user
                st.session_state["auth_flash"] = f"Welcome back, {user['name']}!"
                st.rerun()
            else:
                st.error(message)

        st.markdown('<div class="auth-divider">or continue with</div>', unsafe_allow_html=True)
        _render_social_buttons("login")

    with tab_signup:
        with st.form("signup_form"):
            su_name = st.text_input("Full Name", key="signup_name")
            su_email = st.text_input("Email (User ID)", key="signup_email")
            su_mobile = st.text_input("Mobile Number", key="signup_mobile")
            su_password = st.text_input("Create Password", type="password", key="signup_password")
            submitted_su = st.form_submit_button("Sign Up", type="primary", use_container_width=True)
        if submitted_su:
            success, message = auth.signup_user(su_name, su_email, su_mobile, su_password)
            if success:
                st.success(message)
            else:
                # Includes the "already signed up with this email id" case
                st.warning(message)

        st.markdown('<div class="auth-divider">or sign up with</div>', unsafe_allow_html=True)
        _render_social_buttons("signup")

    st.markdown("</div>", unsafe_allow_html=True)


def _render_social_buttons(context: str):
    col1, col2 = st.columns(2)
    google_url = auth.build_google_auth_url()
    facebook_url = auth.build_facebook_auth_url()

    with col1:
        if google_url:
            st.link_button("🔵 Continue with Google", google_url, use_container_width=True,
                            key=f"google_btn_{context}")
        else:
            st.button("🔵 Continue with Google", disabled=True, use_container_width=True,
                       key=f"google_btn_disabled_{context}",
                       help="Add [google] client_id/client_secret/redirect_uri to secrets.toml to enable this.")
    with col2:
        if facebook_url:
            st.link_button("🔷 Continue with Facebook", facebook_url, use_container_width=True,
                            key=f"facebook_btn_{context}")
        else:
            st.button("🔷 Continue with Facebook", disabled=True, use_container_width=True,
                       key=f"facebook_btn_disabled_{context}",
                       help="Add [facebook] app_id/app_secret/redirect_uri to secrets.toml to enable this.")


def render_account_bar():
    user = st.session_state["auth_user"]
    c1, c2 = st.columns([5, 1])
    with c1:
        st.caption(f"Logged in as **{user['name']}** ({user['email']})")
    with c2:
        if st.button("Log Out", use_container_width=True):
            st.session_state.pop("auth_user", None)
            st.rerun()


_complete_oauth_callback()

if not st.session_state.get("auth_user"):
    render_auth_page()
    st.stop()


# ============================================================ HERO SECTION ==
def _img_b64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def render_hero():
    logo_b64 = _img_b64(LOGO_PATH)
    hero_b64 = _img_b64(HERO_PATH)

    st.markdown(
        """
        <style>
        .hero-wrap {
            background: linear-gradient(135deg, #0D1B2A 0%, #16294D 55%, #0B1220 100%);
            border-radius: 18px;
            padding: 28px 32px;
            margin-bottom: 28px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        }
        .hero-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
            flex-wrap: wrap;
        }
        .hero-logo img {
            width: 64px;
            height: 64px;
            border-radius: 50%;
            box-shadow: 0 4px 14px rgba(0,0,0,0.35);
        }
        .hero-text {
            flex: 1;
            min-width: 220px;
            text-align: center;
        }
        .hero-title {
            color: #FFFFFF;
            font-size: 30px;
            font-weight: 800;
            letter-spacing: 0.5px;
            margin: 0;
            font-family: Georgia, 'Times New Roman', serif;
        }
        .hero-tagline {
            color: #C9A877;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            margin-top: 6px;
        }
        .hero-sub {
            color: #B9C2D0;
            font-size: 13.5px;
            margin-top: 10px;
            max-width: 480px;
            margin-left: auto;
            margin-right: auto;
        }
        .hero-image img {
            width: 190px;
            border-radius: 14px;
            box-shadow: 0 10px 24px rgba(0,0,0,0.4);
        }
        @media (max-width: 700px) {
            .hero-row { flex-direction: column; text-align: center; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    logo_html = f'<div class="hero-logo"><img src="data:image/png;base64,{logo_b64}"/></div>' if logo_b64 else '<div class="hero-logo">📄</div>'
    hero_html = f'<div class="hero-image"><img src="data:image/png;base64,{hero_b64}"/></div>' if hero_b64 else ""

    st.markdown(
        f"""
        <div class="hero-wrap">
          <div class="hero-row">
            {logo_html}
            <div class="hero-text">
              <p class="hero-title">Premium ATS Resume Builder</p>
              <div class="hero-tagline">Simple · Professional · Premium templates</div>
              <p class="hero-sub">
                Fill in your details or upload an existing resume — get a polished,
                recruiter-ready .docx that's built to pass ATS screening.
              </p>
            </div>
            {hero_html}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


render_hero()
render_account_bar()


# ================================================================ STATE ====
def init_state():
    defaults = {
        "name": "", "title": "", "location": "", "phone": "", "email": "", "linkedin": "",
        "summary": "",
        "skills": [{"label": "", "value": ""}],
        "experience": [{"role": "", "company": "", "dates": "", "project": "", "bullets": [""]}],
        "certifications": [""],
        "awards": [""],
        "education": [{"degree": "", "school": "", "details": ""}],
        "resume_tier": "premium",
        "generated_docx": None,
        "generated_template": None,
        "generated_data": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Prefill contact fields from the logged-in account, once.
    if not st.session_state.get("_prefilled_from_account"):
        user = st.session_state.get("auth_user") or {}
        if user.get("name") and not st.session_state["name"]:
            st.session_state["name"] = user["name"]
        if user.get("email") and not st.session_state["email"]:
            st.session_state["email"] = user["email"]
        if user.get("mobile") and user["mobile"] != "N/A" and not st.session_state["phone"]:
            st.session_state["phone"] = user["mobile"]
        st.session_state["_prefilled_from_account"] = True


def load_parsed_into_state(parsed: dict):
    for key in ["name", "title", "location", "phone", "email", "linkedin", "summary"]:
        if parsed.get(key):
            st.session_state[key] = parsed[key]
    if parsed.get("skills"):
        st.session_state["skills"] = parsed["skills"]
    if parsed.get("experience"):
        for job in parsed["experience"]:
            job.setdefault("bullets", [])
            if not job["bullets"]:
                job["bullets"] = [""]
        st.session_state["experience"] = parsed["experience"]
    if parsed.get("certifications"):
        st.session_state["certifications"] = parsed["certifications"]
    if parsed.get("awards"):
        st.session_state["awards"] = parsed["awards"]
    if parsed.get("education"):
        st.session_state["education"] = parsed["education"]


init_state()

# ============================================================ TIER PICKER ==
st.subheader("1. Choose a resume style")

TIER_INFO = {
    "simple": {
        "label": "Simple",
        "desc": "Clean, minimal, maximum ATS safety. Ideal for very conservative applicant tracking systems.",
    },
    "professional": {
        "label": "Professional",
        "desc": "Confident color accents and structured section headers — a step up for corporate roles.",
    },
    "premium": {
        "label": "Premium",
        "desc": "A full-bleed color header banner and refined typography for a standout, high-end look.",
    },
}

tier_cols = st.columns(3)
for col, (key, info) in zip(tier_cols, TIER_INFO.items()):
    with col:
        selected = st.session_state["resume_tier"] == key
        if st.button(
            f"{'✅ ' if selected else ''}{info['label']}",
            key=f"tier_btn_{key}",
            use_container_width=True,
            type="primary" if selected else "secondary",
        ):
            st.session_state["resume_tier"] = key
            st.rerun()
        st.caption(info["desc"])
        st.caption(f"{len(TEMPLATES[key])} template variants — one is picked at random when you generate.")

st.divider()

# ------------------------------------------------------------- mode picker
st.subheader("2. Start with an upload or fill manually")
mode = st.radio(
    "How would you like to start?",
    ["Upload an existing resume", "Fill in manually"],
    horizontal=True,
    label_visibility="collapsed",
)

if mode == "Upload an existing resume":
    uploaded = st.file_uploader("Upload your resume (.pdf or .docx)", type=["pdf", "docx"])
    if uploaded is not None:
        if st.button("Parse resume and pre-fill form"):
            with st.spinner("Reading and parsing your resume..."):
                parsed = parse_resume(uploaded)
            load_parsed_into_state(parsed)
            st.success("Parsed! Review and correct the fields below — auto-parsing isn't perfect.")

st.divider()

# ------------------------------------------------------------------ FORM UI
st.subheader("3. Your Details")

st.markdown("**Contact Details**")
c1, c2 = st.columns(2)
with c1:
    st.session_state["name"] = st.text_input("Full Name", st.session_state["name"])
    st.session_state["location"] = st.text_input("Location (City, State/Country)", st.session_state["location"])
    st.session_state["email"] = st.text_input("Email", st.session_state["email"])
with c2:
    st.session_state["title"] = st.text_input("Headline / Target Job Title", st.session_state["title"])
    st.session_state["phone"] = st.text_input("Phone", st.session_state["phone"])
    st.session_state["linkedin"] = st.text_input("LinkedIn URL (optional)", st.session_state["linkedin"])

st.markdown("**Professional Summary**")
st.session_state["summary"] = st.text_area("Summary", st.session_state["summary"], height=120, label_visibility="collapsed")

st.markdown("**Technical / Core Skills**")
for i, s in enumerate(st.session_state["skills"]):
    col1, col2, col3 = st.columns([2, 4, 0.5])
    s["label"] = col1.text_input(f"Category {i+1}", s.get("label", ""), key=f"skill_label_{i}")
    s["value"] = col2.text_input(f"Skills {i+1}", s.get("value", ""), key=f"skill_value_{i}")
    if col3.button("✕", key=f"skill_del_{i}") and len(st.session_state["skills"]) > 1:
        st.session_state["skills"].pop(i)
        st.rerun()
if st.button("+ Add skill category"):
    st.session_state["skills"].append({"label": "", "value": ""})
    st.rerun()

st.markdown("**Professional Experience**")
for i, job in enumerate(st.session_state["experience"]):
    with st.container(border=True):
        st.markdown(f"Job {i+1}")
        jc1, jc2 = st.columns(2)
        job["role"] = jc1.text_input("Job Title", job.get("role", ""), key=f"job_role_{i}")
        job["company"] = jc2.text_input("Company", job.get("company", ""), key=f"job_company_{i}")
        jc3, jc4 = st.columns(2)
        job["dates"] = jc3.text_input("Dates (e.g. Jan 2022 – Present)", job.get("dates", ""), key=f"job_dates_{i}")
        job["project"] = jc4.text_input("Project (optional)", job.get("project", ""), key=f"job_project_{i}")

        st.caption("Bullet points (start with an action verb, add numbers where possible)")
        for bi, bullet in enumerate(job["bullets"]):
            bc1, bc2 = st.columns([6, 0.5])
            job["bullets"][bi] = bc1.text_input(
                f"Bullet {bi+1}", bullet, key=f"job_{i}_bullet_{bi}", label_visibility="collapsed"
            )
            if bc2.button("✕", key=f"job_{i}_bullet_del_{bi}") and len(job["bullets"]) > 1:
                job["bullets"].pop(bi)
                st.rerun()
        if st.button("+ Add bullet", key=f"job_{i}_add_bullet"):
            job["bullets"].append("")
            st.rerun()

        if st.button("Remove this job", key=f"job_del_{i}") and len(st.session_state["experience"]) > 1:
            st.session_state["experience"].pop(i)
            st.rerun()
if st.button("+ Add another job"):
    st.session_state["experience"].append({"role": "", "company": "", "dates": "", "project": "", "bullets": [""]})
    st.rerun()

st.markdown("**Certifications**")
for i, cert in enumerate(st.session_state["certifications"]):
    cc1, cc2 = st.columns([6, 0.5])
    st.session_state["certifications"][i] = cc1.text_input(
        f"Certification {i+1}", cert, key=f"cert_{i}", label_visibility="collapsed"
    )
    if cc2.button("✕", key=f"cert_del_{i}") and len(st.session_state["certifications"]) > 1:
        st.session_state["certifications"].pop(i)
        st.rerun()
if st.button("+ Add certification"):
    st.session_state["certifications"].append("")
    st.rerun()

st.markdown("**Awards & Achievements**")
for i, award in enumerate(st.session_state["awards"]):
    ac1, ac2 = st.columns([6, 0.5])
    st.session_state["awards"][i] = ac1.text_input(
        f"Award {i+1}", award, key=f"award_{i}", label_visibility="collapsed"
    )
    if ac2.button("✕", key=f"award_del_{i}") and len(st.session_state["awards"]) > 1:
        st.session_state["awards"].pop(i)
        st.rerun()
if st.button("+ Add award"):
    st.session_state["awards"].append("")
    st.rerun()

st.markdown("**Education**")
for i, edu in enumerate(st.session_state["education"]):
    with st.container(border=True):
        edu["degree"] = st.text_input("Degree", edu.get("degree", ""), key=f"edu_degree_{i}")
        edu["school"] = st.text_input("School / University", edu.get("school", ""), key=f"edu_school_{i}")
        edu["details"] = st.text_input("Year / Grade / Extra details", edu.get("details", ""), key=f"edu_details_{i}")
        if st.button("Remove this education entry", key=f"edu_del_{i}") and len(st.session_state["education"]) > 1:
            st.session_state["education"].pop(i)
            st.rerun()
if st.button("+ Add education entry"):
    st.session_state["education"].append({"degree": "", "school": "", "details": ""})
    st.rerun()

st.divider()


# --------------------------------------------------------------- generate
def _collect_data():
    return {
        "name": st.session_state["name"],
        "title": st.session_state["title"],
        "location": st.session_state["location"],
        "phone": st.session_state["phone"],
        "email": st.session_state["email"],
        "linkedin": st.session_state["linkedin"],
        "summary": st.session_state["summary"],
        "skills": [s for s in st.session_state["skills"] if s.get("label") or s.get("value")],
        "experience": [
            {**job, "bullets": [b for b in job["bullets"] if b.strip()]}
            for job in st.session_state["experience"]
            if job.get("role") or job.get("company")
        ],
        "certifications": [c for c in st.session_state["certifications"] if c.strip()],
        "awards": [a for a in st.session_state["awards"] if a.strip()],
        "education": [e for e in st.session_state["education"] if e.get("degree") or e.get("school")],
    }


st.subheader("4. Generate")
tier = st.session_state["resume_tier"]
st.caption(f"Selected style: **{TIER_INFO[tier]['label']}** — a random template from this tier will be used.")

if st.button("🚀 Generate Resume", type="primary"):
    if not st.session_state["name"].strip():
        st.error("Please enter at least your name before generating.")
    else:
        data = _collect_data()
        template = pick_random_template(tier)
        with st.spinner(f"Building your {TIER_INFO[tier]['label']} resume ({template['name']} template)..."):
            docx_bytes = build_resume(data, template=template)

        st.session_state["generated_docx"] = docx_bytes
        st.session_state["generated_template"] = template
        st.session_state["generated_data"] = data
        st.success(f"Your resume is ready! Template used: **{template['name']}** ({TIER_INFO[tier]['label']} tier)")

if st.session_state.get("generated_docx"):
    data = st.session_state["generated_data"]
    file_name = f"{(data['name'] or 'Resume').replace(' ', '_')}_Resume.docx"
    dcol1, dcol2 = st.columns(2)
    with dcol1:
        st.download_button(
            "⬇️ Download Resume (.docx)",
            data=st.session_state["generated_docx"],
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with dcol2:
        check_ats = st.button("🔎 Check ATS Score", use_container_width=True)

    if check_ats:
        result = score_resume(data)
        total = result["total"]

        if total >= 90:
            color = "#1E7B34"
            verdict = "Excellent — highly likely to pass ATS screening."
        elif total >= 75:
            color = "#B8860B"
            verdict = "Good — a few improvements would push this into the top tier."
        else:
            color = "#B33A3A"
            verdict = "Needs work — add more detail before applying."

        st.markdown(
            f"""
            <div style="text-align:center; padding: 18px 0;">
              <div style="font-size:52px; font-weight:800; color:{color};">{total}<span style="font-size:22px;color:#888;">/100</span></div>
              <div style="font-size:15px; color:{color}; font-weight:600;">{verdict}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(min(total, 100) / 100)

        st.markdown("**Score breakdown**")
        for label, s, m, detail in result["breakdown"]:
            pct = s / m if m else 0
            st.write(f"**{label}** — {s}/{m}")
            st.progress(pct)
            st.caption(detail)

        if total < 90:
            st.info(
                "Tip: add numbers/metrics to your bullet points (e.g. \"reduced costs by 20%\"), "
                "start each bullet with an action verb, and make sure every section above has content — "
                "these are the biggest score drivers."
            )
