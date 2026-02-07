import React, { useState, useRef, useEffect } from "react";
import Chart from "chart.js/auto";

const API_UPLOAD = "http://127.0.0.1:8000/api/upload/";
const API_PDF = "http://127.0.0.1:8000/api/report/pdf/";

const USERNAME = "admin";
const PASSWORD = "whatsupgang";
const authHeader = "Basic " + btoa(`${USERNAME}:${PASSWORD}`);

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);

  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  const uploadCSV = async () => {
    if (!file) {
      alert("Select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(API_UPLOAD, {
      method: "POST",
      headers: { Authorization: authHeader },
      body: formData,
    });

    if (!response.ok) {
      alert("Upload failed");
      return;
    }

    const data = await response.json();
    setSummary(data);
  };

  useEffect(() => {
    if (!summary || !canvasRef.current) return;

    const distribution = summary.equipment_type_distribution;
    if (!distribution) return;

    if (chartRef.current) {
      chartRef.current.destroy();
    }

    const ctx = canvasRef.current.getContext("2d");

    chartRef.current = new Chart(ctx, {
      type: "bar",
      data: {
        labels: Object.keys(distribution),
        datasets: [
          {
            label: "Equipment Count",
            data: Object.values(distribution),
            backgroundColor: "rgba(75, 192, 192, 0.6)",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      },
    });
  }, [summary]);

  const downloadPDF = async () => {
    const response = await fetch(API_PDF, {
      headers: { Authorization: authHeader },
    });

    if (!response.ok) {
      alert("PDF download failed");
      return;
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "chemical_equipment_report.pdf";
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>Chemical Equipment Parameter Visualizer</h1>

      <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />
      <br /><br />
      <button onClick={uploadCSV}>Upload CSV</button>

      {summary && (
        <>
          <h2>Summary</h2>
          <p>Total Count: {summary.total_count}</p>
          <p>Average Flowrate: {summary.average_flowrate}</p>
          <p>Average Pressure: {summary.average_pressure}</p>
          <p>Average Temperature: {summary.average_temperature}</p>

          <div style={{ width: "600px", height: "350px" }}>
            <canvas ref={canvasRef}></canvas>
          </div>

          <br />
          <button onClick={downloadPDF}>Download PDF</button>
        </>
      )}
    </div>
  );
}

export default App;
