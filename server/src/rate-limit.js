export class RateLimiter {
  constructor({ limit = 5, windowMs = 60_000, now = Date.now } = {}) {
    this.limit = limit;
    this.windowMs = windowMs;
    this.now = now;
    this.entries = new Map();
  }

  consume(key) {
    const now = this.now();
    const recent = (this.entries.get(key) ?? []).filter((time) => time > now - this.windowMs);
    recent.push(now);
    this.entries.set(key, recent);
    return { allowed: recent.length <= this.limit, retryAfter: Math.max(1, Math.ceil((recent[0] + this.windowMs - now) / 1000)) };
  }

  clear(key) { this.entries.delete(key); }
}

