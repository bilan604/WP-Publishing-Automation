import re
import json
import requests
import asyncio
from bs4 import BeautifulSoup
from parsing import *
from analyzer import get_GPT_statistics_task
import time

testing_serp_response = {
  "request_info": {
    "success": True,
    "topup_credits_remaining": 83,
    "credits_used_this_request": 1
  },
  "search_parameters": {
    "q": "webinar statistics",
    "num": "50",
    "page": "1",
    "max_page": "1",
    "engine": "google"
  },
  "search_metadata": {
    "created_at": "2023-05-11T15:16:03.483Z",
    "processed_at": "2023-05-11T15:16:08.046Z",
    "total_time_taken": 4.56,
    "pages": [
      {
        "created_at": "2023-05-11T15:16:03.483Z",
        "processed_at": "2023-05-11T15:16:08.046Z",
        "total_time_taken": 4.56,
        "page": "1",
        "engine_url": "https://www.google.com/search?q=webinar+statistics&num=50",
        "html_url": "https://api.valueserp.com/search?api_key=0AC5DF2CE3CF44358E2B0F41673DA756&q=webinar+statistics&num=50&page=1&max_page=1&engine=google&output=html",
        "json_url": "https://api.valueserp.com/search?api_key=0AC5DF2CE3CF44358E2B0F41673DA756&q=webinar+statistics&num=50&page=1&max_page=1&engine=google&output=json"
      }
    ]
  },
  "search_information": {
    "original_query_yields_zero_results": False,
    "search_tabs": [
      {
        "position": 1,
        "text": "Immagini",
        "link": "https://www.google.com/search?q=webinar+statistics&num=50&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q_AUoAXoECAEQAw"
      },
      {
        "position": 2,
        "text": "Notizie",
        "link": "https://www.google.com/search?q=webinar+statistics&num=50&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q_AUoAnoECAEQBA"
      },
      {
        "position": 3,
        "text": "Video",
        "link": "https://www.google.com/search?q=webinar+statistics&num=50&source=lnms&tbm=vid&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q_AUoA3oECAEQBQ"
      },
      {
        "position": 4,
        "text": "Libri",
        "link": "https://www.google.com/search?q=webinar+statistics&num=50&source=lnms&tbm=bks&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q_AUoBHoECAEQBg"
      }
    ],
    "total_results": 388000000,
    "time_taken_displayed": 0.65,
    "detected_location": "Italia"
  },
  "answer_box": {
    "answer_box_type": 18,
    "answers": [
      {
        "source": {
          "link": "https://thrivemyway.com/webinar-stats/#:~:text=Webinar%20Registrations%20Statistics%202023,one%20week%20of%20the%20event.",
          "title": "Amazing Webinar Stats 2023 [Trends, Benchmarks and Facts]",
          "displayed_link": "https://thrivemyway.com › Statistics",
          "date": " The average number of registrants for a webinar is 260. On average, you can expect 40% to 50% attendance rates. In general, 54% of people sign up at least eight days before an event. 46% of registrations take place within one week of the event.",
          "date_utc": "2023-04-30T19:16:07.513Z"
        },
        "answer": "Webinar Registrations Statistics 2023 The average number of registrants for a webinar is 260. On average, you can expect 40% to 50% attendance rates. In general, 54% of people sign up at least eight days before an event. 46% of registrations take place within one week of the event."
      }
    ],
    "block_position": 1
  },
  "related_searches": [
    {
      "query": "webinar statistics 2023",
      "link": "https://www.google.com/search?num=50&q=Webinar+statistics+2023&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q1QJ6BQjZARAB",
      "type": "standard"
    },
    {
      "query": "zoom webinar statistics",
      "link": "https://www.google.com/search?num=50&q=Zoom+webinar+statistics&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q1QJ6BQjYARAB",
      "type": "standard"
    },
    {
      "query": "what is a good webinar attendance rate",
      "link": "https://www.google.com/search?num=50&q=What+is+a+good+webinar+attendance+rate&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q1QJ6BQjVARAB",
      "type": "standard"
    },
    {
      "query": "how to calculate webinar attendance rate",
      "link": "https://www.google.com/search?num=50&q=How+to+calculate+webinar+attendance+rate&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q1QJ6BQjSARAB",
      "type": "standard"
    },
    {
      "query": "on24 webinar statistics",
      "link": "https://www.google.com/search?num=50&q=ON24+webinar+statistics&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q1QJ6BQjPARAB",
      "type": "standard"
    },
    {
      "query": "webinar conversion rates",
      "link": "https://www.google.com/search?num=50&q=Webinar+conversion+rates&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q1QJ6BQjOARAB",
      "type": "standard"
    },
    {
      "query": "webinar frequency",
      "link": "https://www.google.com/search?num=50&q=Webinar+frequency&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q1QJ6BQjNARAB",
      "type": "standard"
    },
    {
      "query": "popular webinars",
      "link": "https://www.google.com/search?num=50&q=Popular+webinars&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q1QJ6BQjLARAB",
      "type": "standard"
    }
  ],
  "related_questions": [
    {
      "question": "What is the success rate of webinars?",
      "answer": "The average webinar receives almost 260 registrations, meaning that between 100-110 of those who register would actually show up to the event, and just over 40 would stay for the entire event. What is the average conversion rate for a webinar? The average webinar attendee conversion rate is 55%.",
      "source": {
        "link": "https://www.zippia.com/advice/webinar-statistics/#:~:text=The%20average%20webinar%20receives%20almost%20260%20registrations%2C%20meaning%20that%20between,attendee%20conversion%20rate%20is%2055%25.",
        "displayed_link": "https://www.zippia.com › advice › webinar-statistics",
        "title": "25 Webinar Statistics [2023]: The Average Attendance Rate ..."
      },
      "search": {
        "link": "https://www.google.com/search?num=50&q=What+is+the+success+rate+of+webinars%3F&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Qzmd6BAgoEAY",
        "title": "What is the success rate of webinars?"
      },
      "block_position": 5
    },
    {
      "question": "What are the statistics for webinar in 2023?",
      "answer": "Key Webinar Statistics 2023 – MY Choice 20-40% of webinar attendees are going to turn into qualified leads. 54% of attendees sign-up eight days before a webinar launches. 60-minute webinars attract more attendees than 30-minute webinars. 61% of marketers use webinars as a tactic for their content marketing strategy.",
      "source": {
        "link": "https://abdalslam.com/webinar-statistics#:~:text=Key%20Webinar%20Statistics%202023%20%E2%80%93%20MY%20Choice,-The%20webinar%20market&text=20%2D40%25%20of%20webinar%20attendees,for%20their%20content%20marketing%20strategy.",
        "displayed_link": "https://abdalslam.com › Blog page › Statistics",
        "title": "Webinar Statistics, Trends and Facts 2023 - Abdalslam"
      },
      "search": {
        "link": "https://www.google.com/search?num=50&q=What+are+the+statistics+for+webinar+in+2023%3F&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Qzmd6BAgpEAY",
        "title": "What are the statistics for webinar in 2023?"
      },
      "block_position": 5
    },
    {
      "question": "What are the statistics for webinar registration?",
      "answer": "Webinar Registration Statistics",
      "source": {
        "link": "https://www.demandsage.com/webinar-statistics/",
        "displayed_link": "https://www.demandsage.com › Latest Blog Posts",
        "title": "76 Webinar Statistics For 2023 (Attendance Rate & Trends)"
      },
      "search": {
        "link": "https://www.google.com/search?num=50&q=What+are+the+statistics+for+webinar+registration%3F&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Qzmd6BAgsEAY",
        "title": "What are the statistics for webinar registration?"
      },
      "block_position": 5
    },
    {
      "question": "Are webinars still effective?",
      "answer": "Webinars aren't only used for content marketing and lead generation tactics, they're actually extremely useful when it comes to training and development within businesses.",
      "source": {
        "link": "https://bloggingwizard.com/webinar-statistics/#:~:text=Webinars%20aren't%20only%20used,training%20and%20development%20within%20businesses.",
        "displayed_link": "https://bloggingwizard.com › webinar-statistics",
        "title": "25 Latest Webinar Statistics And Trends For 2023"
      },
      "search": {
        "link": "https://www.google.com/search?num=50&q=Are+webinars+still+effective%3F&sa=X&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Qzmd6BAghEAY",
        "title": "Are webinars still effective?"
      },
      "block_position": 5
    }
  ],
  "pagination": {
    "pages": [
      {
        "current": 1,
        "next": "https://www.google.com/search?q=webinar+statistics&num=50&ei=tAZdZN22CpmjqtsP6JKX8AM&start=50&sa=N&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q8NMDegQIBhAM",
        "other_pages": [
          {
            "page": 2,
            "link": "https://www.google.com/search?q=webinar+statistics&num=50&ei=tAZdZN22CpmjqtsP6JKX8AM&start=50&sa=N&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q8tMDegQIBhAE"
          },
          {
            "page": 3,
            "link": "https://www.google.com/search?q=webinar+statistics&num=50&ei=tAZdZN22CpmjqtsP6JKX8AM&start=100&sa=N&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q8tMDegQIBhAG"
          },
          {
            "page": 4,
            "link": "https://www.google.com/search?q=webinar+statistics&num=50&ei=tAZdZN22CpmjqtsP6JKX8AM&start=150&sa=N&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q8tMDegQIBhAI"
          },
          {
            "page": 5,
            "link": "https://www.google.com/search?q=webinar+statistics&num=50&ei=tAZdZN22CpmjqtsP6JKX8AM&start=200&sa=N&ved=2ahUKEwjd4Kq8x-3-AhWZkWoFHWjJBT4Q8tMDegQIBhAK"
          }
        ],
        "api_pagination": {
          "next": "https://api.valueserp.com/search?api_key=0AC5DF2CE3CF44358E2B0F41673DA756&q=webinar%20statistics&max_page=1&id=req0&page=2&num=50",
          "other_pages": [
            {
              "page": 2,
              "link": "https://api.valueserp.com/search?api_key=0AC5DF2CE3CF44358E2B0F41673DA756&q=webinar%20statistics&max_page=1&id=req0&page=2&num=50"
            },
            {
              "page": 3,
              "link": "https://api.valueserp.com/search?api_key=0AC5DF2CE3CF44358E2B0F41673DA756&q=webinar%20statistics&max_page=1&id=req0&page=3&num=50"
            },
            {
              "page": 4,
              "link": "https://api.valueserp.com/search?api_key=0AC5DF2CE3CF44358E2B0F41673DA756&q=webinar%20statistics&max_page=1&id=req0&page=4&num=50"
            },
            {
              "page": 5,
              "link": "https://api.valueserp.com/search?api_key=0AC5DF2CE3CF44358E2B0F41673DA756&q=webinar%20statistics&max_page=1&id=req0&page=5&num=50"
            }
          ]
        }
      }
    ]
  },
  "organic_results": [
    {
      "position": 1,
      "title": "Webinar Statistics: The Definitive List in 2023 - Luisa Zhou",
      "link": "https://www.luisazhou.com/blog/webinar-statistics/",
      "domain": "www.luisazhou.com",
      "displayed_link": "https://www.luisazhou.com › blog",
      "snippet": "7 mar 2023 — Almost 60% of webinar attendees watch live webinars while only 5% watch both live and on-demand. 36% of attendees watch always-on webinars. 31.",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:PUAwBiCjeQUJ:https://www.luisazhou.com/blog/webinar-statistics/&cd=5&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>webinars</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "rich_snippet": {
        "top": {
          "detected_extensions": {},
          "attributes": [
            {
              "name": "Number of webinars/year",
              "value": "Percentage"
            },
            {
              "name": "150 webinars",
              "value": "86%"
            },
            {
              "name": "50 webinars",
              "value": "57%"
            }
          ],
          "attributes_flat": "Number of webinars/year: Percentage, 150 webinars: 86%, 50 webinars: 57%"
        }
      },
      "date": "7 mar 2023",
      "date_utc": "2023-03-07T00:00:00.000Z",
      "block_position": 4,
      "page": "1",
      "position_overall": 1
    },
    {
      "position": 2,
      "title": "26 Webinar Statistics to Know in 2023 - 99Firms",
      "link": "https://99firms.com/blog/webinar-statistics/",
      "domain": "99firms.com",
      "displayed_link": "https://99firms.com › blog › we...",
      "snippet": "80% of organizations hosting training webinars produce as many as 100 webinars per year, while a total of 93% of webinars for continuing education are organized ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:qZXXQBzv_ZQJ:https://99firms.com/blog/webinar-statistics/&cd=15&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>webinars</b>",
          "Altri siti web con i tuoi termini di ricerca <span>rimandano</span> a questo risultato",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 6,
      "page": "1",
      "position_overall": 2
    },
    {
      "position": 3,
      "title": "22 Stats that Make a Case for Using Webinars in Your ...",
      "link": "https://blog.hubspot.com/marketing/webinar-stats",
      "domain": "blog.hubspot.com",
      "displayed_link": "https://blog.hubspot.com › webi...",
      "snippet": "13 apr 2021 — 67% of marketers in 2020 were increasing their investment in webinars. · The global webinar market is estimated to reach 800 million by 2023, up ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:hbQ44R9SS7gJ:https://blog.hubspot.com/marketing/webinar-stats&cd=16&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Alcuni <span>termini</span> correlati alla tua ricerca compaiono nel risultato: <b> webinars</b>, <b>stats</b>",
          "Altri siti web con i tuoi termini di ricerca <span>rimandano</span> a questo risultato",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "date": "13 apr 2021",
      "date_utc": "2021-04-13T00:00:00.000Z",
      "block_position": 7,
      "page": "1",
      "position_overall": 3
    },
    {
      "position": 4,
      "title": "39 Webinar Statistics 2023 – Effectiveness, Attendance and All",
      "link": "https://webinarcare.com/webinar-statistics/",
      "domain": "webinarcare.com",
      "displayed_link": "https://webinarcare.com › webin...",
      "snippet": "di S Bennett · 2023 — 1. As per the market study, the percentage of webinar attendees is 40-50% approximately. In the case of B2B marketers, the average webinar ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:ok4IR1xTbacJ:https://webinarcare.com/webinar-statistics/&cd=17&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Questo risultato è stato pubblicato o aggiornato <span>di recente</span>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "rich_snippet": {
        "top": {
          "detected_extensions": {},
          "extensions": [
            "di S Bennett",
            "2023 —"
          ]
        }
      },
      "date": "di S Bennett · 2023",
      "date_utc": "2023-01-01T00:00:00.000Z",
      "block_position": 8,
      "page": "1",
      "position_overall": 4
    },
    {
      "position": 5,
      "title": "Webinar Statistics | Livestorm",
      "link": "https://livestorm.co/webinar-statistics",
      "domain": "livestorm.co",
      "displayed_link": "https://livestorm.co › webinar-st...",
      "snippet": "Webinar statistics from thousands of webinars hosted with Livestorm. Understand how your webinars fare against industry standards.",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:WR116QDtbuMJ:https://livestorm.co/webinar-statistics&cd=18&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Altri siti web con i tuoi termini di ricerca <span>rimandano</span> a questo risultato",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "rich_snippet": {
        "top": {
          "detected_extensions": {
            "rating": 8.9,
            "reviews": 982
          }
        }
      },
      "block_position": 9,
      "page": "1",
      "position_overall": 5
    },
    {
      "position": 6,
      "title": "Webinar statistics 2022 - 70+ stats you need to know",
      "link": "https://www.livewebinar.com/blog/webinar-marketing/webinar-statistics-2021-70-webinar-stats-you-need-to-know",
      "domain": "www.livewebinar.com",
      "displayed_link": "https://www.livewebinar.com › ...",
      "snippet": "12 ott 2021 — In B2C webinars, the lead generation survey shows 20% to 40% (Webinar Care). 58% of B2B marketers use webinars as promotional tools (Content ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:Op4iE3ds6UwJ:https://www.livewebinar.com/blog/webinar-marketing/webinar-statistics-2021-70-webinar-stats-you-need-to-know&cd=19&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>stats</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "date": "12 ott 2021",
      "date_utc": "2021-10-12T00:00:00.000Z",
      "block_position": 10,
      "page": "1",
      "position_overall": 6
    },
    {
      "position": 7,
      "title": "25 Latest Webinar Statistics And Trends For 2023",
      "link": "https://bloggingwizard.com/webinar-statistics/",
      "domain": "bloggingwizard.com",
      "displayed_link": "https://bloggingwizard.com › we...",
      "snippet": "1 gen 2023 — The overall percentage of marketers distributing webinars increased from 46% to 62% between 2019 and 2020. Source: Wyzowl. 23. …and were rated ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:JiPudhti3u8J:https://bloggingwizard.com/webinar-statistics/&cd=20&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>webinars</b>",
          "Altri siti web con i tuoi termini di ricerca <span>rimandano</span> a questo risultato",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "prefix": "1 gen 2023",
      "block_position": 11,
      "page": "1",
      "position_overall": 7
    },
    {
      "position": 8,
      "title": "76 Webinar Statistics For 2023 (Attendance Rate & Trends)",
      "link": "https://www.demandsage.com/webinar-statistics/",
      "domain": "www.demandsage.com",
      "displayed_link": "https://www.demandsage.com › ...",
      "snippet": "8 mar 2023 — The conversion rate of communication webinars is 67.05% as of 2023. 95% of organizations say the webinar is a vital strategy for their marketing ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:uxrKY93BSJgJ:https://www.demandsage.com/webinar-statistics/&cd=21&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>webinars</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "rich_snippet": {
        "top": {
          "detected_extensions": {},
          "attributes": [
            {
              "name": "Training Webinars",
              "value": "44.79%"
            },
            {
              "name": "Marketing Webinars",
              "value": "39.10%"
            },
            {
              "name": "Education Webinars",
              "value": "30.79%"
            },
            {
              "name": "Communication Webinars",
              "value": "67.05%"
            }
          ],
          "attributes_flat": "Training Webinars: 44.79%, Marketing Webinars: 39.10%, Education Webinars: 30.79%, Communication Webinars: 67.05%"
        }
      },
      "date": "8 mar 2023",
      "date_utc": "2023-03-08T00:00:00.000Z",
      "block_position": 12,
      "page": "1",
      "position_overall": 8
    },
    {
      "position": 9,
      "title": "29+ Powerful Webinar Statistics, Facts & Trends for 2021",
      "link": "https://findstack.com/resources/webinar-statistics/",
      "domain": "findstack.com",
      "displayed_link": "https://findstack.com › resources",
      "snippet": "Webinar Statistics — Editor's Choice. The average attendance rate is between 40% to 50%. Most people register 8 days before the event. 60% of businesses ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:nWf2xiqn2YEJ:https://findstack.com/resources/webinar-statistics/&cd=22&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>facts</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "prefix": "Webinar Statistics",
      "block_position": 13,
      "page": "1",
      "position_overall": 9
    },
    {
      "position": 10,
      "title": "The Ultimate List of Webinar Statistics for 2023",
      "link": "https://www.growthmarketingpro.com/ultimate-list-of-webinar-statistics/",
      "domain": "www.growthmarketingpro.com",
      "displayed_link": "https://www.growthmarketingpro.com › ...",
      "snippet": "22 feb 2022 — Webinar Engagement Stats · 9. 65% of people register via email for a webinar · 10. Webinars convert between 5% and 20% of viewers to buyers · 11.",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:JIyBYrhcRCoJ:https://www.growthmarketingpro.com/ultimate-list-of-webinar-statistics/&cd=23&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Alcuni <span>termini</span> correlati alla tua ricerca compaiono nel risultato: <b> webinars</b>, <b>stats</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "date": "22 feb 2022",
      "date_utc": "2022-02-22T00:00:00.000Z",
      "block_position": 14,
      "page": "1",
      "position_overall": 10
    },
    {
      "position": 11,
      "title": "22 webinar statistics: what makes a successful webinar?",
      "link": "https://www.ringcentral.com/us/en/blog/webinar-statistics/",
      "domain": "www.ringcentral.com",
      "displayed_link": "https://www.ringcentral.com › w...",
      "snippet": "1 lug 2020 — The average webinar registration page conversion rate is 30% for cold traffic. ... How far out people sign up to your webinar will depend in large ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:MGw9405dUPQJ:https://www.ringcentral.com/us/en/blog/webinar-statistics/&cd=24&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Altri siti web con i tuoi termini di ricerca <span>rimandano</span> a questo risultato",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "date": "1 lug 2020",
      "date_utc": "2020-07-01T00:00:00.000Z",
      "block_position": 15,
      "page": "1",
      "position_overall": 11
    },
    {
      "position": 12,
      "title": "35+ Webinar Statistics & Data (2023) - SupplyGem",
      "link": "https://supplygem.com/publications/webinar-statistics/",
      "domain": "supplygem.com",
      "displayed_link": "https://supplygem.com › webina...",
      "snippet": "10 feb 2023 — 35 Webinar Statistics · 1. Webinars Are Growing Exponentially. As much as 89% of businesses offering webinars have asserted that they can ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:HCzRCs2bqHkJ:https://supplygem.com/publications/webinar-statistics/&cd=25&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "date": "10 feb 2023",
      "date_utc": "2023-02-10T00:00:00.000Z",
      "block_position": 16,
      "page": "1",
      "position_overall": 12
    },
    {
      "position": 13,
      "title": "19+ Webinar Statistics & Benchmarks (2023 Stats + Data)",
      "link": "https://startupbonsai.com/webinar-statistics/",
      "domain": "startupbonsai.com",
      "displayed_link": "https://startupbonsai.com › webi...",
      "snippet": "2 gen 2023 — Webinar statistics – Editor's picks · 39% of B2B marketers use webinars. (Content Marketing Institute) · Thursday is the most popular day to hold ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:bnOSYeZDOLEJ:https://startupbonsai.com/webinar-statistics/&cd=26&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>stats</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "prefix": "2 gen 2023",
      "block_position": 17,
      "page": "1",
      "position_overall": 13
    },
    {
      "position": 14,
      "title": "25 Webinar Statistics [2023]: The Average Attendance Rate ...",
      "link": "https://www.zippia.com/advice/webinar-statistics/",
      "domain": "www.zippia.com",
      "displayed_link": "https://www.zippia.com › advice",
      "snippet": "16 ott 2022 — 25 Webinar Statistics [2023]: The Average Attendance Rate For A Webinar · 58% of B2B marketers use webinars for content marketing. · 54% of B2B ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:8eUmfJAecNwJ:https://www.zippia.com/advice/webinar-statistics/&cd=27&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "rich_snippet": {
        "top": {
          "detected_extensions": {
            "rating": 3.7,
            "reviews": 3
          }
        }
      },
      "date": "16 ott 2022",
      "date_utc": "2022-10-16T00:00:00.000Z",
      "block_position": 18,
      "page": "1",
      "position_overall": 14
    },
    {
      "position": 15,
      "title": "72 Webinar Statistics and Facts for 2023 | FounderJar",
      "link": "https://www.founderjar.com/webinar-statistics/",
      "domain": "www.founderjar.com",
      "displayed_link": "https://www.founderjar.com › w...",
      "snippet": "5 dic 2022 — General Webinar Statistics, Benchmarks, and Facts. 1. 58% of marketers use webinars in their content marketing campaigns. (OptinMonster)Whether ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:HgoVcb1SVp0J:https://www.founderjar.com/webinar-statistics/&cd=28&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>facts</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "date": "5 dic 2022",
      "date_utc": "2022-12-05T00:00:00.000Z",
      "block_position": 19,
      "page": "1",
      "position_overall": 15
    },
    {
      "position": 16,
      "title": "The Ultimate List of Webinar Statistics for 2023 - Adam Enfroy",
      "link": "https://www.adamenfroy.com/webinar-statistics",
      "domain": "www.adamenfroy.com",
      "displayed_link": "https://www.adamenfroy.com › ...",
      "snippet": "18 apr 2023 — As many as 61% of companies use webinars and other forms of content marketing for their business, allowing them to reach their business ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:lMjqA6PWELQJ:https://www.adamenfroy.com/webinar-statistics&cd=29&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>webinars</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "date": "18 apr 2023",
      "date_utc": "2023-04-18T00:00:00.000Z",
      "block_position": 20,
      "page": "1",
      "position_overall": 16
    },
    {
      "position": 17,
      "title": "18 Eye-Opening Statistics On Webinars: 2023 - Outgrow",
      "link": "https://outgrow.co/blog/statistics-on-webinars",
      "domain": "outgrow.co",
      "displayed_link": "https://outgrow.co › blog › statis...",
      "snippet": "25 set 2019 — 18 Eye-Opening Statistics On Webinars: 2023 · 73% of B2B marketers say a webinar is the best way to generate high-quality leads. · The average ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:GFM9zy8IM4EJ:https://outgrow.co/blog/statistics-on-webinars&cd=30&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>webinars</b>",
          "Altri siti web con i tuoi termini di ricerca <span>rimandano</span> a questo risultato",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "date": "25 set 2019",
      "date_utc": "2019-09-25T00:00:00.000Z",
      "block_position": 21,
      "page": "1",
      "position_overall": 17
    },
    {
      "position": 18,
      "title": "Webinar su argomenti di statistica e analisi dati live e gratuiti",
      "link": "https://www.statisticsfordataanalysis.com/webinar",
      "domain": "www.statisticsfordataanalysis.com",
      "displayed_link": "https://www.statisticsfordataanalysis.com › webinar",
      "snippet": "Organizziamo periodicamente webinar gratuiti con l'obiettivo di mostrare l'utilizzo pratico della soluzione Statistics for Data Analysis, ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:67TfVuddqEAJ:https://www.statisticsfordataanalysis.com/webinar&cd=31&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Il risultato è in <span>italiano</span>",
          "Questo risultato sembra pertinente per le ricerche effettuate dal seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 22,
      "page": "1",
      "position_overall": 18
    },
    {
      "position": 19,
      "title": "Webinar statistics provide you attendees insight! - ClickMeeting",
      "link": "https://clickmeeting.com/tools/webinar-statistics",
      "domain": "clickmeeting.com",
      "displayed_link": "https://clickmeeting.com › tools",
      "snippet": "Measure and analyze your webinars. Analyze data on individual attendees and improve both your ... Browse all features. Online events and webinar statistics ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:o_3vPDelyMgJ:https://clickmeeting.com/tools/webinar-statistics&cd=32&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 23,
      "page": "1",
      "position_overall": 19
    },
    {
      "position": 20,
      "title": "The State Of Webinars: Statistics You Need To Know",
      "link": "https://elitecontentmarketer.com/webinar-stats/",
      "domain": "elitecontentmarketer.com",
      "displayed_link": "https://elitecontentmarketer.com › ...",
      "snippet": "30 lug 2022 — 1. Webinars Scheduled In The Morning Have A Relatively Higher Attendance Rate · 2. 28% Of Webinars Are Held On Thursdays · 3. 68% Of Marketers Say ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:tveuPTVD34IJ:https://elitecontentmarketer.com/webinar-stats/&cd=33&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Alcuni <span>termini</span> correlati alla tua ricerca compaiono nel risultato: <b> webinars</b>, <b>stats</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "date": "30 lug 2022",
      "date_utc": "2022-07-30T00:00:00.000Z",
      "block_position": 24,
      "page": "1",
      "position_overall": 20
    },
    {
      "position": 21,
      "title": "Webinar statistics every marketer should track - Quickchannel",
      "link": "https://www.quickchannel.com/blog/webinar-statistics-every-marketer-should-track",
      "domain": "www.quickchannel.com",
      "displayed_link": "https://www.quickchannel.com › ...",
      "snippet": "Webinars are one of the most successful lead generating tools in marketing. Quickchannel is here to help you stay on top of your content marketing efforts.",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:U0IK_d9UfwoJ:https://www.quickchannel.com/blog/webinar-statistics-every-marketer-should-track&cd=34&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>webinars</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 25,
      "page": "1",
      "position_overall": 21
    },
    {
      "position": 22,
      "title": "K-12 Statistics Education Webinars",
      "link": "https://www.amstat.org/education/k-12-statistics-education-webinars",
      "domain": "www.amstat.org",
      "displayed_link": "https://www.amstat.org › k-12-st...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:0rSJKEMx9S8J:https://www.amstat.org/education/k-12-statistics-education-webinars&cd=35&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>webinars</b>",
          "Altri siti web con i tuoi termini di ricerca <span>rimandano</span> a questo risultato",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "rich_snippet": {
        "top": {
          "detected_extensions": {
            "price": 2020
          },
          "extensions": [
            "She is the 2020 recipient of the CRM",
            "SSC Prize in Statistics and an Elected Member of the International Statistical Institute. Dr Moodie serves as an Associate ..."
          ]
        }
      },
      "nested_results": [
        {
          "position": 1,
          "title": "Webinars - CommitteeonInternationalRelationsinStatistics",
          "link": "https://community.amstat.org/committeeoninternationalrelationsinstatistics/events2/webinars",
          "displayed_link": "https://community.amstat.org › ..."
        }
      ],
      "block_position": 26,
      "page": "1",
      "position_overall": 22
    },
    {
      "position": 23,
      "title": "80+ Practical Webinar Statistics - Optimize for Success in 2023",
      "link": "https://influno.com/webinar-statistics/",
      "domain": "influno.com",
      "displayed_link": "https://influno.com › webinar-st...",
      "snippet": "1 mag 2023 — Statistics About Scheduling the Webinar · 14% of marketers host webinars at least once per week. · Be mindful that most attendees can only commit ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:SvCuI484nUsJ:https://influno.com/webinar-statistics/&cd=37&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>webinars</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "date": "1 mag 2023",
      "date_utc": "2023-05-01T00:00:00.000Z",
      "block_position": 27,
      "page": "1",
      "position_overall": 23
    },
    {
      "position": 24,
      "title": "Webinars",
      "link": "https://www.statcan.gc.ca/en/wtc/webinars",
      "domain": "www.statcan.gc.ca",
      "displayed_link": "https://www.statcan.gc.ca › wtc",
      "snippet": "The Webinar series covers a broad range of topics from the Census program to navigating the Statistics Canada website. Our current and relevant webinars are ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:qdhwW4XIxKsJ:https://www.statcan.gc.ca/en/wtc/webinars&cd=38&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>webinars</b>",
          "Altri siti web con i tuoi termini di ricerca <span>rimandano</span> a questo risultato",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 28,
      "page": "1",
      "position_overall": 24
    },
    {
      "position": 25,
      "title": "Joint UNECE/IEA/Eurostat Webinar on Administrative ...",
      "link": "https://unece.org/statistics/events/MicrodataWebinar2023",
      "domain": "unece.org",
      "displayed_link": "https://unece.org › events › Micr...",
      "snippet": "This webinar was a joint event by the UNECE Steering Group on Climate Change-Related Statistics, the International Energy Agency and Eurostat, organized to:.",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:JD0TS4b0RpcJ:https://unece.org/statistics/events/MicrodataWebinar2023&cd=39&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 29,
      "page": "1",
      "position_overall": 25
    },
    {
      "position": 26,
      "title": "Webinars - STAT News",
      "link": "https://www.statnews.com/category/webinars/",
      "domain": "www.statnews.com",
      "displayed_link": "https://www.statnews.com › web...",
      "snippet": "Webinars. STAT's library of webinars on health, science, and biotech issues. Check back for updates.",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:hAG96FfsXxcJ:https://www.statnews.com/category/webinars/&cd=40&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questo <span>termine di ricerca</span> compare nel risultato: <b>webinar</b>",
          "Alcuni <span>termini</span> correlati alla tua ricerca compaiono nel risultato: <b> webinars</b>, <b>stat</b>, <b>stats</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 30,
      "page": "1",
      "position_overall": 26
    },
    {
      "position": 27,
      "title": "The Big Book of Webinar Stats - GoTo",
      "link": "https://www.goto.com/resources/big-book-of-webinar-stats",
      "domain": "www.goto.com",
      "displayed_link": "https://www.goto.com › resources",
      "snippet": "Your source for webinar benchmarks and best practices. ... The Big Book of Webinar Stats. G2W_lg_gated_webinar_stats-jpg. Take the guesswork out of webinars.",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:jDNkAOvCmjEJ:https://www.goto.com/resources/big-book-of-webinar-stats&cd=41&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questo <span>termine di ricerca</span> compare nel risultato: <b>webinar</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>stats</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 31,
      "page": "1",
      "position_overall": 27
    },
    {
      "position": 28,
      "title": "Upcoming Free Dissertation Webinars - Statistics Solutions",
      "link": "https://www.statisticssolutions.com/webinars/",
      "domain": "www.statisticssolutions.com",
      "displayed_link": "https://www.statisticssolutions.com › ...",
      "snippet": "Statistics Solutions offers free monthly webinars for graduate students in the process of completing their dissertation.",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:UcvCCcFcS2oJ:https://www.statisticssolutions.com/webinars/&cd=42&hl=it&ct=clnk&gl=it",
      "sitelinks": {
        "expanded": [
          {
            "title": "Setting Up and Running ...",
            "link": "https://www.statisticssolutions.com/webinars/"
          },
          {
            "title": "Mastering Your Introduction",
            "link": "https://www.statisticssolutions.com/webinars/"
          },
          {
            "title": "Confidently Present Your ...",
            "link": "https://www.statisticssolutions.com/webinars/"
          }
        ]
      },
      "sitelinks_search_box": False,
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>webinars</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 32,
      "page": "1",
      "position_overall": 28
    },
    {
      "position": 29,
      "title": "Webinar Statistics, Trends and Facts 2023 - Abdalslam",
      "link": "https://abdalslam.com/webinar-statistics",
      "domain": "abdalslam.com",
      "displayed_link": "https://abdalslam.com › webinar...",
      "snippet": "10 passaggi",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:c404fmLewqsJ:https://abdalslam.com/webinar-statistics&cd=43&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>facts</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 33,
      "page": "1",
      "position_overall": 29
    },
    {
      "position": 30,
      "title": "60+ Webinar Statistics to Know in 2023 [Shocking Stats]",
      "link": "https://blogginglift.com/webinar-statistics/",
      "domain": "blogginglift.com",
      "displayed_link": "https://blogginglift.com › webin...",
      "snippet": "Editor's Pick (Top Webinar Stats 2023). 95% of businesses consider webinars as an important aspect of their marketing strategy; 73% of B2B companies believe ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:MzrblL_EF-8J:https://blogginglift.com/webinar-statistics/&cd=44&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>stats</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 34,
      "page": "1",
      "position_overall": 30
    },
    {
      "position": 31,
      "title": "Where to find my webinar statistics? | Help - GetResponse",
      "link": "https://www.getresponse.com/help/where-do-i-find-my-webinar-statistics.html",
      "domain": "www.getresponse.com",
      "displayed_link": "https://www.getresponse.com › ...",
      "snippet": "On the Manage webinars page, find the webinar you want to review. When you get there, you can: View unique visitor, registrant, and attendee statistics for each ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:wdMxOITG7R8J:https://www.getresponse.com/help/where-do-i-find-my-webinar-statistics.html&cd=45&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>webinars</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 35,
      "page": "1",
      "position_overall": 31
    },
    {
      "position": 32,
      "title": "Statgraphics Webinars | Statistical Training & Consulting",
      "link": "https://www.statgraphics.com/webinars",
      "domain": "www.statgraphics.com",
      "displayed_link": "https://www.statgraphics.com › ...",
      "snippet": "Webinars. Statgraphics Technologies offers a series of statistics webinars that will help you learn how to use STATGRAPHICS Centurion most effectively, ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:XzQf6SXbkM8J:https://www.statgraphics.com/webinars&cd=46&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Alcuni <span>termini</span> correlati alla tua ricerca compaiono nel risultato: <b> webinars</b>, <b>statistical</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 36,
      "page": "1",
      "position_overall": 32
    },
    {
      "position": 33,
      "title": "Webinar - SPSS",
      "link": "https://www.spss.it/webinar",
      "domain": "www.spss.it",
      "displayed_link": "https://www.spss.it › webinar",
      "snippet": "Organizziamo periodicamente dei webinar gratuiti con l'obiettivo di mostrare l'utilizzo pratico della soluzione Statistics for Data Analysis, ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:OTuVA6kTz5MJ:https://www.spss.it/webinar&cd=47&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Il risultato è in <span>italiano</span>",
          "Questo risultato sembra pertinente per le ricerche effettuate dal seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 37,
      "page": "1",
      "position_overall": 33
    },
    {
      "position": 34,
      "title": "IASE — Webinars",
      "link": "https://iase-web.org/Webinars.php",
      "domain": "iase-web.org",
      "displayed_link": "https://iase-web.org › Webinars",
      "snippet": "Statistical Edutainment - an ISLP webinar in conjunction with IASE ... Gamifying Statistics Education through Elevated Learning Experience (ELX).",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:u1Ah4IwlnboJ:https://iase-web.org/Webinars.php&cd=48&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Alcuni <span>termini</span> correlati alla tua ricerca compaiono nel risultato: <b> webinars</b>, <b>statistical</b>",
          "Altri siti web con i tuoi termini di ricerca <span>rimandano</span> a questo risultato",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 38,
      "page": "1",
      "position_overall": 34
    },
    {
      "position": 35,
      "title": "35 Webinar Statistics in 2023 + Average Attendance Rate",
      "link": "https://codeless.co/webinar-statistics/",
      "domain": "codeless.co",
      "displayed_link": "https://codeless.co › webinar-stat...",
      "snippet": "25 feb 2023 — Key Webinar Statistics. The average registration number of a webinar is around 260. 73% of B2B marketers consider webinars as a highly effective ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:rRC05H8qE7cJ:https://codeless.co/webinar-statistics/&cd=49&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "date": "25 feb 2023",
      "date_utc": "2023-02-25T00:00:00.000Z",
      "block_position": 39,
      "page": "1",
      "position_overall": 35
    },
    {
      "position": 36,
      "title": "Statistics Webinar on ANOVA - YouTube",
      "link": "https://www.youtube.com/watch?v=dCqNTq05Clg",
      "domain": "www.youtube.com",
      "displayed_link": "https://www.youtube.com › watch",
      "prerender": False,
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "thumbnail": True,
      "thumbnail_image": "https://i.ytimg.com/vi/dCqNTq05Clg/mqdefault.jpg?sqp=-oaymwEFCJQBEFM&rs=AMzJL3lhBmI5VFMQcMBCvbeazsIa3S7SpQ",
      "block_position": 40,
      "page": "1",
      "position_overall": 36
    },
    {
      "position": 37,
      "title": "Exporting webinar attendee statistics - TwentyThree",
      "link": "https://www.twentythree.com/help/exporting-webinar-attendee-statistics",
      "domain": "www.twentythree.com",
      "displayed_link": "https://www.twentythree.com › e...",
      "snippet": "After your webinar, you might want to download your attendance statistics to upload to your CRM, marketing automation system or BI tool.",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:FGVSP799ka8J:https://www.twentythree.com/help/exporting-webinar-attendee-statistics&cd=51&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 41,
      "page": "1",
      "position_overall": 37
    },
    {
      "position": 38,
      "title": "Webinar Statistics | Help Center - WebinarNinja",
      "link": "https://help.webinarninja.com/en/articles/4756477-webinar-statistics",
      "domain": "help.webinarninja.com",
      "displayed_link": "https://help.webinarninja.com › ...",
      "snippet": "Webinar Statistics. Webinar Statistics. See all the analytics for your webinars such as registration and attendance rates, chat and question logs, and more.",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:uobZopEK1N0J:https://help.webinarninja.com/en/articles/4756477-webinar-statistics&cd=52&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 42,
      "page": "1",
      "position_overall": 38
    },
    {
      "position": 39,
      "title": "Global Webinar on Strengthening Climate Change ... - ESCAP",
      "link": "https://www.unescap.org/events/2023/global-webinar-strengthening-climate-change-and-disaster-related-statistics-needs-0",
      "domain": "www.unescap.org",
      "displayed_link": "https://www.unescap.org › events",
      "snippet": "Global Webinar on Strengthening Climate Change and Disaster-Related Statistics: Needs, Priorities, and Action for Africa, Latin America and the Caribbean ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:2E-j8FlLywcJ:https://www.unescap.org/events/2023/global-webinar-strengthening-climate-change-and-disaster-related-statistics-needs-0&cd=53&hl=it&ct=clnk&gl=it",
      "related_page_link": "https://www.unescap.org/events/2023/global-webinar-strengthening-climate-change-and-disaster-related-statistics-needs-0",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 43,
      "page": "1",
      "position_overall": 39
    },
    {
      "position": 40,
      "title": "27 B2B webinar statistics that prove you should do one",
      "link": "https://www.isolinecomms.com/strategy/b2b-webinar-statistics/",
      "domain": "www.isolinecomms.com",
      "displayed_link": "https://www.isolinecomms.com › ...",
      "snippet": "14 apr 2023 — Stats on the benefits of B2B webinars · 20 to 40% of webinar audiences become qualified leads (Source: Monster) · 37% of B2B marketers list ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:pcwczsSIKyEJ:https://www.isolinecomms.com/strategy/b2b-webinar-statistics/&cd=54&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Alcuni <span>termini</span> correlati alla tua ricerca compaiono nel risultato: <b> webinars</b>, <b>stats</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "date": "14 apr 2023",
      "date_utc": "2023-04-14T00:00:00.000Z",
      "block_position": 44,
      "page": "1",
      "position_overall": 40
    },
    {
      "position": 41,
      "title": "Public Understanding and Use of Statistics in Relation to the ...",
      "link": "https://council.science/events/pandemic-statistics/",
      "domain": "council.science",
      "displayed_link": "https://council.science › events",
      "snippet": "The webinar will address the following two questions: How effective were statistics in informing citizens and policy makers in thinking about the pandemic and ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:KHJIqghenvMJ:https://council.science/events/pandemic-statistics/&cd=55&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 45,
      "page": "1",
      "position_overall": 41
    },
    {
      "position": 42,
      "title": "35 Webinar Statistics 2023: The Ultimate List for Creators",
      "link": "https://bloggerspassion.com/webinar-statistics/",
      "domain": "bloggerspassion.com",
      "displayed_link": "https://bloggerspassion.com › w...",
      "snippet": "27 feb 2023 — Webinar Growth Statistics · 1. The webinar market is projected to reach $4.44 billion by 2025, according to Frost & Sullivan. · 2. 57% of ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:RxD2jqkoClIJ:https://bloggerspassion.com/webinar-statistics/&cd=56&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "date": "27 feb 2023",
      "date_utc": "2023-02-27T00:00:00.000Z",
      "block_position": 46,
      "page": "1",
      "position_overall": 42
    },
    {
      "position": 43,
      "title": "Webinar Series on Statistical Experience Sharing - OIC-StatCom",
      "link": "https://www.oicstatcom.org/webinar-series.php",
      "domain": "www.oicstatcom.org",
      "displayed_link": "https://www.oicstatcom.org › we...",
      "snippet": "Accordingly, SESRIC has recently initiated the Statistical Experience Sharing Webinar Series through which National Statistics Offices of OIC countries and ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:5Ib8mcaQweEJ:https://www.oicstatcom.org/webinar-series.php&cd=57&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>statistical</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 47,
      "page": "1",
      "position_overall": 43
    },
    {
      "position": 44,
      "title": "Medical Statistics Made Simple Webinar MRCGP AKT MRCP",
      "link": "https://courses.emedica.co.uk/acatalog/Medical-Statistics-Made-Simple-Webinar-MRCGP-AKT.html",
      "domain": "courses.emedica.co.uk",
      "displayed_link": "https://courses.emedica.co.uk › ...",
      "snippet": "If you want to revise now, you can purchase access to the video recording of our MRCGP AKT Masterclass Webinars for Statistics / Admin / High Yield Clinical ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:YwRAtsnfxcQJ:https://courses.emedica.co.uk/acatalog/Medical-Statistics-Made-Simple-Webinar-MRCGP-AKT.html&cd=58&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>webinars</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 48,
      "page": "1",
      "position_overall": 44
    },
    {
      "position": 45,
      "title": "Webinars – IAOS - International Association for Official Statistics",
      "link": "https://iaos-isi.org/webinars/",
      "domain": "iaos-isi.org",
      "displayed_link": "https://iaos-isi.org › webinars",
      "snippet": "“The Independence of Statistical Institutions with a Focus on Arab Region and North Africa” Webinar - 2 November 2022 · \"Big Data and Official Statistics in ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:xALFIdztZW8J:https://iaos-isi.org/webinars/&cd=59&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Alcuni <span>termini</span> correlati alla tua ricerca compaiono nel risultato: <b> webinars</b>, <b>statistical</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 49,
      "page": "1",
      "position_overall": 45
    },
    {
      "position": 46,
      "title": "Webinar on Using Mobile Phone Data for Official Statistics on ...",
      "link": "https://rtc-cea.cepal.org/en/use-of-mobile-phone-data-for-Information-society-statistics",
      "domain": "rtc-cea.cepal.org",
      "displayed_link": "https://rtc-cea.cepal.org › use-of...",
      "snippet": "This webinar is organized by the United Nations Regional Hub for Big Data in Brazil, with the collaboration of the INE of Chile and the Statistics Division ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:RKLZ7VJb2LoJ:https://rtc-cea.cepal.org/en/use-of-mobile-phone-data-for-Information-society-statistics&cd=60&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 50,
      "page": "1",
      "position_overall": 46
    },
    {
      "position": 47,
      "title": "Webinar | International Association of Survey Statisticians (IASS)",
      "link": "http://isi-iass.org/home/webinars/",
      "domain": "isi-iass.org",
      "displayed_link": "http://isi-iass.org › webinars",
      "snippet": "IASS Webinar 26: Integrating Survey and Non-survey Data in the Production of U.S. Official Agricultural Statistics: A Progress Report.",
      "prerender": False,
      "cached_page_link": "http://webcache.googleusercontent.com/search?q=cache:OKtiFYuS0awJ:isi-iass.org/home/webinars/&cd=61&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Un <span>termine</span> correlato alla tua ricerca compare nel risultato: <b>webinars</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 51,
      "page": "1",
      "position_overall": 47
    },
    {
      "position": 48,
      "title": "ACMQ Bi-Monthly Webinar",
      "link": "https://www.acmq.org/index.php?option=com_jevents&task=icalrepeat.detail&evid=15&Itemid=115&year=2024&month=04&day=13&title=&uid=17c82310bc4a08c1686368c0e22c9d54",
      "domain": "www.acmq.org",
      "displayed_link": "https://www.acmq.org › ...",
      "snippet": "ACMQ Bi-Monthly Webinar. Statistics for Users of Quality Data, including using Big Data. April 13th, 2024 | 12:00pm CT. Join ACMQ for the next webinar in ...",
      "prerender": False,
      "cached_page_link": "https://webcache.googleusercontent.com/search?q=cache:HWc2JfL0xDYJ:https://www.acmq.org/index.php%3Foption%3Dcom_jevents%26task%3Dicalrepeat.detail%26evid%3D15%26Itemid%3D115%26year%3D2024%26month%3D04%26day%3D13%26title%3D%26uid%3D17c82310bc4a08c1686368c0e22c9d54&cd=62&hl=it&ct=clnk&gl=it",
      "about_this_result": {
        "your_search_and_this_result": [
          "Questi <span>termini di ricerca</span> compaiono nel risultato: <b> webinar</b>, <b>statistics</b>",
          "Questo risultato sembra pertinente, anche se non è in <span>italiano</span>",
          "Questo risultato sembra pertinente per questa ricerca, anche se in genere viene mostrato per le ricerche effettuate al di fuori del seguente paese: <span>Italia</span>"
        ]
      },
      "block_position": 52,
      "page": "1",
      "position_overall": 48
    }
  ]
}

