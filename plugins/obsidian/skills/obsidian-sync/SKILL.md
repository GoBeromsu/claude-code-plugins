---
name: obsidian-sync
description: "Manage headless Obsidian Sync between local and remote machines using the `obsidian-headless` npm package (CLI: `ob`). Handles the full lifecycle: install, login, vault linking, one-shot sync, continuous watch-mode daemon, status checks, plist daemon setup, and troubleshooting. Use this skill when the user invokes /obsidian-sync, mentions 'obsidian sync', 'vault sync', 'ob sync', 'headless sync', 'obsidian-headless', 'ob login', 'sync setup', or asks about keeping a vault in sync between machines."
---

# Obsidian Sync Skill

Manage headless Obsidian Sync via the `obsidian-headless` npm package between your machines.

## Configuration

Before using this skill, define the following in your `CLAUDE.md` or project settings:

| Variable | Description | Example |
|----------|-------------|---------|
| `<VAULT_PATH>` | Absolute path to your vault | `/Users/you/Documents/Obsidian/MyVault` |
| `<VAULT_NAME>` | Vault name as shown in Obsidian Sync | `MyVault` |
| `<REMOTE_HOST>` | SSH hostname of your remote machine | `my-remote` (configured in `~/.ssh/config`) |
| `<PM2_PROCESS_NAME>` | PM2 process name for the sync daemon | `obsidian-sync` |
| `<LOCAL_DEVICE_NAME>` | Device name for sync version history (local) | `macbook-pro` |
| `<REMOTE_DEVICE_NAME>` | Device name for sync version history (remote) | `mac-mini` |

SSH to remote always uses: `ssh <REMOTE_HOST> "..."` (hostname is configured in `~/.ssh/config`).
For commands needing Homebrew PATH on remote: `ssh <REMOTE_HOST> "zsh -lc '<cmd>'"` or use full path `/opt/homebrew/bin/<tool>`.

## Tool: obsidian-headless

```
npm package : obsidian-headless (official, by obsidianmd)
CLI command : ob
Node.js req : 22+
Official docs: https://help.obsidian.md/sync/headless
```

### Install / Update

```bash
# Install
npm install -g obsidian-headless

# Check current vs latest before updating
npm list -g obsidian-headless    # current installed version
npm info obsidian-headless version  # latest on npm

# Update
npm install -g obsidian-headless@latest

# Then restart daemon on each machine
pm2 restart <PM2_PROCESS_NAME>
ssh <REMOTE_HOST> "zsh -lc 'pm2 restart <PM2_PROCESS_NAME>'"
```

> **`ob --version` vs package version**: `ob --version` shows the CLI's internal version string (e.g. `1.0.0`), NOT the npm package version. Always use `npm list -g obsidian-headless` to get the actual installed package version.

### Key commands

| Command | Purpose |
|---------|---------|
| `ob login` | Interactive auth -- run once per machine |
| `ob sync-list-remote` | List available remote vaults |
| `ob sync-setup --vault "<VAULT_NAME>"` | Link local dir to remote vault |
| `ob sync` | One-shot sync |
| `ob sync --continuous` | Watch-mode sync daemon |
| `ob sync-status` | Show current sync state |
| `ob sync-unlink` | Disconnect vault from remote |

### Auth

- **Account login**: `ob login --email <email> --password "<password>"` -- stores token to `~/.config/obsidian-headless/auth_token`
- **Vault E2E encryption**: separate password passed via `--password` to `ob sync-setup`
- **Daemon (plist)**: no env var needed -- ob reads `~/.config/obsidian-headless/auth_token` automatically. Just set `HOME` in plist `EnvironmentVariables`.

> **Shell gotcha**: if the password contains `!`, wrap it in double quotes in the command string. In zsh single-quoted strings `!` is literal, but passing via `ssh "..."` can mangle it. Safest: use node to spawn the command:
> ```bash
> node -e "const {execSync}=require('child_process'); console.log(execSync('ob login --email X --password \"Y!\"', {encoding:'utf8', stdio:['pipe','pipe','pipe']}))"
> ```

---

## Capabilities

### 1. Check & Install

Before anything, verify `ob` is installed and Node.js is 22+.

```bash
# Local
node --version    # must be v22+
which ob          # if missing -> install

# Remote (use login shell for PATH)
ssh <REMOTE_HOST> "zsh -lc 'node --version'"
ssh <REMOTE_HOST> "zsh -lc 'which ob'"
```

If `ob` is missing:
```bash
# Local
npm install -g obsidian-headless

# Remote
ssh <REMOTE_HOST> "zsh -lc 'npm install -g obsidian-headless'"
```

If Node.js is below 22, see **Troubleshooting** section.

### 2. Login

`ob login` stores credentials to `~/.config/obsidian-headless/auth_token` (not keychain).
Use `--email`/`--password` flags for non-interactive login. If password contains `!`, use node to avoid shell escaping issues.

