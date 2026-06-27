const API_BASE_URL = "http://127.0.0.1:5000";

// For online deployment, use this instead:
// const API_BASE_URL = "https://fake-news-detector-1-bi23.onrender.com";

function showSection(sectionId) {
    const sections = document.querySelectorAll(".page-section");

    sections.forEach(section => {
        section.classList.remove("active-section");
    });

    document.getElementById(sectionId).classList.add("active-section");

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}
const API_BASE_URL = "http://127.0.0.1:5000";
function showSection(sectionId) {
    const sections = document.querySelectorAll(".page-section");

    sections.forEach(section => {
        section.classList.remove("active-section");
    });

    document.getElementById(sectionId).classList.add("active-section");

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}
// For online deployment, use this instead:
// const API_BASE_URL = "https://fake-news-detector-1-bi23.onrender.com";

function openLatestNews() {
    document.getElementById("latestNewsSection").style.display = "block";
    document.getElementById("latestNewsSection").scrollIntoView({ behavior: "smooth" });
}

function closeLatestNews() {
    document.getElementById("latestNewsSection").style.display = "none";
    document.getElementById("latestNewsResult").innerHTML = "";
}

function openImageUpload() {
    document.getElementById("imageUploadSection").style.display = "block";
    document.getElementById("imageUploadSection").scrollIntoView({ behavior: "smooth" });
}

function closeImageUpload() {
    document.getElementById("imageUploadSection").style.display = "none";
    document.getElementById("imageResult").innerHTML = "";
    document.getElementById("extractedTextBox").innerHTML = "";
    document.getElementById("imageInput").value = "";
    document.getElementById("previewImage").style.display = "none";
}

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
        const response = await fetch(`${API_BASE_URL}/predict`, {
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

        resultBox.innerHTML = data.prediction;

        if (data.prediction.includes("Real")) {
            resultBox.style.color = "green";
        } else {
            resultBox.style.color = "red";
        }

    } catch (error) {
        resultBox.innerHTML = "Error connecting to server";
        resultBox.style.color = "red";
    }
}

async function loadLatestNews() {
    const latestNewsBox = document.getElementById("latestNewsResult");

    latestNewsBox.innerHTML = "<p>Loading latest news...</p>";

    try {
        const response = await fetch(`${API_BASE_URL}/latest-news`);
        const data = await response.json();

        if (!response.ok) {
            latestNewsBox.innerHTML = `<p class="error">Error: ${data.error || "Could not load news"}</p>`;
            return;
        }

        const articles = data.articles || [];

        if (articles.length === 0) {
            latestNewsBox.innerHTML = "<p>No latest news found.</p>";
            return;
        }

        latestNewsBox.innerHTML = "";

        articles.forEach(article => {
            const card = document.createElement("div");
            card.className = "news-card";

            const predictionClass = article.prediction.includes("Real") ? "real" : "fake";

            card.innerHTML = `
                ${article.image ? `<img src="${article.image}" alt="News image" class="news-image">` : ""}
                <h3>${article.headline}</h3>
                <p>${article.description || "No description available."}</p>
                <p><strong>Source:</strong> ${article.source}</p>
                <p><strong>Published:</strong> ${article.publishedAt || "Unknown date"}</p>
                <p class="${predictionClass}">
                    <strong>Prediction:</strong> ${article.prediction}
                </p>
                <p><strong>Confidence:</strong> ${article.confidence}%</p>
                <a href="${article.url}" target="_blank">Read full article</a>
            `;

            latestNewsBox.appendChild(card);
        });

    } catch (error) {
        latestNewsBox.innerHTML = "<p class='error'>Error connecting to backend.</p>";
    }
}

document.getElementById("imageInput").addEventListener("change", function () {
    const file = this.files[0];
    const previewImage = document.getElementById("previewImage");

    if (file) {
        previewImage.src = URL.createObjectURL(file);
        previewImage.style.display = "block";
    }
});

function detectSourceFromText(text) {
    const sources = [
        "CNN",
        "BBC",
        "NBC",
        "NPR",
        "Reuters",
        "Associated Press",
        "AP News",
        "Al Jazeera",
        "Bloomberg",
        "The Wall Street Journal",
        "New York Times",
        "Fox News",
        "The Guardian",
        "Financial Times"
    ];

    const lowerText = text.toLowerCase();

    for (const source of sources) {
        if (lowerText.includes(source.toLowerCase())) {
            return source;
        }
    }

    return "Unknown source";
}

async function predictImageNews() {
    const imageInput = document.getElementById("imageInput");
    const imageResult = document.getElementById("imageResult");
    const extractedTextBox = document.getElementById("extractedTextBox");

    if (!imageInput.files || imageInput.files.length === 0) {
        imageResult.innerHTML = "Please upload an image first.";
        imageResult.style.color = "orange";
        return;
    }

    const imageFile = imageInput.files[0];

    imageResult.innerHTML = "Reading text from image...";
    imageResult.style.color = "blue";
    extractedTextBox.innerHTML = "";

    try {
        const ocrResult = await Tesseract.recognize(imageFile, "eng");
        const extractedText = ocrResult.data.text.trim();

        if (!extractedText) {
            imageResult.innerHTML = "No readable text found in the image.";
            imageResult.style.color = "red";
            return;
        }

        const detectedSource = detectSourceFromText(extractedText);

        extractedTextBox.innerHTML = `
            <h3>Extracted Text</h3>
            <p>${extractedText}</p>
            <p><strong>Detected Source:</strong> ${detectedSource}</p>
        `;

        imageResult.innerHTML = "Predicting image news text...";

        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: extractedText })
        });

        const data = await response.json();

        if (!response.ok) {
            imageResult.innerHTML = data.message || "Prediction failed.";
            imageResult.style.color = "red";
            return;
        }

        imageResult.innerHTML = `
            ${data.prediction}<br>
            Source: ${detectedSource}
        `;

        if (data.prediction.includes("Real")) {
            imageResult.style.color = "green";
        } else {
            imageResult.style.color = "red";
        }

    } catch (error) {
        imageResult.innerHTML = "Error reading or analyzing image.";
        imageResult.style.color = "red";
    }
}