# id: sentence
sentence_ids = {}
# flip
sentences = {}

row_numbers = {}

# keyword: set(relevant_data.id)
relevant_data_by_row = {}

SIZE_LIMIT =  500



async def get_api_result(api_key, serps_to_check, query):
    
    params = {
        'api_key': api_key,
        'page': 1,
        'max_page': 1,
        'num': min(99, serps_to_check * 11),
        'q': query
    }

    api_result = requests.get('https://api.valueserp.com/search', params)
    return api_result.json()

def filter_blacklisted(organic_results, blacklisted_urls):
    blacklisted_urls = set(blacklisted_urls)
    return [res for res in organic_results if res["domain"] not in blacklisted_urls]

async def get_resp_text_task(link):
    resp = requests.get(link)
    return resp.text

async def get_update_by_keywords_task(keyword, all_text_tags):
    print("Searching for keywords from link given search query", keyword)
    # for a link for a given keyword
    m = 3

    for text_tag in all_text_tags:
        # generate_id
        sentence = re.sub("[^a-zA-Z|0-9|%|.| ]", " ", text_tag.lower())
        sentence = filter_spacing(sentence)
        print("\n", sentence)
        print(relevant_data_by_row)

        # Skip giant text corpuses
        if len(sentence) >= 500:
            continue
        sentenceLst = sentence.split(" ")
        for gap_size in range(m, 0, -1):
            for i in range(len(sentenceLst)-gap_size+1):
                token = " ".join(sentenceLst[i:i+gap_size])
                if token in row_numbers:
                    # only store sentences with a matching token
                    if sentence not in sentence_ids:
                        id = len(sentence_ids)
                        sentence_ids[sentence] = id
                        sentences[id] = sentence
                    
                    sentence_id = sentence_ids[sentence]
                    # csv row for the keyword
                    row_number = row_numbers[token]
                    # Add the sentence id to the row's keyword
                    
                    # Store at most 1000 sentences per keyword
                    if len(relevant_data_by_row[row_number][token]) <= 500:
                        relevant_data_by_row[row_number][token].add(sentence_id)
                        break
                    else:
                        return
    return

