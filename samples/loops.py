from disnake.ext import tasks, commands
import asyncio

def __init__(bot: commands.Bot):
    """ Initialize events """
    # member_join(bot)
    # member_leave(bot)
    # guild_join(bot)
    # message_send(bot)
    # message_edit(bot)
    # message_delete(bot)
    load_task_manager(bot)



def load_task_manager(bot):
    @tasks.loop(seconds=10)
    async def find_new_poll_routines_task() -> None:
        execute_poll_routines.count
        print('task manager')
        execute_poll_routines.stop()
        print('task canceled')
        await asyncio.sleep(1)
        # await asyncio.sleep(10)
        print(execute_poll_routines.count)
        execute_poll_routines.change_interval(seconds=execute_poll_routines.count)
        execute_poll_routines.start()
    # find_new_poll_routines_task.start()

    @tasks.loop(seconds=1.0)
    async def execute_poll_routines() -> None:
        print('poll')
