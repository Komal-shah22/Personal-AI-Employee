#!/bin/bash

# Ralph Wiggum Loop - "I'm helping!"
# Wrapper script to start Claude Code with the stop hook enabled

set -e

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Default values
MAX_ITERATIONS=10
PROMPT=""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print banner
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}RALPH WIGGUM LOOP - I'M HELPING!${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --max-iterations)
            MAX_ITERATIONS="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS] \"prompt\""
            echo ""
            echo "Options:"
            echo "  --max-iterations N    Maximum iterations (default: 10)"
            echo "  --help, -h           Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 \"Process all pending tasks\""
            echo "  $0 --max-iterations 20 \"Process all emails and invoices\""
            echo ""
            echo "How it works:"
            echo "  1. Starts Claude Code with your prompt"
            echo "  2. Stop hook checks for unprocessed files in Needs_Action/"
            echo "  3. If files exist: continues working (up to max iterations)"
            echo "  4. If no files or max reached: stops"
            echo ""
            exit 0
            ;;
        *)
            PROMPT="$1"
            shift
            ;;
    esac
done

# Validate prompt
if [ -z "$PROMPT" ]; then
    echo -e "${RED}ERROR: No prompt provided${NC}"
    echo "Usage: $0 \"your prompt here\""
    echo "Run with --help for more information"
    exit 1
fi

# Check if stop hook exists
STOP_HOOK="$PROJECT_DIR/.claude/hooks/stop_hook.py"
if [ ! -f "$STOP_HOOK" ]; then
    echo -e "${RED}ERROR: Stop hook not found at $STOP_HOOK${NC}"
    exit 1
fi

# Make stop hook executable
chmod +x "$STOP_HOOK"

# Check if Claude CLI is installed
if ! command -v claude &> /dev/null; then
    echo -e "${RED}ERROR: Claude CLI not found${NC}"
    echo "Install with: npm install -g @anthropic-ai/claude-cli"
    exit 1
fi

# Initialize loop status
PLANS_DIR="$PROJECT_DIR/AI_Employee_Vault/Plans"
mkdir -p "$PLANS_DIR"

LOOP_STATUS="$PLANS_DIR/loop_status.md"
cat > "$LOOP_STATUS" << EOF
---
iteration: 0
max_iterations: $MAX_ITERATIONS
started: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
last_updated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
status: running
---

# Ralph Wiggum Loop Status

**Current Status**: RUNNING

## Progress

- **Iteration**: 0 of $MAX_ITERATIONS
- **Started**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## Initial Prompt

\`\`\`
$PROMPT
\`\`\`

---

*Loop initialized by ralph-loop.sh*
EOF

echo -e "${GREEN}✓ Loop status initialized${NC}"
echo -e "  Max iterations: ${YELLOW}$MAX_ITERATIONS${NC}"
echo -e "  Status file: $LOOP_STATUS"
echo ""

# Export max iterations for stop hook
export RALPH_MAX_ITERATIONS=$MAX_ITERATIONS

# Change to project directory
cd "$PROJECT_DIR"

echo -e "${CYAN}Starting Claude Code with stop hook...${NC}"
echo -e "${YELLOW}Prompt: $PROMPT${NC}"
echo ""
echo -e "${CYAN}========================================${NC}"
echo ""

# Start Claude with the prompt
# The stop hook will automatically trigger when Claude tries to exit
claude -p "$PROMPT"

# After Claude exits, show final status
echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}RALPH LOOP COMPLETE${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Read final status
if [ -f "$LOOP_STATUS" ]; then
    FINAL_ITERATION=$(grep "^iteration:" "$LOOP_STATUS" | cut -d: -f2 | tr -d ' ')
    FINAL_STATUS=$(grep "^status:" "$LOOP_STATUS" | cut -d: -f2 | tr -d ' ')

    echo -e "Final Status: ${YELLOW}$FINAL_STATUS${NC}"
    echo -e "Iterations: ${YELLOW}$FINAL_ITERATION${NC} of ${YELLOW}$MAX_ITERATIONS${NC}"
    echo ""

    # Check for remaining files
    NEEDS_ACTION_DIR="$PROJECT_DIR/AI_Employee_Vault/Needs_Action"
    if [ -d "$NEEDS_ACTION_DIR" ]; then
        REMAINING=$(find "$NEEDS_ACTION_DIR" -name "*.md" ! -name "_*" | wc -l)
        if [ "$REMAINING" -gt 0 ]; then
            echo -e "${YELLOW}⚠ $REMAINING files remain in Needs_Action/${NC}"
            echo ""
            echo "To continue processing:"
            echo "  $0 --max-iterations $MAX_ITERATIONS \"Continue processing remaining tasks\""
        else
            echo -e "${GREEN}✓ All files processed!${NC}"
        fi
    fi
fi

echo ""
