from command import CommandMetaclass
import rich_click as click


class CommandBase(metaclass=CommandMetaclass):
    """Base Command Class"""
    ...


class Alpha(CommandBase):
    """
    Enable :point_right: [yellow]debug mode[/] :point_left:
    """
    XX: object = 1
    
    name = "Name"
    zxcv = "paramName"
    
    def xxx(self, mm):
        """xxx"""
        print("xxx")
        print(self.name)
        print("xxx")
    
    @staticmethod
    def sxxx(mm):
        """sxxx"""
        print("sxxx")
    
    @classmethod
    def cxxx(cls, mm):
        """cxxx"""
        print(cls.name)
        print("cxxx")
    
    @click.command()
    @click.option("--nn", help="nnnnnn")
    def yyy(self, nn) -> None:
        """yyy"""
        print(nn)
        print(self.name)
        print("yyy")
        return "yyy"
    
    @staticmethod
    @click.command()
    @click.option("--nn", help="nnnnnn")
    @click.option("--mm", help="mmmmmmmm")
    def syyy(nn, mm):
        """syyy"""
        print(nn)
        print(mm)
        print("syyy")
        return "syyy"
    
    @classmethod
    @click.command(name="cyyy")
    @click.option("--nn", help="nnnnnn")
    def cyyy(cls, nn):
        """cyyy"""
        print(nn)
        print("cyyy")
        return "cyyy"
    
    @click.option('-m', default="NAME", help="设置NAME")
    def set_name(self, m):
        """设置name"""
        print(self.nn)
        self.name = m
    
    @property
    def nn(self):
        return self.XX
    
    # @click.option('-n', default="XXXX", help="设置XXX")
    # @nn.setter
    # def nn(self, value):
    #     self.XX = value


class Beta(CommandBase):
    """
    Type of file to sync.
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    Sed sed mauris euismod, semper leo quis, sodales augue.
    Donec posuere nulla quis egestas ornare.
    Nam efficitur ex quis diam tempus, nec euismod diam consectetur.
    Etiam vitae nisi at odio hendrerit dictum in at dui.
    Aliquam nulla lacus, pellentesque id ultricies sit amet, mollis nec tellus.
    Aenean arcu justo, pellentesque viverra justo eget, tempus tincidunt lectus.
    Maecenas porttitor risus vitae libero dapibus ullamcorper.
    Cras faucibus euismod erat in porta.
    Phasellus cursus gravida ante vel aliquet.
    In accumsan enim nec ullamcorper gravida.
    Donec malesuada dui ac metus tristique cursus.
    Sed gravida condimentum fermentum.
    Ut sit amet nulla commodo, iaculis tellus vitae, accumsan enim.
    Curabitur mollis semper velit a suscipit.
    """
    
    def __init__(self):
        self.x = None
    
    @click.command()
    @click.option(
        "--input",
        help="Input [magenta bold]file[/]. [dim]\[default: a custom default][/]",
    )
    def red(self, input: str) -> None:
        """Do something blue"""
        print(input)
        print('Beta works as well!')
        print(self.x)
    
    @click.command(help="Input [magenta bold]file[/]. [dim]\[default: a custom default][/]")
    @click.option(
        "--input",
        help="Input [magenta bold]file[/]. [dim]\[default: a custom default][/]",
    )
    def xx(self, input):
        self.x = input


class Gamma(Alpha):
    """sub cmd"""
    
    def __init__(self):
        self.x = None
    
    @click.command()
    @click.option(
        "--input",
        help="Input [magenta bold]file[/]. [dim]\[default: a custom default][/]",
    )
    def red(self, input: str) -> None:
        """Do something blue"""
        print(input)
        print('Beta works as well!')
        print(self.x)
    
    @click.command(help="Input [magenta bold]file[/]. [dim]\[default: a custom default][/]")
    @click.option(
        "--input",
        help="Input [magenta bold]file[/]. [dim]\[default: a custom default][/]",
    )
    def xx(self, input):
        self.x = input


if __name__ == '__main__':
    CommandBase()
