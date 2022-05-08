import os
import PIL
import source
import legend
from isopoly import Isopoly, MergedIsopoly


def main():
    print("Выберите папку с изополями армирования")
    isopoly_dir = source.get_pictures_dir()
    if not isopoly_dir:
        print("Вы ничего не выбрали")
        return
    print(f"Вы выбрали папку {isopoly_dir}")

    legends_data = source.parse_legends(isopoly_dir)
    if not legends_data:
        print("В папке не обнаружен файл данными о легендах изополей")
        return

    if len(legends_data) == 1:
        print("В файле данных одна легенда. Нет смысла дальше работать")
        return

    result_path = os.path.join(isopoly_dir, "result")
    source.create_dir(result_path)

    isopolies = [
        Isopoly(PIL.Image.open(os.path.join(isopoly_dir, file_name)))
        for file_name in os.listdir(isopoly_dir)
        if file_name.endswith("png")
    ]

    if not isopolies:
        print(f'Не удалось найти ни одного изополя. Проверьте указанную папку "{isopoly_dir}"')
        return

    try:

        for isopoly in isopolies:
            isopoly.set_data_into_legend(legends_data)
            isopoly.fill_legend()

        merged_legend = sum([isopoly._legend for isopoly in isopolies])

        merged_isopoly = MergedIsopoly(isopolies[0].size, merged_legend, isopolies)
        merged_isopoly.fill()
        merged_isopoly.save(result_path)
        print(f"Изополе сформировано и сохранено. Результат находится тут: {result_path}")
        merged_isopoly.show()

    except legend.LegendNotFoundException as e:
        print(f'Для изополя "{e._isopoly_name}" не найдены данные в файле csv')
    except legend.ColorsDoNotMatchAreasException as e:
        print(
            f'Для изополя "{e._isopoly_name}" '
            'не совпадает количество цветов в легенде и количество площадей в файле csv\n'
            f'цвета: {e._colors}\n'  # тут надо попрбовать преобразовать таплы в имена цветов
            f'числа: {e._numbers}'
        )


main()
input("Программа завершила свою работу. Нажмите любую клавишу для закрытия окна")
