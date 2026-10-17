# Playbook: Django REST API Contracts & Session Authentication

> **Domain:** Backend  
> **Capability ID:** `backend.django_api_contracts`  
> **Target Engine:** Phaser 4.2.1

---

## 1. Purpose & Scope

This playbook guides connecting a Phaser 4 mobile game client to a Django REST framework backend using secure, host-only session cookies and CSRF protection.

---

## 2. Django Client HTTP Adapter

In browser and PWA environments, direct email/password and session cookie authentication must pass `credentials: 'include'` and include the `X-CSRFToken` header for state-changing requests (POST/PUT):

```javascript
export class DjangoApiClient {
  constructor(baseUrl = '') {
    this.baseUrl = baseUrl;
  }

  getCsrfToken() {
    const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (options.method && options.method.toUpperCase() !== 'GET') {
      const csrf = this.getCsrfToken();
      if (csrf) headers['X-CSRFToken'] = csrf;
    }

    const response = await fetch(url, {
      ...options,
      headers,
      credentials: 'include' // Enforce host-only session cookies
    });

    if (!response.ok) {
      throw new Error(`Django API Error [${response.status}]: ${response.statusText}`);
    }
    return response.json();
  }

  async getProfile() {
    return this.request('/api/v1/profile/');
  }

  async saveGameState(payload) {
    return this.request('/api/v1/save/', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  }
}
```

---

## 3. Django Backend Configuration Reference

In Django's `settings.py`:
```python
# Required for Phaser client fetch with credentials
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", # Local dev server
    "https://game.yourdomain.com",
]

CSRF_COOKIE_HTTPONLY = False  # Allows JS to read csrftoken for X-CSRFToken header
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

---

## 4. Verification Checklist

- [ ] Fetch calls to Django include `credentials: 'include'`.
- [ ] POST requests carry valid `X-CSRFToken` header and avoid 403 Forbidden errors.
- [ ] User profile state loads on clean boot if session cookie is present.
