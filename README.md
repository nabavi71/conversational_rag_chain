# 🚀 LangChain Chatbot with Weaviate (RAG-Based)

## 📌 Overview
This project is a **Dockerized LangChain chatbot** that uses **Weaviate** as a vector database for **Retrieval-Augmented Generation (RAG)**. The chatbot utilizes **Ollama LLM** for natural language processing and provides intelligent responses based on stored documents.

## 🔥 Features
- **Retrieval-Augmented Generation (RAG)**: Fetches relevant documents from Weaviate before answering.
- **Chat History Awareness**: Maintains conversation context.
- **FastAPI API**: Exposes an API for interaction.
- **Docker Support**: Easily deployable using Docker.
- **Configurable LLM**: Supports local models via Ollama.

---

## 🛠️ Installation & Setup
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/nabavi71/conversational_rag_chain.git
cd conversational_rag_chain
```

### **2️⃣ Set Up Environment Variables**
Create a `.env` file and configure:
```
WEAVIATE_HOST=localhost
WEAVIATE_PORT=8080
OLLAMA_HOST=http://localhost
OLLAMA_PORT=11434
MODEL_NAME=mistral
API_KEY=your_api_key  # If authentication is required
```

### **3️⃣ Run Weaviate (if not running already)**
```bash
docker run -d --name weaviate -p 8080:8080 semitechnologies/weaviate:latest
```

### **4️⃣ Build & Run the Chatbot in Docker**
```bash
docker build -t langchain_chatbot .
docker run -it -p 8000:8000 --env-file .env langchain_chatbot
```

---

## 🚀 API Usage
Once the chatbot is running, you can interact via FastAPI.

### **1️⃣ Start the API**
```bash
uvicorn api_service.main:app --host 0.0.0.0 --port 8000
```

### **2️⃣ Access Swagger UI**
Open in browser:
```
http://localhost:8000/docs
```

### **3️⃣ Example API Request**
#### **POST /chat**
```json
{
  "query": "What is LangChain?"
}
```
#### **Response**
```json
{
  "answer": "LangChain is a framework for developing LLM-powered applications."
}
```

---

## 🔧 Troubleshooting
### **1️⃣ Check Weaviate Connection**
```bash
curl http://localhost:8080/v1/.well-known/ready
```
If Weaviate isn’t running, restart the container:
```bash
docker restart weaviate
```

### **2️⃣ Check Logs for Errors**
```bash
docker logs langchain_chatbot
```

### **3️⃣ Debug in Interactive Mode**
```bash
docker run -it --entrypoint /bin/bash langchain_chatbot
```

---

## 📜 License
MIT License.

---

## 🤝 Contributing
Feel free to open issues or pull requests to improve this project!

---

## 📬 Contact
For questions or support, reach out to **[Your Name]** via GitHub issues.

---

### 🚀 Happy Coding! 🎯
