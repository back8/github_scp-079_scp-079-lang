# SCP-079-LANG - Ban or delete by detecting the language
# Copyright (C) 2019 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-LANG.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import pickle
from configparser import RawConfigParser
from os import mkdir
from os.path import exists
from shutil import rmtree
from threading import Lock
from typing import Dict, List, Set, Union

from pyrogram import Chat

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
    filename='log',
    filemode='w'
)
logger = logging.getLogger(__name__)

# Read data from config.ini

# [basic]
bot_token: str = ""
prefix: List[str] = []
prefix_str: str = "/!"

# [bots]
avatar_id: int = 0
captcha_id: int = 0
clean_id: int = 0
lang_id: int = 0
long_id: int = 0
noflood_id: int = 0
noporn_id: int = 0
nospam_id: int = 0
recheck_id: int = 0
tip_id: int = 0
user_id: int = 0
warn_id: int = 0

# [channels]
critical_channel_id: int = 0
debug_channel_id: int = 0
exchange_channel_id: int = 0
hide_channel_id: int = 0
logging_channel_id: int = 0
test_group_id: int = 0

# [custom]
backup: Union[str, bool] = ""
date_reset: str = ""
default_group_link: str = ""
lang_all: Union[str, Set[str]] = ""
lang_name: Union[str, Set[str]] = ""
lang_protect: Union[str, Set[str]] = ""
lang_sticker: Union[str, Set[str]] = ""
lang_text: Union[str, Set[str]] = ""
project_link: str = ""
project_name: str = ""
time_ban: int = 0
time_punish: int = 0
time_new: int = 0
zh_cn: Union[str, bool] = ""

# [encrypt]
key: Union[str, bytes] = ""
password: str = ""

try:
    config = RawConfigParser()
    config.read("config.ini")
    # [basic]
    bot_token = config["basic"].get("bot_token", bot_token)
    prefix = list(config["basic"].get("prefix", prefix_str))
    # [bots]
    avatar_id = int(config["bots"].get("avatar_id", avatar_id))
    captcha_id = int(config["bots"].get("captcha_id", captcha_id))
    clean_id = int(config["bots"].get("clean_id", clean_id))
    lang_id = int(config["bots"].get("lang_id", lang_id))
    long_id = int(config["bots"].get("long_id", long_id))
    noflood_id = int(config["bots"].get("noflood_id", noflood_id))
    noporn_id = int(config["bots"].get("noporn_id", noporn_id))
    nospam_id = int(config["bots"].get("nospam_id", nospam_id))
    recheck_id = int(config["bots"].get("recheck_id", recheck_id))
    tip_id = int(config["bots"].get("tip_id", tip_id))
    user_id = int(config["bots"].get("user_id", user_id))
    warn_id = int(config["bots"].get("warn_id", warn_id))
    # [channels]
    critical_channel_id = int(config["channels"].get("critical_channel_id", critical_channel_id))
    debug_channel_id = int(config["channels"].get("debug_channel_id", debug_channel_id))
    exchange_channel_id = int(config["channels"].get("exchange_channel_id", exchange_channel_id))
    hide_channel_id = int(config["channels"].get("hide_channel_id", hide_channel_id))
    logging_channel_id = int(config["channels"].get("logging_channel_id", logging_channel_id))
    test_group_id = int(config["channels"].get("test_group_id", test_group_id))
    # [custom]
    backup = config["custom"].get("backup", backup)
    backup = eval(backup)
    date_reset = config["custom"].get("date_reset", date_reset)
    default_group_link = config["custom"].get("default_group_link", default_group_link)
    lang_all = config["custom"].get("lang_all", lang_all)
    lang_all = set(lang_all.split())
    lang_name = config["custom"].get("lang_name", lang_name)
    lang_name = set(lang_name.split())
    lang_protect = config["custom"].get("lang_protect", lang_protect)
    lang_protect = set(lang_protect.split())
    lang_sticker = config["custom"].get("lang_sticker", lang_sticker)
    lang_sticker = set(lang_sticker.split())
    lang_text = config["custom"].get("lang_text", lang_text)
    lang_text = set(lang_text.split())
    project_link = config["custom"].get("project_link", project_link)
    project_name = config["custom"].get("project_name", project_name)
    time_ban = int(config["custom"].get("time_ban", time_ban))
    time_punish = int(config["custom"].get("time_punish", time_punish))
    time_new = int(config["custom"].get("time_new", time_new))
    zh_cn = config["custom"].get("zh_cn", zh_cn)
    zh_cn = eval(zh_cn)
    # [encrypt]
    key = config["encrypt"].get("key", key)
    key = key.encode("utf-8")
    password = config["encrypt"].get("password", password)
