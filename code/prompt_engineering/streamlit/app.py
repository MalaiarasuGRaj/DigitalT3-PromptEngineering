import os
import sys
import logging
import re
import io
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

# Setting up directories and paths
current_dir = os.path.dirname(os.path.abspath(__file__))
kit_dir = os.path.abspath(os.path.join(current_dir, ".."))
repo_dir = os.path.abspath(os.path.join(kit_dir, ".."))

sys.path.append(kit_dir)
sys.path.append(repo_dir)

import streamlit as st
from dotenv import load_dotenv
from src.llm_management import LLMManager

# Load environment variables
load_dotenv(os.path.join(repo_dir, '.env'))

# Logging setup
logging.basicConfig(level=logging.INFO)
logging.info("App started at: http://localhost:8501")


@st.cache_data
def call_api(llm_manager: LLMManager, prompt: str, llm_expert: str) -> str:
    """Calls the API endpoint with the prompt and returns the completion text."""
    llm = llm_manager.set_llm(model_expert=llm_expert)
    completion_text = llm.invoke(prompt)
    return completion_text


def extract_pdf_content(pdf_files):
    """Extract text and images from PDF files."""
    combined_text = ""
    for pdf_file in pdf_files:
        try:
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            text = ""
            image_text = ""

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()

                images = page.get_images(full=True)
                for img in images:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))

                    try:
                        image_text += pytesseract.image_to_string(image)
                    except pytesseract.TesseractNotFoundError as e:
                        logging.error(f"Tesseract not found: {e}")
                    except Exception as e:
                        logging.error(f"Error processing image: {e}")

            combined_text += text + " " + image_text
        except Exception as e:
            logging.error(f"Error extracting PDF content: {e}")
    return combined_text


def clean_text(text):
    """Clean extracted text."""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)  # Keep only letters, numbers, and basic punctuation
    return text.strip()


