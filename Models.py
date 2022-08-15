from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from database import Base


class Stg_Product(Base):
    __tablename__ = "Stg_Product"

    index = Column(Integer, primary_key=True, index=True)
    product = Column("Product", String(255))
    product_key = Column("Product Key", String(255))
    hierarchy_level = Column("Hierarchy Level", String(255))
    corporate = Column("Corporate", String(255))
    bu = Column("BU", String(255))
    segment = Column("Segment", String(255))
    category = Column("Category", String(255))
    sub_category = Column("Sub Category", String(255))
    trademark = Column("Trademark", String(255))
    line_extension = Column("Line Extension", String(255))
    sales = Column("Sales", Integer)
    product_filter = Column("Product Filter", String(255))


class Stg_SalesProduct(Base):
    __tablename__ = "Stg_SalesProduct"

    index = Column(Integer, primary_key=True, index=True)
    product = Column("Product", String(255))
    geography = Column("Geography", String(255))
    time = Column("Time", String(255), ForeignKey("Stg_Time.Time"))
    us_parent_company = Column("US Parent Company", String(255))
    product_key = Column("Product Key", String(255), ForeignKey("Stg_Product.Product Key"))
    sales = Column("Sales", DOUBLE_PRECISION)
    sales_chg = Column("Sales % Chg", DOUBLE_PRECISION)
    rom_sales_chg = Column("ROM Sales Chg %", DOUBLE_PRECISION)
    total_sales_chg = Column("Total Sales Chg %", DOUBLE_PRECISION)
    sales_share = Column("Sales Share", DOUBLE_PRECISION)
    segment_sales_share = Column("Segment Sales Share", DOUBLE_PRECISION)
    sales_share_change_vs_ya = Column("Sales Share Change vs YA", DOUBLE_PRECISION)
    volume_chg = Column("Vol % Chg", DOUBLE_PRECISION)
    unit_chg = Column("Unit % Chg", DOUBLE_PRECISION)
    avg_item_per_store_chg = Column("Avg Item Per Store Chg %", DOUBLE_PRECISION)
    iod_chg = Column("IOD Chg %", DOUBLE_PRECISION)
    iod = Column("IOD", DOUBLE_PRECISION)
    nod_chg = Column("NOD Chg %", DOUBLE_PRECISION)
    nod = Column("NOD", DOUBLE_PRECISION)
    segment_sales_share_change_vs_ya = Column("Segment Sales Share Change vs YA", DOUBLE_PRECISION)


class Stg_Geography(Base):
    __tablename__ = "Stg_Geography"

    index = Column(Integer, primary_key=True, index=True)
    geography = Column("Geography", String(255), ForeignKey("Stg_SalesProduct.Geography"))
    geography_key = Column("Geography Key", String(255))
    geography_name = Column("Geography Name", String(255))
    geography_type = Column("Geography Type", String(255))
    geography_channel = Column("Geography Channel", String(255))
    dollar_sales = Column("Dollar Sales", String(255))


class Stg_Time(Base):
    __tablename__ = 'Stg_Time'

    index = Column(Integer, primary_key=True, index=True)
    time = Column("Time", String(255))
    time_key = Column("Time Key", String(255))
    time_desc_long = Column("Time Desc Long", String(255))
    time_desc_short = Column("Time Desc Short", String(255))
    ending_date = Column("Ending Date", String(255))
    time_order = Column("Time Order", DateTime(timezone=True))


class Stg_SalesPackSize(Base):
    __tablename__ = "Stg_SalesPackSize"

    index = Column(Integer, primary_key=True, index=True)
    product = Column("Product", String(255))
    geography = Column("Geography", String(255), ForeignKey("Stg_Geography.Geography"))
    time = Column("Time", String(255), ForeignKey("Stg_Time.Time"))
    us_parent_company = Column("US Parent Company", String(255))
    us_serving_size = Column("US Serving Size", String(255))
    product_key = Column("Product Key", String(255), ForeignKey("Stg_Product.Product Key"))
    sales = Column("Sales", DOUBLE_PRECISION)
    sales_chg = Column("Sales % Chg", DOUBLE_PRECISION)
    rom_sales_chg = Column("ROM Sales Chg %", DOUBLE_PRECISION)
    total_sales_chg = Column("Total Sales Chg %", DOUBLE_PRECISION)
    sales_share = Column("Sales Share", DOUBLE_PRECISION)
    sales_share_change_vs_ya = Column("Sales Share Change vs YA", DOUBLE_PRECISION)
    segment_sales_share = Column("Segment Sales Share", DOUBLE_PRECISION)
    segment_sales_share_change_vs_ya = Column("Segment Sales Share Change vs YA", DOUBLE_PRECISION)
    vol_chg = Column("Vol % Chg", DOUBLE_PRECISION)
    unit_chg = Column("Unit % Chg", DOUBLE_PRECISION)


class Stg_SalesTrademark(Base):
    __tablename__ = 'Stg_SalesTrademark'

    index = Column(Integer, primary_key=True, index=True)
    product = Column("Product", String(255))
    geography = Column("Geography", String(255), ForeignKey("Stg_Geography.Geography"))
    time = Column("Time", String(255), ForeignKey("Stg_Time.Time"))
    us_trademark = Column("US Trademark", String(255))
    us_parent_company = Column("US Parent Company", String(255))
    product_key = Column("Product Key", String(255), ForeignKey("Stg_Product.Product Key"))
    sales = Column("Sales", Integer)
    sales_chg = Column("Sales % Chg", DOUBLE_PRECISION)
    rom_sales_chg = Column("ROM Sales Chg %", DOUBLE_PRECISION)
    sales_share = Column("Sales Share", DOUBLE_PRECISION)
    sales_share_change_vs_ya = Column("Sales Share Change vs YA", DOUBLE_PRECISION)
    segment_sales_share = Column("Segment Sales Share", DOUBLE_PRECISION)
    segment_sales_share_change_vs_ya = Column("Segment Sales Share Change vs YA", DOUBLE_PRECISION)
    vol_chg = Column("Vol % Chg", DOUBLE_PRECISION)
    unit_chg = Column("Unit % Chg", DOUBLE_PRECISION)
    sales_filter = Column("Sales Filter", String(255))
