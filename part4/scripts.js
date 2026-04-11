// Main entry point: runs after the page content has fully loaded
document.addEventListener("DOMContentLoaded", async () => {
  const loginForm = document.getElementById("login-form");
  const loginLink = document.getElementById("login-link");
  const token = getCookie("token");

  // Handle login form submission on login.html
  if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
      event.preventDefault();

      const emailInput = document.getElementById("email");
      const passwordInput = document.getElementById("password");

      const email = emailInput ? emailInput.value.trim() : "";
      const password = passwordInput ? passwordInput.value.trim() : "";

      // Validate inputs before sending the request
      if (!email || !password) {
        alert("Email and password are required.");
        return;
      }

      try {
        const data = await loginUser(email, password);

        // Save JWT token in cookies and redirect to the home page
        document.cookie = `token=${data.access_token}; path=/; max-age=3600`;
        window.location.href = "index.html";
      } catch (error) {
        console.error("Login error:", error);
        alert(error.message || "Unable to connect to the server.");
      }
    });
  }

  // Show login link only when the user is not authenticated
  if (loginLink) {
    loginLink.style.display = token ? "none" : "inline";
  }

  // Fetch and display places on the index page
  const placesList = document.getElementById("places-list");
  if (placesList) {
    try {
      const places = await fetchPlaces(token);
      displayPlaces(places);
      setupPriceFilter(places);
    } catch (error) {
      console.error("Places error:", error);
      placesList.innerHTML = "<p>Unable to load places.</p>";
    }
  }

  // Handle place details page
  if (window.location.pathname.includes("place.html")) {
    const placeId = getPlaceIdFromURL();
    const addReviewSection = document.getElementById("add-review");

    // Show add review form only for authenticated users
    if (addReviewSection) {
      addReviewSection.style.display = token ? "block" : "none";
    }

    // Load selected place details
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

    // Enable review form submission on place details page
    setupReviewForm(token, placeId);
  }

  // Optional support for add_review.html if used as a separate page
  if (window.location.pathname.includes("add_review.html")) {
    // Redirect unauthenticated users to index page
    if (!token) {
      window.location.href = "index.html";
      return;
    }

    const placeId = getPlaceIdFromURL();
    setupReviewForm(token, placeId);
  }
});

// Get a cookie value by its name
function getCookie(name) {
  const cookies = document.cookie.split("; ");

  for (let i = 0; i < cookies.length; i++) {
    const cookieParts = cookies[i].split("=");

    if (cookieParts[0] === name) {
      return cookieParts[1];
    }
  }

  return null;
}

// Extract place ID from the URL query string
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

// Decode JWT token payload
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

// Extract current user ID from JWT token
function getUserIdFromToken(token) {
  if (!token) {
    return null;
  }

  const payload = parseJwt(token);
  if (!payload) {
    return null;
  }

  return payload.sub || payload.identity || null;
}

// Send login request and return token data if successful
async function loginUser(email, password) {
  const response = await fetch("http://127.0.0.1:5000/api/v1/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email, password })
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);

    if (errorData && errorData.error) {
      throw new Error(errorData.error);
    }

    throw new Error("Login failed.");
  }

  return await response.json();
}

// Fetch all places from the backend API
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

// Display places dynamically on the index page
function displayPlaces(places) {
  const placesList = document.getElementById("places-list");

  if (!placesList) {
    return;
  }

  placesList.innerHTML = "";

  if (!places || places.length === 0) {
    placesList.innerHTML = "<p>No places available.</p>";
    return;
  }

  places.forEach((place) => {
    const placeCard = document.createElement("div");
    placeCard.className = "place-card";

    const title = place.title || place.name || "Unnamed Place";
    const price = place.price ?? place.price_per_night ?? place.price_by_night ?? "N/A";
    const description = place.description || "No description available.";

    const titleElement = document.createElement("h3");
    titleElement.textContent = title;

    const priceElement = document.createElement("p");
    priceElement.textContent = `Price: ${price} $/night`;

    const descriptionElement = document.createElement("p");
    descriptionElement.textContent = description;

    const detailsButton = document.createElement("button");
    detailsButton.className = "details-button";
    detailsButton.textContent = "View Details";
    detailsButton.addEventListener("click", () => {
      window.location.href = `place.html?id=${place.id}`;
    });

    placeCard.appendChild(titleElement);
    placeCard.appendChild(priceElement);
    placeCard.appendChild(descriptionElement);
    placeCard.appendChild(detailsButton);

    placesList.appendChild(placeCard);
  });
}