async def get_data_task(keyword, link, credentials):
    try:
        get_resp_text = asyncio.create_task(get_resp_text_task(link))
        src = await get_resp_text
        soup = BeautifulSoup(src, 'html.parser')
    except:
        print("Crash On Request:", link)
        return

    text_tags = ["p", "b", "h3", "h4", "h5", "li", "text"]
    all_text_tags = []
    for text_tag in text_tags:
        tags = soup.find_all(text_tag)
        tags = list(map(str, tags))
        tags = [re.sub("<(.)+?>", " ", tag) for tag in tags]
        tags = [filter_spacing(tag) for tag in tags]
        tags = [tag for tag in tags if len(tag) > 15]
        all_text_tags += tags
    update_sentences_by_keywords = asyncio.create_task(get_update_by_keywords_task(keyword, all_text_tags))
    await update_sentences_by_keywords
    return
    

async def get_keyword_sentences_task(keyword, organic_results, credentials):
    # For each keyword
    key = to_key(keyword)
    for result in organic_results:
        row_number = row_numbers[key]
        if len(relevant_data_by_row[row_number][key]) >= SIZE_LIMIT:
            return

        link = result["link"]
        print(f"Accessing {link=}")
        get_data = asyncio.create_task(get_data_task(keyword, link, credentials))
        await get_data

        ###################################### view
        for row in relevant_data_by_row:
            for keyword in relevant_data_by_row[row]:
                sentence_count = len(relevant_data_by_row[row][keyword])
                if sentence_count > 0:
                    print(f" {keyword}: {sentence_count} sentences")

        dd = listify(relevant_data_by_row)
        if dd:
            with open("data_container/relevant_data_by_row.json", "w") as f1:
                json.dump(dd, f1)
            with open("data_container/sentences.json", "w") as f2:
                json.dump(sentences, f2)        
            with open("data_container/row_numbers.json", "w") as f3:
                json.dump(row_numbers, f3)
    return 


