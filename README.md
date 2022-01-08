# Simple Weather API

Djangoで非常に簡単な天気情報を取得するAPIを開発。

以下に、簡潔だがその開発方法を記す。

# 環境構築

以下のプロジェクトをインストールする。(コマンド入力)

```
pip install django
pip install django-rest-framework
django-admin startproject met_office .
django-admin startapp weather_api
```

`met_office/settings.py`にアクセスして、変数`INSTALL_APPS`、`LANGUAGE_CODE`、`TIME_ZONE`を以下に変更する。

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 追加
    'rest_framework',
    'weather_api'
]

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'
```

これで基本的な環境設定は終了。

# 実装

## Modelの作成

```python
# weather_api/models.py
from django.db import models

# 天気の選択肢
DESCRIPTIONS = (
    (0, "Sunny"),
    (1, "Rain"),
    (3, "Cloudy"),
    (4, "Snow")
)

# 天気情報のモデル
class Description(models.Model):
    weather_description = models.IntegerField(choices=DESCRIPTIONS, default=0)
    temperature = models.FloatField()
    created_on = models.DateTimeField(auto_now_add=True)

    # 作成日時を基準にデータを降順に並べる
    class Meta:
        ordering = ['-created_on']
    
    # 作成日時を管理サイトに表示させる
    def __str__(self):
        return self.created_on
```

以上のプログラムを書き終えたら、以下のコマンドを入力して`db.sqlite3`(デフォルトのデータベース)を作成する

```
python manage.py makemigrations
python manage.py migrate
```

## シリアライザの作成

```python
# weather_api/serializers.py(新規作成)
from rest_framework import serializers
from .models import Description

class DescriptionSerializer(serializers.ModelSerializer):
    
    # 対象となるモデルと表示するデータを指定
    class Meta:
        model = Description
        fields = ['id', 'weather_description', 'temperature', 'created_on']
```

## Viewsの作成

```python
# weather_api/views.py
from rest_framework import viewsets
from .serializers import DescriptionSerializer
from .models import Description


class DescriptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer
```

## ルーティング設定

```python
# weather_api/urls.py(新規作成)
from django.urls import path, include
from weather_api import views
from rest_framework.routers import DefaultRouter

# ルーターのインスタンスを作成
router = DefaultRouter()

# 登録するデータとその情報を記録する
router.register('descriptions', views.DescriptionViewSet)

# Djangoに認識させるためのルーティングを設定する
urlpatterns = [
    path('', include(router.urls))
]
```

## 管理サイトへの登録

```python
# weather_api/admin.py
from django.contrib import admin
from .models import Description

admin.site.register(Description)
```

## プロジェクト側(`met_office`)のルーティング設定

```python
# met_office/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #これを書かないとアプリ側(weather_api)のルーティング設定が反映されないので要注意
    path('', include('weather_api.urls')),
]
```

## 管理者(`superuser`)の作成

```
python manage.py createsuperuser
```

あとは開発者サーバを実行して管理サイトにアクセスし、適当に情報を作成してトップページにアクセスすれば、簡易ではあるが天気情報を取得するAPIを実装できる。

# 開発環境

* Visual Studio Code 1.63
* Django 4.0
* Django REST Framework 3.13.0
* Python 3.10.1