"""
support register unlimited extensible command line tool
"""
import functools
import inspect
import typing
from functools import partial

import typing_extensions
from typing import Dict
from inspect import Parameter

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
CLASS_INSTANCE = "__instance__"


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


def get_typed_annotation(param: inspect.Parameter, globalns: typing.Dict[str, typing.Any]) -> typing.Any:
    annotation = param.annotation
    if isinstance(annotation, str):
        annotation = typing.ForwardRef(annotation)
        annotation = typing.evaluate_forwardref(annotation, globalns, globalns)
    return annotation


def get_typed_signature(call: typing.Callable[..., typing.Any], follow_wrapped: bool = True) -> inspect.Signature:
    signature = inspect.signature(call, follow_wrapped=follow_wrapped)
    globalns = getattr(call, "__globals__", {})
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param, globalns),
        )
        for param in signature.parameters.values()
    ]
    typed_signature = inspect.Signature(typed_params)
    return typed_signature


class CommandMetaclass(type):
    @staticmethod
    def command_wrapper(attr_name, origin_attr_value, klass):
        """command_wrapper"""
        if isinstance(origin_attr_value, staticmethod) or isinstance(origin_attr_value, classmethod):
            attr_value = origin_attr_value.__func__
        else:
            attr_value = origin_attr_value
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
                if isinstance(origin_attr_value, classmethod):
                    signature_attr_value = partial(attr_value, klass)
                elif not isinstance(origin_attr_value, staticmethod):
                    signature_attr_value = partial(attr_value, klass)
                else:
                    signature_attr_value = attr_value
                
                endpoint_signature = get_typed_signature(signature_attr_value, False)
                signature_params = endpoint_signature.parameters
                
                attr = click.command(name=attr_name, help=attr_value.__doc__)(attr_value)
                for k, v in signature_params.items():
                    param_default = None if v.default == Parameter.empty else v.default
                    param_type = any if v.annotation == Parameter.empty else v.annotation.__origin__ if hasattr(v.annotation, '__origin__') else v.annotation
                    param_doc = "" if v.annotation == Parameter.empty else " ".join(v.annotation.__metadata__) if hasattr(v.annotation, '__metadata__') else v.annotation
                    attr = click.option(f"--{k}", help=f"{param_doc}  default: `{param_default}`", required=False if param_default else True, type=param_type, default=param_default)(attr)
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
        klass.__init__(klass)
        
        def cli(*args, **options):
            for option_callback in getattr(klass, CLASS_GROUP_OPTION_CALLBACKS):
                option_callback(klass, **options)
        
        setattr(klass, CLASS_GROUP_ATTR_NAME, click.group(name=klass.__name__.lower(), help=klass.__doc__)(cli))
        klass_command_group: click.Group = getattr(klass, CLASS_GROUP_ATTR_NAME)
        """loop through all attr on class initializers"""
        for attr_name, attr_value in dct.items():
            attr = getattr(klass, attr_name)
            if callable(attr):
                if attr_name.startswith("_"):
                    if not isinstance(attr_value, staticmethod) and not isinstance(attr_value, classmethod):
                        setattr(klass, attr_name, partial(attr_value, klass))
                    continue
                
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
                if attr_name.startswith("_"):
                    continue
                
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
