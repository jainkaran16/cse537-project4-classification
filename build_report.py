"""Generate the CSE 537 Project 4 report in the established course style."""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Table, TableStyle,
)

OUT = "/Users/karan/Desktop/SBU/AI/Project_4/CSE537_Project4_Report.pdf"
NAVY = colors.HexColor("#173B63")
TEXT = colors.HexColor("#172433")
MUTED = colors.HexColor("#536B82")
LINE = colors.HexColor("#B8C9D8")
ALT = colors.HexColor("#EAF1F6")
CODE_BG = colors.HexColor("#F2F5F7")


def page_chrome(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.55)
    canvas.line(0.65 * inch, 10.5 * inch, 7.85 * inch, 10.5 * inch)
    canvas.line(0.65 * inch, 0.48 * inch, 7.85 * inch, 0.48 * inch)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(0.65 * inch, 10.65 * inch, "CSE 537 - Artificial Intelligence")
    canvas.drawRightString(7.85 * inch, 10.65 * inch, "Project 04: Classification")
    canvas.drawString(0.65 * inch, 0.30 * inch, "Implementation, validation and analysis")
    canvas.drawRightString(7.85 * inch, 0.30 * inch, "Page %d" % doc.page)
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle("TitleX", parent=styles["Title"], fontName="Helvetica",
    fontSize=23, leading=27, textColor=NAVY, alignment=0, spaceBefore=4, spaceAfter=5))
styles.add(ParagraphStyle("Subtitle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=11, leading=14, textColor=MUTED, spaceAfter=10))
styles.add(ParagraphStyle("H1X", parent=styles["Heading1"], fontName="Helvetica",
    fontSize=12.5, leading=15, textColor=NAVY, spaceBefore=9, spaceAfter=5,
    keepWithNext=True))
styles.add(ParagraphStyle("BodyX", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.25, leading=12.2, textColor=TEXT, spaceAfter=5))
styles.add(ParagraphStyle("SmallX", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=7.8, leading=10, textColor=MUTED, spaceAfter=4))
styles.add(ParagraphStyle("CodeX", parent=styles["Code"], fontName="Courier",
    fontSize=7.7, leading=10, textColor=TEXT, backColor=CODE_BG,
    borderPadding=5, leftIndent=8, rightIndent=8, spaceAfter=5))


def p(text, style="BodyX"):
    return Paragraph(text, styles[style])


def result_table(headers, rows, widths):
    data = [[p(h, "SmallX") for h in headers]]
    data.extend([[p(str(cell), "BodyX") for cell in row] for row in rows])
    result = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    result.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ALT]),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return result


doc = BaseDocTemplate(OUT, pagesize=letter, leftMargin=0.74 * inch,
    rightMargin=0.74 * inch, topMargin=0.78 * inch, bottomMargin=0.62 * inch,
    title="CSE 537 Project 4: Classification",
    author="Karan Jain and Maitreya Vaghulade")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="main")
doc.addPageTemplates([PageTemplate(id="report", frames=[frame], onPage=page_chrome)])

