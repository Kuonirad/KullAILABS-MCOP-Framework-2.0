import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: process.env.NODE_ENV === 'development' ? { target: 'pino-pretty' } : undefined,
  redact: {
    paths: [
      '*.token',
      '*.secret',
      '*.password',
      '*.key',
      '*.authorization',
      '*.apiKey',
      'token',
      'secret',
      'password',
      'key',
      'authorization',
      'apiKey'
    ],
    remove: false, // Set to true if you want to remove the field entirely, false to redact it
  },
});

export default logger;
