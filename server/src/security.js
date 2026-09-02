import {
  argon2Sync,
  createHmac,
  randomBytes,
  timingSafeEqual,
} from 'node:crypto';

const ARGON_VERSION = 19;
const ARGON_MEMORY = 19456;
const ARGON_PASSES = 2;
const ARGON_PARALLELISM = 1;
const HASH_BYTES = 32;

function derive(password, salt, params = {}) {
  return Buffer.from(argon2Sync('argon2id', {
    message: Buffer.from(password, 'utf8'),
    nonce: salt,
    parallelism: params.parallelism ?? ARGON_PARALLELISM,
    tagLength: HASH_BYTES,
    memory: params.memory ?? ARGON_MEMORY,
    passes: params.passes ?? ARGON_PASSES,
  }));
}

export function hashPassword(password) {
  assertPassword(password);
  const salt = randomBytes(16);
  const hash = derive(password, salt);
  return `$argon2id$v=${ARGON_VERSION}$m=${ARGON_MEMORY},t=${ARGON_PASSES},p=${ARGON_PARALLELISM}$${salt.toString('base64')}$${hash.toString('base64')}`;
}

export function verifyPassword(password, encoded) {
  try {
    const parts = encoded.split('$');
    if (parts.length !== 6 || parts[1] !== 'argon2id' || parts[2] !== `v=${ARGON_VERSION}`) return false;
    const match = /^m=(\d+),t=(\d+),p=(\d+)$/.exec(parts[3]);
    if (!match || typeof password !== 'string' || password.length > 1024) return false;
    const [memory, passes, parallelism] = match.slice(1).map(Number);
    if (memory < ARGON_MEMORY || passes < ARGON_PASSES || parallelism < 1) return false;
    const expected = Buffer.from(parts[5], 'base64');
    const actual = derive(password, Buffer.from(parts[4], 'base64'), { memory, passes, parallelism });
    return expected.length === actual.length && timingSafeEqual(expected, actual);
  } catch {
    return false;
  }
}

export function assertPassword(password) {
  if (typeof password !== 'string' || password.length < 10 || password.length > 1024) {
    throw new ValidationError('password', 'Debe tener entre 10 y 1024 caracteres.');
  }
}

export function normalizeEmail(email) {
  if (typeof email !== 'string' || email.length > 254) throw new ValidationError('email', 'Correo inválido.');
  const normalized = email.trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalized)) throw new ValidationError('email', 'Correo inválido.');
  return normalized;
}

export function validateLoginDto(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new ValidationError('body', 'JSON inválido.');
  const extra = Object.keys(value).filter((key) => !['email', 'password'].includes(key));
  if (extra.length) throw new ValidationError('body', 'Contiene propiedades no permitidas.');
  return { email: normalizeEmail(value.email), password: (assertPassword(value.password), value.password) };
}

export function newSession(sessionSecret) {
  const token = randomBytes(32).toString('base64url');
  return { token, digest: digestToken(token, sessionSecret) };
}

export function digestToken(token, sessionSecret) {
  if (typeof sessionSecret !== 'string' || sessionSecret.length < 32) throw new Error('SESSION_SECRET debe tener al menos 32 caracteres');
  return createHmac('sha256', sessionSecret).update(token, 'utf8').digest('hex');
}

export function parseCookie(header, name) {
  for (const part of String(header ?? '').split(';')) {
    const index = part.indexOf('=');
    if (index >= 0 && part.slice(0, index).trim() === name) {
      try { return decodeURIComponent(part.slice(index + 1).trim()); }
      catch { return null; }
    }
  }
  return null;
}

export function sessionCookie(token, maxAgeSeconds) {
  return `rp_session=${encodeURIComponent(token)}; Path=/api/v1; HttpOnly; Secure; SameSite=Strict; Max-Age=${maxAgeSeconds}`;
}

export function expiredSessionCookie() {
  return 'rp_session=; Path=/api/v1; HttpOnly; Secure; SameSite=Strict; Max-Age=0';
}

export class ValidationError extends Error {
  constructor(field, message) {
    super(message);
    this.name = 'ValidationError';
    this.field = field;
  }
}

