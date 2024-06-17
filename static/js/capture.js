document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const nameInput = document.getElementById('name');
    const captureButton = document.getElementById('capture-button');
    const imagesContainer = document.getElementById('images-container');
    const confirmButton = document.getElementById('confirm-button');
    const resetButton = document.getElementById('reset-button');
    const status = document.getElementById('status');
    let images = [];

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            console.error("Error accessing the webcam: ", err);
            status.textContent = "Failed to access webcam.";
        });

    captureButton.addEventListener('click', () => {
        if (!nameInput.value) {
            status.textContent = 'Please enter your name before capturing an image.';
            return;
        }
        if (images.length < 4) {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            const newImage = canvas.toDataURL('image/jpeg');
            images.push(newImage);
            const imgElement = document.createElement('img');
            imgElement.src = newImage;
            imgElement.classList.add('captured-image');
            imagesContainer.appendChild(imgElement);
            if (images.length === 4) {
                confirmButton.style.display = 'block';
                resetButton.style.display = 'block';
            }
        }
    });

    confirmButton.addEventListener('click', () => {
        if (!nameInput.value) {
            status.textContent = 'Please enter a name.';
            return;
        }
        status.textContent = 'Sending images...';
        fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ images, username: nameInput.value })
        })
        .then(response => response.json())
        .then(data => {
            status.textContent = `Images sent! Response: ${data.message}`;
            images = [];
            imagesContainer.innerHTML = '';
            confirmButton.style.display = 'none';
            resetButton.style.display = 'none';
        })
        .catch(error => {
            status.textContent = `Error sending images: ${error.message}`;
            console.error('Error sending images:', error);
        });
    });

    resetButton.addEventListener('click', () => {
        images = [];
        imagesContainer.innerHTML = '';
        confirmButton.style.display = 'none';
        resetButton.style.display = 'none';
        status.textContent = '';
    });
});
