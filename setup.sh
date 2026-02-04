#!/bin/bash

PROMPT_DIR=~/workspace/prompt-archive
TARGET_DIR=~/.claude

ln -sfn $PROMPT_DIR/TECH_SPEC.md $TARGET_DIR/TECH_SPEC.md
ln -sfn $PROMPT_DIR/LLM.md $TARGET_DIR/CLAUDE.md
ln -sfn $PROMPT_DIR/finish-work.md $TARGET_DIR/commands/finish-work.md
ln -sfn $PROMPT_DIR/.agent/workflows/workflow_maker.md $TARGET_DIR/agents/workflow_maker.md
ln -sfn $PROMPT_DIR/.agent/workflows/planner.md $TARGET_DIR/agents/planner.md
ln -sfn $PROMPT_DIR/.agent/workflows/developer.md $TARGET_DIR/agents/developer.md
ln -sfn $PROMPT_DIR/.agent/workflows/marketer.md $TARGET_DIR/agents/marketer.md
ln -sfn $PROMPT_DIR/.agent/workflows/operator.md $TARGET_DIR/agents/operator.md

ln -sfn $PROMPT_DIR/KOP.md $TARGET_DIR/KOP.md
ln -sfn $PROMPT_DIR/daily_work_feedback_system_prompt $TARGET_DIR/commands/daily_work_feedback_system_prompt