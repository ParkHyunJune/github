# QuerySet API reference

## When QuerySets are evaluated

내부적으로 QuerySet은 실제로 데이터베이스에 도달하지 않고 구성, 필터링, 슬라이스 및 일반적으로 전달 될 수 있습니다. 쿼리 세트를 평가할 때까지 실제로 데이터베이스 활동이 발생하지 않습니다.

QuerySet은 반복 가능하며 처음 반복 할 때 QuerySet을 실행합니다. 예를 들어, 데이터베이스의 모든 항목의 제목을 인쇄합니다.

ex)

```
for e in Entry.objects.all():
    print(e.headline)
```


## Pickling QuerySets

QuerySet을 pickle하면 pickling 전에 메모리에 모든 결과가로드됩니다. pickling은 일반적으로 캐싱의 선구자로 사용되며 캐싱 된 쿼리 세트가 다시로드 될 때 결과가 이미 사용되고 사용할 준비가되기를 원합니다 (데이터베이스 읽기는 캐싱의 목적을 무의미한 시간이 걸릴 수 있습니다). 즉, 쿼리 집합을 실행 취소 할 때 현재 데이터베이스에있는 결과가 아닌 쿼리 된 결과가 포함됩니다.

```
>>> import pickle
>>> query = pickle.loads(s)     # Assuming 's' is the pickled string.
>>> qs = MyModel.objects.all()
>>> qs.query = query            # Restore the original 'query'.
```

## QuerySet API

### Methods that return new QuerySets

Django는 QuerySet에 의해 반환 된 결과의 유형이나 SQL 쿼리가 실행되는 방식을 수정하는 다양한 QuerySet 세분화 메소드를 제공합니다.

#### filter()

##### filter(**kwargs)

지정된 검색 매개 변수와 일치하는 객체가 포함 된 새 QuerySet을 반환합니다. 조회 매개 변수 (** kwargs)는 아래 필드 조회에 설명 된 형식이어야합니다. 여러 매개 변수는 기본 SQL 문에서 AND를 통해 조인됩니다. 더 복잡한 쿼리 (예 : OR 문을 사용하는 쿼리)를 실행해야하는 경우 Q 개체를 사용할 수 있습니다.

#### exclude()

##### exclude(**kwargs)

지정된 조회 매개 변수와 일치하지 않는 객체가 포함 된 새 QuerySet을 반환합니다. 조회 매개 변수 (** kwargs)는 아래 필드 조회에 설명 된 형식이어야합니다. 여러 매개 변수는 기본 SQL 문에서 AND를 통해 조인되며 모든 것은 NOT ()으로 묶입니다

```
Entry.objects.exclude(pub_date__gt=datetime.date(2005, 1, 3), headline='Hello')
```

#### order_by()

##### order_by(*fields)

기본적으로 QuerySet에 의해 반환 된 결과는 모델 메타의 정렬 옵션에 의해 주어진 순서 튜플에 의해 정렬됩니다. order_by 메소드를 사용하여 QuerySet 단위로이 값을 겹쳐 쓸 수 있습니다.

ex) 

```
Entry.objects.filter(pub_date__year=2005).order_by('-pub_date', 'headline')
```

#### reverse()

reverse () 메서드를 사용하여 쿼리 세트의 요소가 반환되는 순서를 바꿉니다. reverse ()를 다시 호출하면 순서가 정상 방향으로 복원됩니다.

ex)

```
my_queryset.reverse()[:5]
```

#### distinct()

##### distinct(*fields)

SQL 쿼리에서 SELECT DISTINCT를 사용하는 새 QuerySet을 반환합니다. 이렇게하면 조회 결과에서 중복 행이 제거됩니다. 기본적으로 QuerySet은 중복 행을 제거하지 않습니다. 실제로 Blog.objects.all ()과 같은 간단한 쿼리는 결과 행이 중복 될 가능성이 있기 때문에 거의 문제가되지 않습니다. 그러나 쿼리가 여러 테이블에 걸쳐있는 경우 QuerySet을 평가할 때 중복 결과를 얻을 수 있습니다. 그것은 distinct ()를 사용할 때입니다.

#### values()

##### values(*fields, **expressions)

iterable로 사용될 때 모델 인스턴스가 아닌 사전을 반환하는 QuerySet을 반환합니다. 각 사전은 모델 오브젝트의 속성 이름에 해당하는 키로 오브젝트를 나타냅니다.

ex)

```
# This list contains a Blog object.
>>> Blog.objects.filter(name__startswith='Beatles')
<QuerySet [<Blog: Beatles Blog>]>

# This list contains a dictionary.
>>> Blog.objects.filter(name__startswith='Beatles').values()
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>
```

#### datetimes()

##### datetimes(field_name, kind, order=’ASC’, tzinfo=None)

QuerySet의 내용 내에서 특정 종류의 모든 사용 가능한 날짜를 나타내는 datetime.datetime 개체의 목록으로 평가되는 QuerySet을 반환합니다. field_name은 모델의 DateTimeField 이름이어야합니다. 종류는 "년", "월", "일", "시간", "분"또는 "초"이어야합니다. 결과 목록의 각 datetime.datetime 객체는 주어진 유형으로 "잘립니다". order는 'ASC'로 기본값은 'ASC'또는 'DESC'여야합니다. 결과를 정렬하는 방법을 지정합니다. tzinfo는 잘라내 기 전에 datetime이 변환되는 시간대를 정의합니다. 사실 주어진 datetime은 사용중인 시간대에 따라 다른 표현을 갖습니다. 이 매개 변수는 datetime.tzinfo 객체 여야합니다. None이면 Django는 현재 시간대를 사용합니다. USE_TZ가 False이면 효과가 없습니다.

#### all()

현재의 QuerySet (또는 QuerySet 서브 클래스)의 복사본을 반환합니다. 이는 모델 매니저 또는 QuerySet을 전달하고 결과에 대해 추가 필터링을 수행하려는 상황에서 유용 할 수 있습니다. 두 객체 모두에서 all ()을 호출하면 작업 할 QuerySet을 확실히 갖게됩니다. QuerySet이 평가 될 때, 일반적으로 QuerySet은 결과를 캐시합니다. QuerySet을 평가 한 후 데이터베이스의 데이터가 변경된 경우 이전에 평가 된 QuerySet에서 all ()을 호출하여 동일한 쿼리에 대한 업데이트 된 결과를 가져올 수 있습니다.

## Methods that do not return QuerySets

#### get()

##### get(**kwargs)

지정된 참조 매개 변수와 일치하는 객체를 반환합니다.이 조회는 필드 조회에서 설명하는 형식이어야합니다. get ()은 둘 이상의 객체가 발견되면 MultipleObjectsReturned를 발생시킵니다. MultipleObjectsReturned 예외는 모델 클래스의 속성입니다. 지정된 매개 변수에 대해 개체를 찾을 수없는 경우 get ()은 DoesNotExist 예외를 발생시킵니다. 

#### create()

##### create(**kwargs)

객체를 작성해 한 번에 저장하는 편리한 메소드입니다. 

ex)

```
p = Person.objects.create(first_name="Bruce", last_name="Springsteen")
```

## Field lookups

필드 조회는 SQL WHERE 절의 meat를 지정하는 방법입니다. 그것들은 QuerySet 메소드 filter (), exclude () 및 get ()에 대한 키워드 인수로 지정됩니다. 

#### contains

ex)

```
Entry.objects.get(headline__contains='Lennon')
```



