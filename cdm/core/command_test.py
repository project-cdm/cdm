from command import CommandMetaclass
import rich_click as click


class CommandBase(metaclass=CommandMetaclass):
    """Base Command Class"""  # test success
    ...


from typing_extensions import Annotated

Meter = Annotated[float, "米"]


class Alpha(CommandBase):
    """
    Enable :point_right: [yellow]debug mode[/] :point_left:
    """
    # test success
    
    XX: object = 1
    
    name = "DefaultName"
    zxcv: Annotated[str, "属性注释"] = "默认值"
    
    @click.option('-v', help="verbose", count=True)  # test success
    @click.option('-m', default="NEW_NAME", help="设置NAME")  # test success
    def set_name(self, m, v):  # test success
        """设置name"""
        self.name = m
        print(self.name)
        print(m)
        print(v)
        print("设置name")
    
    def xxx1(self, mm: Meter = 1):  # test success
        """xxx1"""
        print(mm)
        print(self.name)
        print("xxx1")
    
    def xxx2(self, mm: Meter):  # test success
        """xxx2"""
        print(mm)
        print(self.name)
        print("xxx2")
    
    @staticmethod
    def sxxx1(mm: Annotated[int, "静态方法"]):  # test success
        """sxxx1"""
        print(mm)
        print("sxxx1")
    
    @staticmethod
    def sxxx2(mm: Annotated[int, "静态方法"] = 1):  # test success
        """sxxx2"""
        print(mm)
        print("sxxx2")
    
    @classmethod
    def cxxx1(cls, mm: Annotated[str, "类方法"] = "defaultValue"):  # test success
        """cxxx1"""
        print(cls.name)
        print(mm)
        print("cxxx1")
    
    @classmethod
    def cxxx2(cls, mm: Annotated[str, "类方法"]):  # test success
        """cxxx2"""
        print(cls.name)
        print(mm)
        print("cxxx2")
    
    @click.command()
    @click.option("--nn", help="nnnnnn")
    def yyy(self, nn):  # test success
        """yyy"""
        print(nn)
        print(self.name)
        print("yyy")
    
    @staticmethod
    @click.command()
    @click.option("--nn", help="nnnnnn")
    @click.option("--mm", help="mmmmmmmm")
    def syyy(nn, mm):  # test success
        """syyy"""
        print(nn)
        print(mm)
        print("syyy")
    
    @classmethod
    @click.command(name="cyyy")
    @click.option("--nn", help="nnnnnn")
    def cyyy(cls, nn):  # test success
        """cyyy"""
        print(nn)
        print("cyyy")
    
    @property
    def nn(self):
        return self.XX


class Beta(Alpha):
    """
    sub cmd \r\n
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
    
    # test success
    
    def __init__(self):  # test success
        self.x = 'DefaultX'
    
    @click.command()
    @click.option(
        "--input",
        help="Input [magenta bold]file[/]. [dim]\[default: a custom default][/]",
    )
    def call_other(self, input: str):  # test success
        """call_other"""
        print(self.x)
        self.x = input
        print(self.x)
        self._syy(self.x)
        print(self.x)
        self._cyy(self.x)
        print(self.x)
        self._yyy(self.x)
        print(self.x)
        print("call_other")
    
    def call_other1(self, input: Annotated[str, "输入"]):  # test success
        """call_other1"""
        print(self.x)
        self.x = input
        print(self.x)
        self._syy(self.x)
        print(self.x)
        self._cyy(self.x)
        print(self.x)
        self._yyy(self.x)
        print(self.x)
        print("call_other1")
    
    @classmethod
    def ccall_other(cls, input: Annotated[str, "输入"] = 1):  # test success
        """ccall_other"""
        self = cls
        print(self.x)
        self.x = input
        print(self.x)
        self._syy(self.x)
        print(self.x)
        self._cyy(self.x)
        print(self.x)
        self._yyy(self.x)
        print(self.x)
        print("ccall_other")
    
    @classmethod
    def scall_other(cls, input: str):  # test success
        """scall_other"""
        self = cls
        print(self.x)
        self.x = input
        print(self.x)
        self._syy(self.x)
        print(self.x)
        self._cyy(self.x)
        print(self.x)
        self._yyy(self.x)
        print(self.x)
        print("scall_other")
    
    def call_other_cls(self):  # test success
        """
        call_other_cls
        :return:
        """
        print(Alpha.name)
        print("call_other_cls")
    
    @staticmethod
    def _syy(input):  # test success
        self = Beta
        print(f"_syy::{self},input::{input}")
        self.x = f"{input},{'_syy'}"
    
    @classmethod
    def _cyy(cls, input):  # test success
        self = cls
        print(f"_cyy::{self},input::{input}")
        self.x = f"{input},{'_cyy'}"
    
    def _yyy(self, input):  # test success
        self = self
        print(f"_yyy::{self},input::{input}")
        self.x = f"{input},{'_yyy'}"


if __name__ == '__main__':
    CommandBase()
