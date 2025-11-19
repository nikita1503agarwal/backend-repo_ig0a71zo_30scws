"""
Database Schemas for Urban Bean Coffee Roasters

Each Pydantic model represents a collection. The collection name is the
lowercased class name (handled by helper utilities in this environment).
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class CoffeeProduct(BaseModel):
    title: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Tasting notes / details")
    origin: Optional[str] = Field(None, description="Country or region of origin")
    process: Optional[str] = Field(None, description="Washed / Natural / Honey / etc.")
    roast_level: Optional[str] = Field(None, description="Light / Medium / Dark")
    price: float = Field(..., ge=0, description="Price in USD")
    in_stock: bool = Field(True, description="Availability flag")
    image: Optional[HttpUrl] = Field(None, description="Product image URL")
    categories: List[str] = Field(default_factory=list, description="Tags/categories e.g. single-origin, blend")
    weight_grams: Optional[int] = Field(340, description="Bag weight in grams")

class Article(BaseModel):
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: str
    image: Optional[HttpUrl] = None
    category: Optional[str] = None

class OrderItem(BaseModel):
    product_id: str
    title: str
    quantity: int = Field(1, ge=1)
    price: float = Field(..., ge=0)

class Order(BaseModel):
    items: List[OrderItem]
    subtotal: float = Field(..., ge=0)
    email: str
    shipping_name: str
    shipping_address: str
    city: str
    state: str
    postal_code: str
    country: str
    status: str = Field("pending", description="Order status")
