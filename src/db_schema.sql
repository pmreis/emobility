create table Operators (
    OperatorAbb char(3) primary key,
    OperatorOtherAbb varchar(10) null,
    OperatorName varchar(50) not null,
    CountryIso char(2) not null,
    Tin varchar(20) null, -- Tax Identification Number
    Phone varchar(20) null
);

create table Chargers (
    ChargerId varchar(36) primary key,
    Country char(2) not null,
    OperatorAbb char(3) not null,
    City varchar(100) not null,
    Lat float not null,
    Lon float not null,
    GMapsUrl varchar(1024) not null,
    foreign key(OperatorAbb) references Operators(OperatorAbb)
);

create table Plugs (
    PlugId varchar(36) not null,
    ChargerId varchar(36) not null,
    PlugDesign varchar(30) not null,
    Voltage integer default 400 not null,
    Current integer default 16 not null,
    MaxPower integer default 11000 not null,
    primary key (PlugId, ChargerId),
    foreign key(ChargerId) references Chargers(ChargerId)
);
