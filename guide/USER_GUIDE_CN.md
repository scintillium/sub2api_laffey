# Laffey API 使用文档

> 适用对象：第一次使用中转站、Codex、Claude Code、CC Switch 的用户。  
> 文档目标：照着做即可，不展开复杂原理。

## 目录

- [Laffey API 使用文档](#laffey-api-使用文档)
  - [目录](#目录)
  - [计费模式](#计费模式)
    - [额度来源](#额度来源)
    - [用量在哪里看](#用量在哪里看)
  - [开始前先准备](#开始前先准备)
    - [登录、充值和创建 API Key](#登录充值和创建-api-key)
  - [安装 CC Switch](#安装-cc-switch)
  - [Codex 配置](#codex-配置)
    - [用 CC Switch 配置 API 信息【强烈推荐】](#用-cc-switch-配置-api-信息强烈推荐)
    - [安装 Codex App / Codex CLI](#安装-codex-app--codex-cli)
      - [Codex App 和 Codex CLI 的区别](#codex-app-和-codex-cli-的区别)
    - [Codex App 安装与使用](#codex-app-安装与使用)
      - [1. 安装](#1-安装)
      - [2. 使用：让 Codex App 写一个 Hello World](#2-使用让-codex-app-写一个-hello-world)
    - [Codex CLI 安装与使用](#codex-cli-安装与使用)
      - [1. 不同系统下的安装](#1-不同系统下的安装)
        - [Windows 安装](#windows-安装)
        - [macOS 安装方式一：Homebrew](#macos-安装方式一homebrew)
        - [macOS 安装方式二：Node.js / npm](#macos-安装方式二nodejs--npm)
      - [2. 使用：让 Codex CLI 写一个 Hello World](#2-使用让-codex-cli-写一个-hello-world)
  - [配置 Claude](#配置-claude)
    - [用 CC Switch 配置 Claude 信息【推荐】](#用-cc-switch-配置-claude-信息推荐)
    - [安装 Claude Code](#安装-claude-code)
      - [Windows 安装](#windows-安装-1)
      - [macOS 安装](#macos-安装)
    - [使用：让 Claude Code 写一个 Hello World](#使用让-claude-code-写一个-hello-world)
  - [常见问题](#常见问题)
    - [CC Switch 导入失败](#cc-switch-导入失败)
    - [Codex CLI 不能用](#codex-cli-不能用)
    - [Claude Code 不能用](#claude-code-不能用)
    - [API Key 泄露了怎么办](#api-key-泄露了怎么办)
    - [换服务商或换分组怎么做](#换服务商或换分组怎么做)

## 计费模式

本站的用法可以理解为：你不用把真实账号直接配置到每个工具里，只需要使用 Laffey API 发给你的中转地址和 API Key。实际请求产生的费用会从你的站内额度中扣除。

本站的站内额度以 **美元额度（USD）** 显示和扣减，但充值入口使用人民币金额。当前换算规则为：

```text
1 RMB 充值 = 1 USD 站内额度
```

例如充值 10 RMB，到账后会获得 10 USD 站内额度。后续使用 Codex、Claude Code 或其他兼容客户端时，系统会按照模型用量、分组倍率和计费规则从该额度中扣除。

### 额度来源

| 来源 | 说明 | 到账形式 |
|---|---|---|
| 在线充值 | 通过站内充值入口支付人民币 | 按 1 RMB = 1 USD 换算为站内美元额度 |
| 优惠券 | 活动、补偿或人工发放的优惠 | 折算为站内美元额度 |
| 兑换码 | 输入管理员发放的兑换码 | 可兑换为站内美元额度，也可能包含并发或订阅权限 |
| 管理员赠送 | 管理员直接为账号增加余额或额度 | 按站内美元额度显示 |

### 用量在哪里看

1. 登录 Laffey API, 进入 **仪表盘**。
2. 查看模型、时间、Token、费用、状态。
3. 如果某次请求失败，先看错误信息，再看余额和分组是否正确。

## 开始前先准备

### 登录、充值和创建 API Key

1. 进入 **充值/订阅**，完成充值，或确认你的订阅还有可用额度。
2. 进入左侧 **我的账户**，点击 **API 密钥**，接着点击 **创建密钥**。

   ![创建 API 密钥按钮](images/user-guide/api-key-create-button.png)

3. 名称填写，例如：

   - `Codex 日常使用`
   - `Claude Code 编程`

4. 重点是选择对应分组：

   - 用 Chatgpt/Codex：选 OpenAI 分组。
   - 用 Claude Code：选 Claude / Anthropic 分组。

   ![选择 API 密钥分组](images/user-guide/api-key-select-group.png)

5. 点击创建后，获得一个 `sk-...` 密钥。

   ![复制创建后的 API 密钥](images/user-guide/api-key-copy-created.png)

> API Key 可以任意创建，任意复制，随时可以回来取

## 安装 CC Switch

CC Switch 用来保存多个服务商配置，并在 Codex / Claude 等 agent 之间切换。强烈建议先安装它，后面配置 Codex CLI 和 Claude Code 会更省事。

下载链接：[CC Switch 官网](https://ccswitch.ai/) / [GitHub Releases](https://github.com/farion1231/cc-switch/releases) / [国内网盘下载](https://1drv.ms/f/c/90f4cc5b88f514bf/IgCZ3hpZwYeaSb4WyYu414XJAS2-aNUItNCwhHlJWAsCZJI?e=Zhrieb)

## Codex 配置

Codex 可以通过官方 App 使用，也可以通过 Codex CLI 在终端里使用。Laffey API 同时支持这两种方式，先用 CC Switch 导入一次供应商配置，后面在 Codex App 或 Codex CLI 中切换到这个供应商即可。

### 用 CC Switch 配置 API 信息【强烈推荐】

这一节的目标是：把你刚才创建的 Laffey API Key 导入到 CC Switch，让 CC Switch 帮你管理 Codex 的服务商配置。

1. 第一步 在左侧菜单进入 **我的账户 → API 密钥**。找到要给 Codex 使用的那条 API Key，点击右侧的 **导入到 CCS**。

   ![导入 API 密钥到 CC Switch](images/user-guide/codex-import-to-ccs.png)

2. 浏览器弹出“是否允许打开 CC Switch”或类似提示时，选择 **允许**。

   如果浏览器没有弹窗，或者点击后没有反应，先确认 CC Switch 已经安装并打开过一次。浏览器需要能识别 `ccswitch://` 这种外部应用链接。

   ![浏览器打开 CC Switch 确认弹窗](images/user-guide/browser-open-ccswitch.png)

3. CC Switch 打开后，点击上方模型图标，启动导入的供应商配置。切换完成后，Codex App 和 Codex CLI 都可以使用这个中转配置。

   ![CC Switch 中的 Laffey API 供应商配置](images/user-guide/ccswitch-codex-provider.png)

### 安装 Codex App / Codex CLI

> 注意：使用 Laffey API 中转时，请在 Codex App 或 Codex CLI 中选择刚才通过 CC Switch 导入的 Laffey API 供应商。

#### Codex App 和 Codex CLI 的区别

| 对比项 | Codex App | Codex CLI |
|---|---|---|
| 使用方式 | 图形界面操作 | 终端输入命令 |
| 适合场景 | 看任务、审查代码、用图形界面管理任务 | 在项目目录中让 Codex 直接读写文件、运行测试 |
| 排错难度 | 界面友好，但底层配置不一定可见 | 配置文件清晰，适合排查 Base URL / Key 问题 |

### Codex App 安装与使用

#### 1. 安装

Codex App 建议直接下载安装包。普通用户不需要打开命令行，也不需要手动安装 Node.js。

| 下载方式 | 链接 | 说明 |
|---|---|---|
| 官网下载 | [OpenAI Codex 官网](https://openai.com/codex/) | 进入页面后点击 Download 下载 |
| 微软商店下载 | [Microsoft Store](https://apps.microsoft.com/) | Windows 用户可在微软商店搜索 Codex |
| 苹果商店下载 | [Mac App Store](https://www.apple.com/app-store/) | macOS 用户可在苹果商店搜索 Codex |


#### 2. 使用：让 Codex App 写一个 Hello World

下面只做一个最小示例：让 Codex App 在空文件夹里写一个 `hello.py`。


1. 打开 Codex App，确认当前供应商已经切换到 Laffey API / Codex。

2. 新建一个空文件夹，例如：

   ```text
   helloworld
   ```

   然后在 Codex App 添加项目添加这个文件夹。

1. 在 Codex App 输入框附近找到模式选择，把模式切换为 **Plan / 计划**。这个模式会先让 Codex 给出方案，不会立刻改文件。
![1778638297751](images/user-guide/1778638297751.png)

2. 切换到计划模式后，在输入框里输入：

   ```text
   请为当前文件夹里的 Python Hello World 示例制定一个简短计划。
   目标：
   1. 新建 helloworld.py
   2. 内容输出 Hello, world!
   3. 新建 README.md，说明如何运行
   ```
   然后codex会返回一个执行计划文本
   ![1778638685244](images/user-guide/1778638685244.png)

3. 先阅读 Codex 给出的计划。

   如果计划不符合预期，可以继续和对话框选择否，和codex对话修改需求。
   如果计划合适，选择实施计划。 这里我选择“是，实施此计划”

4. Codex 这时候会自动切出plan模式来创建代码。
   可以看到 Codex 生成了一个 `helloworld.py`文件
   ![1778638983847](images/user-guide/1778638983847.png)

5. 这是我们要求 Codex 直接运行代码，展示结果

   ![Codex 运行 Hello World 结果](images/user-guide/codex-app-run-result.png)

   可以看到，程序正常输出，大功告成！

6. 如果后续新增或更换了 API Key，回到 Laffey API 的 **API 密钥** 页面重新点击 **导入到 CCS**，然后在 Codex App 中切换到新的 Laffey API 供应商。

### Codex CLI 安装与使用

#### 1. 不同系统下的安装

Codex CLI 需要先安装 Node.js 和 npm，或者在 macOS 上使用 Homebrew 直接安装。

##### Windows 安装

1. 进入官网下载并安装 Node.js：[Node.js 官网](https://nodejs.org/)。

2. 安装完成后，打开 PowerShell。

   点击 Windows 开始菜单，搜索 `PowerShell`，打开 **Windows PowerShell**。

   ![打开 Windows PowerShell](images/user-guide/windows-open-powershell.png)

3. 检查 Node.js 和 npm 是否安装成功。

   在 PowerShell 中输入下面两行命令，每输入一行按一次回车：

   ```powershell
   node -v
   npm -v
   ```

   如果两行都显示版本号，例如 `v22.x.x` 和 `10.x.x`，说明安装成功。如果提示找不到命令，关闭 PowerShell 后重新打开再试一次。

   ![检查 Node.js 和 npm 版本](images/user-guide/windows-node-npm-check.png)

4. 安装 Codex CLI。

   继续在 PowerShell 中输入：

   ```powershell
   npm install -g @openai/codex --registry=https://registry.npmmirror.com
   ```

   这一步可能需要等待几十秒到几分钟。等命令执行结束，重新出现可以输入命令的提示符后，再继续下一步。

5. 检查 Codex CLI 是否安装成功。

   ```powershell
   codex --version
   ```

   如果能显示版本号，说明 Codex CLI 安装成功。

   ![检查 Codex CLI 版本](images/user-guide/codex-cli-version-check.png)

##### macOS 安装方式一：Homebrew

1. 如果没有安装 `homebrew`，请查看安装方式二。

   打开终端，执行：

   ```bash
   brew install --cask codex
   ```

2. 检查 Codex CLI 是否安装成功：

   ```bash
   codex --version
   ```

##### macOS 安装方式二：Node.js / npm

1. 下载并安装 Node.js：[Node.js 官网](https://nodejs.org/)。

2. 打开终端，执行：

   ```bash
   npm install -g @openai/codex
   ```

3. 检查 Codex CLI 是否安装成功：

   ```bash
   codex --version
   ```

#### 2. 使用：让 Codex CLI 写一个 Hello World

Codex CLI 的使用方式是：在终端进入项目目录，运行 `codex`，然后把任务交给它。

![Codex CLI 界面示例](images/user-guide/codex-cli-preview.png)

1. 打开 CC Switch，确认当前供应商是刚才导入的 Laffey API / Codex 供应商。

   如果你改过供应商，建议关闭旧的终端窗口，重新打开一个新终端，再继续执行下面的命令。

2. 创建一个测试目录并进入：

   Windows PowerShell：

   ```powershell
   mkdir hello-codex
   cd hello-codex
   ```

   macOS / Linux 终端：

   ```bash
   mkdir hello-codex
   cd hello-codex
   ```

3. 启动 Codex CLI：

   ```bash
   codex
   ```

4. 在 Codex CLI 里先使用计划模式。部分版本会在启动后提供模式选择，可以先选择 **Plan / 计划**；如果没有看到模式选择，就直接输入下面的任务，让 Codex 只给计划、不要马上改文件：

   ```text
   请先使用计划模式，为当前目录里的 Python Hello World 示例制定一个简短计划。
   暂时不要修改文件。
   目标：
   1. 新建 hello.py
   2. 内容输出 Hello, Laffey API!
   3. 新建 README.md，说明运行命令
   ```

   如果 Codex 能正常给出计划，说明 Codex CLI 已经能通过 Laffey API 工作。

5. 阅读计划，确认它只会创建 `hello.py` 和 `README.md` 后，再让 Codex 执行。如果 CLI 有模式选择，可以切回 **Code / 执行**；然后在 Codex CLI 里回复：

   ```text
   计划没问题，请按这个计划执行。
   ```

6. 按 Codex CLI 的提示查看并接受修改。完成后目录里应当至少有：

   ```text
   hello.py
   README.md
   ```

   `hello.py` 预期内容类似：

   ```python
   print("Hello, Laffey API!")
   ```

7. 退出 Codex CLI 后运行：

   Windows PowerShell：

   ```powershell
   python hello.py
   ```

   macOS / Linux 终端：

   ```bash
   python3 hello.py
   ```

   看到下面输出即表示成功：

   ```text
   Hello, Laffey API!
   ```

8. 常用命令：

   | 命令 | 用途 |
   |---|---|
   | `codex` | 正常启动，适合第一次使用 |
   | `codex app` | 启动 Codex App |
   | `codex --version` | 查看版本，确认是否安装成功 |
   | `npm install -g @openai/codex` | 重新安装或升级 npm 版本的 Codex CLI |

## 配置 Claude

Claude Code 是在终端里使用的编程 agent，适合让它阅读项目、修改代码、运行命令。Laffey API 支持 Claude / Anthropic 分组，使用前请先创建一个绑定 Claude / Anthropic 分组的 API Key。

### 用 CC Switch 配置 Claude 信息【推荐】

这一节的目标是：把 Claude Code 要用的 Laffey API Key 导入到 CC Switch，后续通过 CC Switch 切换 Claude 供应商。

1. 进入 **我的账户 → API 密钥**，创建或选择一个给 Claude Code 使用的 API Key。
2. 重点是分组要选择 Claude / Anthropic 相关分组。不要把 Claude Code 用的 Key 绑到 OpenAI / Codex 分组。
3. 点击 API Key 右侧的 **导入到 CCS**。如果浏览器弹出“是否允许打开 CC Switch”，选择 **允许**。
4. CC Switch 打开后，在 Claude / Anthropic 对应的标签页中启用刚导入的 Laffey API 供应商。
5. 切换完成后，关闭旧终端，重新打开一个新终端再启动 Claude Code。

### 安装 Claude Code

Claude Code 需要先安装 Node.js 18 或更新版本。

#### Windows 安装

1. 进入官网下载并安装 Node.js：[Node.js 官网](https://nodejs.org/)。

2. 安装完成后，打开 PowerShell。

   点击 Windows 开始菜单，搜索 `PowerShell`，打开 **Windows PowerShell**。

   ![打开 Windows PowerShell](images/user-guide/windows-open-powershell.png)

3. 检查 Node.js 和 npm 是否安装成功。

   在 PowerShell 中输入下面两行命令，每输入一行按一次回车：

   ```powershell
   node -v
   npm -v
   ```

   如果两行都显示版本号，例如 `v22.x.x` 和 `10.x.x`，说明安装成功。如果提示找不到命令，关闭 PowerShell 后重新打开再试一次。

   ![检查 Node.js 和 npm 版本](images/user-guide/windows-node-npm-check.png)

4. 安装 Claude Code。

   继续在 PowerShell 中输入：

   ```powershell
   npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com
   ```

   这一步使用国内 npm 镜像，可能需要等待几十秒到几分钟。等命令执行结束，重新出现可以输入命令的提示符后，再继续下一步。

5. 检查是否安装成功：

   ```powershell
   claude --version
   ```

#### macOS 安装

如果已经安装 Node.js 18 或更新版本，可以直接执行：

```bash
npm install -g @anthropic-ai/claude-code
```

检查是否安装成功：

```bash
claude --version
```

### 使用：让 Claude Code 写一个 Hello World

下面只做一个最小示例：让 Claude Code 在空文件夹里写一个 `hello.py`。

1. 打开 CC Switch，确认当前 Claude / Anthropic 供应商已经切换到 Laffey API。

2. 创建一个测试目录并进入：

   Windows PowerShell：

   ```powershell
   mkdir hello-claude
   cd hello-claude
   ```

   macOS 终端：

   ```bash
   mkdir hello-claude
   cd hello-claude
   ```

3. 启动 Claude Code：

   ```bash
   claude
   ```

4. 先进入计划模式。Claude Code 通常可以按 `Shift + Tab` 在不同模式之间切换，切到 **Plan Mode / 计划模式** 后再输入：

   ```text
   请先为当前目录里的 Python Hello World 示例制定一个简短计划。
   暂时不要修改文件。
   目标：
   1. 新建 hello.py
   2. 内容输出 Hello, Laffey API!
   3. 新建 README.md，说明运行命令
   ```

5. 阅读计划，确认它只会创建 `hello.py` 和 `README.md` 后，再按 `Shift + Tab` 切回可执行修改的模式，然后回复：

   ```text
   计划没问题，请按这个计划执行。
   ```

6. 按 Claude Code 的提示查看并接受修改。完成后目录里应当至少有：

   ```text
   hello.py
   README.md
   ```

   `hello.py` 预期内容类似：

   ```python
   print("Hello, Laffey API!")
   ```

7. 退出 Claude Code 后运行：

   Windows PowerShell：

   ```powershell
   python hello.py
   ```

   macOS 终端：

   ```bash
   python3 hello.py
   ```

   看到下面输出即表示成功：

   ```text
   Hello, Laffey API!
   ```

8. 常用命令：

   | 命令 | 用途 |
   |---|---|
   | `claude` | 正常启动 Claude Code |
   | `claude --version` | 查看版本，确认是否安装成功 |
   | `/login` | 在 Claude Code 内重新登录或切换账号 |
   | `npm install -g @anthropic-ai/claude-code` | 重新安装或升级 npm 版本的 Claude Code |

## 常见问题

### CC Switch 导入失败

按顺序检查：

1. 是否已经安装 CC Switch。
2. 是否打开过一次 CC Switch。
3. 浏览器是否拦截了 `ccswitch://` 链接。
4. Sub2API **设置 → 站点设置** 中是否隐藏了 CCS 导入按钮。
5. 当前 API Key 是否已经创建成功。

处理方式：

| 问题 | 处理 |
|---|---|
| 点击没反应 | 重新安装 CC Switch，并打开一次 |
| 浏览器弹窗被拦截 | 允许打开外部应用 |
| 提示未安装 | 检查 `ccswitch://` 协议是否注册 |
| 导入了但不能用 | 在 CC Switch 中确认已切到对应供应商 |

### Codex CLI 不能用

按顺序检查：

1. `codex --version` 是否能显示版本。
2. `~/.codex/config.toml` 或 `%userprofile%\.codex\config.toml` 是否存在。
3. `auth.json` 里是否是你的 Sub2API Key。
4. `base_url` 是否是 `https://当前站点域名`，不要多写 `/v1`。
5. API Key 是否绑定 Codex / OpenAI 分组。

### Claude Code 不能用

按顺序检查：

1. `claude --version` 是否能显示版本。
2. `ANTHROPIC_BASE_URL` 是否是 `https://当前站点域名`。
3. `ANTHROPIC_AUTH_TOKEN` 是否是 `sk-你的API密钥`。
4. API Key 是否绑定 Claude / Anthropic 分组。
5. 如果在 Plan Mode 卡住，按 `Shift + Tab` 手动切换模式，再继续输入。

### API Key 泄露了怎么办

1. 立刻登录 Sub2API。
2. 进入 **API 密钥**。
3. 禁用或删除泄露的 Key。
4. 创建新的 Key。
5. 更新 CC Switch、Codex CLI、Codex App、Claude Code 里的配置。

### 换服务商或换分组怎么做

推荐方式：

1. 在 Sub2API 创建新的 API Key。
2. 点击 **导入到 CCS**。
3. 在 CC Switch 里切换到新的供应商。
4. 重新打开 Codex CLI 或 Claude Code。

手动方式：

1. 修改配置文件里的 API Key。
2. 修改配置文件里的中转站地址。
3. 关闭并重新打开客户端。
