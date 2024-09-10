# MAL.AI 🧠🔍  
#### Smart Learning, Enhanced by AI 📚🤖  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-MalaiarasuGRaj-blue)](https://www.linkedin.com/in/malaiarasu-g-raj-38b695252/)  
[![GitHub](https://img.shields.io/github/followers/MalaiarasuGRaj?style=social)](https://github.com/MalaiarasuGRaj)  

---

MAL.AI bridges the gap between users and personalized learning by leveraging AI to create dynamic lessons and quizzes tailored to individual learning preferences and time constraints. Whether you're a beginner or an expert, MAL.AI adapts to your needs.

**Try it here**: [MAL.AI Web App](https://malai.wegic.app/home)

---

## 🚀 Features

- **Personalized Learning Plans**: Generate lessons or quizzes based on your topic, familiarity level, and available time.
- **Content Extraction**: Upload PDFs and extract text and images for enhanced learning experiences.
- **AI-Powered Content Generation**: Using the Google Gemini API, MAL.AI creates engaging lessons and quizzes.
- **PDF Download**: Generate custom PDFs of the generated content for offline study.
- **Streamlined User Interface**: Simple and intuitive design built with Streamlit for ease of use.

---

## 🎯 How to Use

### 1. **Install the Required Dependencies**
Clone this repository and install the dependencies listed in the `requirements.txt` file


### 2. Set Up Google Cloud API Key
MAL.AI uses Google's Generative AI API. Follow the steps below to set up your Google Cloud API Key:

- Create a Google Cloud Project: Create a Project

- Enable the Generative AI API for your project: Enable API

- Create an API Key: Create API Key

Once you have created the API key, copy it and securely store it. You can set it as an environment variable or modify the code (not recommended) to include the key.

### 3. Run the Streamlit App
To launch the MAL.AI application, open a terminal window, navigate to the directory containing your MAL.AI code, and run the following command: `streamlit run app.py`

### 4. Using the Interface
The MAL.AI interface consists of two main sections:

## Main Area:
- **Topic Input:** Enter the topic or subject you wish to learn about.
- **Familiarity Level:** Select your familiarity level (Beginner, Intermediate, Advanced).
- **Learning Mode:** Choose between a Lesson or a Quiz mode.
- **Time Limit:** Set the amount of time you have for the content (in minutes).
- **Upload PDF:** Optionally, upload reference PDFs for additional context.
- **Additional Instructions:** Optionally, provide extra instructions for MAL.AI.
- **Generate Content:** Click the "Generate Content" button to start processing.

## Sidebar:
- Displays developer information (LinkedIn and GitHub links).
- Shows success or error messages.
- Provides a download link for the generated PDF content (if successful).

### 5. Generated Content
## After processing:

- The lesson or quiz will be displayed on the screen.
- You can download the generated content as a PDF for offline use.

### 6. Tips for Best Use:
- Experiment with different familiarity levels and learning modes to see variations in generated content.
- Upload relevant PDFs to enhance the learning experience with additional references.
- Use the "Additional Instructions" section to tailor the output to your learning objectives.
