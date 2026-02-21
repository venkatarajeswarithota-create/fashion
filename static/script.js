async function generateOutfit() {

    const data = {
        gender: document.getElementById("gender").value,
        occasion: document.getElementById("occasion").value,
        season: document.getElementById("season").value,
        preferred_colors: document.getElementById("colors").value,
        budget: document.getElementById("budget").value
    };

    const response = await fetch("/generate-outfit", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await response.json();
    document.getElementById("outfitResult").innerText = result.result;
}


async function chat() {

    const message = document.getElementById("chatInput").value;

    const response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message})
    });

    const result = await response.json();
    document.getElementById("chatResult").innerText = result.reply;
}


async function analyzeImage() {

    const fileInput = document.getElementById("imageInput");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch("/analyze-image", {
        method: "POST",
        body: formData
    });

    const result = await response.json();
    document.getElementById("imageResult").innerText = result.analysis;
}