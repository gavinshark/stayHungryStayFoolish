import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_root():
    """Test the root endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Architecture Smell Scanner"
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_health_check():
    """Test the health check endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_register_user():
    """Test user registration"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Clean up any existing user first
        await client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123"
        })
        
        # Try to register again (should fail)
        response = await client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "username": "testuser2",
            "password": "password123"
        })
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_login():
    """Test user login"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register a new user
        await client.post("/api/v1/auth/register", json={
            "email": "logintest@example.com",
            "username": "logintest",
            "password": "password123"
        })
        
        # Login
        response = await client.post("/api/v1/auth/login", json={
            "email": "logintest@example.com",
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_protected_route_without_token():
    """Test accessing protected route without token"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/projects/")
        assert response.status_code == 403  # Forbidden without token


@pytest.mark.asyncio
async def test_protected_route_with_token():
    """Test accessing protected route with token"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register and login
        await client.post("/api/v1/auth/register", json={
            "email": "protest@example.com",
            "username": "protest",
            "password": "password123"
        })
        
        login_response = await client.post("/api/v1/auth/login", json={
            "email": "protest@example.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        # Access protected route
        response = await client.get(
            "/api/v1/projects/",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200