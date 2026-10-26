# Agent setup reference

Use this when a coach asks their local Claude Code agent to prepare a coaching workspace. The public repository is `https://github.com/jcavnr-collab/coach-skills`; the plugin ID is `cinch-coach@coach-skills`.

## 1. Start in the coach's permanent folder

The coach downloads [Claude Desktop](https://claude.com/download), signs in, creates an empty `Coaching Workspace` folder, then opens **Code > Local > Open folder** and selects it. Their account must have Claude Code access. Desktop includes the Code agent; the terminal CLI is a separate installation. Keep Worktree off if shown so the session uses the selected folder directly.

Resolve and report the actual workspace path before changing files. Use the local session's file and terminal tools. Preserve existing instructions, briefs, memory and unrelated settings. A web chat or cloud session cannot establish this local workspace without access to the computer.

The intended layout is:

```text
Coaching Workspace/
  CLAUDE.md       Working instructions and context-file locations
  MEMORY.md       Saved preferences and decisions
  Agents/         Named assistants' briefs and handoffs
  coach-skills/   Complete public repository download
```

The parent workspace remains the session folder. Keep personal state outside the public repository and the plugin cache. Do not initialize the parent folder as a public Git repository or upload its contents.

## 2. Download the complete repository

From the workspace root, check whether `coach-skills/` already exists. If it is the correct checkout, preserve local changes and reuse it. If it contains something else, resolve that path with the coach before proceeding.

If Git is available, run:

```bash
git clone https://github.com/jcavnr-collab/coach-skills.git ./coach-skills
```

If Git is unavailable, download the [complete main-branch ZIP](https://github.com/jcavnr-collab/coach-skills/archive/refs/heads/main.zip) and extract it with the operating system's archive tools. Rename the extracted `coach-skills-main` directory to `coach-skills` inside the workspace. Downloading this public repository needs no GitHub invitation or account.

Keep all repository files, including the hidden `.claude-plugin` directory. Verify these paths exist under `coach-skills/`:

- `.claude-plugin/marketplace.json`
- `plugins/cinch-coach/.claude-plugin/plugin.json`
- `plugins/cinch-coach/.mcp.json`
- `plugins/cinch-coach/skills/`
- `docs/agent-setup.md`

A download alone does not load the namespaced skills or MCP configuration. Complete the installation below.

## 3. Install the CLI if needed

Run `claude --version`. If it works, reuse that installation. If the command is missing, first check whether the CLI is already installed but absent from this session's PATH. Keep the coach's existing Claude configuration, including any `CLAUDE_CONFIG_DIR` setting, and confirm it matches the local Desktop environment before registering plugins.

For a missing CLI, identify the actual operating system and shell, then use the matching [official Anthropic installer](https://code.claude.com/docs/en/setup):

**macOS, Linux or WSL, in Bash or Zsh:**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Native Windows, in PowerShell:**

```powershell
irm https://claude.ai/install.ps1 | iex
```

The agent can run the matching command through its terminal tool. Follow the application's normal command approvals. If the session cannot run it, give the coach that exact command to run in Terminal or PowerShell. Use the installed Desktop agent to guide this step; the coach does not need an already-working CLI to ask for help.

Read the installer result, refresh the shell environment as instructed, then run `claude --version` again. If PATH has not refreshed, use the installed executable's verified absolute path for this setup and explain how to reopen the terminal or Desktop. Do not repeatedly reinstall over a PATH issue or weaken organization policies. Let the coach complete any required account sign-in through the official flow.

## 4. Register and install the downloaded skills

Check `claude plugin marketplace list` and `claude plugin list --json` first. For a new setup, run these **in the terminal from the workspace root**:

```bash
claude plugin marketplace add ./coach-skills --scope user
claude plugin install cinch-coach@coach-skills --scope user
```

The first command registers the downloaded repository as the marketplace. The second installs its plugin, skills, assets and CinchOS MCP configuration. User scope applies to the current local Claude configuration on this computer. Keep the downloaded folder in place as the marketplace source.

If `coach-skills` is already registered to the same public GitHub repository or the intended local copy, reuse it. An existing GitHub registration may maintain a separate marketplace cache; the workspace download still provides the complete readable source and guide. If the marketplace name points elsewhere or another `cinch-coach` copy is active, explain the conflict and resolve the intended source with the coach. Preserve unrelated plugins.

For an already installed copy, update only when needed:

```bash
claude plugin marketplace update coach-skills
claude plugin update cinch-coach@coach-skills
```

For a local marketplace, refresh the repository first: check its status, then use `git -C ./coach-skills pull --ff-only` for a clean checkout. Stop on local changes or divergence and preserve them. For a ZIP download, download the new archive separately and replace only the public repository after checking for local edits. The parent's personal files stay in place.

If the requested plugin is disabled, enable it with `claude plugin enable cinch-coach@coach-skills`.

## 5. Prepare saved memory and handoffs

Read any existing workspace files first. Create `Agents/` if missing. Prepare a short `CLAUDE.md` that tells future sessions to:

- Work in this parent workspace and keep the public download in `coach-skills/`.
- Read the workspace's `MEMORY.md` at the start of a session.
- Read `Agents/<agent-name>.md` when resuming a named assistant.
- Save confirmed preferences and durable decisions to `MEMORY.md`, and current work or handoffs to the relevant brief.

Create `MEMORY.md` if missing, initially containing only confirmed setup facts. Keep passwords, tokens and athlete records out of these context files. Merge the startup instructions into an existing `CLAUDE.md` without discarding the coach's rules. The setup prompt authorizes preparing these local files; follow any more specific file-write preferences already supplied by the coach.

These are explicit workspace files. `CLAUDE.md` loads as project instructions; its instruction to read `MEMORY.md` carries the saved context forward. This does not relocate Claude Code's built-in automatic memory, which normally lives under `~/.claude/projects/<project>/memory/`, or copy the previous conversation into a new chat. Keep a private backup of the workspace.

Save a setup handoff in `Agents/setup.md` with the workspace path, download source, CLI and plugin versions, completed checks and remaining reload/sign-in steps. Record missing access as unverified rather than successful. Read the created files back.

## 6. Verify, then open a fresh session

Run:

```bash
claude plugin list --json
claude plugin details cinch-coach@coach-skills
```

Check the ID, version, user scope, enabled state and inventory against the downloaded manifests. The package includes `coach-setup`, `cinchos-guide`, `blog-author` and the other shipped skills, plus `cinchos-coaching` and `cinchos-inbox`. On a client without `plugin details`, inspect the installed manifest, skill folders and `.mcp.json` at the installation path returned by `list`.

Ask the coach to choose **New session** in Desktop, select **Local**, and open the **same parent Coaching Workspace folder**. Keep Worktree off. Supply its actual absolute path so they select the right folder. For a terminal session, open a terminal in that folder and run `claude`.

Give the coach this next message:

```text
Read CLAUDE.md, MEMORY.md and Agents/setup.md.
Check that Coach Skills is loaded, then help me run coach-setup.
```

Check that `/cinch-coach:coach-setup` is available in the new session. If it is absent, inspect plugin enablement and the session's configuration before reinstalling. `/reload-plugins` can refresh an existing session on supported clients; a fresh local session is the standard path in this guide. If Desktop still cannot see the CLI after a PATH change, restart the app.

Report these as separate states: repository downloaded, CLI working, plugin installed, skills loaded in the new session, and services connected. The first three do not prove the last two.

## 7. Connect and personalize

Guide the coach through the available Desktop connection controls. If plugin authentication requires the terminal interface, have them open a terminal in the workspace, run `claude`, then open `/mcp` and sign into the required CinchOS connections with their own account. Reopen the Desktop session afterward and check its actual connection state. The plugin already supplies both server addresses; avoid duplicate manual entries. Credentials belong in the provider's sign-in flow.

Help run:

```text
/cinch-coach:coach-setup
```

The skill interviews the coach and prepares their personal instructions. Preserve the workspace's memory and brief-reading rules when merging those instructions. Follow the skill's draft-review steps. Use `cinchos-guide` for read-only connection checks and record which services are usable. Downloading skills does not grant membership, TrainingPeaks access or mailbox permissions; local assistant and document workflows can still be set up without those connections.

For later sessions, reopen the same parent folder and resume a named assistant from its brief. Re-run setup on another computer and bring over the coach's private workspace through their chosen backup method.

## Manual plugin alternative

For a coach who already has a workspace and only needs the plugin, run these **inside an interactive terminal Claude Code session**:

```text
/plugin marketplace add jcavnr-collab/coach-skills
/plugin install cinch-coach@coach-skills
```

This installs the plugin from GitHub. It does not create the workspace's separate repository copy or memory files. Follow the reload prompt, sign in through `/mcp`, then start `coach-setup`.

Sources: [Desktop quickstart](https://code.claude.com/docs/en/desktop-quickstart), [CLI installation](https://code.claude.com/docs/en/setup), [plugin installation](https://code.claude.com/docs/en/discover-plugins), and [instructions and memory](https://code.claude.com/docs/en/memory). UI labels and command availability can vary by client version.
