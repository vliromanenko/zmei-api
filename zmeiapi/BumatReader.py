__version__ = '0.0.1'
__author__ = 'Vlad Romanenko'


import os
import glob
from BumatObject import BumatMaterialObject
from Logger import logger


class BumatReader:
    def __init__(self, folder_path):
        self.bumat_filenames = glob.glob(os.path.join(folder_path, '*.bumat*'))
        if not self.bumat_filenames:
            logger.error(f"Bumat files not found")
            raise RuntimeError(f"Bumat files not found")
        self.bumat_filenames = sorted(self.bumat_filenames, key=self.__bumat_key_val)

        self.bumat_mat_dict = {}
        for bumat_file in self.bumat_filenames:
            bumat_file_index = self.__bumat_key_val(bumat_file)
            self.bumat_mat_dict[bumat_file_index] = self._read_bumat_file(bumat_file)

    @staticmethod
    def __bumat_key_val(string: str) -> int:
        val = int(string.split('bumat')[-1])
        return val

    @staticmethod
    def _get_burnup(bumat_lines):
        burnup = None
        burnup_days = None
        for line in bumat_lines:
            if line.startswith("% Material compositions"):
                # splitting the line by '(' symbol
                # % Material compositions (0.00 MWd/kgU / 0.14 days)
                _splited_line_with_burnup = line.split('(')[1]
                _splited_burnups = _splited_line_with_burnup.split()
                burnup = float(_splited_burnups[0])
                burnup_days = float(_splited_burnups[-2])
                break

        if (burnup is None) or (burnup_days is None):
            logger.error(f"Burnup or burnup_days value not found")
            raise RuntimeError(f"Burnup or burnup_days value not found")
        return burnup, burnup_days

    @staticmethod
    def _get_mat_indexes(bumat_lines: list[str]) -> list[int]:
        # get indexes (lines numbers) for all start lines for each material
        indexes = [i for i, line in enumerate(bumat_lines) if line.startswith("mat  ")]
        indexes.append(len(bumat_lines))
        return indexes

    def _read_bumat_file(self, filename: str) -> list[BumatMaterialObject]:
        with open(filename, 'r') as file:
            bumat_lines = file.readlines()

        burnup, burnup_days = self._get_burnup(bumat_lines)
        # print(burnup, burnup_days)

        mat_indexes = self._get_mat_indexes(bumat_lines)
        # print(mat_indexes[-1])
        # print(bumat_lines[mat_indexes[-1]])

        bumat_material_objects_list = []

        for ind_num, ind in enumerate(mat_indexes):
            if ind == mat_indexes[-1]:
                break
            nuclides = []
            concentrations = []

            _f_name_line = bumat_lines[ind]
            # print(_f_name_line, ind)
            material_name = _f_name_line.split()[1].split('pp')[0]
            concentrations_sum = float(_f_name_line.split()[2])
            vol = float(_f_name_line.split()[4])

            for nuclide_counter in range(ind + 1, mat_indexes[ind_num + 1]):
                _l = bumat_lines[nuclide_counter].split()
                nuclides.append(_l[0].split('.'[0])[0])
                concentrations.append(float(_l[1]))
            bumat_material_object = BumatMaterialObject(
                material_name, burnup, burnup_days, concentrations_sum, vol, nuclides, concentrations
            )
            bumat_material_objects_list.append(bumat_material_object)
        return bumat_material_objects_list


if __name__ == '__main__':
    path = '/home/vlad/Serpent/Calculation/22AU_312/22AU_b'
    b = BumatReader(path)
    print(b.bumat_mat_dict[150][-1])
