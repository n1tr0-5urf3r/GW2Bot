import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from .exceptions import APIError

class CraftingMixin:
    @commands.group()
    async def crafting(self, ctx):
        """Crafting related commands"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @crafting.command(name="calc")
    @commands.cooldown(1, 10, BucketType.user)
    async def crafting_calc(self, ctx, *, item_name: str):
        user = ctx.author
        await ctx.send(item_name)
        item_doc = await self.itemname_to_id(
            ctx, item_name, user, group_duplicates=True)

        try:
            # Resolve the item to its recipe ID
            endpoint_recipe = 'recipes/'
            endpoint_search_output = "{0}search?output={1}".format(endpoint_recipe, item_doc["ids"][0])
            recipes = await self.call_api(endpoint_search_output)
        except APIError as e:
            return await self.error_handler(ctx, e)

        # For now only check the first recipe, dunno if there can more than one recipes per item
        recipe = recipes[0]

        # Get the item's recipe
        recipe_doc = await self.fetch_recipe(recipe)
        ingredients = recipe["ingredients"]

        for ingredient in recipe_doc["ingredients"]:
            ing_id = ingredient["item_id"]

        #for k,v in recipe_doc.items():
        #    await ctx.send("{0},{1}".format(k,v))



