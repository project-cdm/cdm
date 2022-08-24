"""
support register unlimited extensible command line tool
"""
from typing import Dict

try:
    import rich_click as click
    
    click.rich_click.SHOW_ARGUMENTS = False  # Show positional arguments
    click.rich_click.SHOW_METAVARS_COLUMN = False  # Show a column with the option metavar (eg. INTEGER)
    click.rich_click.APPEND_METAVARS_HELP = True  # Append metavar (eg. [TEXT]) after the help text
    click.rich_click.GROUP_ARGUMENTS_OPTIONS = False  # Show arguments with options instead of in own panel
    click.rich_click.OPTION_ENVVAR_FIRST = False  # Show env vars before option help text instead of avert
    click.rich_click.USE_MARKDOWN = False  # Parse help strings as markdown
    click.rich_click.USE_MARKDOWN_EMOJI = True  # Parse emoji codes in markdown :smile:
    click.rich_click.USE_RICH_MARKUP = True  # Parse help strings for rich markup (eg. [red]my text[/])
    click.rich_click.USE_CLICK_SHORT_HELP = False  # Use click's default function to truncate help text
except ImportError as e:
    import click

CLASS_GROUP_ATTR_NAME = "__command_group__"
CLASS_GROUP_OPTION_CALLBACKS = "__option_callbacks__"


class CommandInstance:
    """Command  perform instance"""
    klass = None
    command = None
    origin = None
    
    def __init__(self, command, origin, klass):
        self.command = command
        self.klass = klass
        self.origin = origin
    
    def __call__(self, *args, **kwargs):
        if isinstance(self.origin, staticmethod):
            return self.command(*args, **kwargs)
        return self.command(self.klass, *args, **kwargs)


class CommandMetaclass(type):
    @staticmethod
    def command_wrapper(attr_name, attr_value, klass):
        """command_wrapper"""
        if isinstance(attr_value, staticmethod) or isinstance(attr_value, classmethod):
            attr_value = attr_value.__func__
        if isinstance(attr_value, click.Command):
            """if the function body is packaged by Command"""
            return attr_value
        else:
            """if __click_params__ is present then the function is an option"""
            if hasattr(attr_value, "__click_params__"):
                klass_command_group: click.Group = getattr(klass, CLASS_GROUP_ATTR_NAME)
                klass_command_group.params.extend(getattr(attr_value, "__click_params__"))
                getattr(klass, CLASS_GROUP_OPTION_CALLBACKS).add(attr_value)
                return None
            else:
                attr = click.command(name=attr_name, help=attr_value.__doc__)(attr_value)
                setattr(klass, attr_name, attr)
                return attr
    
    def __call__(cls, *args, **kwargs):
        cls.command_set(cls)
        return getattr(cls, CLASS_GROUP_ATTR_NAME)()
    
    @staticmethod
    def command_set(cls):
        """
        Recursive setting command
        :param cls:
        :return:
        """
        command_group: click.Group = getattr(cls, CLASS_GROUP_ATTR_NAME)
        for sub_cls in cls.__subclasses__():
            cls.command_set(sub_cls)
            sub_command = getattr(sub_cls, CLASS_GROUP_ATTR_NAME)
            command_group.add_command(sub_command, name=sub_command.name)
    
    @staticmethod
    def __new__(mcs, name, bases, dct: Dict[str, any]):
        """metaclass for command """
        
        """create klass and create group"""
        klass = super().__new__(mcs, name, bases, dct)
        setattr(klass, CLASS_GROUP_OPTION_CALLBACKS, set())
        
        def cli(*args, **options):
            for option_callback in getattr(klass, CLASS_GROUP_OPTION_CALLBACKS):
                option_callback(klass, **options)
        
        setattr(klass, CLASS_GROUP_ATTR_NAME, click.group(name=klass.__name__.lower(), help=klass.__doc__)(cli))
        klass_command_group: click.Group = getattr(klass, CLASS_GROUP_ATTR_NAME)
        """loop through all attr on class initializers"""
        for attr_name, attr_value in dct.items():
            if attr_name.startswith("_"):
                continue
            attr = getattr(klass, attr_name)
            if callable(attr):
                if not isinstance(attr, click.Command):
                    attr = mcs.command_wrapper(attr_name, attr_value, klass)
                    if not attr:
                        continue
                if not isinstance(attr.callback, CommandInstance):
                    """the top class to implement this"""
                    attr.callback = CommandInstance(attr.callback, attr_value, klass)
                else:
                    """this is a subclass function, copy it and replace the klass"""
                    setattr(klass, attr_name, attr)
                    getattr(klass, attr_name).callback.klass = klass
                
                """inject the replacement object"""
                klass_command_group.add_command(attr, attr_name)
            else:
                """if it's not a callable"""
                
                def callback(ctx, param, value: bool, option_name=attr_name) -> None:
                    if not value or ctx.resilient_parsing:
                        return
                    click.echo(getattr(klass(), option_name), ctx.color)
                    ctx.exit()
                
                klass_command_group.params.append(
                    click.Option(param_decls=(f"--{attr_name}",),
                                 help=attr_name,
                                 is_flag=True,
                                 expose_value=False,
                                 is_eager=True,
                                 callback=callback,
                                 ))
        return klass
