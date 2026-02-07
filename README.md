# Chemical Equipment Parameter Visualizer

A full-stack hybrid application to upload chemical equipment CSV data, analyze key parameters, visualize insights, and generate downloadable PDF reports.

This project includes:
- A Django REST backend
- A React web frontend
- A PyQt5 desktop application
- Basic Authentication
- Chart visualizations
- PDF report generation

---

## Features

- Upload CSV files containing chemical equipment data
- Compute summary statistics:
  - Total equipment count
  - Average flow rate
  - Average pressure
  - Average temperature
- Visualize equipment type distribution using charts
- Download analyzed data as a PDF report
- Secure API access using Basic Authentication
- Use via Web App or Desktop App

---

## Project Structure

Chemical-Equipment-Parameter-Visualizer/
│
├── backend/
│ ├── backend/ # Django project settings
│ ├── equipment/ # API app (upload, summary, PDF)
│ ├── db.sqlite3
│ ├── manage.py
│ └── requirements.txt
│
├── web-frontend/
│ ├── src/
│ │ └── App.js # React frontend
│ └── package.json
│
├── desktop_app/
│ ├── app.py # PyQt5 desktop app
│ └── requirements.txt
│
└── README.md

## API Endpoints
Endpoint	      Method	Description
/api/upload/	   POST	   Upload CSV & get summary
/api/report/pdf/	GET	   Download PDF report

All API requests require Basic Authentication.

## Authentication

The backend uses Basic Auth.

Example credentials:

Username: admin
Password: whatsupgang


Used by:

React frontend

PyQt desktop app

curl / Postman


## Technologies Used

Python
Django & Django REST Framework
React.js
Chart.js
PyQt5
Matplotlib
SQLite
HTML / CSS
JavaScript


## Output Examples

Interactive chart (equipment type distribution)
Summary statistics
Downloadable PDF report

## Author

Hargun Kohli
Computer Science Engineering
Full Stack Developer