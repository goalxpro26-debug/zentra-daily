---
title: "Signal blocks screenshots to keep AI agents out of your private chats"
excerpt: "The encrypted messaging app is switching off screenshots on iPhones and Android phones by default, saying the AI assistants built into the operating systems can read decrypted messages straight off the screen."
category: "Technology & AI"
categorySlug: "technology-ai"
date: "November 21, 2026"
author: "Zentra Daily Newsroom"
heroLabel: "A sealed phone screen — the message stays where it was sent"
heroTone: "linear-gradient(135deg,#10151a,#3a4550)"
heroImage: "/images/articles/signal-blocks-screenshots-ai-agents-ios-android.webp"
sourceName: "Signal"
sourceUrl: "https://signal.org/blog/protecting-your-privacy/"
sourceName2: "The Register"
sourceUrl2: "https://www.theregister.com/security/2026/11/20/signal-slams-door-on-prying-ai-agents-to-protect-privacy/5311466"
---

*Illustration — not a photograph.*

Signal, the encrypted messaging app, is switching off screenshots inside its own app — not to stop people saving messages, but to stop the artificial intelligence built into their phones from reading them.

The change, announced on Friday by Signal president Meredith Whittaker, blocks screenshots by default on iPhones running iOS 27 and switches on screen protection on Android phones when an AI assistant tries to capture what is on the display. The target is the new generation of operating-system assistants — Apple's Siri AI, with its Onscreen Awareness feature, and Google's Gemini Intelligence — which scan whatever is on screen so they can answer questions and carry out tasks.

That scanning is the problem, Signal says. A message may be encrypted as it travels, but once it arrives it is decrypted and shown in plain text on the screen. When an AI agent reads the screen, it captures that text and can store it locally or send it to a remote server — entirely outside Signal's control, and unseen by the other people in the conversation.

Users can switch the protection off under Privacy, then App Security, in the app's settings. Signal warns against doing so: turning it off can expose not only your own messages but also those sent by your contacts, and it breaks the app's privacy guarantee.

The move follows a similar step last year, when Signal blocked Microsoft's Recall feature from taking periodic screenshots of its app on Windows 11. But the company is candid that blocking screenshots is only a partial answer. It does not stop AI agents reaching app data through other routes, such as files stored on the device or notifications, and it offers no protection at all if the person at the other end of a conversation has switched the protection off. On macOS, Signal says it cannot implement the protection at all.

Signal also points to third-party agents beyond the built-in ones. It cites reporting by Reuters that Meta's Muse agent was able to read Signal messages by using the deep permissions users are encouraged to grant during setup — accessibility tools on a Mac and push notifications on Android — which Signal describes as a skeleton key meant to help people use their devices, not to hand their chats to an AI.

Rather than fighting each new agent one by one, Signal is asking Apple, Google and Microsoft for something more basic: a simple, well-documented way for developers to opt their apps out of AI data access — screen reading, file access and notifications — without breaking the app, plus clear documentation of how the agents actually work. Whittaker says the company is in conversation with Apple and Google and is cautiously optimistic.

She frames the stakes bluntly: the way AI agents are being woven into operating systems is an existential threat to Signal's mission, and to any developer trying to guarantee privacy in the app. Signal is the canary in the coal mine, the post says — but the problem, it argues, affects the whole ecosystem.

## Sources

- [Signal — "Signal is Serious About Protecting Your Privacy"](https://signal.org/blog/protecting-your-privacy/)
- [The Register — "Signal slams door on prying AI agents to protect privacy"](https://www.theregister.com/security/2026/11/20/signal-slams-door-on-prying-ai-agents-to-protect-privacy/5311466)
