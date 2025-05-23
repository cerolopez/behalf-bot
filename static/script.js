function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (!userInput.trim()) return;

    let chatBox = document.getElementById("chat-box");
    
    // Append user message
    let userMessage = document.createElement("div");
    userMessage.className = "message user";          // add classes
    let finalInput = `<p>${userInput}</p>`;          // wrap input in <p> to match output
    userMessage.innerHTML = finalInput;             // add wrapped input to new div
    chatBox.appendChild(userMessage);

    // Append bot response
    let botMessage = document.createElement("div");
    botMessage.className = "message bot";
    botMessage.innerHTML = "<p><em>Generating...</em></p>";
    chatBox.appendChild(botMessage);

    // Clear input field
    document.getElementById("user-input").value = "";

    // Send message to Flask backend
    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => {
        if (response.status === 429) {
            alert("Slow down! You've hit the request limit. Try again in a minute.")
            throw new Error("Too many requests");
        }
        return response.json()
    })
    .then(data => {

        // replace text in div
        botMessage.innerHTML = data.response;

        // Scroll chat to bottom
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => console.error("Error:", error));
}

function openPopup() {
    document.getElementById("popup").style.display = "block";
    document.getElementById("overlay").style.display = "block";
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
    document.getElementById("overlay").style.display = "none";
}

function sendIntro() {
    let chatBox = document.getElementById("chat-box");

    // Append bot response
    let botMessage = document.createElement("div");
    botMessage.className = "message bot";
    botMessage.innerHTML = "<p>Hi there! I'm Behalf Bot. What would you like to know about Cecilia's background?</p>";
    chatBox.appendChild(botMessage);
}