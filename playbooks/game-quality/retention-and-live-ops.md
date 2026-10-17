# Playbook: Daily Rewards, Quests & Retention LiveOps

> **Domain:** Game Quality  
> **Capability ID:** `game_quality.retention_and_live_ops`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides implementing retention mechanics: 7-day daily login streaks, quest tracking systems, and remote live-ops configuration via Cloudflare KV or Django backends.

---

## 2. Daily Login Streak Architecture

Track login calendar status resiliently using UTC midnight timestamps:

```javascript
export class DailyRewardManager {
  static checkDailyReward() {
    const lastClaim = localStorage.getItem('last_daily_claim');
    const streak = parseInt(localStorage.getItem('daily_streak') || '0', 10);
    const now = Date.now();
    const oneDayMs = 86400000;

    if (!lastClaim) {
      return { canClaim: true, day: 1, streak: 1 };
    }

    const elapsed = now - parseInt(lastClaim, 10);
    if (elapsed >= oneDayMs && elapsed < oneDayMs * 2) {
      // Valid consecutive day login
      const nextDay = (streak % 7) + 1;
      return { canClaim: true, day: nextDay, streak: streak + 1 };
    } else if (elapsed >= oneDayMs * 2) {
      // Streak broken, reset to day 1
      return { canClaim: true, day: 1, streak: 1 };
    }

    return { canClaim: false, nextAvailableInMs: oneDayMs - elapsed };
  }

  static claimReward(day) {
    localStorage.setItem('last_daily_claim', Date.now().toString());
    localStorage.setItem('daily_streak', day.toString());
  }
}
```

---

## 3. Remote Feature Configuration (LiveOps)

Fetch remote balance tweaks or event flags without requiring a full code re-deploy:

```javascript
export async function fetchLiveConfig(apiUrl = '/api/v1/config/') {
  try {
    const res = await fetch(apiUrl);
    if (res.ok) {
      const config = await res.json();
      return config; // e.g. { doubleXpWeekend: true, holidayTheme: 'halloween' }
    }
  } catch (err) {
    console.warn('[LiveOps] Failed to fetch remote config; using local fallback');
  }
  return { doubleXpWeekend: false, holidayTheme: 'default' };
}
```

---

## 4. Verification Checklist

- [ ] Daily streak increments properly on simulated 24-hour time forward step.
- [ ] Streak resets to Day 1 after 48 hours of inactivity.
- [ ] Network failure during live config fetch gracefully defaults to local presets.
