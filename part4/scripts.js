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

    setupReviewForm(token, placeId);
  }

  // Optional support for add_review.html if you use it later
  if (window.location.pathname.includes("add_review.html")) {
    if (!token) {
      window.location.href = "index.html";
      return;
    }

    const params = new URLSearchParams(window.location.search);
    const placeId = params.get("id");
    setupReviewForm(token, placeId);
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

function parseJwt(token) {
  try {
    const payload = token.split(".")[1];
    const base64 = payload.replace(/-/g, "+").replace(/_/g, "/");
    const decoded = decodeURIComponent(
      atob(base64)
        .split("")
        .map((char) => "%" + ("00" + char.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );

    return JSON.parse(decoded);
  } catch (error) {
    console.error("JWT parse error:", error);
    return null;
  }
}

function getUserIdFromToken(token) {
  if (!token) {
    return null;
  }

  const payload = parseJwt(token);
  if (!payload) {
    return null;
  }

  // flask-jwt-extended غالبًا يخزن الهوية في sub
  return payload.sub || payload.identity || null;
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

    const price =
      place.price ??
      place.price_per_night ??
      place.price_by_night ??
      "N/A";

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
        const price =
          place.price ??
          place.price_per_night ??
          place.price_by_night ??
          0;

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
  const reviewsSection = document.getElementById("reviews");

  if (placeDetails) {
    placeDetails.innerHTML = "";

    const container = document.createElement("div");
    container.className = "place-info";

    const price =
      place.price ??
      place.price_per_night ??
      place.price_by_night ??
      "N/A";

    const description = place.description || "No description available";

    let ownerText = "Unknown";
    if (place.owner) {
      const firstName = place.owner.first_name || "";
      const lastName = place.owner.last_name || "";
      ownerText = `${firstName} ${lastName}`.trim() || "Unknown";
    }

    container.innerHTML = `
      <h2>${place.title}</h2>
      <p><strong>Host:</strong> ${ownerText}</p>
      <p><strong>Price:</strong> ${price} $/night</p>
      <p><strong>Description:</strong> ${description}</p>
    `;

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

    placeDetails.appendChild(container);
  }

  if (reviewsSection) {
    reviewsSection.innerHTML = "";

    if (place.reviews && place.reviews.length > 0) {
      const reviewsTitle = document.createElement("h3");
      reviewsTitle.textContent = "Reviews";
      reviewsSection.appendChild(reviewsTitle);

      place.reviews.forEach((review) => {
        const reviewCard = document.createElement("div");
        reviewCard.className = "review-card";

        reviewCard.innerHTML = `
          <p><strong>User:</strong> ${review.user_name || review.user || review.user_id || "Anonymous"}</p>
          <p><strong>Rating:</strong> ${review.rating}</p>
          <p>${review.text}</p>
        `;

        reviewsSection.appendChild(reviewCard);
      });
    }
  }
}

function setupReviewForm(token, placeId) {
  const reviewForm = document.getElementById("review-form");

  if (!reviewForm) {
    return;
  }

  reviewForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!token) {
      window.location.href = "index.html";
      return;
    }

    if (!placeId) {
      alert("Place ID not found");
      return;
    }

    const reviewTextElement = document.getElementById("review-text");
    const ratingElement = document.getElementById("rating");

    const reviewText = reviewTextElement ? reviewTextElement.value.trim() : "";
    const rating = ratingElement ? Number(ratingElement.value) : 5;

    if (!reviewText) {
      alert("Review text is required");
      return;
    }

    const userId = getUserIdFromToken(token);

    if (!userId) {
      alert("Unable to identify user from token");
      return;
    }

    try {
      const response = await submitReview(token, placeId, reviewText, rating, userId);

      if (response.ok) {
        alert("Review submitted successfully!");
        reviewForm.reset();

        if (window.location.pathname.includes("place.html")) {
          await fetchPlaceDetails(placeId, token);
        } else {
          window.location.href = `place.html?id=${placeId}`;
        }
      } else {
        const errorData = await response.json().catch(() => null);

        if (errorData && errorData.error) {
          alert(errorData.error);
        } else {
          alert("Failed to submit review");
        }
      }
    } catch (error) {
      console.error("Review submit error:", error);
      alert("Failed to submit review");
    }
  });
}

async function submitReview(token, placeId, reviewText, rating, userId) {
  return await fetch("http://127.0.0.1:5000/api/v1/reviews/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({
      text: reviewText,
      rating: rating,
      user_id: userId,
      place_id: placeId
    })
  });
}