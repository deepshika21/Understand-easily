# 💡 Understand Easily
An AI-powered concept explanation assistant that adapts explanations based on learning level and exam format. Built using Streamlit, n8n, and Google Gemini.

---

## 🚀 Live Demo
🔗 **Streamlit App:** *[your URL here]*  
🔗 **n8n Workflow (screenshot or exported JSON):** *[add link or image]*

---

## 📌 Overview
Understand Easily is an educational AI assistant designed to help students learn concepts clearly instead of memorising definitions. Users can select their **explanation level** (Beginner → Advanced) and choose an **exam mode** (Normal, 2-mark, 5-mark answer).  
The system then generates clean, precise, exam-ready explanations.

---

## 🧠 Features
- Multi-level explanations:
  - Beginner  
  - School Student  
  - College Student  
  - Advanced  
- Exam-aware answer formatting:
  - Normal  
  - 2-mark  
  - 5-mark  
- Clean and responsive Streamlit UI  
- Persistent chat history (local storage)  
- n8n-based agent workflow  
- Controlled AI outputs using strict prompts

---

## 🏗️ Architecture
  Streamlit UI → n8n Webhook → AI Agent (Gemini)
  ↳ System Prompt
  ↳ User Prompt
  ↳ Memory

### **Frontend (Streamlit)**
- Sends concept + explanation level + exam mode to n8n
- Displays chat bubbles
- Stores chat history in `chats.json`

### **Backend (n8n)**
- Webhook receives request  
- AI Agent uses:
  - Google Gemini Chat Model  
  - Strict system prompt  
  - Custom user prompt with fallbacks  
- Returns clean text output back to Streamlit

---

## 🧩 Core Prompts

### **System Prompt**
Defines strict rules:
- Clear, accurate explanations  
- No markdown  
- Follow explanation level  
- Follow exam mode style  
- No extra formatting  

### **User Prompt**
Injects:
  Concept: {{ concept }}
  Explanation Level: {{ level }}
  Exam Mode: {{ exam_mode }}
---

## 🛠️ Tech Stack
- **Python**
- **Streamlit**
- **n8n**
- **Google Gemini (AI Model)**
- **REST Webhooks**
- **Local JSON storage**




