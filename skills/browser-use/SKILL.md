---
name: browser-use
description: Automates browser interactions for web testing, form filling, screenshots, and data extraction. Use when the user needs to navigate websites, interact with web pages, fill forms, take screenshots, or extract information from web pages.
allowed-tools: Bash(browser-use:*)
---

# Browser Automation with browser-use CLI

The `browser-use` command provides fast, persistent browser automation. It maintains browser sessions across commands, enabling complex multi-step workflows.

## Prerequisites

Before using this skill, `browser-use` must be installed and configured. Run diagnostics to verify:

```bash
browser-use doctor
```

For more information, see https://github.com/browser-use/browser-use/blob/main/browser_use/skill_cli/README.md

## Core Workflow

1. **Navigate**: `browser-use open <url>` - Opens URL (starts browser if needed)
2. **Inspect**: `browser-use state` - Returns clickable elements with indices
3. **Interact**: Use indices from state to interact (`browser-use click 5`, `browser-use input 3 "text"`)
4. **Verify**: `browser-use state` or `browser-use screenshot` to confirm actions
5. **Repeat**: Browser stays open between commands

## Browser Modes

```bash
browser-use --browser chromium open <url>      # Default: headless Chromium
browser-use --browser chromium --headed open <url>  # Visible Chromium window
browser-use --browser real open <url>          # Real Chrome (no profile = fresh)
browser-use --browser real --profile "Default" open <url>  # Real Chrome with your login sessions
browser-use --browser remote open <url>        # Cloud browser
```

- **chromium**: Fast, isolated, headless by default
- **real**: Uses a real Chrome binary. Without `--profile`, uses a persistent but empty CLI profile at `~/.config/browseruse/profiles/cli/`. With `--profile "ProfileName"`, copies your actual Chrome profile (cookies, logins, extensions)
- **remote**: Cloud-hosted browser with proxy support

## Essential Commands

```bash
# Navigation
browser-use open <url>                    # Navigate to URL
browser-use back                          # Go back
browser-use scroll down                   # Scroll down (--amount N for pixels)

# Page State (always run state first to get element indices)
browser-use state                         # Get URL, title, clickable elements
browser-use screenshot                    # Take screenshot (base64)
browser-use screenshot path.png           # Save screenshot to file

# Interactions (use indices from state)
browser-use click <index>                 # Click element
browser-use type "text"                   # Type into focused element
browser-use input <index> "text"          # Click element, then type
browser-use keys "Enter"                  # Send keyboard keys
browser-use select <index> "option"       # Select dropdown option

# Data Extraction
browser-use eval "document.title"         # Execute JavaScript
browser-use get text <index>              # Get element text
browser-use get html --selector "h1"      # Get scoped HTML

# Wait
browser-use wait selector "h1"            # Wait for element
browser-use wait text "Success"          # Wait for text

# Session
browser-use sessions                      # List active sessions
browser-use close                         # Close current session
browser-use close --all                   # Close all sessions

# AI Agent
browser-use -b remote run "task"         # Run agent in cloud (async by default)
browser-use task status <id>              # Check cloud task progress
```

## Commands

### Navigation & Tabs
```bash
browser-use open <url>                    # Navigate to URL
browser-use back                          # Go back in history
browser-use scroll down                   # Scroll down
browser-use scroll up                    # Scroll up
browser-use scroll down --amount 1000    # Scroll by specific pixels (default: 500)
browser-use switch <tab>                  # Switch to tab by index
browser-use close-tab                    # Close current tab
browser-use close-tab <tab>              # Close specific tab
```

### Page State
```bash
browser-use state                         # Get URL, title, and clickable elements
browser-use screenshot                    # Take screenshot (outputs base64)
browser-use screenshot path.png           # Save screenshot to file
browser-use screenshot --full path.png   # Full page screenshot
```

### Interactions
```bash
browser-use click <index>                # Click element
browser-use type "text"                  # Type text into focused element
browser-use input <index> "text"         # Click element, then type text
browser-use keys "Enter"                 # Send keyboard keys
browser-use keys "Control+a"             # Send key combination
browser-use select <index> "option"      # Select dropdown option
browser-use hover <index>                # Hover over element (triggers CSS :hover)
browser-use dblclick <index>             # Double-click element
browser-use rightclick <index>           # Right-click element (context menu)
```

Use indices from `browser-use state`.

### JavaScript & Data
```bash
browser-use eval "document.title"        # Execute JavaScript, return result
browser-use get title                    # Get page title
browser-use get html                     # Get full page HTML
browser-use get html --selector "h1"     # Get HTML of specific element
browser-use get text <index>             # Get text content of element
browser-use get value <index>            # Get value of input/textarea
browser-use get attributes <index>       # Get all attributes of element
browser-use get bbox <index>             # Get bounding box (x, y, width, height)
```

### Cookies
```bash
browser-use cookies get                  # Get all cookies
browser-use cookies get --url <url>      # Get cookies for specific URL
browser-use cookies set <name> <value>   # Set a cookie
browser-use cookies set name val --domain .example.com --secure --http-only
browser-use cookies set name val --same-site Strict  # SameSite: Strict, Lax, or None
browser-use cookies set name val --expires 1735689600  # Expiration timestamp
browser-use cookies clear                # Clear all cookies
browser-use cookies clear --url <url>   # Clear cookies for specific URL
browser-use cookies export <file>        # Export all cookies to JSON file
browser-use cookies export <file> --url <url>  # Export cookies for specific URL
browser-use cookies import <file>        # Import cookies from JSON file
```

