from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis_om import HashModel
from redis import Redis

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = Redis(
    host="redis-11384.c212.ap-south-1-1.ec2.redns.redis-cloud.com",
    port=11384,
    password="5LzyQh1AKERfGYhCTy9Pq4vh4S2TL3us",
    decode_responses=True
)


# Separate Pydantic model for validation
class ProductSchema(BaseModel):
    name: str
    price: float
    quantity: int

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.get("/products/{pk}")
def get(pk: str):
    return Product.get(pk)

@app.post("/products")
def create(product: ProductSchema):
    new_product = Product(**product.dict())
    return new_product.save()

@app.delete("/products/{pk}")
def delete(pk: str):
    return Product.delete(pk)