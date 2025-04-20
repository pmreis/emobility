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
where length(ChargerNapId) > 9;

with recursive
    countAllChargers as (
        select count(1) total
        from Chargers
    ),
    cte1 as (
        select
            OperatorMobAbb party_id,
            count(1) as 'count'
        from Chargers
        group by OperatorMobAbb
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