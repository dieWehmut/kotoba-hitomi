# Kotoba Hitomi

Kotoba Hitomi 是一个集成前后端的多语言 AI 辅助应用，支持 Web 和 Android 平台。前端基于 Vue 3 + Vite，移动端采用 Capacitor，后端为 Python 服务。

## 目录结构

```
.
├── backend/                # Python 后端服务
│   ├── main.py             # 后端主程序入口
│   ├── generate_cert.py    # 证书生成脚本
│   ├── requirements.txt    # Python 依赖
│   └── package.json        # Node 相关依赖（如有）
├── kotobahitomi/           # 前端与移动端项目
│   ├── src/                # 前端源码（Vue 3）
│   ├── public/             # 静态资源
│   ├── android/            # Android 项目（Capacitor 集成）
│   ├── package.json        # 前端依赖
│   └── vite.config.js      # Vite 配置
└── README.md               # 项目说明文档
```

## 技术栈

- 前端：Vue 3, Vite, Capacitor, JavaScript/TypeScript
- 移动端：Android (Capacitor)
- 后端：Python 3
- 依赖管理：npm, pip

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/dieWehmut/kotoba-hitomi.git
cd kotoba-hitomi
```

### 2. 安装前端依赖

```bash
cd kotobahitomi
npm install
```

### 3. 启动前端开发服务器

```bash
npm run dev
```

### 4. 安装后端依赖

```bash
cd ../backend
pip install -r requirements.txt
```

### 5. 启动后端服务

```bash
python main.py
```

### 6. 构建 Android 应用

```bash
cd ../kotobahitomi
npx cap sync android
npx cap open android
# 使用 Android Studio 进行构建和调试
```

## 配置说明

- 后端环境变量请参考 `backend/.env` 文件。
- 前端多语言资源位于 `kotobahitomi/src/locales/`。

## 贡献

欢迎提交 issue 和 PR！

## License

MIT

