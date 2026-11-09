---
title: "DeepMind says its AI agents found two cracks in retired encryption"
excerpt: "Google DeepMind says AI agents, supervised by humans and working with academic cryptographers, found two previously unknown weaknesses in 1024-bit RSA — but the headline numbers are theoretical, not measured end to end."
category: "Technology & AI"
categorySlug: "technology-ai"
date: "November 8, 2026"
author: "Zentra Daily Newsroom"
heroLabel: "London / Mountain View"
heroTone: "linear-gradient(135deg,#222,#777)"
sourceName: "BYOBot — AI Daily Newsstand, November 8, 2026"
sourceUrl: "https://byobot.ai/ai-news/ai-daily-newsstand-november-8-2026"
sourceName2: "The Art of CTO — Daily Sync, November 8, 2026"
sourceUrl2: "https://theartofcto.com/daily-sync/2026-11-08-daily-sync"
---

Google DeepMind says its AI agents have found two previously unknown weaknesses in 1024-bit RSA, the encryption standard that once protected much of the internet and is now considered retired. The work was announced on November 6 by Pushmeet Kohli, DeepMind's vice-president of science, and it is the kind of result that sounds dramatic in a headline and demands careful reading in the detail.

The agents worked under human supervision and alongside academic cryptographers. They found two distinct weaknesses. The first concerns padding — the extra structure wrapped around a message before signing, designed to make forgery harder. According to DeepMind, once an attacker controls about half of the signed block, padding buys almost nothing. Where the attacker controls only a short fingerprint, the agents produced an algorithm DeepMind estimates is around 1,600 times faster than the best published method.

The second weakness is batch factoring. When many keys share a bit length, one expensive precomputation can be spread across all of them, cutting the average cost per additional key by roughly 30 times, according to DeepMind's estimates. Taken together, the two findings suggest that 1024-bit RSA — already retired from serious use — is weaker than cryptographers had believed.

## The asterisks matter

Every headline move in this story, as the daily AI briefing that first pulled it together put it, came with an asterisk about who checked it. The capability is real, and the evidence is partial. That is the honest summary.

Both of the big multipliers — 1,600 times faster, 30 times cheaper — are theoretical rather than measured end to end. The part of the work that actually ran was a sandboxed reproduction against a 1024-bit key that an academic team had already broken, published on the IACR ePrint archive in September. In that reproduction, DeepMind reports its agents used 3.5 times less CPU time than factoring the key outright. That is a real, measured result, but it is a much smaller number than the headline figures, and the gap between the two is the gap between a laboratory reproduction and a claim about the general case.

This is not a reason to dismiss the work. Finding previously unknown weaknesses in a well-studied cryptosystem is a genuine achievement, and the fact that AI agents did it — working with humans, not instead of them — is a meaningful signal about where AI-assisted research is heading. It is, however, a reason to describe the result precisely: two weaknesses found, one measured reproduction, and theoretical estimates for the rest.

## Why 1024-bit RSA, and why now

RSA with 1024-bit keys has been retired for years. Modern systems use 2048-bit keys or more, or have moved to other algorithms entirely. Nobody's bank account or email was put at risk by this announcement, and DeepMind is not claiming otherwise. The significance is different: it is about what AI agents can now do in a field — cryptanalysis — that has traditionally required rare, specialised human expertise.

Cryptanalysis is a good test case for AI research assistance because it is both deeply mathematical and deeply empirical. An agent that can search a large space of possible attacks, test them, and refine the promising ones is doing something that looks a lot like research. The DeepMind result suggests that agents are getting good enough at that loop to produce results that human cryptographers had not found. That is the story, more than the specific weaknesses in a retired key size.

It is also a story about verification. The cryptography community will now do what it always does with a new claim: try to reproduce it, probe its limits, and decide how much of it holds up. The IACR ePrint archive, where the underlying reproduction was published, is the right venue for that scrutiny. If the findings survive it, they will be folded into the field's understanding of RSA. If parts of them do not, the field will say so. Either outcome is how science is supposed to work.

## The wider AI week

The DeepMind result was the front page of a busy week in AI. Google's Gemini Omni 1.2 Flash video model became generally available, with clips running up to 15 seconds instead of 10 and pricing reported to be 30 percent below the previous version. NVIDIA put open-weight checkpoints for its Cosmos 3 world models on Hugging Face on November 5, for driving and robotics simulation. Thinking Machines Lab released Inkling 2 Small, a 594-billion-parameter mixture-of-experts model with roughly 17 billion parameters active per request.

There was also a sobering counterpoint. METR, an independent evaluation nonprofit, published an assessment on November 5 of how much AI is speeding up AI research inside Anthropic, based on on-site work from August 12 to October 29. Anthropic, the report found, is improving model capabilities on well-specified tasks at about twice the rate it managed from March 2024 to October 2025. But Anthropic held unilateral redaction rights and cut a majority of the evidence METR found most informative. The capability is real in every case, the briefing concluded, and the evidence is partial in every case. That sentence applies to the DeepMind result too — and it is worth keeping in mind as AI research accelerates.
