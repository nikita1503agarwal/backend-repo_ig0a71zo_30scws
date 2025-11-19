import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import create_document, get_documents, db
from schemas import CoffeeProduct, Article, Order, OrderItem

app = FastAPI(title="Urban Bean Coffee Roasters API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Urban Bean Coffee Roasters API running"}

# Catalog endpoints
@app.get("/api/products", response_model=List[CoffeeProduct])
def list_products(category: Optional[str] = None):
    filt = {"in_stock": True}
    if category:
        filt["categories"] = {"$in": [category]}
    docs = get_documents("coffeeproduct", filt)
    # Map Mongo docs to schema-safe dicts
    return [CoffeeProduct(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.post("/api/products", response_model=str)
def create_product(product: CoffeeProduct):
    try:
        inserted_id = create_document("coffeeproduct", product)
        return inserted_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Articles
@app.get("/api/articles", response_model=List[Article])
def list_articles(category: Optional[str] = None):
    filt = {}
    if category:
        filt["category"] = category
    docs = get_documents("article", filt)
    return [Article(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.post("/api/articles", response_model=str)
def create_article(article: Article):
    try:
        return create_document("article", article)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Orders (simplified checkout capture)
@app.post("/api/orders", response_model=str)
def create_order(order: Order):
    try:
        return create_document("order", order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                response["collections"] = db.list_collection_names()[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
