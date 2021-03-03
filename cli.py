import asyncio
from functools import wraps
import click
import json

from sd_alert_pipe.lasair import LasairService
from sd_alert_pipe.common import gather_data


def coro(f):
    """
    Wrapper to turn click commands into coroutines
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    pass


@cli.command()
@coro
@click.argument('name')
async def lasair_query(name: str) -> None:
    ls = LasairService()
    results = await ls.stored_query(name)
    if results.get('error'):
        click.echo(results['error'])
        return 1
    click.echo('{:<13} {:<20} {:<12} {:<12} {:<9} {:<3}'.format('Name', 'UTC', 'Rising', 'Fading', 'Age', 'Class.'))
    for result in results['digest']:
        click.echo('{:<13} {:<20} {:<12} {:<12} {:<9} {:<3}'.format(
            result['objectId'], result['UTC'], result['rising'],
            result['fading'], '{:1.5f}'.format(result['age']), result['sherlock']
        ))


@cli.command()
@coro
@click.argument('objectid')
async def fetch_object(objectid: str) -> None:
    results = await gather_data(objectid)
    click.echo(json.dumps(results.dict(), indent=2))

if __name__ == '__main__':
    cli()
