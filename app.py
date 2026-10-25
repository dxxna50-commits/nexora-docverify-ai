import streamlit as st
from pypdf import PdfReader
from io import BytesIO
from datetime import datetime
import re


# ---------- PAGE CONFIGURATION ----------

st.set_page_config(
    page_title="◈ NEXORA DOCVERIFY AI",
    page_icon="📄",
    layout="wide"
)


# ---------- CUSTOM DESIGN ----------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg: #07111F;
        --panel: #101E30;
        --cyan: #54E6E6;
        --blue: #4287FF;
        --text: #EDF5FF;
        --muted: #9EB2CC;
        --border: rgba(137, 178, 220, 0.20);
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                ellipse at 12% 5%,
                rgba(37, 106, 170, 0.22),
                transparent 38%
            ),
            radial-gradient(
                ellipse at 90% 30%,
                rgba(35, 190, 200, 0.10),
                transparent 35%
            ),
            #07111F;
        color: var(--text);
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -0.6px;
        color: #EDF5FF;
    }

    h2 {
        font-size: 1.55rem !important;
    }

    p, label, .stMarkdown {
        color: #D6E4F5;
    }

    [data-testid="stSidebar"] {
        background: #0A1727;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--cyan);
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 36px 38px;
        border: 1px solid rgba(84, 230, 230, 0.28);
        border-radius: 22px;
        background: linear-gradient(
            120deg,
            rgba(17, 39, 64, 0.98),
            rgba(15, 48, 72, 0.94),
            rgba(17, 34, 59, 0.98)
        );
        margin-bottom: 22px;
        box-shadow: 0 18px 55px rgba(0, 0, 0, 0.22);
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 230px;
        height: 230px;
        right: -75px;
        top: -100px;
        border-radius: 50%;
        border: 1px solid rgba(84, 230, 230, 0.25);
        box-shadow:
            0 0 0 24px rgba(84, 230, 230, 0.035),
            0 0 0 50px rgba(84, 230, 230, 0.025);
        pointer-events: none;
    }

    .hero-kicker {
        color: #54E6E6;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 13px;
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(32px, 4vw, 52px);
        font-weight: 700;
        line-height: 1.12;
        letter-spacing: -1.8px;
        color: #FFFFFF;
        margin: 0;
    }

    .hero-title span {
        color: #54E6E6;
    }

    .hero-subtitle {
        color: #B9CBE0;
        font-size: 16px;
        line-height: 1.7;
        max-width: 700px;
        margin-top: 14px;
        margin-bottom: 0;
    }

    .hero-tag {
        display: inline-block;
        margin-top: 22px;
        padding: 7px 12px;
        border: 1px solid rgba(84, 230, 230, 0.30);
        border-radius: 30px;
        color: #A9F7F1;
        background: rgba(84, 230, 230, 0.07);
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1px;
    }

    .section-label {
        color: #54E6E6;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .metric-card {
        background: linear-gradient(
            145deg,
            rgba(21, 39, 61, 0.96),
            rgba(12, 27, 44, 0.96)
        );
        border: 1px solid rgba(137, 178, 220, 0.22);
        border-radius: 16px;
        padding: 21px;
        min-height: 125px;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.13);
    }

    .metric-label {
        color: #A8BCD3;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.3px;
        text-transform: uppercase;
    }

    .metric-value {
        font-family: 'Space Grotesk', sans-serif;
        color: #FFFFFF;
        font-size: 32px;
        font-weight: 700;
        margin-top: 10px;
        line-height: 1.2;
    }

    .metric-note {
        color: #829BB8;
        font-size: 12px;
        margin-top: 6px;
    }

    div[data-testid="stFileUploader"] {
        background: rgba(16, 30, 48, 0.65);
        border: 1px dashed rgba(84, 230, 230, 0.40);
        border-radius: 16px;
        padding: 12px;
    }

    div[data-testid="stExpander"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        background: rgba(16, 30, 48, 0.50);
    }

    .stButton > button {
        background: linear-gradient(100deg, #168EAE, #397CFF);
        color: white;
        border: 0;
        border-radius: 10px;
        padding: 0.65rem 1.3rem;
        font-weight: 700;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border: 1px solid #76F0F0;
        color: white;
        box-shadow: 0 0 18px rgba(66, 135, 255, 0.25);
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    hr {
        border-color: rgba(137, 178, 220, 0.17);
    }

    .footer-note {
        color: #8198B2;
        font-size: 12px;
        text-align: center;
        letter-spacing: 0.5px;
        padding-top: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------- TEXT EXTRACTION ----------

def extract_pdf_text(file):
    pdf = PdfReader(BytesIO(file.getvalue()))
    pages = []

    for page in pdf.pages:
        pages.append(page.extract_text() or "")

    return "\n".join(pages)


# ---------- FIELD EXTRACTION ----------

def find_field(text, patterns):
    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.MULTILINE
        )

        if match:
            value = match.group(1).strip()
            value = re.split(r"\s{2,}", value)[0]
            return value.strip(" :,-")

    return ""


def extract_fields(text):
    return {
        "Applicant name": find_field(text, [
            r"^\s*(?:applicant\s+name|full\s+name|name)"
            r"\s*[:\-]\s*([^\n\r]+)",
            r"^\s*(?:applicant\s+name|full\s+name|name)"
            r"\s*\n\s*([^\n\r]+)"
        ]),

        "Date of birth": find_field(text, [
            r"^\s*(?:date\s+of\s+birth|DOB)"
            r"\s*[:\-]\s*([^\n\r]+)",
            r"^\s*(?:date\s+of\s+birth|DOB)"
            r"\s*\n\s*([^\n\r]+)"
        ]),

        "Application date": find_field(text, [
            r"^\s*(?:application\s+date|date\s+of\s+application)"
            r"\s*[:\-]\s*([^\n\r]+)",
            r"^\s*(?:application\s+date|date\s+of\s+application)"
            r"\s*\n\s*([^\n\r]+)"
        ])
    }


# ---------- NORMALIZATION ----------

def normalize_name(value):
    return " ".join(value.casefold().split())


def normalize_date(value):
    value = value.strip()

    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d/%m/%y",
        "%d-%m-%y",
        "%d %B %Y",
        "%d %b %Y",
        "%B %d, %Y",
        "%b %d, %Y"
    ]

    for date_format in formats:
        try:
            return datetime.strptime(
                value, date_format
            ).date().isoformat()
        except ValueError:
            continue

    return value.casefold()


# ---------- VERIFICATION RULES ----------

def verify_documents(documents, required_fields):
    findings = []

    # Check required fields in every document.
    for document in documents:
        fields = document["fields"]

        for field in required_fields:
            if not fields.get(field, "").strip():
                findings.append({
                    "Document": document["filename"],
                    "Check": "Missing required field",
                    "Field": field,
                    "Details": (
                        f"{field} was not detected. "
                        "Check the original document manually."
                    ),
                    "Status": "Review required"
                })

    # Compare names and dates across documents.
    comparable_fields = [
        "Applicant name",
        "Date of birth",
        "Application date"
    ]

    for field in comparable_fields:
        values = []

        for document in documents:
            value = document["fields"].get(field, "").strip()

            if value:
                if field == "Applicant name":
                    normalized = normalize_name(value)
                else:
                    normalized = normalize_date(value)

                values.append({
                    "filename": document["filename"],
                    "value": value,
                    "normalized": normalized
                })

        if len(values) >= 2:
            distinct_values = {
                item["normalized"] for item in values
            }

            if len(distinct_values) > 1:
                details = "; ".join(
                    f"{item['filename']}: {item['value']}"
                    for item in values
                )

                findings.append({
                    "Document": "Multiple documents",
                    "Check": "Possible mismatch",
                    "Field": field,
                    "Details": (
                        f"Different values were found. {details}. "
                        "Confirm which value is correct."
                    ),
                    "Status": "Review required"
                })

    return findings


# ---------- HERO HEADER ----------

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">
            NEXORA SYSTEMS &nbsp; / &nbsp; DOCUMENT INTELLIGENCE
        </div>
        <h1 class="hero-title">
            ◈ NEXORA <span>DOCVERIFY AI</span>
        </h1>
        <p class="hero-subtitle">
            A smarter way to review application documents.
            Extract key information, detect missing fields, and
            identify inconsistencies with a human reviewer in control.
        </p>
        <div class="hero-tag">
            ◈ &nbsp; SMART DOCUMENT REVIEW
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    "Welcome to your document review workspace. "
    "Upload PDF files below to begin."
)

