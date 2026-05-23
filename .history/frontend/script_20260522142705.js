async function predictNews() {
    const text = document.getElementById("newsInput").value;
    const result = document.getElementById("result");

    result.innerHTML = "Analyzing...";

    const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
    });

    const data = await response.json();

    result.innerHTML =
        data.prediction +
        "<br><small>Confidence: " +
        data.confidence +
        "</small>";

    if (data.prediction.includes("FAKE")) {
        result.style.color = "red";
    } else {
        result.style.color = "green";
    }
}