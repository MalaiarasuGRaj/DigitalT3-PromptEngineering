import streamlit as st
from PIL import Image
import pytesseract
import io
import re
import logging
import fitz  # PyMuPdf
import google.generativeai as genai
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Set up logging
logging.basicConfig(level=logging.INFO)

# Streamlit Components
st.title("MAL.AI 🧠🔍")
st.markdown('<style>h1{color: orange; text-align: center; margin-bottom: 0px;}</style>', unsafe_allow_html=True)
st.subheader('Smart Learning, Enhanced by AI 📚🤖')
st.markdown('<style>h3{text-align: center; margin-top: 0;}</style>', unsafe_allow_html=True)

# Streamlit Sidebar for User Input and Profile
with st.sidebar:
    # Add LinkedIn logo and link
    linkedin_url = "https://www.linkedin.com/in/malaiarasu-g-raj-38b695252/"
    github_url = "https://github.com/MalaiarasuGRaj"

    st.markdown(f"""
    Developed By:<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<font color='orange'>**Malaiarasu GRaj**</font><br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[LinkedIn]({linkedin_url}) | [GitHub]({github_url})
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Input preferences section
    st.header("Input your preferences")

    # Topic input field
    topic = st.text_input("Topic/Subject:", placeholder="Enter a topic...")

    # Familiarity level dropdown with no default selection
    familiarity = st.selectbox("Familiarity Level:", ["Select...", "Beginner", "Intermediate", "Advanced"])

    # Learning mode radio button with no default selection
    learning_mode = st.radio("Learning Mode:", ["Select...", "Lesson", "Quiz"])

    # Time available slider with small text box beside it
    st.markdown("### Time Available (Minutes):")
    col1, col2 = st.columns([4, 1])

    # Initialize state for time if not already initialized
    if 'time_available' not in st.session_state:
        st.session_state.time_available = 30  # Default value

    # Slider with label hidden
    with col1:
        st.session_state.time_available = st.slider(
            "Time Available Slider",
            min_value=5,
            max_value=120,
            value=st.session_state.time_available,
            format="%d minutes",
            key="time_available_slider",
            label_visibility="collapsed"
        )

    # Text input (small box) with label hidden
    with col2:
        time_available_text = st.text_input(
            "Time Available Box",
            value=str(st.session_state.time_available),
            max_chars=3,
            key="time_available_text",
            label_visibility="collapsed"
        )

        # Update session state with text input value
        if time_available_text:
            st.session_state.time_available = int(time_available_text)

    # Check if all required fields are filled
    if topic and familiarity != "Select..." and learning_mode != "Select..." and st.session_state.time_available:
        st.success("All required fields are filled!")
        uploaded_files = st.file_uploader("Upload Reference Material (Optional, PDF)", type=["pdf"],
                                          accept_multiple_files=True)
        additional_instructions = st.text_area("Additional Instructions (Optional):")
        generate_button = st.button("Generate Content")
    else:
        st.error("Please fill all the fields to proceed.")
        uploaded_files = None
        additional_instructions = None
        generate_button = None

# Function to extract text and images from PDF
def extract_pdf_content(pdf_files):
    combined_text = ""
    for pdf_file in pdf_files:
        try:
            doc = fitz.open(stream=pdf_file)
            text = ""
            image_text = ""

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()  # Extract text from page

                images = page.get_images(full=True)
                for img in images:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))

                    try:
                        image_text += pytesseract.image_to_string(image)  # Extract text from images using Tesseract
                    except pytesseract.TesseractNotFoundError as e:
                        logging.error(f"Tesseract not found: {e}")
                    except Exception as e:
                        logging.error(f"Error processing image: {e}")

            combined_text += text + " " + image_text
        except Exception as e:
            logging.error(f"Error extracting PDF content: {e}")
    return combined_text


# Function to clean extracted text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)  # Keep only letters, numbers, and basic punctuation
    return text.strip()


# Set up Gemini API key
api_key = "AIzaSyDIU2KmhMTybjDvsIx6rwDYoicAzHGV3RA"
genai.configure(api_key=api_key)


# Function to generate content using Gemini API
def generate_content(topic, familiarity, learning_mode, time_available, uploaded_files, additional_instructions):
    if learning_mode == "Lesson":
        prompt = f"As an experienced educator, craft a detailed and engaging lecture on '{topic}' for a {familiarity} level learner. Your role is to guide the learner through the topic in a way that makes it easy to understand within {time_available} minutes. Provide clear explanations using storytelling and relatable real-world examples. Contextualize the information with practical applications, and keep the learner motivated throughout. Additionally, recommend 2-3 free, high-quality online courses and 1-2 projects for practical application. {additional_instructions} should also be incorporated to enhance the learning experience."

    elif learning_mode == "Quiz":
        prompt = f"As an experienced educator, create a comprehensive quiz on '{topic}' for a {familiarity} level learner. Your role is to assess the learner's understanding through multiple-choice, true/false, and short-answer questions. Clearly explain each question with instructions and context. Provide immediate feedback on correct and incorrect answers to enhance the learning process. Ensure the quiz can be completed within {time_available} minutes and consider {additional_instructions} to tailor the assessment effectively."


    if uploaded_files:
        prompt += f" Use the following content for reference: {uploaded_files}"

    try:
        # Call Gemini API to generate content
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Failed to generate content: {e}")
        return None


# Function to generate PDF from text using reportlab
def generate_pdf(content):
    pdf_output = io.BytesIO()
    c = canvas.Canvas(pdf_output, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    text_object = c.beginText(40, height - 40)
    text_object.setFont("Helvetica", 12)
    text_object.setTextOrigin(40, height - 40)

    # Add text to the PDF
    for line in content.split('\n'):
        text_object.textLine(line)

    c.drawText(text_object)
    c.showPage()
    c.save()
    pdf_output.seek(0)
    return pdf_output


# Button click handler
if generate_button:
    if uploaded_files:
        pdf_files = [file.getvalue() for file in uploaded_files]
        pdf_content = extract_pdf_content(pdf_files)
        cleaned_text = clean_text(pdf_content)
    else:
        cleaned_text = ""

    content = generate_content(topic, familiarity, learning_mode, st.session_state.time_available, uploaded_files,
                               additional_instructions)

    if content:
        # Store the content in session state to keep it persistent
        st.session_state['content'] = content

        # Generate PDF
        pdf_output = generate_pdf(content)

        # Display the generated content
        st.markdown(content)

        # Show success message after content display
        st.sidebar.success("Content generated successfully!")

        # Provide a download link for the generated PDF
        st.sidebar.download_button("Download PDF", pdf_output, file_name="generated_content.pdf",
                                   mime="application/pdf")
    else:
        st.sidebar.error("Failed to generate content.")
