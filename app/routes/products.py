from fastapi import APIRouter, HTTPException, status, Depends
from pymongo import DESCENDING

from app.db import get_db
from app.dependencies import get_request_id
from app.models import ProductIn, ProductOut
from pymongo.errors import DuplicateKeyError

from app.schemas import SearchResponse


router = APIRouter(prefix="/products", tags=["products"])

def serialize(product):
    if not product:
        return None
    product["id"] = str(product.pop("_id"))
    return product

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductIn, request_id: str | None = Depends(get_request_id)):
    db = get_db()

    try:
        res = db.products.insert_one(payload.model_dump())
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product with this ID already exists."
        )
    
    created = db.products.find_one({"_id": res.inserted_id})
    return serialize(created)

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: str):
    product = get_db().products.find_one({"product_id": product_id})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    return serialize(product)

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: str, payload: ProductIn):
    db = get_db()
    result = db.products.update_one({"product_id": product_id}, {"$set": payload.model_dump()})
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    updated_product = db.products.find_one({"product_id": product_id})
    return serialize(updated_product)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str):
    db = get_db()
    result = db.products.delete_one({"product_id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    return {"detail": "Product deleted successfully."}  

@router.get("/search", response_model=SearchResponse)
def search_products(
    q: str | None = None,
    category: str | None = None,
    brand: str | None = None,
    price_min: float | None = None,
    price_max: float | None = None,
    limit: int = 10,
    offset: int = 0
):
    db = get_db()
    must_filters = []
    if q:
        must_filters.append({"$text": {"$search": q}})
    if category:
        must_filters.append({"category": category})
    if brand:
        must_filters.append({"brand": brand})

    price_filters = {}
    if price_min is not None:
        price_filters["$gte"] = price_min
    if price_max is not None:
        price_filters["$lte"] = price_max
    if price_filters:
        must_filters.append({"price": price_filters})

    match_stage = {"$and": must_filters} if must_filters else {}   

    pipeline = []

    if match_stage:
        pipeline.append({"$match": match_stage})

    pipeline.extend([
        {
            "$facet": {
                "items": [
                    {"$sort": {"_id": DESCENDING}},
                    {"$skip": offset},
                    {"$limit": limit},
                ],
                "total_count": [{"$count": "count"}],
                "cat_counts": [
                    {"$unwind": {"path": "$categories", "preserveNullAndEmptyArrays": True}},
                    {"$group": {"_id": "$brand", "count": {"$sum": 1}}},
                ],
                "brand_counts": [
                    {"$group": {"_id": "$brand", "count": {"$sum": 1}}},
                ]
            }
        }
        
        ])
    
    result = list(db.products.aggregate(pipeline))
    if not result:
        return SearchResponse(total=0, items=[], facets={"categories": {}, "brands": {}})

    doc = result[0]
    total_count = doc.get("total_count", [{}])[0].get("count", 0) if doc.get("total_count") else 0
    
    items = [serialize(item) for item in doc.get("items", [])]
    
    facets = FaceCounts(
        categories={d["_id"]: d["count"] for d in doc.get("cat_counts", []) if d.get("_id")},
        brands={d["_id"]: d["count"] for d in doc.get("brand_counts", []) if d.get("_id")}
    )
    
    for item in items:
        facets["categories"][item.get("category", "Unknown")] = facets["categories"].get(item.get("category", "Unknown"), 0) + 1
        facets["brands"][item.get("brand", "Unknown")] = facets["brands"].get(item.get("brand", "Unknown"), 0) + 1
    
    return SearchResponse(total=total_count, items=items, facets=facets).model_dump()