except Exception as e:
    logger.warning(f"Read data from config.ini error: {e}", exc_info=True)

# Check
if (bot_token in {"", "[DATA EXPUNGED]"}
        or prefix == []
        or avatar_id == 0
        or captcha_id == 0
        or clean_id == 0
        or lang_id == 0
        or long_id == 0
        or noflood_id == 0
        or noporn_id == 0
        or nospam_id == 0
        or recheck_id == 0
        or tip_id == 0
        or user_id == 0
        or warn_id == 0
        or critical_channel_id == 0
        or debug_channel_id == 0
        or exchange_channel_id == 0
        or hide_channel_id == 0
        or logging_channel_id == 0
        or test_group_id == 0
        or backup not in {False, True}
        or date_reset in {"", "[DATA EXPUNGED]"}
        or default_group_link in {"", "[DATA EXPUNGED]"}
        or lang_all in {"", "[DATA EXPUNGED]"} or lang_all == set()
        or lang_name in {"", "[DATA EXPUNGED]"} or lang_name == set()
        or lang_protect in {"", "[DATA EXPUNGED]"} or lang_protect == set()
        or lang_sticker in {"", "[DATA EXPUNGED]"} or lang_sticker == set()
        or lang_text in {"", "[DATA EXPUNGED]"} or lang_text == set()
        or project_link in {"", "[DATA EXPUNGED]"}
        or project_name in {"", "[DATA EXPUNGED]"}
        or time_ban == 0
        or time_punish == 0
        or time_new == 0
        or zh_cn not in {False, True}
        or key in {b"", b"[DATA EXPUNGED]", "", "[DATA EXPUNGED]"}
        or password in {"", "[DATA EXPUNGED]"}):
    logger.critical("No proper settings")
    raise SystemExit("No proper settings")

bot_ids: Set[int] = {avatar_id, captcha_id, clean_id, lang_id, long_id, noflood_id,
                     noporn_id, nospam_id, recheck_id, tip_id, user_id, warn_id}

