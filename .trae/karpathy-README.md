# Andrej Karpathy 编码指南 - Trae 版本

本目录包含适配Trae IDE的Andrej Karpathy编码指南，可以直接复制到任何Trae项目中使用。

## 📦 包含文件

```
.trae/
├── rules/
│   └── karpathy-guidelines.md      # 全局编码规范（始终生效）
└── skills/
    └── karpathy-guidelines/
        └── SKILL.md                # 可调用的技能（按需激活）
```

## 🚀 如何复制到其他项目

### 方式一：完整复制（推荐）

在新项目根目录下执行：

```powershell
# 1. 创建目录结构
New-Item -ItemType Directory -Force -Path ".trae\rules"
New-Item -ItemType Directory -Force -Path ".trae\skills\karpathy-guidelines"

# 2. 复制规则文件
Copy-Item "path\to\your\current\project\.trae\rules\karpathy-guidelines.md" ".trae\rules\"

# 3. 复制技能文件
Copy-Item "path\to\your\current\project\.trae\skills\karpathy-guidelines\SKILL.md" ".trae\skills\karpathy-guidelines\"
```

### 方式二：手动创建

1. 在新项目的 `.trae/rules/` 目录下创建 `karpathy-guidelines.md`
2. 在新项目的 `.trae/skills/karpathy-guidelines/` 目录下创建 `SKILL.md`
3. 将这两个文件的内容复制过去即可

## 💡 使用方式

### 作为全局规则（自动生效）

规则文件 `.trae/rules/karpathy-guidelines.md` 会自动被Trae读取，所有编码操作都会遵循这些准则。

### 作为技能调用（按需激活）

你可以通过调用 `karpathy-guidelines` 技能来特别强调使用这些准则，适用于：
- 重要的代码重构
- 复杂功能的实现
- 代码审查场景

## 📋 四大核心原则

1. **编码前思考** - 不要假设，不要隐藏困惑，要呈现权衡
2. **简洁优先** - 用最少的代码解决问题，不做投机性的事
3. **精准修改** - 只碰必须碰的，只清理自己造成的混乱
4. **目标驱动执行** - 定义成功标准，循环直到验证通过

## 🔗 原始来源

- GitHub仓库: https://github.com/multica-ai/andrej-karpathy-skills
- 灵感来源: Andrej Karpathy 的推文

## 📝 版本

- 原始版本: Andrej Karpathy
- Trae适配版本: 2024
