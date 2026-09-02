# API de seguridad (fundación)

Base ejecutable para `/api/v1/health`, `/api/v1/auth/login`, `/api/v1/auth/logout` y `/api/v1/me`.

Requiere Node 24.7 o superior (Argon2id y SQLite nativos). No se debe exponer detrás de HTTP: la cookie siempre usa `Secure` y el proxy debe terminar TLS.

```powershell
cd server
npm test
$env:SESSION_SECRET = '<secreto aleatorio de al menos 32 caracteres>'
$env:DATABASE_PATH = '..\data\repuestospro.sqlite'
$env:RUN_MIGRATIONS = '1' # solo al crear una base vacía
npm start
```

El proceso no crea usuarios iniciales ni contiene secretos por defecto. El tenant se obtiene exclusivamente desde membresías activas. Todo repositorio operacional nuevo debe recibir un `RequestContext` generado por `requestContext`, filtrar por `tenantId` y comprobar un permiso concreto.

La limitación de login incluida es local al proceso. Antes de escalar horizontalmente debe reemplazarse por un adaptador compartido (por ejemplo Redis), manteniendo la misma política y agregando métricas.

