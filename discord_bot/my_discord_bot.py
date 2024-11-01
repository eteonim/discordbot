import discord
from discord.ext import commands
from discord.ui import Button, View
import tkinter as tk
from tkinter import messagebox
import threading

# 디스코드 봇 설정
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 역할과 채널 ID 설정
JOIN_ROLE_ID = 1178742198204899378  # 입장 시 부여할 역할 ID
AUTH_ROLE_ID = 1178280653213671516  # 인증된 역할 ID
LOG_CHANNEL_ID = 1301787752597032980  # 로그 채널 ID

@bot.event
async def on_ready():
    print(f'{bot.user}로 로그인되었습니다!')

@bot.event
async def on_member_join(member):
    role = member.guild.get_role(JOIN_ROLE_ID)
    if role:
        await member.add_roles(role)
        
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(f'{member.mention}님이 서버에 들어오셨습니다!')

    button = Button(label='인증하기', style=discord.ButtonStyle.green)

    async def button_callback(interaction):
        auth_role = member.guild.get_role(AUTH_ROLE_ID)
        if auth_role:
            await member.add_roles(auth_role)
            # 인증 후 JOIN_ROLE_ID 역할 제거
            await member.remove_roles(role)
            await interaction.response.send_message(f'{member.mention}님이 인증되었습니다!', ephemeral=True)
        else:
            await interaction.response.send_message("인증 역할을 찾을 수 없습니다.", ephemeral=True)

    button.callback = button_callback
    view = View()
    view.add_item(button)
    
    await member.send('환영합니다! 아래 버튼을 클릭하여 인증하세요.', view=view)

@bot.event
async def on_member_remove(member):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(f'{member.mention}님이 서버를 나가셨습니다!')

def run_bot():
    bot.run('YOUR_BOT_TOKEN')  # 여기에 실제 봇 토큰을 입력하세요.

def start_bot():
    threading.Thread(target=run_bot).start()
    messagebox.showinfo("봇 실행", "봇이 실행되었습니다!")

def stop_bot():
    bot.loop.stop()
    messagebox.showinfo("봇 종료", "봇이 종료되었습니다.")
    root.quit()

# GUI 애플리케이션 생성
root = tk.Tk()
root.title("디스코드 봇 관리")

start_button = tk.Button(root, text="봇 실행", command=start_bot)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="봇 종료", command=stop_bot)
stop_button.pack(pady=10)

root.mainloop()
