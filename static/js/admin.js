document.addEventListener('DOMContentLoaded', () => {
    const photosContainer = document.getElementById('photos-container');

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
            const userDiv = document.createElement('div');
            userDiv.classList.add('user-card');

            const username = document.createElement('h2');
            username.textContent = user.username;
            userDiv.appendChild(username);

            const imagesDiv = document.createElement('div');
            imagesDiv.classList.add('images-container');
            user.images.forEach(image => {
                const img = document.createElement('img');
                img.src = `/known_faces/${username}/${image}`;
                imagesDiv.appendChild(img);
            });
            userDiv.appendChild(imagesDiv);

            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.classList.add('delete-button');
            deleteButton.addEventListener('click', () => {
                deleteUser(user.id, userDiv);
            });
            userDiv.appendChild(deleteButton);

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



