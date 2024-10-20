document.getElementById("analyze-button").addEventListener("click", async () => {
    const textInput = document.getElementById("text-input").value;

    // Call the fake news detection endpoint
    const response = await fetch('http://localhost:8000/predict/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: textInput })
    });

    const prediction = await response.json();
    document.getElementById("prediction-result").innerText = `Prediction: ${prediction.label} (Score: ${prediction.score})`;

    // Call the Google Custom Search API
    const searchResponse = await fetch(`http://localhost:8000/search/?query=${encodeURIComponent(textInput)}`);
    const searchResults = await searchResponse.json();

    // Display search results

    const resultsContainer = document.getElementById("search-results");
    resultsContainer.innerHTML = "";  // Clear previous results

    if (Array.isArray(searchResults) && searchResults.length > 0) {
        searchResults.forEach(result => {
            const item = document.createElement("div");
            item.className = "search-item";
            item.innerHTML = `<h3><a href="${result.link}" target="_blank">${result.title}</a></h3><p>${result.snippet}</p>`;
            resultsContainer.appendChild(item);
        });
    } else {
        resultsContainer.innerHTML = "<p>No results found.</p>";
    }
});
document.getElementById("classify-button").addEventListener("click", async () => {
    const fileInput = document.getElementById("image-input");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an image to classify.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    // Call the classify-image endpoint
    const response = await fetch("http://localhost:8000/classify-image/", {
        method: "POST",
        body: formData,
    });

    const result = await response.json();
    const resultDiv = document.getElementById("classification-result");

    if (result.error) {
        resultDiv.innerText = `Error: ${result.error}`;
    } else {
        resultDiv.innerText = `Label: ${result.label} (Confidence: ${result.confidence}) - ${result.ai_generated}`;
    }
});
