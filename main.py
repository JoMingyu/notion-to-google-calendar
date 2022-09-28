import json
from dataclasses import dataclass
from typing import List

import arrow
from arrow import Arrow
from notion_client import Client

notion = Client(auth="...")


@dataclass
class Schedule:
    datetime: Arrow
    place: str
    id: str
    partners: List[str]


# data = notion.databases.query('0f63dbfa-dd64-4d81-bdb4-94b435a627ba')
data = json.loads(open('example.json').read())

schedules = []

for x in data['results'][:3]:
    properties = x['properties']
    schedule = Schedule(
        datetime=arrow.get(properties['날짜']['date']['start']),
        place=properties['장소 (datafield)']['rollup']['array'][0]['title'][0]['text']['content'],
        id=x['id'],
        partners=[n['name'] for n in properties['동행']['multi_select']]
    )
    schedules.append(schedule)


for schedule in schedules:
    print(schedule)


# - snapshot끼리 비교함. 비교기준은 datetime
# - 삭제된 것이 있는 경우 : 해당 시각의 schedule을 그대로 따라가서 삭제
# - 추가된 것이 있는 경우 : 해당 시각에 schedule을 추가
# - 수정된 것이 있는 경우 : 해당 시각의 schedule을 update
# last edited time은 유의미한가? -> 모르겠음
