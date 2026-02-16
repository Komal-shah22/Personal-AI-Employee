# PM2 Ecosystem Configuration for Personal AI Employee

module.exports = {
  apps: [
    {
      name: 'gmail-watcher',
      script: 'watchers/gmail_watcher.py',
      interpreter: 'python3',
      watch: false,
      autorestart: true,
      max_restarts: 10,
      min_uptime: '10s',
      restart_delay: 5000,
      error_file: 'AI_Employee_Vault/Logs/pm2-gmail-error.log',
      out_file: 'AI_Employee_Vault/Logs/pm2-gmail-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss'
    },
    {
      name: 'whatsapp-watcher',
      script: 'watchers/whatsapp_watcher.py',
      interpreter: 'python3',
      watch: false,
      autorestart: true,
      max_restarts: 10,
      min_uptime: '10s',
      restart_delay: 5000,
      error_file: 'AI_Employee_Vault/Logs/pm2-whatsapp-error.log',
      out_file: 'AI_Employee_Vault/Logs/pm2-whatsapp-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss'
    },
    {
      name: 'file-watcher',
      script: 'watchers/filesystem_watcher.py',
      interpreter: 'python3',
      watch: false,
      autorestart: true,
      max_restarts: 10,
      min_uptime: '10s',
      restart_delay: 5000,
      error_file: 'AI_Employee_Vault/Logs/pm2-file-error.log',
      out_file: 'AI_Employee_Vault/Logs/pm2-file-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss'
    },
    {
      name: 'orchestrator',
      script: 'orchestrator.py',
      interpreter: 'python3',
      watch: false,
      autorestart: false,
      cron_restart: '*/5 * * * *',  // Every 5 minutes
      error_file: 'AI_Employee_Vault/Logs/pm2-orchestrator-error.log',
      out_file: 'AI_Employee_Vault/Logs/pm2-orchestrator-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss'
    }
  ]
};
