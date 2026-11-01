"""Global CSS. All colours / fonts live in the :root block, change them there to re-skin the whole app."""

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

:root{
  --font-body:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;
  --font-head:'Plus Jakarta Sans','Inter',system-ui,sans-serif;
  --bg:#FFFFFF; --soft:#F5F7FC; --ink:#0A0F1F; --ink-2:#1B2236; --muted:#5E6A85; --line:#E4E8F2;
  --brand:#3B5BFF; --brand-2:#7C4DFF; --ok:#00A88F; --bad:#E5324F; --warn:#D98A00;
  --radius:20px; --radius-sm:12px; --shadow:0 18px 50px -20px rgba(20,30,80,.25);
}

/* ───────── base ───────── */
html, body, .stApp, [class*="st-"]{font-family:var(--font-body);}
.stApp{background:var(--bg); color:var(--ink);}
h1,h2,h3,h4,h5{font-family:var(--font-head)!important; letter-spacing:-.025em; color:var(--ink);}
p, li{color:var(--ink-2);}
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stSidebar"],
[data-testid="collapsedControl"], [data-testid="stSidebarCollapsedControl"], [data-testid="stStatusWidget"]{display:none!important;}
header[data-testid="stHeader"]{background:transparent; height:0;}
.block-container{max-width:1240px; padding:0 28px 0 28px!important;}
div[data-testid="stVerticalBlock"]{gap:0;}
.stMarkdown p{margin-bottom:0;}

/* ───────── navbar ───────── */
.st-key-navbar{position:sticky; top:0; z-index:1000; background:rgba(255,255,255,.86);
  backdrop-filter:saturate(180%) blur(14px); -webkit-backdrop-filter:saturate(180%) blur(14px);
  border-bottom:1px solid var(--line); padding:12px 28px; margin:0 -28px;}
.st-key-navbar [data-testid="stHorizontalBlock"]{align-items:center; gap:4px;}
.gz-logo{display:flex; align-items:center; gap:10px; font-family:var(--font-head); font-weight:800;
  font-size:19px; letter-spacing:.02em; color:var(--ink);}
.gz-logo .mark{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;font-size:18px;
  background:linear-gradient(135deg,var(--brand),var(--brand-2)); box-shadow:0 8px 20px -8px var(--brand);}
.gz-logo small{font-weight:600;color:var(--muted);letter-spacing:.14em;font-size:11px;margin-left:2px}
.st-key-navbar .stButton>button{border:none!important; background:transparent!important; box-shadow:none!important;
  font-family:var(--font-body); font-weight:600; font-size:12.5px; letter-spacing:.09em; text-transform:uppercase;
  color:var(--ink-2)!important; padding:8px 10px; border-radius:999px; min-height:0; width:100%;}