```bash
# Local
node -e "const {execSync}=require('child_process'); console.log(execSync('ob login --email EMAIL --password \"PASS\"', {encoding:'utf8', stdio:['pipe','pipe','pipe']}))"

# Remote
ssh <REMOTE_HOST> "zsh -lc 'node -e \"const {execSync}=require(\\\"child_process\\\"); console.log(execSync(\\\"ob login --email EMAIL --password PASS\\\", {encoding:\\\"utf8\\\", stdio:[\\\"pipe\\\",\\\"pipe\\\",\\\"pipe\\\"]}))\"'"
```

### 3. Link Vault

`ob sync-setup` requires `--password` for E2E encryption (separate from account login password).
Use `--device-name` to identify the device in sync version history.

```bash
# Local
cd <VAULT_PATH> && ob sync-setup --vault "<VAULT_NAME>" --password "VAULT_ENC_PASS" --device-name "<LOCAL_DEVICE_NAME>"

# Remote
ssh <REMOTE_HOST> "zsh -lc 'cd <VAULT_PATH> && ob sync-setup --vault \"<VAULT_NAME>\" --password \"VAULT_ENC_PASS\" --device-name \"<REMOTE_DEVICE_NAME>\"'"

# List available remote vaults if unsure of the vault name
ob sync-list-remote
ssh <REMOTE_HOST> "zsh -lc 'ob sync-list-remote'"
```

### 4. Run Sync

```bash
# One-shot (local)
cd <VAULT_PATH> && ob sync

# One-shot (remote)
ssh <REMOTE_HOST> "zsh -lc 'cd <VAULT_PATH> && ob sync'"

# Continuous watch mode (foreground)
cd <VAULT_PATH> && ob sync --continuous
```

### 5. Status Check

```bash
# Local
cd <VAULT_PATH> && ob sync-status

# Remote
ssh <REMOTE_HOST> "zsh -lc 'cd <VAULT_PATH> && ob sync-status'"
```

### 6. Setup Continuous Sync Daemon (PM2)

Both machines run `ob sync --continuous` as a **PM2-managed process** with a LaunchAgent for boot persistence.

#### Day-to-day management

```bash
# Check status (both machines)
pm2 list
ssh <REMOTE_HOST> "zsh -lc 'pm2 list'"

# View logs
pm2 logs <PM2_PROCESS_NAME> --lines 30
ssh <REMOTE_HOST> "zsh -lc 'pm2 logs <PM2_PROCESS_NAME> --lines 30 --nostream'"

# Restart
pm2 restart <PM2_PROCESS_NAME>
ssh <REMOTE_HOST> "zsh -lc 'pm2 restart <PM2_PROCESS_NAME>'"

# Stop / start
pm2 stop <PM2_PROCESS_NAME>
pm2 start <PM2_PROCESS_NAME>
```

For **fresh setup on a new machine** (PM2 install + LaunchAgent plist creation), see [`references/pm2-setup.md`](references/pm2-setup.md).

---

## Troubleshooting

### `ob: command not found`
-> Install: `npm install -g obsidian-headless`
-> If installed but not found in SSH: use full path `$(npm root -g)/../bin/ob` or `zsh -lc 'ob ...'`

### Node.js version too old (< 22)

**via nvm** (if nvm is installed):
```bash
nvm install 22
nvm use 22
nvm alias default 22
```

**via Homebrew**:
```bash
brew install node@22
brew link --overwrite node@22
```

### Keychain access denied (auth fails non-interactively)
-> Use `OBSIDIAN_AUTH_TOKEN` env var instead of keychain
-> Get token: `ob login` interactively, then copy token from output or `security find-generic-password -s 'obsidian-headless' -w`
-> Set in plist's `EnvironmentVariables` dict

### SSH connection to remote fails
-> Check Tailscale or your VPN/network configuration
-> Quick check: `ssh -o ConnectTimeout=5 <REMOTE_HOST> "echo ok"`

### Sync conflicts
-> `ob sync-status` shows conflict details
-> By default, Obsidian Sync keeps both versions -- check the `.obsidian/trash/` folder

### PM2 process not running after reboot
-> Check LaunchAgent loaded: `launchctl list | grep PM2`
-> Check PM2 resurrect log: `cat /tmp/<PM2_LAUNCHAGENT_LABEL>.err`
-> Ensure `pm2 save` was run before reboot: `ls $HOME/.pm2/dump.pm2`
-> Manual resurrect: `pm2 resurrect`

### PM2 process errored/stopped
-> `pm2 logs <PM2_PROCESS_NAME>` -- check error output
-> Verify vault is linked: `cd <VAULT_PATH> && ob sync-status`
-> Verify auth token: `cat ~/.config/obsidian-headless/auth_token`
-> Restart: `pm2 restart <PM2_PROCESS_NAME>`
