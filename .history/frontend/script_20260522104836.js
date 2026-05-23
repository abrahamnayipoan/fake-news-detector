async function predictNews() {
    // Get input text
    const text = document.getElementById("newsInput").value;

    // Get result box
    const result = document.getElementById("result");

    console.log("User input:", text);

    // Validate input
    if (text.trim() === "") {
        result.innerText = "Please enter some news text!";
        result.style.color = "red";
        return;
    }

    // Show loading state
    result.innerText = "Checking news...";
    result.style.color = "blue";

    try {
        // Send request to Flask backend
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        // Convert response to JSON
        const data = await response.json();

        console.log("Server response:", data);

        // Show result
        result.innerText = data.prediction;

        // Color based on result
        if (data.prediction.includes("FAKE")) {
            result.style.color = "red";
        } else {
            result.style.color = "green";
        }

    } catch (error) {
        console.log("Error:", error);
        result.innerText = "Backend not connected!";
        result.style.color = "orange";
    }
}

