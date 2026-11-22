---
title: "Microsoft says a months-old bug and its own safeguards caused the global Outlook outage"
excerpt: "Microsoft's final report on last week's global Microsoft 365 outage says a software bug that had sat dormant since July, testing that failed to catch it, and safety systems that spread the failure combined to take Outlook offline around the world."
category: "Technology & AI"
categorySlug: "technology-ai"
date: "November 22, 2026"
author: "Zentra Daily Newsroom"
heroLabel: "A bug since July, missed in testing — then the safeguards spread it"
heroTone: "linear-gradient(135deg,#0d1117,#3a4550)"
heroImage: "/images/articles/microsoft-says-months-old-bug-and-own-safeguards-caused-global-outlook-outage.webp"
sourceName: "GeekWire"
sourceUrl: "https://www.geekwire.com/2026/microsofts-final-outlook-outage-report-details-testing-gaps-and-safeguards-that-backfired/"
sourceName2: "Chosun Biz"
sourceUrl2: "https://biz.chosun.com/en/en-it/2026/11/17/MJP3AIQQ7NAKNIKW5ZKE6FG7YU/"
---

Microsoft has released its final report on last week's global Microsoft 365 outage, blaming a software bug that had sat dormant since July, testing that failed to catch it, and safety systems that spread the failure around the world.

The bug came from a Windows update Microsoft began rolling out in July to its network gateway, the servers in front of Outlook and Microsoft 365. It changed how those servers handle incoming connections: under heavy load, the connection process bogged down, with tasks stuck waiting on each other until the servers ran out of memory and stopped responding.

The flaw hit hardest on the company's newer, more powerful servers, and for more than three months it caused no problems at all. One reason it went unnoticed is that Microsoft's testing did not match the real world: its labs mostly used older servers running a different mix of traffic. "Our testing did not adequately represent the combination of hardware and traffic mix encountered during this incident," the company acknowledged in the report, released Friday, a week after the outage was resolved.

The report lays out three conditions that finally set the bug off. Nearly 14% of the gateway's server capacity was already offline that day for routine software updates. About 15 hours earlier, a routing glitch on Teams' own gateway moved all Teams traffic worldwide onto the email servers. Then the US workday began, with failures starting around 8 a.m. Pacific. Without the bug, the report says, all three together would have been routine.

What turned a local failure global was Microsoft's own protection. As servers stopped responding, its systems automatically moved their traffic to healthy servers nearby, which had the same bug and buckled. At the low point, more than 80% of the gateway's servers in North America were unresponsive, and within about two hours servers in every region were affected. Getting the service back was its own problem: as servers came back online, they were swamped by pent-up demand and froze again, a pattern engineers call a "thundering herd."

The report also settles two questions that hung over the outage: it was not hackers, and it was not AI. "This incident was confirmed not to be caused by a cyberattack, and we found no evidence of malicious activity," it says. "This change was not caused by AI tooling." Its first customer notice went out about 20 minutes after the outage took hold, and no business email was lost.

The report lists 13 next steps, including production-like testing, due by the end of March; changing how traffic shifts between regions so a problem in one part of the world stays there; and splitting up the servers that handle email so a surge elsewhere cannot take email down. Some fixes are due by the end of the year or March; several have no date yet. Chief executive Satya Nadella told the Ignite conference this week that Microsoft has work to do on resilience.

*Illustration — not a photograph.*

## Sources

- [GeekWire — "Microsoft's final Outlook outage report details testing gaps and safeguards that backfired"](https://www.geekwire.com/2026/microsofts-final-outlook-outage-report-details-testing-gaps-and-safeguards-that-backfired/)
- [Chosun Biz — "Microsoft says four-month-old bug and testing gap crippled Outlook, Teams" (Yonhap)](https://biz.chosun.com/en/en-it/2026/11/17/MJP3AIQQ7NAKNIKW5ZKE6FG7YU/)
