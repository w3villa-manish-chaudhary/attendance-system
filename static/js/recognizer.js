document.addEventListener('DOMContentLoaded', () => {
    const liveFeed = document.getElementById('live-feed');
    const faceTableBody = document.getElementById('face-table-body');

    const ws = new WebSocket('ws://localhost:8000/socket.io/');

    ws.onopen = () => {
        console.log('WebSocket connection established');
    };

    ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.type === 'face_recognition') {
            const faceId = message.face_id;
            const timestamp = new Date(message.timestamp * 1000).toLocaleString();

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${faceTableBody.children.length + 1}</td>
                <td>${faceId}</td>
                <td>${timestamp}</td>
            `;
            faceTableBody.appendChild(row);
        }
    };

    ws.onclose = () => {
        console.log('WebSocket connection closed');
    };

    liveFeed.onerror = () => {
        liveFeed.src = 'https://cdn.osxdaily.com/wp-content/uploads/2013/12/there-is-no-connected-camera-mac.jpg';
    };
});
