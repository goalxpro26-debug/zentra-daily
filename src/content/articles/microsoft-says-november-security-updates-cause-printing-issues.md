---
title: "Microsoft says November security updates may break printing"
excerpt: "Microsoft warned that its November 2026 security updates can stop documents with complex formatting from printing, mainly in Word — the latest in a run of problems with this month's Patch Tuesday release."
category: "Technology & AI"
categorySlug: "technology-ai"
date: "November 13, 2026"
author: "Zentra Daily Newsroom"
heroLabel: "Redmond, Washington"
heroTone: "linear-gradient(135deg,#14181d,#3d4a58)"
heroImage: "/images/articles/microsoft-says-november-security-updates-cause-printing-issues.webp"
sourceName: "BleepingComputer"
sourceUrl: "https://www.bleepingcomputer.com/news/microsoft/microsoft-says-november-security-updates-cause-printing-issues/"
sourceName2: "How-To Geek"
sourceUrl2: "https://www.howtogeek.com/word-printing-problems-microsofts-november-windows-updates-are-the-likely-cause/"
---

Microsoft has warned customers that its November 2026 security updates may break printing for documents with complex formatting, in the latest problem to surface from this month's Patch Tuesday release.

In a service alert seen by BleepingComputer, the company said printing "might fail for documents containing images rendered with a height or width value of zero at the selected printing resolution" after the November updates — or later updates — are installed. The issue affects devices running Windows 10 or later and Windows Server 2016 or later.

The bug mainly hits people printing Microsoft Word documents through the Windows Graphics Device Interface, the system that handles how documents are drawn on screen and on paper. Microsoft said printing from other applications could also be affected.

The trigger is easy to miss. The zero-sized images at the heart of the problem can sit inside a document even when no graphic is visible — they are used in some complex formatting, such as invisible images added as watermarks, layout anchors, or by document-generation tools. A file can look perfectly normal on screen and still fail to print.

## A troubled update

The printing fault is not the only problem with the November release. Microsoft has also confirmed that the updates fail to install on some Windows 11 machines that took October's non-security preview update, leaving affected devices repeatedly retrying the install or showing error codes 0x80070306, 0x800f0989 or 0x800f0993. The company said it would repair affected devices automatically within 24 to 48 hours, with no action needed from users.

The same batch of updates has also triggered Windows activation and licensing failures, with error code 0x80041008, and Microsoft has acknowledged performance and stability problems in SQL Server on systems updated since October's Patch Tuesday.

It is a familiar pattern. Windows updates in March and July 2025 caused printing problems of their own — the first made some USB printers print random text, the second broke the "Print to PDF" feature — and August 2026 .NET Framework updates broke printing and PDF export in apps built on the Windows Presentation Foundation framework.

## What is still unknown

Microsoft said it is investigating the printing issue and will share more information when it has it. It has not announced a permanent fix, a workaround, or a date for one, so users who hit the problem have little to do for now but watch for an updated advisory — and check whether a document that will not print contains the kind of hidden formatting that triggers the bug.

*Illustration — not a photograph.*

## Sources

- [BleepingComputer — "Microsoft says November security updates cause printing issues"](https://www.bleepingcomputer.com/news/microsoft/microsoft-says-november-security-updates-cause-printing-issues/)
- [How-To Geek — "Word printing problems? Microsoft's November Windows updates are the likely cause"](https://www.howtogeek.com/word-printing-problems-microsofts-november-windows-updates-are-the-likely-cause/)
