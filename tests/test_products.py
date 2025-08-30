import os
import requests

BASE = os.getenv("BASE_URL", "http://localhost:8000")

def test_healthz():
    response = requests.get(f"{BASE}/healthz")
    assert response.status_code == 200
    #assert response.json() == {"status": "ok"}  

def test_create_product():
    payload = {
        "product_id": "TEST-ABC",
        "name": "Test Item",
        "description": "A sample product for testing",
        "price": 10.5,
        "currency": "USD",
        "category": "electronics",   # must be one of ProductType
        "tags": ["ci", "test"],
        "variants": [
            {
                "sku": "TEST-ABC-001",
                "price": 10.5,
                "stock": 100,
                "size": "M",
                "color": "red"
            }
        ],
        "attributes": {"material": "cotton", "origin": "USA"},
        "product_type": "electronics",
        "active": True
    }
    response = requests.post(f"{BASE}/products", json=payload,
                              headers={"X-Request-ID": "test-123"} )
    print("STATUS:", response.status_code)
    
    try:
        print("RESPONSE text/json:", response.json())
    except ValueError:
        print("Non-JSON response:", response.text)
       
    assert response.status_code in [200, 201, 409]
    assert response.json()["product_id"] == payload["product_id"]

    response2 = requests.get(f"{BASE}/products/{payload['product_id']}")
    assert response2.status_code == 200
    assert response2.json()["product_id"] == payload["product_id"]