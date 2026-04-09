document.addEventListener('DOMContentLoaded', async () => {

  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      const response = await fetch('http://127.0.0.1:5000/api/v1/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });

      if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = 'index.html';
      } else {
        alert('Login failed: ' + response.statusText);
      }
    });
  }

  const loginLink = document.getElementById("login-link");
  const token = getCookie("token");

  if (loginLink) {
    if (token) {
      loginLink.style.display = "none";
    } else {
      loginLink.style.display = "inline";
    }
  }

  const placesList = document.getElementById("places-list");

  if (placesList) {
    try {
      const places = await fetchPlaces();
      displayPlaces(places);
    } catch (error) {
      console.error(error);
    }
  }
});

function getCookie(name) {
  const cookies = document.cookie.split("; ");

  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].split("=");

    if (cookie[0] === name) {
      return cookie[1];
    }
  }

  return null;
}

async function fetchPlaces() {
  const token = getCookie("token");

  const headers = {
    "Content-Type": "application/json"
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch("http://127.0.0.1:5000/api/v1/places", {
    method: "GET",
    headers: headers
  });

  if (!response.ok) {
    throw new Error("Failed to fetch places");
  }

  const places = await response.json();
  return places;
}

function displayPlaces(places) {
  const placesList = document.getElementById("places-list");
  placesList.innerHTML = "";

  places.forEach((place) => {
    const placeCard = document.createElement("div");
    placeCard.className = "place-card";

    placeCard.innerHTML = `
      <h3>${place.title}</h3>
      <p>Price: ${place.price} $/night</p>
      <button class="details-button">View Details</button>
    `;

    placesList.appendChild(placeCard);
  });
}