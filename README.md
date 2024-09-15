# QuiZenius AI - Smart Learning, Enhanced by AI 📚🤖

QuiZenius AI is an intelligent learning platform that tailors educational content based on user input. It leverages AI to generate personalized lessons or quizzes depending on the learner’s needs, familiarity level, and available time. This project builds on SambaNova’s AI Starter Kit, incorporating customization for a streamlined user experience.

## User Interface

![QuiZenius AI Tool UI](https://drive.google.com/uc?id=1-keB_NkrOP0ylqrQEwcAk5_hyKENxT9T)

## ✨ Features
- **Personalized Learning:** Generate AI-driven lessons or quizzes on any topic, customized to the learner's familiarity level and time availability.
- **Real-Time Content Generation:** Content is produced dynamically based on user input, utilizing advanced large language models (LLMs).
- **Interactive Interface:** Streamlit-based user interface with customizable themes and responsive design.
- **Multiple Input Options:** Supports text input, familiarity levels, learning modes, and optional file uploads (PDFs) for enhanced reference material.

## ✨ Enhancing Learning with the RACE Prompting Technique

QuiZenius AI uses the **RACE Technique** to generate personalized lessons or quizzes. This technique ensures that prompts are detailed, engaging, and tailored to each user’s learning needs and constraints.

### RACE Technique in Action
- **Role**: The platform acts as an experienced educator, ensuring that content is delivered clearly and effectively, tailored to the user’s learning needs.

- **Action**: QuiZenius AI crafts detailed prompts, guiding the creation of well-structured lessons or quizzes. These prompts motivate learners, keeping them engaged while matching their familiarity level and time constraints.

- **Context**: Whether generating content for a beginner or an advanced learner, the RACE technique ensures the lessons or quizzes fit the time available and incorporate any additional materials (e.g., PDFs).

- **Example**:

   - **For a Lesson**:  
     "Explain the key concepts of the topic clearly to a learner with intermediate knowledge. Use real-life examples and aim to complete the lesson within 15 minutes. Provide links to two recommended resources for further study."

   - **For a Quiz**:  
     "Create a 10-question quiz to test understanding of the topic. Include multiple-choice, true/false, and short-answer questions. Offer feedback after each question and ensure the quiz can be completed within 10 minutes."


## 🔧 Key Modifications from the Base Code
1. **Config File Adjustments:** 
   - Updated `config.yaml` to enhance the use case.
   - `max_tokens_to_generate` set to `1600` for more extensive content.
   - Temperature set to `0.5` to balance creativity and coherence.
   - Enabled `coe` for advanced control of the output.
   - Selected the expert model as `"Meta-Llama-3.1-405B-Instruct"`.

2. **🎨 Custom Theme Setup:** 
   - Created a `.streamlit` directory inside the `prompt_engineering` folder.
   - Developed a custom `config.toml` file to define the tool's theme, ensuring a cohesive look and feel across the user interface.

3. **📄 PDF Content Extraction:**
   - Extracts text and images from uploaded PDFs.
   - Incorporates OCR (Tesseract) to process text within images found in PDF files.

4. **📝 Streamlined User Input:**
   - Expander sections for required and additional fields, offering a clean and intuitive user experience.
   - Real-time validation of inputs to ensure required fields are filled before content generation.

## 🚀 How to Run the Project
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/MalaiarasuGRaj/DigitalT3-PromptEngineering
   cd prompt_engineering
   python3 -m venv prompt_engineering_env
   source prompt_engineering_env/bin/activate

2. **Install Dependencies:** Make sure you have all the required packages installed:
    ```bash
    pip install -r requirements.txt

3. **Set up Environment Variables:**
    - Create a `.env` file in the root directory of the repository.
    - Inside the `.env` file, paste the following line and replace the placeholder with your actual SambaNova API key:
    
    ```bash
    SAMBANOVA_API_KEY = "your_sambanova_api_key_here"

4. **Run the Streamlit App:**
    ```bash
    streamlit run streamlit/app.py --browser.gatherUsageStats false

5. **Access the Application:** The application will be available at http://localhost:8501.

## 💡 How to Use the Tool

1. Input your Preferences:

   - Choose a topic, set your familiarity level, select a learning mode (Lesson or Quiz), and specify the available time.
   - You can optionally upload PDFs as reference material for more tailored content generation.

2. Generate Content:

   - Once all required fields are filled, click the "Generate Content" button to produce lessons or quizzes.

3. Customize the Output:

   - The generated content can be customized further by specifying additional instructions or selecting a preferred language.

## 🛠 Technology Stack
- Frontend: Streamlit
- Backend: SambaNova’s LLM API
- PDF Processing: PyMuPDF (fitz) and Tesseract OCR
- Environment Management: dotenv

## 👨‍💻 Future Improvements
- Implement more advanced user profiling to better tailor content to individual learning preferences.
- Incorporate additional language models for greater flexibility in content generation.
- Add support for multiple file formats beyond PDFs (e.g., Word documents).
- **Integrate a Chatbot:** Implement an AI-powered chatbot to clarify doubts in real-time, providing users with instant assistance on topics or concepts they are struggling with.

## Developed By
**Malaiarasu GRaj**  
[LinkedIn](https://www.linkedin.com/in/malaiarasu-g-raj-38b695252/) | [GitHub](https://github.com/MalaiarasuGRaj)
