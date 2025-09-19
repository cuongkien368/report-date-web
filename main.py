from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import datetime

app = FastAPI()

# Cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Định nghĩa model Order
class Order(BaseModel):
    order_id: int
    product: str
    quantity: int
    price: float
    datetime: datetime.datetime

# Dữ liệu mẫu
fake_data = [
    {"order_id": 1, "product": "Coconut", "quantity": 10, "price": 2.5, "datetime": datetime.datetime(2025, 9, 1, 10, 30)},
    {"order_id": 2, "product": "Taro", "quantity": 5, "price": 3.0, "datetime": datetime.datetime(2025, 9, 2, 14, 15)},
    {"order_id": 3, "product": "Coconut", "quantity": 20, "price": 2.5, "datetime": datetime.datetime(2025, 9, 3, 9, 0)},
]

@app.get("/orders", response_model=List[Order])
def get_orders():
    return fake_data
