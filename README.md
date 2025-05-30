# Adam Project - AI Saviour


![Autoplaying GIF](./adam-digital.gif)


<div align="center">
  <a href="www.adamproject.live">WEBSITE</a> •
  <a href="https://github.com/Mosescod/Adam-Project/blob/main/LORE.md">LORE</a> •
  <a href="https://github.com/Mosescod/Adam-Project/blob/main/LICENSE">LICENSE</a> •
  <a href="https://github.com/Mosescod/Adam-Project/blob/main/CONTRIBUTING.md">CONTRIBUTING</a>
</div>

<br>

<div align="center">

[![Live Demo](https://img.shields.io/badge/Hades-Live_Demo-4CAF50?style=for-the-badge&logo=vercel)](https://www.adamproject.live/)
[![API Status](https://img.shields.io/website?down_message=offline&label=API&up_message=online&url=https%3A%2F%2Fyour-vercel-app.vercel.app%2Fapi%2Fchat)](https://www.adamproject.live/)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![GitHub Stars](https://img.shields.io/github/stars/Mosescod/Adam-Project.svg)](https://github.com/Mosescod/Adam-Project/stargazers)

</div>

## About Adam

Adam is an advanced conversational AI designed to engage in meaningful, context-aware dialogues. Unlike typical chatbots, Adam maintains conversation history, understands nuanced queries, and crafts thoughtful responses using a unique knowledge synthesis system.

```python
# Example interaction
response = adam.query("Explain consciousness")
print(response)
# "*shapes clay* Consciousness is like the river that flows..."
```
## Feature	Description
<div>
� Clay Metaphors	Unique responses framed through creative clay-working analogies
  
🧠 Contextual Memory	Remembers conversation history for coherent multi-turn dialogues

⚡ Real-time Performance	Tracks and displays response times with visual feedback

🔄 Continuous Learning	Improves through interaction with a built-in memory system

🛡️ Safety Filters	Built-in ethical protocols for responsible AI interactions
</div>

## Live Adam

Tip: Try the live chat 

🚀 Installation
Quick Start (Docker)
bash
docker-compose up -d
Manual Installation
Clone the repository:

```bash
git clone https://github.com/Mosescod/Adam-Project.git
cd adamOS
Install dependencies:
```

```bash
pip install -r requirements.txt
Configure environment:
```

```bash
cp .env.example .env
Run the server:
```

```bash
python app.py
Visit http://localhost:5000 to start chatting with Adam!
```

## 🔌 API Usage
Adam provides a simple REST API for integration:

```javascript
// JavaScript Example
const response = await fetch('http://localhost:5000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: "unique-user-id",
    message: "What is the meaning of life?"
  })
});
API Endpoints
Endpoint	Method	Description
/api/chat	POST	Main conversation endpoint
/api/conversation	GET	Retrieve chat history
/api/system/status	GET	Health check 
```

## 🛠️ Tech Stack
<div align="center">
Python
Flask
JavaScript
HTML5
CSS3
</div>


## 🤝 Contributing
We welcome contributions! Please follow these steps:

Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

See our Contribution Guidelines for more details.



## 📄 License
Distributed under the MIT License. See LICENSE for more information.

<div align="center">
GitHub Issues
GitHub Forks
GitHub Contributors

</div>
