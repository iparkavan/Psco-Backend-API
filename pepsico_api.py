from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from Models import Stg_Product, Stg_SalesProduct, Base, Stg_Geography, Stg_Time
import Schemas
from database import SessionLocal, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/getdata/{product_term}")
async def root(product_term: str, db: Session = Depends(get_db)):
    data = []

    products = db.query(func.sum(Stg_Product.sales).label("sales_sum")).filter(Stg_Product.bu == product_term).all()
    products_segment = db.query(Stg_Product.segment).filter(Stg_Product.bu == product_term, Stg_Product.segment != None).group_by(Stg_Product.segment).all()

    sales_products = db.query(func.sum(Stg_Product.sales).label("sales_sum"),
        func.sum(Stg_SalesProduct.sales_chg).label("sales_mean"),
                              func.sum(Stg_SalesProduct.sales_share).label("sales_share"),
                              func.sum(Stg_SalesProduct.sales_share_change_vs_ya).label("share_chg"),
                              func.sum(Stg_SalesProduct.volume_chg).label("volume_mean"),
                              func.sum(Stg_SalesProduct.unit_chg).label("unit_mean"),
                              ).join(Stg_Product).all()

    data.append({
        "items": [],
        "name": product_term,
        "sales_sum": sales_products[0].sales_sum,
        "sales_mean": sales_products[0].sales_mean,
        "sales_share": sales_products[0].sales_share,
        "share_chg": sales_products[0].share_chg,
        "volume_mean": sales_products[0].volume_mean,
        "unit_mean": sales_products[0].unit_mean,
    })

    for i in range(len(products_segment)):
        if products_segment[i].segment != 'null':
            sales_products = db.query(func.sum(Stg_SalesProduct.sales).label("sales_sum"),
                                      func.sum(Stg_SalesProduct.sales_chg).label("sales_mean"),
                                      func.sum(Stg_SalesProduct.sales_share).label("sales_share"),
                                      func.sum(Stg_SalesProduct.sales_share_change_vs_ya).label("share_chg"),
                                      func.sum(Stg_SalesProduct.volume_chg).label("volume_mean"),
                                      func.sum(Stg_SalesProduct.unit_chg).label("unit_mean"),
                                      ).join(Stg_Product).filter(Stg_Product.segment == products_segment[i].segment).all()

            data[0]['items'].append({
                "items": [],
                "name": products_segment[i].segment,
                "sales_sum": sales_products[0].sales_sum,
                "sales_mean": sales_products[0].sales_mean,
                "sales_share": sales_products[0].sales_share,
                "share_chg": sales_products[0].share_chg,
                "volume_mean": sales_products[0].volume_mean,
                "unit_mean": sales_products[0].unit_mean,
            })


        products_category = db.query(Stg_Product.category).filter(Stg_Product.segment == products_segment[i].segment, Stg_Product.category != None).group_by(Stg_Product.category).all()

        for j in range(len(products_category)):
            sales_details = db.query(func.sum(Stg_SalesProduct.sales).label("sales_sum"),
                func.sum(Stg_SalesProduct.sales_chg).label("sales_mean"),
                                      func.sum(Stg_SalesProduct.sales_share).label("sales_share"),
                                      func.sum(Stg_SalesProduct.sales_share_change_vs_ya).label("share_chg"),
                                      func.sum(Stg_SalesProduct.volume_chg).label("volume_mean"),
                                      func.sum(Stg_SalesProduct.unit_chg).label("unit_mean"),
                                      ).join(Stg_Product).filter(Stg_Product.category == products_category[j].category).all()

            data[0]['items'][i]['items'].append({
                "items": [],
                "name": products_category[j].category,
                "sales_sum": sales_details[0].sales_sum,
                "sales_mean": sales_details[0].sales_mean,
                "sales_share": sales_details[0].sales_share,
                "share_chg": sales_details[0].share_chg,
                "volume_mean": sales_details[0].volume_mean,
                "unit_mean": sales_details[0].unit_mean,
            })

            product_sub_category = db.query(Stg_Product.sub_category).filter(Stg_Product.category == products_category[j].category, Stg_Product.sub_category != None).group_by(Stg_Product.sub_category).all()

            for k in range(len(product_sub_category)):
                sales_details = db.query(func.sum(Stg_SalesProduct.sales).label("sales_sum"),
                                         func.sum(Stg_SalesProduct.sales_chg).label("sales_mean"),
                                         func.sum(Stg_SalesProduct.sales_share).label("sales_share"),
                                         func.sum(Stg_SalesProduct.sales_share_change_vs_ya).label("share_chg"),
                                         func.sum(Stg_SalesProduct.volume_chg).label("volume_mean"),
                                         func.sum(Stg_SalesProduct.unit_chg).label("unit_mean"),
                                         ).join(Stg_Product).filter(
                    Stg_Product.sub_category == product_sub_category[k].sub_category).all()

                data[0]['items'][i]['items'][j]['items'].append({
                    "items": [],
                    "name": product_sub_category[k].sub_category,
                    "sales_sum": sales_details[0].sales_sum,
                    "sales_mean": sales_details[0].sales_mean,
                    "sales_share": sales_details[0].sales_share,
                    "share_chg": sales_details[0].share_chg,
                    "volume_mean": sales_details[0].volume_mean,
                    "unit_mean": sales_details[0].unit_mean,
                })

    return data
