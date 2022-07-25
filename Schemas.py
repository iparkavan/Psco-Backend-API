from pydantic import BaseModel, validator


class Stg_Product(BaseModel):
    product: str
    corporate: str
    bu: str
    product_key: str
    sales: int
    segment: str = None

    @validator("segment")
    def replace_none(cls, v):
        return v or "None"

    class Config:
        orm_mode=True
