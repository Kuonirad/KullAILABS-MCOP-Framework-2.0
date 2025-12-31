import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  redact: {
    paths: ['*.token', '*.secret', '*.password', '*.key', '*.authorization', '*.apiKey'],
    censor: '[Redacted]',
  },
  transport: process.env.NODE_ENV === 'development' ? { target: 'pino-pretty' } : undefined,
});

export default logger;
