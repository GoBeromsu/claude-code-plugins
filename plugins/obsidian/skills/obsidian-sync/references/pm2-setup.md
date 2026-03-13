# PM2 Sync Daemon -- Fresh Setup

Use this guide when setting up `ob sync --continuous` as a PM2 daemon on a new machine.

## Prerequisites

- PM2 installed: `npm install -g pm2`
- `ob` installed and logged in (see main SKILL.md)
- Vault linked: `ob sync-setup` completed

## Configuration

Replace these placeholders with your actual values:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `<VAULT_PATH>` | Absolute path to your Obsidian vault | `/Users/you/Documents/Obsidian/MyVault` |
| `<PM2_PROCESS_NAME>` | Name for the PM2 process | `obsidian-sync` |
| `<OB_PATH>` | Full path to the `ob` binary | Output of `which ob` |
| `<PM2_LAUNCHAGENT_LABEL>` | LaunchAgent plist label | `com.PM2.yourusername` |
| `<NODE_BIN_PATH>` | Path to your Node.js bin directory | Output of `dirname $(which node)` |

## Setup Steps

```bash
# 1. Install PM2
npm install -g pm2

# 2. Start ob sync as PM2 process
cd <VAULT_PATH>
pm2 start <OB_PATH> --name <PM2_PROCESS_NAME> -- sync --continuous

# 3. Save process list (survives reboot)
pm2 save

# 4. Create LaunchAgent for boot persistence (no sudo needed)
cat > ~/Library/LaunchAgents/<PM2_LAUNCHAGENT_LABEL>.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string><PM2_LAUNCHAGENT_LABEL></string>
    <key>KeepAlive</key>
    <true/>
    <key>ProgramArguments</key>
    <array>
      <string>/bin/sh</string>
      <string>-c</string>
      <string><PM2_PATH> resurrect</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>LaunchOnlyOnce</key>
    <true/>
    <key>EnvironmentVariables</key>
    <dict>
      <key>PATH</key>
      <string><NODE_BIN_PATH>:/usr/local/bin:/usr/bin:/bin</string>
      <key>PM2_HOME</key>
      <string>$HOME/.pm2</string>
    </dict>
    <key>StandardErrorPath</key>
    <string>/tmp/<PM2_LAUNCHAGENT_LABEL>.err</string>
    <key>StandardOutPath</key>
    <string>/tmp/<PM2_LAUNCHAGENT_LABEL>.out</string>
  </dict>
</plist>
EOF

# 5. Load LaunchAgent
launchctl load ~/Library/LaunchAgents/<PM2_LAUNCHAGENT_LABEL>.plist
launchctl list | grep PM2   # verify
```

> **Why LaunchAgent instead of `pm2 startup`**: PM2's built-in `pm2 startup` creates a LaunchDaemon (requires sudo). The manual LaunchAgent approach achieves the same boot persistence without sudo -- it calls `pm2 resurrect` at user login, restoring all saved PM2 processes.

## Quick Reference

To find your actual paths:
```bash
which ob           # OB_PATH
which pm2          # PM2_PATH
dirname $(which node)  # NODE_BIN_PATH
```
