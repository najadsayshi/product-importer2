from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from uuid import UUID

class ProductBase(BaseModel):
    sku: str
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    active: Optional[bool] = True

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    class Config:
        orm_mode = True

class WebhookIn(BaseModel):
    url: HttpUrl
    event_type: str
    enabled: Optional[bool] = True

class WebhookOut(WebhookIn):
    id: int
    class Config:
        orm_mode = True

class ImportJobOut(BaseModel):
    id: UUID
    filename: str
    total_rows: int
    processed_rows: int
    status: str
    class Config:
        orm_mode = True
