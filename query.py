from sqlalchemy.sql import func

from Models import (
    Stg_SalesProduct,
    Stg_Geography,
    Stg_Product,
    Stg_SalesTrademark,
    Stg_SalesPackSize,
    Stg_Time,
)


def get_geography_for_type(db, geo_type):
    return db.query(Stg_Geography.geography).filter(Stg_Geography.geography_type == geo_type).all()


def get_geography_details_count(db, geo, product_term, product_key, time_period):
    if product_key == 'na':
        return db.query(Stg_SalesProduct.index).join(Stg_Product).join(Stg_Time).filter(Stg_Product.bu == product_term,
                                                                   Stg_SalesProduct.geography == geo,
                                                                   Stg_Time.time_desc_short == time_period).count()
    else:
        return db.query(Stg_SalesProduct).join(Stg_Product).join(Stg_Time).filter(Stg_Product.bu == product_term,
                                                                   Stg_SalesProduct.geography == geo,
                                                                   Stg_SalesProduct.product_key == product_key,
                                                                   Stg_Time.time_desc_short == time_period).count()


def get_geography_details(db, geo, product_term, product_key, time_period):
    if product_key == 'na':
        return db.query(func.sum(Stg_SalesProduct.sales).label("sales_sum"),
                        func.sum(Stg_SalesProduct.sales_chg).label("sales_mean"),
                        func.sum(Stg_SalesProduct.sales_share).label("sales_share"),
                        func.sum(Stg_SalesProduct.sales_share_change_vs_ya).label("share_chg")
                        ).join(Stg_Product).join(Stg_Time).filter(Stg_Product.bu == product_term,
                                                   Stg_SalesProduct.geography == geo,
                                                   Stg_Time.time_desc_short == time_period).all()
    else:
        return db.query(func.sum(Stg_SalesProduct.sales).label("sales_sum"),
                        func.sum(Stg_SalesProduct.sales_chg).label("sales_mean"),
                        func.sum(Stg_SalesProduct.sales_share).label("sales_share"),
                        func.sum(Stg_SalesProduct.sales_share_change_vs_ya).label("share_chg")
                        ).join(Stg_Product).join(Stg_Time).filter(Stg_Product.bu == product_term,
                                                   Stg_SalesProduct.geography == geo,
                                                   Stg_SalesProduct.product_key == product_key,
                                                   Stg_Time.time_desc_short == time_period).all()


def get_all_trademark(db, product_term, time_period):
    return db.query(Stg_SalesTrademark.us_trademark).join(Stg_Product).join(Stg_Time).filter(Stg_Product.bu == product_term, Stg_Time.time_desc_short == time_period).group_by(Stg_SalesTrademark.us_trademark).all()


def get_trade_count(db, product_term, product_key, time_period):
    if product_key == 'na':
        return db.query(Stg_SalesTrademark).join(Stg_Product).join(Stg_Time).filter(Stg_Product.bu == product_term,
                                                                                    Stg_Time.time_desc_short == time_period).count()
    else:
        return db.query(Stg_SalesTrademark).join(Stg_Product).join(Stg_Time).filter(Stg_Product.bu == product_term,
                                                                     Stg_SalesTrademark.product_key == product_key,
                                                                     Stg_Time.time_desc_short == time_period).count()


def get_trade_details(db, product_term, product_key, time_period):
    if product_key == 'na':
        return db.query(func.sum(Stg_SalesTrademark.sales).label("sales_sum"),
                        func.sum(Stg_SalesTrademark.sales_chg).label("sales_mean"),
                        func.sum(Stg_SalesTrademark.sales_share).label("sales_share"),
                        func.sum(Stg_SalesTrademark.sales_share_change_vs_ya).label("share_chg")
                        ).join(Stg_Product).join(Stg_Time).filter(Stg_Product.bu == product_term,
                                                                  Stg_Time.time_desc_short == time_period).all()
    else:
        return db.query(func.sum(Stg_SalesTrademark.sales).label("sales_sum"),
                        func.sum(Stg_SalesTrademark.sales_chg).label("sales_mean"),
                        func.sum(Stg_SalesTrademark.sales_share).label("sales_share"),
                        func.sum(Stg_SalesTrademark.sales_share_change_vs_ya).label("share_chg")
                        ).join(Stg_Product).join(Stg_Time).filter(Stg_Product.bu == product_term,
                                                   Stg_SalesTrademark.product_key == product_key,
                                                   Stg_Time.time_desc_short == time_period).all()


def get_pack_size(db, product_term, product_key, time_period):
    return db.query(Stg_SalesPackSize.us_serving_size).join(Stg_Product).join(Stg_Time).filter(Stg_Product.bu == product_term,
                                                                                Stg_SalesPackSize.product_key == product_key,
                                                                                Stg_Time.time_desc_short == time_period).group_by(
        Stg_SalesPackSize.us_serving_size).all()


def get_pack_size_count(db, product_term, product_key, pack_size, time_period):
    return db.query(Stg_SalesPackSize).join(Stg_Product).join(Stg_Time).filter(Stg_Product.bu == product_term,
                                                                Stg_SalesPackSize.product_key == product_key,
                                                                Stg_SalesPackSize.us_serving_size == pack_size,
                                                                Stg_Time.time_desc_short == time_period).count()


def get_pack_size_details(db, product_term, product_key, pack_size, time_period):
    return db.query(func.sum(Stg_SalesPackSize.sales).label("sales_sum"),
                    func.sum(Stg_SalesPackSize.sales_chg).label("sales_mean"),
                    func.sum(Stg_SalesPackSize.sales_share).label("sales_share"),
                    func.sum(Stg_SalesPackSize.sales_share_change_vs_ya).label("share_chg")
                    ).join(Stg_Product).join(Stg_Time).filter(Stg_Product.bu == product_term,
                                               Stg_SalesPackSize.product_key == product_key,
                                               Stg_SalesPackSize.us_serving_size == pack_size,
                                               Stg_Time.time_desc_short == time_period).all()
