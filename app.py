"""
🔍 AI Job Hunter Pro - Powered by Gemini + Google Search Grounding
Smart job matching, company analysis, and trust scoring platform.
"""

import streamlit as st
import json
import time
import hashlib
from datetime import datetime

# ─── Page Config ───
st.set_page_config(
    page_title="AI Job Hunter Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───
st.markdown("""
<style>
/* ── Import Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,500;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Global ── */
.stApp {
    font-family: 'DM Sans', sans-serif;
}

/* ── Hero Header ── */
.hero-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(56, 189, 248, 0.06) 0%, transparent 50%),
                radial-gradient(circle at 70% 50%, rgba(168, 85, 247, 0.04) 0%, transparent 50%);
    pointer-events: none;
}
.hero-header h1 {
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    font-size: 2rem;
    background: linear-gradient(135deg, #38bdf8, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.5rem 0;
    position: relative;
}
.hero-header p {
    color: #94a3b8;
    font-size: 1rem;
    margin: 0;
    position: relative;
}

/* ── Stat Card ── */
.stat-card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border: 1px solid rgba(56, 189, 248, 0.1);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}
.stat-card:hover {
    border-color: rgba(56, 189, 248, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(56, 189, 248, 0.1);
}
.stat-number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #38bdf8;
    display: block;
}
.stat-label {
    color: #64748b;
    font-size: 0.85rem;
    margin-top: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Job Card ── */
.job-card {
    background: linear-gradient(145deg, #1e293b, #162032);
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.job-card:hover {
    border-color: rgba(56, 189, 248, 0.3);
    box-shadow: 0 4px 20px rgba(56, 189, 248, 0.08);
}
.job-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(180deg, #38bdf8, #a78bfa);
    border-radius: 4px 0 0 4px;
}
.job-title {
    font-weight: 700;
    font-size: 1.15rem;
    color: #f1f5f9;
    margin-bottom: 0.4rem;
}
.job-company {
    color: #38bdf8;
    font-weight: 500;
    font-size: 0.95rem;
}
.job-location {
    color: #64748b;
    font-size: 0.85rem;
    margin-top: 0.2rem;
}
.job-match {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 0.5rem;
}
.match-high { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
.match-medium { background: rgba(250, 204, 21, 0.15); color: #facc15; border: 1px solid rgba(250, 204, 21, 0.3); }
.match-low { background: rgba(248, 113, 113, 0.15); color: #f87171; border: 1px solid rgba(248, 113, 113, 0.3); }

/* ── Trust Badge ── */
.trust-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
}
.trust-high { background: rgba(34, 197, 94, 0.12); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.25); }
.trust-medium { background: rgba(250, 204, 21, 0.12); color: #facc15; border: 1px solid rgba(250, 204, 21, 0.25); }
.trust-low { background: rgba(248, 113, 113, 0.12); color: #f87171; border: 1px solid rgba(248, 113, 113, 0.25); }

/* ── Company Review Card ── */
.review-card {
    background: linear-gradient(145deg, #1e293b, #162032);
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1rem;
}
.review-section-title {
    font-weight: 700;
    color: #f1f5f9;
    font-size: 1.1rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Sidebar Styling ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}

/* ── Button Override ── */
.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
    transition: all 0.3s ease;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    font-family: 'DM Sans', sans-serif;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
}

/* ── Info Box ── */
.info-box {
    background: rgba(56, 189, 248, 0.08);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    color: #94a3b8;
    font-size: 0.9rem;
    margin: 0.75rem 0;
}

/* ── Divider ── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.2), transparent);
    margin: 1.5rem 0;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f172a; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #475569; }

/* ── Loading Animation ── */
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 5px rgba(56, 189, 248, 0.2); }
    50% { box-shadow: 0 0 20px rgba(56, 189, 248, 0.4); }
}
.searching {
    animation: pulse-glow 2s ease-in-out infinite;
}

/* ── Tag ── */
.skill-tag {
    display: inline-block;
    background: rgba(168, 85, 247, 0.12);
    color: #c4b5fd;
    border: 1px solid rgba(168, 85, 247, 0.25);
    border-radius: 8px;
    padding: 0.2rem 0.6rem;
    font-size: 0.78rem;
    margin: 0.15rem;
    font-family: 'JetBrains Mono', monospace;
}
</style>
""", unsafe_allow_html=True)


# ─── Session State Initialization ───
if "jobs_database" not in st.session_state:
    st.session_state.jobs_database = []
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if "company_reviews" not in st.session_state:
    st.session_state.company_reviews = {}
if "cv_text" not in st.session_state:
    st.session_state.cv_text = ""
if "cv_analysis" not in st.session_state:
    st.session_state.cv_analysis = None
if "search_count" not in st.session_state:
    st.session_state.search_count = 0
if "total_jobs_found" not in st.session_state:
    st.session_state.total_jobs_found = 0

# ─── Load API Key from Streamlit Secrets (Cloud) or manual input ───
def get_api_key():
    """Get API key from Streamlit secrets (Cloud) or session state (manual input)."""
    # Priority 1: Streamlit Cloud secrets
    try:
        key = st.secrets.get("gemini", {}).get("api_key", "")
        if key and key != "YOUR_GEMINI_API_KEY_HERE":
            return key
    except Exception:
        pass
    # Priority 2: Manual input from session state
    return st.session_state.get("api_key_input", "")


# ─── Gemini API Functions ───
def call_gemini(prompt, use_search=False, api_key=""):
    """Call Gemini API with optional Google Search grounding."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        if use_search:
            # Use google_search tool (current supported syntax)
            response = model.generate_content(
                contents=prompt,
                tools={"google_search": {}},
            )
        else:
            response = model.generate_content(contents=prompt)
        
        return response.text
    except Exception as e:
        return f"ERROR: {str(e)}"


def search_jobs(criteria, api_key):
    """Search for jobs using Gemini + Google Search Grounding."""
    prompt = f"""
Kamu adalah asisten pencari kerja profesional. Cari lowongan kerja berdasarkan kriteria berikut:

KRITERIA PENCARIAN:
{criteria}

INSTRUKSI PENTING:
1. Cari sebanyak mungkin lowongan yang relevan dari Jobstreet Indonesia, LinkedIn, Glints, Kalibrr, dan sumber lainnya
2. Prioritaskan hasil dari jobstreet.co.id dan id.indeed.com
3. Untuk setiap lowongan, berikan informasi LENGKAP

FORMAT OUTPUT - Berikan HANYA JSON array tanpa backtick atau markdown, dengan format:
[
  {{
    "title": "Judul Posisi",
    "company": "Nama Perusahaan",
    "location": "Lokasi",
    "salary_range": "Range Gaji (jika ada, atau 'Tidak dicantumkan')",
    "job_type": "Full-time/Part-time/Contract/Remote",
    "requirements": ["req1", "req2", "req3"],
    "description": "Deskripsi singkat pekerjaan dalam 2-3 kalimat",
    "source": "Sumber (Jobstreet/LinkedIn/Glints/dll)",
    "url": "URL lowongan jika tersedia, atau '#'",
    "posted_date": "Tanggal posting atau 'Baru-baru ini'"
  }}
]

Berikan MINIMAL 8-15 lowongan yang paling relevan. Jika tidak menemukan cukup banyak, perluas pencarian ke sumber lain.
Pastikan output HANYA berupa JSON array yang valid, tanpa teks tambahan apapun.
"""
    return call_gemini(prompt, use_search=True, api_key=api_key)


def match_cv_with_jobs(cv_text, jobs, api_key):
    """Match CV with found jobs using Gemini."""
    jobs_text = json.dumps(jobs, ensure_ascii=False, indent=2)
    prompt = f"""
Kamu adalah AI career advisor profesional. Analisis kecocokan antara CV kandidat dengan lowongan kerja yang ditemukan.

CV KANDIDAT:
{cv_text}

LOWONGAN KERJA YANG DITEMUKAN:
{jobs_text}

INSTRUKSI:
Untuk SETIAP lowongan, berikan analisis kecocokan. Berikan HANYA JSON array tanpa backtick atau markdown:

[
  {{
    "job_index": 0,
    "match_score": 85,
    "match_level": "HIGH/MEDIUM/LOW",
    "matching_skills": ["skill1", "skill2"],
    "missing_skills": ["skill1"],
    "recommendation": "Penjelasan singkat mengapa cocok/tidak cocok",
    "tips": "Tips spesifik untuk melamar posisi ini"
  }}
]

ATURAN SCORING:
- 80-100: HIGH match - kualifikasi sangat sesuai
- 50-79: MEDIUM match - cukup sesuai, ada beberapa gap
- 0-49: LOW match - banyak gap signifikan

Pastikan output HANYA berupa JSON array yang valid.
"""
    return call_gemini(prompt, use_search=False, api_key=api_key)


def analyze_company(company_name, api_key):
    """Analyze company reputation and trustworthiness using Gemini + Search."""
    prompt = f"""
Kamu adalah analis perusahaan profesional. Lakukan riset mendalam tentang perusahaan berikut:

PERUSAHAAN: {company_name}

Cari informasi dari berbagai sumber: review karyawan (Glassdoor, Jobplanet, Indeed), berita, media sosial, dan data publik lainnya.

Berikan HANYA JSON tanpa backtick atau markdown, dengan format:
{{
  "company_name": "{company_name}",
  "industry": "Industri perusahaan",
  "founded": "Tahun berdiri atau 'Tidak diketahui'",
  "size": "Ukuran perusahaan (jumlah karyawan)",
  "headquarters": "Lokasi kantor pusat",
  "description": "Deskripsi singkat perusahaan (2-3 kalimat)",
  "trust_score": 75,
  "trust_level": "HIGH/MEDIUM/LOW",
  "glassdoor_rating": "Rating jika ada atau 'N/A'",
  "pros": ["kelebihan1", "kelebihan2", "kelebihan3"],
  "cons": ["kekurangan1", "kekurangan2"],
  "red_flags": ["red flag jika ada"],
  "green_flags": ["green flag jika ada"],
  "salary_reputation": "Reputasi gaji (Kompetitif/Rata-rata/Di bawah rata-rata/Tidak ada data)",
  "work_life_balance": "Rating WLB (Baik/Cukup/Buruk/Tidak ada data)",
  "career_growth": "Peluang karir (Baik/Cukup/Terbatas/Tidak ada data)",
  "news_summary": "Ringkasan berita terkini tentang perusahaan (2-3 kalimat)",
  "overall_verdict": "Verdict keseluruhan dalam 2-3 kalimat",
  "recommendation": "RECOMMENDED/PROCEED_WITH_CAUTION/NOT_RECOMMENDED"
}}

ATURAN TRUST SCORE:
- 80-100: HIGH - Perusahaan terpercaya, reputasi baik
- 50-79: MEDIUM - Cukup baik, ada beberapa catatan
- 0-49: LOW - Banyak masalah, perlu hati-hati

Berikan penilaian JUJUR dan OBJEKTIF berdasarkan data yang ditemukan.
Pastikan output HANYA berupa JSON object yang valid.
"""
    return call_gemini(prompt, use_search=True, api_key=api_key)


def analyze_cv(cv_text, api_key):
    """Analyze CV and extract key information."""
    prompt = f"""
Analisis CV berikut dan ekstrak informasi kunci.

CV:
{cv_text}

Berikan HANYA JSON tanpa backtick atau markdown:
{{
  "name": "Nama kandidat",
  "current_role": "Posisi saat ini atau terakhir",
  "experience_years": "Estimasi tahun pengalaman",
  "education": "Pendidikan terakhir",
  "top_skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
  "industries": ["industri1", "industri2"],
  "summary": "Ringkasan profil profesional dalam 2-3 kalimat",
  "suggested_roles": ["role1", "role2", "role3"],
  "suggested_keywords": ["keyword pencarian1", "keyword pencarian2", "keyword pencarian3"]
}}

Pastikan output HANYA berupa JSON object yang valid.
"""
    return call_gemini(prompt, use_search=False, api_key=api_key)


def parse_json_response(response_text):
    """Parse JSON from Gemini response, handling various formats."""
    if response_text.startswith("ERROR:"):
        return None
    
    text = response_text.strip()
    # Remove markdown code fences
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find JSON in the response
        start_arr = text.find('[')
        start_obj = text.find('{')
        
        if start_arr != -1 and (start_obj == -1 or start_arr < start_obj):
            end = text.rfind(']') + 1
            if end > start_arr:
                try:
                    return json.loads(text[start_arr:end])
                except:
                    pass
        
        if start_obj != -1:
            end = text.rfind('}') + 1
            if end > start_obj:
                try:
                    return json.loads(text[start_obj:end])
                except:
                    pass
        
        return None


def generate_job_id(job):
    """Generate unique ID for a job."""
    unique_str = f"{job.get('title','')}{job.get('company','')}{job.get('location','')}"
    return hashlib.md5(unique_str.encode()).hexdigest()[:12]


# ─── UI Components ───
def render_header():
    st.markdown("""
    <div class="hero-header">
        <h1>🎯 AI Job Hunter Pro</h1>
        <p>Pencarian kerja cerdas dengan AI — temukan, cocokkan, dan verifikasi perusahaan impian Anda</p>
    </div>
    """, unsafe_allow_html=True)


def render_stats():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-number">{len(st.session_state.jobs_database)}</span>
            <div class="stat-label">Lowongan Tersimpan</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-number">{st.session_state.search_count}</span>
            <div class="stat-label">Total Pencarian</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-number">{len(st.session_state.company_reviews)}</span>
            <div class="stat-label">Perusahaan Diulas</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        high_match = sum(1 for j in st.session_state.jobs_database if j.get("match_level") == "HIGH")
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-number">{high_match}</span>
            <div class="stat-label">High Match</div>
        </div>
        """, unsafe_allow_html=True)


