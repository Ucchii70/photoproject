from django.db import models

# Create your models here.
# accountsアプリのmodelsモジュールからCustomUserをインポート
from accounts.models import CustomUser

# djangoで提供されるベースのモデルクラス, データベースのテーブルを定義し、やりとりする
class Category(models.Model):
    """
    投稿する写真のカテゴリを管理するモデル
    """
    # カテゴリ名のフィールド
    title = models.CharField(
        verbose_name='カテゴリ',
        max_length=20
        )
    # def __str__(self)により、管理画面に表示されるモデル内のデータ（レコード）を判別するための、名前（文字列）を定義する
    def __str__(self):
        """
        オブジェクトを文字列に変換して返す
        Returns(str):カテゴリ名
        """
        return self.title

class PhotoPost(models.Model):
    """
    投稿されたデータを管理するモデル
    """
    # CustomUserモデル(user_id)とPhotoPostモデルを1対多の関係で結びつける
    # CustomUserが親でPhotoPostが子の関係となる
    user = models.ForeignKey(
        CustomUser,
        # フィールドのタイトル
        verbose_name='ユーザー',
        # ユーザーを削除する場合はそのユーザーの投稿データも全て削除する
        on_delete = models.CASCADE,
        blank=True,
        null=True
        )
    
    # Categoryモデル(title)とPhotoPostモデルを1対多の関係で結びつける
    # Categoryが親でPhotoPostが子の関係となる
    category = models.ForeignKey(
        Category,
        # フィールドのタイトル
        verbose_name='カテゴリ',
        # カテゴリに関連付けられた投稿データが存在する場合はそのカテゴリを削除できないようにする
        on_delete = models.PROTECT,
        blank=True, 
        null=True
        )
    
    # タイトル用のフィールド
    title = models.CharField(
        verbose_name='タイトル',
        max_length=200
        )
    
    # コメント用のフィールド
    comment = models.TextField(
        verbose_name='コメント',
        )
    
    # イメージのフィールド
    image1 = models.ImageField(
        verbose_name='イメージ1',
        upload_to='photos' # photosにファイルを保存
        )
    
    # イメージのフィールド2
    image2 = models.ImageField(
        verbose_name='イメージ2',
        upload_to='photos', # photosにファイルを保存
        blank='True', # フィールド値の設定は必須ではない
        null='True', # データベースにnullが保存されることを許容
        )
    
    # 投稿日時のフィールド
    posted_at = models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True # 日時を自動追加
        )
    
    def __str__(self):
        """
        オブジェクトを文字列に変換して返す
        Return(str):投稿記事のタイトル
        """
        return self.title






















