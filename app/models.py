from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, conlist, PositiveFloat

class Variant(BaseModel):
    sku: str = Field(..., min_length=1, max_length=100)
    price: PositiveFloat = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    size: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=50)


class ProductType(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    HOME = "home"
    BOOKS = "books"
    TOYS = "toys"

class ProductIn(BaseModel):
    product_id:str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: PositiveFloat = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    category: ProductType
    tags: conlist(str, min_length=0)
    variants: Optional[List[Variant]] = Field(None, max_length=100)
    attributes: Dict[str, str] = {}
    product_type: ProductType = ProductType.ELECTRONICS
    active: bool = True

class ProductOut(ProductIn):
    id: str