// Set up client-side filtering by maximum price
function setupPriceFilter(places) {
  const priceFilter = document.getElementById("price-filter");

  if (!priceFilter) {
    return;
  }

  // Load the required dropdown options
  priceFilter.innerHTML = `
    <option value="all" selected>All</option>
    <option value="10">10</option>
    <option value="50">50</option>
    <option value="100">100</option>
  `;

  // Filter places without reloading the page
  priceFilter.addEventListener("change", (event) => {
    const selectedValue = event.target.value;

    if (selectedValue === "all") {
      displayPlaces(places);
      return;
    }

    const filteredPlaces = places.filter((place) => {
      const price = place.price ?? place.price_per_night ?? place.price_by_night ?? 0;
      return Number(price) <= Number(selectedValue);
    });

    displayPlaces(filteredPlaces);
  });
}

// Fetch selected place details from the API
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

// Display selected place information and its reviews
function displayPlaceDetails(place) {
  const placeDetails = document.getElementById("place-details");
  const reviewsSection = document.getElementById("reviews");

  if (placeDetails) {
    placeDetails.innerHTML = "";

    const container = document.createElement("div");
    container.className = "place-info";

    const title = place.title || place.name || "Unnamed Place";
    const price = place.price ?? place.price_per_night ?? place.price_by_night ?? "N/A";
    const description = place.description || "No description available";

    let ownerText = "Unknown";
    if (place.owner) {
      const firstName = place.owner.first_name || "";
      const lastName = place.owner.last_name || "";
      ownerText = `${firstName} ${lastName}`.trim() || "Unknown";
    }

    const titleElement = document.createElement("h2");
    titleElement.textContent = title;

    const ownerElement = document.createElement("p");
    ownerElement.innerHTML = `<strong>Host:</strong> ${ownerText}`;

    const priceElement = document.createElement("p");
    priceElement.innerHTML = `<strong>Price:</strong> ${price} $/night`;

    const descriptionElement = document.createElement("p");
    descriptionElement.innerHTML = `<strong>Description:</strong> ${description}`;

    container.appendChild(titleElement);
    container.appendChild(ownerElement);
    container.appendChild(priceElement);
    container.appendChild(descriptionElement);

    if (place.amenities && place.amenities.length > 0) {
      const amenitiesTitle = document.createElement("h3");
      amenitiesTitle.textContent = "Amenities";
      container.appendChild(amenitiesTitle);

      const amenitiesList = document.createElement("ul");

      place.amenities.forEach((amenity) => {
        const item = document.createElement("li");
        item.textContent = amenity.name;
        amenitiesList.appendChild(item);
      });

      container.appendChild(amenitiesList);
    } else {
      const noAmenities = document.createElement("p");
      noAmenities.textContent = "No amenities available.";
      container.appendChild(noAmenities);
    }

    placeDetails.appendChild(container);
  }

  if (reviewsSection) {
    reviewsSection.innerHTML = "";

    const reviewsTitle = document.createElement("h3");
    reviewsTitle.textContent = "Reviews";
    reviewsSection.appendChild(reviewsTitle);

    if (place.reviews && place.reviews.length > 0) {
      place.reviews.forEach((review) => {
        const reviewCard = document.createElement("div");
        reviewCard.className = "review-card";

        const userName = review.user_name || review.user || review.user_id || "Anonymous";

        reviewCard.innerHTML = `
          <p><strong>User:</strong> ${userName}</p>
          <p><strong>Rating:</strong> ${review.rating}</p>
          <p>${review.text}</p>
        `;

        reviewsSection.appendChild(reviewCard);
      });
    } else {
      const noReviews = document.createElement("p");
      noReviews.textContent = "No reviews yet.";
      reviewsSection.appendChild(noReviews);
    }
  }
}

// Display an error message when place details cannot be loaded
function showPlaceError(message) {
  const placeDetails = document.getElementById("place-details");
  const reviewsSection = document.getElementById("reviews");
  const addReviewSection = document.getElementById("add-review");

  if (placeDetails) {
    placeDetails.innerHTML = `<p>${message}</p>`;
  }

  if (reviewsSection) {
    reviewsSection.innerHTML = "";
  }

  if (addReviewSection) {
    addReviewSection.style.display = "none";
  }
}

// Set up review form submission
function setupReviewForm(token, placeId) {
  const reviewForm = document.getElementById("review-form");

  if (!reviewForm) {
    return;
  }

  reviewForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    // Redirect user if not authenticated
    if (!token) {
      window.location.href = "index.html";
      return;
    }

    // Validate place ID
    if (!placeId) {
      alert("Place ID not found");
      return;
    }

    const reviewTextElement = document.getElementById("review-text");
    const ratingElement = document.getElementById("rating");

    const reviewText = reviewTextElement ? reviewTextElement.value.trim() : "";
    const rating = ratingElement ? Number(ratingElement.value) : 5;

    // Prevent empty review submission
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
        window.location.reload();
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

// Send the review data to the backend API
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