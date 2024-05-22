# HTTP リクエストを処理し、指定されたテンプレートとコンテキストデータを使用して、レスポンスを生成するために使用
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render

# テンプレートを描画するためのビュー, listview(データベースから取得した複数のオブジェクトを表示するための汎用ビュー)
# detailview(写真詳細), deleteview(削除ビュー)
from django.views.generic import TemplateView, ListView, DetailView, DeleteView

# 新しいオブジェクトをデータベースに作成するためのビュー, ユーザーがフォームを提出すると、新しいオブジェクトが作成される
from django.views.generic import CreateView

# URL パターンの名前を使用して URL を解決する, Django のビュー内でリダイレクト先の URL を動的に解決、遅延評価を提供し、ビューが評価される時点では URL パターンの逆引きが行われる
from django.urls import reverse_lazy

# forms.pyからインポートし、ユーザーの入力データを受け取り、バリデーション(チェック)を行ったりデータベースに保存するために使用する
from .forms import PhotoPostForm

# クラスベースビューで関数ベースビューのデコレータ(シンプルな記述で機能を付与する)を使用する
from django.utils.decorators import method_decorator

# ユーザーがログインしていない場合にログインページにリダイレクトするデコレータ, 特定のビューへのアクセスを制限する
from django.contrib.auth.decorators import login_required

# modelsモジュールからモデルPhotoPostをインポート
from .models import PhotoPost

import os

from pathlib import Path

import photoproject.settings as set

#import logging


class IndexView(ListView):
    """
    トップページのビュー
    """
    # index.htmlをレンダリングする
    template_name = 'index.html'
    # 投稿日時を降順に並び替える
    queryset = PhotoPost.objects.order_by('-posted_at')
    # 1ページに表示するレコードの件数
    paginate_by = 9

# デコレータにより、CreatePhotoViewへのアクセスはログインユーザーに限定される
# ログイン状態でなければ、settings.pyのLOGIN_URLにリダイレクトされる
@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):
    """
    写真投稿ページのビュー
    PhotoPostFormで定義されているモデルとフィールドと連携して投稿データをデータベースに登録する

    Attributes:
        form_class:モデルとフィールドが登録されたフォームクラス
        template_name:レンダリングするテンプレート
        success_url:データベースへの登録完了後のリダイレクト先
    """
    # forms.pyのPhotopostFormをフォームクラスとして登録
    form_class = PhotoPostForm
    # レンダリングするテンプレート
    template_name = 'post_photo.html'
    # フォームデータ登録完了後のリダイレクト先
    success_url = reverse_lazy('photo:post_done')

    def form_valid(self, form):
        """
        CreateViewクラスのform_valid()をオーバーライド(サブクラス（派生クラス）が親クラス（基底クラス）のメソッドを再定義すること)
        フォームのバリデーション(整合性の検証)を通過した時に呼ばれる
        フォームクラスの登録をここで行う

        parameters:
            form(django.forms.Form):
                form_classに格納されているPhotoPostFormオブジェクト

        Return:
            HttpResponseRedirectオブジェクト:
                スーパークラスのform_varid()の戻り値を返すことで
                success_urlで設定されているURLにリダイレクトさせる
        """
        # commit = FalseにしてPOSTされたデータを取得
        postdata = form.save(commit=False)
        # 投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        # 投稿データをデータベースに登録
        postdata.save()
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)
    
class PostSuccessView(TemplateView):
    """
    投稿完了ページのビュー

    Attributes:
        template_name:レンダリングするテンプレート
    """
    # index.htmlをレンダリングする
    template_name = 'post_success.html'

