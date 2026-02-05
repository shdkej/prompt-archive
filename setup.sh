#!/bin/bash

PROMPT_DIR=~/workspace/prompt-archive
TARGET_DIR=~/.claude

ln -sfn $PROMPT_DIR/LLM.md $TARGET_DIR/CLAUDE.md
ln -sfn $PROMPT_DIR/BRAND.md $TARGET_DIR/BRAND.md
ln -sfn $PROMPT_DIR/TECH_SPEC.md $TARGET_DIR/TECH_SPEC.md
ln -sfn $PROMPT_DIR/.agent/workflows/workflow-master.md $TARGET_DIR/agents/workflow-master.md
ln -sfn $PROMPT_DIR/.agent/workflows/planner.md $TARGET_DIR/agents/planner.md
ln -sfn $PROMPT_DIR/.agent/workflows/developer.md $TARGET_DIR/agents/developer.md
ln -sfn $PROMPT_DIR/.agent/workflows/marketer.md $TARGET_DIR/agents/marketer.md
ln -sfn $PROMPT_DIR/.agent/workflows/operator.md $TARGET_DIR/agents/operator.md

ln -sfn $PROMPT_DIR/KOP.md $TARGET_DIR/KOP.md

ln -sfn $PROMPT_DIR/TDD.md $TARGET_DIR/TDD.md

# Skills
mkdir -p $TARGET_DIR/skills/daily-feedback-system
ln -sfn $PROMPT_DIR/DAILY-FEEDBACK-SYSTEM.md $TARGET_DIR/skills/daily-feedback-system/skill.md

mkdir -p $TARGET_DIR/skills/omc
ln -sfn $PROMPT_DIR/OMC.md $TARGET_DIR/skills/omc/skill.md