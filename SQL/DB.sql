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