async function predictNews() {
    const text = document.getElementById("newsInput").value;
    const result = document.getElementById("result");

    if (text.trim() === "") {
        result.innerText = "Please enter news text!";
        result.style.color = "red";
        return;
    }

    result.innerText = "Checking...";
    result.style.color = "blue";

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        result.innerText = data.prediction;

        if (data.prediction.includes("FAKE")) {
            result.style.color = "red";
        } else {
            result.style.color = "green";
        }

    } catch (error) {
        console.log(error);
        result.innerText = "Backend not connected!";
        result.style.color = "orange";
    }
}

