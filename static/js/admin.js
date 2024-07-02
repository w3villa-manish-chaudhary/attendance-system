document.addEventListener('DOMContentLoaded', () => {
    const photosContainer = document.getElementById('photos-container');
    const userCardTemplate = document.getElementById('user-card-template').content;

    // Function to fetch user data
    async function fetchUserData() {
        try {
            const response = await fetch('http://localhost:8000/get_faces');
            const data = await response.json();
            displayUserData(data);
        } catch (error) {
            console.error('Error fetching user data:', error);
        }
    }

    // Function to display user data
    function displayUserData(users) {
        users.forEach(user => {
            const userCard = userCardTemplate.cloneNode(true);
            const userDiv = userCard.querySelector('.user-card');
            userDiv.dataset.userId = user.id;

            const username = userCard.querySelector('.username');
            username.textContent = user.username;

            const imagesDiv = userCard.querySelector('.images-container');
            
            // Display up to four images
            user.images.slice(0, 4).forEach(image => {
                const img = document.createElement('img');
                img.src = `data:image/jpeg;base64,${image.data}`;
                img.alt = image.filename;
                imagesDiv.appendChild(img);
            });

            const deleteButton = userCard.querySelector('.delete-button');
            deleteButton.addEventListener('click', () => {
                deleteUser(user.id, userDiv);
            });

            photosContainer.appendChild(userDiv);
        });
    }

    // Function to delete a user
    async function deleteUser(userId, userDiv) {
        try {
            const response = await fetch(`http://localhost:8000/delete_user/${userId}`, { method: 'DELETE' });
            if (response.ok) {
                userDiv.remove();
            } else {
                console.error('Error deleting user:', response.statusText);
            }
        } catch (error) {
            console.error('Error deleting user:', error);
        }
    }

    fetchUserData();
});
