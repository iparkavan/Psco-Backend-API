from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from Models import Stg_Product, Stg_SalesProduct, Base, Stg_Time
from database import SessionLocal, engine
from query import (
    get_geography_for_type,
    get_geography_details,
    get_geography_details_count,
    get_all_trademark,
    get_trade_count,
    get_trade_details,
    get_pack_size,
    get_pack_size_count,
    get_pack_size_details,
    get_competitor,
)

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


@app.get("/getproductdata/{product_term}/{time_period}")
async def root(product_term: str, time_period: str = 'L1W', db: Session = Depends(get_db)):
    data = []
    products_segment = db.query(Stg_Product.segment).filter(Stg_Product.bu == product_term,
                                                            Stg_Product.segment != None).group_by(
        Stg_Product.segment).all()

    sales_products_count = db.query(Stg_SalesProduct.index).join(Stg_Product).join(Stg_Time).filter(
        Stg_Product.bu == product_term,
        Stg_Product.segment != None,
        Stg_Product.category != None,
        Stg_Product.sub_category != None,
        Stg_Time.time_desc_short == time_period).count()

    sales_products = db.query(func.sum(Stg_SalesProduct.sales).label("sales_sum"),
                              func.sum(Stg_SalesProduct.sales_chg).label("sales_mean"),
                              func.sum(Stg_SalesProduct.sales_share).label("sales_share"),
                              func.sum(Stg_SalesProduct.sales_share_change_vs_ya).label("share_chg"),
                              func.sum(Stg_SalesProduct.volume_chg).label("volume_mean"),
                              func.sum(Stg_SalesProduct.unit_chg).label("unit_mean"),
                              func.sum(Stg_SalesProduct.rom_sales_chg).label("rom_sales_chg"),
                              func.sum(Stg_SalesProduct.segment_sales_share).label("segment_sales_share"),
                              func.sum(Stg_SalesProduct.segment_sales_share_change_vs_ya).label("segment_sales_share_change_vs_ya"),
                              ).join(Stg_Product).join(Stg_Time).filter(
        Stg_Product.bu == product_term,
        Stg_Product.segment != None,
        Stg_Product.category != None,
        Stg_Product.sub_category != None,
        Stg_Time.time_desc_short == time_period).all()

    data.append({
        "items": [],
        "name": product_term,
        "sales_sum": sales_products[0].sales_sum,
        "sales_mean": sales_products[0].sales_mean/sales_products_count if  sales_products[0].sales_mean else 0,
        "sales_share": sales_products[0].sales_share,
        "share_chg": sales_products[0].share_chg,
        "volume_mean": sales_products[0].volume_mean/sales_products_count if sales_products[0].volume_mean else 0,
        "unit_mean": sales_products[0].unit_mean/sales_products_count if sales_products[0].unit_mean else 0,
        "rom_sales_chg": sales_products[0].rom_sales_chg/sales_products_count if sales_products[0].rom_sales_chg else 0,
        "segment_sales_share": sales_products[0].segment_sales_share,
        "segment_sales_share_change_vs_ya": sales_products[0].segment_sales_share_change_vs_ya,
    })

    for i in range(len(products_segment)):
        if products_segment[i].segment != 'null':
            sales_products_count = db.query(Stg_SalesProduct.index).join(Stg_Product).join(Stg_Time).filter(
                Stg_Product.segment == products_segment[i].segment,
                Stg_Product.bu == product_term,
                Stg_Product.category != None,
                Stg_Product.sub_category != None,
                Stg_Time.time_desc_short == time_period).count()

            sales_products = db.query(func.sum(Stg_SalesProduct.sales).label("sales_sum"),
                                      func.sum(Stg_SalesProduct.sales_chg).label("sales_mean"),
                                      func.sum(Stg_SalesProduct.sales_share).label("sales_share"),
                                      func.sum(Stg_SalesProduct.sales_share_change_vs_ya).label("share_chg"),
                                      func.sum(Stg_SalesProduct.volume_chg).label("volume_mean"),
                                      func.sum(Stg_SalesProduct.unit_chg).label("unit_mean"),
                                      func.sum(Stg_SalesProduct.rom_sales_chg).label("rom_sales_chg"),
                                      func.sum(Stg_SalesProduct.segment_sales_share).label("segment_sales_share"),
                                      func.sum(Stg_SalesProduct.segment_sales_share_change_vs_ya).label(
                                          "segment_sales_share_change_vs_ya"),
                                      ).join(Stg_Product).join(Stg_Time).filter(
                Stg_Product.segment == products_segment[i].segment,
                Stg_Product.bu == product_term,
                Stg_Product.category != None,
                Stg_Product.sub_category != None,
                Stg_Time.time_desc_short == time_period).all()

            data[0]['items'].append({
                "items": [],
                "name": products_segment[i].segment,
                "sales_sum": sales_products[0].sales_sum/sales_products_count if sales_products[0].sales_sum else 0,
                "sales_mean": sales_products[0].sales_mean,
                "sales_share": sales_products[0].sales_share,
                "share_chg": sales_products[0].share_chg,
                "volume_mean": sales_products[0].volume_mean/sales_products_count if sales_products[0].volume_mean else 0,
                "unit_mean": sales_products[0].unit_mean/sales_products_count if sales_products[0].unit_mean else 0,
                "rom_sales_chg": sales_products[0].rom_sales_chg/sales_products_count if sales_products[0].rom_sales_chg else 0,
                "segment_sales_share": sales_products[0].segment_sales_share,
                "segment_sales_share_change_vs_ya": sales_products[0].segment_sales_share_change_vs_ya,
            })

        products_category = db.query(Stg_Product.category).filter(Stg_Product.segment == products_segment[i].segment,
                                                                  Stg_Product.category != None).group_by(
            Stg_Product.category).all()

        for j in range(len(products_category)):
            sales_products_count = db.query(Stg_SalesProduct.index).join(Stg_Product).join(Stg_Time).filter(
                Stg_Product.category == products_category[j].category,
                Stg_Product.bu == product_term,
                Stg_Product.sub_category != None,
                Stg_Time.time_desc_short == time_period).count()

            sales_details = db.query(func.sum(Stg_SalesProduct.sales).label("sales_sum"),
                                     func.sum(Stg_SalesProduct.sales_chg).label("sales_mean"),
                                     func.sum(Stg_SalesProduct.sales_share).label("sales_share"),
                                     func.sum(Stg_SalesProduct.sales_share_change_vs_ya).label("share_chg"),
                                     func.sum(Stg_SalesProduct.volume_chg).label("volume_mean"),
                                     func.sum(Stg_SalesProduct.unit_chg).label("unit_mean"),
                                     func.sum(Stg_SalesProduct.rom_sales_chg).label("rom_sales_chg"),
                                     func.sum(Stg_SalesProduct.segment_sales_share).label("segment_sales_share"),
                                     func.sum(Stg_SalesProduct.segment_sales_share_change_vs_ya).label(
                                         "segment_sales_share_change_vs_ya"),
                                     ).join(Stg_Product).join(Stg_Time).filter(
                Stg_Product.category == products_category[j].category,
                Stg_Product.bu == product_term,
                Stg_Product.sub_category != None,
                Stg_Time.time_desc_short == time_period).all()

            data[0]['items'][i]['items'].append({
                "items": [],
                "name": products_category[j].category,
                "sales_sum": sales_details[0].sales_sum,
                "sales_mean": sales_details[0].sales_mean/sales_products_count if sales_details[0].sales_mean else 0,
                "sales_share": sales_details[0].sales_share,
                "share_chg": sales_details[0].share_chg,
                "volume_mean": sales_details[0].volume_mean/sales_products_count if sales_details[0].volume_mean else 0,
                "unit_mean": sales_details[0].unit_mean/sales_products_count if sales_details[0].unit_mean else 0,
                "rom_sales_chg": sales_details[0].rom_sales_chg/sales_products_count if sales_details[0].rom_sales_chg else 0,
                "segment_sales_share": sales_details[0].segment_sales_share,
                "segment_sales_share_change_vs_ya": sales_details[0].segment_sales_share_change_vs_ya,
            })

            product_sub_category = db.query(Stg_Product.sub_category).filter(
                Stg_Product.category == products_category[j].category, Stg_Product.sub_category != None).group_by(
                Stg_Product.sub_category).all()

            for k in range(len(product_sub_category)):
                sales_products_count = db.query(Stg_SalesProduct).join(Stg_Product).join(Stg_Time).filter(
                    Stg_Product.sub_category == product_sub_category[k].sub_category,
                    Stg_Product.bu == product_term,
                    Stg_Time.time_desc_short == time_period).count()

                sales_details = db.query(func.sum(Stg_SalesProduct.sales).label("sales_sum"),
                                         func.sum(Stg_SalesProduct.sales_chg).label("sales_mean"),
                                         func.sum(Stg_SalesProduct.sales_share).label("sales_share"),
                                         func.sum(Stg_SalesProduct.sales_share_change_vs_ya).label("share_chg"),
                                         func.sum(Stg_SalesProduct.volume_chg).label("volume_mean"),
                                         func.sum(Stg_SalesProduct.unit_chg).label("unit_mean"),
                                         func.sum(Stg_SalesProduct.rom_sales_chg).label("rom_sales_chg"),
                                         func.sum(Stg_SalesProduct.segment_sales_share).label("segment_sales_share"),
                                         func.sum(Stg_SalesProduct.segment_sales_share_change_vs_ya).label(
                                             "segment_sales_share_change_vs_ya"),
                                         ).join(Stg_Product).join(Stg_Time).filter(
                    Stg_Product.sub_category == product_sub_category[k].sub_category,
                    Stg_Product.bu == product_term,
                    Stg_Time.time_desc_short == time_period).all()

                data[0]['items'][i]['items'][j]['items'].append({
                    "items": [],
                    "name": product_sub_category[k].sub_category,
                    "sales_sum": sales_details[0].sales_sum,
                    "sales_mean": sales_details[0].sales_mean/sales_products_count if sales_details[0].sales_mean else 0,
                    "sales_share": sales_details[0].sales_share,
                    "share_chg": sales_details[0].share_chg,
                    "volume_mean": sales_details[0].volume_mean/sales_products_count if sales_details[0].volume_mean else 0,
                    "unit_mean": sales_details[0].unit_mean/sales_products_count if sales_details[0].unit_mean else 0,
                    "rom_sales_chg": sales_details[0].rom_sales_chg/sales_products_count if sales_details[0].rom_sales_chg else 0,
                    "segment_sales_share": sales_details[0].segment_sales_share,
                    "segment_sales_share_change_vs_ya": sales_details[0].segment_sales_share_change_vs_ya,
                })

    return data