def render_job_card(job, index, show_match=True):
    """Render a single job card."""
    match_score = job.get("match_score", 0)
    match_level = job.get("match_level", "N/A")
    
    if match_level == "HIGH":
        match_class = "match-high"
        match_emoji = "🟢"
    elif match_level == "MEDIUM":
        match_class = "match-medium"
        match_emoji = "🟡"
    elif match_level == "LOW":
        match_class = "match-low"
        match_emoji = "🔴"
    else:
        match_class = ""
        match_emoji = "⚪"
    
    skills_html = ""
    for skill in job.get("requirements", [])[:6]:
        skills_html += f'<span class="skill-tag">{skill}</span>'
    
    match_html = ""
    if show_match and match_level != "N/A":
        match_html = f'<span class="job-match {match_class}">{match_emoji} {match_score}% Match</span>'
    
    salary = job.get("salary_range", "Tidak dicantumkan")
    source = job.get("source", "N/A")
    
    st.markdown(f"""
    <div class="job-card">
        <div class="job-title">{job.get("title", "N/A")}</div>
        <div class="job-company">🏢 {job.get("company", "N/A")}</div>
        <div class="job-location">📍 {job.get("location", "N/A")} &nbsp;|&nbsp; 💰 {salary} &nbsp;|&nbsp; 🌐 {source}</div>
        <div style="margin-top: 0.5rem;">{skills_html}</div>
        {match_html}
    </div>
    """, unsafe_allow_html=True)


