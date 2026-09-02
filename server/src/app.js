import { randomUUID } from 'node:crypto';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
import { RateLimiter } from './rate-limit.js';
import {
  ValidationError, digestToken, expiredSessionCookie, newSession, parseCookie,
  sessionCookie, validateLoginDto, verifyPassword,
} from './security.js';

const MAX_BODY = 16 * 1024;
const STATIC_TYPES = new Map([
  ['.html', 'text/html; charset=utf-8'], ['.css', 'text/css; charset=utf-8'],
  ['.js', 'text/javascript; charset=utf-8'], ['.json', 'application/json; charset=utf-8'],
  ['.png', 'image/png'], ['.jpg', 'image/jpeg'], ['.jpeg', 'image/jpeg'],
  ['.svg', 'image/svg+xml'], ['.ico', 'image/x-icon'], ['.webp', 'image/webp'],
]);
const DUMMY_HASH = '$argon2id$v=19$m=19456,t=2,p=1$MDEyMzQ1Njc4OWFiY2RlZg==$MjNC57CDZ1O9dKpS0V99XJ5GflKx/86nmcRZqBtMhG8=';

async function jsonBody(request, maximum = MAX_BODY) {
  let size = 0;
  const chunks = [];
  for await (const chunk of request) {
    size += chunk.length;
    if (size > maximum) throw new ValidationError('body', 'El cuerpo excede el tamaño permitido.');
    chunks.push(chunk);
  }
  try { return JSON.parse(Buffer.concat(chunks).toString('utf8')); }
  catch { throw new ValidationError('body', 'JSON inválido.'); }
}

function send(response, status, body, requestId, headers = {}) {
  response.writeHead(status, { 'content-type': 'application/json; charset=utf-8', 'x-request-id': requestId, ...headers });
  response.end(body === undefined ? undefined : JSON.stringify(body));
}

const error = (code, message, requestId, details) => ({ code, message, requestId, ...(details ? { details } : {}) });
const publicIdentity = ({ user, memberships }) => ({
  user: { id: user.id, email: user.email, displayName: user.display_name },
  memberships: memberships.map((m) => ({ id: m.id, tenantId: m.tenant_id, tenantName: m.tenant_name, defaultBranchId: m.default_branch_id, permissions: m.permissions })),
});

async function serveStatic(response, pathname, staticRoot, requestId) {
  if (!staticRoot) return false;
  const relative = pathname === '/' ? 'index.html' : decodeURIComponent(pathname).replace(/^\/+/, '');
  const safe = normalize(relative).replaceAll('\\', '/');
  if (safe.startsWith('../') || safe.includes('/../') || safe.startsWith('.') || safe.includes('/.')) return false;
  const extension = extname(safe).toLowerCase();
  if (!STATIC_TYPES.has(extension)) return false;
  const top = safe.split('/')[0];
  if (['server', 'database', 'docs', 'deployment', 'tools', 'contracts', 'portable', 'var'].includes(top)) return false;
  try {
    const body = await readFile(join(staticRoot, safe));
    response.writeHead(200, { 'content-type': STATIC_TYPES.get(extension), 'x-request-id': requestId, 'cache-control': 'no-cache' });
    response.end(body);
    return true;
  } catch (caught) {
    if (caught.code === 'ENOENT') return false;
    throw caught;
  }
}

