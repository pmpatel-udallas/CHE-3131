import ipywidgets as widgets
from IPython.display import display
import os

DATASETS = ["dye1", "dye2", "dye3"]
LABELS = [
    "HOMO-12", "HOMO-11", "HOMO-10", "HOMO-9", "HOMO-8",
    "HOMO-7",  "HOMO-6",  "HOMO-5",  "HOMO-4", "HOMO-3",
    "HOMO-2",  "HOMO-1",  "HOMO",    "LUMO",   "LUMO+1", "LUMO+2"
]

# ── Widgets ───────────────────────────────────────────────────────────────────
set_selector = widgets.Dropdown(
    options=DATASETS,
    value=DATASETS[0],
    description="Dataset:",
    style={"description_width": "80px"},
    layout=widgets.Layout(width="250px"),
)

# Hidden integer slider drives everything — index into LABELS
idx_slider = widgets.IntSlider(
    min=0, max=len(LABELS) - 1, value=0,
    continuous_update=False,
    layout=widgets.Layout(width="500px"),
)

# Play button: auto-steps through orbitals
play = widgets.Play(
    min=0, max=len(LABELS) - 1, value=0,
    step=1, interval=800,          # ms between steps
    description="Auto",
)
widgets.jslink((play, "value"), (idx_slider, "value"))   # keep in sync

# Prev / Next buttons
btn_prev = widgets.Button(description="◀ Prev", layout=widgets.Layout(width="90px"))
btn_next = widgets.Button(description="Next ▶", layout=widgets.Layout(width="90px"))

def prev_orbital(_):
    idx_slider.value = max(0, idx_slider.value - 1)

def next_orbital(_):
    idx_slider.value = min(len(LABELS) - 1, idx_slider.value + 1)

btn_prev.on_click(prev_orbital)
btn_next.on_click(next_orbital)

img_widget = widgets.Image(format="jpg", width=500)
label_out  = widgets.HTML()

# ── Update ────────────────────────────────────────────────────────────────────
def update(change):
    label = LABELS[idx_slider.value]
    path  = os.path.join("Sample-Data/Orbital_Pictures", set_selector.value, f"{label}.jpg")
    if os.path.exists(path):
        with open(path, "rb") as f:
            img_widget.value = f.read()
        label_out.value = (
            f"<div style='text-align:center; font-size:18px; font-family:monospace; margin-top:6px;'>"
            f"<b>{label}</b> &nbsp;·&nbsp; {set_selector.value}</div>"
        )
    else:
        img_widget.value = b""
        label_out.value  = (
            f"<div style='color:red; text-align:center;'>"
            f"Image not found: <code>{path}</code></div>"
        )

idx_slider.observe(update, names="value")
set_selector.observe(update, names="value")
update(None)

# ── Layout ────────────────────────────────────────────────────────────────────
controls = widgets.HBox([btn_prev, play, idx_slider, btn_next])
display(widgets.VBox([set_selector, controls, img_widget, label_out]))