# 特定のカテゴリに関連する最新の写真投稿(カテゴリ一覧)を取得するためのクエリを実行し、その結果をListViewで表示する
class CategoryView(ListView):
    """
    カテゴリページのビュー
    Attributes:
        template_name:レンダリングするテンプレート
        paginate_by:1ページに表示するレコードの件数
    """
    # index.htmlをレンダリングする
    template_name = 'index.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9

    # 特定のクエリを実行してデータベースからレコードを取得するためのメソッド
    def get_queryset(self):
        """
        クエリを実行する
        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset()のオーバーライド(継承、拡張、変更)によりクエリを実行する
        returns:クエリによって取得されたレコード
        """
        # self.kwargsでURLのパターンから抽出されたキーワード引数を保持する辞書を取得し、categoryキーの値(Categorysテーブルのid)を取得
        category_id = self.kwargs['category']
        # filter(フィールド名=id)で絞り込む, objects.filter=categoryフィールドが指定されたcategory_idに等しいPhotoPostオブジェクトを取得, 降順で
        categories = PhotoPost.objects.filter(category=category_id).order_by('-posted_at')
        # クエリによって取得されたレコードを返す
        return categories
    
# ユーザー一覧
class UserView(ListView):
    """
    ユーザーの投稿一覧ページのビュー
    Attribute:
        template_name:レンダリングするテンプレート
        paginate_by:1ページに表示されるレコードの件数
    """
    # index.htmlをレンダリングする
    template_name = 'index.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9

    def get_queryset(self):
        """
        クエリを実行する
        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset()のオーバーライドにより、クエリを実行する
        Returns:クエリによって取得されたレコード
        """
        # self.kwargsで、キーワードの辞書を取得し、userキーの値(ユーザーテーブルのid)を取得
        user_id = self.kwargs['user']
        # filter(フィールド名＝id)で絞り込む
        user_list = PhotoPost.objects.filter(user=user_id).order_by('-posted_at')
        # クエリによって取得されたレコードを返す
        return user_list
    
# 写真詳細ページ
class DetailView(DetailView):
    """
    詳細ページのビュー
    投稿記事の詳細を表示するので、DetailViewを継承する
    Attributes:
        template_name:レンダリングするテンプレート
        model:モデルのクラス
    """
    #post.htmlをレンダリングする
    template_name = 'detail.html'
    model = PhotoPost
    
# マイページを表示
class MypageView(ListView):
    """
    マイページのビュー
    Attributes:
        template_name:レンダリングするテンプレート
        paginate_by:1ページに表示するレコードの件数
    """
    # mypage.htmlをレンダリングする
    template_name = 'mypage.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9

    def get_queryset(self):
        """
        クエリを実行する
        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset()のオーバーライドにより、クエリを実行する
        Returns:クエリによって取得されたレコード
        """
        # 現在ログインしているユーザー名はHttpRequest.userに格納されている
        # filter(userフィールド=userオブジェクト)で絞り込む
        queryset = PhotoPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        
        # クエリによって取得されたレコードを返す
        return queryset

class PhotoDeleteView(DeleteView):
    """
    レコードの削除を行うビュー

    Attributes:
        model:モデル
        template_name:レンダリングするテンプレート
        paginate_by:1ページに表示するレコードの件数
        success_url:削除完了後のリダイレクト先
    """
    # 操作の対象はPhotoPostモデル
    model = PhotoPost
    # photo_delete.htmlをレンダリング
    template_name = 'photo_delete.html'
    # 処理完了後にマイページにリダイレクト
    success_url = reverse_lazy('photo:mypage')

    def delete(self, request, *args, **kwargs):
        """
        メソッドが実行されると、対応するレコードが削除され、
        指定されたsuccess_url（削除後にリダイレクトするURL）にリダイレクトされます。
        Parameters:
            self:PhotoDeleteViewオブジェクト
            request:WSGIRequest(HttpRequest)オブジェクト
            args:位置引数として渡される辞書(dict)
            kwargs:キーワード付きの辞書(dict)
            {'pk':21}のようにレコードのidが渡される

        Returns:
            HttpResponseRedirect(success_url)を返して
            success_urlにリダイレクト
        """
        
        # レコードの取得
        instance = self.delete()

        # # 画像のパスを取得
        image_path = os.path.join(set.MEDIA_ROOT, instance)

        # # 画像が存在する場合は削除
        if os.path.exists(image_path):
            os.remove(image_path)
        
        # スーパークラスのdelete()を実行
        return super().delete(request, *args, **kwargs)
