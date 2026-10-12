"""Comparison chart: Hermes vs OpenClaw vs own minimal bot (Telegram video/audio pipeline)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

G, Y, R = "#d4edda", "#fff3cd", "#f8d7da"
cols = ["Criterion", "Hermes Agent", "OpenClaw", "Own minimal bot"]
rows = [
    ["License", "MIT (hermes-agent site)", "MIT for userbot plugin; core: verify", "Your choice"],
    ["Telegram Bot API", "Yes: text, voice, images, files", "Yes; inbound media cap default 5 MB", "Yes: python-telegram-bot"],
    ["Local Bot API (2 GB files)", "Not documented in sources", "Not documented in sources", "Yes: you run tdlib server"],
    ["Local CPU ASR (Shenava)", "Via custom STT backend (unverified)", "Via CLI entry, e.g. local whisper", "Direct: sherpa-onnx in Python"],
    ["Video understanding on CPU", "Custom endpoint possible (unverified)", "Default examples use Gemini/OpenAI APIs", "Direct: ffmpeg frames + local VLM"],
    ["Vendor API by default", "Yes: Nous Portal default", "Yes: OpenAI/Google examples", "None"],
    ["Moving parts", "High: memory, skills, cron, gateway", "High: Node runtime, plugins", "Low: 1 Python process + 1 ffmpeg"],
    ["Fit to 'keep it simple'", "Low", "Low", "High"],
    ["Our effort to build", "Medium (config + glue)", "Medium (config + glue)", "Medium (bot + pipeline)"],
]
# colour: green = good for this goal, yellow = partial/unverified, red = poor fit
_unused = [
]
colors = [
    [Y, Y, Y],
    [G, Y, Y],
    [Y, Y, G],
    [Y, Y, G],
    [Y, Y, G],
    [R, R, G],
    [R, R, G],
    [R, R, G],
    [Y, Y, Y],
]
fig, ax = plt.subplots(figsize=(14, 7.2))
ax.axis("off")
tbl = ax.table(cellText=rows, colLabels=cols, loc="center", cellLoc="left",
               colWidths=[0.22, 0.26, 0.26, 0.26])
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1, 2.1)
for (r, c), cell in tbl.get_celld().items():
    if r == 0:
        cell.set_facecolor("#343a40")
        cell.get_text().set_color("white")
        cell.get_text().set_weight("bold")
    elif c == 0:
        cell.set_facecolor("#f1f3f5")
    else:
        cell.set_facecolor(colors[r - 1][c - 1])
ax.set_title("Telegram video/audio bot: gateway options (green = best fit, yellow = partial/unverified, red = poor fit)",
             fontsize=12, pad=12)
fig.text(0.01, 0.01, "Sources: hermes-agent.nousresearch.com (Telegram docs, MIT), docs.openclaw.ai media-understanding, "
         "open-claw.bot Telegram docs, overpod/openclaw-channel-telegram-userbot (MIT). "
         "Rows marked 'unverified' or 'not documented' were not tested.", fontsize=7.5, color="#495057")
plt.savefig("gateway_comparison.png", dpi=150, bbox_inches="tight")
print("saved gateway_comparison.png")
