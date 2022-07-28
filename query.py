from sqlalchemy.sql import func

from Models import Stg_SalesProduct, Stg_Geography


def get_geography_for_type(db, geo_type):
    return db.query(Stg_Geography.geography).filter(Stg_Geography.geography_type==geo_type).all()


def get_geography_details_count(db, geo):
    return db.query(Stg_SalesProduct).filter(Stg_SalesProduct.geography==geo).count()


def get_geography_details(db, geo):
    return db.query(func.sum(Stg_SalesProduct.sales).label("sales_sum"),
             func.sum(Stg_SalesProduct.sales_chg).label("sales_mean"),
             func.sum(Stg_SalesProduct.sales_share).label("sales_share"),
             func.sum(Stg_SalesProduct.sales_share_change_vs_ya).label("share_chg")
             ).filter(Stg_SalesProduct.geography==geo).all()