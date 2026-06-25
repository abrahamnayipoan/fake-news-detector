async function predictNews() {
    const text = document.getElementById("newsInput").value;
    const resultBox = document.getElementById("result");

    if (text.trim() === "") {
        resultBox.innerHTML = "Please enter news text!";
        resultBox.style.color = "orange";
        return;
    }

    resultBox.innerHTML = "Analyzing...";
    resultBox.style.color = "blue";

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        if (!response.ok) {
            resultBox.innerHTML = data.message || "Something went wrong";
            resultBox.style.color = "red";
            return;
        }

        const resultText = data.prediction;
        resultBox.innerHTML = resultText;

        if (resultText === "Real News") {
            resultBox.style.color = "green";
        } else if (resultText === "Fake News") {
            resultBox.style.color = "red";
        } else {
            resultBox.style.color = "black";
        }

    } catch (error) {
        resultBox.innerHTML = "Error connecting to server";
        resultBox.style.color = "red";
    }
}