from pydantic import BaseModel
from typing import Optional, List, Dict

class QueryParams(BaseModel):
    q: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    limit: Optional[int] = 10
    offset: Optional[int] = 0

class FacetCounts(BaseModel):
    categories: Dict[str, int] = {}
    brands: Dict[str, int] = {}

class SearchResponse(BaseModel):
    total: int
    items: list
    facets: FacetCounts