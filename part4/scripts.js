const API_BASE_URL = "http://127.0.0.1:5000/api/v1";
let placesCache = [];

// Dark Mode Management
function initializeDarkMode() {
  const savedTheme = localStorage.getItem("theme") || "light";
  if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
  }
  
  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", toggleDarkMode);
    updateThemeToggleIcon();
  }
}

function toggleDarkMode() {
  document.body.classList.toggle("dark-mode");
  const isDarkMode = document.body.classList.contains("dark-mode");
  localStorage.setItem("theme", isDarkMode ? "dark" : "light");
  updateThemeToggleIcon();
}

function updateThemeToggleIcon() {
  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    const isDarkMode = document.body.classList.contains("dark-mode");
    themeToggle.textContent = isDarkMode ? "☀️" : "🌙";
  }
}

window.addEventListener("DOMContentLoaded", async () => {
  initializeDarkMode();
  const token = getCookie("token");
  const loginForm = document.getElementById("login-form");
  const logoutButton = document.getElementById("logout-button");

  updateNavigation(token);

  if (logoutButton) {
    logoutButton.addEventListener("click", () => {
      deleteCookie("token");
      window.location.reload();
    });
  }

  if (loginForm) {
    loginForm.addEventListener("submit", handleLoginSubmit);
  }

  if (document.getElementById("places-list")) {
    await initializePlaceList(token);
  }

  if (window.location.pathname.endsWith("place.html")) {
    const placeId = getPlaceIdFromURL();
    const addReviewSection = document.getElementById("add-review");

    if (addReviewSection) {
      addReviewSection.style.display = token ? "block" : "none";
    }

    if (placeId) {
      try {
        await fetchPlaceDetails(placeId, token);
      } catch (error) {
        console.error("Place details error:", error);
        showPlaceError("Unable to load place details.");
      }
    } else {
      showPlaceError("Invalid place ID.");
    }

    setupReviewForm(token, placeId);
  }

  if (window.location.pathname.endsWith("add_review.html")) {
    if (!token) {
      window.location.href = "login.html";
      return;
    }

    const placeId = getPlaceIdFromURL();
    if (!placeId) {
      const title = document.getElementById("place-name");
      if (title) title.textContent = "Place ID missing.";
      return;
    }

    try {
      const place = await fetchPlaceDetails(placeId, token, false);
      const placeName = document.getElementById("place-name");
      if (placeName) {
        placeName.textContent = `Reviewing: ${place.title || "Place"}`;
      }
    } catch (error) {
      console.error("Add review place error:", error);
      const placeName = document.getElementById("place-name");
      if (placeName) {
        placeName.textContent = "Unable to load place.";
      }
    }

    setupReviewForm(token, placeId);
  }
});

async function handleLoginSubmit(event) {
  event.preventDefault();
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const email = emailInput?.value.trim() || "";
  const password = passwordInput?.value.trim() || "";

  if (!email || !password) {
    alert("Email and password are required.");
    return;
  }

  try {
    const data = await loginUser(email, password);
    setCookie("token", data.access_token, 1);
    window.location.href = "index.html";
  } catch (error) {
    console.error("Login error:", error);
    alert(error.message || "Unable to connect to the server.");
  }
}

function updateNavigation(token) {
  const loginLink = document.getElementById("login-link");
  const logoutButton = document.getElementById("logout-button");

  if (token) {
    loginLink?.classList.add("hidden");
    logoutButton?.classList.remove("hidden");
  } else {
    loginLink?.classList.remove("hidden");
    logoutButton?.classList.add("hidden");
  }
}

async function initializePlaceList(token) {
  try {
    placesCache = await fetchPlaces(token);
    renderPlaces(placesCache);
    setupFilters();
  } catch (error) {
    console.error("Places error:", error);
    const placesList = document.getElementById("places-list");
    if (placesList) {
      placesList.innerHTML = "<p class='empty-state'>Unable to load places.</p>";
    }
  }
}

