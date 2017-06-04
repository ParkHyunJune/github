# Django Models

Django에서 Model은 데이타 서비스를 제공하는 Layer이다. Django의 Model은 각 Django App안에 기본적으로 생성되는 models.py 모듈 안에 정의하게 된다. models.py 모듈 안에 하나 이상의 모델 클래스를 정의할 수 있으며, 하나의 모델 클래스는 데이타베이스에서 하나의 테이블에 해당된다.

> 모델 클래스는 필드를 정의하기 위해 인스턴스 변수가 아닌 클래스 변수를 사용하는데, 이는 그 변수가 테이블 필드의 내용을 갖는 것이 아니라, 테이블의 컬럼 메타 데이타를 정의하는 것이기 때문이다. 필드를 정의하는 각각의 클래스 변수는 models.CharField(), models,IntegerField(), models.DateTimeField(), models.TextField() 등의 각 필드 타입에 맞는 Field 클래스 객체를 생성하여 할당한다. Field 클래스는 여러 종류가 있는데, 생성자 호출시 필요한 옵션들을 지정할 수 있다. 각 Field 클래스마다 반드시 지정해야 주어야 하는 옵션이 있을 수 있는데, 예를 들어 CharField (와 그 서브클래스들)은 필드의 최대 길이를 나타내는 max_length를 항상 지정해 주어야 한다.

## Field type

모델의 필드에는 다양한 타입들이 있는데, 모든 필드 타입 클래스들은 추상클래스인 "Field" 클래스의 파생클래스들이다.


|Field Type   | 내용 |
|---|---|
|CharField   |	제한된 문자열 필드 타입. 최대 길이를 max_length 옵션에 지정해야 한다. 문자열의 특별한 용도에 따라 CharField의 파생클래스로서, 이메일 주소를 체크를 하는 EmailField, IP 주소를 체크를 하는 GenericIPAddressField, 콤마로 정수를 분리한 CommaSeparatedIntegerField, 특정 폴더의 파일 패스를 표현하는 FilePathField, URL을 표현하는 URLField 등이 있다.   |
|TextField  |	대용량 문자열을 갖는 필드   |
|IntegerField   |	32 비트 정수형 필드. 정수 사이즈에 따라 BigIntegerField, SmallIntegerField 을 사용할 수도 있다.   |
|BooleanField   |true/false 필드. Null 을 허용하기 위해서는 NullBooleanField를 사용한다.|
|DateTimeField   |	날짜와 시간을 갖는 필드. 날짜만 가질 경우는 DateField, 시간만 가질 경우는 TimeField를 사용한다.   |
|DecimalField   |	소숫점을 갖는 decimal 필드   |
|BinaryField   |	바이너리 데이타를 저장하는 필드   |
|FileField   |파일 업로드 필드   |
|ImageField   |FileField의 파생클래스로서 이미지 파일인지 체크한다.   |
|UUIDField   |	GUID (UUID)를 저장하는 필드   |


## Field option

모델의 필드는 필드 타입에 따라 여러 옵션(혹은 Argument)를 가질 수 있다. 예를 들어, CharField는 문자열 최대 길이를 의미하는 max_length 라는 옵션을 갖는다. 필드 옵션을 일반적으로 생성자에서 Argument로 지정한다. 

|필드 옵션   | 내용  |
|:-:|---|
|null (Field.null)   |null=True 이면, Empty 값을 DB에 NULL로 저장한다. DB에서 Null이 허용된다. 예: models.IntegerField(null=True)   |
|blank (Field.blank)   |blank=False 이면, 필드가 Required 필드이다. blank=True 이면, Optional 필드이다. 예: models.DateTimeField(blank=True)   |
|primary_key (Field.primary_key)   |해당 필드가 Primary Key임을 표시한다. 예: models.CharField(max_length=10, primary_key=True)   |
|unique (Field.unique)   |	해당 필드가 테이블에서 Unique함을 표시한다. 해당 컬럼에 대해 Unique Index를 생성한다. 예: models.IntegerField(unique=True)   |
|default (Field.default)   |	필드의 디폴트값을 지정한다. 예: models.CharField(max_length=2, default="WA")   |
|db_column (Field.db_column)   |컬럼명은 디폴트로 필드명을 사용하는데, 만약 다르게 쓸 경우 지정한다.   |

