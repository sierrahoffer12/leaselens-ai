import re
import fitz  # PyMuPDF
import streamlit as st

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_lease_terms(text):
    patterns = {
        "Property Address": r"(?:Property Address|Premises):\s*(.+)",
        "Lease Size (sqft)": r"(?:Lease Size|Square Feet):\s*([\d,]+)",
        "Sign Date": r"(?:Sign Date|Date of Execution):\s*(.+)",
        "Expiration Date": r"(?:Expiration Date|Lease End Date):\s*(.+)",
        "Lease Term (months)": r"(?:Lease Term):\s*(\d+)\s*months",
        "Base Rent": r"(?:Base Rent):\s*\$?([\d,.]+)",
        "Effective Rent": r"(?:Effective Rent):\s*\$?([\d,.]+)",
        "Escalations": r"(?:Escalations):\s*(.+)",
        "Free Rent Months": r"(?:Free Rent Months):\s*(\d+)",
        "Tenant": r"(?:Tenant):\s*(.+)",
        "Tenant Representation": r"(?:Tenant Representation|Tenant Rep):\s*(.+)",
        "Landlord": r"(?:Landlord):\s*(.+)",
        "Landlord Representation": r"(?:Landlord Representation|Landlord Rep):\s*(.+)"
    }

    terms = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            terms[key] = match.group(1).strip()
    return terms

st.title("LeaseLens AI - Lease Abstractor Tool")
st.write("Upload a commercial lease document (PDF) to extract key terms.")

uploaded_file = st.file_uploader("Choose a lease document (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text and analyzing lease..."):
        text = extract_text_from_pdf(uploaded_file)
        lease_terms = extract_lease_terms(text)

    st.subheader("📄 Extracted Lease Summary")
    if lease_terms:
        for key, value in lease_terms.items():
            st.markdown(f"**{key}**: {value}")
    else:
        st.warning("No lease terms found. Please check the document formatting.")