st.info(
    "Prototype notice: alerts are generated by verification rules. "
    "They are not proof of fraud or document authenticity."
)


# ---------- SIDEBAR SETTINGS ----------

st.sidebar.markdown(
    """
    <div style="
        font-family: 'Space Grotesk', sans-serif;
        font-size: 23px;
        font-weight: 700;
        color: #54E6E6;
        padding-bottom: 5px;
    ">
        ◈ NEXORA DOCVERIFY AI &nbsp; • &nbsp;
    </div>
    <div style="
        font-size: 11px;
        letter-spacing: 2px;
        color: #9EB2CC;
        margin-bottom: 20px;
    ">
        REVIEW SETTINGS
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("Verification rules")

required_fields = st.sidebar.multiselect(
    "Fields required in each PDF",
    options=[
        "Applicant name",
        "Date of birth",
        "Application date"
    ],
    default=[
        "Applicant name",
        "Date of birth"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Tip: select Application date if every uploaded document "
    "must contain an application date."
)

st.sidebar.caption(
    "NEXORA DOCVERIFY • Prototype"
)


# ---------- DOCUMENT UPLOAD ----------

st.markdown(
    '<div class="section-label">01 / DOCUMENT INTAKE</div>',
    unsafe_allow_html=True
)

st.header("Upload documents")

uploaded_files = st.file_uploader(
    "Choose text-based PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)


# Reset old results when the uploaded file list changes.
upload_signature = tuple(
    (file.name, file.size) for file in uploaded_files
) if uploaded_files else tuple()

if st.session_state.get("upload_signature") != upload_signature:
    st.session_state["upload_signature"] = upload_signature
    st.session_state["findings"] = []
    st.session_state["verified"] = False


# ---------- READ UPLOADED FILES ----------

if uploaded_files:
    documents = []

    for file in uploaded_files:
        try:
            text = extract_pdf_text(file)
            fields = extract_fields(text)

            documents.append({
                "filename": file.name,
                "text": text,
                "fields": fields
            })

        except Exception:
            st.error(
                f"Could not read {file.name}. "
                "Check whether it is a valid PDF."
            )

    if documents:
        st.success(
            f"Successfully read {len(documents)} PDF document(s)."
        )

        # ---------- EXTRACTED INFORMATION ----------

        st.divider()

        st.markdown(
            '<div class="section-label">02 / DATA EXTRACTION</div>',
            unsafe_allow_html=True
        )

        st.header("Extracted information")

        for document in documents:
            with st.expander(
                f"📄  {document['filename']}",
                expanded=False
            ):
                st.write("**Detected fields**")

                for field, value in document["fields"].items():
                    if value:
                        st.write(f"**{field}:** {value}")
                    else:
                        st.write(f"**{field}:** Not detected")

                with st.expander("View full extracted text"):
                    st.text(
                        document["text"]
                        if document["text"].strip()
                        else "No selectable text was found in this PDF."
                    )

        # ---------- VERIFICATION ----------

        st.divider()

        st.markdown(
            '<div class="section-label">03 / VALIDATION ENGINE</div>',
            unsafe_allow_html=True
        )

        st.header("Verification results")

        st.write(
            "Run the configured rules to check for missing fields "
            "and possible differences between documents."
        )

        if st.button("Run verification", type="primary"):
            st.session_state["findings"] = verify_documents(
                documents,
                required_fields
            )
            st.session_state["verified"] = True

        if st.session_state.get("verified", False):
            findings = st.session_state["findings"]
            total_documents = len(documents)
            total_findings = len(findings)

            st.write("")

            # ---------- DASHBOARD METRICS ----------

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            Documents uploaded
                        </div>
                        <div class="metric-value">
                            {total_documents}
                        </div>
                        <div class="metric-note">
                            PDFs processed
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            Findings to review
                        </div>
                        <div class="metric-value"
                             style="color: #54E6E6;">
                            {total_findings}
                        </div>
                        <div class="metric-note">
                            Rule-based alerts
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col3:
                st.markdown(
                    """
                    <div class="metric-card">
                        <div class="metric-label">
                            Verification status
                        </div>
                        <div class="metric-value"
                             style="font-size: 25px; color: #8FC7FF;">
                            COMPLETED
                        </div>
                        <div class="metric-note">
                            Rules executed
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.write("")

            # ---------- FINDINGS LIST ----------

            if findings:
                st.warning(
                    f"{len(findings)} finding(s) need human review."
                )

                for index, finding in enumerate(findings, start=1):
                    with st.container(border=True):
                        st.markdown(
                            f"**{index}. {finding['Check']} — "
                            f"{finding['Field']}**"
                        )

                        st.caption(
                            f"Document: {finding['Document']}"
                        )

                        st.write(finding["Details"])

                        st.caption(
                            "Recommended action: Review the original "
                            "document and confirm the correct information."
                        )
            else:
                st.success(
                    "No missing required fields or cross-document "
                    "mismatches were detected by the configured rules."
                )

            st.caption(
                "A human reviewer must investigate flagged items. "
                "No alerts do not guarantee that a document is correct."
            )

        else:
            st.caption(
                "Select Run verification to display your results."
            )

else:
    st.info(
        "No documents uploaded yet. Add one or more text-based PDFs "
        "to start the review."
    )


# ---------- NEXT STEPS ----------

st.divider()

st.markdown(
    '<div class="section-label">04 / FUTURE DEVELOPMENT</div>',
    unsafe_allow_html=True
)

st.header("What's next?")

next_col1, next_col2, next_col3 = st.columns(3)

with next_col1:
    st.markdown("**01 — OCR Support**")
    st.caption(
        "Read scanned documents and image-based PDFs."
    )

with next_col2:
    st.markdown("**02 — Custom Rules**")
    st.caption(
        "Configure checks for different application types."
    )

with next_col3:
    st.markdown("**03 — Export Reports**")
    st.caption(
        "Generate downloadable verification summaries."
    )

st.divider()

st.markdown(
    """
    <div class="footer-note">
        NEXORA DOCVERIFY AI &nbsp; • &nbsp;
        DOCUMENT INTELLIGENCE &nbsp; • &nbsp;
        HUMAN REVIEW STAYS IN CONTROL
    </div>
    """,
    unsafe_allow_html=True
)