### Primary key

primary_key
값이 True 이면, 해당 필드를 모델의 primary key 로 정의한다.

기본적으로 Django는 별도로 지정하지 않는 경우, "id"라는 IntegerField 하나를 모델에 자동으로 추가하고, 그 필드에 "primary_key=True" 옵션을 설정한다. 자동으로 생성되지 않도록 하고 싶다면, 원하는 필드에 primary_key=True 옵션을 주면 된다.

*주의* 

**기존의 모델 객체에 primary key 필드값을 변경하고 저장하는 경우, 기존 모델 객체의 primary key 필드값이 바뀌는 것이 아니라, 새로운 모델 객체가 생성된다. 물론 기존의 모델객체는 DB상에서 지워지지 않않는다.**

## Relationships

Django는 3가지 대표적인 데이터베이스 관계 형태(일대다, 다대다, 일대일)를 제공한다.

### Many-to-one relationships

일대다 관계를 정의하려면 django.db.models.ForeignKey 클래스를 이용하여 필드를 선언하면 된다.

ForeignKey 필드 선언시에 관계를 맺을 모델 클래스를 인자로 넘겨주어야 한다.

소문자화한 모델의 이름을 필드 이름으로 사용하는것이 일반적이지만, 꼭 그래야만 하는 것은 아니다.

### Many-to-many relationships

다대다 관계를 선언할때는 ManyToManyField를 사용한다. ForeignKey 필드와 마찬가지로 관계를 가지는 모델 클래스를 첫번째 인자로 받는다.

ForeignKey 필드와 마찬가지로 재귀적인 관계를 선언할 수 있으며, 인자로 클래스 대신 클래스 이름을 전달할 수도 있다.

ManyToManyField는 관계를 가지는 두 모델 클래스 중에 한쪽에만 선언하면 된다. 

### Extra fields on many-to-many relationships

다대다 관계를 가지는 두 개의 모델 이외에 두 모델의 관계와 추가 데이터를 저장할 또다른 모델이 필요하다. 이를 중간(intermediate) 모델이라고 한다. 중간모델은 관계를 가지는 두 모델에 대한 ForeignKey 필드를 선언하고 추가적인 필드를 선언하면 된다.

### One-to-one relationships

일대일 관계를 정의하려면, OneToOneField를 이용하면 된다. 다른 관계 필드와 마찬가지로 모델 클래스의 어트리뷰트로 선언하면 된다. 

일대일 관계는 다른 모델을 확장하여 새로운 모델을 만드는 경우 유용하게 사용될 수 있다.

OneToOneField는 관계를 맺는 모델 클래스를 첫번째 인자로 받는다.

## Meta options

모델클래스 내부에 Meta 라는 이름의 클래스 선언해서 모델에 메타데이터를 추가할 수 있다.

ex) 


```
from django.db import models

class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"
```


"모델 메타데이터"란 앞서 보았던 필드 단위의 옵션들과 달리 모델 단위의 옵션이라고 볼 수 있다. 예를들면, 정렬 옵션(ordering), 데이터베이스 테이블 이름(db_table), 또는 읽기 좋은 이름이나 복수(plural) 이름을 지정해 줄 수 있다(verbose_name, verbose_name_plural). 모델클래스에 Meta 클래스를 반드시 선언해야 하는 것은 아니며, 모든 옵션을 모두 설정해야 하는 것도 아니다.


## Model methods

- `__unicode__()` (Python 2)
모델 객체가 문자열로 표현되어야 하는 경우에 호출된다. admin이나 console 에서 모델 객체를 표시하는 경우에 많이 쓰이게 된다.  

- `__str__()` (Python 3)
파이썬 3의 경우에는, `__unicode__()` 대신에 `__str__()` 로 선언한다.

- 기본 구현은 아무런 도움이 되지 않는 문자열을 리턴하기 때문에, 모든 모델에 대해 오버라이드 해서 알맞게 구현해주는게 좋다.