function setCookie(name, value, days) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; path=/; expires=${expires}`;
}

function deleteCookie(name) {
  document.cookie = `${name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT`;
}

function getCookie(name) {
  return document.cookie
    .split(";")
    .map((cookie) => cookie.trim())
    .find((cookie) => cookie.startsWith(`${name}=`))
    ?.split("=")[1] || null;
}

function getPlaceIdFromURL() {
  return new URLSearchParams(window.location.search).get("id");
}

function parseJwt(token) {
  try {
    const payload = token.split(".")[1];
    const base64 = payload.replace(/-/g, "+").replace(/_/g, "/");
    const decoded = decodeURIComponent(
      atob(base64)
        .split("")
        .map((char) => `%${("00" + char.charCodeAt(0).toString(16)).slice(-2)}`)
        .join("")
    );
    return JSON.parse(decoded);
  } catch (error) {
    console.error("JWT parse error:", error);
    return null;
  }
}

function getUserIdFromToken(token) {
  const payload = parseJwt(token);
  return payload?.sub || payload?.identity || null;
}

async function loginUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email, password })
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.error || "Login failed.");
  }
  return response.json();
}

async function fetchPlaces(token) {
  const headers = token ? { Authorization: `Bearer ${token}` } : {};
  const response = await fetch(`${API_BASE_URL}/places/`, { headers });
  if (!response.ok) {
    throw new Error("Failed to fetch places");
  }
  return response.json();
}

function renderPlaces(places) {
  const placesList = document.getElementById("places-list");
  if (!placesList) return;

  placesList.innerHTML = "";

  if (!places?.length) {
    placesList.innerHTML = "<p class='empty-state'>No places available.</p>";
    return;
  }

  places.forEach((place, index) => {
    const card = document.createElement("article");
    card.className = "place-card";
    card.dataset.price = place.price ?? place.price_per_night ?? 0;
    card.style.animation = `fadeIn 0.6s ease-out ${index * 0.05}s both`;

    const title = place.title || place.name || "Unnamed Place";
    const price = place.price ?? place.price_per_night ?? place.price_by_night ?? 0;
    const description = place.description || "No description available.";

    card.innerHTML = `
      <h3>${title}</h3>
      <div class="meta"><span>💰 ${price} $/night</span><span>🏠 ${place.id.substring(0, 8)}</span></div>
      <p>${description.substring(0, 120)}${description.length > 120 ? "..." : ""}</p>
      <button class="details-button">View Details →</button>
    `;

    card.querySelector(".details-button").addEventListener("click", () => {
      window.location.href = `place.html?id=${place.id}`;
    });

    placesList.appendChild(card);
  });
}

function setupFilters() {
  const priceFilter = document.getElementById("price-filter");
  const searchInput = document.getElementById("search-input");
  if (!priceFilter || !searchInput) return;

  const thresholds = ["all", 50, 100, 150, 200, 300, 500];
  priceFilter.innerHTML = thresholds
    .map((value) => {
      if (value === "all") return `<option value="all" selected>All Prices</option>`;
      return `<option value="${value}">Up to $${value}/night</option>`;
    })
    .join("");

  priceFilter.addEventListener("change", filterPlaces);
  searchInput.addEventListener("input", filterPlaces);
}

function filterPlaces() {
  const priceFilter = document.getElementById("price-filter");
  const searchInput = document.getElementById("search-input");
  const maxPrice = priceFilter?.value === "all" ? Infinity : Number(priceFilter.value);
  const searchTerm = searchInput?.value.trim().toLowerCase() || "";

  const filtered = placesCache.filter((place) => {
    const price = Number(place.price ?? place.price_per_night ?? place.price_by_night ?? 0);
    const matchesPrice = price <= maxPrice;
    const title = (place.title || "").toLowerCase();
    const description = (place.description || "").toLowerCase();
    const matchesSearch = title.includes(searchTerm) || description.includes(searchTerm);
    return matchesPrice && (!searchTerm || matchesSearch);
  });

  renderPlaces(filtered);
}

async function fetchPlaceDetails(placeId, token, render = true) {
  const headers = token ? { Authorization: `Bearer ${token}` } : {};
  const response = await fetch(`${API_BASE_URL}/places/${placeId}`, { headers });
  if (!response.ok) {
    throw new Error("Failed to fetch place details");
  }
  const place = await response.json();
  if (render) displayPlaceDetails(place);
  return place;
}

function displayPlaceDetails(place) {
  const placeDetails = document.getElementById("place-details");
  const reviewsSection = document.getElementById("reviews");

  if (placeDetails) {
    placeDetails.innerHTML = "";
    const container = document.createElement("div");
    container.className = "place-info";

    const title = place.title || place.name || "Unnamed Place";
    const price = place.price ?? place.price_per_night ?? place.price_by_night ?? "N/A";
    const description = place.description || "No description available.";
    const ownerName = place.owner ? `${place.owner.first_name || ""} ${place.owner.last_name || ""}`.trim() : "Unknown";

    container.innerHTML = `
      <h2>✨ ${title}</h2>
      <p><strong>🏠 Host:</strong> ${ownerName}</p>
      <p><strong>💰 Price:</strong> $${price}/night</p>
      <p><strong>📝 Description:</strong> ${description}</p>
    `;

    if (Array.isArray(place.amenities) && place.amenities.length) {
      const amenitiesTitle = document.createElement("h3");
      amenitiesTitle.textContent = "🎉 Amenities";
      const amenitiesList = document.createElement("ul");
      place.amenities.forEach((amenity) => {
        const item = document.createElement("li");
        item.textContent = amenity.name;
        amenitiesList.appendChild(item);
      });
      container.appendChild(amenitiesTitle);
      container.appendChild(amenitiesList);
    }

    placeDetails.appendChild(container);
  }

  if (reviewsSection) {
    reviewsSection.innerHTML = "";
    const reviewsTitle = document.createElement("h2");
    reviewsTitle.textContent = "⭐ Reviews";
    reviewsSection.appendChild(reviewsTitle);

    if (Array.isArray(place.reviews) && place.reviews.length) {
      place.reviews.forEach((review) => {
        const reviewCard = document.createElement("article");
        reviewCard.className = "review-card";
        const reviewer = review.user_name || review.user || review.user_id || "Anonymous";
        const stars = "⭐".repeat(review.rating);
        reviewCard.innerHTML = `
          <p><strong>👤 ${reviewer}</strong></p>
          <p class="rating">${stars}</p>
          <p>${review.text}</p>
        `;
        reviewsSection.appendChild(reviewCard);
      });
    } else {
      const noReviews = document.createElement("p");
      noReviews.textContent = "No reviews yet. Be the first to share your experience!";
      noReviews.style.textAlign = "center";
      noReviews.style.color = "#64748b";
      reviewsSection.appendChild(noReviews);
    }
  }
}

function showPlaceError(message) {
  const placeDetails = document.getElementById("place-details");
  const reviewsSection = document.getElementById("reviews");
  const addReviewSection = document.getElementById("add-review");
  if (placeDetails) placeDetails.innerHTML = `<p style="text-align:center;color:#ef4444;">${message}</p>`;
  if (reviewsSection) reviewsSection.innerHTML = "";
  if (addReviewSection) addReviewSection.style.display = "none";
}

function setupReviewForm(token, placeId) {
  const reviewForm = document.getElementById("review-form");
  if (!reviewForm) return;

  reviewForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!token) {
      window.location.href = "login.html";
      return;
    }
    if (!placeId) {
      alert("Place ID not found.");
      return;
    }

    const reviewText = document.getElementById("review-text")?.value.trim() || "";
    const rating = Number(document.getElementById("rating")?.value || 0);

    if (!reviewText || !rating) {
      alert("Please add a review and rating.");
      return;
    }

    const userId = getUserIdFromToken(token);
    if (!userId) {
      alert("Unable to identify user from token.");
      return;
    }

    try {
      const response = await submitReview(token, placeId, reviewText, rating, userId);
      if (response.ok) {
        alert("🎉 Review submitted successfully!");
        reviewForm.reset();
        window.location.reload();
      } else {
        const errorData = await response.json().catch(() => null);
        alert(errorData?.error || "Failed to submit review.");
      }
    } catch (error) {
      console.error("Review submit error:", error);
      alert("Failed to submit review.");
    }
  });
}

function submitReview(token, placeId, reviewText, rating, userId) {
  return fetch(`${API_BASE_URL}/reviews/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      text: reviewText,
      rating,
      user_id: userId,
      place_id: placeId
    })
  });
}