# Languages
lang: Dict[str, str] = {
    # Admin
    "admin": (zh_cn and "管理员") or "Admin",
    "admin_group": (zh_cn and "群管理") or "Group Admin",
    "admin_project": (zh_cn and "项目管理员") or "Project Admin",
    # Basic
    "colon": (zh_cn and "：") or ": ",
    "score": (zh_cn and "评分") or "Score",
    "name": (zh_cn and "名称") or "Name",
    "action": (zh_cn and "执行操作") or "Action",
    "enabled": (zh_cn and "启用") or "Enabled",
    "disabled": (zh_cn and "禁用") or "Disabled",
    "clear": (zh_cn and "清空数据") or "Clear Data",
    "description": (zh_cn and "说明") or "Description",
    "reason": (zh_cn and "原因") or "Reason",
    "rollback": (zh_cn and "数据回滚") or "Rollback",
    "custom_group": (zh_cn and "群组自定义") or "Group Custom",
    "reset": (zh_cn and "重置数据") or "Reset Data",
    "version": (zh_cn and "版本") or "Version",
    # Config
    "default": (zh_cn and "默认") or "Default",
    "custom": (zh_cn and "自定义") or "Custom",
    "config_show": (zh_cn and "查看设置") or "Show Config",
    "config": (zh_cn and "设置") or "Settings",
    "delete": (zh_cn and "协助删除") or "Help Delete",
    "yes": (zh_cn and "是") or "Yes",
    "no": (zh_cn and "否") or "No",
    "name_default": (zh_cn and "默认名称设置") or "Default Name Setting",
    "name_enable": (zh_cn and "检查消息名称") or "Check Message's Name",
    "name_lang": (zh_cn and "封禁名称语言") or "Name Languages",
    "text_default": (zh_cn and "默认文字设置") or "Default text Setting",
    "text_enable": (zh_cn and "检查消息文字") or "Check Message's Text",
    "text_lang": (zh_cn and "删除文字语言") or "Text Languages",
    "sticker_default": (zh_cn and "默认贴纸设置") or "Default Sticker Setting",
    "sticker_enable": (zh_cn and "检查贴纸标题") or "Check Sticker's Title",
    "sticker_lang": (zh_cn and "删除贴纸语言") or "Sticker Title Languages",
    "filter": (zh_cn and "过滤") or "Filter",
    "ignore": (zh_cn and "忽略") or "Ignore",
    "spc": (zh_cn and "特殊中文") or "Special Chinese Characters",
    "spe": (zh_cn and "特殊英文") or "Special English Characters",
    "config_change": (zh_cn and "更改设置") or "Change Config",
    "config_button": (zh_cn and "请点击下方按钮进行设置") or "Press the Button to Config",
    "config_go": (zh_cn and "前往设置") or "Go to Config",
    "config_create": (zh_cn and "创建设置会话") or "Create Config Session",
    "config_updated": (zh_cn and "已更新") or "Updated",
    # Command
    "command_para": (zh_cn and "命令参数有误") or "Incorrect Command Parameter",
    "command_type": (zh_cn and "命令类别有误") or "Incorrect Command Type",
    "command_lack": (zh_cn and "命令参数缺失") or "Lack of Parameter",
    "config_locked": (zh_cn and "设置当前被锁定") or "Config is Locked",
    "command_usage": (zh_cn and "用法有误") or "Incorrect Usage",
    # Debug
    "triggered_by": (zh_cn and "触发消息") or "Triggered By",
    # Emergency
    "issue": (zh_cn and "发现状况") or "Issue",
    "exchange_invalid": (zh_cn and "数据交换频道失效") or "Exchange Channel Invalid",
    "auto_fix": (zh_cn and "自动处理") or "Auto Fix",
    "protocol_1": (zh_cn and "启动 1 号协议") or "Initiate Protocol 1",
    "transfer_channel": (zh_cn and "频道转移") or "Transfer Channel",
    "emergency_channel": (zh_cn and "应急频道") or "Emergency Channel",
    # Group
    "group_name": (zh_cn and "群组名称") or "Group Name",
    "group_id": (zh_cn and "群组 ID") or "Group ID",
    "reason_permissions": (zh_cn and "权限缺失") or "Missing Permissions",
    "reason_user": (zh_cn and "缺失 USER") or "Missing USER",
    "leave_approve": (zh_cn and "已批准退出群组") or "Approve to Leave the Group",
    "refresh": (zh_cn and "刷新群管列表") or "Refresh Admin Lists",
    "leave_auto": (zh_cn and "自动退出并清空数据") or "Leave automatically",
    "reason_leave": (zh_cn and "非管理员或已不在群组中") or "Not Admin in Group",
    "status_joined": (zh_cn and "已加入群组") or "Joined the Group",
    "status_left": (zh_cn and "已退出群组") or "Left the Group",
    "reason_admin": (zh_cn and "获取管理员列表失败") or "Failed to Fetch Admin List",
    "reason_unauthorized": (zh_cn and "未授权使用") or "Unauthorized",
    "inviter": (zh_cn and "邀请人") or "Inviter",
    # More
    "privacy": (zh_cn and "可能涉及隐私而未转发") or "Not Forwarded Due to Privacy Reason",
    "cannot_forward": (zh_cn and "此类消息无法转发至频道") or "The Message Cannot be Forwarded to Channel",
    # Message Types
    "gam": (zh_cn and "游戏") or "Game",
    "ser": (zh_cn and "服务消息") or "Service",
    # Record
    "project": (zh_cn and "项目编号") or "Project",
    "project_origin": (zh_cn and "原始项目") or "Original Project",
    "status": (zh_cn and "状态") or "Status",
    "user_id": (zh_cn and "用户 ID") or "User ID",
    "level": (zh_cn and "操作等级") or "Level",
    "rule": (zh_cn and "规则") or "Rule",
    "message_type": (zh_cn and "消息类别") or "Message Type",
    "message_game": (zh_cn and "游戏标识") or "Game Short Name",
    "message_lang": (zh_cn and "消息语言") or "Message Language",
    "message_freq": (zh_cn and "消息频率") or "Message Frequency",
    "user_score": (zh_cn and "用户得分") or "User Score",
    "user_bio": (zh_cn and "用户简介") or "User Bio",
    "user_name": (zh_cn and "用户昵称") or "User Name",
    "from_name": (zh_cn and "来源名称") or "Forward Name",
    "more": (zh_cn and "附加信息") or "Extra Info",
    # Terminate
    "auto_ban": (zh_cn and "自动封禁") or "Auto Ban",
    "name_examine": (zh_cn and "名称检查") or "Name Examination",
    "name_ban": (zh_cn and "名称封禁") or "Ban by Name",
    "watch_user": (zh_cn and "敏感追踪") or "Watched User",
    "watch_ban": (zh_cn and "追踪封禁") or "Watch Ban",
    "score_user": (zh_cn and "用户评分") or "High Score",
    "score_ban": (zh_cn and "评分封禁") or "Ban by Score",
    "auto_delete": (zh_cn and "自动删除") or "Auto Delete",
    "watch_delete": (zh_cn and "追踪删除") or "Watch Delete",
    # Test
    "record_content": (zh_cn and "过滤记录") or "Recorded content",
    "record_link": (zh_cn and "过滤链接") or "Recorded link",
    "white_listed": (zh_cn and "白名单") or "White Listed",
    # Unit
    "members": (zh_cn and "名") or "member(s)",
    "messages": (zh_cn and "条") or "message(s)"
}

