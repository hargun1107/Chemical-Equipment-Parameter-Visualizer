import React, { useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const res = await axios.post(
        "http://127.0.0.1:8000/api/upload/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setSummary(res.data);
    } catch (error) {
      alert("Upload failed. Check backend server.");
    } finally {
      setLoading(false);
    }
  };

  const chartData = summary
    ? {
        labels: Object.keys(summary.equipment_type_distribution),
        datasets: [
          {
            label: "Equipment Count",
            data: Object.values(summary.equipment_type_distribution),
            backgroundColor: "rgba(54, 162, 235, 0.7)",
          },
        ],
      }
    : null;

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>Chemical Equipment Parameter Visualizer</h1>

      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <br />
      <br />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload CSV"}
      </button>

      {summary && (
        <div style={{ marginTop: "30px" }}>
          <h2>Summary</h2>
          <p><b>Total Count:</b> {summary.total_count}</p>
          <p><b>Average Flowrate:</b> {summary.average_flowrate}</p>
          <p><b>Average Pressure:</b> {summary.average_pressure}</p>
          <p><b>Average Temperature:</b> {summary.average_temperature}</p>
        </div>
      )}

      {chartData && (
        <div style={{ width: "600px", marginTop: "40px" }}>
          <h2>Equipment Type Distribution</h2>
          <Bar data={chartData} />
        </div>
      )}
    </div>
  );
}

export default App;
