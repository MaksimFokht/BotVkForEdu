# VkBotForEdu - Бот для сообщества ВК, который направлен для помощи старосте группы в её деятельности и не только.
***
.gitignore
=====================
bot_config.py - конфигурационный файл, который включает в себя:
  - Токены ВК сообщества для подключения бота.
  - ID Администратора и доверенных лиц.
  - Строка к подключению к БД.
  - Название таблицы отчета.
  - Текстовая справка о боте.
***
Как запустить
=====================
Для начала понадобится ВК сообщество с включенным Callback API, где необходимо будет получить токены для привязки бота. После этого создать конфигурационный файл и добавить туда токены под свое сообщество. Заливаем бота на любой хостинг(я использовал Heroku) настраиваем его и связываем с группой ВК.
***
Команды бота
=====================
  - **.skip** - система добавления и просмотра пропущенных часов студента 
  - **.exam** - выводит список экзаменов/зачетов 
  - **.ci** - выводит в консоль информацию о беседе 
  - **.ca** <.команда> - добавляет в БД команду 
  - **.enable** <.команда> - включает команду 
  - **.disable** <.команда> - выключает команду 
  - **.ea** <название_дисциплины> <тип_аттестации> <дата> - добавляет экзамен/зачет в список 
  - **.test** - проверка работоспособности бота 
