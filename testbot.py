import discord
from discord.ext import commands

client = commands.Bot(command_prefix = "?")

@client.event
async def on_ready():
    print("bot test begins")

#on message commands
filtered_words = ["fuck", "pussy"  ]
@client.event
async def on_message(message):
    for word in filtered_words:
        if word in message.content:
            await message.delete()
    
   
   
   
    if ':' == message.content[0] and ':' == message.content[-1]:
        emoji_name = message.content[1:-1]
        
        for emoji in message.guild.emojis:
            if emoji_name == emoji.name:
                await message.channel.send(str(emoji))
                await message.delete()
                break

    await client.process_commands(message)
 
#error prevention
@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("you dont have permission 🙄")
        await ctx.message.delete()
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("argument missing 😶")
        await ctx.message.delete()
    else:
        raise error 

       
#fun command
@client.command()
async def hello(ctx):
    await ctx.send("testbot says hi")

#purge
@client.command(aliases=['Purge'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx,amount=2):
    await ctx.channel.purge(limit = amount)

#kick user
@client.command(aliases=['Kick'])
@commands.has_permissions(kick_members=True)
async def kick(ctx,member : discord.Member,*,reason= "No reason provided"):
    try:
        await member.kick(reason=reason)

        await member.send("you have been kicked "+reason)
    except:
        await member.kick(reason=reason)
        await ctx.send("dm are closed")
    
    await ctx.send(member.name + "was kicked")

#ban user
@client.command(aliases=['Ban'])
@commands.has_permissions(ban_members=True)
async def ban(ctx,member : discord.Member,*,reason= "No reason provided"):
    try:
        await member.ban(reason=reason)
        await member.send("you have been banned "+reason)
    except:
        await member.ban(reason=reason)
        await ctx.send("dm are closed")
   
    await ctx.send(member.name+"was banned")

#unban user
@client.command(aliases=['Unban'])
@commands.has_permissions(ban_members=True)
async def unban(ctx,*,member):
    banned_user = await ctx.guild.bans()
    member_name, member_disc = member.split('#')
    for banned_entry in banned_user :
        user = banned_entry.user
        if (user.name , user.discrimination) == (member_name,member_disc):
            await ctx.guild.unban(user)
            await ctx.send(member_name + "has been unbanned !")
            return
    await ctx.send(member+" was not found") 

#whois
@client.command(aliases=['user','info'])
@commands.has_permissions(kick_members=True)
async def whois(ctx,member : discord.Member):
    embed =discord.Embed(title =member.name , description =member.mention )
    embed.add_field(name = "ID" , value = member.id , inline = True)
    embed.set_thumbnail(url =member.avatar_url)
    embed.set_footer(icon_url= ctx.author.avatar_url ,text = f"used by{ctx.author.name}")
    await ctx.send(embed = embed)

#poll
@client.command(aliases = ['Poll'])
async def poll(ctx,*,message):
    channel = ctx.channel
    try :
        op1 , op2 = message.split("or")
        text = f"React with ✅ for {op1} or ❎ for {op2}"
    except:
        await channel.send("correct syntax: [choice1] or [choice2]")
        return

    embed = discord.Embed(title = 'Poll' , description = text )
    message_ = await channel.send(embed=embed)
    await message_.add_reaction('✅')     
    await message_.add_reaction('❎')    
    await ctx.message.delete()

#invite
@client.command(aliases = ["Invite","inv"])
async def invite(ctx):
    try:
        await ctx.send("https://discord.com/oauth2/authorize?client_id=796571765878423582&permissions=8&scope=bot")
    except:
        await ctx.author.send("https://discord.com/oauth2/authorize?client_id=796571765878423582&permissions=8&scope=bot")
    

client.run("Nzk2NTcxNzY1ODc4NDIzNTgy.X_Z3RA.KrC6vOaf8jXXNglgrPfZ049kOes") 
 