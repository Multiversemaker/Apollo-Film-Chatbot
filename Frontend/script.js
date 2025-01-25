const backendUrl = "http://127.0.0.1:9001";
const country_mapping = {
    "amerika": "united states",
    "amerika serikat": "united states",
    "us": "united states",
    "inggris": "united kingdom",
    "jepang": "japan",
    "indonesia": "indonesia"
};
const genre_keywords = [
    "action", "comedy", "drama", "horror", "thriller", "romance",
    "sci-fi", "science fiction", "fantasy", "adventure", "animation"
];

// Display welcome message on page load
window.onload = function () {
    addMessage('Hi there! Welcome to the Movie Chatbot. How can I help you today?', 'bot');
};

function detectYear(message) {
    const yearMatch = message.match(/\b(19|20)\d{2}\b/); // Matches years from 1900 to 2099
    return yearMatch ? yearMatch[0] : null;
}

// Function to type out messages with a typing effect
function typeMessage(text, element) {
    let index = 0;
    element.innerHTML = '';

    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = text;
    const textContent = tempDiv.textContent;

    function type() {
        if (index < text.length) {
            element.innerHTML = text.substring(0, index + 1);
            index++;
            setTimeout(type, Math.random() * 30 + 20);
        }
    }
    type();
}

// Add typing animation (three dots)
function addTypingAnimation() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-animation';
    typingDiv.innerHTML = `
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    `;
    document.getElementById('messages').appendChild(typingDiv);
    return typingDiv;
}

// Remove typing animation
function removeTypingAnimation(element) {
    if (element && element.parentNode) {
        element.parentNode.removeChild(element);
    }
}

// Format movie details
function formatMovieDetails(movie) {
    const title = movie.title || 'Untitled';
    const origin = movie.origin || 'Unknown';
    const genres = movie.genres && movie.genres.length > 0
        ? `${movie.genres.join(', ')}`
        : 'unknown genre';
    const description = movie.description || 'No description available';
    const actors = movie.actors && movie.actors.length > 0
        ? `${movie.actors.join(', ')}`
        : 'unknown actors';

    return {
        text: `<p style="margin: 0 0 15px 0; line-height: 1.5;">
        <strong>${title}</strong> is a ${genres} film from ${origin}.
        The film stars ${actors}, with a plot about ${description}.
        </p>`,
        key: title.toLowerCase()
    };
}

// Main function to send a message and process the response
async function sendMessage() {
    const userMessage = document.getElementById('user-message').value.trim().toLowerCase();
    if (userMessage === '') {
        alert('Please enter a message!');
        return;
    }

    addMessage(userMessage, 'user');
    document.getElementById('user-message').value = '';

    const typingAnimation = addTypingAnimation();

    try {
        let searchTerm = userMessage;
        let searchType = 'general';
        let response;

        // 1. Check if it's a "recommendation" query based on IMDb rating
        if (userMessage.includes("rekomendasi") || userMessage.includes("rekomendasi film")) {
            response = await fetch(`${backendUrl}/recommend-movies?min_rating=7`);
            searchType = 'recommendation';
        } 
        else {
            // 2. Check if it's a country-based search
            const countryKeywords = ["negara", "dari", "asal", "buatan"];
            const isCountrySearch = countryKeywords.some(keyword => userMessage.includes(keyword));
            if (isCountrySearch) {
                const country = Object.keys(country_mapping).find(key => userMessage.includes(key));
                if (country) {
                    searchTerm = country_mapping[country];
                    searchType = 'country';
                }
            }

            // 3. Check if it's a genre-based search
            const genre = genre_keywords.find(genre => userMessage.includes(genre));
            if (genre) {
                searchTerm = genre;
                searchType = 'genre';
            }

            // 4. Check if it's a year-based search
            const year = detectYear(userMessage);
            if (year) {
                searchTerm = year;
                searchType = 'year';
            }

            // Send request to the backend
            response = await fetch(
                `${backendUrl}/movie-with-attribute?movie_attribute=${encodeURIComponent(searchTerm)}&search_type=${searchType}`
            );
        }

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        removeTypingAnimation(typingAnimation);

        if (data.length === 0 || data.message) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message bot';
            document.getElementById('messages').appendChild(messageDiv);
            const errorMessage = data.message || `Maaf, saya tidak menemukan film yang sesuai untuk '${searchTerm}'. Apakah ada pertanyaan lain?`;
            typeMessage(errorMessage, messageDiv);
        } else {
            const uniqueMovies = new Map();
            data.forEach(movie => {
                const formatted = formatMovieDetails(movie);
                if (!uniqueMovies.has(formatted.key)) {
                    uniqueMovies.set(formatted.key, formatted.text);
                }
            });

            let message = '';
            if (searchType === 'recommendation') {
                message = 'Berikut adalah beberapa rekomendasi film dengan rating IMDb tinggi:\n\n';
            } else if (searchType === 'country') {
                message = `Berikut film-film dari ${searchTerm}:\n\n`;
            } else if (searchType === 'genre') {
                message = `Berikut film-film dengan genre ${searchTerm}:\n\n`;
            } else if (searchType === 'year') {
                message = `Berikut film-film dari tahun ${searchTerm}:\n\n`;
            } else {
                message = 'Berikut informasi film yang Anda cari:\n\n';
            }
            message += Array.from(uniqueMovies.values()).join('');

            const messageDiv = document.createElement('div');
            messageDiv.className = 'message bot';
            document.getElementById('messages').appendChild(messageDiv);
            typeMessage(message + '\nAda yang ingin ditanyakan lagi?', messageDiv);
        }
    } catch (error) {
        console.error('Error:', error);
        removeTypingAnimation(typingAnimation);
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';
        document.getElementById('messages').appendChild(messageDiv);
        typeMessage('Maaf, terjadi kesalahan. Silakan coba lagi nanti.', messageDiv);
    }

    const messagesContainer = document.getElementById('messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Function to add a message to the chat window
function addMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.innerHTML = message;

    const messagesContainer = document.getElementById('messages');
    messagesContainer.appendChild(messageDiv);

    // Automatically scroll to the latest message
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}