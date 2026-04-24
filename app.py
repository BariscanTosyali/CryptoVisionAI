import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import base64

st.set_page_config(
    page_title="CryptoVision AI // Yapı Kredi Yatırım",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
#  LOGO
# ─────────────────────────────────────────
def get_base64(path):
    try:
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

yk_b64      = get_base64('yk_logo.png.webp')
yk_logo_src = f'data:image/webp;base64,{yk_b64}' if yk_b64 else None

# ─────────────────────────────────────────
#  STİL
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0d14;
    color: #e0e6f0;
}

/* Navbar */
.yk-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 40px;
    background: #0c1018;
    border-bottom: 2px solid #1e2a3a;
    margin: -60px -60px 30px -60px;
    position: relative;
    z-index: 999;
}
.yk-nav-links { display: flex; gap: 28px; font-size: 14px; font-weight: 500; color: #c0cfe0; }
.yk-nav-links span { cursor: pointer; }
.yk-btn {
    background: #ff8a00;
    color: white;
    padding: 9px 22px;
    border-radius: 6px;
    font-weight: 700;
    border: none;
    cursor: pointer;
    font-size: 13px;
}

/* Hero */
.hero-title {
    font-size: 100px;
    font-weight: 900;
    background: -webkit-linear-gradient(#00d1ff, #005f73);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin: 10px 0 4px 0;
    letter-spacing: 2px;
    line-height: 1.1;
    text-transform: uppercase;
}
.hero-sub {
    font-size: 18px;
    font-weight: 700;
    color: #00d1ff;
    text-align: center;
    margin-bottom: 36px;
    opacity: 0.8;
    font-family: 'Space Mono', monospace;
    letter-spacing: 5px;
}

/* Sinyal */
.signal-banner {
    border-radius: 12px;
    padding: 20px 32px;
    text-align: center;
    margin-bottom: 20px;
    border: 1.5px solid;
    position: relative;
    overflow: hidden;
}
.signal-banner::before {
    content: '';
    position: absolute;
    inset: 0;
    opacity: 0.06;
    background: radial-gradient(circle at 50% 0%, currentColor, transparent 70%);
}
.signal-value { font-size: 52px; font-weight: 800; letter-spacing: -1px; line-height: 1; }

/* Metrik kart */
.mc {
    background: #0f1520;
    border: 1px solid #1e2a3a;
    border-radius: 10px;
    padding: 15px 18px;
    position: relative;
    overflow: hidden;
    height: 100%;
}
.mc::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #004B9D, #00d1ff);
}
.mc-label { font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: #5a7090; font-family: 'Space Mono', monospace; margin-bottom: 7px; }
.mc-value { font-size: 22px; font-weight: 700; font-family: 'Space Mono', monospace; }
.mc-delta { font-size: 11px; margin-top: 4px; font-family: 'Space Mono', monospace; }

/* Bölüm başlığı */
.st { font-size: 12px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: #5a7090; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
.st::after { content: ''; flex: 1; height: 1px; background: #1e2a3a; }

/* Volatilite badge */
.vbadge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-family: 'Space Mono', monospace; font-size: 11px; font-weight: 700; letter-spacing: 1px; }
.vbadge-h { background: rgba(255,75,75,.12); color: #ff4b4b; border: 1px solid rgba(255,75,75,.35); }
.vbadge-l { background: rgba(0,209,255,.10); color: #00d1ff; border: 1px solid rgba(0,209,255,.3); }

/* Korelasyon bilgi şeridi */
.corr-info {
    background: #0f1520;
    border: 1px solid #1e3a5a;
    border-left: 3px solid #004B9D;
    border-radius: 8px;
    padding: 10px 14px;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: #7090a8;
    margin-top: 8px;
}

/* Footer */
.footer {
    margin-top: 36px;
    padding: 16px 0 4px 0;
    border-top: 1px solid #1e2a3a;
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: #2a3a50;
    font-family: 'Space Mono', monospace;
    line-height: 1.8;
}
.disclaimer {
    font-size: 10px;
    color: #243040;
    line-height: 1.7;
    margin-top: 8px;
    padding: 10px 14px;
    background: #0b0f18;
    border-radius: 6px;
    border-left: 3px solid #003087;
}

section[data-testid="stSidebar"] { background-color: #0c1018; border-right: 1px solid #1a2235; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  NAVBAR
# ─────────────────────────────────────────
logo_html = (
    f'<img src="{yk_logo_src}" height="38">'
    if yk_logo_src
    else '<span style="color:#fff;font-weight:800;font-size:18px;">Yapı<span style="color:#00d1ff;">Kredi</span> Yatırım</span>'
)
st.markdown(f"""
<div class="yk-nav">
    {logo_html}
    <div class="yk-nav-links">
        <span>Hizmetler</span><span>Ürünler</span>
        <span>İşlem Kanalları</span><span>Hakkımızda</span>
    </div>
    <button class="yk-btn">Hesap Aç</button>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  VERİ YÜKLEME
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    comp = pd.read_csv('model_comparison.csv')
    with np.load('ui_plot_data.npz') as raw:
        plots = {k: raw[k] for k in raw.files}
    return comp, plots


@st.cache_data
def compute_corr_matrix(plots):
    coins  = ['BTC', 'ETH', 'SOL', 'BNB', 'ADA']
    series = {c: plots[f'{c}_actuals'] for c in coins if f'{c}_actuals' in plots}
    if len(series) < 2:
        return None
    min_len = min(len(v) for v in series.values())
    df_t    = pd.DataFrame({c: v[-min_len:] for c, v in series.items()})
    return df_t.corr().round(4)


def compute_vol_regime(plots, coin):
    key = f'{coin}_actuals'
    if key not in plots:
        return None, None, None
    vals        = plots[key].astype(float)
    recent_std  = float(np.std(vals[-20:]))
    overall_std = float(np.std(vals))
    regime      = "Yüksek ⚠️" if recent_std > overall_std else "Düşük ✅"
    return recent_std, overall_std, regime

# ─────────────────────────────────────────
#  YARDIMCI FONKSİYONLAR
# ─────────────────────────────────────────
def signal_cfg(sig):
    return {
        "AL":  {"color": "#00FF00", "bg": "#00FF0011", "border": "#00FF00"},
        "SAT": {"color": "#FF4B4B", "bg": "#FF4B4B11", "border": "#FF4B4B"},
        "TUT": {"color": "#FFA500", "bg": "#FFA50011", "border": "#FFA500"},
    }.get(sig, {"color": "#808080", "bg": "#80808011", "border": "#808080"})


def compute_signal(last_pred, acc, risk):
    if acc >= risk:
        if last_pred >  0.0005: return "AL"
        if last_pred < -0.0005: return "SAT"
    return "TUT"


def mc(label, value, delta=None, delta_color="#8090a8"):
    d = f'<div class="mc-delta" style="color:{delta_color}">{delta}</div>' if delta else ""
    return f'<div class="mc"><div class="mc-label">{label}</div><div class="mc-value">{value}</div>{d}</div>'


def plot_layout(h=450):
    return dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10,13,20,1)",
        height=h,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(gridcolor="#1a2235"),
        yaxis=dict(gridcolor="#1a2235", zeroline=True,
                   zerolinecolor="#1e3a5a", zerolinewidth=1.5),
        font=dict(family="Syne, sans-serif"),
    )


# ─────────────────────────────────────────
#  ANA UYGULAMA
# ─────────────────────────────────────────
try:
    df_comp, plots = load_data()

    available = sorted({k.split('_')[0] for k in plots if k.endswith('_actuals')})

    # ── Hero ──────────────────────────────
    st.markdown('<p class="hero-title">CryptoVision AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">BİR YAPIKREDİ ÜRÜNÜ</p>', unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────
    with st.sidebar:
        st.markdown(
            '<div style="font-family:Space Mono;font-size:10px;letter-spacing:3px;'
            'color:#00d1ff;margin-bottom:18px;">CRYPTOVISION AI // v2.1</div>',
            unsafe_allow_html=True)

        selected = st.selectbox("Varlık Seçimi", available)
        st.markdown("---")

        risk_level = st.slider("Risk Eşiği (%)", 50, 95, 65)
        st.caption(f"Güven < %{risk_level} → otomatik TUT")

        max_w  = len(plots.get(f'{selected}_actuals', np.array([])))
        window = st.slider("Görüntüleme Penceresi (dk)", 10, max_w, min(100, max_w))

        st.markdown("---")

        # Volatilite badge
        rv, ov, regime = compute_vol_regime(plots, selected)
        if regime:
            bcls = "vbadge-h" if "Yüksek" in regime else "vbadge-l"
            st.markdown(
                '<div style="font-size:10px;letter-spacing:2px;color:#5a7090;'
                'text-transform:uppercase;margin-bottom:6px;">Volatilite Rejimi</div>'
                f'<span class="vbadge {bcls}">{regime}</span>',
                unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("---")
        show_conf  = st.checkbox("Güven Bandı",       value=True)
        show_eq    = st.checkbox("Kümülatif Getiri",   value=True)
        show_corr  = st.checkbox("Korelasyon Matrisi", value=True)
        show_table = st.checkbox("Tüm Varlık Tablosu", value=True)

        st.markdown("---")
        with st.expander("⚙️ Model Bilgisi"):
            st.markdown("""
            **Mimari:** LSTM (2 katman, 50 unit) + ARIMA(5,1,0)  
            **Girdi:** 60 dakikalık pencere  
            **Eğitim/Test:** %80 / %20  
            **Epoch:** 5 · **Batch:** 128–256 · **Loss:** MAE  
            **Özellikler:** RSI(14), SMA Oranı, Mum Gölgeleri, Volatilite
            """)

    # ── Veri Kesimi ───────────────────────
    actuals = plots[f'{selected}_actuals'][-window:].astype(float)
    preds   = plots[f'{selected}_preds'][-window:].astype(float)
    resid   = actuals - preds

    # CSV'den direkt oku — 5 coin de mevcut
    row       = df_comp[df_comp['Coin'] == selected].iloc[0]
    lstm_acc  = float(row['LSTM_Acc'])
    lstm_cor  = float(row['LSTM_Corr'])
    arima_str = f"{float(row['ARIMA_Pred']):.2f}" if str(row['ARIMA_Pred']) not in ('nan', 'N/A', '') else "—"

    signal  = compute_signal(preds[-1], lstm_acc, risk_level)
    scfg    = signal_cfg(signal)
    dir_acc = float(np.mean(np.sign(actuals) == np.sign(preds)) * 100)

    # ── Sinyal Banner ─────────────────────
    st.markdown(f"""
    <div class="signal-banner"
         style="background:{scfg['bg']};border-color:{scfg['border']};color:{scfg['color']}">
        <div style="font-family:Space Mono;font-size:10px;letter-spacing:3px;opacity:.6;">
            YAPAY ZEKA KARARI
        </div>
        <div class="signal-value">{signal}</div>
        <div style="font-size:12px;opacity:.5;font-family:Space Mono;margin-top:8px;">
            Güven: %{lstm_acc:.1f} &nbsp;·&nbsp; Eşik: %{risk_level} &nbsp;·&nbsp;
            Son ivme: {preds[-1]:+.5f}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Metrik Kartlar ────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(mc("Model Başarısı", f"%{lstm_acc:.2f}",
            delta="↑ Yüksek" if lstm_acc >= 75 else "↓ Orta",
            delta_color="#00e676" if lstm_acc >= 75 else "#ffa726"), unsafe_allow_html=True)
    with c2:
        st.markdown(mc("Korelasyon", f"{lstm_cor:.4f}",
            delta="Güçlü" if lstm_cor >= 0.8 else "Zayıf",
            delta_color="#00e676" if lstm_cor >= 0.8 else "#ffa726"), unsafe_allow_html=True)
    with c3:
        st.markdown(mc("Yön Doğruluğu", f"%{dir_acc:.1f}",
            delta=f"Son {window} dk"), unsafe_allow_html=True)
    with c4:
        st.markdown(mc("ARIMA Tahmini", arima_str,
            delta="Sonraki dk fiyatı"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Ana Grafik ────────────────────────
    st.markdown('<div class="st">📊 Teknik Analiz & İvme Haritası</div>', unsafe_allow_html=True)

    fig = go.Figure()

    if show_conf:
        std = np.std(resid)
        fig.add_trace(go.Scatter(y=preds + std, line=dict(color="rgba(0,209,255,0)"),
                                 showlegend=False, hoverinfo="skip"))
        fig.add_trace(go.Scatter(y=preds - std, fill="tonexty",
                                 fillcolor="rgba(0,209,255,0.05)",
                                 line=dict(color="rgba(0,209,255,0)"),
                                 name="Güven Bandı (±1σ)"))

    fig.add_trace(go.Scatter(y=actuals, name="Gerçek Değişim",
                             line=dict(color="#00d1ff", width=2.5)))
    fig.add_trace(go.Scatter(y=preds, name="LSTM Tahmini",
                             line=dict(color="rgba(255,255,255,0.35)",
                                       width=1.5, dash="dot")))

    buy_idx  = [i for i in range(len(preds)) if preds[i] >  0.0005 and lstm_acc > risk_level]
    sell_idx = [i for i in range(len(preds)) if preds[i] < -0.0005 and lstm_acc > risk_level]

    if buy_idx:
        fig.add_trace(go.Scatter(x=buy_idx, y=[actuals[i] for i in buy_idx],
            mode="markers", name="AL",
            marker=dict(symbol="triangle-up", size=13, color="#00FF00",
                        line=dict(width=1, color="white"))))
    if sell_idx:
        fig.add_trace(go.Scatter(x=sell_idx, y=[actuals[i] for i in sell_idx],
            mode="markers", name="SAT",
            marker=dict(symbol="triangle-down", size=13, color="#FF4B4B",
                        line=dict(width=1, color="white"))))

    lay = plot_layout(450)
    lay["hovermode"] = "x unified"
    lay["legend"]    = dict(orientation="h", y=1.02, yanchor="bottom", x=1, xanchor="right")
    fig.update_layout(**lay)
    st.plotly_chart(fig, use_container_width=True)

    # ── Volatilite Detay ──────────────────
    if rv is not None:
        st.markdown('<div class="st">🌡️ Volatilite Rejimi Detayı</div>', unsafe_allow_html=True)
        is_high  = "Yüksek" in regime
        box_bg   = "rgba(255,75,75,.07)"  if is_high else "rgba(0,209,255,.06)"
        box_bdr  = "rgba(255,75,75,.35)"  if is_high else "rgba(0,209,255,.3)"
        yorum    = ("Piyasa normalin üzerinde hareketli. Pozisyon büyüklüklerinizi küçük tutun."
                    if is_high else
                    "Piyasa sakin seyrediyor. Normal pozisyon boyutları kullanılabilir.")
        va, vb, vc = st.columns([1, 1, 2])
        with va:
            st.markdown(mc("Güncel Volatilite", f"{rv:.6f}"), unsafe_allow_html=True)
        with vb:
            st.markdown(mc("Ortalama Volatilite", f"{ov:.6f}"), unsafe_allow_html=True)
        with vc:
            st.markdown(
                f'<div style="background:{box_bg};border:1px solid {box_bdr};'
                f'border-radius:10px;padding:14px 18px;">'
                f'<div class="mc-label">Rejim Yorumu</div>'
                f'<div style="font-size:15px;font-weight:700;margin-bottom:6px;">{regime}</div>'
                f'<div style="font-size:12px;color:#8090a8;">{yorum}</div>'
                f'</div>', unsafe_allow_html=True)

    # ── Hata Dağılımı + İşlem Günlüğü ────
    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns(2)

    with left:
        st.markdown('<div class="st">📉 Hata (Residual) Dağılımı</div>', unsafe_allow_html=True)
        fig_h = px.histogram(resid, nbins=30,
                             color_discrete_sequence=["#00d1ff"],
                             labels={"value": "Hata Miktarı"}, opacity=.75)
        fig_h.update_layout(**plot_layout(280), showlegend=False)
        st.plotly_chart(fig_h, use_container_width=True)

    with right:
        st.markdown('<div class="st">📋 Son İşlem Günlüğü</div>', unsafe_allow_html=True)
        log_df = pd.DataFrame({
            "Zaman":  [f"−{abs(i)} dk" for i in range(-5, 0)],
            "Tahmin": [f"{preds[i]:+.5f}"   for i in range(-5, 0)],
            "Gerçek": [f"{actuals[i]:+.5f}" for i in range(-5, 0)],
            "Sonuç":  ["✅" if np.sign(preds[i]) == np.sign(actuals[i])
                       else "❌" for i in range(-5, 0)],
        })
        st.dataframe(log_df, use_container_width=True, hide_index=True)

    # ── Kümülatif Getiri ──────────────────
    if show_eq:
        st.markdown('<div class="st">📈 Simüle Kümülatif Getiri</div>', unsafe_allow_html=True)
        cum  = np.cumsum(np.sign(preds) * actuals)
        fret = cum[-1]
        rcol = "#00e676" if fret >= 0 else "#ff4b4b"

        fig_e = go.Figure()
        fig_e.add_hline(y=0, line=dict(color="#1e3a5a", width=1, dash="dot"))
        fig_e.add_trace(go.Scatter(y=cum, fill="tozeroy",
            fillcolor="rgba(0,209,255,.07)",
            line=dict(color="#00d1ff", width=2),
            name="Kümülatif Getiri"))
        lay_e = plot_layout(280)
        lay_e["annotations"] = [dict(
            x=0.98, y=0.92, xref="paper", yref="paper",
            text=f"Dönem Getirisi: <b style='color:{rcol}'>{fret:+.4f}</b>",
            showarrow=False, font=dict(size=13, color="#e0e6f0"),
            align="right", bgcolor="rgba(10,13,20,.6)"
        )]
        fig_e.update_layout(**lay_e)
        st.plotly_chart(fig_e, use_container_width=True)

    # ── Korelasyon Matrisi ────────────────
    if show_corr:
        corr_m = compute_corr_matrix(plots)
        if corr_m is not None:
            st.markdown('<div class="st">🔗 Coin Korelasyon Matrisi</div>', unsafe_allow_html=True)
            fig_c = px.imshow(
                corr_m,
                color_continuous_scale=[[0, "#ff4b4b"], [.5, "#0a0d14"], [1, "#00d1ff"]],
                zmin=-1, zmax=1, text_auto=".2f", aspect="auto"
            )
            fig_c.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                height=340,
                margin=dict(l=10, r=10, t=10, b=10),
                coloraxis_colorbar=dict(title="r", tickvals=[-1, -.5, 0, .5, 1]),
                font=dict(family="Syne, sans-serif"),
            )
            fig_c.update_traces(textfont=dict(size=14, color="white"))
            st.plotly_chart(fig_c, use_container_width=True)

            upper = corr_m.where(
                np.triu(np.ones(corr_m.shape), k=1).astype(bool)
            ).stack().dropna().sort_values()
            if len(upper) > 0:
                lo, hi = upper.index[0], upper.index[-1]
                st.markdown(
                    f'<div class="corr-info">'
                    f'🔴 En düşük: <b style="color:#ff4b4b">{lo[0]} – {lo[1]}</b>'
                    f' ({upper.iloc[0]:.3f}) &nbsp;&nbsp;&nbsp;'
                    f'🔵 En yüksek: <b style="color:#00d1ff">{hi[0]} – {hi[1]}</b>'
                    f' ({upper.iloc[-1]:.3f})'
                    f'</div>',
                    unsafe_allow_html=True)

    # ── Tüm Varlık Tablosu ────────────────
    if show_table:
        st.markdown('<div class="st">🏆 Tüm Varlık Karşılaştırması</div>', unsafe_allow_html=True)
        rows = []
        for coin in available:
            a   = plots[f'{coin}_actuals'].astype(float)
            p   = plots[f'{coin}_preds'].astype(float)
            r   = df_comp[df_comp['Coin'] == coin].iloc[0]
            acc = float(r['LSTM_Acc'])
            cor = float(r['LSTM_Corr'])
            arp = f"{float(r['ARIMA_Pred']):.2f}" if str(r['ARIMA_Pred']) not in ('nan', 'N/A', '') else "—"
            _, _, reg = compute_vol_regime(plots, coin)
            rows.append({
                "Varlık":          coin,
                "Tahmin Başarısı": f"%{acc:.2f}",
                "Korelasyon":      f"{cor:.4f}",
                "ARIMA Tahmini":   arp,
                "Volatilite":      reg or "—",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ── Karar Mekanizması ─────────────────
    st.markdown('<div class="st">🔍 Karar Verme Mekanizması</div>', unsafe_allow_html=True)
    with st.expander("Model hangi verileri işleyerek bu karara vardı?"):
        ia, ib = st.columns(2)
        with ia:
            st.markdown("""
            **Girdi Özellikleri:**
            - **RSI (14):** Aşırı alım/satım tespiti
            - **SMA Oranı:** Fiyat / 15 dk ortalama
            - **Mum Gölgeleri:** Üst/alt gölge oranları
            - **Volatilite:** 15 dk rolling std / fiyat
            """)
        with ib:
            st.markdown(f"""
            **Anlık Analiz — {selected}:**
            - Son tahmin: `{preds[-1]:+.5f}`
            - AL eşiği: `> +0.0005`
            - SAT eşiği: `< -0.0005`
            - Pencere: son `{window}` dakika
            - Yön doğruluğu: `%{dir_acc:.1f}`
            - MAE: `{np.mean(np.abs(resid)):.5f}`
            """)

    # ── Footer ────────────────────────────
    st.markdown("""
    <div class="footer">
        <div>© 2025 Yapı Kredi Yatırım Menkul Değerler A.Ş.<br>CryptoVision AI · AR&GE Demo</div>
        <div style="text-align:right">LSTM + ARIMA · Dakikalık Veri<br>G-Research Crypto Forecasting Dataset</div>
    </div>
    <div class="disclaimer">
        ⚠️ Bu uygulama yalnızca araştırma ve geliştirme amaçlıdır. Gerçek yatırım kararlarında
        kullanılmamalıdır. Yapı Kredi Yatırım Menkul Değerler A.Ş. bu model çıktılarından
        doğabilecek sonuçlardan sorumlu tutulamaz. Geçmiş performans geleceği garanti etmez.
    </div>
    """, unsafe_allow_html=True)

except FileNotFoundError as e:
    st.error(f"⚠️ Gerekli dosya bulunamadı: {e}")
    st.info("Notebook'u çalıştırarak `model_comparison.csv` ve `ui_plot_data.npz` dosyalarını oluşturun.")
except Exception as e:
    st.error(f"Sistem Hatası: {e}")
    raise e
