# -*- coding: utf-8 -*-
"""
ChatGPT 国际软件代理管家
Python 3.12 + PySide6 + psutil
通过 ProxyBridge_CLI.exe 按进程名分流：名单内软件走本地代理，其余进程默认直连。

注意：
1. 需要先安装 ProxyBridge Windows 版，并确认 ProxyBridge_CLI.exe、
   ProxyBridgeCore.dll 和 WinDivert 相关文件来自官方安装包。
2. ProxyBridge CLI 需要管理员权限。
3. 端口协议预设只是常见默认值，必须在“端口协议设置”中按实际监听协议核对。
4. HTTP 代理不支持 UDP 转发。默认对名单内软件的 UDP 流量使用 BLOCK，
   以避免 UDP/QUIC 流量意外直连；如确认需要 SOCKS5 UDP，可在代码中调整。
"""

import ctypes
import json
import os
import subprocess
import sys
import time
from pathlib import Path

try:
    import psutil
except ImportError:
    raise SystemExit("缺少 psutil。请运行：python -m pip install psutil")

try:
    from PySide6.QtCore import Qt, QTimer, QSize
    from PySide6.QtGui import QAction, QIcon, QPixmap, QPainter, QColor, QPen, QFont
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QLabel, QPushButton, QComboBox,
        QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QSystemTrayIcon,
        QMenu, QMessageBox, QDialog, QDialogButtonBox, QTableWidget,
        QTableWidgetItem, QHeaderView, QFileDialog, QCheckBox, QTextEdit,
        QLineEdit, QFormLayout
    )
except ImportError:
    raise SystemExit("缺少 PySide6。请运行：python -m pip install PySide6")

APP_NAME = "ChatGPT 国际软件代理管家"   # 需求 5：标题可在此处修改
PROCESS_NAME = "ChatGPT.exe"
PORTS = [8892,88, 8100, 10801, 10802, 10805, 10806, 10822, 10999]
ICON_FILE = "fso_publish_qt.ico"        # 需求 2：托盘/窗口图标文件

# 需求 1：浏览器不参与代理。这里既从默认清单里移除，也做兜底黑名单，
# 即使用户在设置里手动加入浏览器进程名，也会在保存/生成配置时被剔除。
BROWSER_PROCESS_NAMES = {
    "chrome.exe", "firefox.exe", "brave.exe", "opera.exe", "vivaldi.exe",
    "msedge.exe", "iexplore.exe", "chromium.exe", "thorium.exe",
}

# 常见国际软件进程名初始清单（不含浏览器），可在“设置”里编辑。
DEFAULT_PROXY_APPS = [
    "ChatGPT.exe", "Codex.exe",
]



# 便于首次配置的预设，不代表这些端口必然使用对应协议。
DEFAULT_PROTOCOLS = {
    8892: "SOCKS5",
    88: "HTTP",
    8100: "HTTP",
    10801: "SOCKS5",
    10802: "SOCKS5",
    10805: "SOCKS5",
    10806: "SOCKS5",
    10822: "SOCKS5",
    10999: "SOCKS5",
}


def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def app_data_dir():
    base = os.environ.get("LOCALAPPDATA") or str(Path.home())
    p = Path(base) / "ChatGPTProxyManager"
    p.mkdir(parents=True, exist_ok=True)
    return p


APP_DIR = app_data_dir()
CONFIG_FILE = APP_DIR / "settings.json"
PROFILE_DIR = APP_DIR / "profiles"
LOG_FILE = APP_DIR / "manager.log"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)


def default_settings():
    return {
        "selected_port": 88,
        "remember_selection": True,
        "auto_prompt": False,
        "monitor_enabled": True,
        "auto_start_proxy": True,
        "proxy_apps": DEFAULT_PROXY_APPS.copy(),
        # 需求 3：每个软件的独立代理开关，值为 False 表示该软件直连。
        "app_enabled": {name: True for name in DEFAULT_PROXY_APPS},
        "proxybridge_cli": r"C:\Program Files\ProxyBridge\ProxyBridge_CLI.exe",
        "protocols": {str(k): v for k, v in DEFAULT_PROTOCOLS.items()},
        "startup_task": False,
        "verbose": 1,
    }


def sanitize_apps(apps):
    """去重、去空、剔除浏览器进程名（需求 1）。"""
    result = []
    seen = set()
    for name in apps or []:
        name = str(name).strip()
        if not name or name == "*":
            continue
        low = name.lower()
        if low in BROWSER_PROCESS_NAMES:
            continue
        if low in seen:
            continue
        seen.add(low)
        result.append(name)
    return result


