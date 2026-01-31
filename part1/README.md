# HBnB Evolution – High-Level Package Diagram

## Architecture Overview

The HBnB application follows a **three-layer architecture**:

1. Presentation Layer  
2. Business Logic Layer  
3. Persistence Layer  

Communication between layers is handled through a **Facade pattern**, which provides a unified interface.

---

## High-Level Package Diagram

```mermaid
flowchart LR
  subgraph P[Presentation Layer (Services / API)]
    API[API Controllers / Routes]
  end

  subgraph F[Facade]
    FAC[HBnBFacade\n(Unified Interface)]
  end

  subgraph B[Business Logic Layer (Models / Core)]
    SVC[Services / Managers\n(User, Place, Review, Amenity)]
    DM[Domain Models\nUser, Place, Review, Amenity]
  end

  subgraph D[Persistence Layer (Storage)]
    REPO[Repositories / DAO]
    DB[(Database)]
  end

  API --> FAC
  FAC --> SVC
  SVC --> DM
  SVC --> REPO
  REPO --> DB

That’s three backticks to close the diagram block.

---

## 2️⃣ Add the explanation section (required)

Under the diagram, paste this:

```markdown
---

## Layer Responsibilities

### Presentation Layer
Handles user interaction through API endpoints. It receives requests and forwards them to the facade without containing business rules.

### Facade
Provides a unified interface (HBnBFacade) for all operations. It simplifies communication by preventing the Presentation Layer from directly interacting with multiple services.

### Business Logic Layer
Contains core models (User, Place, Review, Amenity) and application rules. Services manage operations such as creating places, registering users, and handling reviews.

### Persistence Layer
Responsible for storing and retrieving data. Repositories/DAO abstract database operations so that the business logic does not depend on database details.

---

## Data Flow

API Request → Facade → Business Services → Repositories → Database  
Response returns through the same path in reverse.
