🧪 Chemical Equipment Parameter Visualizer

A full-stack hybrid application to upload chemical equipment CSV data, analyze parameters, visualize insights 📊, and generate downloadable PDF reports 📄.

Built with Django + React + PyQt5, this project works as:
- 🌐 Web Application  
- 🖥️ Desktop Application  

---

✨ Features

✅ Upload CSV files containing chemical equipment data  
📈 Automatic computation of:
- Total equipment count
- Average flow rate
- Average pressure
- Average temperature  

📊 Interactive chart visualization (Equipment Type Distribution)  
📄 Downloadable PDF summary report  
🔐 Secure API access using Basic Authentication  
🖥️ Works on Web + Desktop  

---

🗂️ Project Structure
Chemical-Equipment-Parameter-Visualizer/
│
├── backend/ # Django backend (API + PDF)
││ ├── backend/
││ ├── equipment/
││ ├── manage.py
││ └── requirements.txt
│
├── web-frontend/ # React web app
││ ├── src/App.js
││ └── package.json
│
├── desktop_app/ # PyQt5 desktop app
││ ├── app.py
││ └── requirements.txt
│
└── README.md

---

🔗 API Endpoints
Endpoint	Method	Description
/api/upload/	POST	Upload CSV & get summary
/api/report/pdf/	GET	Download PDF report

All endpoints require Basic Authentication

---

🔐 Authentication

Example credentials:

Username: admin
Password: whatsupgang


Used by:

React web app 🌐
PyQt desktop app 🖥️
curl / Postman 🧪

---

🧰 Technologies Used

🐍 Python
🌐 Django & Django REST Framework
⚛️ React.js
📊 Chart.js
🖥️ PyQt5
📈 Matplotlib
🗄️ SQLite
🎨 HTML / CSS / JavaScript

---

📤 Outputs

✔ Summary statistics
✔ Interactive bar chart
✔ Downloadable PDF report

---

👨‍💻 Author

Hargun Kohli
🎓 Computer Science Engineering
💻 Full-Stack Developer (Web + Desktop)