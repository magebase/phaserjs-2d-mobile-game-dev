# Playbook: Backend Reliability & Edge Observability

> **Domain:** Backend  
> **Capability ID:** `backend.reliability_and_observability`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides instrumenting mobile clients with crash boundaries, exponential backoff network retries, and edge observability to detect runtime regressions before players report them.

---

## 2. Exponential Backoff Network Interceptor

Flaky mobile cellular networks frequently drop connections. Automatically retry transient network failures:

```javascript
export async function fetchWithRetry(url, options = {}, maxRetries = 3, baseDelayMs = 500) {
  let attempt = 0;
  while (attempt < maxRetries) {
    try {
      const response = await fetch(url, options);
      if (response.ok) return response;
      if (response.status >= 500) throw new Error(`Server Error ${response.status}`);
      return response; // Client errors (4xx) should not retry
    } catch (err) {
      attempt++;
      if (attempt >= maxRetries) throw err;
      const delay = baseDelayMs * Math.pow(2, attempt) + Math.random() * 200;
      await new Promise(res => setTimeout(res, delay));
    }
  }
}
```

---

## 3. Global Client Error Boundary

Catch unhandled JavaScript exceptions in Phaser and report them quietly:

```javascript
export function registerCrashHandler(reportEndpoint = '/api/v1/crashes/') {
  window.addEventListener('error', (event) => {
    const payload = {
      message: event.message,
      source: event.filename,
      lineno: event.lineno,
      colno: event.colno,
      stack: event.error ? event.error.stack : null,
      userAgent: navigator.userAgent,
      timestamp: Date.now()
    };

    if (navigator.sendBeacon) {
      navigator.sendBeacon(reportEndpoint, JSON.stringify(payload));
    }
  });

  window.addEventListener('unhandledrejection', (event) => {
    const payload = {
      message: event.reason ? event.reason.message : 'Unhandled Promise Rejection',
      stack: event.reason ? event.reason.stack : null,
      timestamp: Date.now()
    };
    if (navigator.sendBeacon) {
      navigator.sendBeacon(reportEndpoint, JSON.stringify(payload));
    }
  });
}
```

---

## 4. Verification Checklist

- [ ] Network fetch retries up to 3 times with exponential backoff on 5xx errors.
- [ ] Simulated unhandled exception dispatches a crash beacon without alerting the player.
- [ ] Client telemetry operates asynchronously without impacting frame time.