def load_settings():
    settings = default_settings()
    try:
        if CONFIG_FILE.exists():
            raw = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                settings.update(raw)
    except Exception:
        pass
    settings.setdefault("protocols", {})
    if not isinstance(settings.get("proxy_apps"), list):
        settings["proxy_apps"] = DEFAULT_PROXY_APPS.copy()
    # 兼容旧版本：旧内置预设名单不再默认启用；保留用户自行添加的进程名。
    legacy_preset = {
        "chatgpt.exe", "codex.exe", "discord.exe", "slack.exe", "telegram.exe",
        "whatsapp.exe", "signal.exe", "zoom.exe", "teams.exe", "ms-teams.exe",
        "skype.exe", "spotify.exe", "steam.exe", "steamwebhelper.exe",
        "epicgameslauncher.exe", "battle.net.exe", "agent.exe",
        "riotclientservices.exe", "ubisoftconnect.exe", "galaxyclient.exe",
        "origin.exe", "eadesktop.exe", "dropbox.exe", "googledrivefs.exe",
        "codex-computer-use-swift.exe", "icloud.exe", "code.exe", "cursor.exe",
        "windsurf.exe", "githubdesktop.exe", "figma.exe", "notion.exe",
        "obsidian.exe", "postman.exe", "docker desktop.exe",
        "docker desktop backend.exe", "docker.exe", "adobe premiere pro.exe",
        "photoshop.exe", "illustrator.exe", "acrobat.exe", "creative cloud.exe",
        "virtualbox.exe", "codex-windows-sandbox-service.exe",
    }
    loaded_apps = sanitize_apps(settings["proxy_apps"])
    if loaded_apps and all(name.lower() in legacy_preset for name in loaded_apps):
        # 原名单仅由旧内置预设组成时，自动迁移为 ChatGPT + Codex。
        settings["proxy_apps"] = DEFAULT_PROXY_APPS.copy()
    else:
        settings["proxy_apps"] = loaded_apps
    if not settings["proxy_apps"]:
        settings["proxy_apps"] = DEFAULT_PROXY_APPS.copy()
    # 规范独立开关字典
    enabled = settings.get("app_enabled")
    if not isinstance(enabled, dict):
        enabled = {}
    settings["app_enabled"] = {
        name: bool(enabled.get(name, True)) for name in settings["proxy_apps"]
    }
    settings.setdefault("auto_start_proxy", True)
    for port, proto in DEFAULT_PROTOCOLS.items():
        settings["protocols"].setdefault(str(port), proto)
    if settings.get("selected_port") not in PORTS:
        settings["selected_port"] = 88
    return settings


def save_settings(settings):
    CONFIG_FILE.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def write_log(message):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    try:
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    return line


def enabled_apps(settings):
    """当前需要走代理的软件列表（受独立开关控制，并剔除浏览器）。"""
    enabled = settings.get("app_enabled", {})
    apps = [name for name in settings.get("proxy_apps", []) if enabled.get(name, True)]
    apps = sanitize_apps(apps)
    return apps


def make_profile(port, protocol, proxy_apps=None):
    """生成按进程分流的 ProxyBridge 配置：名单内 TCP 走代理，名单外直连。

    为避免 HTTP 代理不支持 UDP 时发生 UDP/QUIC 直连，名单内应用 UDP 默认 BLOCK；
    其他应用 UDP/TCP 默认 DIRECT。
    """
    proto = "http" if protocol.upper() == "HTTP" else "socks5"
    apps = sanitize_apps(proxy_apps or DEFAULT_PROXY_APPS)
    if not apps:
        apps = [PROCESS_NAME]
    process_names = ";".join(apps)
    profile = {
        "Version": "1.0",
        "LocalhostViaProxy": False,
        "IsTrafficLoggingEnabled": True,
        "ProxyConfigs": [{
            "Id": 1, "Type": proto, "Host": "127.0.0.1", "Port": str(port),
            "Username": "", "Password": ""
        }],
        "ProxyRules": [
            {
                "ProcessName": process_names, "TargetHosts": "*", "TargetPorts": "*",
                "Protocol": "TCP", "Action": "PROXY", "IsEnabled": True,
                "ProxyConfigId": 1
            },
            {
                "ProcessName": process_names, "TargetHosts": "*", "TargetPorts": "*",
                "Protocol": "UDP", "Action": "BLOCK", "IsEnabled": True,
                "ProxyConfigId": 1
            },
            {
                "ProcessName": "*", "TargetHosts": "*", "TargetPorts": "*",
                "Protocol": "BOTH", "Action": "DIRECT", "IsEnabled": True,
                "ProxyConfigId": 1
            }
        ]
    }
    path = PROFILE_DIR / f"InternationalApps_{port}_{proto}.pbprofile"
    path.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_app_icon():
    """需求 2：加载 fso_publish_qt.ico；找不到则返回 None 由调用方回退。"""
    candidates = [
        Path.cwd() / ICON_FILE,
        Path(__file__).resolve().parent / ICON_FILE,
        APP_DIR / ICON_FILE,
    ]
    if getattr(sys, "frozen", False):
        candidates.insert(0, Path(sys.executable).resolve().parent / ICON_FILE)
    for path in candidates:
        try:
            if path.is_file():
                icon = QIcon(str(path))
                if not icon.isNull():
                    return icon
        except Exception:
            continue
    return None


