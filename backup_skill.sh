#!/bin/bash
# Skill 备份脚本

SKILL_NAME="feishu-doc-copier"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="${SKILL_NAME}_${TIMESTAMP}"

echo "开始备份 ${SKILL_NAME}..."

# 创建备份目录
mkdir -p ${BACKUP_DIR}

# 备份 Skill 目录
tar -czf "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" ${SKILL_NAME}/

# 备份 .skill 文件（如果存在）
if [ -f "${SKILL_NAME}.skill" ]; then
    cp "${SKILL_NAME}.skill" "${BACKUP_DIR}/${BACKUP_NAME}.skill"
    echo "✓ 已备份 .skill 文件"
fi

echo "✓ 备份完成: ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
echo ""
echo "备份内容:"
ls -lh ${BACKUP_DIR}/${BACKUP_NAME}*