### Wait Conditions
```bash
browser-use wait selector "h1"          # Wait for element to be visible
browser-use wait selector ".loading" --state hidden  # Wait for element to disappear
browser-use wait selector "#btn" --state attached    # Wait for element in DOM
browser-use wait text "Success"          # Wait for text to appear
browser-use wait selector "h1" --timeout 5000  # Custom timeout in ms
```

### Python Execution
```bash
browser-use python "x = 42"              # Set variable
browser-use python "print(x)"            # Access variable (outputs: 42)
browser-use python "print(browser.url)"  # Access browser object
browser-use python --vars                # Show defined variables
browser-use python --reset               # Clear Python namespace
browser-use python --file script.py      # Execute Python file
```

The Python session maintains state across commands. The `browser` object provides:
- `browser.url`, `browser.title`, `browser.html` — page info
- `browser.goto(url)`, `browser.back()` — navigation
- `browser.click(index)`, `browser.type(text)`, `browser.input(index, text)`, `browser.keys(keys)` — interactions
- `browser.screenshot(path)`, `browser.scroll(direction, amount)` — visual
- `browser.wait(seconds)`, `browser.extract(query)` — utilities

### Agent Tasks

#### Remote Mode Options

When using `--browser remote`, additional options are available:

```bash
# Specify LLM model
browser-use -b remote run "task" --llm gpt-4o
browser-use -b remote run "task" --llm claude-sonnet-4-20250514

# Proxy configuration (default: us)
browser-use -b remote run "task" --proxy-country uk

# Session reuse
browser-use -b remote run "task 1" --keep-alive        # Keep session alive after task
browser-use -b remote run "task 2" --session-id abc-123 # Reuse existing session

# Execution modes
browser-use -b remote run "task" --flash       # Fast execution mode
browser-use -b remote run "task" --wait       # Wait for completion (default: async)

# Advanced options
browser-use -b remote run "task" --thinking   # Extended reasoning mode
browser-use -b remote run "task" --no-vision  # Disable vision (enabled by default)

# Using a cloud profile
browser-use session create --profile <cloud-profile-id> --keep-alive
browser-use -b remote run "task" --session-id <session-id>

# Task configuration
browser-use -b remote run "task" --start-url https://example.com
browser-use -b remote run "task" --allowed-domain example.com
browser-use -b remote run "task" --structured-output '{"type":"object"}'
browser-use -b remote run "task" --judge
browser-use -b remote run "task" --judge-ground-truth "expected answer"
```

### Task Management
```bash
browser-use task list                    # List recent tasks
browser-use task list --limit 20         # Show more tasks
browser-use task list --status finished  # Filter by status
browser-use task list --json             # JSON output

browser-use task status <task-id>        # Get task status
browser-use task status <task-id> -c    # All steps with reasoning
browser-use task status <task-id> -v    # All steps with URLs + actions
browser-use task status <task-id> --last 5  # Last N steps
browser-use task stop <task-id>          # Stop a running task
browser-use task logs <task-id>          # Get execution logs
```

### Cloud Session Management
```bash
browser-use session list                 # List cloud sessions
browser-use session list --status active
browser-use session get <session-id>    # Get session details + live URL
browser-use session stop <session-id>   # Stop a session
browser-use session stop --all          # Stop all active sessions
browser-use session create --keep-alive
browser-use session create --start-url https://example.com
browser-use session share <session-id>  # Create public share URL
```

### Tunnels
```bash
browser-use tunnel <port>                # Start tunnel (returns URL)
browser-use tunnel list                  # Show active tunnels
browser-use tunnel stop <port>          # Stop tunnel
browser-use tunnel stop --all           # Stop all tunnels
```

### Profile Management

#### Local Chrome Profiles (`--browser real`)
```bash
browser-use -b real profile list         # List local Chrome profiles
browser-use -b real profile cookies "Default"  # Show cookie domains in profile
```

#### Cloud Profiles (`--browser remote`)
```bash
browser-use -b remote profile list
browser-use -b remote profile get <id>
browser-use -b remote profile create --name "My Profile"
browser-use -b remote profile update <id> --name "New"
browser-use -b remote profile delete <id>
```

#### Syncing
```bash
browser-use profile sync --from "Default" --domain github.com
browser-use profile sync --from "Default"
```

## Common Workflows

### Exposing Local Dev Servers
```bash
# 1. Start your dev server
npm run dev &  # localhost:3000

# 2. Expose via tunnel
browser-use tunnel 3000
# → url: https://abc.trycloudflare.com

# 3. Cloud browser can now reach your local server
browser-use --browser remote open https://abc.trycloudflare.com
```

### Authenticated Browsing with Profiles
```bash
# Use your existing Chrome login session
browser-use --browser real --profile "Default" open https://github.com
browser-use state
```

## Installation on Windows

```bash
# Requires Python 3.8+
pip install browser-use
browser-use doctor   # Verify installation
```

## Security Notes

- Prefer local Chromium mode (`--browser chromium`) for sensitive sites
- `--browser remote` sends browsing data to browser-use cloud
- `--profile "ProfileName"` accesses your real Chrome profile (cookies, logins)
- Tunnel creates public URLs to local ports — use with caution
