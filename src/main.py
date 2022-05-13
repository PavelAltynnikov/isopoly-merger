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

    legends_data = legend.parse_legends(legend.find_legends_data_path(isopoly_dir))
    result_path = os.path.join(isopoly_dir, "merge result")
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

    except legend.LegendsSourceFileNotFoundException as e:
        print(f"В папке не обнаружен файл-данных легенд изополей: {e.directory}")
    except legend.LegendsSourceFileIsEmptyException as e:
        print(f'Файл-данных легенд "{e.file_path}" пуст')
    except legend.LegendsSourceFileHasOneLegendException as e:
        print(
            f'Файл-данных легенд "{e.file_path}" содержит данные для одной легенды. '
            'Нет смысла дальше работать'
        )
    except legend.LegendNotFoundException as e:
        print(f'Для изополя "{e._isopoly_name}" не найдены данные в файле csv')
    except legend.ColorsDoNotMatchAreasException as e:
        print(
            f'Для изополя "{e.isopoly_name}" '
            'не совпадает количество цветов в легенде и количество площадей в файле csv\n'
            f'цвета: {e.colors}\n'  # тут надо попробовать преобразовать таплы в имена цветов
            f'числа: {e.numbers}'
        )


main()
input("Программа завершила свою работу. Нажмите любую клавишу для закрытия окна")
