document.getElementById("verifyBtn").addEventListener("click", async function () {
  const inputText = document.getElementById("urlInput").value.trim();
  const resultDiv = document.getElementById("result");

  if (!inputText) {
    resultDiv.textContent = "Please enter a URL.";
    resultDiv.style.color = "orange";
    return;
  }

  const inputType = "url"; // default, you can add a selector for email later

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        input: inputText,
        type: inputType
      })
    });

    const data = await response.json();

    if (data.result === "Phishing") {
      resultDiv.textContent = "PHISHING DETECTED!";
      resultDiv.style.color = "red";
    } else if (data.result === "Legitimate") {
      resultDiv.textContent = "LEGITIMATE LINK";
      resultDiv.style.color = "green";
    } else if (data.error) {
      resultDiv.textContent = "Error: " + data.error;
      resultDiv.style.color = "red";
    }

  } catch (error) {
    console.error("Error:", error);
    resultDiv.textContent = "Cannot connect to backend. Make sure the Flask server is running.";
    resultDiv.style.color = "red";
  }
});
