import io
import pandas as pd
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configure Streamlit page
st.set_page_config(
    page_title="Text to Excel & PDF Converter",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Text to Excel & PDF Converter")
st.write("Convert your raw tabular text into professional Excel and PDF documents directly using Python libraries.")

# Input text area
raw_text = st.text_area(
    "Paste your tabular text here:",
    height=200,
    placeholder="Name, Age, Department\nAlice, 30, Engineering\nBob, 25, Design"
)

# Delimiter selection
delimiter_option = st.selectbox(
    "Select Delimiter",
    ["Comma (,)", "Tab (\t)", "Pipe (|)", "Semicolon (;)"]
)

delimiter_map = {
    "Comma (,)": ",",
    "Tab (\t)": "\t",
    "Pipe (|)": "|",
    "Semicolon (;)": ";"
}
sep = delimiter_map[delimiter_option]

# Helper function to generate Excel file in memory
def generate_excel(text, separator):
    df = pd.read_csv(io.StringIO(text), sep=separator)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output.getvalue()

# Helper function to generate PDF file in memory
def generate_pdf(text, separator):
    df = pd.read_csv(io.StringIO(text), sep=separator)
    output = io.BytesIO()
    p = canvas.Canvas(output, pagesize=letter)
    width, height = letter

    p.drawString(50, height - 50, "Converted Document Report")
    y = height - 80

    headers = " | ".join(str(col) for col in df.columns)
    p.drawString(50, y, headers)
    y -= 20

    for _, row in df.head(30).iterrows():
        row_str = " | ".join(str(val) for val in row.values)
        p.drawString(50, y, row_str)
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 50

    p.save()
    output.seek(0)
    return output.getvalue()

# Action buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Excel", use_container_width=True):
        if not raw_text.strip():
            st.warning("Please enter some text first.")
        else:
            try:
                excel_data = generate_excel(raw_text, sep)
                st.success("Excel generated successfully!")
                st.download_button(
                    label="📥 Download Excel File",
                    data=excel_data,
                    file_name="converted.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error parsing text into Excel: {e}")

with col2:
    if st.button("Generate PDF", use_container_width=True):
        if not raw_text.strip():
            st.warning("Please enter some text first.")
        else:
            try:
                pdf_data = generate_pdf(raw_text, sep)
                st.success("PDF generated successfully!")
                st.download_button(
                    label="📥 Download PDF File",
                    data=pdf_data,
                    file_name="converted.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error parsing text into PDF: {e}")