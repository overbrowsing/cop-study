# An Analysis of UNFCCC COP Host Country Websites (1995–2024)

## Overview

This repository contains the code for the study *[The Environmental Impact of COP Websites: An Analysis of UNFCCC COP Host Country Websites (1995-2024)]()*. The study evaluates the potential growth and environmental impact of COP host country websites by analysing webpage size and composition. We use the Wayback Machine to retrieve webpages and the [Website Carbon API](https://api.websitecarbon.com) to calculate CO₂e emissions, which uses v3 of the [Sustainable Web Design Model](https://sustainablewebdesign.org/estimating-digital-emissions/), a collaborative open-source initiative.

The Python script developed for this study utilises Playwright to load pages within Chromium and capture resource sizes. Since the [Wayback Machine's API](https://web.archive.org/web/20130329115724/http://faq.web.archive.org/page-without-wayback-code/) for viewing unmodified webpages does not account for content delivered by third parties or CDNs, it was not possible to use it for calculating the total webpage size. We account for the additional size introduced by the Wayback Machine's archiving process, as well as the resources and scripts included by the Wayback Machine that may not have been present on the original site. For further details, please refer to the research paper (Section 4.7) for a complete description of our data collection and standardisation methodology.

## Dataset

The URLs of COP host country websites were retrieved using the Wayback Machine, regardless of whether the site was still active. The earliest available snapshot from the event's start date was selected, or the closest alternative if none was available, excluding those marked as green in the Wayback Machine interface, which indicate redirects (3xx). The snapshot date was recorded in the dataset. This approach ensures that websites are assessed at their peak operational state, as some may be updated throughout the conference. For instance, the COP28 host country website was modified following [media scrutiny](https://www.abc.net.au/news/2023-10-31/un-cop28-climate-summit-accused-greenwashing-website-low-carbon/103020978).

Attendee figures are sourced from the [UNFCCC's COP in-session participant data](https://unfccc.int/process-and-meetings/parties-non-party-stakeholders/non-party-stakeholders/statistics-on-non-party-stakeholders/statistics-on-participation-and-in-session-engagement).

| **COP**   | Host Country                           | Event Date              | Attendees  | COP Host Country Website                                                                                         | Still Active?                                             |
|-----------|----------------------------------------|-------------------------|------------|------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| **COP1**  | 🇩🇪 Berlin, Germany                      | 28.03.1995 - 07.04.1995 | 3,969      | *No website found*                                                                                               | *No website found*                                        |
| **COP2**  | 🇨🇭 Geneva, Switzerland                  | 08.07.1996 - 19.07.1996 | 1,584      | *No website found*                                                                                               | *No website found*                                        |
| **COP3**  | 🇯🇵 Kyoto, Japan                         | 01.12.1997 - 11.12.1997 | 9,850      | [Snapshot 04.06.2003](https://web.archive.org/web/20030604214733if_/unfccc.int/cop3/)                            | [Yes](https://unfccc.int/cop3)                            |
| **COP4**  | 🇦🇷 Buenos Aires, Argentina              | 02.11.1998 - 13.11.1998 | 4,941      | [Snapshot 01.10.2003](https://web.archive.org/web/20031001073646if_/unfccc.int/cop4/)                            | [Yes](https://unfccc.int/cop4)                            |
| **COP5**  | 🇩🇪 Bonn, Germany                        | 25.10.1999 - 05.11.1999 | 4,188      | [Snapshot 18.06.2003](https://web.archive.org/web/20030618164207if_/unfccc.int/cop5/)                            | [Yes](https://unfccc.int/cop5)                            |
| **COP6**  | 🇳🇱 The Hague, Netherlands               | 13.11.2000 - 24.11.2000 | 6,994      | [Snapshot 05.06.2003](https://web.archive.org/web/20030605042026if_/unfccc.int/cop6/)                            | [Yes](https://unfccc.int/cop6)                            |
| **COP7**  | 🇲🇦 Marrakech, Morocco                   | 29.10.2001 - 10.11.2001 | 4,460      | [Snapshot 19.11.2001](https://web.archive.org/web/20011205115501if_/unfccc.int/cop7/)                            | [Yes](https://unfccc.int/cop7)                            |
| **COP8**  | 🇮🇳 New Delhi, India                     | 23.10.2002 - 01.11.2002 | 4,352      | [Snapshot 09.12.2002](https://web.archive.org/web/20030410192139if_/unfccc.int/cop8/)                            | [Yes](https://unfccc.int/cop8)                            |
| **COP9**  | 🇮🇹 Milan, Italy                         | 01.12.2003 - 12.12.2003 | 5,151      | [Snapshot 27.11.2003](https://web.archive.org/web/20031127040856if_/unfccc.int/cop9/)                            | [Yes](https://unfccc.int/cop9)                            |
| **COP10** | 🇦🇷 Buenos Aires, Argentina              | 06.12.2004 - 17.12.2004 | 6,151      | [Snapshot 04.12.2024](https://web.archive.org/web/20041204134444if_/cop10.medioambiente.gov.ar/en/default.asp)   | [No](https://cop10.medioambiente.gov.ar/en/default.asp)   |
| **COP11** | 🇨🇦 Montreal, Canada                     | 28.11.2005 - 09.12.2005 | 9,474      | [Snapshot 12.02.2006](https://web.archive.org/web/20060212181228if_/montreal2005.gc.ca/)                         | [No](https://montreal2005.gc.ca)                          |
| **COP12** | 🇰🇪 Nairobi, Kenya                       | 06.11.2006 - 17.11.2006 | 5,948      | [Snapshot 05.11.2006](https://web.archive.org/web/20061105123100if_/nairobi2006.go.ke/)                          | [No](https://nairobi2006.go.ke)                           |
| **COP13** | 🇮🇩 Bali, Indonesia                      | 03.12.2007 - 15.12.2007 | 10,829     | [Snapshot 24.12.2007](https://web.archive.org/web/20071224045128if_/climate.web.id/welcome)                      | [No](https://climate.web.id)                              |
| **COP14** | 🇵🇱 Poznań, Poland                       | 01.12.2008 - 12.12.2008 | 9,249      | [Snapshot 02.12.2008](https://web.archive.org/web/20081202104529if_/cop14.gov.pl/)                               | [No](https://cop14.gov.pl)                                |
| **COP15** | 🇩🇰 Copenhagen, Denmark                  | 07.12.2009 - 18.12.2009 | 27,294     | [Snapshot 09.12.2009](https://web.archive.org/web/20091209152318if_/en.cop15.dk/)                                | [No](https://en.cop15.dk)                                 |
| **COP16** | 🇲🇽 Cancún, Mexico                       | 29.11.2010 - 10.12.2010 | 11,848     | [Snapshot 07.12.2010](https://web.archive.org/web/20101207041810if_/cc2010.mx/en/)                               | [No](https://cc2010.mx)                                   |
| **COP17** | 🇿🇦 Durban, South Africa                 | 28.11.2011 - 09.12.2011 | 13,397     | [Snapshot 28.11.2011](https://web.archive.org/web/20111128174848if_/cop17-cmp7durban.com/)                       | [No](https://cop17-cmp7durban.com/)                       |
| **COP18** | 🇶🇦 Doha, Qatar                          | 26.11.2012 - 08.12.2012 | 9,004      | [Snapshot 27.11.2012](https://web.archive.org/web/20121127234132if_/cop18.qa/)                                   | [No](https://cop18.qa/)                                   |
| **COP19** | 🇵🇱 Warsaw, Poland                       | 11.11.2013 - 23.11.2013 | 8,375      | [Snapshot 23.11.2013](https://web.archive.org/web/20131123041818if_/cop19.gov.pl/)                               | [No](https://cop19.gov.pl)                                |
| **COP20** | 🇵🇪 Lima, Peru                           | 01.12.2014 - 12.12.2014 | 11,175     | [Snapshot 01.12.2014](https://web.archive.org/web/20141201124431if_/cop20.pe/)                                   | [No](https://cop20.pe)                                    |
| **COP21** | 🇫🇷 Paris, France                        | 30.11.2015 - 12.12.2015 | 28,187     | [Snapshot 10.12.2015](https://web.archive.org/web/20151210193304if_/cop21.gouv.fr/)                              | [No](https://cop21.gouv.fr)                               |
| **COP22** | 🇲🇦 Marrakech, Morocco                   | 07.11.2016 - 18.11.2016 | 22,564     | [Snapshot 16.11.2016](https://web.archive.org/web/20161116144643if_/cop22-morocco.com/)                          | [No](https://cop22-morocco.com)                           |
| **COP23** | 🇫🇯 Fiji (Hosted by Germany)             | 06.11.2017 - 17.11.2017 | 16,028     | [Snapshot 08.11.2017](https://web.archive.org/web/20171105004203if_/cop23.com.fj/)                               | [No](https://cop23.com.fj)                                |
| **COP24** | 🇵🇱 Katowice, Poland                     | 02.12.2018 - 14.12.2018 | 18,856     | [Snapshot 02.12.2018](https://web.archive.org/web/20181202112300if_/cop24.gov.pl/)                               | [No](https://cop24.gov.pl)                                |
| **COP25** | 🇪🇸 Spain (Hosted by Chile)              | 02.12.2019 - 13.12.2019 | 22,354     | [Snapshot 06.12.2019](https://web.archive.org/web/20191206011858if_/cop25.cl/#/)                                 | [No](https://cop25.cl)                                    |
| **COP26** | 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Glasgow, Scotland                    | 31.10.2021 - 12.11.2021 | 30,501     | [Snapshot 31.10.2021](https://web.archive.org/web/20201031095434if_/ukcop26.org/)                                | [No](https://ukcop26.org) 🌱                               |
| **COP27** | 🇪🇬 Sharm El-Sheikh, Egypt               | 06.11.2022 - 18.11.2022 | 36,674     | [Snapshot 06.11.2022](https://web.archive.org/web/20221106043724if_/cop27.eg/#/)                                 | [No](https://cop27.eg) 🌱                                  |
| **COP28** | 🇦🇪 Dubai, United Arab Emirates          | 30.11.2023 - 12.12.2023 | 70,002     | [Snapshot 30.11.2023](https://web.archive.org/web/20231130020512if_/cop28.com/)                                  | [No](https://cop28.com) 🌱                                 |
| **COP29** | 🇦🇿 Baku, Azerbaijan                     | 11.11.2024 - 22.11.2024 | 40,335     | [Snapshot 11.11.2024](https://web.archive.org/web/20241111035138if_/cop29.az/en/home)                            | [Yes](https://cop29.az) 🌱                                 |

*🌱 Marks websites hosted on renewable energy, checked via [The Green Web Foundation](https://thegreenwebfoundation.org) or inferred from available sources.*

## How to Repeat the Study

### Prerequisites

- Python installed on your machine.

### Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/overbrowsing/cop-study
    cd cop-study
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install Playwright**:
    ```bash
    playwright install
    ```

4. **Run the Python Scripts**:

    #### Full Page Size and CO₂ Emissions
    **[`run.py`](/scripts/run.py)**: This script calculates the size of each webpage listed in the [`dataset.csv`](/data/dataset.csv) file and saves the results as a CSV file titled [`results.csv`](/data/results.csv), located in the [`data`](/data/) directory. The script will also generate a chart based on the final CO₂e emissions results.

    ```bash
    python run.py
    ```

## Contributing

Contributions are welcome. Please feel free to [submit an issue](https://github.com/overbrowsing/cop-study/issues) or a [pull request](https://github.com/overbrowsing/cop-study/pulls).

## License

cop-study is released under the [MIT](/LICENSE) license. Feel free to use and modify it as needed.