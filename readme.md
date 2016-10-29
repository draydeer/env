# Env

Агент доставки конфигураций локальному приложению.

### Общие сведения

Агент предоставляет возможность доставки документов конфигураций конечному локальному приложению, их сборку из удаленных источников данных и дальнейшей периодической синхронизации изменений.
Итоговый документ конфигурации представляет собой контейнер пар вида "ключ-значение", где значением может быть как некий примитив, так и другой вложенный контейнер.

### Режимы работы

Агент поддерживает несколько режимов работы сервиса:

*master* - по запросу выполняет сборку документа из удаленных источников данных, передает, кэширует в течение определенного срока и, затем, удаляет их кэша до следующего заспроса.

*client* - по запросу передает собранный документ из *master*-узла, кеширует его и, затем, периодически синхронизирует его состояние из *master*-узла.

*keeper* - по запросу выполняет сборку документа из удаленных источников данных, передает, кеширует его и, затем, периодически синхронизирует его состояние из удаленных источников данных.