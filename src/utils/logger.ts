import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  redact: [
    'req.headers.authorization',
    'req.headers.cookie',
    'password',
    '*.password',
    'token',
    '*.token',
    'secret',
    '*.secret',
    'key',
    '*.key',
    'credential',
    '*.credential',
    'access_token',
    '*.access_token',
    'refreshToken',
    '*.refreshToken',
    'apiKey',
    '*.apiKey',
    'api_key',
    '*.api_key'
  ],
  transport: process.env.NODE_ENV === 'development' ? { target: 'pino-pretty' } : undefined,
});

export default logger;
