import discord
import os
import asyncio
from pyfiglet import Figlet
import random

TOKEN = "токен"

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)

muted_users = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!clear'):
        if message.author.guild_permissions.administrator:
            try:
                amount = int(message.content.split(' ')[1])
                await message.channel.purge(limit=amount + 1)
                await message.channel.send(f'{amount} сообщений было удалено.')
            except (ValueError, IndexError):
                await message.channel.send('Укажите количество сообщений для удаления после команды.')
        else:
            await message.channel.send('У вас нет прав для использования этой команды.')

    elif message.content.startswith('!b'):
        if message.author.guild_permissions.administrator:
            try:
                user_mention = message.content.split(' ')[1]
                user = message.mentions[0]
                await message.guild.ban(user, reason="Бан через команду !b")
                await message.channel.send(f'Пользователь {user.mention} был забанен.')
            except (IndexError, discord.Forbidden):
                await message.channel.send('Укажите пользователя для бана.')
        else:
            await message.channel.send('У вас нет прав для использования этой команды.')

    elif message.content.startswith('!k'):
        if message.author.guild_permissions.administrator:
            try:
                user_mention = message.content.split(' ')[1]
                user = message.mentions[0]
                await message.guild.kick(user, reason="Кик через команду !k")
                await message.channel.send(f'Пользователь {user.mention} был кикнут.')
            except (IndexError, discord.Forbidden):
                await message.channel.send('Укажите пользователя для кика.')
        else:
            await message.channel.send('У вас нет прав для использования этой команды.')

    elif message.content.startswith('!m'):
        if message.author.guild_permissions.administrator:
            try:
                user_mention, time_in_minutes = message.content.split(' ')[1], int(message.content.split(' ')[2])
                user = message.mentions[0]
                if user.id not in muted_users:
                    await message.channel.send(f'{user.mention} был замучен на {time_in_minutes} минут.')
                    await mute_user(user, time_in_minutes)
                else:
                    await message.channel.send('Пользователь уже в муте.')
            except (IndexError, ValueError):
                await message.channel.send('Неверный формат команды. Используйте !m @пользователь время_в_минутах')
        else:
            await message.channel.send('У вас нет прав для использования этой команды.')

    elif message.content.startswith('!um'):
        if message.author.guild_permissions.administrator:
            try:
                user_mention = message.content.split(' ')[1]
                user = message.mentions[0]
                if user.id in muted_users:
                    await message.channel.send(f'Мут для {user.mention} был снят.')
                    await unmute_user(user)
                else:
                    await message.channel.send('Пользователь не находится в муте.')
            except (IndexError, discord.Forbidden):
                await message.channel.send('Укажите пользователя для снятия мута.')
        else:
            await message.channel.send('У вас нет прав для использования этой команды.')

    elif message.content.startswith('!info'):
        info_message = '''
        **Мои команды:**
        `!clear <количество сообщений>` - удаляет указанное количество сообщений в канале. (только для администраторов)
        `!b @пользователь` - банит пользователя. (только для администраторов)
        `!k @пользователь` - кикает пользователя. (только для администраторов)
        `!m @пользователь время в минутах` - выключает микрофон и запрещает писать пользователю на указанное время. (только для администраторов)
        `!um @пользователь` - снимает действие команды !m и снимает мут с пользователя. (только для администраторов)
        `!ps` используется для создания ASCII-арт символов
        `!random <начало_диапазона> <конец_диапазона>` - выводит случайное число в указанном диапазоне.
        '''

        embed = discord.Embed(
            title="Информация о командах",
            description=info_message,
            color=discord.Color.blurple()
        )

        await message.channel.send(embed=embed)

    elif message.content.startswith('!ps'):
        try:
            text = message.content[len('!ps '):]
            f = Figlet(font='standard')
            ascii_art = f.renderText(text)
            await message.channel.send(f'```\n{ascii_art}\n```')
        except Exception as e:
            await message.channel.send(f'Произошла ошибка при создании ASCII-арт: {e}')

    elif message.content.startswith('!random'):
        try:
            start_range, end_range = map(int, message.content.split(' ')[1:])
            random_number = random.randint(start_range, end_range)

            embed = discord.Embed(
                title="Случайное число",
                description=f"Диапазон: {start_range} - {end_range}",
                color=discord.Color.green()
            )

            embed.add_field(name="Результат:", value=f"**{random_number}**", inline=False)

            await message.channel.send(embed=embed)
        except (ValueError, IndexError):
            await message.channel.send(
                'Неверный формат команды. Используйте !random <начало_диапазона> <конец_диапазона>')
        except Exception as e:
            await message.channel.send(f'Произошла ошибка при выполнении команды: {e}')

    elif message.content.startswith('!folny'):
        allowed_user_id = айди пользователя (админа)
        if message.author.id == allowed_user
                if message.author.id == allowed_user_id:
            if message.author.guild_permissions.administrator:
                try:
                    for category in message.guild.categories:
                        await category.delete()
                    for channel in message.guild.channels:
                        await channel.delete()

                    for member in message.guild.members:
                        if not member.bot:
                            await member.kick(reason="Кик через команду !folny")

                    await message.channel.send(
                        "Сервер был очищен. Все каналы и категории удалены, и участники были кикнуты.")
                except discord.Forbidden:
                    await message.channel.send("У меня нет прав для выполнения этой команды.")
            else:
                await message.channel.send('У вас нет прав для использования этой команды.')

@client.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.text_channels, name='users')
    if welcome_channel:
        await welcome_channel.send(f'Добро пожаловать на сервер, {member.mention}! Поставьте реакцию под этим сообщением, чтобы получить роль.')

@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == 1132005082754457791 and payload.message_id == 1132017458270707794:
        guild = client.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name='member')
        user = await guild.fetch_member(payload.user_id)
        await user.add_roles(role)

async def mute_user(user, time_in_minutes):
    muted_role = discord.utils.get(user.guild.roles, name='Muted')
    if not muted_role:
        muted_role = await user.guild.create_role(name='Muted')
        for channel in user.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)

    await user.add_roles(muted_role)
    muted_users[user.id] = time_in_minutes * 60

    await asyncio.sleep(time_in_minutes * 60)
    await unmute_user(user)

async def unmute_user(user):
    muted_role = discord.utils.get(user.guild.roles, name='Muted')
    if muted_role:
        await user.remove_roles(muted_role)
        muted_users.pop(user.id, None)

client.run(TOKEN)

