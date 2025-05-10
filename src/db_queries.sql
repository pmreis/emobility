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


with recursive
    countAllChargers as (
        select count(1) total
        from Chargers
    ),
    cte1 as (
        select
            OperatorAbb party_id,
            count(1) as 'count'
        from Chargers
        group by OperatorAbb
        order by count desc
    ),
    cte2 as (
        select
            row_number() over() idx,
            cte1.*,
            cast(cte1.count as real) / cast(countAllChargers.total as real) mrkt_shr
        from cte1, countAllChargers
    )
select
    cte2.*,
    sum(mrkt_shr) over (order by idx) mrkt_shr_acc
from cte2;