async def get_relevant_data_by_row_task(keywords, num_pages, blacklisted_urls, credentials):
    # For each csv row, containing a list of comma separated keywords
    for keyword in keywords.split(","):
        # Add 'statistics' back to the search query
        query = keyword
        if "statistics" not in keyword:
            query += " statistics"
        
        get_serp_response = asyncio.create_task(get_api_result(credentials["VALUE_SERP_API_KEY"], num_pages, query))
        serp_response = await get_serp_response
        if serp_response['request_info']['success'] == False:
            print("SERP Response unsuccessful")
            serp_response = testing_serp_response
        
        organic_results = serp_response["organic_results"]
        organic_results = filter_blacklisted(organic_results, blacklisted_urls)
        get_keyword_sentences = asyncio.create_task(get_keyword_sentences_task(keyword, organic_results, credentials))
        await get_keyword_sentences

        # Safety precaution for saving
        try:
            # convert set of sentence ids to list
            do = False
            dd = listify(relevant_data_by_row)
            for k in dd:
                for kk in dd[k]:
                    if len(dd[k][kk]) > 0:
                        do = True
                        break
            if do:
                with open("data_container/relevant_data_by_row.json", "w") as f1:
                    json.dump(dd, f1)
            if len(sentences) > 50:
                with open("data_container/sentences.json", "w") as f2:
                    json.dump(sentences, f2)
            if row_numbers:
                with open("data_container/row_numbers.json", "w") as f3:
                    json.dump(row_numbers, f3)
        except:
            print("Error on saving data")
            pass
            
    return


# main function for handle
async def get_handle_statistics(queries, blacklisted_urls, credentials):
    # initialize the maps
    for rowNo in queries:
        keywords = queries[rowNo]["Keywords"]
        rowNo = str(rowNo)
        for keyword in keywords.split(","):
            if keyword != "statistics":
                filtered_keyword = to_key(keyword)
            
            if filtered_keyword:
                # track the row number of the keyword in the original csv sheet
                row_numbers[filtered_keyword] = rowNo
                # keyword: set(sentence_id)
            if rowNo not in relevant_data_by_row:
                relevant_data_by_row[rowNo] = {}
            relevant_data_by_row[rowNo][filtered_keyword] = set({})

    for rowNo in queries:
        keywords = queries[rowNo]["Keywords"]
        num_pages = queries[rowNo]["SERPNumber"]
        # for each row
        get_relevant_data_by_row = asyncio.create_task(get_relevant_data_by_row_task(keywords, num_pages, blacklisted_urls, credentials))
        await get_relevant_data_by_row
    
    # Prompting
    get_GPT_statistics = asyncio.create_task(get_GPT_statistics_task(credentials))
    await get_GPT_statistics
    return


