document.addEventListener("DOMContentLoaded", async () => {
  const loginForm = document.getElementById("login-form");

  if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
      event.preventDefault();

      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;

      const response = await fetch("http://127.0.0.1:5000/api/v1/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
      });

      if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = "index.html";
      } else {
        alert("Login failed: " + response.statusText);
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
      const places = await fetchPlaces(token);
      displayPlaces(places);
      setupPriceFilter(places);
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

async function fetchPlaces(token) {
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

  return await response.json();
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
      <button onclick="window.location.href='place.html?id=${place.id}'" class="details-button">View Details</button>
    `;

    placesList.appendChild(placeCard);
  });
}

function setupPriceFilter(places) {
  const priceFilter = document.getElementById("price-filter");

  if (!priceFilter) {
    return;
  }

  priceFilter.innerHTML = `
    <option value="10">10</option>
    <option value="50">50</option>
    <option value="100">100</option>
    <option value="all" selected>All</option>
  `;

  priceFilter.addEventListener("change", (event) => {
    const selectedValue = event.target.value;

    if (selectedValue === "all") {
      displayPlaces(places);
    } else {
      const filteredPlaces = places.filter((place) => place.price <= Number(selectedValue));
      displayPlaces(filteredPlaces);
    }
  });
}
document.addEventListener("DOMContentLoaded", () => {
  if (window.location.pathname.includes("place.html")) {
    
    const params = new URLSearchParams(window.location.search);
    const placeId = params.get("id");

    console.log("Place ID:", placeId);

    const token = getCookie("token");

    if (token) {
      console.log("User logged in");
    } else {
      console.log("Not logged in");
    }

  }
});
if (placeId) {
  fetchPlaceDetails(placeId, token);
}
async function fetchPlaceDetails(placeId, token) {
  const headers = {
    "Content-Type": "application/json"
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
    method: "GET",
    headers: headers
  });

  if (!response.ok) {
    console.error("Failed to fetch place details");
    return;
  }

  const place = await response.json();
  console.log(place);
}