function sendBothMessages() {
    let userInput = document.getElementById("user-input").value;
    if (!userInput.trim()) return;

    let claudeBox = document.getElementById("claude-box");
    // Append user message for Claude
    let userMessage1 = document.createElement("div");
    userMessage1.className = "message user";          // add classes
    let finalInput1 = `<p>${userInput}</p>`;          // wrap input in <p> to match output
    userMessage1.innerHTML = finalInput1;             // add wrapped input to new div
    claudeBox.appendChild(userMessage1);

    // Append bot response for Claude
    let botMessage1 = document.createElement("div");
    botMessage1.className = "message bot";
    botMessage1.innerHTML = "<p><em>Generating...</em></p>";
    claudeBox.appendChild(botMessage1);

    // Send message to Flask backend
    fetch("/chatClaude", {
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
        botMessage1.innerHTML = data.response;

        // Scroll chat to bottom
        claudeBox.scrollTop = claudeBox.scrollHeight;
    })
    .catch(error => console.error("Error:", error));

    let gptBox = document.getElementById("gpt-box");
    // Append user message for GPT-4
    let userMessage2 = document.createElement("div");
    userMessage2.className = "message user";          // add classes
    let finalInput2 = `<p>${userInput}</p>`;          // wrap input in <p> to match output
    userMessage2.innerHTML = finalInput2;             // add wrapped input to new div
    gptBox.appendChild(userMessage2);

    // Append bot response for GPT-4
    let botMessage2 = document.createElement("div");
    botMessage2.className = "message bot";
    botMessage2.innerHTML = "<p><em>Generating...</em></p>";
    gptBox.appendChild(botMessage2);

    fetch("/chatGPT", {
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
        botMessage2.innerHTML = data.response;

        // Scroll chat to bottom
        gptBox.scrollTop = gptBox.scrollHeight;
    })
    .catch(error => console.error("Error:", error));

    // Clear input field
    document.getElementById("user-input").value = "";
}