// static/script.js
const socket = io.connect('BoxStudios.pythonanywhere.com', { secure: true });

function sendMessage() {
    const messageInput = document.getElementById("message-input");
    const message = messageInput.value;

    if (message.trim() === "") {
        // Do not send empty messages
        return;
    }

    // Clear the input field
    messageInput.value = "";

    // Emit the message to the server using SocketIO
    socket.emit("message", { message });
}

socket.on("message", function(data) {
    // Update the chat box with the received message
    updateChatBox(data.message);
});

function updateChatBox(message) {
    const chatBox = document.getElementById("chat-box");

    // Create a new message element and append it to the chat box
    const messageElement = document.createElement("div");
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
}