.st-key-navbar .stButton>button:hover{background:var(--soft)!important; color:var(--brand)!important;}
.st-key-navbar .stButton>button p{font-size:12.5px; font-weight:600; letter-spacing:.09em; text-transform:uppercase; color:inherit!important;}
.st-key-nav_signup button, .st-key-nav_logout button{background:var(--ink)!important; color:#fff!important; padding:9px 18px!important;}
.st-key-nav_signup button p, .st-key-nav_logout button p{color:#fff!important;}
.st-key-nav_signup button:hover, .st-key-nav_logout button:hover{background:var(--brand)!important; color:#fff!important;}

/* ───────── buttons (global) ───────── */
.stButton>button, .stDownloadButton>button, .stFormSubmitButton>button, .stLinkButton>a{
  border-radius:999px!important; font-weight:600; padding:.65rem 1.4rem; transition:all .18s ease;
  border:1.5px solid var(--ink); font-family:var(--font-body);}
button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"]{
  background:var(--ink)!important; color:#fff!important; border:1.5px solid var(--ink)!important;}
button[data-testid="stBaseButton-primary"] p, button[data-testid="stBaseButton-primaryFormSubmit"] p{color:#fff!important;}
button[data-testid="stBaseButton-primary"]:hover, button[data-testid="stBaseButton-primaryFormSubmit"]:hover{
  background:var(--brand)!important; border-color:var(--brand)!important; transform:translateY(-1px);
  box-shadow:0 12px 26px -12px var(--brand);}
button[data-testid="stBaseButton-secondary"], button[data-testid="stBaseButton-secondaryFormSubmit"]{
  background:#fff!important; color:var(--ink)!important;}
button[data-testid="stBaseButton-secondary"]:hover{border-color:var(--brand)!important; color:var(--brand)!important;}
button:disabled{opacity:.45!important; cursor:not-allowed!important;}

/* ───────── inputs ───────── */
.stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"]>div{
  border-radius:var(--radius-sm)!important; border:1.5px solid var(--line)!important; background:#fff!important;
  padding:.7rem .9rem; font-size:15px;}
.stTextInput input:focus{border-color:var(--brand)!important; box-shadow:0 0 0 4px rgba(59,91,255,.12)!important;}
.stTextInput label p, .stSelectbox label p, .stFileUploader label p{font-weight:600; font-size:13px; color:var(--ink-2);}
[data-testid="stFileUploaderDropzone"]{border:2px dashed #C7CFE6!important; border-radius:var(--radius)!important;
  background:var(--soft)!important; padding:2rem 1rem;}
[data-testid="stFileUploaderDropzone"]:hover{border-color:var(--brand)!important; background:#EEF1FF!important;}
.stTabs [data-baseweb="tab-list"]{gap:6px; border-bottom:1px solid var(--line);}
.stTabs [data-baseweb="tab"]{font-weight:600; padding:10px 16px; border-radius:10px 10px 0 0;}
.stTabs [aria-selected="true"]{color:var(--brand)!important;}
.stTabs [data-baseweb="tab-highlight"]{background:var(--brand)!important;}
[data-testid="stExpander"]{border:1px solid var(--line)!important; border-radius:16px!important; background:#fff; margin-bottom:12px;}
[data-testid="stExpander"] summary{padding:18px 22px; font-weight:600; font-family:var(--font-head); font-size:17px;}
[data-testid="stExpander"] details>div{padding:0 22px 18px 22px;}
[data-testid="stDataFrame"]{border:1px solid var(--line); border-radius:14px; overflow:hidden;}
[data-testid="stImage"] img{border-radius:16px; border:1px solid var(--line);}
[data-testid="stAlert"]{border-radius:14px;}

/* ───────── hero ───────── */
.st-key-hero{position:relative; padding:72px 0 30px 0; overflow:hidden;}
.st-key-hero::before{content:""; position:absolute; inset:0 -50vw; z-index:0; pointer-events:none;
  background-image:linear-gradient(to right,rgba(59,91,255,.07) 1px,transparent 1px),
                   linear-gradient(to bottom,rgba(59,91,255,.07) 1px,transparent 1px);
  background-size:56px 56px;
  -webkit-mask-image:radial-gradient(ellipse 70% 70% at 50% 40%,#000 30%,transparent 100%);
          mask-image:radial-gradient(ellipse 70% 70% at 50% 40%,#000 30%,transparent 100%);}
.st-key-hero>*{position:relative; z-index:1;}
.gz-badge{display:inline-flex; align-items:center; gap:8px; padding:7px 14px; border-radius:999px; background:#fff;
  border:1px solid var(--line); font-size:12px; font-weight:700; letter-spacing:.1em; color:var(--ink-2);
  box-shadow:0 6px 18px -10px rgba(20,30,80,.3); text-transform:uppercase;}
.gz-badge i{width:8px;height:8px;border-radius:50%;background:var(--ok);box-shadow:0 0 0 4px rgba(0,168,143,.18);}
.gz-h1{font-family:var(--font-head); font-weight:800; font-size:clamp(38px,5.4vw,68px); line-height:1.02;
  letter-spacing:-.04em; margin:22px 0 20px 0; color:var(--ink);}
.gz-h1 em{font-style:normal; background:linear-gradient(100deg,var(--brand),var(--brand-2)); -webkit-background-clip:text;
  background-clip:text; color:transparent;}
.gz-lead{font-size:18px; line-height:1.65; color:var(--muted); max-width:560px; margin-bottom:26px;}
.gz-stats{display:flex; gap:34px; margin-top:34px; flex-wrap:wrap;}
.gz-stats div b{display:block; font-family:var(--font-head); font-size:32px; letter-spacing:-.03em; color:var(--ink);}
.gz-stats div span{font-size:12px; letter-spacing:.1em; text-transform:uppercase; color:var(--muted); font-weight:600;}
.gz-illus{position:relative; display:grid; place-items:center; min-height:420px;}
.gz-illus img{width:100%; max-width:470px; filter:drop-shadow(0 40px 40px rgba(59,91,255,.18)); animation:float 6s ease-in-out infinite;}
.gz-chip{position:absolute; background:#fff; border:1px solid var(--line); border-radius:14px; padding:10px 14px;
  font-size:13px; font-weight:600; box-shadow:var(--shadow); display:flex; gap:8px; align-items:center;}
.gz-chip.a{top:46px; right:6px; animation:float 5s ease-in-out infinite .4s;}
.gz-chip.b{bottom:70px; left:0; animation:float 5.5s ease-in-out infinite .9s;}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}

/* ───────── marquee ───────── */
.gz-marquee-wrap{padding:34px 0 10px 0; text-align:center;}
.gz-marquee-wrap p{font-size:13px; letter-spacing:.14em; text-transform:uppercase; color:var(--muted); font-weight:600; margin-bottom:18px;}
.gz-marquee{overflow:hidden; -webkit-mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent);
  mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent);}
.gz-track{display:flex; gap:14px; width:max-content; animation:scroll 32s linear infinite;}
.gz-pill{padding:12px 22px; border:1px solid var(--line); border-radius:999px; font-weight:700; color:var(--ink-2);
  font-family:var(--font-head); background:#fff; white-space:nowrap;}
@keyframes scroll{to{transform:translateX(-50%)}}

/* ───────── sections ───────── */
.gz-section{padding:92px 0 10px 0;}
.gz-eyebrow{font-size:12.5px; font-weight:700; letter-spacing:.18em; text-transform:uppercase; color:var(--brand); margin-bottom:14px;}
.gz-h2{font-family:var(--font-head); font-weight:800; font-size:clamp(30px,3.6vw,46px); line-height:1.08; letter-spacing:-.035em;
  margin:0 0 18px 0; max-width:860px; color:var(--ink);}
.gz-p{font-size:17px; line-height:1.7; color:var(--muted); max-width:760px; margin-bottom:14px;}
.gz-split{display:grid; grid-template-columns:1.1fr .9fr; gap:56px; align-items:center;}
.gz-flow{background:var(--soft); border:1px solid var(--line); border-radius:28px; padding:34px;}
.gz-flow .row{display:flex; align-items:center; gap:14px; padding:14px 16px; background:#fff; border:1px solid var(--line);
  border-radius:14px; font-weight:600; margin-bottom:12px;}
.gz-flow .row:last-child{margin-bottom:0}
.gz-flow .row span{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:#EEF1FF;font-size:16px;}
.gz-flow .row small{margin-left:auto; color:var(--muted); font-weight:500; font-size:12.5px;}
.gz-grid4{display:grid; grid-template-columns:repeat(4,1fr); gap:18px; margin-top:34px;}
.gz-grid3{display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-top:34px;}
.gz-card{background:#fff; border:1px solid var(--line); border-radius:var(--radius); padding:28px; transition:all .2s ease; height:100%;}
.gz-card:hover{transform:translateY(-4px); box-shadow:var(--shadow); border-color:#CBD3F5;}
.gz-num{font-family:var(--font-head); font-weight:800; font-size:14px; color:var(--brand); letter-spacing:.1em; margin-bottom:46px; display:flex; justify-content:space-between;}
.gz-card h3{font-size:20px; line-height:1.25; margin:0 0 12px 0; font-weight:700;}
.gz-card p{font-size:15px; line-height:1.65; color:var(--muted); margin:0;}
.gz-step .big{font-family:var(--font-head); font-weight:800; font-size:64px; letter-spacing:-.05em; line-height:1;
  background:linear-gradient(180deg,var(--brand),rgba(124,77,255,.25)); -webkit-background-clip:text; background-clip:text; color:transparent; margin-bottom:22px;}
.gz-step h3{font-size:15px; letter-spacing:.16em; margin:0 0 10px 0; font-weight:800;}
.gz-step p{font-size:13px; letter-spacing:.04em; line-height:1.7; text-transform:uppercase; font-weight:500; color:var(--muted);}

/* dark band */
.gz-dark{margin-top:96px; border-radius:32px; padding:68px 56px; color:#fff; position:relative; overflow:hidden;
  background:radial-gradient(900px 400px at 85% -10%,rgba(124,77,255,.55),transparent 60%),
             radial-gradient(700px 400px at 0% 110%,rgba(59,91,255,.55),transparent 60%),#0A0F1F;}
.gz-dark::after{content:""; position:absolute; inset:0; pointer-events:none;
  background-image:linear-gradient(to right,rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(to bottom,rgba(255,255,255,.05) 1px,transparent 1px);
  background-size:48px 48px;}
.gz-dark>*{position:relative; z-index:1;}
.gz-dark .gz-eyebrow{color:#9DB0FF;}
.gz-dark .gz-h2{color:#fff; text-transform:uppercase; font-size:clamp(28px,3.4vw,44px);}
.gz-dark .gz-p{color:#B9C2DE;}

/* numbered list */
.gz-list{margin-top:30px; border-top:1px solid var(--line);}
.gz-li{display:grid; grid-template-columns:70px 1fr 1.4fr; gap:20px; align-items:center; padding:26px 8px; border-bottom:1px solid var(--line); transition:all .2s;}
.gz-li:hover{background:var(--soft); padding-left:20px;}
.gz-li .n{font-family:var(--font-head); font-weight:800; color:var(--brand); letter-spacing:.08em;}
.gz-li .t{font-family:var(--font-head); font-weight:700; font-size:21px; letter-spacing:-.02em;}
.gz-li .d{color:var(--muted); font-size:15px;}

/* case cards */
.gz-case{background:#fff; border:1px solid var(--line); border-radius:24px; padding:30px; height:100%; display:flex; flex-direction:column;}
.gz-tag{display:inline-block; padding:5px 12px; border-radius:999px; font-size:11px; font-weight:700; letter-spacing:.1em; text-transform:uppercase; background:#EEF1FF; color:var(--brand); align-self:flex-start; margin-bottom:18px;}
.gz-case h3{font-size:22px; margin:0 0 16px 0; font-weight:700;}
.gz-case h5{font-size:11.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--muted); margin:14px 0 6px 0; font-family:var(--font-body)!important; font-weight:700;}
.gz-case p{font-size:14.5px; line-height:1.6; color:var(--ink-2); margin:0;}
.gz-metric{margin-top:auto; padding-top:22px;}
.gz-metric div{border-top:1px dashed var(--line); padding-top:16px;}
.gz-metric small{display:block; color:var(--muted); font-size:12px; font-weight:600; letter-spacing:.06em; text-transform:uppercase;}
.gz-metric b{font-family:var(--font-head); font-size:20px; letter-spacing:-.02em;}
.gz-metric b i{font-style:normal; color:var(--brand); margin:0 8px;}

/* page header */
.gz-page{padding:64px 0 26px 0; position:relative;}
.gz-page .gz-h2{font-size:clamp(32px,4vw,52px); margin-bottom:12px;}

/* result card */
.gz-result{border-radius:24px; padding:30px; border:1.5px solid var(--line); background:#fff; box-shadow:var(--shadow);}
.gz-result.bad{border-color:#F6B9C4; background:linear-gradient(180deg,#FFF5F7,#fff);}
.gz-result.ok{border-color:#9DE2D4; background:linear-gradient(180deg,#F0FCF9,#fff);}
.gz-result.warn{border-color:#F2D79A; background:linear-gradient(180deg,#FFFAEE,#fff);}
.gz-result .lbl{font-size:12px; letter-spacing:.16em; text-transform:uppercase; font-weight:700; color:var(--muted);}
.gz-result .verdict{font-family:var(--font-head); font-weight:800; font-size:40px; letter-spacing:-.04em; margin:6px 0 4px 0;}
.gz-result.bad .verdict{color:var(--bad)} .gz-result.ok .verdict{color:var(--ok)} .gz-result.warn .verdict{color:var(--warn)}
.gz-bar{height:12px; background:#E9ECF5; border-radius:99px; overflow:hidden; margin:8px 0 18px 0;}
.gz-bar>div{height:100%; border-radius:99px;}
.gz-bar.f>div{background:linear-gradient(90deg,#FF7A90,var(--bad));}
.gz-bar.n>div{background:linear-gradient(90deg,#5FD9C3,var(--ok));}
.gz-prob{display:flex; justify-content:space-between; font-size:14px; font-weight:600;}
.gz-note{font-size:13px; line-height:1.6; color:var(--muted); border-top:1px dashed var(--line); padding-top:14px; margin-top:6px;}

/* kpi */
.gz-kpis{display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin:8px 0 24px 0;}
.gz-kpi{background:#fff; border:1px solid var(--line); border-radius:18px; padding:22px;}
.gz-kpi small{display:block; font-size:11.5px; letter-spacing:.12em; text-transform:uppercase; font-weight:700; color:var(--muted);}
.gz-kpi b{display:block; font-family:var(--font-head); font-size:34px; letter-spacing:-.04em; margin-top:8px; color:var(--ink);}
.gz-kpi span{font-size:12.5px; color:var(--muted);}

/* auth */
.gz-auth-side{border-radius:28px; padding:48px 40px; min-height:560px; color:#fff; position:relative; overflow:hidden;
  background:radial-gradient(500px 300px at 90% 0%,rgba(124,77,255,.6),transparent 60%),
             radial-gradient(500px 300px at 0% 100%,rgba(59,91,255,.6),transparent 60%),#0A0F1F;}
.gz-auth-side h2{color:#fff; font-size:36px; line-height:1.1; margin:18px 0 14px 0; font-weight:800;}
.gz-auth-side p{color:#B9C2DE; line-height:1.7; font-size:15px;}
.gz-auth-side ul{list-style:none; padding:0; margin:26px 0 0 0;}
.gz-auth-side li{color:#E7EBFF; padding:9px 0; font-size:14.5px; display:flex; gap:10px;}
.gz-auth-side li::before{content:"✓"; color:#6FE3CC; font-weight:800;}

/* footer */
.gz-footer{margin-top:110px; padding:56px 0 30px 0; border-top:1px solid var(--line);}
.gz-footer-grid{display:grid; grid-template-columns:1.6fr 1fr 1fr 1fr; gap:36px;}
.gz-footer h4{font-size:13px; letter-spacing:.14em; text-transform:uppercase; margin:0 0 14px 0; color:var(--ink);}
.gz-footer p, .gz-footer li, .gz-footer a{font-size:14.5px; color:var(--muted); line-height:1.9; text-decoration:none; list-style:none;}
.gz-footer ul{padding:0; margin:0;}
.gz-footer a:hover{color:var(--brand);}
.gz-copy{margin-top:36px; padding-top:20px; border-top:1px solid var(--line); font-size:13px; color:var(--muted); display:flex; justify-content:space-between; flex-wrap:wrap; gap:10px;}
.gz-disclaimer{background:#FFFAEE; border:1px solid #F2D79A; border-radius:14px; padding:14px 18px; font-size:13.5px; color:#6B4B00; line-height:1.6;}

@media (max-width:900px){
  .gz-split,.gz-footer-grid{grid-template-columns:1fr;}
  .gz-grid4,.gz-grid3,.gz-kpis{grid-template-columns:1fr 1fr;}
  .gz-li{grid-template-columns:44px 1fr;} .gz-li .d{grid-column:1 / -1;}
  .gz-dark{padding:44px 26px;}
}
@media (max-width:560px){ .gz-grid4,.gz-grid3,.gz-kpis{grid-template-columns:1fr;} }
"""
