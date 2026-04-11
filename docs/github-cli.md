# GitHub CLI (`gh`) 完全指南

> 版本：2.88.1 | 官方文档：https://cli.github.com/manual

GitHub CLI 是 GitHub 官方的命令行工具，让你直接在终端中与 GitHub 交互，无需切换到浏览器。

## 目录

- [安装](#安装)
- [认证 (auth)](#认证-auth)
- [仓库 (repo)](#仓库-repo)
- [Issue (issue)](#issue-issue)
- [Pull Request (pr)](#pull-request-pr)
- [Release (release)](#release-release)
- [GitHub Actions](#github-actions)
- [搜索 (search)](#搜索-search)
- [API 调用 (api)]#api-调用-api)
- [Secrets & Variables](#secrets--variables)
- [组织 (org)](#组织-org)
- [Gist (gist)](#gist-gist)
- [标签 (label)](#标签-label)
- [Projects (project)](#projects-project)
- [Codespace (codespace)](#codespace-codespace)
- [扩展 (extension)](#扩展-extension)
- [别名 (alias)](#别名-alias)
- [配置 (config)](#配置-config)
- [其他命令](#其他命令)
- [通用技巧](#通用技巧)

---

## 安装

```bash
# macOS (Homebrew)
brew install gh

# Ubuntu/Debian
sudo apt install gh
# 或使用官方安装脚本
(type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
  && sudo mkdir -p -m 755 /etc/apt/keyrings \
  && out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  && cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
  && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
  && sudo apt update \
  && sudo apt install gh -y

# Windows (winget)
winget install --id GitHub.cli

# 验证安装
gh --version
```

---

## 认证 (auth)

```bash
# 登录 GitHub（交互式引导）
gh auth login

# 登录指定主机（如 GitHub Enterprise）
gh auth login --hostname github.example.com

# 使用 token 登录
gh auth login --with-token < mytoken.txt

# 查看当前认证状态
gh auth status

# 刷新认证凭据
gh auth refresh

# 刷新并添加额外权限 scope
gh auth refresh -s project,read:org

# 切换账户
gh auth switch

# 获取当前 token
gh auth token

# 登出
gh auth logout

# 配置 git 使用 gh 认证
gh auth setup-git
```

---

## 仓库 (repo)

```bash
# 查看当前仓库信息
gh repo view

# 在浏览器中打开仓库
gh repo view --web

# 克隆仓库
gh repo clone owner/repo
gh repo clone owner/repo my-folder

# 创建新仓库（当前目录）
gh repo create

# 创建新仓库并指定名称
gh repo create my-project --public
gh repo create my-project --private

# 创建仓库并关联已有目录
gh repo create my-project --public --source=. --remote=origin --push

# 列出仓库
gh repo list                          # 当前用户的仓库
gh repo list --limit 10              # 限制数量
gh repo list org-name                # 某组织的仓库

# Fork 仓库
gh repo fork owner/repo
gh repo fork owner/repo --clone       # Fork 并克隆

# 删除仓库（需要确认）
gh repo delete owner/repo

# 重命名仓库
gh repo rename new-name

# 归档 / 取消归档仓库
gh repo archive owner/repo
gh repo unarchive owner/repo

# 编辑仓库设置
gh repo edit --description "新描述"
gh repo edit --enable-issues=false
gh repo edit --visibility private

# 同步 fork 仓库
gh repo sync

# 设置当前目录的默认仓库
gh repo set-default owner/repo

# 查看 gitignore 模板
gh repo gitignore
gh repo gitignore Python

# 查看可用的 license
gh repo license
```

**repo 参数格式：**

| 格式 | 示例 |
|------|------|
| `OWNER/REPO` | `cli/cli` |
| 完整 URL | `https://github.com/OWNER/REPO` |

---

## Issue (issue)

```bash
# 列出 issue
gh issue list                        # 默认打开状态的 issue
gh issue list --state all            # 所有状态
gh issue list --label bug            # 按标签筛选
gh issue list --author username      # 按作者筛选
gh issue list --assignee username    # 按指派人筛选
gh issue list --limit 20             # 限制数量
gh issue list --search "关键词"       # 搜索

# 查看 issue 状态概览
gh issue status

# 创建 issue（交互式）
gh issue create

# 创建 issue（非交互式）
gh issue create --title "标题" --body "描述内容"
gh issue create --title "Bug" --label "bug,help wanted" --assignee username

# 从文件读取 body
gh issue create --title "标题" --body-file ./issue_body.md

# 查看 issue
gh issue view 123
gh issue view 123 --web              # 在浏览器中打开

# 查看 issue 评论
gh issue view 123 --comments

# 关闭 issue
gh issue close 123
gh issue close 123 --comment "已修复" --reason "completed"

# 重新打开 issue
gh issue reopen 123

# 添加评论
gh issue comment 123 --body "评论内容"

# 编辑 issue
gh issue edit 123 --title "新标题" --body "新描述"
gh issue edit 123 --add-label "bug" --remove-label "question"

# 锁定 / 解锁讨论
gh issue lock 123
gh issue unlock 123

# 置顶 / 取消置顶
gh issue pin 123
gh issue unpin 123

# 转移 issue 到其他仓库
gh issue transfer 123 owner/other-repo

# 管理 issue 关联的分支
gh issue develop 123
```

**issue 参数格式：**

| 格式 | 示例 |
|------|------|
| 数字 | `123` |
| URL | `https://github.com/OWNER/REPO/issues/123` |

**通用 `-R` 标志：** 指定其他仓库 `gh issue list -R owner/repo`

---

## Pull Request (pr)

```bash
# 列出 PR
gh pr list                           # 默认打开状态的 PR
gh pr list --state all               # 所有状态
gh pr list --author username         # 按作者筛选
gh pr list --reviewer username       # 按审查者筛选
gh pr list --label "enhancement"     # 按标签筛选
gh pr list --base main               # 按目标分支筛选
gh pr list --head feature-branch     # 按源分支筛选
gh pr list --search "关键词"          # 搜索

# 查看 PR 状态概览
gh pr status

# 创建 PR（交互式）
gh pr create

# 创建 PR（自动填充 commit 信息）
gh pr create --fill

# 创建 PR（非交互式）
gh pr create --title "标题" --body "描述"
gh pr create --title "标题" --body "描述" --base main --head feature
gh pr create --title "标题" --label "enhancement" --reviewer username

# 从文件读取 body
gh pr create --title "标题" --body-file ./pr_body.md

# 查看 PR
gh pr view 321
gh pr view 321 --web                 # 在浏览器中打开

# 查看 PR diff
gh pr diff 321

# 查看 PR CI 状态
gh pr checks 321

# 检出 PR 到本地
gh pr checkout 321

# 合并 PR
gh pr merge 321                      # 交互式选择合并方式
gh pr merge 321 --merge              # Merge commit
gh pr merge 321 --squash             # Squash and merge
gh pr merge 321 --rebase             # Rebase and merge
gh pr merge 321 --delete-branch      # 合并后删除分支

# 关闭 PR
gh pr close 321

# 重新打开 PR
gh pr reopen 321

# 标记 PR 为 ready for review
gh pr ready 321

# 更新 PR 分支（从 base 更新）
gh pr update-branch 321

# 添加评论
gh pr comment 321 --body "评论内容"

# 添加 review
gh pr review 321                     # 交互式
gh pr review 321 --approve           # 批准
gh pr review 321 --request-changes   # 请求修改
gh pr review 321 --comment --body "建议"

# 回退 PR
gh pr revert 321

# 锁定 / 解锁讨论
gh pr lock 321
gh pr unlock 321
```

**PR 参数格式：**

| 格式 | 示例 |
|------|------|
| 数字 | `321` |
| URL | `https://github.com/OWNER/REPO/pull/321` |
| 分支名 | `feature-branch` 或 `OWNER:feature-branch` |

---

## Release (release)

```bash
# 列出 release
gh release list
gh release list --limit 5

# 查看 release
gh release view v1.0.0
gh release view v1.0.0 --web

# 创建 release
gh release create v1.0.0
gh release create v1.0.0 --title "版本 1.0.0" --notes "发布说明"
gh release create v1.0.0 --notes-file CHANGELOG.md

# 创建 release 并上传资产
gh release create v1.0.0 ./dist/app.tar.gz

# 上传资产到已有 release
gh release upload v1.0.0 ./file1.txt ./file2.zip

# 下载 release 资产
gh release download v1.0.0
gh release download v1.0.0 --pattern "*.tar.gz"

# 删除 release
gh release delete v1.0.0

# 删除指定资产
gh release delete-asset v1.0.0 old-file.zip

# 编辑 release
gh release edit v1.0.0 --title "新标题" --notes "新说明"

# 验证 release（SLSA 来源证明）
gh release verify v1.0.0
gh release verify-asset v1.0.0 ./app.tar.gz
```

---

## GitHub Actions

### 工作流运行 (run)

```bash
# 列出最近的运行
gh run list
gh run list --limit 10
gh run list --workflow "CI"
gh run list --branch main

# 查看运行详情
gh run view 12345
gh run view 12345 --web
gh run view 12345 --log            # 查看日志
gh run view 12345 --log-failed    # 仅查看失败步骤的日志

# 实时监控运行
gh run watch 12345

# 重新运行
gh run rerun 12345
gh run rerun 12345 --failed       # 仅重新运行失败的 job

# 取消运行
gh run cancel 12345

# 下载运行产物
gh run download 12345
gh run download 12345 --name build-artifact

# 删除运行记录
gh run delete 12345
```

### 工作流 (workflow)

```bash
# 列出工作流
gh workflow list

# 查看工作流
gh workflow view "CI"
gh workflow view "CI" --web
gh workflow view "CI" --yaml       # 查看 YAML 定义

# 启用 / 禁用工作流
gh workflow enable "CI"
gh workflow disable "CI"

# 手动触发工作流 (需要 workflow_dispatch 事件)
gh workflow run "CI" --ref main
gh workflow run "Deploy" -f environment=production -f version=1.0.0
```

### 缓存 (cache)

```bash
# 列出缓存
gh cache list
gh cache list --limit 20

# 删除缓存
gh cache delete 123456789
gh cache delete --all               # 删除所有缓存
```

---

## 搜索 (search)

```bash
# 搜索仓库
gh search repos "react dashboard" --limit 10
gh search repos "react" --language JavaScript --stars ">1000"

# 搜索 issue
gh search issues "内存泄漏" --repo owner/repo
gh search issues "bug" --label bug --state open

# 搜索 PR
gh search prs "性能优化" --repo owner/repo

# 搜索代码
gh search code "console.log" --repo owner/repo

# 搜索 commit
gh search commits "fix typo" --repo owner/repo

# 排除标签（需要 -- 分隔符）
gh search issues -- "query -label:wontfix"

# 输出为 JSON
gh search repos "react" --json name,description,url --limit 5

# 使用 jq 过滤
gh search repos "react" --jq '.[].full_name' --limit 5
```

---

## API 调用 (api)

```bash
# GET 请求
gh api repos/{owner}/{repo}
gh api repos/{owner}/{repo}/issues

# POST 请求
gh api repos/{owner}/{repo}/issues -f title="标题" -f body="内容"

# PATCH 请求
gh api repos/{owner}/{repo} -X PATCH -f description="新描述"

# DELETE 请求
gh api repos/{owner}/{repo}/issues/123 -X DELETE

# GraphQL 查询
gh api graphql -f query='
  query($owner: String!, $name: String!) {
    repository(owner: $owner, name: $name) {
      issues(first: 10) {
        nodes { title, number }
      }
    }
  }' -F owner='{owner}' -F name='{repo}'

# 从文件读取请求体
gh api repos/{owner}/{repo}/rulesets --input file.json

# 使用 jq 过滤响应
gh api repos/{owner}/{repo}/issues --jq '.[].title'

# 分页获取所有结果
gh api repos/{owner}/{repo}/issues --paginate

# 自定义请求头
gh api -H 'Accept: application/vnd.github.v3.raw+json' repos/{owner}/{repo}/README.md

# 预览 API 功能
gh api --preview baptiste,nebula repos/{owner}/{repo}/releases

# 查看完整请求和响应
gh api repos/{owner}/{repo} --verbose

# 缓存响应
gh api repos/{owner}/{repo} --cache "1h"

# 占位符 {owner}, {repo}, {branch} 自动替换为当前仓库的值
```

**占位符：** `{owner}`、`{repo}`、`{branch}` 会自动替换为当前目录仓库的对应值。

---

## Secrets & Variables

```bash
# Secrets（加密值，用于 Actions）
gh secret list                          # 列出 secrets
gh secret set MY_SECRET                 # 交互式设置
gh secret set MY_SECRET --body "value"  # 直接设置
echo "value" | gh secret set MY_SECRET  # 通过管道设置
gh secret set MY_SECRET --repo owner/repo  # 指定仓库
gh secret set MY_SECRET --org my-org    # 组织级别
gh secret set MY_SECRET --env production # 环境级别
gh secret delete MY_SECRET              # 删除

# Variables（非加密值，用于 Actions）
gh variable list                        # 列出 variables
gh variable set MY_VAR --body "value"   # 设置
gh variable get MY_VAR                  # 获取
gh variable delete MY_VAR               # 删除
```

---

## 组织 (org)

```bash
# 列出所属组织
gh org list
gh org list --limit 50
```

---

## Gist (gist)

```bash
# 列出 gist
gh gist list

# 创建 gist
gh gist create file.py                  # 从文件创建
echo "hello" | gh gist create          # 从 stdin 创建
gh gist create --public file.py         # 公开 gist

# 查看 gist
gh gist view gist-id
gh gist view gist-id --web

# 克隆 gist
gh gist clone gist-id

# 编辑 gist
gh gist edit gist-id --filename "new-name.py"

# 重命名 gist 中的文件
gh gist rename gist-id old-name.py new-name.py

# 删除 gist
gh gist delete gist-id
```

---

## 标签 (label)

```bash
# 列出标签
gh label list

# 创建标签
gh label create "bug" --color "d73a4a" --description "Bug 报告"

# 编辑标签
gh label edit "bug" --color "ff0000" --name "critical-bug"

# 删除标签
gh label delete "bug"

# 从其他仓库克隆标签
gh label clone owner/source-repo
```

---

## Projects (project)

> 最低需要 `project` scope：`gh auth refresh -s project`

```bash
# 列出项目
gh project list --owner owner-name

# 创建项目
gh project create --owner monalisa --title "Roadmap"

# 查看项目
gh project view 1 --owner cli
gh project view 1 --owner cli --web

# 管理字段
gh project field-list 1 --owner cli
gh project field-create 1 --owner cli --name "Status" --datatype "single_select"

# 管理项目条目
gh project item-list 1 --owner cli
gh project item-add 1 --owner cli --url https://github.com/owner/repo/issues/1
gh project item-create 1 --owner cli --title "Draft issue" --body "Description"

# 编辑 / 删除项目条目
gh project item-edit 1 --id item-id --field-id field-id --single-select-option-id option-id
gh project item-delete 1 --owner cli --id item-id
gh project item-archive 1 --owner cli --id item-id

# 其他操作
gh project close 1 --owner cli
gh project edit 1 --owner cli --title "New Title"
gh project delete 1 --owner cli
gh project copy 1 --owner cli --target-owner new-owner
gh project mark-template 1 --owner cli
gh project link 1 --owner cli --repository owner/repo
gh project unlink 1 --owner cli --repository owner/repo
```

---

## Codespace (codespace)

```bash
# 列出 codespace
gh codespace list
# 别名: gh cs list

# 创建 codespace
gh codespace create

# 用 VS Code 打开
gh codespace code

# SSH 连接
gh codespace ssh

# 查看 codespace 详情
gh codespace view

# 查看 logs
gh codespace logs

# 管理端口
gh codespace ports

# 复制文件
gh codespace cp local-file codespace:/path/

# 停止 codespace
gh codespace stop

# 删除 codespace
gh codespace delete

# 重建 codespace
gh codespace rebuild

# 用 JupyterLab 打开
gh codespace jupyter
```

---

## 扩展 (extension)

GitHub CLI 扩展是第三方仓库，提供额外的 `gh` 命令。

```bash
# 搜索扩展
gh extension search "keyword"

# 安装扩展
gh extension install owner/gh-extension-name

# 列出已安装扩展
gh extension list

# 升级扩展
gh extension upgrade
gh extension upgrade extension-name

# 移除扩展
gh extension remove extension-name

# 浏览扩展（交互式 UI）
gh extension browse

# 创建新扩展
gh extension create my-extension

# 直接执行扩展
gh extension exec my-extension-name
```

扩展仓库命名规则：仓库名必须以 `gh-` 开头，且包含同名可执行文件。

---

## 别名 (alias)

```bash
# 创建别名
gh alias set prc 'pr create'
gh alias set il 'issue list --label'
gh alias set co 'pr checkout'

# 列出别名
gh alias list

# 从 YAML 文件导入别名
gh alias import aliases.yml

# 删除别名
gh alias delete prc

# 示例：设置复杂别名（查看 issue 数量）
gh alias set issue-count 'issue list --state all --json number --jq length'
```

---

## 配置 (config)

```bash
# 查看所有配置
gh config list

# 获取指定配置
gh config get git_protocol
gh config get editor

# 设置配置
gh config set git_protocol ssh
gh config set editor "vim"
gh config set prompt enabled
gh config set pager "less -R"

# 可用配置项
# git_protocol   - git 操作使用的协议 {https | ssh}，默认 https
# editor         - 文本编辑器
# prompt         - 是否启用交互式提示 {enabled | disabled}，默认 enabled
# pager          - 终端分页器
# browser        - 默认浏览器
# color_labels   - 是否用 RGB 颜色显示标签 {enabled | disabled}
# spinner        - 是否显示加载动画 {enabled | disabled}，默认 enabled

# 清除缓存
gh config clear-cache
```

---

## 其他命令

```bash
# 在浏览器中打开（仓库/issue/PR）
gh browse
gh browse --settings            # 打开仓库设置
gh browse 123                   # 打开 issue/PR #123

# 查看 token 相关的许可证信息
gh licenses

# 生成 shell 补全脚本
gh completion -s bash > ~/.bash_completion.d/gh
gh completion -s zsh > ~/.zsh/completions/_gh

# 查看相关信息
gh status                        # 查看相关的 issue/PR/通知
```

---

## 通用技巧

### 环境变量

```bash
# 设置 token（优先级从高到低）
GH_TOKEN=xxx gh api repos/{owner}/{repo}
GITHUB_TOKEN=xxx gh api repos/{owner}/{repo}

# GitHub Enterprise
GH_ENTERPRISE_TOKEN=xxx
GH_HOST=github.example.com
```

### 指定仓库的 `-R` 标志

几乎所有需要仓库上下文的命令都支持 `-R`：

```bash
gh issue list -R owner/repo
gh pr create -R owner/repo
gh run list -R owner/repo
```

### JSON 输出

```bash
# 输出 JSON
gh repo view --json name,description,url

# jq 过滤
gh pr list --json number,title,author --jq '.[] | "\(.number)\t\(.title)"'

# Go template
gh issue list --json number,title --template '{{range .}}{{.number}}: {{.title}}{{"\n"}}{{end}}'
```

### 管道和脚本

```bash
# 获取所有 issue 标题
gh issue list --json title --jq '.[].title'

# 获取仓库 stars 数
gh repo view --json stargazerCount --jq '.stargazerCount'

# 批量操作：关闭所有标记为 wontfix 的 issue
gh issue list --label wontfix --json number --jq '.[].number' | xargs -I {} gh issue close {}
```