def main():
    # Streamlit page configuration
    st.set_page_config(page_title='QuiZenius AI', layout="centered", initial_sidebar_state="expanded",
                       menu_items={'Get help': 'https://github.com/sambanova/ai-starter-kit/issues/new'})

    # HTML and CSS for centering and styling the title, subheader with modern font and italic text
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap');

        .title-container {
            text-align: center;
            padding: 40px 0;
        }
        .sambanova {
            font-size: 40px;
            font-weight: bold;
            color: #FFCC00;
        }
        .quizenius {
            font-size: 40px;
            font-weight: bold;
            color: white;
        }
        .subheader {
            font-size: 24px;
            color: white;
            font-style: italic;
            font-family: 'Lato', sans-serif;
        }
    </style>
    <div class="title-container">
        <span class="sambanova">SambaNova's</span>&nbsp;
        <span class="quizenius">QuiZenius AI</span>
        <div class="subheader">Smart Learning, Enhanced by AI 📚🤖</div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize LLM Manager
    llm_manager = LLMManager()
    llm_info = llm_manager.llm_info

    # Streamlit Sidebar for User Input and Profile
    with st.sidebar:
        linkedin_url = "https://www.linkedin.com/in/malaiarasu-g-raj-38b695252/"
        github_url = "https://github.com/MalaiarasuGRaj"

        st.markdown(f"""
             <style>
                 .link-style {{
                     color: #FFCC00; /* Initial color */
                     text-decoration: none; /* Remove underline */
                     font-weight: normal; /* Normal weight */
                     transition: all 0.3s ease; /* Smooth transition for hover effect */
                     font-size: 16px; /* Initial font size */
                 }}
                 .link-style:hover {{
                     color: #0033cc; /* Dark blue color on hover */
                     transform: scale(1.2); /* Bulge effect */
                     font-weight: bold; /* Make bold */
                     font-size: 18px; /* Increase font size */
                 }}
             </style>
             Developed By:<br>
             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #FFCC00;"><b>Malaiarasu GRaj</b></span><br>
             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="{linkedin_url}" class="link-style" target="_blank">LinkedIn</a> | 
             <a href="{github_url}" class="link-style" target="_blank">GitHub</a>
             """, unsafe_allow_html=True)

        st.markdown("""
                    <style>
                        .divider {
                            border: none;
                            height: 1px;
                            background: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 1), rgba(255, 255, 255, 0));
                            margin: 20px 0;
                            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                        }
                    </style>
                    <hr class="divider">
                    <br>
                    """, unsafe_allow_html=True)

        # Expander for required fields
        with st.expander("Primary Inputs", expanded=True):
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

        # Expander for optional fields
        with st.expander("Additional Inputs"):
            # Add Preferred Language (Optional)
            preferred_language = st.text_input("Preferred Language (Optional):",
                                               placeholder="Enter preferred language...")

            # PDF Upload field (Optional)
            uploaded_files = st.file_uploader("Upload Reference Material (Optional, PDF)", type=["pdf"],
                                              accept_multiple_files=True)

            # Additional Instructions field (Optional):
            additional_instructions = st.text_area("Additional Instructions (Optional):")

        # Validate required fields after both expanders
        if topic and familiarity != "Select..." and learning_mode != "Select..." and st.session_state.time_available:
            # Display success message
            success_message = st.empty()
            success_message.success("All required fields are filled!")

            # JavaScript to close success message after 3 seconds
            st.markdown("""
                <script>
                setTimeout(function() {
                    const successDiv = document.querySelector('.stAlert');
                    if (successDiv) {
                        successDiv.style.display = 'none';
                    }
                }, 3000);
                </script>
            """, unsafe_allow_html=True)

            # Generate button
            generate_button = st.button("Generate Content")

            # Trigger content generation on button click
            if generate_button:
                st.session_state.generate_content = True
        else:
            st.error("Please fill all the required fields to proceed.")
            preferred_language = None
            uploaded_files = None
            additional_instructions = None
            generate_button = None

    # Initialize session state for content generation
    if 'generate_content' not in st.session_state:
        st.session_state.generate_content = False

    # Generate content if the button is clicked
    if st.session_state.generate_content:
        if learning_mode == "Lesson":
            prompt = f"As an experienced educator, explain the reasoning behind the key concepts of '{topic}' to a {familiarity} level learner. Structure the explanation to ensure clarity within {st.session_state.time_available} minutes. Contextualize the content with real-world examples and guide the learner through the topic using relatable storytelling. Keep the learner motivated by highlighting practical applications. Finally, evaluate the learning process by recommending 2-3 free, high-quality online courses and relevant YouTube lectures with their links (Don't provide any dummy link that does not exist, provide links that really exist). Also suggest 1-2 projects for hands-on practice. Incorporate {additional_instructions} to further enhance the experience."

        elif learning_mode == "Quiz":
            prompt = f"As an experienced educator, assess the learner’s understanding of '{topic}' with a quiz designed for a {familiarity} level learner. Include multiple-choice, true/false, and short-answer questions. Provide detailed instructions and context for each question. Evaluate the learner's progress by giving immediate feedback on correct and incorrect answers. Ensure the quiz fits within {st.session_state.time_available} minutes, and integrate {additional_instructions} to make the assessment more tailored and effective."

        if preferred_language:
            prompt += f" Use {preferred_language} language in the response."

        if additional_instructions:
            prompt += f" Additionally, {additional_instructions}"

        # Handle uploaded PDF content
        if uploaded_files:
            extracted_text = extract_pdf_content(uploaded_files)
            clean_extracted_text = clean_text(extracted_text)
            prompt += f" Reference the following additional material: {clean_extracted_text}"

        # Call the API using the prompt
        response = call_api(llm_manager, prompt, llm_info["select_expert"])

        # Display the response
        st.write(response)

        # Reset content generation flag
        st.session_state.generate_content = False

if __name__ == "__main__":
    main()
