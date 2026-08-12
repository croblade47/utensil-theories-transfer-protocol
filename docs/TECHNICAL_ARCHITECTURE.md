# Technical Architecture & Transfer Protocol Specification
**Protocol**: Utensil Theories Transfer Protocol (UTTP)  
**System Architecture**: Hybrid Physical Zine Bootstrap + React Web Studio

---

## 1. Zero-Friction Physical AI Bootstrap Architecture

The Utensil Theories Transfer Protocol solves the AI adoption barrier for non-technical users by embedding machine-readable system directives into physical paper pages:

```
[ Physical 8-Page Zine ]
        │
        ├─► Page 1: High-Contrast Color Category Cover + $2 Starburst + Vector QR
        │
        ├─► Page 2: Universal AI Launch Page (Fiducials [▲], CODE: H1..H8, AI Directives)
        │       │
        │       └─► User Points Smartphone Camera (ChatGPT / Gemini / Copilot)
        │               │
        │               └─► AI Model Reads Printed System Directives
        │                       │
        │                       ├─► Sets Role: Senior Assistant (Speak Aloud)
        │                       ├─► Sets Language Level: 6th Grade Plain Text
        │                       └─► Initiates Spoken Audio Greeting
        │
        └─► Pages 3–8: Task-Specific Prompt Templates (Doctor Notes, Bills, Wi-Fi, Scams)
```

---

## 2. Print Imposition Engine Architecture

The web application and standalone HTML zines implement standard 1-sheet 8-page zine imposition mechanics:

- **Paper Format**: 11" x 8.5" US Letter Landscape
- **Imposition Grid**: 4 columns x 2 rows
- **Rotation Rule**: Top row (Pages 8, 1, 4, 5) rendered upside down (180° rotation) relative to bottom row (Pages 7, 2, 3, 6) so that folding paper in half twice creates a correctly oriented book.
- **Center Slit**: Horizontal dotted cut line with 16pt vertical padding.

---

## 3. Technology Stack

- **Frontend Framework**: React 18 + TypeScript + Vite 6.4.3
- **Styling System**: Custom Vanilla CSS Tokens + HSL Category Color System
- **Icons**: Lucide React
- **Speech Subsystem**: Web Speech API (`SpeechSynthesis` & `webkitSpeechRecognition`)
- **PDF Compilation**: Edge Headless `--print-to-pdf` rendering engine
