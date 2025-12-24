# 🎯 AI Interview Trainer

An AI-powered interview preparation platform that helps candidates practice interviews using resume-based, job-specific AI questions with real-time evaluation and scoring.

Built using **Streamlit** and **Google Gemini API**.

---

## 🚀 Key Features

- 📄 Upload resume (PDF or Image)
- 📝 Paste job description
- 🤖 AI-generated interview questions
- ✍️ Text-based answer submission
- 📊 AI-powered evaluation & scoring (out of 10)
- 🧠 Detailed feedback and improvement suggestions
- 📥 Download complete interview report (JSON)
- 🔐 Secure API key handling (not stored)

---

## 🧠 How It Works

1. User uploads their resume  
2. User enters the job description  
3. AI generates role-specific interview questions  
4. User answers each question  
5. AI evaluates answers using resume + JD context  
6. Final score and detailed feedback are generated  

---

## 🛠️ Tech Stack

| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| Backend AI | Google Gemini API |
| OCR | OpenCV + Tesseract |
| PDF Parsing | PyPDF2 |
| Image Processing | Pillow |
| Language | Python |
| Data Handling | NumPy |

---

## 📂 Project Structure

```
AI-Interview-Trainer/
│
├── interview.py          # Main Streamlit application
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Ignored files
├── .env.example          # Environment variable template
└── venv/                 # Local virtual environment (ignored)
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Interview-Trainer.git
cd AI-Interview-Trainer
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Mac / Linux**
```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Gemini API Key

You have two options:

**Option A (Recommended):**  
Enter the API key directly in the Streamlit sidebar.

**Option B:**  
Create a `.env` file (not uploaded to GitHub):

```
GEMINI_API_KEY=your_api_key_here
```

---

### 5️⃣ Run the Application

```bash
streamlit run interview.py
```

The app will automatically open in your browser.

---

## 📊 Output & Reports

- AI-generated interview questions
- Score for each answer
- Detailed feedback and improvement suggestions
- Downloadable JSON report containing:
  - Questions
  - Answers
  - Evaluations
  - Scores
  - Average score
  - Timestamp

---

## 🔐 Security Practices

- API keys are never committed to GitHub
- `.env` file is ignored using `.gitignore`
- Virtual environment (`venv`) is excluded from version control

---

## 🧪 Supported Resume Formats

- ✅ PDF (`.pdf`)
- ✅ Images (`.png`, `.jpg`, `.jpeg`)

---

## 👨‍💻 Author

**Keshav Arora**  
B.Tech (ECE)  
Python Developer | AI/ML Enthusiast  
📍 Noida, India

---

## ⭐ Future Enhancements

- 🎙️ Voice-based interview answers
- 📹 Video interview analysis
- 🧠 Domain-specific interview modes
- 👥 User authentication and history tracking
- ☁️ Cloud deployment (Streamlit Cloud / AWS)

---

## 📜 License

This project is open-source and available under the **MIT License**.

---

⭐ If you found this project useful, please consider giving it a star!
