# OpenRouter Setup & Scoring Guide

## Quick Start

### 1. Get Your OpenRouter API Key
- Visit: https://openrouter.ai/keys
- Create a new API key (free tier, no payment required)
- Copy the key

### 2. Add the Key to `.env`
```bash
# Edit .env and replace sk_or_YOUR_KEY_HERE with your actual key
OPENROUTER_API_KEY=sk_or_xxxxxxxxxx
```

### 3. Run the Scoring Pipeline
```bash
# Score all 44 occupations (will take ~1-2 minutes)
python3 score.py

# Or test on first 10 only:
python3 score.py --start 0 --end 10

# Re-score everything (ignores cache):
python3 score.py --force
```

### 4. Rebuild Site Data
```bash
python3 build_site_data.py
```

### 5. View Results
- Refresh http://localhost:8001
- Toggle to "AI Exposure" layer to see the scores
- Each occupation now has real AI automation exposure ratings

## What Happens

1. **score.py** reads `occupations_ph.csv`
2. Sends each occupation to Claude Haiku via OpenRouter
3. Claude rates AI exposure (0-10 scale) with PH-specific context
4. Saves results incrementally to `scores.json`
5. **build_site_data.py** merges scores into `site/data.json`
6. Frontend treemap colors reflect real AI exposure analysis

## OpenRouter vs Anthropic

| Aspect | OpenRouter | Anthropic |
|--------|-----------|-----------|
| API Format | OpenAI-compatible | Proprietary |
| Free Tier | ✅ Yes | ❌ No (requires credit card) |
| Setup | 2 minutes | More complex |
| Models | Claude, GPT, Llama, etc. | Claude only |
| First 44 occupations | Free | Not free |

## Estimated Scoring Time

- 44 occupations × 0.5s delay = ~25 seconds base
- Claude response time: ~1-2s per occupation
- **Total: ~1-2 minutes**

## Troubleshooting

**"OPENROUTER_API_KEY is not set"**
- Make sure `.env` exists and has the key
- Kill and restart your Python script if you added the key after starting

**"401 Unauthorized"**
- Your API key is invalid or expired
- Get a new one from https://openrouter.ai/keys

**"Rate limited"**
- Free tier has rate limits
- Wait a few seconds and retry, or use `--delay 1.0` for slower scoring

**Partial scoring (script interrupted)**
- Re-run `python3 score.py` — it will resume from cached results
- Use `--force` if you want to re-score from scratch

## Next Steps

1. Get your OpenRouter key
2. Update `.env`
3. Run `python3 score.py`
4. Run `python3 build_site_data.py`
5. Enjoy the interactive treemap with real AI exposure data! 🎉
