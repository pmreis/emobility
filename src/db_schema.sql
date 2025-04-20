create table Chargers (
    Id integer primary key autoincrement,
    Country char(2) not null,
    ChargerNapId varchar(20) not null,
    OperatorMobAbb char(3) not null,
    OperatorNapAbb varchar(10) not null,
    OperatorName varchar(50) not null,
    unique (Country, ChargerNapId)
);

create table Plugs (
    Id integer primary key autoincrement,
    ChargerId integer not null,
    PlugNapId varchar(30) not null,
    PlugDesign varchar(30) not null,
    Voltage integer default 400 not null,
    Current integer default 16 not null,
    MaxPower integer default 11000 not null,
    foreign key(ChargerId) references Chargers(Id)
);

create table Ravel (
    Id integer primary key autoincrement,
    Name varchar(50) not null
);