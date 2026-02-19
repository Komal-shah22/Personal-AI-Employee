#!/usr/bin/env node
/**
 * Health check for Docker container
 * Exits 0 if healthy, 1 if unhealthy
 */
const fs = require('fs');
const path = require('path');

const VAULT_PATH = process.env.VAULT_PATH || '/app/AI_Employee_Vault';
const MAX_STALE_MINUTES = 10;

function checkHealth() {
  try {
    // Check if vault is accessible
    const vaultExists = fs.existsSync(VAULT_PATH);
    if (!vaultExists) {
      console.error('UNHEALTHY: Vault not found');
      process.exit(1);
    }

    // Check last activity timestamp
    const logsPath = path.join(VAULT_PATH, 'Logs');
    const logFiles = fs.readdirSync(logsPath)
      .filter(f => f.endsWith('.json'))
      .sort()
      .reverse();

    if (logFiles.length === 0) {
      console.error('UNHEALTHY: No log files found');
      process.exit(1);
    }

    const latestLog = path.join(logsPath, logFiles[0]);
    const stats = fs.statSync(latestLog);
    const ageMinutes = (Date.now() - stats.mtimeMs) / 1000 / 60;

    if (ageMinutes > MAX_STALE_MINUTES) {
      console.error(`UNHEALTHY: No activity for ${ageMinutes.toFixed(1)} minutes`);
      process.exit(1);
    }

    console.log('HEALTHY');
    process.exit(0);

  } catch (error) {
    console.error('UNHEALTHY:', error.message);
    process.exit(1);
  }
}

checkHealth();
