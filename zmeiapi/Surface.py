__version__ = "0.0.1"
__author__ = "Vlad Romanenko"


from abc import ABC, abstractmethod


class Surface:
    instances = []

    @classmethod
    def write_instances_to_file(cls, filename):
        """
        Class method to write all instances into the file
        :param filename: name of the file
        :type filename: str
        :return: None
        :rtype: None
        """
        with open(filename, 'w') as file:
            for instance in cls.instances:
                file.writelines(instance.lines)

    def __init__(self):
        self.__class__.instances.append(self)

    class AbstractSurface(ABC):
        @abstractmethod
        def __init__(self, name: str, params: list[float | int]):
            self.name = name
            self.params = params
            self.line = f''

            self._check_surf_parameters()

        def __str__(self):
            return self.line

        @abstractmethod
        def _check_surf_parameters(self):
            pass

        def _create_lines(self, surf_type: str):
            self.line += f'{self.name:15} {surf_type:15} '
            for param in self.params:
                self.line += f'{param:10} '
            self.line += f'\n'
            pass

    class Cylz(AbstractSurface):
        def __init__(self, name: str, params: list[float | int]):
            super().__init__(name, params)
            super()._create_lines('cylz')

        def _check_surf_parameters(self):
            if len(self.params) != 3 or len(self.params) != 5:
                assert AttributeError('Wrong parameters number, loot at the class description')
            pass


if __name__ == '__main__':
    surf = Surface().Cylz('surfc', [1, 3.0, 1.0])
    surf1 = Surface().Cylz('surfc', [1, 3.0, 1.0])
    print(surf)
    print(Surface.instances)
