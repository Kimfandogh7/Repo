"""One-off patch: add native-chart support to finale_build.py (idempotent)."""
p = "/home/user/Repo/edu-agent/tools/deck/finale_build.py"
s = open(p, encoding="utf-8").read()
if "replace_bars_with_native_chart" in s:
    print("already patched")
    raise SystemExit(0)

s = s.replace(
    "import copy\nimport os\nimport sys\n",
    "import copy\nimport os\nimport sys\n\n"
    "from pptx.chart.data import CategoryChartData\n"
    "from pptx.dml.color import RGBColor\n"
    "from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION\n"
    "from pptx.util import Pt\n", 1)

helpers = '''def drop_unused_image_rels(slide, removed_rids):
    """Remove relationships to photos taken off the stage groups (no orphan media)."""
    xml = slide._element.xml
    for rid in removed_rids:
        if f'r:embed="{rid}"' not in xml:
            slide.part.drop_rel(rid)


def replace_bars_with_native_chart(slide):
    """Slide 2: drawn bars become a native, editable PowerPoint bar chart.

    The caption text boxes inside the old !!stage group survive as top-level shapes.
    The chart takes the !!stage name so the morph anchor on this slide is kept.
    """
    grp = next(sh for sh in slide.shapes if sh.name == "!!stage" and sh.shape_type == 6)
    captions = []
    for child in grp.shapes:
        if child.has_text_frame and ("won more" in child.text_frame.text
                                     or "15 of 18" in child.text_frame.text):
            captions.append(copy.deepcopy(child._element))
    grp._element.getparent().remove(grp._element)

    cd = CategoryChartData()
    cd.categories = ["Ferrari", "BAR Honda", "Renault", "Williams"]
    cd.add_series("Wins", (15, 1, 1, 1))
    gf = slide.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, 80 * PX, 775 * PX,
                                880 * PX, 700 * PX, cd)
    gf.name = "!!stage"
    ch = gf.chart
    ch.has_legend = False
    ch.font.name = "Arial"
    ch.font.color.rgb = RGBColor(0x1A, 0x0E, 0x0B)
    plot = ch.plots[0]
    plot.gap_width = 55
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.font.size = Pt(30)
    dl.font.bold = True
    dl.number_format = "0"
    dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    ser = plot.series[0]
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = RGBColor(0xE0, 0x18, 0x06)
    cat = ch.category_axis
    cat.reverse_order = True
    cat.tick_labels.font.size = Pt(28)
    cat.has_major_gridlines = False
    cat.format.line.fill.background()
    val = ch.value_axis
    val.minimum_scale = 0
    val.maximum_scale = 17
    val.has_major_gridlines = False
    val.visible = False
    for el in captions:
        slide.shapes._spTree.append(el)
    return gf


def main():'''
s = s.replace("def main():", helpers, 1)

old_strip = '''        # 1) drop the old photo layers from the stage groups on slides 1 and 3
        for sh in list(slide.shapes):
            if sh.name == "!!stage" and sh.shape_type == 6:
                for child in list(sh.shapes):
                    if child.shape_type == 13:  # PICTURE
                        child._element.getparent().remove(child._element)'''
new_strip = '''        # 1) drop the old photo layers from the stage groups on slides 1 and 3
        removed = []
        for sh in list(slide.shapes):
            if sh.name == "!!stage" and sh.shape_type == 6:
                for child in list(sh.shapes):
                    if child.shape_type == 13:  # PICTURE
                        removed.append(child._element.blipFill.blip.rEmbed)
                        child._element.getparent().remove(child._element)
        drop_unused_image_rels(slide, removed)
        # 1b) slide 2: drawn bars -> native chart
        if idx == 2:
            replace_bars_with_native_chart(slide)'''
assert old_strip in s, "strip block not found"
s = s.replace(old_strip, new_strip, 1)
open(p, "w", encoding="utf-8").write(s)
print("patched")
