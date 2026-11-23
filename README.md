# eMobility @ Europe

A repository containing a wide range of information related with electric mobility in Europe, with a focus on Portugal.

Here you can find references to legal frameworks, existing APIs, documentation and data.

The goal is to track the evolution of sustainable mobility milestones on each European country and also find inconsistencies and blockers.

**Structure**

- ./data  - contains data sources and analysis outputs
- ./docs  - contains technical documents (mainly in PDF)
- ./legal - contains legal documents (mainly in PDF)
- ./src   - contains source code

## Table of contents
1. [The European Green Deal](#the-european-green-deal)
2. [The Fit for 55 package](#the-fit-for-55-package)
3. [AFIR - Alternative Fuels Infrastructure Regulation](#afir---alternative-fuels-infrastructure-regulation)
4. [Portuguese Law](#portuguese-legal-framework-for-electric-mobility)
5. [National Access Points (NAP)](#national-access-points-nap)
    1. [Norway - Nobil](#no---norway)
    2. [Portugal -Mobi.e](#pt---portugal)
6. [Possible barriers for eMobility in Portugal](#possible-barriers-for-emobility-in-portugal)
7. [DATEX II Documentation](#datex-ii-documentation)

> NOTE: Work in Progress. Join the cause!

## The European Green Deal

The European Green Deal is a set of policy initiatives launched by the European Union (EU) aimed at making Europe the first climate-neutral continent by 2050. This means reducing greenhouse gas emissions to a level where they are balanced by removal or offsetting, effectively eliminating the net contribution to global warming.

**Key Goals**:
1. **Climate Neutrality by 2050**: The primary goal is to reduce EU's greenhouse gas emissions by at least 55% by 2030 (from 1990 levels) and to achieve full climate neutrality by 2050.

2. **Economic Growth Decoupled from Resource Use**: The deal promotes economic growth that doesn't rely on the unsustainable consumption of natural resources, transitioning towards a circular economy where waste is minimized and resources are reused.

3. **No Person and No Place Left Behind**: The Green Deal includes a "Just Transition Mechanism" to support regions and workers who might be adversely affected by the transition to a green economy, ensuring fairness and equity in the shift towards sustainability.

**Priorities**:
1. Clean Energy
    - Supplying clean, affordable and secure energy
2. Circular Economy
    - Mobilising industry for a clean and circular economy
3. Efficient Renovations
    - Building and renovating in an energy andd resource efficient way
4. Sustainable Mobility
    - Accelerating the shift to sustainable and smart mobility
5. Sustainable Food
    - From 'Farm to Fork': designing a fair, healthy and environmentally-friendly food system
6. Preserving Biodiversity
    - Preserving and restoring ecosystems and biodiversity
7. Climate Action
    - Increasing the EU's climate ambition for 2030 and 2050
8. Zero Pollution
    - A zero pollution ambition for a toxic-free environment

More info:
- https://commission.europa.eu/strategy-and-policy/priorities-2019-2024/european-green-deal_en
- https://sharedgreendeal.eu/

## The Fit for 55 package

The **Fit for 55 package** is a central part of the **European Green Deal**. It consists of a set of legislative proposals designed to ensure that the European Union (EU) meets its target of reducing greenhouse gas emissions by 55% by 2030 (compared to 1990 levels), which is a crucial milestone towards achieving the broader goal of climate neutrality by 2050 as outlined in the European Green Deal.

 ![fit-4-55](legal/fit-for-55-actions.png)

More info: https://www.consilium.europa.eu/en/policies/green-deal/fit-for-55/

## AFIR - Alternative Fuels Infrastructure Regulation

The **Alternative Fuels Infrastructure Regulation (AFIR)** is a key legislative proposal within the **Fit for 55 package**, which itself is part of the broader **European Green Deal**. AFIR aims to establish a comprehensive and cohesive infrastructure across the European Union for alternative fuels, such as electricity, hydrogen, and biofuels, to support the decarbonization of the transport sector.

- [Summary Info EN](http://eur-lex.europa.eu/EN/legal-content/summary/deployment-of-alternative-fuels-infrastructure.html)
- [Summary Info PT](http://eur-lex.europa.eu/PT/legal-content/summary/deployment-of-alternative-fuels-infrastructure.html)
- [Proposal](http://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52021PC0559)
- [Regulation](http://data.europa.eu/eli/reg/2023/1804/oj)
- [Q&A](https://transport.ec.europa.eu/transport-themes/clean-transport/alternative-fuels-sustainable-mobility-europe/alternative-fuels-infrastructure/questions-and-answers-regulation-deployment-alternative-fuels-infrastructure-eu-20231804_en)

## Portuguese legal framework for electric mobility

In August 2025, Portugal overhauled the RJME via Decree-Law 93/2025 to align with the EU’s Alternative Fuels Infrastructure Regulation (AFIR, applicable since 13 April 2024). The new regime mandates ad-hoc charging (no prior contract), broad electronic payment options (e.g., bank card/QR), open roaming, smart and bidirectional charging, adds maritime charging, eliminates the CEME figure and the previous centralized network management, and sets a transition period until 31 December 2026 to meet AFIR’s data/transparency rules and EU coverage/power goals.

### Portuguese legal framework for electric mobility

- [DL 93/2025 @ Journal of the Republic](https://diariodarepublica.pt/dr/detalhe/decreto-lei/93-2025-928937303)

### Revoked at 2025-08-19
- [DL 39/2010 @ Journal of the Republic](https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/2010-171436738)
- [DL 39/2010 as PDF](legal/DL_39_2010.pdf)
- Regulation (Portuguese Only): [RME](legal/RME%20Consolidado.pdf)
- RME Changes between 2021 and 2023: [RME Diff](legal/RME_Diff_2021_2023.pdf)

## National Access Points (NAP)

https://napcore.eu/description-naps/national-access-point/

Country notes below track **AFIR Art. 20 style access** for public EV charging data: preferably **DATEX II**, **no account / no contract**, usable cross-border. Sources cross-checked with NAPCORE and [evnapdata.eu/naps](https://evnapdata.eu/naps) (Nov 2026).

| Access bar used here | Meaning |
|----------------------|---------|
| Open DATEX II | Public DATEX II XML/API, no login |
| Open other format | Public national data, not DATEX II |
| Registration / key | Free or paid gate before data |
| Contract / unclear | Formal process or no usable feed found |

### AT - Austria

- NAP: https://mobilitydata.gv.at
- Format: E-Control Ladestellenverzeichnis (XLSX), not DATEX II
- Access: API with **free account**
- Finding: national register exists; not open DATEX II without registration

### BE - Belgium

- NAP: https://transportdata.be
- Format: mix (OCPI / DATEX II / AFIR Energy Infrastructure) per provider
- Access: **API key or token** per provider (partial network coverage)
- Finding: DATEX II appears for some CPOs, but not a single open national dump

### BG - Bulgaria

- NAP: https://sipbg.gov.bg/bgnap
- Format / access: no EV charging feed found on the NAP (public transport focus)
- Finding: not usable for AFIR charging observability yet

### CH - Switzerland

- NAP / open data: https://opentransportdata.swiss
- Format: SFOE charging data (OICP JSON), not DATEX II
- Access: open download
- Finding: open non-DATEX; EEA/NAPCORE-adjacent, not EU AFIR-bound the same way

### CY - Cyprus

- NAP: https://traffic4cyprus.org.cy/en/dataset/electricvehiclecharges
- Static DATEX-like XML: https://fixcyprus.cy/gnosis/open/api/nap/datasets/electric_vehicle_chargers/
- Format: labelled DATEX II; custom `chargingPoint` profile (not full EnergyInfrastructureSite/refillPoint like PT/ES)
- Access: **open download, no account**
- Finding: public, but **very small** (~171 points / ~0.4 MB) and schema-incomplete vs PT/ES

### CZ - Czechia

- Traffic NAP: https://registr.dopravniinfo.cz
- EV source: Ministry of Industry and Trade (MPO) statutory registry (XLSX); link changes per release
- Access: open download
- Finding: open spreadsheet register, not DATEX II via NAP

### DE - Germany

- NAP: https://mobilithek.info
- Format: Bundesnetzagentur / NOW national registry (CSV tables), not DATEX II
- Access: open CDN download (cloud fetches sometimes blocked)
- Finding: large open non-DATEX national dataset

### DK - Denmark

- NAP: https://nap.vd.dk (Dataudveksleren)
- Format: DATEX II v3 / AFIR Energy Infrastructure (per CPO)
- Access: **NAP registration / login** required to discover/use endpoints; partial CPO coverage
- Finding: DATEX II exists, but gated — fails the no-account bar

### EE - Estonia

- NAP: https://peatus.ee
- Format / access: no clear public EV charging DATEX/open feed found
- Finding: not usable yet

### EL - Greece

- NAP: https://nap.gov.gr
- EV source: Ministry electromobility registry (electrokinisi.yme.gov.gr), OCPI JSON (zipped)
- Access: open download
- Finding: open non-DATEX (via ministry registry, not a DATEX NAP dump)

### ES - Spain

- NAP info: https://nap.dgt.es/dataset/puntos-de-recarga-electrica-para-vehiculos
- Static DATEX II: https://nap.dgt.es/datex2/v3/miterd/EnergyInfrastructureTablePublication/electrolineras.xml
- Map of fast chargers (greater than 43 kW): https://www.mapareve.es/mapa-puntos-recarga
- Format: DATEX II v3 EnergyInfrastructureTablePublication
- Access: **open download, no account**
- Finding: meets the open DATEX II bar used in this repo

#### Deployed chargers in the last 30 days

 ![ES_Deployed](data/outputs/ES_Last30DayDeployedChargers.png)
* Chart data source = DGT NAP

### FI - Finland

- NAP: https://finap.fi
- Format: Fintraffic Digitraffic AFIR charging API (GeoJSON)
- Access: open API
- Finding: open non-DATEX national API

### FR - France

- NAP: https://transport.data.gouv.fr
- Static IRVE: https://transport.data.gouv.fr/datasets/base-nationale-des-points-de-recharge-pour-vehicules-electriques-en-france-irve
- Format: national IRVE **CSV** schemas (statique / dynamique) — **no public DATEX II XML** equivalent to PT/ES
- Access: open download
- Finding: strong open national data, wrong format for DATEX-only pipelines until FR publishes DATEX II (EU DATEX obligation from 14 Apr 2026)

### HR - Croatia

- NAP: https://promet-info.hr
- EV source: city/open-data fragments (e.g. Zagreb); NAP itself has little charging coverage
- Access: open downloads where present
- Finding: partial / not a national DATEX charging feed

### HU - Hungary

- NAP: https://napportal.kozut.hu
- Format: DATEX II 3.3 (subscribed datasets, e.g. CPO aggregates)
- Access: **account + per-dataset subscription**
- Finding: DATEX II gated

### IE - Ireland

- Portal: https://data.gov.ie
- Format: operator/council datasets (CSV / GeoJSON), fragmented
- Access: open downloads
- Finding: partial open non-DATEX coverage

### IS - Iceland

- NAPCORE list includes IS; no solid open national DATEX EV dump identified here yet
- Finding: TBD / not confirmed open DATEX II

### IT - Italy

- NAP / PUN: https://cciss.it (Piattaforma Unica Nazionale)
- Format: expected DATEX II; access **login / formal contract**
- Finding: not publicly scrapable

### LI - Liechtenstein

- Listed in this repo for EEA completeness; not highlighted on the NAPCORE NAP table used above
- Finding: TBD

### LT - Lithuania

- Source: https://ev.vialietuva.lt
- Format: OCPI 2.3 JSON API
- Access: open paginated API
- Finding: open non-DATEX

### LU - Luxembourg

- Portal: https://data.public.lu
- Format: Chargy feed (KML)
- Access: API key published in catalog
- Finding: open-ish non-DATEX (key in catalog)

### LV - Latvia

- NAP: https://transportdata.gov.lv
- Format: DATEX II v3.4 (Eco-Movement dataset on NAP)
- Access: **account + dataset key**
- Finding: DATEX II gated

### MT - Malta

- Geoservices / informal map exports; no solid official NAP DATEX charging feed
- Finding: weak / third-party style coverage

### NL - Netherlands

- NAP / NDW: https://ntm.ndw.nu
- Format: NDW GeoJSON + OCPI tariffs
- Access: open download
- Finding: open non-DATEX

### NO - Norway

- Info: https://info.nobil.no/api
- Doc: https://info.nobil.no/images/API-dokumentasjon/API_NOBIL_Documentation_v3_20240603.pdf
- Format: NOBIL API v3 JSON (not DATEX II)
- Access: free API key
- Finding: mature open-ish non-DATEX register; NAPCORE-associated, not EU AFIR-bound the same way

### PL - Poland

- NAP: https://kpd.gddkia.gov.pl
- Format: DATEX II v3.5 (AFI profile) web service
- Access: **formal contract**
- Finding: DATEX II not publicly open

### PT - Portugal

- Static Data (IMT NAP detail): https://nap-portugal.imt-ip.pt/nap/multimodalsupplydetail/148
- Dynamic Data: https://nap-portugal.imt-ip.pt/nap/multimodalsupplydetail/149
- Static DATEX II feed used here: https://pgm.mobie.pt/integration/nap/evChargingInfra
- Mobi.e's chargers map: https://mobie.pt/en/charging/findachargingstation
- Format: DATEX II v3
- Access: **open API/download, no account**
- Finding: meets the open DATEX II bar used in this repo

#### Deployed chargers in the last 30 days

 ![PT_Deployed](data/outputs/PT_Last30DayDeployedChargers.png)
* Chart data source = IMT / Mobi.e

#### Notes on Mobi.e :
During the transition period (until December 31, 2026), Mobi.e will provide data to the official National Access Point (IMT).

Mobi.e's reach and responsibilities extend beyond a NAP, namely it is responsible for activation and financial flows of the charging infrastructure. Mobi.e is a monopoly established by law, as recognized by the national energy regulator ERSE and also a mandatory roaming platform.

 | ![mobie=monopoly](legal/ERSE_Mobie_Monopoly.png) |
 |:--:|
 | *image source: https://www.erse.pt/en/eletric-mobility/functioning/* |

 The monopoly status of Mobi.e can also be verified in the official report on page 180 of the PDF.
- [ERSE Annual Report 2020, copy](legal/ERSE_relatorio_ce_2020_pt.pdf)
- [ERSE Annual Report 2020, online](https://www.erse.pt/media/3cdpftgs/relat%C3%B3rio_ce-2020_pt.pdf)
- Info: https://mobie.pt/en/mobienetwork/finding-charging-points
- Docs: https://www.mobie.pt/en/mobility/technical-rules-procedures


#### Possible barriers for eMobility in Portugal

Portugal set its legal framework for electric mobility in 2010 with Decree-Law 39/2010, creating the RJME and the MOBI.E-based, centrally managed model with defined market roles and incentives, which structured how charging operators and service providers interacted and how a public pilot network would be deployed. Over the years the RJME was amended but kept that centralized architecture as the backbone of the system.

Although initially praised, the Portuguese model later became a source of frustration for EV users, revealed several areas needing urgent improvement, and above all failed to comply with AFIR. This lead some entities to report on the issues or barriers of the Portuguese model, which can still be found below.

#### Autoridade da Concorrência (AdC)

The Portuguese Competition Authority – Autoridade da Concorrência (AdC) carried out an analysis of the competition conditions in the electric vehicle recharging sector, which resulted in the identification of barriers that could jeopardise the development and expansion of an electric vehicle recharging network with adequate, efficient, and competitive coverage.

 ![AdC](legal/AdC_Barriers_Recommendations.jpg)

**Sources**:
- [Main Page EN](https://www.concorrencia.pt/en/public-consultations/public-consultation-study-competition-and-electric-vehicle-recharging-portugal)
- [Main Page PT](https://www.concorrencia.pt/pt/consultas-publicas/consulta-publica-ao-estudo-concorrencia-e-mobilidade-eletrica-em-portugal)
- Complete report on study (Portuguese Only): [AdC Report](legal/Adc_Report.pdf)
- One Pager PT: [AdC One Pager PT, v2](legal/AdC_One_Pager_PT.pdf)
- One Pager EN: [AdC One Pager EN, v1](legal/AdC_One_Pager_EN.pdf)

#### Public consultation on the Study into Competition and Electric Vehicle Recharging in Portugal

This was the AdC's most participated public consultation, which illustrates the high level of interest in this sector. Alongside the opinion of the sector's regulator - ERSE - the AdC received 183 contributions from public entities, individual consumers, consumer associations, operators and associations of companies in the electric mobility sector, entities in the electricity sector and entities from other sectors.

| Num |         Entity        |   PDF
|-----|-----------------------|-----------
|  1  | AMME                  | [pdf](legal/AdC%20Contribs/Contributo%20Amme.pdf)
|  2  | ANMP                  | [pdf](legal/AdC%20Contribs/Contributo%20ANMP.pdf)
|  3  | APOCME                | [pdf](legal/AdC%20Contribs/contributo%20Apocme.pdf)
|  4  | APREN                 | [pdf](legal/AdC%20Contribs/Contributo%20Apren.pdf)
|  5  | ASFAC                 | [pdf](legal/AdC%20Contribs/Contributo%20ASFAC.pdf.pdf)
|  6  | AVERE                 | [pdf](legal/AdC%20Contribs/Contributo%20Avere.pdf.pdf)
|  7  | CM Odivelas           | [pdf](legal/AdC%20Contribs/Contributo%20CM%20Odivelas.pdf)
|  8  | DECO                  | [pdf](legal/AdC%20Contribs/Contributo%20DECO.pdf)
|  9  | DGC                   | [pdf](legal/AdC%20Contribs/Contributo%20DGC.pdf)
|  10 | EDP                   | [pdf](legal/AdC%20Contribs/Contributo%20Edp.pdf)
|  11 | Elergone energia      | [pdf](legal/AdC%20Contribs/Contributo%20Elergone%20energia.pdf)
|  12 | EMEL                  | [pdf](legal/AdC%20Contribs/Contributo%20Emel.pdf)
|  13 | Endesa                | [pdf](legal/AdC%20Contribs/Contributo%20Endesa.pdf)
|  14 | ENSE                  | [pdf](legal/AdC%20Contribs/Contributo%20Ense.pdf)
|  15 | E-Redes               | [pdf](legal/AdC%20Contribs/Contributo%20E-Redes.pdf)
|  16 | EVIO                  | [pdf](legal/AdC%20Contribs/Contributo%20Evio.pdf)
|  17 | Galp                  | [pdf](legal/AdC%20Contribs/Contributo%20Galp.pdf)
|  18 | Helexia               | [pdf](legal/AdC%20Contribs/Contributo%20Helexia.pdf)
|  19 | Iberdrola- BP Pulse   | [pdf](legal/AdC%20Contribs/Contributo%20Iberdrola-%20BP%20Pulse.pdf)
|  20 | Iberdrola             | [pdf](legal/AdC%20Contribs/Contributo%20Iberdrola.pdf)
|  21 | IMT                   | [pdf](legal/AdC%20Contribs/Contributo%20IMT.pdf)
|  22 | miio                  | [pdf](legal/AdC%20Contribs/Contributo%20miio.pdf)
|  23 | MOBI.E                | [pdf](legal/AdC%20Contribs/Contributo%20Mobi.E.pdf)
|  24 | Renewing              | [pdf](legal/AdC%20Contribs/Contributo%20Renewing.pdf)
|  25 | Tesla                 | [pdf](legal/AdC%20Contribs/Contributo%20Tesla.pdf)
|  26 | UVE                   | [pdf](legal/AdC%20Contribs/Contributo%20UVE.pdf)
|  27 | ERSE                  | [pdf](legal/AdC%20Contribs/Parecer%20ERSE.pdf)


#### AVERE

AVERE has taken note of the preliminary report of the Estudo concorrência e mobilidade elétrica em Portugal and wish to express our agreement with the intention of the recommendations made to the Portuguese government to make fundamental changes to the Portuguese recharging network, to improve the current system in benefit of BEV users.

- [Blog Page](https://www.avere.org/blogpages/policy-details/2024/03/05/AVEREs-Reaction-Letter-to-the-Report-on-Recharging-Network-Published-by-the-Portuguese-Competition-Authority) * Now unavailable due to site restructuring, check it in the [Internet Archive](https://web.archive.org/web/20240422192745/https://www.avere.org/blogpages/policy-details/2024/03/05/AVEREs-Reaction-Letter-to-the-Report-on-Recharging-Network-Published-by-the-Portuguese-Competition-Authority)
- Reaction Letter: [AVERE's Reaction Letter](legal/AVERE_Reaction_Letter_AdC.pdf)

### RO - Romania

- Portal fragments: https://data.gov.ro (e.g. PNRR-financed stations by municipality)
- Format: XLSX aggregates
- Access: open download
- Finding: partial open non-DATEX; not a full national DATEX NAP dump

### SE - Sweden

- NAP: https://trafficdata.se
- Format: NOBIL API v3 JSON
- Access: free API key
- Finding: open-ish non-DATEX (same NOBIL family as NO)

### SI - Slovenia

- NAP: https://nap.si
- Format: DATEX II v3.6 / TPEG EMI (EV charging)
- Access: **account registration**
- Finding: DATEX II gated

### SK - Slovakia

- NAP: https://ndsas.sk
- Format / access: no usable public EV charging DATEX/open feed found
- Finding: not usable yet

### UK - United Kingdom

- Listed on NAPCORE NAP table; **not EU AFIR-bound** (post-Brexit). Domestic rules: [Public Charge Point Regulations 2023](https://www.legislation.gov.uk/uksi/2023/1168/contents/made)
- **Former national dump:** [National Chargepoint Registry (NCR)](https://www.gov.uk/guidance/find-and-use-data-on-public-electric-vehicle-chargepoints) — CSV/JSON/XML + API, **no login** — **decommissioned 28 Nov 2024**. Archive on request via `consumerofferconsult@ozev.gov.uk`
- **Current model:** no government replacement aggregate open dataset. Each public CPO must publish **reference + availability** data free of charge in a machine-readable form aligned with **OCPI** (no T&Cs barrier). Feeds are **per operator**, not one national DATEX/NAP XML
- Operator feed lists / health: [OpenStreetMap UK EV open-data list](https://wiki.openstreetmap.org/wiki/EV_charge_points_in_the_United_Kingdom), [ChargerStatus feed health](https://www.chargerstatus.com/feed-health/)
- Official statistics (aggregated, not a raw station dump): DfT EV charging statistics (often via Zapmap)
- Finding: **no single open national DATEX/XML source** like PT/ES; UK is a **federated OCPI open-data** landscape after NCR closure

## DATEX II Documentation

- [Official Documentation](https://docs.datex2.eu/)
- [Energy Infrastructure Diagrams](https://docs.datex2.eu/levels/mastering/energy/)