export function createApi({ store, sessionSecret, sessionTtlSeconds = 8 * 60 * 60, limiter = new RateLimiter(), staticRoot, localMode = false }) {
  return createServer(async (request, response) => {
    const requestId = request.headers['x-request-id']?.slice(0, 128) || randomUUID();
    const url = new URL(request.url, 'https://local.invalid');
    try {
      if (request.method === 'GET' && ['/api/v1/health', '/health/live', '/health/ready'].includes(url.pathname)) return send(response, 200, { status: 'ok', version: '0.1.0-foundation' }, requestId);
      const isLoopback = ['127.0.0.1', '::1', '::ffff:127.0.0.1'].includes(request.socket.remoteAddress);
      if (localMode && isLoopback && request.method === 'GET' && url.pathname === '/api/v1/local/workshop-state') {
        return send(response, 200, store.getLocalWorkshopState() ?? { schemaVersion: 4, state: null, updatedAt: null }, requestId, { 'cache-control': 'no-store' });
      }
      if (localMode && isLoopback && ['PUT', 'POST'].includes(request.method) && url.pathname === '/api/v1/local/workshop-state') {
        const state = await jsonBody(request, 5 * 1024 * 1024);
        if (!state || typeof state !== 'object' || !Array.isArray(state.clients) || !Array.isArray(state.vehicles) || !Array.isArray(state.workOrders)) {
          throw new ValidationError('body', 'El estado del Taller no es válido.');
        }
        return send(response, 200, store.saveLocalWorkshopState(state), requestId, { 'cache-control': 'no-store' });
      }
      if (request.method === 'GET' && await serveStatic(response, url.pathname, staticRoot, requestId)) return;

      if (request.method === 'POST' && url.pathname === '/api/v1/auth/login') {
        if (!String(request.headers['content-type'] ?? '').toLowerCase().startsWith('application/json')) return send(response, 415, error('UNSUPPORTED_MEDIA_TYPE', 'Se requiere application/json.', requestId), requestId);
        const dto = validateLoginDto(await jsonBody(request));
        const ip = request.socket.remoteAddress ?? 'unknown';
        const key = `${ip}:${dto.email}`;
        const attempt = limiter.consume(key);
        if (!attempt.allowed) return send(response, 429, error('RATE_LIMITED', 'Demasiados intentos.', requestId), requestId, { 'retry-after': attempt.retryAfter });
        const user = store.findLoginIdentity(dto.email);
        const valid = verifyPassword(dto.password, user?.password_hash ?? DUMMY_HASH);
        if (!valid || user?.status !== 'active') return send(response, 401, error('UNAUTHORIZED', 'Credenciales inválidas.', requestId), requestId);
        limiter.clear(key);
        const session = newSession(sessionSecret);
        store.createSession({ userId: user.id, digest: session.digest, ttlSeconds: sessionTtlSeconds, ipAddress: ip, userAgent: request.headers['user-agent'] });
        const identity = store.sessionIdentity(session.digest);
        return send(response, 200, publicIdentity(identity), requestId, { 'set-cookie': sessionCookie(session.token, sessionTtlSeconds), 'cache-control': 'no-store' });
      }

      const token = parseCookie(request.headers.cookie, 'rp_session');
      const digest = token ? digestToken(token, sessionSecret) : null;
      const identity = digest ? store.sessionIdentity(digest) : null;
      if (!identity) return send(response, 401, error('UNAUTHORIZED', 'Sesión ausente, vencida o inválida.', requestId), requestId);

      if (request.method === 'POST' && url.pathname === '/api/v1/auth/logout') {
        store.revokeSession(digest);
        response.writeHead(204, { 'set-cookie': expiredSessionCookie(), 'x-request-id': requestId, 'cache-control': 'no-store' });
        return response.end();
      }
      if (request.method === 'GET' && url.pathname === '/api/v1/me') return send(response, 200, publicIdentity(identity), requestId, { 'cache-control': 'no-store' });
      return send(response, 404, error('NOT_FOUND', 'Recurso no encontrado.', requestId), requestId);
    } catch (caught) {
      if (caught instanceof ValidationError) return send(response, 400, error('VALIDATION_ERROR', caught.message, requestId, { field: caught.field }), requestId);
      console.error(JSON.stringify({ level: 'error', requestId, message: caught.message }));
      return send(response, 500, error('INTERNAL_ERROR', 'Error interno.', requestId), requestId);
    }
  });
}
