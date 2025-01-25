// Function to handle sending the user's message
function sendMessage() {
    const message = document.getElementById("user-input").value;
    const chatContainer = document.getElementsByClassName("chat-container");

    // Menambahkan pertanyaan user ke chat
    chatContainer.innerHTML += `<div>User: ${message}</div>`;

    // Mengirimkan permintaan ke server untuk mencari film
    fetch(`${backendUrl}/movie-with-attribute?movie_attribute=${encodeURIComponent(userMessage)}`, {
        method: "GET",
    })
        .then(response => response.json())
        .then(data => {
            console.log("Data received:", data); // Log data untuk memeriksa respons
            if (data && Array.isArray(data) && data.length > 0) {
                // Jika ada film yang ditemukan, tampilkan hasilnya
                const movie = data[0];
                chatContainer.innerHTML += `
                    <div>Bot: 
                        <strong>Title:</strong> ${movie.title}<br>
                        <strong>Description:</strong> ${movie.description}<br>
                        <strong>Origin:</strong> ${movie.origin}<br>
                        <strong>Actors:</strong> ${movie.actors.join(', ')}<br>
                        <strong>Genres:</strong> ${movie.genres.join(', ')}
                    </div>
                `;
            } else if (data.message) {
                // Jika tidak ada film ditemukan, tampilkan pesan kesalahan
                chatContainer.innerHTML += `<div>Bot: ${data.message}</div>`;
            } else {
                chatContainer.innerHTML += `<div>Bot: No movies found based on your search.</div>`;
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
            chatContainer.innerHTML += `<div>Bot: Sorry, something went wrong.</div>`;
        });
}


// Function to display messages in the chat box
function displayMessage(message, sender) {
    const chatBox = document.getElementById("chat-box");

    // Create a new div for the message
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(sender + "-message");

    const messageContent = document.createElement("span");
    messageContent.classList.add("message");
    messageContent.innerHTML = message;  // Use innerHTML to support HTML formatting (e.g., line breaks)

    messageDiv.appendChild(messageContent);
    chatBox.appendChild(messageDiv);

    // Scroll to the latest message
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to fetch movie data from the Flask API
async function fetchMovies(userInput) {
    try {
        const response = await fetch(`http://127.0.0.1:9001/movie-with-attribute?movie_attribute=${userInput}`);
        
        if (response.ok) {
            const data = await response.json();
            return formatMovieResponse(data);
        } else {
            return "Sorry, there was an error while fetching the movies.";
        }
    } catch (error) {
        return "Error: " + error.message;
    }
}

// Function to format the movie response from the API
function formatMovieResponse(data) {
    if (Array.isArray(data) && data.length > 0) {
        return data.map(movie => {
            return `
                <strong>${movie.title}</strong><br>
                <em>Origin:</em> ${movie.origin}<br>
                <em>Description:</em> ${movie.description}<br>
                <em>Actors:</em> ${movie.actors.join(", ")}<br>
                <em>Genres:</em> ${movie.genres.join(", ")}<br><br>
            `;
        }).join(""); // Join multiple messages into a single string
    } else {
        return "No movies found based on your search.";
    }
}
