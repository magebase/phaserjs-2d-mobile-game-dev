# Playbook: Identity, Cloud Saves & Conflict Resolution

> **Domain:** Backend  
> **Capability ID:** `backend.identity_save_state_and_progression`  
> **Target Engine:** Phaser 4.2.1  
> **Resolves Hard Blocker:** RB-06 (Save / Progress Data Loss)

---

## 1. Purpose & Scope

This playbook guides implementing a resilient, offline-first save system for Phaser 4 games. It guarantees that player progression is immediately saved locally, synchronized to the cloud when connected, and gracefully resolved during sync conflicts.

---

## 2. Local-First Save Architecture

Never make local progression dependent on synchronous server responses:

```javascript
export class SaveStateManager {
  constructor(apiClient) {
    this.api = apiClient;
    this.storageKey = 'phaser_game_save_v1';
    this.pendingSync = false;

    // Listen for reconnection
    window.addEventListener('online', () => this.syncToCloud());
  }

  getLocalState() {
    try {
      const data = localStorage.getItem(this.storageKey);
      return data ? JSON.parse(data) : this.getDefaultState();
    } catch {
      return this.getDefaultState();
    }
  }

  getDefaultState() {
    return {
      version: 1,
      updatedAt: Date.now(),
      level: 1,
      coins: 0,
      inventory: []
    };
  }

  saveLocal(mutations) {
    const current = this.getLocalState();
    const updated = {
      ...current,
      ...mutations,
      updatedAt: Date.now()
    };

    localStorage.setItem(this.storageKey, JSON.stringify(updated));
    this.syncToCloud();
    return updated;
  }

  async syncToCloud() {
    if (!navigator.onLine || !this.api || this.pendingSync) return;
    this.pendingSync = true;

    try {
      const localState = this.getLocalState();
      const serverResponse = await this.api.saveGameState(localState);

      // Conflict resolution: if server has newer state, resolve
      if (serverResponse && serverResponse.updatedAt > localState.updatedAt) {
        localStorage.setItem(this.storageKey, JSON.stringify(serverResponse));
      }
    } catch (err) {
      console.warn('[SaveManager] Cloud sync deferred (offline or server error):', err.message);
    } finally {
      this.pendingSync = false;
    }
  }
}
```

---

## 3. Conflict Resolution Strategy

When resolving save conflicts between multiple devices:
1. **Timestamp Check**: If server `updatedAt > local updatedAt`, inspect progression.
2. **Progression Monotonicity**: Maximize level, unlocked chapters, and total score:
   $$\text{Resolved Level} = \max(\text{local.level}, \text{remote.level})$$
3. **Currency Merge**: Retain the higher balance or sum delta earnings.

---

## 4. Verification Checklist

- [ ] Hard-refreshing the browser tab preserves current score, level, and items.
- [ ] Simulating offline mode (`navigator.onLine = false`) still allows gameplay and saves locally.
- [ ] Restoring online connectivity triggers background sync without freezing gameplay.
