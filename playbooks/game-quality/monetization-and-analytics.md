# Playbook: Rewarded Ads, IAP & Event Analytics

> **Domain:** Game Quality  
> **Capability ID:** `game_quality.monetization_and_analytics`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides integrating non-intrusive rewarded ads (e.g. revive on defeat, double coins), web/PWA checkout flows, and privacy-preserving lightweight telemetry.

---

## 2. Rewarded Ad Lifecycle Wrapper

Rewarded ads must be fail-safe: if the ad provider fails to fill or network drops, never lock the player in an unrecoverable state:

```javascript
export class AdManager {
  static showRewardedRevive(onRewarded, onFailed) {
    // If running in PWA or web context with AdSense / CrazyGames / Poki
    if (window.AdProvider && typeof window.AdProvider.showReward === 'function') {
      window.AdProvider.showReward()
        .then(() => onRewarded())
        .catch((err) => {
          console.warn('[AdManager] Ad failed or dismissed:', err);
          onFailed(err);
        });
    } else {
      // Offline / dev fallback: grant reward directly or notify
      console.log('[AdManager] Ad provider unavailable; granting dev reward');
      onRewarded();
    }
  }
}
```

---

## 3. Privacy-Preserving Event Telemetry

Dispatch high-value funnel events without bloating client requests:

```javascript
export class GameAnalytics {
  static trackEvent(eventName, properties = {}) {
    const payload = {
      event: eventName,
      timestamp: Date.now(),
      props: properties
    };

    // Use sendBeacon for reliable background transmission
    if (navigator.sendBeacon) {
      navigator.sendBeacon('/api/v1/telemetry/', JSON.stringify(payload));
    } else {
      fetch('/api/v1/telemetry/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        keepalive: true
      }).catch(() => {});
    }
  }
}
```

---

## 4. Verification Checklist

- [ ] Ad dismissal or network failure does not freeze game loop; callbacks return control.
- [ ] Analytics telemetry calls never block rendering or frame updates.
- [ ] No personally identifiable information (PII) is included in telemetry payloads.
