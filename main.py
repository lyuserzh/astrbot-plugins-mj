import os
import random

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star
from astrbot.api import logger, AstrBotConfig
import astrbot.api.message_components as Comp


class MJPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig = None):
        super().__init__(context)
        self.config = config or {}
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        # mj 视频
        self.mj_videos = ["mj1.mp4", "mj2.mp4"]
        # isa 图片
        self.isa_image = "isa.png"
        self._last_video: str | None = None
        logger.info("关键词自动回复插件已加载")

    def _cfg_bool(self, key: str, default: bool = True) -> bool:
        try:
            val = self.config.get(key, default)
            return bool(val)
        except Exception:
            return default

    def _pick_video(self) -> str:
        """轮流 + 随机选视频"""
        available = [
            name
            for name in self.mj_videos
            if os.path.isfile(os.path.join(self.plugin_dir, name))
        ]
        if not available:
            return ""

        if self._last_video and len(available) > 1:
            others = [n for n in available if n != self._last_video]
            if others and random.random() < 0.8:
                choice = random.choice(others)
            else:
                choice = random.choice(available)
        else:
            choice = random.choice(available)

        self._last_video = choice
        return choice

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent):
        """检测到关键词时回复文字 / 图片 / 视频"""
        original = event.message_str.strip()
        if not original:
            return

        if event.get_sender_id() == event.get_self_id():
            return

        text_lower = original.lower()

        # 按优先级匹配：mj / isa / 牛来
        keywords = ["mj", "isa", "牛来"]
        matched_kw = None
        for kw in keywords:
            if kw.isascii():
                if kw in text_lower:
                    matched_kw = kw
                    break
            else:
                if kw in original:
                    matched_kw = kw
                    break

        if not matched_kw:
            return

        logger.info(f"检测到「{matched_kw}」，来自 {event.get_sender_name()}")

        # ----- mj：可选文字 + 视频 -----
        if matched_kw == "mj":
            if self._cfg_bool("send_mj_text", True):
                yield event.plain_result("mj")

            video_name = self._pick_video()
            if not video_name:
                logger.warning("没有可用的 mj 视频，请放置 mj1.mp4 / mj2.mp4")
            else:
                path = os.path.abspath(os.path.join(self.plugin_dir, video_name))
                logger.info(f"发送视频: {video_name}")
                yield event.chain_result([Comp.Video.fromFileSystem(path=path)])
            return

        # ----- isa：可选文字 + 图片 -----
        if matched_kw == "isa":
            if self._cfg_bool("send_isa_text", True):
                yield event.plain_result("isa")

            img_path = os.path.join(self.plugin_dir, self.isa_image)
            if not os.path.isfile(img_path):
                logger.warning(f"图片不存在: {img_path}，请放置 isa.png")
            else:
                abs_path = os.path.abspath(img_path)
                logger.info(f"发送图片: {self.isa_image}")
                yield event.chain_result(
                    [Comp.Image.fromFileSystem(path=abs_path)]
                )
            return

        # ----- 牛来：仅文字 -----
        if matched_kw == "牛来":
            yield event.plain_result("牛来")
            return

    async def terminate(self):
        logger.info("关键词自动回复插件已卸载")
