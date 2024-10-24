import os
import logging
from pyrogram import Client
import asyncio
from datetime import datetime, time, timedelta
import pytz

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimpleSigner:
    def __init__(self):
        # 使用固定的 API 凭证
        self.api_id = 611335
        self.api_hash = "d524b414d21f4d37f08684c1df41ac9c"
        # 从环境变量获取聊天ID和签到消息
        self.chat_id = int(os.environ["CHAT_ID"])
        self.sign_message = os.environ.get("SIGN_MESSAGE", "/sign")
        
        self.app = Client(
            "my_account",
            api_id=self.api_id,
            api_hash=self.api_hash
        )
        
    async def send_sign_message(self):
        try:
            async with self.app:
                await self.app.send_message(self.chat_id, self.sign_message)
                logger.info(f"签到成功: {datetime.now()}")
        except Exception as e:
            logger.error(f"签到失败: {e}")
            await asyncio.sleep(60)
            return await self.send_sign_message()

    async def run_daily(self):
        while True:
            try:
                now = datetime.now(pytz.timezone('Asia/Shanghai'))
                target = datetime.combine(now.date(), time(6, 0))  # 每天6点签到
                target = pytz.timezone('Asia/Shanghai').localize(target)
                
                if now > target:
                    target += timedelta(days=1)
                
                wait_seconds = (target - now).total_seconds()
                logger.info(f"下次签到时间: {target}")
                await asyncio.sleep(wait_seconds)
                
                await self.send_sign_message()
            except Exception as e:
                logger.error(f"运行错误: {e}")
                await asyncio.sleep(300)

async def main():
    signer = SimpleSigner()
    logger.info("签到程序启动...")
    await signer.run_daily()

if __name__ == "__main__":
    asyncio.run(main())
