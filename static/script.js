function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (!userInput.trim()) return;

    let chatBox = document.getElementById("chat-box");
    
    // Append user message
    let userMessage = document.createElement("div");
    userMessage.className = "message user";
    userMessage.innerText = userInput;
    chatBox.appendChild(userMessage);

    // Append bot response
    let botMessage = document.createElement("div");
    botMessage.className = "message bot";
    botMessage.innerHTML = "<em>Generating...</em>";
    chatBox.appendChild(botMessage);

    // Clear input field
    document.getElementById("user-input").value = "";

    // Send message to Flask backend
    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {

        // replace text in div
        botMessage.innerHTML = data.response;

        // Scroll chat to bottom
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => console.error("Error:", error));
}

function generatingResponse() {

}