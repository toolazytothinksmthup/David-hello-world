import html
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("Hello World Motion Lab")
st.caption("A tiny app for experimenting with typography, backgrounds, and continuous motion.")

with st.sidebar:
    st.header("Controls")
    name = st.text_input("Enter your name", value="Hello World", max_chars=100)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact", "Comic Sans MS"],
    )
    font_size = st.slider("Font size (px)", min_value=20, max_value=120, value=48, step=2)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Sky", "Sunset", "Forest", "Lavender", "Ocean"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
    )
    speed = st.slider("Animation speed", min_value=1, max_value=10, value=5, help="Higher values move the effects faster.")
    effect_density = st.slider("Effect density", min_value=10, max_value=100, value=50, step=10)

backgrounds = {
    "Light": ("#ffffff", "#151515"),
    "Dark": ("#10131a", "#ffffff"),
    "Sky": ("linear-gradient(135deg, #b8e7ff, #eaf8ff)", "#12304a"),
    "Sunset": ("linear-gradient(135deg, #ff9966, #ff5e62, #6a5acd)", "#ffffff"),
    "Forest": ("linear-gradient(135deg, #153b2e, #6b9b68)", "#ffffff"),
    "Lavender": ("linear-gradient(135deg, #e8dfff, #c6d7ff)", "#30234a"),
    "Ocean": ("linear-gradient(135deg, #064e73, #20a4b8)", "#ffffff"),
}
bg, text_color = backgrounds[background]
safe_name = html.escape(name or "Hello World")

# Values are inserted into a self-contained HTML document. Escape user-provided text
# and quote the font family to keep the rendered markup well-formed.
safe_font = html.escape(font_family, quote=True)
safe_effect = effect.lower().replace(" ", "-")
animation_duration = round(11 - speed, 2)
count = effect_density

html_doc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  .stage {{
    position: relative; isolation: isolate; width: 100%; height: 620px;
    overflow: hidden; border-radius: 18px; background: {bg}; color: {text_color};
    font-family: "{safe_font}", sans-serif;
  }}
  .effects {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; z-index: 1; }}
  .name-layer {{
    position: absolute; inset: 0; z-index: 2; display: flex; align-items: center;
    justify-content: center; padding: 32px; overflow: hidden; font-size: {font_size}px;
    font-weight: 800; line-height: 1.2; text-shadow: 0 2px 12px rgba(0,0,0,.12);
  }}
  .center-name {{ text-align: center; overflow-wrap: anywhere; }}
  .repeat-name {{ display: flex; flex-direction: column; gap: .22em; text-align: center; white-space: nowrap; }}
  .ticker {{ white-space: nowrap; position: absolute; left: 0; width: max-content; animation: ticker {max(5, 15 - speed):.2f}s linear infinite; }}
  @keyframes ticker {{ from {{ transform: translateX(100vw); }} to {{ transform: translateX(-100%); }} }}
  .particle {{ position: absolute; top: -12%; left: var(--x); opacity: var(--o); font-size: var(--size);
    animation: fall var(--dur) linear var(--delay) infinite; filter: drop-shadow(0 1px 2px rgba(0,0,0,.12)); }}
  @keyframes fall {{ 0% {{ transform: translate3d(0,-8vh,0) rotate(0deg); }} 100% {{ transform: translate3d(var(--drift),115vh,0) rotate(360deg); }} }}
  .wind {{ position: absolute; left: -35%; top: var(--y); width: var(--w); height: 3px; border-radius: 9px;
    background: currentColor; opacity: .22; animation: gust var(--dur) linear var(--delay) infinite; }}
  @keyframes gust {{ from {{ transform: translateX(0) scaleX(.5); }} to {{ transform: translateX(180vw) scaleX(1.5); }} }}
  .tornado {{ position: absolute; left: 50%; top: 50%; width: 20px; height: 20px; border-radius: 50%;
    transform: translate(-50%,-50%); animation: spin 2s linear infinite; }}
  .tornado::before, .tornado::after {{ content: ""; position: absolute; inset: -150px; border: 5px dashed currentColor;
    border-radius: 42% 58% 55% 45%; opacity: .45; animation: spin 3s linear infinite; }}
  .tornado::after {{ inset: -95px; border-width: 8px; animation-direction: reverse; }}
  @keyframes spin {{ to {{ rotate: 360deg; }} }}
  .hint {{ position: absolute; bottom: 14px; left: 18px; z-index: 3; font: 12px/1.4 Arial, sans-serif; opacity: .65; }}
  @media (prefers-reduced-motion: reduce) {{
    .particle, .wind, .ticker, .tornado, .tornado::before, .tornado::after {{ animation-duration: 30s !important; }}
  }}
