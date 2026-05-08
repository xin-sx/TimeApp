# TimeApp - Android 时间设置应用

## 功能说明
- 界面包含年、月、日、时、分五个输入框
- 每个输入框下方有"修改"按钮
- 点击"修改"按钮会：
  1. 播放系统默认铃声
  2. 铃声结束后弹出对话框让你修改对应的时间值
- 底部有"保存方案"按钮用于保存设置

## 构建说明

### 方法一：使用 Android Studio
1. 使用 Android Studio 打开此项目
2. 等待 Gradle 同步完成
3. 点击 Build > Build Bundle(s) / APK(s) > Build APK(s)
4. APK 文件将生成在 `app/build/outputs/apk/debug/` 或 `app/build/outputs/apk/release/`

### 方法二：使用命令行
```bash
# 进入项目目录
cd TimeApp

# 授权
chmod +x gradlew

# 构建 Debug APK
./gradlew assembleDebug

# 或构建 Release APK
./gradlew assembleRelease
```

### 方法三：使用 Android SDK Command Line Tools
```bash
# 设置环境变量
export ANDROID_HOME=/path/to/android-sdk

# 构建
./gradlew assembleRelease
```

## 项目结构
```
TimeApp/
├── app/
│   ├── src/main/
│   │   ├── java/com/example/timeapp/
│   │   │   └── MainActivity.java     # 主界面逻辑
│   │   ├── res/
│   │   │   ├── layout/
│   │   │   │   └── activity_main.xml # 界面布局
│   │   │   ├── values/
│   │   │   │   ├── strings.xml       # 字符串资源
│   │   │   │   ├── colors.xml        # 颜色定义
│   │   │   │   └── styles.xml         # 样式定义
│   │   │   ├── mipmap-*/             # 应用图标
│   │   │   └── xml/
│   │   │       ├── backup_rules.xml
│   │   │       └── data_extraction_rules.xml
│   │   └── AndroidManifest.xml
│   └── build.gradle
├── build.gradle                        # 项目级构建配置
├── gradle.properties                  # Gradle 属性
└── gradlew                            # Gradle Wrapper 脚本
```

## 安装 APK
构建完成后，将 APK 文件传输到 Android 手机，在手机上允许安装未知来源的应用，然后安装即可。