@app.get("/getgeography/{geo_type}/{product_term}/{product_key}/{time_period}")
async def root(geo_type: str, product_term: str, product_key: str, time_period: str = 'L1W',  db: Session = Depends(get_db)):
    data = []
    geography_data = get_geography_for_type(db, geo_type)
    for each_geography in geography_data:
        geo_details_count = get_geography_details_count(db, each_geography.geography, product_term, product_key, time_period)
        geo_details = get_geography_details(db, each_geography.geography, product_term, product_key, time_period)
        data.append({
            "name": each_geography.geography,
            "sales_sum": geo_details[0].sales_sum,
            "sales_mean": geo_details[0].sales_mean / geo_details_count if geo_details[0].sales_mean else 0,
            "sales_share": geo_details[0].sales_share,
            "share_chg": geo_details[0].share_chg
        })

    return data


@app.get("/gettrademark/{product_term}/{product_key}/{time_period}")
async def root(product_term: str, product_key: str, time_period: str = 'L1W', db: Session = Depends(get_db)):
    data = []
    trademarks = get_all_trademark(db, product_term, time_period)
    for each_trademark in trademarks:
        trade_details_count = get_trade_count(db, product_term, product_key, time_period)
        trade_details = get_trade_details(db, product_term, product_key, time_period)
        data.append({
            "name": each_trademark.us_trademark,
            "sales_sum": trade_details[0].sales_sum,
            "sales_mean": trade_details[0].sales_mean / trade_details_count if trade_details[0].sales_mean else 0,
            "sales_share": trade_details[0].sales_share,
            "share_chg": trade_details[0].share_chg
        })

    return data


@app.get("/getpacksize/{product_term}/{product_key}/{time_period}")
async def root(product_term: str, product_key: str, time_period: str = 'L1W', db: Session = Depends(get_db)):
    data = []
    pack_size = get_pack_size(db, product_term, product_key, time_period)
    for each_pack_size in pack_size:
        pack_size_count = get_pack_size_count(db, product_term, product_key, each_pack_size.us_serving_size, time_period)
        pack_size_details = get_pack_size_details(db, product_term, product_key, each_pack_size.us_serving_size, time_period)
        data.append({
            "name": each_pack_size.us_serving_size,
            "sales_sum": pack_size_details[0].sales_sum,
            "sales_mean": pack_size_details[0].sales_mean / pack_size_count if pack_size_details[0].sales_mean else 0,
            "sales_share": pack_size_details[0].sales_share,
            "share_chg": pack_size_details[0].share_chg
        })

    return data


@app.get("/getcompetitor/{product_term}/{product_key}/{time_period}/{geo_type}")
async def root(product_term: str, product_key: str, time_period: str, geo_type: str, db: Session = Depends(get_db)):
    return get_competitor(db, product_term, product_key, time_period, geo_type)
