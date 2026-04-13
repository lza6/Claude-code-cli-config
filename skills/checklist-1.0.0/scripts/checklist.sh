#!/bin/bash

# Checklist - Task Checklist Manager for AI Agents

set -e

CHECKLIST_DIR="${HOME}/.checklist"
ACTIVE_DIR="${CHECKLIST_DIR}/active"
TEMPLATES_DIR="${CHECKLIST_DIR}/templates"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

mkdir -p "${CHECKLIST_DIR}" "${ACTIVE_DIR}" "${TEMPLATES_DIR}"

print_status() {
    echo -e "${BLUE}[checklist]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# List available templates
cmd_templates() {
    print_status "Available templates:"
    echo ""
    
    local count=1
    for template in "${TEMPLATES_DIR}"/*.json; do
        if [[ -f "$template" ]]; then
            local name=$(basename "$template" .json)
            local desc=$(jq -r '.description // "No description"' "$template" 2>/dev/null || echo "Template")
            echo "  $count. $name - $desc"
            ((count++))
        fi
    done
    
    if [[ $count -eq 1 ]]; then
        echo "  No templates yet. Use 'checklist create <name>' to create one."
    fi
}

# Show current checklist
cmd_show() {
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_warning "No active checklist. Create one with 'checklist create <template>'"
        return
    fi
    
    local name=$(jq -r '.name' "$active_file")
    local total=$(jq -r '.items | length' "$active_file")
    local completed=$(jq -r '[.items[] | select(.status == "done")] | length' "$active_file")
    
    echo ""
    echo "📋 Checklist: $name"
    echo "Progress: ${completed}/${total}"
    echo ""
    
    local progress=$((completed * 100 / total))
    local bars=$((progress / 5))
    printf "["
    printf "%${bars}s" | tr ' ' '█'
    printf "%$((20 - bars))s" | tr ' ' '─'
    printf "] %d%%\n" "$progress"
    echo ""
    
    local idx=1
    jq -r '.items[] | "\(.status)\t\(.id)\t\(.text)\t\(.reason // "")"' "$active_file" | while read -r status id text reason; do
        case "$status" in
            done)
                echo "✅ $idx. $text";;
            skip)
                echo "⏭️  $idx. $text (reason: $reason)";;
            *)
                echo "⬜ $idx. $text";;
        esac
        ((idx++))
    done
}

# Mark item as done
cmd_done() {
    local item_num="$1"
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_error "No active checklist"
        return 1
    fi
    
    # Update status using jq
    local temp=$(mktemp)
    jq --argjson num "$item_num" '(.items[] | select(.id == num)).status = "done"' "$active_file" > "$temp" && mv "$temp" "$active_file"
    
    print_success "Marked item $item_num as done"
    cmd_show
}

# Mark item as skipped
cmd_skip() {
    local item_num="$1"
    local reason="${2:-"Skipped"}"
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_error "No active checklist"
        return 1
    fi
    
    local temp=$(mktemp)
    jq --argjson num "$item_num" --arg reason "$reason" '(.items[] | select(.id == num)).status = "skip" | (.items[] | select(.id == num)).reason = reason' "$active_file" > "$temp" && mv "$temp" "$active_file"
    
    print_success "Skipped item $item_num: $reason"
    cmd_show
}

# Add custom item
cmd_add() {
    local text="$1"
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_error "No active checklist. Create one first."
        return 1
    fi
    
    local next_id=$(jq '[.items[].id] | max + 1' "$active_file")
    local temp=$(mktemp)
    jq --argjson id "$next_id" --arg text "$text" '.items += [{"id": id, "text": text, "status": "pending", "required": true}]' "$active_file" > "$temp" && mv "$temp" "$active_file"
    
    print_success "Added: $text"
    cmd_show
}

# Reset checklist
cmd_reset() {
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_error "No active checklist"
        return 1
    fi
    
    local temp=$(mktemp)
    jq '.items[] |= {"id": .id, "text": .text, "status": "pending", "required": .required, "reason": null}' "$active_file" > "$temp" && mv "$temp" "$active_file"
    
    print_success "Checklist reset"
    cmd_show
}

# Create checklist from template or custom
cmd_create() {
    local name="$1"
    
    if [[ -z "$name" ]]; then
        print_error "Template name required"
        echo "Usage: checklist create <template-name>"
        echo ""
        echo "Available templates:"
        cmd_templates
        return 1
    fi
    
    # Check if template exists
    local template_file="${TEMPLATES_DIR}/${name}.json"
    
    if [[ -f "$template_file" ]]; then
        cp "$template_file" "${ACTIVE_DIR}/current.json"
        print_success "Created checklist from template: $name"
    else
        # Create custom checklist
        cat > "${ACTIVE_DIR}/current.json" << EOF
{
  "name": "$name",
  "description": "Custom checklist",
  "items": []
}
EOF
        print_success "Created new checklist: $name"
    fi
    
    cmd_show
}

# Export checklist
cmd_export() {
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_error "No active checklist"
        return 1
    fi
    
    local name=$(jq -r '.name' "$active_file")
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local export_file="${CHECKLIST_DIR}/history/${name}_${timestamp}.json"
    
    mkdir -p "${CHECKLIST_DIR}/history"
    cp "$active_file" "$export_file"
    
    print_success "Exported to: $export_file"
}

# Usage
usage() {
    cat << EOF
Checklist - Task Checklist Manager (v1.0.0)

Usage: checklist <command> [options]

Commands:
    templates              List available templates
    create <name>         Create checklist from template or new
    show                  Show current checklist
    done <num>            Mark item as done
    skip <num> <reason>   Skip item with reason
    add "<text>"          Add custom item
    reset                 Reset all items to pending
    export                Export checklist to history

Examples:
    checklist templates
    checklist create deploy
    checklist show
    checklist done 3
    checklist add "Verify output"
    checklist export

EOF
    exit 1
}

# Main
case "$1" in
    templates)
        cmd_templates
        ;;
    create)
        cmd_create "$2"
        ;;
    show)
        cmd_show
        ;;
    done)
        cmd_done "$2"
        ;;
    skip)
        cmd_skip "$2" "$3"
        ;;
    add)
        cmd_add "$2"
        ;;
    reset)
        cmd_reset
        ;;
    export)
        cmd_export
        ;;
    help|--help|-h|"")
        usage
        ;;
    *)
        print_error "Unknown command: $1"
        usage
        ;;
esac