def draw_fallback_icon():
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.setPen(QPen(QColor("#0f5132"), 3))
    painter.setBrush(QColor("#16a36a"))
    painter.drawRoundedRect(3, 3, 58, 58, 14, 14)
    painter.setPen(QPen(QColor("#ffffff"), 4))
    painter.setFont(QFont("Arial", 31, QFont.Weight.Bold))
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "P")
    painter.end()
    return QIcon(pixmap)


class ProtocolDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("端口协议设置")
        self.setMinimumWidth(430)
        self.settings = settings
        layout = QVBoxLayout(self)
        note = QLabel("请按你的代理客户端实际监听协议选择。端口号本身不能可靠判断协议。")
        note.setWordWrap(True)
        layout.addWidget(note)

        self.table = QTableWidget(len(PORTS), 2)
        self.table.setHorizontalHeaderLabels(["本地端口", "协议"])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        for row, port in enumerate(PORTS):
            item = QTableWidgetItem(str(port))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 0, item)
            combo = QComboBox()
            combo.addItems(["HTTP", "SOCKS5"])
            current = settings["protocols"].get(str(port), DEFAULT_PROTOCOLS[port])
            combo.setCurrentText(current.upper())
            self.table.setCellWidget(row, 1, combo)
        layout.addWidget(self.table)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def apply_changes(self):
        for row, port in enumerate(PORTS):
            combo = self.table.cellWidget(row, 1)
            self.settings["protocols"][str(port)] = combo.currentText()