story = [
    p("Project 04: Classification", "TitleX"),
    p("Decision trees, Naive Bayes, odds ratios and enhanced digit features", "Subtitle"),
    p("Karan Jain - SBU ID: 117420953<br/>Maitreya Vaghulade - SBU ID: 117437999"),
    p("CSE 537 - Artificial Intelligence | November 16, 2026", "SmallX"),
    p("1. Implementation and testing", "H1X"),
    p("We completed the four designated files: <font name='Courier'>id3.py</font>, "
      "<font name='Courier'>naiveBayes.py</font>, <font name='Courier'>dataClassifier.py</font> "
      "and <font name='Courier'>answers.py</font>. Public APIs and all other starter "
      "files remain unchanged. The final ZIP was extracted into a fresh directory; "
      "the edited files compile and every command reported below was rerun from that package."),
    p("Independent tests cover separable Boolean data, XOR, majority ties, pruning, "
      "Laplace probability calculations, smallest-k tie selection, odds ranking and "
      "binary enhanced features. The final model reaches the handout's 84% test threshold."),
    p("2. Question 1: ID3 decision tree", "H1X"),
    p("The learner chooses the remaining binary feature with maximum information gain, "
      "using base-2 entropy and a deterministic majority-label tie break. Pure nodes and "
      "nodes without remaining features become leaves. Zero-gain splits remain available "
      "because a later split can still solve parity-like data such as XOR."),
    p("Reduced-error pruning proceeds bottom-up. For validation examples reaching a node, "
      "its subtree is replaced by the node's majority-label leaf whenever the leaf is at "
      "least as accurate. Test labels are never used for pruning."),
    result_table(["Configuration", "Validation", "Test", "Nodes", "Leaves"], [
        ["ID3", "52%", "44%", "45", "23"],
        ["ID3 with pruning", "54%", "46%", "31", "16"],
    ], [2.45*inch, .85*inch, .75*inch, .75*inch, .75*inch]),
    p("Table 1. Pruning removes 14 of 45 nodes (31%) and improves validation and test "
      "accuracy by two percentage points.", "SmallX"),
    p("python3 dataClassifier.py -c id3 -d digits<br/>"
      "python3 dataClassifier.py -c id3 -d digits -p", "CodeX"),
    p("3. Question 2: Naive Bayes", "H1X"),
    p("Class priors are empirical frequencies and are not smoothed. For each binary "
      "feature f and label y, P(f=1|y) = (count(f=1,y)+k)/(count(y)+2k). Counts are "
      "collected once and reused for every candidate k. Classification sums log P(y) "
      "and the log conditional probability of every present or absent feature."),
    result_table(["Configuration", "Training", "Validation", "Test", "Selected k"], [
        ["Fixed-k Naive Bayes", "100", "69%", "55%", "2"],
        ["Autotuned Naive Bayes", "100", "74%", "65%", "0.1"],
        ["Basic features", "1,000", "82%", "78%", "0.001"],
        ["Enhanced features", "1,000", "85%", "84%", "0.001"],
    ], [2.15*inch, .75*inch, .85*inch, .70*inch, .90*inch]),
    p("Table 2. Autotuning gains ten test points over k=2 with 100 examples. More "
      "training data supports a smaller smoothing value.", "SmallX"),
    p("The 74% validation and 65% test results match the handout's reference values. "
      "Naive Bayes assumes conditional independence even though neighboring pixels and "
      "shape features are correlated; many weak image cues still combine effectively."),
    p("python3 dataClassifier.py -c naiveBayes -k 2<br/>"
      "python3 dataClassifier.py -c naiveBayes --autotune", "CodeX"),
    PageBreak(),
    p("4. Question 3: Odds ratios", "H1X"),
    p("Features are ranked by P(f=1|label 3) / P(f=1|label 6), and the top 100 are "
      "returned. The measured pattern matches handout choice <b>(a)</b>. Because the "
      "handout names q2 while the starter file contains q3, both functions return "
      "<font name='Courier'>'a'</font>."),
    p("python3 dataClassifier.py -a -d digits -c naiveBayes -o -1 3 -2 6", "CodeX"),
    p("5. Question 4: Enhanced digit features", "H1X"),
    p("Every added feature is binary. Multi-valued properties use one-hot or cumulative "
      "threshold encodings. The extractor adds component and hole counts, total and "
      "regional ink densities, bounding-box aspect, symmetry, 4 x 4 zone densities, "
      "center-of-mass thresholds and scan-line crossing thresholds."),
    result_table(["Feature set", "Validation", "Test", "Test gain"], [
        ["Basic pixels", "82%", "78%", "-"],
        ["Pixels plus enhanced features", "85%", "84%", "+6 points"],
    ], [3.0*inch, .9*inch, .8*inch, 1.05*inch]),
    p("Table 3. Enhanced features meet the handout's full 84% test threshold. Topology, "
      "balance and stroke-transition summaries resist small writing shifts.", "SmallX"),
    p("python3 dataClassifier.py -d digits -c naiveBayes -f -a -t 1000", "CodeX"),
    p("6. Verification results", "H1X"),
    result_table(["Check", "Result", "Evidence"], [
        ["Edited-file syntax", "PASS", "All four files compile under Python 3"],
        ["ID3 XOR regression", "PASS", "All four truth-table rows classified"],
        ["Reduced-error pruning", "PASS", "45 to 31 nodes; 44% to 46% test"],
        ["Naive Bayes reference", "PASS", "74% validation / 65% test"],
        ["Odds ranking", "PASS", "100 features; answer (a)"],
        ["Enhanced features", "PASS", "All values binary; 85% / 84%"],
        ["Submission archive", "PASS", "Fresh extraction and CRC verification"],
    ], [2.0*inch, .70*inch, 3.35*inch]),
    p("Table 4. Independent checks and fresh-package runs against the final archive.", "SmallX"),
    p("ID3 exposes feature interactions but is sensitive to the small training sample; "
      "validation-guided pruning makes it smaller and slightly more accurate. Naive Bayes "
      "is stronger for this image task. Compact shape summaries add information that raw "
      "pixel identity alone misses."),
]

doc.build(story)
print(OUT)
