# Производит отправку/удаление файлов на Яндекс Диск.


**Создать приложение и получить токен:**
```
https://yandex.ru/dev/disk/api/concepts/quickstart.html#quickstart__debug-token
```

**Получение токена:**

```
https://oauth.yandex.ru/authorize?response_type=token&client_id=<идентификатор_приложения>
```
Тут appid: ```https://oauth.yandex.ru```

На Яндекс.Диске создать папку **/backup**

В **core/api/yandex.py** добавить полученный токен

Далее выполнить:

```shell
chmod +x backup
```
```shell
sudo ln -s $(pwd)/backup /usr/local/bin
```

Аргументы скрипта: 

* **--path** пусть до каталога/файла
* **--action** **delete** или **upload**

Пример использования:

```shell
backup --path /home/beloslav/projects/backup-ya/ --action upload
```