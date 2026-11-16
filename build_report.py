"""Build the CSE 537 Project 4 report as a polished PDF."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, Flowable,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas


OUT = "/Users/karan/Desktop/SBU/AI/Project_4/CSE537_Project4_Report.pdf"
NAVY = colors.HexColor("#17365D")
BLUE = colors.HexColor("#2F75B5")
TEAL = colors.HexColor("#2A9D8F")
PALE = colors.HexColor("#EAF2F8")
INK = colors.HexColor("#24313D")
MUTED = colors.HexColor("#5D6D7E")
LIGHT = colors.HexColor("#D5DEE8")
GREEN = colors.HexColor("#DFF2E8")


class AccuracyBars(Flowable):
    def __init__(self, rows, width=430, height=145):
        super().__init__()
        self.rows = rows
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        label_w = 112
        bar_w = self.width - label_w - 42
        y = self.height - 24
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(NAVY)
        c.drawString(0, y + 13, "Measured test accuracy")
        for label, value, color in self.rows:
            c.setFont("Helvetica", 8.5)
            c.setFillColor(INK)
            c.drawString(0, y, label)
            c.setFillColor(colors.HexColor("#EEF2F5"))
            c.roundRect(label_w, y - 2, bar_w, 11, 3, fill=1, stroke=0)
            c.setFillColor(color)
            c.roundRect(label_w, y - 2, bar_w * value / 100.0, 11, 3,
                        fill=1, stroke=0)
            c.setFillColor(INK)
            c.setFont("Helvetica-Bold", 8.5)
            c.drawRightString(self.width, y, "%d%%" % value)
            y -= 25


class OddsSketch(Flowable):
    """Faithful 28x28 rendering of the final odds-ratio console output."""
    def __init__(self, width=125, height=112):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.setFillColor(colors.HexColor("#101820"))
        c.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#37E68D"))
        rows = (
            "                            ",
            "                            ",
            "                            ",
            "                            ",
            "           ##               ",
            "        ####        #       ",
            "     #######        ##      ",
            "   ########         ###     ",
            "   #######       ## ###     ",
            "      ###       ######      ",
            "               ##    #      ",
            "                            ",
            "                            ",
            "                            ",
            "                            ",
            "                            ",
            "                      #     ",
            "                      #     ",
            "                      #     ",
            "                      #     ",
            "     ##              ##     ",
            "     ###             #      ",
            "     ####          ##       ",
            "     #######     ####       ",
            "       ##############       ",
            "           ####  ##         ",
            "                            ",
            "                            ",
        )
        size = 3.25
        ox, oy = 17, 10
        for y, row in enumerate(rows):
            for x, char in enumerate(row):
                if char != " ":
                    c.rect(ox + x * size, oy + (27 - y) * size,
                           2.45, 2.45, fill=1, stroke=0)


def header_footer(c, doc):
    c.saveState()
    if doc.page > 1:
        c.setStrokeColor(LIGHT)
        c.line(0.72 * inch, 10.35 * inch, 7.78 * inch, 10.35 * inch)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(0.72 * inch, 10.48 * inch, "CSE 537 - Project 4: Classification")
        c.drawRightString(7.78 * inch, 0.46 * inch, "Page %d" % doc.page)
        c.drawString(0.72 * inch, 0.46 * inch, "Jain and Vaghulade")
    c.restoreState()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    "CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=31, leading=35, textColor=NAVY, alignment=TA_LEFT,
    spaceAfter=14,
))
styles.add(ParagraphStyle(
    "CoverSub", parent=styles["Normal"], fontName="Helvetica",
    fontSize=15, leading=21, textColor=BLUE, spaceAfter=12,
))
styles.add(ParagraphStyle(
    "H1x", parent=styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=20, leading=24, textColor=NAVY, spaceBefore=5, spaceAfter=10,
))
styles.add(ParagraphStyle(
    "Page5Title", parent=styles["H1x"], leftIndent=12, spaceBefore=12,
))
styles.add(ParagraphStyle(
    "H2x", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=12.5, leading=16, textColor=BLUE, spaceBefore=11, spaceAfter=5,
))
styles.add(ParagraphStyle(
    "Bodyx", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=9.5, leading=14, textColor=INK, spaceAfter=7,
))
styles.add(ParagraphStyle(
    "Smallx", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=8, leading=11, textColor=MUTED, spaceAfter=4,
))
styles.add(ParagraphStyle(
    "Callout", parent=styles["BodyText"], fontName="Helvetica-Bold",
    fontSize=11, leading=15, textColor=NAVY, backColor=GREEN,
    borderColor=TEAL, borderWidth=0.7, borderPadding=9, spaceBefore=7,
    spaceAfter=11,
))
styles.add(ParagraphStyle(
    "CodexBlock", parent=styles["Code"], fontName="Courier", fontSize=7.4,
    leading=10.2, textColor=INK, backColor=colors.HexColor("#F3F6F8"),
    borderPadding=7, spaceBefore=4, spaceAfter=7,
))


def p(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def result_table(rows, widths=(2.65 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch)):
    data = [[p("Configuration", "Smallx"), p("Validation", "Smallx"),
             p("Test", "Smallx"), p("Selected k", "Smallx")]]
    for row in rows:
        data.append([p(str(v), "Bodyx") for v in row])
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.35, LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


doc = BaseDocTemplate(
    OUT, pagesize=letter, leftMargin=0.72 * inch, rightMargin=0.72 * inch,
    topMargin=0.78 * inch, bottomMargin=0.68 * inch,
    title="CSE 537 Project 4: Classification",
    author="Karan Jain and Maitreya Vaghulade",
)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
              id="main", leftPadding=0, rightPadding=0,
              topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="report", frames=[frame],
                                   onPage=header_footer)])

story = []

# Cover
story += [Spacer(1, 0.72 * inch), p("CSE 537", "CoverSub"),
          p("Project 4:<br/>Classification", "CoverTitle"),
          Spacer(1, 0.10 * inch)]
accent = Table([[""]], colWidths=[1.25 * inch], rowHeights=[5])
accent.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), TEAL)]))
story += [accent, Spacer(1, 0.35 * inch),
          p("Decision Trees, Naive Bayes, Odds Ratios, and Enhanced Digit Features",
            "CoverSub"), Spacer(1, 0.64 * inch)]
team = Table([
    [p("Karan Jain", "H2x"), p("Maitreya Vaghulade", "H2x")],
    [p("SBU ID: 117420953", "Bodyx"), p("SBU ID: 117437999", "Bodyx")],
], colWidths=[3.25 * inch, 3.25 * inch])
team.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), PALE),
    ("BOX", (0, 0), (-1, -1), 0.6, LIGHT),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, LIGHT),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 14),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
]))
story += [team, Spacer(1, 0.65 * inch),
          p("Submitted November 16, 2026", "Bodyx"),
          p("Stony Brook University", "Smallx"), PageBreak()]

# Summary
story += [p("Executive Summary", "H1x"),
          p("This project implements an ID3 decision tree with reduced-error pruning and a Bernoulli naive Bayes classifier with Laplace smoothing. All results below are from the final submitted code and the exact commands specified in the handout."),
          p("The strongest required configuration was automatically tuned naive Bayes. The enhanced binary feature extractor raised test accuracy from 78% to 84% with 1,000 training images, satisfying the handout's higher extra-credit threshold.", "Callout"),
          AccuracyBars([
              ("ID3", 44, BLUE), ("ID3 + pruning", 46, TEAL),
              ("Naive Bayes (100)", 65, BLUE),
              ("NB basic (1,000)", 78, BLUE),
              ("NB enhanced (1,000)", 84, TEAL),
          ]), Spacer(1, 4),
          p("Experimental protocol", "H2x"),
          p("The supplied digit splits were used without reshuffling. Unless a command explicitly specifies 1,000 training images, the harness default is 100 training images, 100 validation images, and 100 test images. Accuracy is the fraction of exact label matches. Hyperparameters were selected only on validation data; test data was used for final evaluation."),
          p("Implementation integrity", "H2x"),
          p("Public class and method names were preserved. Features consumed by naive Bayes are binary. The implementation compiles under Python 3, and targeted regression tests cover smoothing, deterministic tie handling, odds ranking, pruning, and the zero-information XOR root case."),
          PageBreak()]

# ID3
story += [p("Question 1 - ID3 Decision Tree", "H1x"),
          p("Method", "H2x"),
          p("At each internal node, ID3 evaluates every remaining binary feature and chooses the feature with maximum information gain. Entropy is H(S) = -sum p(c) log2 p(c), and gain is the parent entropy minus the size-weighted entropy of the two child partitions. Recursion stops when a node is pure or no features remain; the leaf predicts the local majority label."),
          p("Zero-gain splits are intentionally allowed. This detail is needed for parity-like data: no root feature may be individually informative even though later splits perfectly separate the labels. Deterministic label ordering resolves majority ties, and each node stores its local majority as a safe fallback."),
          p("Reduced-error pruning", "H2x"),
          p("When <b>-p</b> is enabled, pruning proceeds bottom-up using the validation examples that reach each node. A subtree is replaced by its node-majority leaf whenever that leaf is at least as accurate as the subtree on those held-out examples. This favors the simpler model on ties and never consults the test set."),
          result_table([
              ("ID3, no pruning", "52%", "44%", "n/a"),
              ("ID3, reduced-error pruning", "54%", "46%", "n/a"),
          ]), Spacer(1, 8),
          p("The unpruned tree contained 45 nodes and 23 leaves. Pruning reduced it to 31 nodes and 16 leaves - a 31% reduction in total nodes - while improving validation accuracy by 2 points and test accuracy by 2 points. This is the expected direction: validation-guided simplification removes branches fitted to idiosyncrasies in the small training sample."),
          p("Reproduction", "H2x"),
          p("python3 dataClassifier.py -c id3 -d digits<br/>python3 dataClassifier.py -c id3 -d digits -p", "CodexBlock"),
          PageBreak()]

# NB
story += [Spacer(1, 12), p("Question 2 - Naive Bayes", "Page5Title"),
          p("Parameter estimation", "H2x"),
          p("The classifier estimates the empirical class prior P(Y) without smoothing. For every binary feature f and class y, it stores the Laplace-smoothed conditional P(f=1 | y) = (count(f=1,y) + k) / (count(y) + 2k). Counts are collected once and reused across the entire tuning grid."),
          p("Classification uses log-joint scores to avoid numerical underflow: log P(y) + sum log P(f_i | y). Both present and absent pixels contribute to the score. Automatic tuning evaluates k in {0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50}; validation ties select the smaller k."),
          result_table([
              ("Fixed-k NB, 100 training images", "69%", "55%", "2"),
              ("Autotuned NB, 100 training images", "74%", "65%", "0.1"),
              ("Basic NB, 1,000 training images", "82%", "78%", "0.001"),
              ("Enhanced NB, 1,000 training images", "85%", "84%", "0.001"),
          ]), Spacer(1, 9),
          p("Analysis", "H2x"),
          p("The 74% validation and 65% test results for 100 examples match the handout's approximate autotuned reference values. Increasing training data sharply improves the pixel model because conditional estimates become less sparse. The selected k correspondingly falls from 0.1 to 0.001: with more observations, less smoothing is needed."),
          p("Relative to fixed k=2 (69% validation / 55% test), automatic tuning gains 5 validation points and 10 test points. This confirms that the amount of smoothing materially affects the small-data model."),
          p("python3 dataClassifier.py -c naiveBayes -k 2<br/>python3 dataClassifier.py -c naiveBayes --autotune", "CodexBlock"),
          p("The main limitation is conditional independence: neighboring pixels and shape measurements are correlated. Even so, many weak pixel cues combine effectively, while global features recover shape information that individual pixels miss."),
          PageBreak()]

# Odds + enhanced
odds_table = Table([[OddsSketch(), p(
    "The actual command output has the same two-region structure as handout choice <b>(a)</b>: a concentration in the upper-left and another toward the lower-right. These locations favor a 3 relative to a 6 because a 6 more often closes its lower loop and carries stronger left-side ink. Both <b>q2()</b> and the starter-code-compatible <b>q3()</b> return <b>'a'</b>.", "Bodyx")]], colWidths=[1.95 * inch, 4.45 * inch])
odds_table.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("BOX", (0, 0), (-1, -1), 0.5, LIGHT),
    ("BACKGROUND", (0, 0), (-1, -1), PALE),
]))
story += [Spacer(1, 12), p("Question 3 - Odds Ratios", "Page5Title"),
          p("For labels y1 and y2, features are ranked by P(f=1 | y1) / P(f=1 | y2). The implementation sorts all learned features by this ratio and returns the top 100, with deterministic ordering for exact ties."),
          odds_table, Spacer(1, 8),
          p("python3 dataClassifier.py -a -d digits -c naiveBayes -o -1 3 -2 6", "CodexBlock"),
          p("Question 4 - Enhanced Features", "H1x"),
          p("Every enhanced feature is binary, preserving compatibility with the Bernoulli model. Multi-valued properties are represented with one-hot or cumulative-threshold encodings. The extractor adds:"),
          p("- Foreground component count and enclosed background-region (hole) count.<br/>- Ink-density thresholds and bounding-box aspect categories.<br/>- Horizontal and vertical symmetry indicators.<br/>- Coarse 4 x 4 zone densities and whole-region densities.<br/>- Center-of-mass thresholds for x and y.<br/>- Horizontal and vertical scan-line crossing thresholds."),
          p("With 1,000 training images, these features improve validation accuracy from 82% to 85% and test accuracy from 78% to 84%. The 6-point test gain reaches the handout's >=84% threshold. The improvement indicates that topology, balance, and stroke-transition cues compensate for small spatial shifts that raw pixel identity handles poorly.", "Callout"), Spacer(1, 10),
          p("python3 dataClassifier.py -d digits -c naiveBayes -f -a -t 1000", "CodexBlock"),
          PageBreak()]

# Verification
story += [p("Verification and Conclusions", "H1x"),
          p("Verification matrix", "H2x")]
checks = [
    ("Python syntax", "PASS", "All edited assignment files compile under Python 3."),
    ("ID3 separable data", "PASS", "Learns a simple Boolean decision boundary."),
    ("ID3 XOR regression", "PASS", "Zero-gain root splits remain available; predicts all four rows."),
    ("Reduced-error pruning", "PASS", "31 nodes versus 45; validation and test both improve."),
    ("Naive Bayes reference", "PASS", "74% validation / 65% test with autotuning and 100 images."),
    ("Odds ranking", "PASS", "Returns exactly 100 descending-ratio features; visual choice (a)."),
    ("Enhanced features", "PASS", "All values are binary; 85% validation / 84% test."),
    ("Documentation", "PASS", "Edited files include method docstrings and rationale for non-obvious logic."),
]
check_data = [[p("Check", "Smallx"), p("Status", "Smallx"), p("Evidence", "Smallx")]]
check_data += [[p(a), p(b), p(c)] for a, b, c in checks]
checks_table = Table(check_data, colWidths=[1.55 * inch, 0.75 * inch, 4.1 * inch], repeatRows=1)
checks_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
    ("TEXTCOLOR", (1, 1), (1, -1), colors.HexColor("#157347")),
    ("GRID", (0, 0), (-1, -1), 0.35, LIGHT),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story += [checks_table, Spacer(1, 12),
          p("Conclusions", "H2x"),
          p("ID3 demonstrates the value of explicit interaction modeling but is sensitive to a small training set; held-out pruning makes it smaller and slightly more accurate. Naive Bayes is substantially stronger on this high-dimensional image task, particularly as the training set grows. The final feature experiment shows the central lesson of the project: a few carefully designed shape summaries can contribute information that a much larger collection of raw measurements misses."),
          p("All reported metrics are reproducible from the final code using the commands printed in their respective sections. No test labels are used during training, tuning, feature design execution, or pruning."),
          Spacer(1, 16),
          p("Reference", "H2x"),
          p("CSE 537 Project 4: Classification handout, Fall 2026. ID3 follows the information-gain formulation described in Tom M. Mitchell, <i>Machine Learning</i>, Chapter 3 (1997).", "Smallx")]

doc.build(story)
print(OUT)
