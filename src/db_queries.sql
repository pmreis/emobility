-- delete from Plugs;
-- delete from Chargers;
-- delete from sqlite_sequence;


select distinct PlugDesign
from Plugs;


select *
from Plugs
where PlugDesign = 'iec60309x2single16';


select *
from Chargers
where length(ChargerId) > 9;


select PlugId, count(1) qnt
from Plugs
group by PlugId
order by qnt desc;


select *
from Plugs
where PlugId in (
    'PT*ATL*EAMD*00095*1',
    'PT*ATL*EAMD*00095*2',
    'PT*ATL*EAMD*00095*3',
    'PT*ATL*ENZR*00035*1',
    'PT*ATL*ENZR*00035*2'
)


with cte as (
    select OperatorAbb, count(1) qnt
    from Chargers
    group by OperatorAbb
    having qnt < 6
)
select o.*, cte.qnt
from Operators o
join cte on cte.OperatorAbb = o.OperatorAbb
order by cte.qnt, o.OperatorAbb;


select strftime('%Y', DeployDate), count(1)
from Chargers
group by strftime('%Y', DeployDate);


select p.*
from Plugs p
join Chargers c on c.ChargerId = p.ChargerId
join Operators o on o.OperatorAbb = c.OperatorAbb
where o.OperatorAbb = 'IOY'
order by c.ChargerId
limit 100;


select City, count(1) Qty
from Chargers
group by City
order by Qty desc, City asc;


with
countAllChargers as (
    select count(1) total
    from Chargers
    where Country = 'PT'
        and Status = 'Present'
),
cte1 as (
    select
        o.OperatorAbb 'Operator',
        o.OperatorName,
        count(c.OperatorAbb) as 'Qty'
    from Operators o
    left join Chargers c on c.OperatorAbb = o.OperatorAbb
        and o.CountryIso = 'PT'
        and c.Status = 'Present'
    group by o.OperatorAbb
    order by Qty desc
),
cte2 as (
    select
    row_number() over() 'Rank',
    cte1.*,
    cast(cte1.Qty as real) / cast(countAllChargers.total as real) 'MarketShare'
    from cte1, countAllChargers
)
select
cte2.*,
sum(MarketShare) over (order by Rank) 'CumulativeMarketShare'
from cte2;


alter table Chargers
rename column DeployDate to InsertedDate;

update Chargers
set InsertedDate = '2025-01-02'
where InsertedDate < '2018-01-01';

select ChargerId,
    OperatorAbb,
    City,
    Lat,
    Lon
from Chargers c
where c.InsertedDate = date('now')
order by ChargerId;


select d.Distrito, count(1) Qty
from Chargers c
join Concelhos cc on cc.Alias = c.City
join Distritos d on d.Id = cc.Distrito
group by d.Id
order by Qty desc, d.Distrito asc;


update Concelhos
set Alias = 'Lagoa, Faro',
    Concelho = 'Lagoa'
where Id = '0806';

update Concelhos
set Alias = 'Lagoa, Azores',
    Concelho = 'Lagoa'
where Id = '4201';

update Concelhos
set Alias = 'Calheta, Madeira',
    Concelho = 'Calheta'
where Id = '3101';

update Concelhos
set Alias = 'Calheta, Azores',
        Concelho = 'Calheta'
where Id = '4501';

select *
from Concelhos
where Id in ('0806', '4201', '3101', '4501');


select c.ChargerId, c.Status
from Chargers c
left outer join Plugs p on p.ChargerId = c.ChargerId
where p.ChargerId is null;


with recursive
    dates(InsertedDate) as (
        values(date('now', '-30 days'))
        union all
        select date(InsertedDate, '+1 day')
        from dates
        where InsertedDate < date('now')
    ),
    lastDates as (
        select InsertedDate, '0' as Qnt
        from dates
    ),
    chargersCount as (
        select c.InsertedDate, Count(c.ChargerId) as Qnt
        from Chargers c
        where c.InsertedDate >= DATETIME('now', '-30 days')
        group by c.InsertedDate
    ),
    dataUnion as (
        select *
        from lastDates
        union
        select *
        from chargersCount
    )
select InsertedDate, sum(Qnt) Qnt
from dataUnion
group by InsertedDate
order by InsertedDate;


select *
from Chargers
order by InsertedDate desc;


-- Check Chargers absent from NAP
select *
from Chargers
where Status = 'Removed'
order by InsertedDate desc;

-- Check Chargers absent from NAP for more than 90 days
select *
from Chargers
where Status = 'Removed'
    and InsertedDate < date('now', '-90 days')
order by InsertedDate desc;

-- Delete Chargers absent from NAP for more than 90 days
delete
from Plugs
where ChargerId in (
    select ChargerId
    from Chargers
    where Status = 'Removed'
        and InsertedDate < date('now', '-90 days')
);

with
klsChargers as (
    select *
    from Chargers c
    where c.OperatorAbb in ('KLS')
        and c.Status = 'Present'
),
galpChargers as (
    select *
    from Chargers c
    where c.OperatorAbb in ('GLP')
        and c.Status = 'Present'
)
select
    k.ChargerId as 'Id KLS',
        k.Lat ||',' || k.Lon 'geoKLC',
    g.ChargerId as 'Id GLP'
        , g.Lat ||',' || g.Lon 'geoGLP'
from klsChargers k
join galpChargers g on abs(g.Lat - k.Lat) < 0.0013
    and abs(g.Lon - k.Lon) < 0.0013
where
    cast(substr(k.ChargerId, 5, 5) as integer) < cast(substr(g.ChargerId, 5, 5) as integer)
    and substr(g.ChargerId, 5, 1) <> '9'
order by k.ChargerId;