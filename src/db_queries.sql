-- delete from Plugs;
-- delete from Chargers;
-- delete from sqlite_sequence;

select distinct PlugDesign
from Plugs;

select *
from Plugs
where PlugDesign = 'iec60309x2single16';

with recursive
    countAllChargers as (
        select count(1) total
        from Chargers
    ),
    cte as (
        select
            OperatorMobAbb party_id,
        count(1) as 'count'
        from Chargers
        group by OperatorMobAbb
        order by count desc
    )
select
    row_number() over() idx,
    cte.*,
    cast(cte.count as real) / cast(countAllChargers.total as real) mrkt_shr
from cte, countAllChargers;