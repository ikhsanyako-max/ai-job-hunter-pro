"""
🔍 AI Job Hunter Pro v2 - Powered by Gemini REST API + Google Search
Cumulative job search, CV matching, company deep analysis & trust scoring.
"""

import streamlit as st
import json
import requests
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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,500;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;600&display=swap');
.stApp { font-family: 'DM Sans', sans-serif; }
.hero-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 20px; padding: 2.5rem 2rem; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
}
.hero-header::before {
    content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(56,189,248,0.06) 0%, transparent 50%),
                radial-gradient(circle at 70% 50%, rgba(168,85,247,0.04) 0%, transparent 50%);
    pointer-events: none;
}
.hero-header h1 {
    font-family: 'DM Sans', sans-serif; font-weight: 700; font-size: 2rem;
    background: linear-gradient(135deg, #38bdf8, #a78bfa, #38bdf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 0.5rem 0; position: relative;
}
.hero-header p { color: #94a3b8; font-size: 1rem; margin: 0; position: relative; }
.stat-card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border: 1px solid rgba(56, 189, 248, 0.1); border-radius: 16px;
    padding: 1.5rem; text-align: center; transition: all 0.3s ease;
}
.stat-card:hover { border-color: rgba(56,189,248,0.3); transform: translateY(-2px); box-shadow: 0 8px 30px rgba(56,189,248,0.1); }
.stat-number { font-family: 'JetBrains Mono', monospace; font-size: 2rem; font-weight: 700; color: #38bdf8; display: block; }
.stat-label { color: #64748b; font-size: 0.85rem; margin-top: 0.25rem; text-transform: uppercase; letter-spacing: 0.05em; }
.job-card {
    background: linear-gradient(145deg, #1e293b, #162032);
    border: 1px solid rgba(148, 163, 184, 0.1); border-radius: 16px;
    padding: 1.5rem; margin-bottom: 1rem; transition: all 0.3s ease;
    position: relative; overflow: hidden;
}
.job-card:hover { border-color: rgba(56,189,248,0.3); box-shadow: 0 4px 20px rgba(56,189,248,0.08); }
.job-card::after {
    content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%;
    background: linear-gradient(180deg, #38bdf8, #a78bfa); border-radius: 4px 0 0 4px;
}
.job-title { font-weight: 700; font-size: 1.15rem; color: #f1f5f9; margin-bottom: 0.4rem; }
.job-company { color: #38bdf8; font-weight: 500; font-size: 0.95rem; }
.job-location { color: #64748b; font-size: 0.85rem; margin-top: 0.2rem; }
.job-match { display: inline-block; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; font-family: 'JetBrains Mono', monospace; margin-top: 0.5rem; }
.match-high { background: rgba(34,197,94,0.15); color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
.match-medium { background: rgba(250,204,21,0.15); color: #facc15; border: 1px solid rgba(250,204,21,0.3); }
.match-low { background: rgba(248,113,113,0.15); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }
.trust-badge { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.4rem 1rem; border-radius: 20px; font-weight: 600; font-size: 0.85rem; }
.trust-high { background: rgba(34,197,94,0.12); color: #4ade80; border: 1px solid rgba(34,197,94,0.25); }
.trust-medium { background: rgba(250,204,21,0.12); color: #facc15; border: 1px solid rgba(250,204,21,0.25); }
.trust-low { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.25); }
.review-card {
    background: linear-gradient(145deg, #1e293b, #162032);
    border: 1px solid rgba(148,163,184,0.1); border-radius: 16px; padding: 2rem; margin-bottom: 1rem;
}
.review-section-title { font-weight: 700; color: #f1f5f9; font-size: 1.1rem; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%); }
.stButton > button { border-radius: 12px; font-weight: 600; font-family: 'DM Sans', sans-serif; transition: all 0.3s ease; }
.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
.stTabs [data-baseweb="tab"] { border-radius: 10px; font-family: 'DM Sans', sans-serif; }
.info-box { background: rgba(56,189,248,0.08); border: 1px solid rgba(56,189,248,0.2); border-radius: 12px; padding: 1rem 1.25rem; color: #94a3b8; font-size: 0.9rem; margin: 0.75rem 0; }
.section-divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(56,189,248,0.2), transparent); margin: 1.5rem 0; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f172a; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
.skill-tag { display: inline-block; background: rgba(168,85,247,0.12); color: #c4b5fd; border: 1px solid rgba(168,85,247,0.25); border-radius: 8px; padding: 0.2rem 0.6rem; font-size: 0.78rem; margin: 0.15rem; font-family: 'JetBrains Mono', monospace; }
.search-round { background: rgba(56,189,248,0.08); border: 1px solid rgba(56,189,248,0.15); border-radius: 12px; padding: 0.6rem 1rem; margin: 0.5rem 0; color: #94a3b8; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)


# ─── Session State ───
defaults = {
    "jobs_database": [], "search_history": [], "company_reviews": {},
    "cv_text": "", "cv_analysis": None, "search_count": 0,
    "latest_results": [], "cumulative_results": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def get_api_key():
    try:
        key = st.secrets.get("gemini", {}).get("api_key", "")
        if key and key != "YOUR_GEMINI_API_KEY_HERE":
            return key
    except Exception:
        pass
    return st.session_state.get("api_key_input", "")


# ═══════════════════════════════════════
# GEMINI REST API (NO SDK NEEDED)
# ═══════════════════════════════════════

def call_gemini(prompt, use_search=False, api_key=""):
    """Call Gemini via REST API — zero SDK dependency."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    if use_search:
        payload["tools"] = [{"google_search": {}}]
    try:
        resp = requests.post(url, json=payload, timeout=120)
        data = resp.json()
        if "error" in data:
            return f"ERROR: {data['error'].get('message', str(data['error']))}"
        candidates = data.get("candidates", [])
        if not candidates:
            return "ERROR: Tidak ada respons dari Gemini."
        parts = candidates[0].get("content", {}).get("parts", [])
        return "".join(p.get("text", "") for p in parts)
    except requests.exceptions.Timeout:
        return "ERROR: Request timeout. Coba lagi."
    except Exception as e:
        return f"ERROR: {str(e)}"


def parse_json_response(text):
    """Parse JSON from Gemini response."""
    if not text or text.startswith("ERROR:"):
        return None
    t = text.strip()
    for fence in ["```json", "```"]:
        if t.startswith(fence):
            t = t[len(fence):]
    if t.endswith("```"):
        t = t[:-3]
    t = t.strip()
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        for start_char, end_char in [('[', ']'), ('{', '}')]:
            s = t.find(start_char)
            e = t.rfind(end_char)
            if s != -1 and e > s:
                try:
                    return json.loads(t[s:e+1])
                except:
                    continue
    return None


def gen_job_id(job):
    s = f"{job.get('title','')}{job.get('company','')}{job.get('location','')}".lower()
    return hashlib.md5(s.encode()).hexdigest()[:12]


# ═══════════════════════════════════════
# SEARCH PROMPTS
# ═══════════════════════════════════════

def build_search_prompt(criteria, exclude_companies=None, round_num=1):
    """Build search prompt that avoids duplicates across rounds."""
    exclude_text = ""
    if exclude_companies:
        exclude_text = f"""
PENTING - JANGAN tampilkan lowongan dari perusahaan berikut (sudah ditemukan sebelumnya):
{', '.join(exclude_companies)}
Cari dari perusahaan LAIN yang belum pernah muncul.
"""
    
    variation_hints = [
        "Cari dari portal karir perusahaan langsung, startup baru, dan perusahaan menengah.",
        "Fokus pada perusahaan multinasional, BUMN, dan perusahaan manufaktur/industri.",
        "Cari dari perusahaan konsultan, outsourcing, dan perusahaan yang baru buka lowongan.",
        "Fokus pada e-commerce, fintech, healthtech, dan perusahaan teknologi.",
        "Cari dari perusahaan logistik, FMCG, otomotif, dan sektor energi.",
    ]
    hint = variation_hints[(round_num - 1) % len(variation_hints)]
    
    return f"""
Kamu adalah asisten pencari kerja profesional. Cari lowongan kerja berdasarkan kriteria berikut:

KRITERIA: {criteria}

INSTRUKSI KHUSUS RONDE {round_num}:
- {hint}
- Cari dari sumber berbeda: Jobstreet, LinkedIn, Glints, Kalibrr, Indeed, karir.com, portal karir perusahaan
- Berikan MINIMAL 10-15 lowongan yang BERBEDA dari ronde sebelumnya
{exclude_text}

FORMAT: Berikan HANYA JSON array valid tanpa backtick/markdown:
[
  {{
    "title": "Judul Posisi",
    "company": "Nama Perusahaan",
    "location": "Lokasi",
    "salary_range": "Range Gaji (atau 'Tidak dicantumkan')",
    "job_type": "Full-time/Part-time/Contract/Remote",
    "requirements": ["req1", "req2", "req3"],
    "description": "Deskripsi singkat 2-3 kalimat",
    "source": "Sumber (Jobstreet/LinkedIn/dll)",
    "url": "URL lowongan atau '#'",
    "posted_date": "Tanggal posting atau 'Baru-baru ini'"
  }}
]

Pastikan output HANYA JSON array valid. Jangan ulangi perusahaan yang sama.
"""


def build_match_prompt(cv_text, jobs):
    jobs_json = json.dumps(jobs, ensure_ascii=False)
    return f"""
Analisis kecocokan CV dengan lowongan kerja.

CV: {cv_text}

LOWONGAN: {jobs_json}

Berikan HANYA JSON array tanpa backtick:
[
  {{
    "job_index": 0,
    "match_score": 85,
    "match_level": "HIGH/MEDIUM/LOW",
    "matching_skills": ["skill1", "skill2"],
    "missing_skills": ["skill1"],
    "recommendation": "Penjelasan singkat",
    "tips": "Tips melamar"
  }}
]
Scoring: 80-100=HIGH, 50-79=MEDIUM, 0-49=LOW.
"""


def build_company_prompt(company_name):
    return f"""
Lakukan riset mendalam tentang perusahaan: {company_name}

Cari dari SEMUA sumber yang tersedia: website resmi perusahaan, Google, review karyawan (Glassdoor, Jobplanet, Indeed), LinkedIn, berita, media sosial, data publik.

ANALISIS KHUSUS:
1. Cek apakah website perusahaan AKTIF dan kapan terakhir diupdate
2. Cek keaktifan media sosial (LinkedIn, Instagram, dll)
3. Cek apakah perusahaan masih aktif merekrut
4. Cek berita terbaru tentang perusahaan (PHK, ekspansi, masalah hukum, dll)
5. Cek review karyawan terbaru

Berikan HANYA JSON tanpa backtick:
{{
  "company_name": "{company_name}",
  "industry": "Industri",
  "founded": "Tahun berdiri atau 'Tidak diketahui'",
  "size": "Ukuran perusahaan",
  "headquarters": "Lokasi kantor pusat",
  "website": "URL website resmi atau 'Tidak ditemukan'",
  "description": "Deskripsi 2-3 kalimat",
  "trust_score": 75,
  "trust_level": "HIGH/MEDIUM/LOW",
  "website_status": "Aktif/Tidak Aktif/Tidak Ditemukan",
  "website_last_update": "Kapan terakhir website diupdate (perkiraan)",
  "social_media_active": true,
  "social_media_details": "Detail keaktifan LinkedIn, Instagram, dll",
  "actively_hiring": true,
  "hiring_details": "Detail rekrutmen terbaru",
  "glassdoor_rating": "Rating atau 'N/A'",
  "pros": ["kelebihan1", "kelebihan2", "kelebihan3"],
  "cons": ["kekurangan1", "kekurangan2"],
  "red_flags": ["red flag jika ada"],
  "green_flags": ["green flag jika ada"],
  "salary_reputation": "Kompetitif/Rata-rata/Di bawah rata-rata/Tidak ada data",
  "work_life_balance": "Baik/Cukup/Buruk/Tidak ada data",
  "career_growth": "Baik/Cukup/Terbatas/Tidak ada data",
  "recent_news": ["berita terkini 1", "berita terkini 2"],
  "news_sentiment": "Positif/Netral/Negatif/Tidak ada berita",
  "overall_verdict": "Verdict keseluruhan 2-3 kalimat",
  "recommendation": "RECOMMENDED/PROCEED_WITH_CAUTION/NOT_RECOMMENDED"
}}
"""


def build_cv_prompt(cv_text):
    return f"""
Analisis CV berikut dan ekstrak informasi kunci.
CV: {cv_text}
Berikan HANYA JSON tanpa backtick:
{{
  "name": "Nama",
  "current_role": "Posisi saat ini/terakhir",
  "experience_years": "Estimasi tahun pengalaman",
  "education": "Pendidikan terakhir",
  "top_skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
  "industries": ["industri1", "industri2"],
  "summary": "Ringkasan profil 2-3 kalimat",
  "suggested_roles": ["role1", "role2", "role3"],
  "suggested_keywords": ["keyword1", "keyword2", "keyword3"]
}}
"""


# ═══════════════════════════════════════
# UI RENDERERS
# ═══════════════════════════════════════

def render_job_card(job, idx, show_match=True):
    ml = job.get("match_level", "N/A")
    ms = job.get("match_score", 0)
    mc = {"HIGH": ("match-high", "🟢"), "MEDIUM": ("match-medium", "🟡"), "LOW": ("match-low", "🔴")}.get(ml, ("", "⚪"))
    
    skills = "".join(f'<span class="skill-tag">{s}</span>' for s in job.get("requirements", [])[:6])
    match_html = f'<span class="job-match {mc[0]}">{mc[1]} {ms}% Match</span>' if show_match and ml != "N/A" else ""
    sal = job.get("salary_range", "Tidak dicantumkan")
    src = job.get("source", "N/A")
    rnd = job.get("search_round", "")
    rnd_html = f' &nbsp;|&nbsp; 🔄 Ronde {rnd}' if rnd else ""
    
    st.markdown(f"""
    <div class="job-card">
        <div class="job-title">{job.get("title", "N/A")}</div>
        <div class="job-company">🏢 {job.get("company", "N/A")}</div>
        <div class="job-location">📍 {job.get("location", "N/A")} &nbsp;|&nbsp; 💰 {sal} &nbsp;|&nbsp; 🌐 {src}{rnd_html}</div>
        <div style="margin-top: 0.5rem;">{skills}</div>
        {match_html}
    </div>
    """, unsafe_allow_html=True)


def render_company_review(review):
    ts = review.get("trust_score", 0)
    tl = review.get("trust_level", "N/A")
    rec = review.get("recommendation", "N/A")
    tc = {"HIGH": "trust-high", "MEDIUM": "trust-medium"}.get(tl, "trust-low")
    te = {"HIGH": "✅", "MEDIUM": "⚠️"}.get(tl, "❌")
    ts_color = "#4ade80" if ts >= 80 else "#facc15" if ts >= 50 else "#f87171"
    rec_map = {"RECOMMENDED": "✅ Direkomendasikan", "PROCEED_WITH_CAUTION": "⚠️ Hati-hati", "NOT_RECOMMENDED": "❌ Tidak Direkomendasikan"}
    rec_text = rec_map.get(rec, rec)
    
    pros_html = "".join(f"<li style='color:#4ade80;margin:0.2rem 0;'>{p}</li>" for p in review.get("pros", []))
    cons_html = "".join(f"<li style='color:#f87171;margin:0.2rem 0;'>{c}</li>" for c in review.get("cons", []))
    green_html = "".join(f"<li style='color:#4ade80;margin:0.2rem 0;'>{g}</li>" for g in review.get("green_flags", []))
    red_html = "".join(f"<li style='color:#f87171;margin:0.2rem 0;'>{r}</li>" for r in review.get("red_flags", []))
    news_html = "".join(f"<li style='color:#cbd5e1;margin:0.2rem 0;'>{n}</li>" for n in review.get("recent_news", []))
    
    # Website & social media status
    ws = review.get("website_status", "N/A")
    ws_icon = "🟢" if ws == "Aktif" else "🔴" if ws == "Tidak Aktif" else "⚪"
    sma = review.get("social_media_active", None)
    sma_icon = "🟢" if sma else "🔴" if sma is False else "⚪"
    ah = review.get("actively_hiring", None)
    ah_icon = "🟢" if ah else "🔴" if ah is False else "⚪"
    ns = review.get("news_sentiment", "N/A")
    ns_icon = "🟢" if ns == "Positif" else "🔴" if ns == "Negatif" else "🟡"
    
    st.markdown(f"""
    <div class="review-card">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
            <div>
                <h2 style="color:#f1f5f9;margin:0;font-size:1.5rem;">{review.get("company_name", "N/A")}</h2>
                <p style="color:#64748b;margin:0.25rem 0;">{review.get("industry", "")} · {review.get("size", "")} · {review.get("headquarters", "")}</p>
                <p style="color:#475569;margin:0.15rem 0;font-size:0.85rem;">🌐 {review.get("website", "N/A")}</p>
            </div>
            <div style="text-align:right;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:700;color:{ts_color};">{ts}/100</div>
                <span class="trust-badge {tc}">{te} {tl} TRUST</span>
            </div>
        </div>
        <div class="section-divider"></div>
        <p style="color:#cbd5e1;font-size:0.95rem;">{review.get("description", "")}</p>
        
        <!-- Online Presence Status -->
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.75rem;margin:1rem 0;">
            <div style="background:rgba(15,23,42,0.5);border-radius:10px;padding:0.75rem;text-align:center;">
                <div style="font-size:1.2rem;">{ws_icon}</div>
                <div style="color:#94a3b8;font-size:0.75rem;">Website</div>
                <div style="color:#f1f5f9;font-size:0.8rem;font-weight:600;">{ws}</div>
            </div>
            <div style="background:rgba(15,23,42,0.5);border-radius:10px;padding:0.75rem;text-align:center;">
                <div style="font-size:1.2rem;">{sma_icon}</div>
                <div style="color:#94a3b8;font-size:0.75rem;">Social Media</div>
                <div style="color:#f1f5f9;font-size:0.8rem;font-weight:600;">{"Aktif" if sma else "Tidak Aktif" if sma is False else "N/A"}</div>
            </div>
            <div style="background:rgba(15,23,42,0.5);border-radius:10px;padding:0.75rem;text-align:center;">
                <div style="font-size:1.2rem;">{ah_icon}</div>
                <div style="color:#94a3b8;font-size:0.75rem;">Recruiting</div>
                <div style="color:#f1f5f9;font-size:0.8rem;font-weight:600;">{"Aktif" if ah else "Tidak" if ah is False else "N/A"}</div>
            </div>
            <div style="background:rgba(15,23,42,0.5);border-radius:10px;padding:0.75rem;text-align:center;">
                <div style="font-size:1.2rem;">{ns_icon}</div>
                <div style="color:#94a3b8;font-size:0.75rem;">Berita</div>
                <div style="color:#f1f5f9;font-size:0.8rem;font-weight:600;">{ns}</div>
            </div>
        </div>
        
        <!-- Social Media Detail -->
        <div style="background:rgba(15,23,42,0.3);border-radius:10px;padding:0.75rem;margin-bottom:1rem;">
            <div style="color:#94a3b8;font-size:0.8rem;">📱 Detail Media Sosial & Online</div>
            <div style="color:#cbd5e1;font-size:0.9rem;">{review.get("social_media_details", "N/A")}</div>
            <div style="color:#94a3b8;font-size:0.8rem;margin-top:0.3rem;">📋 Status Rekrutmen</div>
            <div style="color:#cbd5e1;font-size:0.9rem;">{review.get("hiring_details", "N/A")}</div>
        </div>
        
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
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
                <ul style="padding-left:1.2rem;margin:0;">{red_html if red_html else '<li style="color:#64748b;">Tidak ada</li>'}</ul>
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
        <ul style="padding-left:1.2rem;margin:0;">{news_html if news_html else '<li style="color:#64748b;">Tidak ada berita terkini</li>'}</ul>
        <div style="background:rgba(56,189,248,0.06);border-radius:12px;padding:1rem;margin-top:1rem;">
            <div style="color:#38bdf8;font-weight:700;margin-bottom:0.5rem;">📋 Verdict</div>
            <p style="color:#e2e8f0;margin:0 0 0.5rem 0;">{review.get("overall_verdict", "")}</p>
            <div style="font-weight:700;font-size:1.1rem;">{rec_text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════

with st.sidebar:
    st.markdown("### ⚙️ Konfigurasi")
    cloud_key_available = False
    try:
        ck = st.secrets.get("gemini", {}).get("api_key", "")
        if ck and ck != "YOUR_GEMINI_API_KEY_HERE":
            cloud_key_available = True
    except:
        pass
    
    if cloud_key_available:
        st.success("✅ API Key via Cloud Secrets")
        api_key = get_api_key()
    else:
        api_key_input = st.text_input("🔑 Gemini API Key", type="password",
            value=st.session_state.get("api_key_input", ""),
            help="Gratis di aistudio.google.com")
        if api_key_input:
            st.session_state.api_key_input = api_key_input
        api_key = get_api_key()
        if api_key:
            st.success("✅ API Key terhubung")
        else:
            st.warning("⚠️ Masukkan API Key")
            st.markdown('<div class="info-box">Buka <a href="https://aistudio.google.com" target="_blank">aistudio.google.com</a> → Get API Key</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📄 Upload CV")
    cv_file = st.file_uploader("Upload CV (PDF/TXT)", type=["pdf", "txt"])
    cv_manual = st.text_area("Atau paste profil Anda:", value=st.session_state.cv_text, height=120,
        placeholder="5 tahun pengalaman Data Analyst, Python, SQL...")
    
    if cv_file:
        if cv_file.type == "text/plain":
            st.session_state.cv_text = cv_file.read().decode("utf-8")
        elif cv_file.type == "application/pdf":
            try:
                import PyPDF2, io
                reader = PyPDF2.PdfReader(io.BytesIO(cv_file.read()))
                st.session_state.cv_text = "".join(p.extract_text() or "" for p in reader.pages)
            except Exception as e:
                st.error(f"Error: {e}")
    elif cv_manual:
        st.session_state.cv_text = cv_manual
    
    if st.session_state.cv_text and api_key:
        if st.button("🔍 Analisis CV", use_container_width=True):
            with st.spinner("Menganalisis..."):
                r = call_gemini(build_cv_prompt(st.session_state.cv_text), api_key=api_key)
                p = parse_json_response(r)
                if p:
                    st.session_state.cv_analysis = p
                    st.success("✅ CV dianalisis!")
    
    if st.session_state.cv_analysis:
        cv = st.session_state.cv_analysis
        st.markdown("---")
        st.markdown(f"### 👤 {cv.get('name', 'Profil Anda')}")
        st.markdown(f"📌 {cv.get('current_role', 'N/A')}")
        st.markdown(f"⏱️ {cv.get('experience_years', '?')} tahun")
        st.markdown(f"🎓 {cv.get('education', 'N/A')}")
        for s in cv.get("top_skills", []):
            st.markdown(f"` {s} `")


# ═══════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════

# Header
st.markdown("""
<div class="hero-header">
    <h1>🎯 AI Job Hunter Pro</h1>
    <p>Pencarian kumulatif — setiap pencarian menambah koleksi Anda. Cari terus sampai puas!</p>
</div>
""", unsafe_allow_html=True)

# Stats
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="stat-card"><span class="stat-number">{len(st.session_state.jobs_database)}</span><div class="stat-label">Total Lowongan</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat-card"><span class="stat-number">{st.session_state.search_count}</span><div class="stat-label">Ronde Pencarian</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-card"><span class="stat-number">{len(st.session_state.company_reviews)}</span><div class="stat-label">Perusahaan Diulas</div></div>', unsafe_allow_html=True)
with c4:
    hm = sum(1 for j in st.session_state.jobs_database if j.get("match_level") == "HIGH")
    st.markdown(f'<div class="stat-card"><span class="stat-number">{hm}</span><div class="stat-label">High Match</div></div>', unsafe_allow_html=True)


# Tabs
tab_search, tab_db, tab_reviews, tab_help = st.tabs(["🔍 Pencarian", "📂 Database", "🏢 Ulasan Perusahaan", "❓ Panduan"])


# ══════════════════════════════════════
# TAB 1: CUMULATIVE SEARCH
# ══════════════════════════════════════

with tab_search:
    st.markdown("### 🔍 Pencarian Lowongan Kumulatif")
    st.markdown('<div class="info-box">Setiap klik <b>"Cari Lagi"</b> menambah hasil baru ke koleksi Anda. Tidak ada duplikat!</div>', unsafe_allow_html=True)
    
    col_l, col_r = st.columns([2, 1])
    with col_l:
        job_keyword = st.text_input("🎯 Posisi / Kata Kunci", placeholder="Data Analyst, PPIC, Software Engineer")
        cl1, cl2 = st.columns(2)
        with cl1:
            job_location = st.text_input("📍 Lokasi", placeholder="Jakarta, Cikarang, Remote")
        with cl2:
            job_type = st.selectbox("💼 Tipe", ["Semua", "Full-time", "Part-time", "Contract", "Remote", "Internship"])
    with col_r:
        experience_level = st.selectbox("📊 Level", ["Semua", "Fresh Graduate", "Junior (1-3 thn)", "Mid (3-5 thn)", "Senior (5+ thn)", "Manager"])
        additional = st.text_input("🔧 Filter Tambahan", placeholder="Python, remote-friendly")
    
    # Build criteria text
    parts = []
    if job_keyword: parts.append(f"Posisi: {job_keyword}")
    if job_location: parts.append(f"Lokasi: {job_location}")
    if job_type != "Semua": parts.append(f"Tipe: {job_type}")
    if experience_level != "Semua": parts.append(f"Level: {experience_level}")
    if additional: parts.append(f"Filter: {additional}")
    criteria = "\n".join(parts)
    
    # Search buttons
    bc1, bc2, bc3 = st.columns(3)
    with bc1:
        do_search = st.button("🚀 Cari Lowongan", use_container_width=True, type="primary",
                              disabled=not (job_keyword and api_key))
    with bc2:
        do_search_match = st.button("🎯 Cari & Cocokkan CV", use_container_width=True,
                                    disabled=not (job_keyword and api_key and st.session_state.cv_text))
    with bc3:
        do_search_more = st.button("🔄 Cari Lagi (+Tambah)", use_container_width=True,
                                   disabled=not (job_keyword and api_key and st.session_state.search_count > 0))
    
    if not api_key:
        st.info("👈 Masukkan Gemini API Key di sidebar.")
    
    # Execute search
    should_search = do_search or do_search_match or do_search_more
    
    if should_search and job_keyword:
        round_num = st.session_state.search_count + 1
        
        # Get existing companies to exclude
        existing_companies = list(set(j.get("company", "") for j in st.session_state.jobs_database))
        exclude = existing_companies if do_search_more and existing_companies else None
        
        with st.status(f"🔍 Ronde {round_num} — Mencari lowongan baru...", expanded=True) as status:
            st.write(f"🌐 Menghubungi Gemini + Google Search (Ronde {round_num})...")
            
            prompt = build_search_prompt(criteria, exclude_companies=exclude, round_num=round_num)
            raw = call_gemini(prompt, use_search=True, api_key=api_key)
            
            st.write("📊 Memproses hasil...")
            jobs = parse_json_response(raw)
            
            if jobs and isinstance(jobs, list):
                # Tag each job with round number
                existing_ids = {j["id"] for j in st.session_state.jobs_database}
                new_jobs = []
                for job in jobs:
                    job["id"] = gen_job_id(job)
                    job["search_round"] = round_num
                    job["found_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    job["search_query"] = job_keyword
                    if job["id"] not in existing_ids:
                        new_jobs.append(job)
                        existing_ids.add(job["id"])
                
                st.write(f"✅ {len(new_jobs)} lowongan BARU ditemukan! ({len(jobs) - len(new_jobs)} duplikat dilewati)")
                
                # Match with CV if requested
                if do_search_match and st.session_state.cv_text and new_jobs:
                    st.write("🤖 Mencocokkan dengan CV...")
                    mr = call_gemini(build_match_prompt(st.session_state.cv_text, new_jobs), api_key=api_key)
                    matches = parse_json_response(mr)
                    if matches and isinstance(matches, list):
                        for m in matches:
                            idx = m.get("job_index", 0)
                            if 0 <= idx < len(new_jobs):
                                new_jobs[idx].update({
                                    "match_score": m.get("match_score", 0),
                                    "match_level": m.get("match_level", "N/A"),
                                    "matching_skills": m.get("matching_skills", []),
                                    "missing_skills": m.get("missing_skills", []),
                                    "recommendation": m.get("recommendation", ""),
                                    "tips": m.get("tips", ""),
                                })
                        new_jobs.sort(key=lambda x: x.get("match_score", 0), reverse=True)
                        st.write("✅ CV matching selesai!")
                
                # Add to database
                st.session_state.jobs_database.extend(new_jobs)
                st.session_state.search_count = round_num
                st.session_state.latest_results = new_jobs
                
                status.update(label=f"✅ Ronde {round_num} selesai — {len(new_jobs)} baru, total {len(st.session_state.jobs_database)} lowongan!", state="complete")
            else:
                st.session_state.latest_results = []
                status.update(label="⚠️ Tidak ada hasil", state="error")
                if raw.startswith("ERROR:"):
                    st.error(raw)
                else:
                    st.warning("Format error. Coba ubah kata kunci.")
                    with st.expander("🔧 Debug"):
                        st.code(raw[:2000])
    
    # Display cumulative results summary
    if st.session_state.search_count > 0:
        st.markdown("---")
        st.markdown(f"### 📊 Ringkasan {st.session_state.search_count} Ronde Pencarian")
        
        # Show round history
        rounds = {}
        for j in st.session_state.jobs_database:
            r = j.get("search_round", 0)
            rounds[r] = rounds.get(r, 0) + 1
        
        round_cols = st.columns(min(len(rounds), 6))
        for i, (r, count) in enumerate(sorted(rounds.items())):
            with round_cols[i % len(round_cols)]:
                st.markdown(f'<div class="search-round">🔄 Ronde {r}: <b>{count}</b> lowongan</div>', unsafe_allow_html=True)
    
    # Display latest results
    if st.session_state.latest_results:
        st.markdown(f"### 📋 Hasil Terbaru ({len(st.session_state.latest_results)} lowongan baru)")
        
        for i, job in enumerate(st.session_state.latest_results):
            render_job_card(job, i, show_match=True)
            
            with st.expander(f"📝 {job.get('title', '')} @ {job.get('company', '')}"):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f"**Deskripsi:** {job.get('description', 'N/A')}")
                    st.markdown(f"**Tipe:** {job.get('job_type', 'N/A')} | **Tanggal:** {job.get('posted_date', 'N/A')}")
                    if job.get("url") and job["url"] != "#":
                        st.markdown(f"🔗 [Buka Lowongan]({job['url']})")
                    if job.get("recommendation"):
                        st.info(f"💡 {job['recommendation']}")
                    if job.get("tips"):
                        st.success(f"📌 {job['tips']}")
                with c2:
                    if job.get("matching_skills"):
                        st.markdown("**✅ Skills Cocok:**")
                        for s in job["matching_skills"]: st.markdown(f"- {s}")
                    if job.get("missing_skills"):
                        st.markdown("**⚠️ Skills Kurang:**")
                        for s in job["missing_skills"]: st.markdown(f"- {s}")
                
                if st.button(f"🏢 Ulas {job.get('company', '')}", key=f"rv_{i}"):
                    with st.spinner(f"Menganalisis {job.get('company', '')}..."):
                        rr = call_gemini(build_company_prompt(job["company"]), use_search=True, api_key=api_key)
                        rv = parse_json_response(rr)
                        if rv:
                            st.session_state.company_reviews[job["company"]] = rv
                            st.success(f"✅ Ulasan tersimpan! Buka tab Ulasan Perusahaan.")


# ══════════════════════════════════════
# TAB 2: DATABASE
# ══════════════════════════════════════

with tab_db:
    st.markdown(f"### 📂 Database ({len(st.session_state.jobs_database)} lowongan)")
    
    if not st.session_state.jobs_database:
        st.markdown('<div class="info-box">Database kosong. Mulai pencarian di tab Pencarian.</div>', unsafe_allow_html=True)
    else:
        cd1, cd2, cd3 = st.columns([2, 1, 1])
        with cd1:
            db_q = st.text_input("🔍 Filter:", placeholder="Cari judul, perusahaan, lokasi...")
        with cd2:
            db_sort = st.selectbox("Urutkan:", ["Terbaru", "Match ↑", "Match ↓", "Perusahaan A-Z"])
        with cd3:
            db_filter = st.selectbox("Level:", ["Semua", "HIGH", "MEDIUM", "LOW"])
        
        fdb = st.session_state.jobs_database.copy()
        if db_q:
            q = db_q.lower()
            fdb = [j for j in fdb if q in j.get("title","").lower() or q in j.get("company","").lower() or q in j.get("location","").lower()]
        if db_filter != "Semua":
            fdb = [j for j in fdb if j.get("match_level") == db_filter]
        if db_sort == "Match ↑": fdb.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        elif db_sort == "Match ↓": fdb.sort(key=lambda x: x.get("match_score", 0))
        elif db_sort == "Perusahaan A-Z": fdb.sort(key=lambda x: x.get("company", "").lower())
        else: fdb.reverse()
        
        st.markdown(f"Menampilkan **{len(fdb)}** dari **{len(st.session_state.jobs_database)}**")
        
        ec1, ec2 = st.columns(2)
        with ec1:
            if st.button("📤 Export JSON"):
                st.download_button("⬇️ Download", json.dumps(st.session_state.jobs_database, ensure_ascii=False, indent=2),
                    f"jobs_{datetime.now().strftime('%Y%m%d_%H%M')}.json", "application/json")
        with ec2:
            if st.button("🗑️ Hapus Semua", type="secondary"):
                st.session_state.jobs_database = []
                st.session_state.search_count = 0
                st.session_state.latest_results = []
                st.rerun()
        
        for i, job in enumerate(fdb):
            render_job_card(job, i + 2000, show_match=True)
            cc1, cc2, cc3 = st.columns(3)
            with cc1:
                if job.get("url") and job["url"] != "#":
                    st.markdown(f"[🔗 Buka]({job['url']})")
            with cc2:
                co = job.get("company", "")
                if co and st.button(f"🏢 Ulas", key=f"dbr_{i}"):
                    if api_key:
                        with st.spinner(f"Menganalisis {co}..."):
                            rr = call_gemini(build_company_prompt(co), use_search=True, api_key=api_key)
                            rv = parse_json_response(rr)
                            if rv: st.session_state.company_reviews[co] = rv; st.success("✅ Tersimpan!")
            with cc3:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.jobs_database = [j for j in st.session_state.jobs_database if j["id"] != job["id"]]
                    st.rerun()


# ══════════════════════════════════════
# TAB 3: COMPANY REVIEWS (DEEP ANALYSIS)
# ══════════════════════════════════════

with tab_reviews:
    st.markdown("### 🏢 Ulasan & Trust Score Perusahaan")
    st.markdown('<div class="info-box">Analisis mendalam: website, media sosial, berita, review karyawan, dan aktivitas rekrutmen</div>', unsafe_allow_html=True)
    
    cr1, cr2 = st.columns([3, 1])
    with cr1:
        company_input = st.text_input("🔍 Nama perusahaan:", placeholder="Tokopedia, Gojek, Astra, Bank BCA")
    with cr2:
        st.markdown("<br>", unsafe_allow_html=True)
        review_btn = st.button("🔎 Analisis Mendalam", use_container_width=True, type="primary")
    
    if review_btn and company_input and api_key:
        with st.spinner(f"🔍 Riset mendalam {company_input}..."):
            rr = call_gemini(build_company_prompt(company_input), use_search=True, api_key=api_key)
            rv = parse_json_response(rr)
            if rv:
                st.session_state.company_reviews[company_input] = rv
                st.success("✅ Selesai!")
            else:
                st.error("Gagal. Coba lagi.")
                with st.expander("Debug"): st.code(rr[:2000])
    
    if st.session_state.company_reviews:
        st.markdown(f"---")
        for cn, rv in st.session_state.company_reviews.items():
            render_company_review(rv)
    else:
        st.markdown('<div class="info-box">Belum ada ulasan. Ketik nama perusahaan di atas atau klik "Ulas" di tab Pencarian/Database.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════
# TAB 4: HELP
# ══════════════════════════════════════

with tab_help:
    st.markdown("### ❓ Panduan")
    st.markdown("""
    <div class="review-card">
        <div class="review-section-title">🔄 Pencarian Kumulatif — Cara Kerja</div>
        <ol style="color:#cbd5e1;line-height:2;">
            <li><b>Cari Lowongan</b> — pencarian pertama menemukan ~12 lowongan</li>
            <li><b>Cari Lagi (+Tambah)</b> — mencari lowongan BARU dari perusahaan lain</li>
            <li>Setiap ronde otomatis menghindari duplikat perusahaan sebelumnya</li>
            <li>Hasil terus bertambah: 12 → 24 → 36 → 48 → dan seterusnya</li>
            <li>Semua tersimpan di Database — filter, sort, dan export kapan saja</li>
        </ol>
    </div>
    <div class="review-card">
        <div class="review-section-title">🏢 Analisis Perusahaan Mendalam</div>
        <ul style="color:#cbd5e1;line-height:2;">
            <li><b>Website Check</b> — Apakah website perusahaan aktif dan terupdate</li>
            <li><b>Media Sosial</b> — Keaktifan LinkedIn, Instagram, dll</li>
            <li><b>Status Rekrutmen</b> — Apakah masih aktif merekrut</li>
            <li><b>Berita Terkini</b> — PHK, ekspansi, masalah hukum, dll</li>
            <li><b>Review Karyawan</b> — Dari Glassdoor, Jobplanet, Indeed</li>
            <li><b>Trust Score</b> — Skor 0-100 berdasarkan semua data di atas</li>
        </ul>
    </div>
    <div class="review-card">
        <div class="review-section-title">💰 Biaya</div>
        <ul style="color:#cbd5e1;line-height:2;">
            <li><b>Gemini API:</b> Gratis (~500 pencarian/hari)</li>
            <li><b>Tanpa library Google</b> — menggunakan REST API langsung</li>
            <li><b>Streamlit Cloud:</b> Gratis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