# Init

all_commands: List[str] = [
    "config",
    "config_lang",
    "l",
    "long",
    "mention",
    "print",
    "t2s",
    "version"
]

chats: Dict[int, Chat] = {}
# chats = {
#     -10012345678: Chat
# }

contents: Dict[str, str] = {}
# contents = {
#     "content": "fr"
# }

declared_message_ids: Dict[int, Set[int]] = {}
# declared_message_ids = {
#     -10012345678: {123}
# }

default_config: Dict[str, Union[bool, int, Dict[str, Union[bool, List[str], Set[str]]]]] = {
    "default": True,
    "lock": 0,
    "delete": True,
    "name": {
        "default": True,
        "enable": True,
        "list": lang_name
    },
    "text": {
        "default": True,
        "enable": True,
        "list": lang_text
    },
    "sticker": {
        "default": True,
        "enable": True,
        "list": lang_sticker
    },
    "spc": True,
    "spe": False
}

default_user_status: Dict[str, Dict[Union[int, str], Union[float, int]]] = {
    "detected": {},
    "join": {},
    "score": {
        "captcha": 0.0,
        "clean": 0.0,
        "lang": 0.0,
        "long": 0.0,
        "noflood": 0.0,
        "noporn": 0.0,
        "nospam": 0.0,
        "recheck": 0.0,
        "warn": 0.0
    }
}

left_group_ids: Set[int] = set()

locks: Dict[str, Lock] = {
    "admin": Lock(),
    "message": Lock(),
    "regex": Lock(),
    "test": Lock(),
    "text": Lock()
}

receivers: Dict[str, List[str]] = {
    "bad": ["ANALYZE", "APPEAL", "AVATAR", "CAPTCHA", "CLEAN", "LANG", "LONG",
            "MANAGE", "NOFLOOD", "NOPORN", "NOSPAM", "RECHECK", "USER", "WATCH"],
    "declare": ["ANALYZE", "AVATAR", "CLEAN", "LANG", "LONG",
                "NOFLOOD", "NOPORN", "NOSPAM", "RECHECK", "USER", "WATCH"],
    "score": ["ANALYZE", "CAPTCHA", "CLEAN", "LANG", "LONG",
              "MANAGE", "NOFLOOD", "NOPORN", "NOSPAM", "RECHECK"],
    "watch": ["ANALYZE", "CAPTCHA", "CLEAN", "LANG", "LONG",
              "MANAGE", "NOFLOOD", "NOPORN", "NOSPAM", "RECHECK", "WATCH"]
}

