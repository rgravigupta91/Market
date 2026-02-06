use market;

create table Country(
	CountryId INT auto_increment primary key,
    CountryName varchar(50)
);

insert into Country values(1, 'India');

create table StockExchange(
	CODE varchar(5) primary key,
    CountryId INT,
    Name varchar(30),
    foreign key (CountryId) references Country(CountryId)
);

insert into StockExchange values('BSE',1, 'Bombay Stock Exchange');
insert into StockExchange values('NSE',1, 'National Stock Exchange');

create table Sector(
	SectorId int4 primary key,
    Name varchar(50),
    ParentSectorId int4,
    foreign key (ParentSectorId) references Sector(SectorId)
);

Create table Industry(
	IndustryId int2 primary key,
    Name varchar(100),
    SectorId int1
);

insert into Sector values(1,'Durable Goods',null);
insert into Sector values(2,'Non-Durable Goods',null);
insert into Sector values(3,'Materials',null);
insert into Sector values(4,'Industrials',null);
insert into Sector values(5,'Financials',null);
insert into Sector values(6,'Energy',null);
insert into Sector values(7,'Consumer Discretionary',null);
insert into Sector values(8,'Information Technology',null);
insert into Sector values(9,'Communication Services',null);
insert into Sector values(10,'Real Estate',null);
insert into Sector values(11,'Health Care',null);
insert into Sector values(12,'Consumer Staples',null);
insert into Sector values(13,'Utilities',null);
insert into Sector values(14,'Mining and Minirals',null);

create table StockStatus(
	StatusID int1 primary key,
    Status varchar(25)
);
insert into StockStatus values(1,'Listed');
insert into StockStatus values(2,'Temporarily Suspended');

create table TradingStatus(
	TradingStatusID int1 primary key,
    TradingStatus varchar(20)
);
insert into TradingStatus values(1,'Active');
insert into TradingStatus values(2,'stockSuspended');


create table stock(
	ISIN varchar(20) primary key,
    StockName varchar(50),
    SectorId INT4,
    ListingDate Date,
    stock_status int1,
    trading_status int1,
    foreign key (SectorId) references Sector(SectorId),
    foreign key (stock_status) references StockStatus(StatusID),
    foreign key (trading_status) references TradingStatus(TradingStatusID)
);

create table StockExchange_StockCode(
	ISIN varchar(20) not null,
    StockExchange varchar(5) not null,
    Symbol varchar(20) not null,
    primary key (ISIN, StockExchange),
    foreign key (ISIN) references stock(ISIN),
    foreign key (StockExchange) references StockExchange(CODE)
);

create table StockDailyUpdate(
	StockExchange VARCHAR(5) NOT NULL,
	Symbol varchar(20) not null,
    Date date not null,
    open float,
    high float,
    low float,
    close float,
    volume bigint,
    delivery bigint,
    PRIMARY KEY (StockExchange, Symbol, Date),
    FOREIGN KEY (StockExchange) 
        REFERENCES StockExchange_StockCode(StockExchange)
);
use market;
# alter table StockDailyUpdate drop foreign key stockdailyupdate_ibfk_1;
# alter table stockexchange_stockcode drop foreign key stockexchange_stockcode_ibfk_2;

create table Dividends(
	ISIN varchar(20),
    RecordDate date not null,
    dividend float,
    PRIMARY KEY (ISIN, RecordDate),
    FOREIGN KEY (ISIN) 
        REFERENCES stock(ISIN)
);

# "alter table DealType modify column description varchar(5);"
create table DealType(
	ID varchar(1) primary key,
    description varchar(5)
);

insert into DealType values('B','Buy');
insert into DealType values('S','Sell');

create table client(
	client_id varchar(10) primary key,
    name varchar(150)
);

/*
SELECT TABLE_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE REFERENCED_TABLE_NAME = 'BlockDeal';
*/

-- check table blockdeal;

-- SHOW TABLE STATUS LIKE 'blockdeal';
-- SHOW VARIABLES LIKE 'datadir';
-- drop table client;
-- drop table BlockDeal;
-- SHOW ENGINE INNODB STATUS \G;
create table BlockDeal(
	UUID varchar(36),
    ISIN varchar(20),
    DealDate date,
    StockExchange varchar(5),
    Client varchar(10),
    DealType varchar(1),
    Quantity int4,
    price float,
    Primary Key(UUID),
    foreign key (ISIN) references stock(ISIN),
    foreign key (StockExchange) references StockExchange(CODE),
    foreign key (Client) references client(client_id),
    foreign key (DealType) references DealType(ID)
);

create table BlackListed(
	ISIN varchar(20)
);


-- alter table BlockDeal add column UUID varchar(36) first;
-- alter table blockdeal DROP PRIMARY KEY, 
-- add primary key (UUID);
-- drop table blockdeal;
-- (UUID, ISIN, DealDate, StockExchange, Client, DealType);




SET GLOBAL net_read_timeout=600;
SET GLOBAL net_write_timeout=600;
SET GLOBAL wait_timeout=600;
SET GLOBAL max_allowed_packet=1073741824;  -- 1 GB

SET GLOBAL net_read_timeout = 600;
SET GLOBAL net_write_timeout = 600;
SET GLOBAL interactive_timeout = 600;
SET GLOBAL wait_timeout = 600;
SET GLOBAL innodb_lock_wait_timeout = 600;



#   ------------ Views -------------------------------
create view v_blockdeal as select ISIN, DealDate, sum(Quantity) as quantity, round(avg(price), 2) as price from market.blockdeal where DealType = 'B' group by ISIN, DealDate;

create or replace view v_stockdailyupdate as
select 
s.ISIN, 
s.SectorId, 
sdu.Date, 
sdu.open, 
sdu.high, 
sdu.low, 
sdu.close, 
sdu.volume, 
sdu.delivery,
case coalesce(bl.isin, '-')
when '-' then null
else 'X' end as BlackListed,
coalesce(d.dividend, 0) as dividend, 
coalesce(vbd.quantity, 0) as blockdeal_quantity,
coalesce(vbd.price, 0) as blockdeal_avg_price
from market.stock as s
inner join market.stockexchange_stockcode as sd on s.ISIN = sd.ISIN
inner join market.stockdailyupdate as sdu on sd.Symbol = sdu.Symbol
left outer join market.dividends as d on s.ISIN = d.ISIN and sdu.Date = d.RecordDate
left outer join market.v_blockdeal as vbd on s.ISIN = vbd.ISIN and sdu.Date = vbd.DealDate
left outer join market.BlackListed as bl on s.ISIN = bl.isin
where s.ListingDate is not null and s.stock_status = 1 and s.trading_status = 1 and sd.StockExchange = 'NSE';