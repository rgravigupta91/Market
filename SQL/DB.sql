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

create table stock(
	ISIN varchar(20) primary key,
    StockName varchar(50),
    SectorId INT4,
    foreign key (SectorId) references Sector(SectorId)
);

create table StockExchange_StockCode(
	ISIN varchar(20) not null,
    StockExchange varchar(5) not null,
    Symbol varchar(20) not null,
    primary key (ISIN, StockExchange),
    foreign key (ISIN) references stock(ISIN),
    foreign key (StockExchange) references StockExchange(CODE)
);
use market;

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