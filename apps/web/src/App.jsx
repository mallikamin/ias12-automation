import { useState, useEffect } from "react";

function App() {
  const [status, setStatus] = useState("Checking...");
  const [env, setEnv] = useState("");

  useEffect(() => {
    fetch("/api/health")
      .then((res) => res.json())
      .then((data) => {
        setStatus(data.status === "ok" ? "Connected" : "Error");
        setEnv(data.env);
      })
      .catch(() => {
        setStatus("API Unavailable");
      });
  }, []);

  return (
    <div style={{ fontFamily: "Arial, sans-serif", padding: "40px" }}>
      <h1>IAS 12 Automation - Sitara Infotech</h1>
      <p>Deferred tax computation, journals, and disclosures</p>

      <div
        style={{
          marginTop: "20px",
          padding: "20px",
          border: "1px solid #ccc",
          borderRadius: "8px",
          maxWidth: "300px",
        }}
      >
        <h3>API Status</h3>
        <p>
          Status:{" "}
          <strong style={{ color: status === "Connected" ? "green" : "red" }}>
            {status}
          </strong>
        </p>
        {env && <p>Environment: {env}</p>}
      </div>
    </div>
  );
}

export default App;