class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("程序设置")
        self.setMinimumWidth(560)
        self.settings = settings
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.cli_edit = QLineEdit(settings.get("proxybridge_cli", ""))
        browse = QPushButton("浏览…")
        browse.clicked.connect(self.browse_cli)
        cli_row = QHBoxLayout()
        cli_row.addWidget(self.cli_edit, 1)
        cli_row.addWidget(browse)
        cli_widget = QWidget()
        cli_widget.setLayout(cli_row)
        form.addRow("ProxyBridge_CLI.exe", cli_widget)
        layout.addLayout(form)

        self.remember = QCheckBox("记住上次选择的端口")
        self.remember.setChecked(bool(settings.get("remember_selection", True)))
        layout.addWidget(self.remember)
        self.auto_start = QCheckBox("程序启动后自动开启代理（默认端口 88）")
        self.auto_start.setChecked(bool(settings.get("auto_start_proxy", True)))
        layout.addWidget(self.auto_start)
        self.monitor = QCheckBox("监测代理名单中的软件；发现新软件时自动开启代理")
        self.monitor.setChecked(bool(settings.get("monitor_enabled", True)))
        layout.addWidget(self.monitor)

        app_label = QLabel("默认仅 ChatGPT.exe、Codex.exe 走代理；其他软件可在此每行添加一个 .exe 进程名（浏览器会被自动忽略）：")
        layout.addWidget(app_label)
        self.apps_edit = QTextEdit()
        self.apps_edit.setMinimumHeight(190)
        self.apps_edit.setPlainText("\n".join(settings.get("proxy_apps", DEFAULT_PROXY_APPS)))
        layout.addWidget(self.apps_edit)
        app_hint = QLabel("提示：浏览器进程（Chrome/Edge/Firefox/Brave/Opera/Vivaldi 等）默认永不代理。")
        app_hint.setWordWrap(True)
        app_hint.setStyleSheet("color: #64748b;")
        layout.addWidget(app_hint)

        self.protocol_btn = QPushButton("端口协议设置…")
        self.protocol_btn.clicked.connect(self.edit_protocols)
        layout.addWidget(self.protocol_btn)

        self.protocols = dict(settings.get("protocols", {}))
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def browse_cli(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "选择 ProxyBridge_CLI.exe", str(Path(self.cli_edit.text()).parent),
            "ProxyBridge CLI (ProxyBridge_CLI.exe);;可执行文件 (*.exe)"
        )
        if path:
            self.cli_edit.setText(path)

    def edit_protocols(self):
        temp = dict(self.settings)
        temp["protocols"] = self.protocols
        dlg = ProtocolDialog(temp, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            dlg.apply_changes()
            self.protocols = temp["protocols"]

    def apply_changes(self):
        self.settings["proxybridge_cli"] = self.cli_edit.text().strip()
        self.settings["remember_selection"] = self.remember.isChecked()
        self.settings["auto_start_proxy"] = self.auto_start.isChecked()
        self.settings["auto_prompt"] = False
        self.settings["monitor_enabled"] = self.monitor.isChecked()
        apps = sanitize_apps(
            [x.strip() for x in self.apps_edit.toPlainText().splitlines() if x.strip()]
        )
        if not apps:
            apps = DEFAULT_PROXY_APPS.copy()
        self.settings["proxy_apps"] = apps
        old_enabled = self.settings.get("app_enabled", {})
        self.settings["app_enabled"] = {
            name: bool(old_enabled.get(name, True)) for name in apps
        }
        self.settings["protocols"] = self.protocols


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.cli_process = None
        self.current_port = None
        self.current_profile = None
        self.cli_output_handle = None
        self.known_pids = set()
        self._allow_quit = False
        self._last_notified_app = None
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(760, 640)
        icon = load_app_icon()
        self._app_icon = icon if icon is not None else draw_fallback_icon()
        self.setWindowIcon(self._app_icon)
        self.build_ui()
        self.build_tray()
        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self.check_processes)
        self.monitor_timer.start(1000)
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_status)
        self.refresh_timer.start(1500)
        self.log(f"程序已启动。代理名单 {len(self.settings.get('proxy_apps', []))} 个进程；默认端口 {self.settings.get('selected_port', 88)}。")
        self.check_processes(initial=True)
        if self.settings.get("auto_start_proxy", True):
            QTimer.singleShot(1200, self.start_proxy)

    # ---------- UI ----------
    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(22, 18, 22, 18)
        root.setSpacing(12)

        title = QLabel("ChatGPT 国际软件代理管家")
        title.setStyleSheet("font-size: 26px; font-weight: 800;")
        root.addWidget(title)
        desc = QLabel("代理名单内的软件走所选本地代理；其他所有进程（含浏览器）默认直连。")
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 13px; color: #64748b;")
        root.addWidget(desc)

        group = QGroupBox("代理设置")
        grid = QGridLayout(group)
        grid.addWidget(QLabel("代理端口："), 0, 0)
        self.port_combo = QComboBox()
        self.populate_ports()
        self.port_combo.currentIndexChanged.connect(self.port_selection_changed)
        grid.addWidget(self.port_combo, 0, 1)
        self.status_label = QLabel("状态：未启动")
        self.status_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        grid.addWidget(self.status_label, 1, 0, 1, 2)
        root.addWidget(group)

        buttons = QHBoxLayout()
        self.start_btn = QPushButton("开启代理")
        self.start_btn.clicked.connect(self.start_proxy)
        self.stop_btn = QPushButton("关闭代理")
        self.stop_btn.clicked.connect(self.stop_proxy)
        self.stop_btn.setEnabled(False)
        self.hide_btn = QPushButton("最小化到托盘")
        self.hide_btn.clicked.connect(self.hide_to_tray)
        buttons.addWidget(self.start_btn)
        buttons.addWidget(self.stop_btn)
        buttons.addWidget(self.hide_btn)
        root.addLayout(buttons)

        buttons2 = QHBoxLayout()
        self.settings_btn = QPushButton("设置…")
        self.settings_btn.clicked.connect(self.open_settings)
        self.startup_btn = QPushButton("设置开机自启")
        self.startup_btn.clicked.connect(self.install_startup_task)
        self.log_btn = QPushButton("打开日志")
        self.log_btn.clicked.connect(self.open_log)
        buttons2.addWidget(self.settings_btn)
        buttons2.addWidget(self.startup_btn)
        buttons2.addWidget(self.log_btn)
        root.addLayout(buttons2)

        # 需求 3 + 6：软件代理管理表（可单独开关 + 显示当前状态）
        apps_group = QGroupBox("软件代理管理与当前状态")
        apps_layout = QVBoxLayout(apps_group)
        self.apps_table = QTableWidget(0, 4)
        self.apps_table.setHorizontalHeaderLabels(
            ["软件进程名", "走代理", "运行状态", "代理状态"]
        )
        self.apps_table.verticalHeader().setVisible(False)
        header = self.apps_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.apps_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.apps_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        apps_layout.addWidget(self.apps_table)
        hint = QLabel("提示：取消勾选“走代理”即让该软件直连（会立即重建配置并重启 ProxyBridge）；灰色表示当前未运行。")
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #64748b; font-size: 12px;")
        apps_layout.addWidget(hint)
        root.addWidget(apps_group)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMaximumHeight(150)
        self.log_view.setPlaceholderText("运行日志…")
        root.addWidget(self.log_view)
        self.statusBar().showMessage(f"配置目录：{APP_DIR}")
        self.rebuild_apps_table()

    def populate_ports(self):
        current = self.settings.get("selected_port", 88)
        self.port_combo.blockSignals(True)
        self.port_combo.clear()
        for port in PORTS:
            proto = self.settings["protocols"].get(str(port), DEFAULT_PROTOCOLS[port])
            self.port_combo.addItem(f"{port} ({proto})", port)
        idx = self.port_combo.findData(current)
        self.port_combo.setCurrentIndex(idx if idx >= 0 else 0)
        self.port_combo.blockSignals(False)

    def rebuild_apps_table(self):
        apps = self.settings.get("proxy_apps", [])
        enabled = self.settings.get("app_enabled", {})
        self.apps_table.setRowCount(len(apps))
        self._app_checks = {}
        for row, name in enumerate(apps):
            name_item = QTableWidgetItem(name)
            self.apps_table.setItem(row, 0, name_item)

            check = QCheckBox()
            check.setChecked(bool(enabled.get(name, True)))
            check.stateChanged.connect(
                lambda state, n=name: self.toggle_app_proxy(n, state == Qt.CheckState.Checked.value)
            )
            holder = QWidget()
            h = QHBoxLayout(holder)
            h.setContentsMargins(0, 0, 0, 0)
            h.setAlignment(Qt.AlignmentFlag.AlignCenter)
            h.addWidget(check)
            self.apps_table.setCellWidget(row, 1, holder)
            self._app_checks[name] = check

            for col in (2, 3):
                it = QTableWidgetItem("-")
                it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.apps_table.setItem(row, col, it)

    def update_apps_status(self, running_processes):
        """需求 6：刷新每个软件运行状态与代理状态。"""
        if not hasattr(self, "apps_table"):
            return
        enabled = self.settings.get("app_enabled", {})
        proxy_on = self.cli_process is not None and self.cli_process.poll() is None
        for row in range(self.apps_table.rowCount()):
            name_item = self.apps_table.item(row, 0)
            if not name_item:
                continue
            name = name_item.text()
            is_running = name.lower() in running_processes
            run_item = self.apps_table.item(row, 2)
            proxy_item = self.apps_table.item(row, 3)
            if run_item is None or proxy_item is None:
                continue
            run_item.setText("运行中" if is_running else "未运行")
            if not enabled.get(name, True):
                proxy_item.setText("直连")
                proxy_item.setForeground(QColor("#64748b"))
            elif proxy_on:
                proxy_item.setText("代理中" if is_running else "已启用")
                proxy_item.setForeground(QColor("#138a54"))
            else:
                proxy_item.setText("代理未运行")
                proxy_item.setForeground(QColor("#b45309"))

    def toggle_app_proxy(self, name, checked):
        """需求 3：单独开启/关闭某个软件的代理，立即生效。"""
        self.settings.setdefault("app_enabled", {})[name] = bool(checked)
        save_settings(self.settings)
        self.log(f"{name} → {'走代理' if checked else '直连'}（单独开关）")
        # 立即按新名单重建配置并重启 CLI，使开关生效。
        if self.cli_process and self.cli_process.poll() is None:
            self.restart_proxy_for_current_port()
        self.refresh_status()

    def build_tray(self):
        # 需求 2：优先使用 fso_publish_qt.ico
        self.tray = QSystemTrayIcon(self._app_icon, self)
        self.tray.setToolTip(APP_NAME + "：双击打开，右键管理代理")
        menu = QMenu()
        show_action = QAction("打开管理界面", self)
        show_action.triggered.connect(self.show_window)
        self.tray_start_action = QAction("开启代理", self)
        self.tray_start_action.triggered.connect(self.start_proxy)
        self.tray_stop_action = QAction("关闭代理", self)
        self.tray_stop_action.triggered.connect(self.stop_proxy)
        self.tray_port_menu = menu.addMenu("切换代理端口")
        for port in PORTS:
            action = QAction(str(port), self)
            action.triggered.connect(lambda checked=False, p=port: self.switch_port(p))
            self.tray_port_menu.addAction(action)
        menu.addSeparator()
        menu.addAction(self.tray_start_action)
        menu.addAction(self.tray_stop_action)
        menu.addSeparator()
        menu.addAction(show_action)
        settings_action = QAction("设置…", self)
        settings_action.triggered.connect(self.open_settings)
        menu.addAction(settings_action)
        quit_action = QAction("退出程序", self)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.tray_activated)
        # 需求 4：点击托盘气泡关闭对应软件的代理
        self.tray.messageClicked.connect(self.on_tray_message_clicked)
        self.tray.show()
        self.log("系统托盘图标已创建。")

    def on_tray_message_clicked(self):
        """需求 4：点击右下角提示，关闭刚才提示软件的代理。"""
        name = self._last_notified_app
        if not name:
            return
        self.log(f"用户点击托盘提示，关闭 {name} 的代理。")
        check = getattr(self, "_app_checks", {}).get(name)
        if check is not None:
            check.setChecked(False)  # 触发 toggle_app_proxy
        else:
            self.toggle_app_proxy(name, False)
        self._last_notified_app = None

    def log(self, message):
        line = write_log(message)
        if hasattr(self, "log_view"):
            self.log_view.append(line)

    def selected_port(self):
        return int(self.port_combo.currentData())

    def port_selection_changed(self):
        port = self.selected_port()
        if self.settings.get("remember_selection", True):
            self.settings["selected_port"] = port
            save_settings(self.settings)
        # 已经运行时，切换端口立即重建配置并切换，不要求用户手动关闭/开启。
        if (self.cli_process and self.cli_process.poll() is None
                and self.current_port != port):
            QTimer.singleShot(0, lambda target=port: self.restart_proxy_for_current_port(target))

    def switch_port(self, port):
        idx = self.port_combo.findData(port)
        if idx >= 0:
            self.port_combo.setCurrentIndex(idx)
        # currentIndexChanged 会自动处理运行中的端口切换。
        if not (self.cli_process and self.cli_process.poll() is None):
            self.settings["selected_port"] = port
            save_settings(self.settings)

    def restart_proxy_for_current_port(self, target_port=None):
        # 必须使用新选择的端口，不能误用旧的 current_port。
        port = int(target_port if target_port is not None else self.selected_port())
        if self.stop_proxy():
            idx = self.port_combo.findData(port)
            if idx >= 0 and self.port_combo.currentData() != port:
                self.port_combo.setCurrentIndex(idx)
            self.settings["selected_port"] = port
            save_settings(self.settings)
            self.start_proxy()

    # ---------- 代理启停 ----------
    def start_proxy(self):
        port = self.selected_port()
        cli = Path(self.settings.get("proxybridge_cli", ""))
        if not cli.is_file():
            QMessageBox.warning(
                self, APP_NAME,
                "找不到 ProxyBridge_CLI.exe。\n\n请先安装 ProxyBridge，然后在“设置…”中指定 CLI 路径。"
            )
            self.open_settings()
            return
        core = cli.parent / "ProxyBridgeCore.dll"
        if not core.exists():
            QMessageBox.warning(
                self, APP_NAME,
                f"同目录没有找到：\n{core}\n\n请确认使用官方完整安装包，并将 CLI 与 DLL 保持在同一目录。"
            )
            return

        if self.cli_process and self.cli_process.poll() is None:
            if self.current_port == port:
                self.log(f"代理已经运行，端口 {port}。")
                return
            if not self.stop_proxy():
                return

        apps = enabled_apps(self.settings)
        if not apps:
            self.log("代理名单为空（或全部被关闭），不启动 ProxyBridge。")
            self.refresh_status()
            return

        protocol = self.settings["protocols"].get(str(port), DEFAULT_PROTOCOLS[port]).upper()
        profile = make_profile(port, protocol, apps)
        args = [str(cli), "--profile", str(profile), "--verbose", str(self.settings.get("verbose", 1))]
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0
            creationflags = subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NEW_PROCESS_GROUP
            self.cli_output_handle = LOG_FILE.open("a", encoding="utf-8", errors="replace")
            self.cli_output_handle.write(
                f"\n--- ProxyBridge CLI start: port={port}, protocol={protocol}, apps={len(apps)} ---\n"
            )
            self.cli_output_handle.flush()
            self.cli_process = subprocess.Popen(
                args,
                cwd=str(cli.parent),
                stdin=subprocess.DEVNULL,
                stdout=self.cli_output_handle,
                stderr=subprocess.STDOUT,
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            QApplication.processEvents()
            time.sleep(0.8)
            if self.cli_process.poll() is not None:
                try:
                    output = self.cli_process.stdout.read() if self.cli_process.stdout else ""
                except Exception:
                    output = ""
                self.log(f"ProxyBridge 启动失败，退出码 {self.cli_process.returncode}。{output[-1500:]}")
                QMessageBox.critical(
                    self, APP_NAME,
                    "ProxyBridge CLI 很快就退出了。\n请检查管理员权限、配置格式、驱动和代理端口。\n\n"
                    + output[-1200:]
                )
                self.cli_process = None
                return
            self.current_port = port
            self.current_profile = profile
            self.log(f"已启动 ProxyBridge：{len(apps)} 个软件 → {protocol} 127.0.0.1:{port}")
            self.refresh_status()
        except Exception as exc:
            self.log(f"启动代理失败：{exc}")
            QMessageBox.critical(self, APP_NAME, f"启动 ProxyBridge 失败：\n{exc}")

    def stop_proxy(self):
        proc = self.cli_process
        if not proc or proc.poll() is not None:
            self.cli_process = None
            self.current_port = None
            self.refresh_status()
            self.log("代理当前未运行。")
            return True
        try:
            self.log("正在请求 ProxyBridge 正常停止…")
            try:
                proc.send_signal(signal_ctrl_break())
                proc.wait(timeout=4)
            except Exception:
                pass
            if proc.poll() is None:
                self.log("正常停止超时，尝试结束 CLI 进程。")
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    proc.kill()
            self.log("ProxyBridge CLI 已停止。")
        except Exception as exc:
            self.log(f"停止 CLI 时出现问题：{exc}")
            return False
        finally:
            self.cli_process = None
            self.current_port = None
            self.current_profile = None
            if self.cli_output_handle:
                try:
                    self.cli_output_handle.flush()
                    self.cli_output_handle.close()
                except Exception:
                    pass
                self.cli_output_handle = None
            self.refresh_status()
        return True

    def refresh_status(self):
        running = self.cli_process is not None and self.cli_process.poll() is None
        if running:
            self.status_label.setText(f"状态：代理运行中  |  127.0.0.1:{self.current_port}")
            self.status_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #138a54;")
        else:
            self.status_label.setText("状态：代理未运行")
            self.status_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #64748b;")
            if self.cli_process is not None:
                self.log(f"ProxyBridge CLI 已退出，退出码 {self.cli_process.returncode}")
                self.cli_process = None
                self.current_port = None
        self.start_btn.setEnabled(not running)
        self.stop_btn.setEnabled(running)
        self.tray_start_action.setEnabled(not running)
        self.tray_stop_action.setEnabled(running)
        # 状态表按当前运行情况刷新
        try:
            names = self._running_app_names()
            self.update_apps_status(names)
        except Exception:
            pass

    def _running_app_names(self):
        return {name.lower() for name in getattr(self, "_current_running", set())}

    # ---------- 进程监测 ----------
    def check_processes(self, initial=False):
        if not self.settings.get("monitor_enabled", True):
            return
        apps = sanitize_apps(self.settings.get("proxy_apps", DEFAULT_PROXY_APPS))
        app_names = {str(x).strip().lower() for x in apps if str(x).strip()}
        found = {}
        try:
            for proc in psutil.process_iter(["pid", "name"]):
                try:
                    name = (proc.info.get("name") or "").strip()
                    if name.lower() in app_names:
                        found[int(proc.info["pid"])] = name
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception as exc:
            self.log(f"进程监测异常：{exc}")
            return

        self._current_running = set(found.values())
        self.update_apps_status({n.lower() for n in self._current_running})

        current_pids = set(found)
        new_pids = current_pids - self.known_pids
        if initial:
            new_pids = set()
        self.known_pids = current_pids

        if new_pids:
            # 只对“已启用代理”的新启动软件提示
            enabled = self.settings.get("app_enabled", {})
            notified = None
            for pid in sorted(new_pids):
                name = found[pid]
                self.log(f"检测到代理名单软件：{name}，PID={pid}")
                if enabled.get(name, True) and notified is None:
                    notified = name
            if notified:
                # 需求 4：右下角提示，点击可关闭该软件代理
                self._last_notified_app = notified
                self.tray.showMessage(
                    APP_NAME,
                    f"监测到您已经打开 {notified} 并自动代理，点击可关闭该软件的代理模式。",
                    QSystemTrayIcon.MessageIcon.Information,
                    6000
                )
            # 确保 CLI 在运行
            if self.cli_process is None or self.cli_process.poll() is not None:
                self.log("名单软件已启动，自动开启代理。")
                self.start_proxy()

    # ---------- 其他 ----------
    def open_settings(self):
        dlg = SettingsDialog(self.settings, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            dlg.apply_changes()
            save_settings(self.settings)
            self.populate_ports()
            self.rebuild_apps_table()
            self.log("设置已保存。")
            if self.cli_process and self.cli_process.poll() is None:
                self.restart_proxy_for_current_port()

    def hide_to_tray(self):
        self.hide()
        if not self.tray.isVisible():
            self.tray.show()
        self.tray.showMessage(
            APP_NAME,
            "程序已缩到系统托盘。双击图标可重新打开，右键可管理代理。",
            QSystemTrayIcon.MessageIcon.Information,
            3000
        )
        self.log("主窗口已隐藏到系统托盘。")

    def show_window(self):
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized)
        self.raise_()
        self.activateWindow()

    def tray_activated(self, reason):
        if reason in (QSystemTrayIcon.ActivationReason.DoubleClick,
                      QSystemTrayIcon.ActivationReason.Trigger):
            self.show_window()

    def open_log(self):
        try:
            os.startfile(str(LOG_FILE))
        except Exception as exc:
            QMessageBox.warning(self, APP_NAME, f"无法打开日志：{exc}")

    def install_startup_task(self):
        task_name = "ChatGPTProxyManager"
        if getattr(sys, "frozen", False):
            command = f'"{sys.executable}"'
        else:
            script = str(Path(__file__).resolve())
            python_exe = Path(sys.executable)
            pythonw = python_exe.with_name("pythonw.exe")
            launch_exe = str(pythonw if pythonw.exists() else python_exe)
            command = f'"{launch_exe}" "{script}"'
        import getpass
        current_user = os.environ.get("USERDOMAIN", "") + "\\" + getpass.getuser()
        cmd = [
            "schtasks", "/Create", "/TN", task_name,
            "/SC", "ONLOGON", "/RL", "HIGHEST", "/IT",
            "/RU", current_user, "/F", "/TR", command
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
            if result.returncode == 0:
                self.settings["startup_task"] = True
                save_settings(self.settings)
                self.log("已创建开机登录启动计划任务。")
                QMessageBox.information(self, APP_NAME, "已设置登录后自动启动（最高权限）。")
            else:
                self.log(f"创建开机任务失败：{result.stderr or result.stdout}")
                QMessageBox.warning(self, APP_NAME,
                                    "创建计划任务失败。\n请确认程序以管理员身份运行。\n\n"
                                    + (result.stderr or result.stdout))
        except Exception as exc:
            QMessageBox.critical(self, APP_NAME, f"创建计划任务失败：{exc}")

    def closeEvent(self, event):
        if self._allow_quit:
            event.accept()
        else:
            event.ignore()
            self.hide_to_tray()

    def quit_app(self):
        self._allow_quit = True
        self.stop_proxy()
        self.tray.hide()
        QApplication.quit()


def signal_ctrl_break():
    import signal
    return getattr(signal, "CTRL_BREAK_EVENT", 1)


def main():
    if os.name != "nt":
        raise SystemExit("本程序仅支持 Windows。")

    if not is_admin():
        result = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable,
            subprocess.list2cmdline(sys.argv),
            str(Path.cwd()), 1
        )
        if result > 32:
            return 0
        app = QApplication(sys.argv)
        QMessageBox.critical(None, APP_NAME, "需要管理员权限才能启动 ProxyBridge CLI。")
        return 1

    try:
        ctypes.windll.kernel32.FreeConsole()
    except Exception:
        pass

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())