</style>
</head>
<body>
<div class="stage">
  <div class="effects" id="effects" aria-hidden="true"></div>
  <div class="name-layer" id="nameLayer"></div>
  <div class="hint">Hello World Motion Lab · Live preview</div>
</div>
<script>
(() => {{
  const effect = {safe_effect!r};
  const density = {count};
  const duration = {animation_duration};
  const symbols = {{
    rain: ["💧", "💦"], snow: ["❄️", "❅", "❆"], hail: ["🧊", "●"],
    confetti: ["🎉", "🎊", "🟣", "🟡", "🟢", "🔺"]
  }};
  const effects = document.getElementById("effects");
  const nameLayer = document.getElementById("nameLayer");
  const nameText = {safe_name!r};
  const mode = {name_mode.lower()!r};
  if (mode === "ticker tape") {{
    const ticker = document.createElement("div");
    ticker.className = "ticker";
    ticker.textContent = nameText;
    nameLayer.appendChild(ticker);
  }} else if (mode === "repeated") {{
    const repeated = document.createElement("div");
    repeated.className = "repeat-name";
    for (let i = 0; i < 6; i++) {{
      const line = document.createElement("div");
      line.textContent = nameText;
      repeated.appendChild(line);
    }}
    nameLayer.appendChild(repeated);
  }} else {{
    const centered = document.createElement("div");
    centered.className = "center-name";
    centered.textContent = nameText;
    nameLayer.appendChild(centered);
  }}

  if (effect === "none") return;
  if (effect === "tornado") {{
    const tornado = document.createElement("div");
    tornado.className = "tornado";
    effects.appendChild(tornado);
    return;
  }}
  for (let i = 0; i < density; i++) {{
    const item = document.createElement("span");
    item.style.setProperty("--x", (Math.random() * 100) + "%");
    item.style.setProperty("--o", (0.35 + Math.random() * 0.6).toFixed(2));
    item.style.setProperty("--size", (12 + Math.random() * 18) + "px");
    item.style.setProperty("--dur", (duration * (0.65 + Math.random() * 0.8)) + "s");
    item.style.setProperty("--delay", (-Math.random() * duration) + "s");
    item.style.setProperty("--drift", ((Math.random() - 0.5) * 180) + "px");
    if (effect === "wind-gust") {{
      item.className = "wind";
      item.style.setProperty("--y", (Math.random() * 100) + "%");
      item.style.setProperty("--w", (50 + Math.random() * 180) + "px");
      item.textContent = "";
    }} else {{
      item.className = "particle";
      if (effect === "wind-gust") item.textContent = "💨";
      else {{
        const choices = symbols[effect] || ["💨"];
        item.textContent = choices[Math.floor(Math.random() * choices.length)];
      }}
      if (effect === "rain") item.style.fontSize = (10 + Math.random() * 8) + "px";
      if (effect === "hail") item.style.fontWeight = "bold";
    }}
    effects.appendChild(item);
  }}
}})();
</script>
</body>
</html>"""

components.html(html_doc, height=635, scrolling=False)

st.info("Tip: change the name, font, background, or effect in the sidebar. The preview animates continuously without repeatedly rerunning the Streamlit app.")