- `get_absolute_url()`
이 메서드는 Django가 해당 모델 객체의 URL을 계산할 수 있도록 한다. Django는 이 메서드를 모델 객체를 URL로 표현하는 경우에 사용하며, admin 사이트에서도 사용한다. 


## Model inheritance

Django 에서의 모델 상속은 파이썬에서의 클래스 상속과 거의 동일한 형태로 이루어진다. 단, 모델 상속의 경우에 베이스 클래스는 django.db.models.Model 클래스의 서브 클래스여야 한다. 

이때, 부모 모델이 자신의 데이터베이스 테이블을 가지도록 할 것인지, 아니면 부모 모델은 실제로 테이블을 생성하지 않고 자식 모델들이 부모 모델에 선언된 공통 필드를 각각 자신의 테이블에 생성할지를 결정해야 한다.


### Abstract base classes

추상 클래스 방식은 여러개의 모델 클래스가 공통적인 정보를 가지도록 하고 싶은 경우에 유용하다. Meta클래스에 abstract=True 옵션을 선언하면 그 모델 클래스는 추상클래스가 된다. 이렇게 만들어진 추상클래스는 데이터베이스에 테이블을 생성하지 않는다. 다만, 다른 모델들이 이 클래스를 상속받을 수 있으며, 부모클래스에 선언된 필드들은 자식 클래스의 테이블에 추가된다. 이때 부모 클래스와 자식 클래스가 동일한 이름의 필드를 가지고 있는 경우에는 Django가 예외를 발생시킨다.


### Meta inheritance

자식 클래스가 Meta 클래스를 가지지 않는 경우, 자식 클래스는 부모의 메타 클래스를 상속 받는다. 만약 자식 클래스에서 부모 Meta 클래스를 상속 받으려면 아래와 같이 부모 클래스에 선언된 Meta 클래스로부터 상속 받으면 된다. 

### Multi-table inheritance

Multi-table 상속은 부모 모델이든 자식 모델이든 모두 각자의 데이터베이스 테이블을 가진다. 즉, 공통부분의 데이터는 부모모델의 테이블에 저장하고, 자식모델의 데이터는 자식모델의 테이블에 저장되며, 자식 모델은 부모 모델에 대한 링크를 가진다. 이때, 링크는 내부적으로 OneToOneField를 사용한다.

ex) 

```
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)
```

### Meta and multi-table inheritance

multi-table 상속의 경우 기본적으로 자식모델은 부모모델의 Meta 클래스를 상속받지 않는다. 단, 자식모델에 ordering, get_latest_by 옵션이 지정되지 않은 경우에 한해, 부모 모델의 해당 설정값을 상속받는다.

## Proxy models

multi-table 상속을 사용하는 경우, 각각의 자식 클래스들 마다 테이블이 생성된다. 부모 모델이 가지는 데이터 이외에 추가적으로 자식 모델이 가지는 데이터를 저장하기 위한 당연한 동작이다. 하지만 가끔은 부모 모델의 메서드(파이썬 코드)만 재정의 한다던가 새로 추가하고 싶을 수도 있다. 즉, 테이블을 가지는 모델을 상속받되, 자식모델은 테이블을 만들필요가 없는 경우에 해당된다.

### Proxy model managers

Proxy 모델에 manager를 지정하지 않는 경우, 부모 모델의 manager를 상속받습니다. 직접 지정한 경우, 지정한 manager가 디폴트로 사용되며, 부모클래스의 manager도 사용할 수 있습니다.

ex) 

```
from django.db import models

class NewManager(models.Manager):
    # ...
    pass

class MyPerson(Person):
    objects = NewManager()

    class Meta:
        proxy = True
```

## Multiple inheritance

파이썬의 상속과 마찬가지로 Django 모델 또한 다중 상속(Multiple Inheritance)이 가능하다. 단, 이 경우 파이썬의 "name resolution rules" 이 적용된다. 예를들어, 부모 클래스들이 각각 Meta 클래스를 가지는 경우 첫번째 부모의 Meta 클래스를 상속받게 되며, 나머지 부모 클래스의 Meta 클래스는 무시된다.