recorded_ids: Dict[int, Set[int]] = {}
# recorded_ids = {
#     -10012345678: {12345678}
# }

regex: Dict[str, bool] = {
    "ad": False,
    "ban": False,
    "con": False,
    "del": False,
    "iml": False,
    "spc": True,
    "spe": True,
    "wb": True
}

sender: str = "LANG"

should_hide: bool = False

version: str = "0.1.1"

# Load data from pickle

# Init dir
try:
    rmtree("tmp")
except Exception as e:
    logger.info(f"Remove tmp error: {e}")

for path in ["data", "tmp"]:
    if not exists(path):
        mkdir(path)

# Init ids variables

admin_ids: Dict[int, Set[int]] = {}
# admin_ids = {
#     -10012345678: {12345678}
# }

bad_ids: Dict[str, Set[Union[int, str]]] = {
    "channels": set(),
    "users": set()
}
# bad_ids = {
#     "channels": {-10012345678},
#     "users": {12345678}
# }

except_ids: Dict[str, Set[str]] = {
    "channels": set(),
    "long": set(),
    "temp": set()
}
# except_ids = {
#     "channels": {-10012345678},
#     "long": {"content"},
#     "temp": {"content"}
# }

user_ids: Dict[int, Dict[str, Dict[Union[int, str], Union[float, int]]]] = {}
# user_ids = {
#     12345678: {
#         "detected": {
#               -10012345678: 1512345678
#         },
#         "join": {
#             -10012345678: 1512345678
#         },
#         "score": {
#             "captcha": 0.0,
#             "clean": 0.0,
#             "lang": 0.0,
#             "long": 0.0,
#             "noflood": 0.0,
#             "noporn": 0.0,
#             "nospam": 0.0,
#             "recheck": 0.0,
#             "warn": 0.0
#         }
#     }
# }

watch_ids: Dict[str, Dict[int, int]] = {
    "ban": {},
    "delete": {}
}
# watch_ids = {
#     "ban": {
#         12345678: 0
#     },
#     "delete": {
#         12345678: 0
#     }
# }

# Init data variables

configs: Dict[int, Dict[str, Union[bool, int, Dict[str, Union[bool, List[str], Set[str]]]]]] = {}
# configs = {
#     -10012345678: {
#         "default": True,
#         "lock": 0,
#         "delete": True,
#         "name": {
#             "default": True,
#             "enable": True,
#             "list": set()
#         },
#         "text": {
#             "default": True,
#             "enable": True,
#             "list": set()
#         },
#         "sticker": {
#             "default": True,
#             "enable": True,
#             "list": set()
#         },
#         "spc": True,
#         "spe": False
#     }
# }

# Init word variables

for word_type in regex:
    locals()[f"{word_type}_words"]: Dict[str, Dict[str, Union[float, int]]] = {}

# type_words = {
#     "regex": 0
# }

# Load data
file_list: List[str] = ["admin_ids", "bad_ids", "except_ids", "user_ids", "watch_ids", "configs"]
file_list += [f"{f}_words" for f in regex]
for file in file_list:
    try:
        try:
            if exists(f"data/{file}") or exists(f"data/.{file}"):
                with open(f"data/{file}", "rb") as f:
                    locals()[f"{file}"] = pickle.load(f)
            else:
                with open(f"data/{file}", "wb") as f:
                    pickle.dump(eval(f"{file}"), f)
        except Exception as e:
            logger.error(f"Load data {file} error: {e}", exc_info=True)
            with open(f"data/.{file}", "rb") as f:
                locals()[f"{file}"] = pickle.load(f)
    except Exception as e:
        logger.critical(f"Load data {file} backup error: {e}", exc_info=True)
        raise SystemExit("[DATA CORRUPTION]")

# Start program
copyright_text = (f"SCP-079-{sender} v{version}, Copyright (C) 2019 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
