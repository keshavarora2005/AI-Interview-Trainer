import streamlit as st
import os
import cv2
import pytesseract
import google.generativeai as genai
import json
from datetime import datetime
import PyPDF2
import tempfile
import numpy as np
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="AI Interview Trainer",
    page_icon="🎯",
    layout="wide"
)

class AIInterviewTrainer:
    def __init__(self, gemini_api_key):
        """Initialize the AI Interview Trainer"""
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def extract_text_from_pdf(self, pdf_file):
        """Extract text from PDF resume"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            st.error(f"Error extracting PDF: {e}")
            return None
    
    def extract_text_from_image(self, image_file):
        """Extract text from image resume using OpenCV and Tesseract"""
        try:
            # Convert uploaded file to OpenCV format
            image = Image.open(image_file)
            img_array = np.array(image)
            
            # Convert RGB to BGR for OpenCV
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            else:
                img = img_array
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding for better OCR
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            
            # Use pytesseract to extract text
            text = pytesseract.image_to_string(thresh)
            return text
        except Exception as e:
            st.error(f"Error extracting from image: {e}")
            return None
    
    def generate_interview_questions(self, resume_text, job_description, num_questions=5):
        """Generate interview questions using Gemini API"""
        prompt = f"""
        Based on the following resume and job description, generate {num_questions} relevant interview questions.
        
        Resume:
        {resume_text}
        
        Job Description:
        {job_description}
        
        Generate questions that assess:
        1. Technical skills relevant to the job
        2. Experience mentioned in the resume
        3. Problem-solving abilities
        4. Cultural fit
        
        Format: Return only the questions, numbered 1 to {num_questions}, one per line.
        """
        
        try:
            response = self.model.generate_content(prompt)
            questions = response.text.strip().split('\n')
            questions = [q.strip() for q in questions if q.strip()]
            return questions
        except Exception as e:
            st.error(f"Error generating questions: {e}")
            return []
    
    def evaluate_answer(self, question, answer, resume_text, job_description):
        """Evaluate user answer using Gemini API"""
        prompt = f"""
        Evaluate the following interview answer:
        
        Question: {question}
        Answer: {answer}
        
        Resume Context:
        {resume_text[:500]}
        
        Job Description Context:
        {job_description[:500]}
        
        Provide:
        1. Score out of 10
        2. Detailed feedback on the answer
        3. Suggestions for improvement
        
        Format your response as:
        Score: [number]/10
        Feedback: [detailed feedback]
        Suggestions: [improvement suggestions]
        """
        
        try:
            response = self.model.generate_content(prompt)
            evaluation = response.text.strip()
            
            # Extract score
            score_line = [line for line in evaluation.split('\n') if 'Score:' in line]
            score = score_line[0].split(':')[1].strip() if score_line else "N/A"
            
            return {
                'score': score,
                'evaluation': evaluation
            }
        except Exception as e:
            st.error(f"Error evaluating answer: {e}")
            return {'score': 'N/A', 'evaluation': 'Error in evaluation'}


def main():
    # Title and description
    st.title("🎯 AI Interview Trainer")
    st.markdown("### Practice your interview skills with AI-powered feedback")
    st.markdown("---")
    
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'evaluations' not in st.session_state:
        st.session_state.evaluations = []
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = ""
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    
    # Sidebar for API configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input (stored in session state for security)
        if 'api_key' not in st.session_state:
            st.session_state.api_key = ""
        
        api_key_input = st.text_input(
            "Gemini API Key",
            type="password",
            value=st.session_state.api_key,
            help="Enter your Google Gemini API key"
        )
        
        if api_key_input:
            st.session_state.api_key = api_key_input
            st.success("✅ API Key configured")
        
        st.markdown("---")
        st.markdown("### 📊 Progress")
        if st.session_state.questions:
            st.metric("Questions Answered", 
                     f"{st.session_state.current_question}/{len(st.session_state.questions)}")
        
        st.markdown("---")
        st.markdown("### 🔄 Reset")
        if st.button("Start New Interview"):
            for key in list(st.session_state.keys()):
                if key != 'api_key':
                    del st.session_state[key]
            st.rerun()
    
    # Main content area
    if st.session_state.step == 1:
        # Step 1: Upload Resume and Job Description
        st.header("📄 Step 1: Upload Your Resume")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Upload Resume")
            uploaded_file = st.file_uploader(
                "Choose a file (PDF or Image)",
                type=['pdf', 'png', 'jpg', 'jpeg'],
                help="Upload your resume in PDF or image format"
            )
            
            if uploaded_file:
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                
                # Display preview
                if uploaded_file.type == "application/pdf":
                    st.info("📄 PDF file detected")
                else:
                    st.image(uploaded_file, caption="Resume Preview", use_container_width=True)
        
        with col2:
            st.subheader("Job Description")
            job_description = st.text_area(
                "Enter the job description",
                height=300,
                help="Paste the job description you're applying for"
            )
            
            num_questions = st.slider(
                "Number of Questions",
                min_value=3,
                max_value=10,
                value=5,
                help="Select how many interview questions you want"
            )
        
        # Process button
        if st.button("🚀 Generate Interview Questions", type="primary", use_container_width=True):
            if not st.session_state.api_key:
                st.error("⚠️ Please enter your Gemini API key in the sidebar")
            elif not uploaded_file:
                st.error("⚠️ Please upload your resume")
            elif not job_description:
                st.error("⚠️ Please enter a job description")
            else:
                with st.spinner("Processing resume..."):
                    try:
                        trainer = AIInterviewTrainer(st.session_state.api_key)
                        
                        # Extract text from resume
                        if uploaded_file.type == "application/pdf":
                            resume_text = trainer.extract_text_from_pdf(uploaded_file)
                        else:
                            resume_text = trainer.extract_text_from_image(uploaded_file)
                        
                        if resume_text:
                            st.session_state.resume_text = resume_text
                            st.session_state.job_description = job_description
                            
                            # Generate questions
                            with st.spinner("Generating interview questions..."):
                                questions = trainer.generate_interview_questions(
                                    resume_text, job_description, num_questions
                                )
                                
                                if questions:
                                    st.session_state.questions = questions
                                    st.session_state.step = 2
                                    st.success("✅ Questions generated successfully!")
                                    st.rerun()
                                else:
                                    st.error("Failed to generate questions")
                        else:
                            st.error("Failed to extract text from resume")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
    
    elif st.session_state.step == 2:
        # Step 2: Interview Questions
        st.header("💬 Interview Questions")
        
        if st.session_state.current_question < len(st.session_state.questions):
            question_num = st.session_state.current_question
            question = st.session_state.questions[question_num]
            
            st.markdown(f"### Question {question_num + 1} of {len(st.session_state.questions)}")
            st.info(question)
            
            # Answer input
            answer = st.text_area(
                "Your Answer",
                height=200,
                key=f"answer_{question_num}",
                help="Type your answer here"
            )
            
            col1, col2 = st.columns([1, 4])
            
            with col1:
                if st.button("Submit Answer", type="primary", use_container_width=True):
                    if not answer.strip():
                        st.error("Please provide an answer")
                    else:
                        with st.spinner("Evaluating your answer..."):
                            try:
                                trainer = AIInterviewTrainer(st.session_state.api_key)
                                evaluation = trainer.evaluate_answer(
                                    question,
                                    answer,
                                    st.session_state.resume_text,
                                    st.session_state.job_description
                                )
                                
                                st.session_state.answers.append(answer)
                                st.session_state.evaluations.append(evaluation)
                                st.session_state.current_question += 1
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error during evaluation: {e}")
        else:
            # All questions answered
            st.session_state.step = 3
            st.rerun()
    
    elif st.session_state.step == 3:
        # Step 3: Results and Report
        st.header("📊 Interview Report")
        st.success("🎉 Interview completed!")
        
        # Overall statistics
        col1, col2, col3 = st.columns(3)
        
        scores = []
        for eval_data in st.session_state.evaluations:
            score_str = eval_data['score']
            try:
                score_num = float(score_str.split('/')[0])
                scores.append(score_num)
            except:
                scores.append(0)
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        with col1:
            st.metric("Total Questions", len(st.session_state.questions))
        with col2:
            st.metric("Average Score", f"{avg_score:.1f}/10")
        with col3:
            st.metric("Completion", "100%")
        
        st.markdown("---")
        
        # Detailed feedback for each question
        for i in range(len(st.session_state.questions)):
            with st.expander(f"Question {i+1}: {st.session_state.questions[i]}", expanded=(i==0)):
                st.markdown("**Your Answer:**")
                st.write(st.session_state.answers[i])
                
                st.markdown("**Evaluation:**")
                st.info(st.session_state.evaluations[i]['evaluation'])
        
        # Download report button
        st.markdown("---")
        report_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'questions': st.session_state.questions,
            'answers': st.session_state.answers,
            'evaluations': [e['evaluation'] for e in st.session_state.evaluations],
            'scores': [e['score'] for e in st.session_state.evaluations],
            'average_score': f"{avg_score:.1f}/10"
        }
        
        report_json = json.dumps(report_data, indent=4)
        
        st.download_button(
            label="📥 Download Report (JSON)",
            data=report_json,
            file_name=f"interview_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )


if __name__ == "__main__":
    main()