# arhivach-tools
Выгрузка постов из [архива](http://arhivach.ng) тредов 2ch.hk

## Install
```bash
pip install -r requirements.txt
```
## Using
```bash
python scraping.py -h
```
```bash
usage: scraping.py [-h] [-U URL] [-E END] [-S START] [-D STEP] [-T THREAD_COUNT] [-O OUT]

optional arguments:
  -h, --help            show this help message and exit
  -U URL, --url URL     arhivach url
  -E END, --end END     end post id
  -S START, --start START
                        start post id
  -D STEP, --step STEP  iteration step
  -T THREAD_COUNT, --thread_count THREAD_COUNT
                        count of worker threads
  -O OUT, --out OUT     output file
```

## Output .csv format
Выходной файл имеет следующую структуру:

| post_id | post_datetime | post_tags | poster_name | reply_to | post_text |
| ------- |:---------------------| :----------:| :-------------: |:-------------| :-----|
| 5906244 |	28/10/19 Пнд 23:19:22 | ['2ch.hk'] | Аноним | [] | Вернулась бывшая спустя 5 месяцев. Съезжаемся. |
| 5906254 | 28/10/19 Пнд 23:21:52 | ['2ch.hk'] | Аноним | ['5906244'] | >>5906244 Помянем. |

* `post_id` - идентификатор поста
* `post_datetime` - дата и время поста (у старых постов есть только дата)
* `post_tags` - теги треда, в котором находится пост
* `poster_name` - имя автора поста
* `reply_to` - идентификаторы постов, на которые отвечает данный пост
* `post_text` - текст поста