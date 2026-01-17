"""Integration tests for Links CRUD endpoints"""

def test_get_links_list(client, sample_links):
    """Test GET /links returns list with correct count"""
    response = client.get("/links")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(sample_links)
    assert data[0]["imdbId"] == "tt0111161"

def test_get_link_by_id_existing(client, sample_links):
    """Test GET /links/{link_id} returns existing link"""
    link_id = sample_links[0].movieId
    response = client.get(f"/links/{link_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["movieId"] == link_id
    assert data["imdbId"] == "tt0111161"
    assert data["tmdbId"] == "278"

def test_get_link_by_id_not_found(client):
    """Test GET /links/{link_id} returns 404 for non-existing link"""
    response = client.get("/links/99999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Link not found"

def test_create_link(client, db_session):
    """Test POST /links creates new link"""
    new_link = {
        "movieId": 100,
        "imdbId": "tt1234567",
        "tmdbId": "999"
    }
    
    response = client.post("/links", json=new_link)
    
    assert response.status_code == 201
    data = response.json()
    assert data["movieId"] == 100
    assert data["imdbId"] == "tt1234567"
    
    # Verify link was added to database
    from db import Link
    link_in_db = db_session.query(Link).filter(Link.movieId == 100).first()
    assert link_in_db is not None
    assert link_in_db.imdbId == "tt1234567"

def test_update_link(client, sample_links, db_session):
    """Test PUT /links/{link_id} updates existing link"""
    link_id = sample_links[0].movieId
    updated_data = {
        "movieId": link_id,
        "imdbId": "tt9999999",
        "tmdbId": "111"
    }
    
    response = client.put(f"/links/{link_id}", json=updated_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["imdbId"] == "tt9999999"
    assert data["tmdbId"] == "111"
    
    # Verify link was updated in database
    from db import Link
    link_in_db = db_session.query(Link).filter(Link.movieId == link_id).first()
    assert link_in_db.imdbId == "tt9999999"

def test_update_link_not_found(client):
    """Test PUT /links/{link_id} returns 404 for non-existing link"""
    updated_data = {
        "movieId": 99999,
        "imdbId": "tt0000000",
        "tmdbId": "000"
    }
    
    response = client.put("/links/99999", json=updated_data)
    
    assert response.status_code == 404

def test_delete_link(client, sample_links, db_session):
    """Test DELETE /links/{link_id} removes link from database"""
    link_id = sample_links[0].movieId
    
    response = client.delete(f"/links/{link_id}")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Link deleted successfully"
    
    # Verify link was deleted from database
    from db import Link
    link_in_db = db_session.query(Link).filter(Link.movieId == link_id).first()
    assert link_in_db is None

def test_delete_link_not_found(client):
    """Test DELETE /links/{link_id} returns 404 for non-existing link"""
    response = client.delete("/links/99999")
    
    assert response.status_code == 404

"""Integration tests for Movies CRUD endpoints"""

def test_get_movies_list(client, sample_movies):
    """Test GET /movies returns list with correct count"""
    response = client.get("/movies")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(sample_movies)
    assert data[0]["title"] == "Test Movie 1"

def test_get_movie_by_id_existing(client, sample_movies):
    """Test GET /movies/{id} returns existing movie"""
    movie_id = sample_movies[0].movieId
    response = client.get(f"/movies/{movie_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["movieId"] == movie_id
    assert data["title"] == "Test Movie 1"
    assert data["genres"] == "Action|Comedy"

def test_get_movie_by_id_not_found(client):
    """Test GET /movies/{id} returns 404 for non-existing movie"""
    response = client.get("/movies/99999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"

def test_create_movie(client, db_session):
    """Test POST /movies creates new movie"""
    new_movie = {
        "movieId": 100,
        "title": "New Test Movie",
        "genres": "Comedy|Romance"
    }
    
    response = client.post("/movies", json=new_movie)
    
    assert response.status_code == 201
    data = response.json()
    assert data["movieId"] == 100
    assert data["title"] == "New Test Movie"
    
    # Verify movie was added to database
    from db import Movie
    movie_in_db = db_session.query(Movie).filter(Movie.movieId == 100).first()
    assert movie_in_db is not None
    assert movie_in_db.title == "New Test Movie"

def test_update_movie(client, sample_movies, db_session):
    """Test PUT /movies/{id} updates existing movie"""
    movie_id = sample_movies[0].movieId
    updated_data = {
        "movieId": movie_id,
        "title": "Updated Movie Title",
        "genres": "Sci-Fi|Action"
    }
    
    response = client.put(f"/movies/{movie_id}", json=updated_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Movie Title"
    assert data["genres"] == "Sci-Fi|Action"
    
    # Verify movie was updated in database
    from db import Movie
    movie_in_db = db_session.query(Movie).filter(Movie.movieId == movie_id).first()
    assert movie_in_db.title == "Updated Movie Title"

def test_update_movie_not_found(client):
    """Test PUT /movies/{id} returns 404 for non-existing movie"""
    updated_data = {
        "movieId": 99999,
        "title": "This won't work",
        "genres": "Drama"
    }
    
    response = client.put("/movies/99999", json=updated_data)
    
    assert response.status_code == 404

def test_delete_movie(client, sample_movies, db_session):
    """Test DELETE /movies/{id} removes movie from database"""
    movie_id = sample_movies[0].movieId
    
    response = client.delete(f"/movies/{movie_id}")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Movie deleted successfully"
    
    # Verify movie was deleted from database
    from db import Movie
    movie_in_db = db_session.query(Movie).filter(Movie.movieId == movie_id).first()
    assert movie_in_db is None

def test_delete_movie_not_found(client):
    """Test DELETE /movies/{id} returns 404 for non-existing movie"""
    response = client.delete("/movies/99999")
    
    assert response.status_code == 404

def test_get_ratings_list(client, sample_ratings):
    """Test GET /ratings returns list with correct count"""
    response = client.get("/ratings")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(sample_ratings)
    assert data[0]["rating"] == 5.0

def test_get_rating_by_id_existing(client, sample_ratings):
    """Test GET /ratings/{id} returns existing rating"""
    rating_id = sample_ratings[0].id
    response = client.get(f"/ratings/{rating_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["userId"] == 1
    assert data["movieId"] == 1
    assert data["rating"] == 5.0

def test_get_rating_by_id_not_found(client):
    """Test GET /ratings/{id} returns 404 for non-existing rating"""
    response = client.get("/ratings/99999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Rating not found"

def test_create_rating(client, db_session):
    """Test POST /ratings creates new rating"""
    new_rating = {
        "userId": 5,
        "movieId": 10,
        "rating": 4.5,
        "timestamp": 1234567999
    }
    
    response = client.post("/ratings", json=new_rating)
    
    assert response.status_code == 201
    data = response.json()
    assert data["userId"] == 5
    assert data["movieId"] == 10
    assert data["rating"] == 4.5
    
    # Verify rating was added to database
    from db import Rating
    rating_in_db = db_session.query(Rating).filter(
        Rating.userId == 5, 
        Rating.movieId == 10
    ).first()
    assert rating_in_db is not None
    assert rating_in_db.rating == 4.5

def test_update_rating(client, sample_ratings, db_session):
    """Test PUT /ratings/{id} updates existing rating"""
    rating_id = sample_ratings[0].id
    updated_data = {
        "userId": 1,
        "movieId": 1,
        "rating": 3.5,
        "timestamp": 9999999999
    }
    
    response = client.put(f"/ratings/{rating_id}", json=updated_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 3.5
    assert data["timestamp"] == 9999999999
    
    # Verify rating was updated in database
    from db import Rating
    rating_in_db = db_session.query(Rating).filter(Rating.id == rating_id).first()
    assert rating_in_db.rating == 3.5

def test_update_rating_not_found(client):
    """Test PUT /ratings/{id} returns 404 for non-existing rating"""
    updated_data = {
        "userId": 99,
        "movieId": 99,
        "rating": 1.0,
        "timestamp": 0
    }
    
    response = client.put("/ratings/99999", json=updated_data)
    
    assert response.status_code == 404

def test_delete_rating(client, sample_ratings, db_session):
    """Test DELETE /ratings/{id} removes rating from database"""
    rating_id = sample_ratings[0].id
    
    response = client.delete(f"/ratings/{rating_id}")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Rating deleted successfully"
    
    # Verify rating was deleted from database
    from db import Rating
    rating_in_db = db_session.query(Rating).filter(Rating.id == rating_id).first()
    assert rating_in_db is None

def test_delete_rating_not_found(client):
    """Test DELETE /ratings/{id} returns 404 for non-existing rating"""
    response = client.delete("/ratings/99999")
    
    assert response.status_code == 404

def test_get_tags_list(client, sample_tags):
    """Test GET /tags returns list with correct count"""
    response = client.get("/tags")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(sample_tags)
    assert data[0]["tag"] == "awesome"

def test_get_tag_by_id_existing(client, sample_tags):
    """Test GET /tags/{id} returns existing tag"""
    tag_id = sample_tags[0].id
    response = client.get(f"/tags/{id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["userId"] == 1
    assert data["movieId"] == 1
    assert data["tag"] == "awesome"

def test_get_tag_by_id_not_found(client):
    """Test GET /tags/{id} returns 404 for non-existing tag"""
    response = client.get("/tags/99999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Tag not found"

def test_create_tag(client, db_session):
    """Test POST /tags creates new tag"""
    new_tag = {
        "userId": 5,
        "movieId": 10,
        "tag": "amazing",
        "timestamp": 1234567999
    }
    
    response = client.post("/tags", json=new_tag)
    
    assert response.status_code == 201
    data = response.json()
    assert data["userId"] == 5
    assert data["movieId"] == 10
    assert data["tag"] == "amazing"
    
    # Verify tag was added to database
    from db import Tag
    tag_in_db = db_session.query(Tag).filter(
        Tag.userId == 5, 
        Tag.movieId == 10,
        Tag.tag == "amazing"
    ).first()
    assert tag_in_db is not None
    assert tag_in_db.tag == "amazing"

def test_update_tag(client, sample_tags, db_session):
    """Test PUT /tags/{id} updates existing tag"""
    tag_id = sample_tags[0].id
    updated_data = {
        "userId": 1,
        "movieId": 1,
        "tag": "updated tag",
        "timestamp": 9999999999
    }
    
    response = client.put(f"/tags/{tag_id}", json=updated_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["tag"] == "updated tag"
    assert data["timestamp"] == 9999999999
    
    # Verify tag was updated in database
    from db import Tag
    tag_in_db = db_session.query(Tag).filter(Tag.id == tag_id).first()
    assert tag_in_db.tag == "updated tag"

def test_update_tag_not_found(client):
    """Test PUT /tags/{id} returns 404 for non-existing tag"""
    updated_data = {
        "userId": 99,
        "movieId": 99,
        "tag": "nonexistent",
        "timestamp": 0
    }
    
    response = client.put("/tags/99999", json=updated_data)
    
    assert response.status_code == 404

def test_delete_tag(client, sample_tags, db_session):
    """Test DELETE /tags/{id} removes tag from database"""
    tag_id = sample_tags[0].id
    
    response = client.delete(f"/tags/{tag_id}")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Tag deleted successfully"
    
    # Verify tag was deleted from database
    from db import Tag
    tag_in_db = db_session.query(Tag).filter(Tag.id == tag_id).first()
    assert tag_in_db is None

def test_delete_tag_not_found(client):
    """Test DELETE /tags/{id} returns 404 for non-existing tag"""
    response = client.delete("/tags/99999")
    
    assert response.status_code == 404

def test_login_success(client, sample_user):
    """Test successful login with valid credentials"""
    response = client.post("/login", json={
        "username": "testuser",
        "password": "testpass123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


def test_login_invalid_username(client, sample_user):
    """Test login with non-existent username"""
    response = client.post("/login", json={
        "username": "nonexistent",
        "password": "testpass123"
    })
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_invalid_password(client, sample_user):
    """Test login with wrong password"""
    response = client.post("/login", json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_missing_fields(client):
    """Test login with missing fields"""
    response = client.post("/login", json={
        "username": "testuser"
    })
    
    assert response.status_code == 422  # Validation error


# ==================== USER CREATION TESTS ====================

def test_create_user_without_token(client):
    """Test creating a regular user without authentication (should succeed)"""
    response = client.post("/users", 
        json={
            "username": "newuser",
            "password": "newpass123",
            "roles": ["ROLE_USER"]
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["roles"] == ["ROLE_USER"]
    assert "password" not in data
    assert "password_hash" not in data


def test_create_admin_without_token(client):
    """Test creating admin user without authentication (should fail)"""
    response = client.post("/users",
        json={
            "username": "newadmin",
            "password": "adminpass123",
            "roles": ["ROLE_USER", "ROLE_ADMIN"]
        }
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Authorization required to create admin user"


def test_create_admin_as_non_admin(client, auth_token):
    """Test creating admin user as non-admin (should fail)"""
    response = client.post("/users",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "username": "newadmin",
            "password": "adminpass123",
            "roles": ["ROLE_USER", "ROLE_ADMIN"]
        }
    )
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required to create admin user"


def test_create_user_duplicate_username(client, sample_user):
    """Test creating a user with existing username"""
    response = client.post("/users",
        json={
            "username": "testuser",  # Already exists
            "password": "newpass123",
            "roles": ["ROLE_USER"]
        }
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"


def test_create_admin_user(client, admin_token):
    """Test creating a new admin user"""
    response = client.post("/users",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "username": "newadmin",
            "password": "adminpass",
            "roles": ["ROLE_USER", "ROLE_ADMIN"]
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newadmin"
    assert "ROLE_ADMIN" in data["roles"]

def test_get_user_details_with_token(client, auth_token, sample_user):
    """Test getting user details with valid token"""
    response = client.get("/user_details",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["user_id"] == sample_user.id
    assert data["roles"] == ["ROLE_USER"]
    assert "token_issued_at" in data
    assert "token_expires_at" in data


def test_get_user_details_without_token(client):
    """Test getting user details without token"""
    response = client.get("/user_details")
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Authorization header missing"


def test_get_user_details_invalid_token(client):
    """Test getting user details with invalid token"""
    response = client.get("/user_details",
        headers={"Authorization": "Bearer invalid_token_here"}
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def test_get_user_details_malformed_header(client):
    """Test getting user details with malformed authorization header"""
    response = client.get("/user_details",
        headers={"Authorization": "InvalidFormat"}
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authorization header format"


def test_admin_user_details(client, admin_token, sample_admin):
    """Test getting admin user details"""
    response = client.get("/user_details",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "adminuser"
    assert "ROLE_ADMIN" in data["roles"]