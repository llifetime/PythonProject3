# test/conftest.py
import coverage


def pytest_sessionstart(session):
    """Запускается в начале сессии тестирования"""
    print("\n🚀 Начало тестирования с отсчетом покрытия")

    # Инициализация coverage
    session.config.cov = coverage.Coverage(
        source=['src'],
        omit=['*test*', '*__pycache__*']
    )
    session.config.cov.start()


def pytest_sessionfinish(session, exitstatus):
    """Запускается в конце сессии тестирования"""
    print("\n📊 Завершение тестирования - генерация отчетов...")

    # Останавливаем coverage
    session.config.cov.stop()
    session.config.cov.save()

    # Выводим отчет
    print("\n" + "=" * 50)
    print("ОТЧЕТ О ПОКРЫТИИ ТЕСТАМИ")
    print("=" * 50)

    session.config.cov.report(show_missing=True)

    # Генерируем дополнительные отчеты
    session.config.cov.html_report(directory='htmlcov')
    session.config.cov.xml_report(outfile='coverage.xml')

    print("\n📁 HTML отчет: htmlcov/index.html")
    print("📁 XML отчет: coverage.xml")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Добавляем информацию в терминальный вывод"""
    terminalreporter.section("Coverage Summary")
    # Можно добавить дополнительную статистику здесь
