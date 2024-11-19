window.api.receive('python-output', (data) => {
    addMessage('assistant', data);
    hideRecordingIndicator();
});

document.addEventListener('DOMContentLoaded', () => {
    const inputField = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const micButton = document.getElementById('mic-button');

    sendButton.addEventListener('click', () => {
        sendMessage();
    });

    micButton.addEventListener('click', () => {
        window.api.send('run-python-mic');
        showRecordingIndicator();
        showRecordingAnimation();
        showHologram();
        sshowHologram();
    });

    inputField.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});
// Function to show the recording animation
function showRecordingAnimation() {
    const animation = document.getElementById("recording-animation");
    animation.style.display = "block";
    
    // Hide animation after some time if needed
    setTimeout(() => {
        animation.style.display = "none";
    }, 5000); // Adjust duration as needed
}
function sshowHologram() {
    const hologram = document.getElementById("hologram-container");
    hologram.style.display = "block";
    
    // Hide the hologram after a while if needed
    setTimeout(() => {
        hologram.style.display = "none";
    }, 5000); // Adjust duration as needed
}

function sendMessage() {
    const inputField = document.getElementById('user-input');
    const message = inputField.value.trim();
    if (message) {
        addMessage('user', message);
        window.api.send('run-python', message);
        inputField.value = '';
    }
}

function addMessage(sender, message) {
    const chatWindow = document.getElementById('chat-window');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = message;
    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function showRecordingIndicator() {
    const indicator = document.getElementById('recording-indicator');
    indicator.style.display = 'flex';
}

function hideRecordingIndicator() {
    const indicator = document.getElementById('recording-indicator');
    indicator.style.display = 'none';
}
function showHologram() {
    const hologram = document.getElementById("hologram-container");
    hologram.style.display = "block";
    
    // Hide the hologram after a while if needed
    setTimeout(() => {
        hologram.style.display = "none";
    }, 5000); // Adjust duration as needed
}