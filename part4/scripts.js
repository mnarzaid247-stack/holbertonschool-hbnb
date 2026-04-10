document.addEventListener("DOMContentLoaded", async () => {
  const loginForm = document.getElementById("login-form");
  const loginLink = document.getElementById("login-link");
  const token = getCookie("token");

  // Login form handling
  if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
      event.preventDefault();

      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;

      try {
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
      } catch (error) {
        console.error("Login error:", error);
      }
    });
  }

  // Show/hide login link
  if (loginLink) {
    if (token) {
      loginLink.style.display = "none";
    } else {
      loginLink.style.display = "inline";
    }
  }

  // Index page: fetch and display places
  const placesList = document.getElementById("places-list");
  if (placesList) {
    try {
      const places = await fetchPlaces(token);
      displayPlaces(places);
      setupPriceFilter(places);
    } catch (error) {
      console.error("Places error:", error);
    }
  }

  // Place details page
  if (window.location.pathname.includes("place.html")) {
    const params = new URLSearchParams(window.location.search);
    const placeId = params.get("id");

    const addReviewSection = document.getElementById("add-review");
    if (addReviewSection) {
      if (token) {
        addReviewSection.style.display = "block";
      } else {
        addReviewSection.style.display = "none";
      }
    }

    if (placeId) {
      try {
        await fetchPlaceDetails(placeId, token);
      } catch (error) {
        console.error("Place details error:", error);
      }
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
  const headers = {};

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch("http://127.0.0.1:5000/api/v1/places/", {
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

    const price = place.price ?? place.price_per_night ?? "N/A";

    placeCard.innerHTML = `
      <h3>${place.title}</h3>
      <p>Price: ${price} $/night</p>
      <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">
        View Details
      </button>
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
      const filteredPlaces = places.filter((place) => {
        const price = place.price ?? place.price_per_night ?? 0;
        return price <= Number(selectedValue);
      });

      displayPlaces(filteredPlaces);
    }
  });
}

async function fetchPlaceDetails(placeId, token) {
  const headers = {};

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
    method: "GET",
    headers: headers
  });

  if (!response.ok) {
    throw new Error("Failed to fetch place details");
  }

  const place = await response.json();
  displayPlaceDetails(place);
}

function displayPlaceDetails(place) {
  const placeDetails = document.getElementById("place-details");

  if (!placeDetails) {
    return;
  }

  placeDetails.innerHTML = "";

  const container = document.createElement("div");
  const price = place.price ?? place.price_per_night ?? "N/A";
  const description = place.description || "No description available";

  container.innerHTML = `
    <h2>${place.title}</h2>
    <p><strong>Price:</strong> ${price} $/night</p>
    <p><strong>Description:</strong> ${description}</p>
  `;

  // Amenities
  if (place.amenities && place.amenities.length > 0) {
    const amenitiesTitle = document.createElement("h3");
    amenitiesTitle.textContent = "Amenities";
    container.appendChild(amenitiesTitle);

    const amenitiesList = document.createElement("ul");

    place.amenities.forEach((amenity) => {
      const li = document.createElement("li");
      li.textContent = amenity.name;
      amenitiesList.appendChild(li);
    });

    container.appendChild(amenitiesList);
  }

  // Reviews
  if (place.reviews && place.reviews.length > 0) {
    const reviewsTitle = document.createElement("h3");
    reviewsTitle.textContent = "Reviews";
    container.appendChild(reviewsTitle);

    place.reviews.forEach((review) => {
      const reviewCard = document.createElement("div");
      reviewCard.className = "review-card";

      reviewCard.innerHTML = `
        <p><strong>User:</strong> ${review.user_name || review.user || "Anonymous"}</p>
        <p><strong>Rating:</strong> ${review.rating}</p>
        <p>${review.text}</p>
      `;

      container.appendChild(reviewCard);
    });
  }

  placeDetails.appendChild(container);
}