def render_company_review(review):
    """Render company review card."""
    trust_score = review.get("trust_score", 0)
    trust_level = review.get("trust_level", "N/A")
    rec = review.get("recommendation", "N/A")
    
    if trust_level == "HIGH":
        trust_class = "trust-high"
        trust_emoji = "✅"
    elif trust_level == "MEDIUM":
        trust_class = "trust-medium"
        trust_emoji = "⚠️"
    else:
        trust_class = "trust-low"
        trust_emoji = "❌"
    
    rec_text = {
        "RECOMMENDED": "✅ Direkomendasikan",
        "PROCEED_WITH_CAUTION": "⚠️ Lanjutkan dengan Hati-hati",
        "NOT_RECOMMENDED": "❌ Tidak Direkomendasikan"
    }.get(rec, rec)
    
    pros_html = "".join(f"<li style='color:#4ade80;margin:0.2rem 0;'>{p}</li>" for p in review.get("pros", []))
    cons_html = "".join(f"<li style='color:#f87171;margin:0.2rem 0;'>{c}</li>" for c in review.get("cons", []))
    green_html = "".join(f"<li style='color:#4ade80;margin:0.2rem 0;'>{g}</li>" for g in review.get("green_flags", []))
    red_html = "".join(f"<li style='color:#f87171;margin:0.2rem 0;'>{r}</li>" for r in review.get("red_flags", []))
    
    st.markdown(f"""
    <div class="review-card">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
            <div>
                <h2 style="color:#f1f5f9;margin:0;font-size:1.5rem;">{review.get("company_name", "N/A")}</h2>
                <p style="color:#64748b;margin:0.25rem 0;">{review.get("industry", "")} · {review.get("size", "")} · {review.get("headquarters", "")}</p>
            </div>
            <div style="text-align:right;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:700;color:{'#4ade80' if trust_score>=80 else '#facc15' if trust_score>=50 else '#f87171'};">
                    {trust_score}/100
                </div>
                <span class="trust-badge {trust_class}">{trust_emoji} {trust_level} TRUST</span>
            </div>
        </div>
        <div class="section-divider"></div>
        <p style="color:#cbd5e1;font-size:0.95rem;">{review.get("description", "")}</p>
        
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem;">
            <div>
                <div class="review-section-title">👍 Kelebihan</div>
                <ul style="padding-left:1.2rem;margin:0;">{pros_html}</ul>
            </div>
            <div>
                <div class="review-section-title">👎 Kekurangan</div>
                <ul style="padding-left:1.2rem;margin:0;">{cons_html}</ul>
            </div>
        </div>
        
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem;">
            <div>
                <div class="review-section-title">🟢 Green Flags</div>
                <ul style="padding-left:1.2rem;margin:0;">{green_html}</ul>
            </div>
            <div>
                <div class="review-section-title">🔴 Red Flags</div>
                <ul style="padding-left:1.2rem;margin:0;">{red_html if red_html else '<li style="color:#64748b;">Tidak ada red flag ditemukan</li>'}</ul>
            </div>
        </div>
        
        <div class="section-divider"></div>
        
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;text-align:center;">
            <div>
                <div style="color:#64748b;font-size:0.8rem;text-transform:uppercase;">Gaji</div>
                <div style="color:#f1f5f9;font-weight:600;">{review.get("salary_reputation", "N/A")}</div>
            </div>
            <div>
                <div style="color:#64748b;font-size:0.8rem;text-transform:uppercase;">Work-Life Balance</div>
                <div style="color:#f1f5f9;font-weight:600;">{review.get("work_life_balance", "N/A")}</div>
            </div>
            <div>
                <div style="color:#64748b;font-size:0.8rem;text-transform:uppercase;">Karir</div>
                <div style="color:#f1f5f9;font-weight:600;">{review.get("career_growth", "N/A")}</div>
            </div>
        </div>
        
        <div class="section-divider"></div>
        
        <div class="review-section-title">📰 Berita Terkini</div>
        <p style="color:#94a3b8;font-size:0.9rem;">{review.get("news_summary", "Tidak ada berita terkini.")}</p>
        
        <div style="background:rgba(56,189,248,0.06);border-radius:12px;padding:1rem;margin-top:1rem;">
            <div style="color:#38bdf8;font-weight:700;margin-bottom:0.5rem;">📋 Verdict</div>
            <p style="color:#e2e8f0;margin:0 0 0.5rem 0;">{review.get("overall_verdict", "")}</p>
            <div style="font-weight:700;font-size:1.1rem;">{rec_text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Sidebar ───
with st.sidebar:
    st.markdown("### ⚙️ Konfigurasi")
    
    # Check if secret is already configured in Streamlit Cloud
    cloud_key_available = False
    try:
        cloud_key = st.secrets.get("gemini", {}).get("api_key", "")
        if cloud_key and cloud_key != "YOUR_GEMINI_API_KEY_HERE":
            cloud_key_available = True
    except Exception:
        pass
    
    if cloud_key_available:
        st.success("✅ API Key terhubung via Cloud Secrets")
        api_key = get_api_key()
    else:
        api_key_input = st.text_input(
            "🔑 Gemini API Key",
            type="password",
            value=st.session_state.get("api_key_input", ""),
            help="Dapatkan API key gratis di aistudio.google.com"
        )
        if api_key_input:
            st.session_state.api_key_input = api_key_input
        api_key = get_api_key()
        
        if api_key:
            st.success("✅ API Key terhubung")
        else:
            st.warning("⚠️ Masukkan API Key untuk mulai")
            st.markdown("""
            <div class="info-box">
                <strong>Cara mendapatkan API Key gratis:</strong><br>
                1. Buka <a href="https://aistudio.google.com" target="_blank">aistudio.google.com</a><br>
                2. Login dengan akun Google<br>
                3. Klik "Get API Key"<br>
                4. Salin dan tempel di sini
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📄 Upload CV")
    cv_file = st.file_uploader(
        "Upload CV Anda (PDF/TXT)",
        type=["pdf", "txt"],
        help="CV akan dianalisis untuk mencocokkan dengan lowongan"
    )
    
    cv_manual = st.text_area(
        "Atau paste CV / ringkasan profil Anda:",
        value=st.session_state.cv_text,
        height=150,
        placeholder="Contoh: 5 tahun pengalaman sebagai Data Analyst, mahir Python, SQL, Tableau, pengalaman di industri fintech..."
    )
    
    if cv_file:
        if cv_file.type == "text/plain":
            st.session_state.cv_text = cv_file.read().decode("utf-8")
        elif cv_file.type == "application/pdf":
            try:
                import PyPDF2
                import io
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(cv_file.read()))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
                st.session_state.cv_text = text
            except ImportError:
                st.error("Install PyPDF2: `pip install PyPDF2`")
            except Exception as e:
                st.error(f"Error membaca PDF: {e}")
    elif cv_manual:
        st.session_state.cv_text = cv_manual
    
    if st.session_state.cv_text and api_key:
        if st.button("🔍 Analisis CV", use_container_width=True):
            with st.spinner("Menganalisis CV..."):
                result = analyze_cv(st.session_state.cv_text, api_key)
                parsed = parse_json_response(result)
                if parsed:
                    st.session_state.cv_analysis = parsed
                    st.success("✅ CV berhasil dianalisis!")
                else:
                    st.error("Gagal menganalisis CV. Coba lagi.")
    
    if st.session_state.cv_analysis:
        cv = st.session_state.cv_analysis
        st.markdown("---")
        st.markdown("### 👤 Profil Anda")
        st.markdown(f"**{cv.get('name', 'N/A')}**")
        st.markdown(f"📌 {cv.get('current_role', 'N/A')}")
        st.markdown(f"⏱️ {cv.get('experience_years', 'N/A')} tahun pengalaman")
        st.markdown(f"🎓 {cv.get('education', 'N/A')}")
        st.markdown("**Top Skills:**")
        for skill in cv.get("top_skills", []):
            st.markdown(f"` {skill} `")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;color:#475569;font-size:0.75rem;padding:1rem 0;">
        Built with Streamlit + Gemini AI<br>
        Free tier: ~500 searches/day
    </div>
    """, unsafe_allow_html=True)


# ─── Main Content ───
render_header()
render_stats()

# ─── Tabs ───
tab_search, tab_database, tab_reviews, tab_help = st.tabs([
    "🔍 Pencarian Lowongan",
    "📂 Database Lowongan",
    "🏢 Ulasan Perusahaan",
    "❓ Panduan"
])

# ══════════════════════════════════════════════
# TAB 1: JOB SEARCH
# ══════════════════════════════════════════════
with tab_search:
    st.markdown("### 🔍 Cari Lowongan Kerja")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        job_keyword = st.text_input(
            "🎯 Posisi / Kata Kunci",
            placeholder="Contoh: Data Analyst, Software Engineer, Marketing Manager"
        )
        
        col_loc, col_type = st.columns(2)
        with col_loc:
            job_location = st.text_input(
                "📍 Lokasi",
                placeholder="Contoh: Jakarta, Bandung, Remote"
            )
        with col_type:
            job_type = st.selectbox(
                "💼 Tipe Pekerjaan",
                ["Semua", "Full-time", "Part-time", "Contract", "Remote", "Internship"]
            )
    
    with col_right:
        salary_min = st.text_input(
            "💰 Gaji Minimum (opsional)",
            placeholder="Contoh: 10000000"
        )
        experience_level = st.selectbox(
            "📊 Level Pengalaman",
            ["Semua", "Fresh Graduate", "Junior (1-3 tahun)", "Mid (3-5 tahun)", "Senior (5+ tahun)", "Manager"]
        )
        additional_filter = st.text_input(
            "🔧 Filter Tambahan (opsional)",
            placeholder="Contoh: Python, remote-friendly"
        )
    
    # Build search criteria
    criteria_parts = []
    if job_keyword:
        criteria_parts.append(f"Posisi: {job_keyword}")
    if job_location:
        criteria_parts.append(f"Lokasi: {job_location}")
    if job_type != "Semua":
        criteria_parts.append(f"Tipe: {job_type}")
    if salary_min:
        criteria_parts.append(f"Gaji minimum: Rp {salary_min}")
    if experience_level != "Semua":
        criteria_parts.append(f"Level: {experience_level}")
    if additional_filter:
        criteria_parts.append(f"Filter: {additional_filter}")
    
    search_criteria = "\n".join(criteria_parts)
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        search_clicked = st.button(
            "🚀 Cari Lowongan",
            use_container_width=True,
            type="primary",
            disabled=not (job_keyword and api_key)
        )
    
    with col_btn2:
        search_and_match = st.button(
            "🎯 Cari & Cocokkan dengan CV",
            use_container_width=True,
            disabled=not (job_keyword and api_key and st.session_state.cv_text)
        )
    
    if not api_key:
        st.info("👈 Masukkan Gemini API Key di sidebar untuk mulai pencarian.")
    
    if search_clicked or search_and_match:
        if not job_keyword:
            st.warning("Masukkan kata kunci posisi terlebih dahulu.")
        else:
            # Search jobs
            with st.status("🔍 Mencari lowongan...", expanded=True) as status:
                st.write("🌐 Menghubungi Gemini AI + Google Search...")
                st.write(f"📋 Kriteria: {search_criteria}")
                
                raw_result = search_jobs(search_criteria, api_key)
                
                st.write("📊 Memproses hasil pencarian...")
                jobs = parse_json_response(raw_result)
                
                if jobs and isinstance(jobs, list):
                    st.session_state.search_count += 1
                    st.write(f"✅ Ditemukan {len(jobs)} lowongan!")
                    
                    # Match with CV if requested
                    if search_and_match and st.session_state.cv_text:
                        st.write("🤖 Mencocokkan dengan CV Anda...")
                        match_result = match_cv_with_jobs(
                            st.session_state.cv_text, jobs, api_key
                        )
                        matches = parse_json_response(match_result)
                        
                        if matches and isinstance(matches, list):
                            for match in matches:
                                idx = match.get("job_index", 0)
                                if 0 <= idx < len(jobs):
                                    jobs[idx]["match_score"] = match.get("match_score", 0)
                                    jobs[idx]["match_level"] = match.get("match_level", "N/A")
                                    jobs[idx]["matching_skills"] = match.get("matching_skills", [])
                                    jobs[idx]["missing_skills"] = match.get("missing_skills", [])
                                    jobs[idx]["recommendation"] = match.get("recommendation", "")
                                    jobs[idx]["tips"] = match.get("tips", "")
                            
                            # Sort by match score
                            jobs.sort(key=lambda x: x.get("match_score", 0), reverse=True)
                            st.write("✅ Pencocokan CV selesai!")
                    
                    # Add unique ID and timestamp
                    for job in jobs:
                        job["id"] = generate_job_id(job)
                        job["found_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        job["search_query"] = job_keyword
                    
                    st.session_state.latest_results = jobs
                    status.update(label=f"✅ Selesai — {len(jobs)} lowongan ditemukan!", state="complete")
                else:
                    st.session_state.latest_results = []
                    status.update(label="⚠️ Tidak ada hasil atau format error", state="error")
                    if raw_result.startswith("ERROR:"):
                        st.error(raw_result)
                    else:
                        st.warning("Gemini tidak mengembalikan format yang valid. Coba ubah kata kunci.")
                        with st.expander("🔧 Debug: Raw Response"):
                            st.code(raw_result[:2000])
    
    # Display results
    if "latest_results" in st.session_state and st.session_state.latest_results:
        results = st.session_state.latest_results
        
        st.markdown("---")
        st.markdown(f"### 📋 Hasil Pencarian ({len(results)} lowongan)")
        
        # Filter & sort options
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            sort_by = st.selectbox(
                "Urutkan berdasarkan:",
                ["Match Score (Tertinggi)", "Match Score (Terendah)", "Default"]
            )
        with col_f2:
            filter_match = st.selectbox(
                "Filter match level:",
                ["Semua", "HIGH", "MEDIUM", "LOW"]
            )
        
        filtered = results
        if filter_match != "Semua":
            filtered = [j for j in results if j.get("match_level") == filter_match]
        
        if sort_by == "Match Score (Tertinggi)":
            filtered.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        elif sort_by == "Match Score (Terendah)":
            filtered.sort(key=lambda x: x.get("match_score", 0))
        
        # Save all to database button
        if st.button("💾 Simpan SEMUA ke Database", use_container_width=True):
            existing_ids = {j["id"] for j in st.session_state.jobs_database}
            added = 0
            for job in filtered:
                if job["id"] not in existing_ids:
                    st.session_state.jobs_database.append(job)
                    existing_ids.add(job["id"])
                    added += 1
            st.success(f"✅ {added} lowongan baru ditambahkan ke database! ({len(filtered) - added} sudah ada)")
        
        # Display each job
        for i, job in enumerate(filtered):
            render_job_card(job, i, show_match=True)
            
            with st.expander(f"📝 Detail — {job.get('title', 'N/A')} @ {job.get('company', 'N/A')}"):
                col_d1, col_d2 = st.columns([2, 1])
                
                with col_d1:
                    st.markdown(f"**Deskripsi:** {job.get('description', 'N/A')}")
                    st.markdown(f"**Tipe:** {job.get('job_type', 'N/A')}")
                    st.markdown(f"**Tanggal:** {job.get('posted_date', 'N/A')}")
                    
                    if job.get("url") and job["url"] != "#":
                        st.markdown(f"🔗 [Buka Lowongan]({job['url']})")
                    
                    if job.get("recommendation"):
                        st.info(f"💡 **Rekomendasi:** {job['recommendation']}")
                    if job.get("tips"):
                        st.success(f"📌 **Tips Melamar:** {job['tips']}")
                
                with col_d2:
                    if job.get("matching_skills"):
                        st.markdown("**✅ Skills Cocok:**")
                        for s in job["matching_skills"]:
                            st.markdown(f"- {s}")
                    if job.get("missing_skills"):
                        st.markdown("**⚠️ Skills Kurang:**")
                        for s in job["missing_skills"]:
                            st.markdown(f"- {s}")
                
                col_act1, col_act2 = st.columns(2)
                with col_act1:
                    if st.button(f"💾 Simpan ke Database", key=f"save_{i}"):
                        existing_ids = {j["id"] for j in st.session_state.jobs_database}
                        if job["id"] not in existing_ids:
                            st.session_state.jobs_database.append(job)
                            st.success("✅ Tersimpan!")
                        else:
                            st.info("ℹ️ Sudah ada di database")
                
                with col_act2:
                    if st.button(f"🏢 Ulas Perusahaan", key=f"review_{i}"):
                        company = job.get("company", "")
                        if company:
                            with st.spinner(f"Menganalisis {company}..."):
                                review_result = analyze_company(company, api_key)
                                review = parse_json_response(review_result)
                                if review:
                                    st.session_state.company_reviews[company] = review
                                    st.success(f"✅ Ulasan {company} tersimpan! Lihat di tab Ulasan Perusahaan.")
                                else:
                                    st.error("Gagal menganalisis perusahaan.")


# ══════════════════════════════════════════════
# TAB 2: DATABASE
# ══════════════════════════════════════════════
with tab_database:
    st.markdown("### 📂 Database Lowongan Tersimpan")
    
    if not st.session_state.jobs_database:
        st.markdown("""
        <div class="info-box">
            <strong>Database masih kosong.</strong><br>
            Mulai pencarian di tab "Pencarian Lowongan" dan simpan lowongan yang menarik ke sini.
        </div>
        """, unsafe_allow_html=True)
    else:
        # Database controls
        col_db1, col_db2, col_db3 = st.columns([2, 1, 1])
        with col_db1:
            db_search = st.text_input("🔍 Cari di database:", placeholder="Filter berdasarkan judul, perusahaan, atau lokasi")
        with col_db2:
            db_sort = st.selectbox(
                "Urutkan:",
                ["Terbaru", "Match Tertinggi", "Match Terendah", "Perusahaan A-Z"],
                key="db_sort"
            )
        with col_db3:
            db_filter_level = st.selectbox(
                "Filter level:",
                ["Semua", "HIGH", "MEDIUM", "LOW"],
                key="db_filter"
            )
        
        filtered_db = st.session_state.jobs_database.copy()
        
        if db_search:
            db_search_lower = db_search.lower()
            filtered_db = [
                j for j in filtered_db
                if db_search_lower in j.get("title", "").lower()
                or db_search_lower in j.get("company", "").lower()
                or db_search_lower in j.get("location", "").lower()
            ]
        
        if db_filter_level != "Semua":
            filtered_db = [j for j in filtered_db if j.get("match_level") == db_filter_level]
        
        if db_sort == "Match Tertinggi":
            filtered_db.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        elif db_sort == "Match Terendah":
            filtered_db.sort(key=lambda x: x.get("match_score", 0))
        elif db_sort == "Perusahaan A-Z":
            filtered_db.sort(key=lambda x: x.get("company", "").lower())
        else:
            filtered_db.reverse()
        
        st.markdown(f"Menampilkan **{len(filtered_db)}** dari **{len(st.session_state.jobs_database)}** lowongan")
        
        # Export option
        if st.button("📤 Export ke JSON"):
            json_str = json.dumps(st.session_state.jobs_database, ensure_ascii=False, indent=2)
            st.download_button(
                "⬇️ Download JSON",
                data=json_str,
                file_name=f"jobs_database_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json"
            )
        
        for i, job in enumerate(filtered_db):
            render_job_card(job, i + 1000, show_match=True)
            
            col_a, col_b, col_c = st.columns([1, 1, 1])
            with col_a:
                if job.get("url") and job["url"] != "#":
                    st.markdown(f"[🔗 Buka Lowongan]({job['url']})")
            with col_b:
                company = job.get("company", "")
                if company and st.button(f"🏢 Ulas {company}", key=f"db_review_{i}"):
                    if api_key:
                        with st.spinner(f"Menganalisis {company}..."):
                            review_result = analyze_company(company, api_key)
                            review = parse_json_response(review_result)
                            if review:
                                st.session_state.company_reviews[company] = review
                                st.success(f"✅ Ulasan tersimpan!")
                    else:
                        st.warning("Masukkan API Key terlebih dahulu.")
            with col_c:
                if st.button("🗑️ Hapus", key=f"del_{i}"):
                    st.session_state.jobs_database = [
                        j for j in st.session_state.jobs_database if j["id"] != job["id"]
                    ]
                    st.rerun()
        
        st.markdown("---")
        if st.button("🗑️ Hapus Semua Database", type="secondary"):
            st.session_state.jobs_database = []
            st.rerun()


# ══════════════════════════════════════════════
# TAB 3: COMPANY REVIEWS
# ══════════════════════════════════════════════
with tab_reviews:
    st.markdown("### 🏢 Ulasan & Trust Score Perusahaan")
    
    # Manual company search
    col_r1, col_r2 = st.columns([3, 1])
    with col_r1:
        company_input = st.text_input(
            "🔍 Cari ulasan perusahaan:",
            placeholder="Masukkan nama perusahaan, contoh: Tokopedia, Gojek, Bank BCA"
        )
    with col_r2:
        st.markdown("<br>", unsafe_allow_html=True)
        review_btn = st.button("🔎 Analisis", use_container_width=True, type="primary")
    
    if review_btn and company_input and api_key:
        with st.spinner(f"🔍 Menganalisis {company_input}..."):
            review_result = analyze_company(company_input, api_key)
            review = parse_json_response(review_result)
            if review:
                st.session_state.company_reviews[company_input] = review
                st.success(f"✅ Analisis selesai!")
            else:
                st.error("Gagal menganalisis. Coba lagi.")
                with st.expander("🔧 Debug"):
                    st.code(review_result[:2000])
    elif review_btn and not api_key:
        st.warning("Masukkan API Key terlebih dahulu.")
    
    # Display all reviews
    if st.session_state.company_reviews:
        st.markdown(f"---")
        st.markdown(f"**{len(st.session_state.company_reviews)} perusahaan telah diulas:**")
        
        for company_name, review in st.session_state.company_reviews.items():
            render_company_review(review)
    else:
        st.markdown("""
        <div class="info-box">
            <strong>Belum ada ulasan perusahaan.</strong><br>
            Anda bisa:<br>
            • Ketik nama perusahaan di atas untuk langsung menganalisis<br>
            • Klik "Ulas Perusahaan" pada lowongan di tab Pencarian atau Database
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4: HELP
# ══════════════════════════════════════════════
with tab_help:
    st.markdown("### ❓ Panduan Penggunaan")
    
    st.markdown("""
    <div class="review-card">
        <div class="review-section-title">🚀 Cara Memulai</div>
        <ol style="color:#cbd5e1;line-height:2;">
            <li><strong>Dapatkan API Key</strong> — Buka <a href="https://aistudio.google.com" target="_blank" style="color:#38bdf8;">aistudio.google.com</a>, login, klik "Get API Key"</li>
            <li><strong>Masukkan API Key</strong> — Tempel di sidebar kiri</li>
            <li><strong>Upload CV</strong> — Upload PDF atau paste ringkasan profil Anda</li>
            <li><strong>Mulai Pencarian</strong> — Masukkan kriteria dan klik "Cari & Cocokkan"</li>
            <li><strong>Simpan & Review</strong> — Simpan lowongan menarik dan ulas perusahaannya</li>
        </ol>
    </div>
    
    <div class="review-card">
        <div class="review-section-title">💡 Tips Pencarian Efektif</div>
        <ul style="color:#cbd5e1;line-height:2;">
            <li>Gunakan kata kunci spesifik: "Data Analyst Python" lebih baik dari "Analyst"</li>
            <li>Coba beberapa variasi kata kunci untuk hasil lebih lengkap</li>
            <li>Setiap pencarian baru akan menambah koleksi di database Anda</li>
            <li>Upload CV yang lengkap untuk pencocokan yang lebih akurat</li>
            <li>Selalu ulas perusahaan sebelum melamar untuk menghindari red flags</li>
        </ul>
    </div>
    
    <div class="review-card">
        <div class="review-section-title">📊 Memahami Skor</div>
        <ul style="color:#cbd5e1;line-height:2;">
            <li><span style="color:#4ade80;font-weight:700;">HIGH (80-100%)</span> — Sangat cocok, langsung apply!</li>
            <li><span style="color:#facc15;font-weight:700;">MEDIUM (50-79%)</span> — Cukup cocok, pertimbangkan untuk upskill</li>
            <li><span style="color:#f87171;font-weight:700;">LOW (0-49%)</span> — Kurang cocok, perlu banyak penyesuaian</li>
        </ul>
        <br>
        <ul style="color:#cbd5e1;line-height:2;">
            <li><span style="color:#4ade80;font-weight:700;">✅ RECOMMENDED</span> — Perusahaan terpercaya</li>
            <li><span style="color:#facc15;font-weight:700;">⚠️ PROCEED WITH CAUTION</span> — Ada beberapa catatan</li>
            <li><span style="color:#f87171;font-weight:700;">❌ NOT RECOMMENDED</span> — Banyak red flag</li>
        </ul>
    </div>
    
    <div class="review-card">
        <div class="review-section-title">💰 Biaya & Batasan</div>
        <ul style="color:#cbd5e1;line-height:2;">
            <li><strong>Gemini API Free Tier:</strong> Gratis, ~500 pencarian Google/hari</li>
            <li><strong>Model yang digunakan:</strong> Gemini 2.0 Flash (gratis)</li>
            <li><strong>Tidak perlu SerpAPI</strong> — Gemini langsung mencari Google</li>
            <li><strong>Data tidak disimpan permanen</strong> — Export ke JSON untuk backup</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
