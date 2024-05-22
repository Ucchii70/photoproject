from django.urls import path
# viewsモジュールをインポート
from . import views

#viewsをインポートしてauth_viewsという名前で利用する
from django.contrib.auth import views as auth_views

# URLパターンを逆引きできるように名前をつける
app_name = 'accounts'
# URLパターンを登録するための変数
urlpatterns = [
    # サインアップページビューの呼び出し
    # 「 https://<ホスト名>/signup/ 」へのアクセスに対して、viewsモジュールのSignUpViewをインスタンス化する
    path('signup/',
         views.SignUpView.as_view(),
         name='signup'),

    # サインアップ完了ページのビューの呼びだし
    # 「 https://<ホスト名>/signup_success/ 」へのアクセスに対して、viewsモジュールのSignUpSuccessViewをインスタンス化する
    path('signup_success/', 
        views.SignUpSuccessView.as_view(),
        name='signup_success'),

    # ログインページの表示
    # https://<ホスト名>/login/へのアクセスに対して、django.contrib.auth.views.LoginViewをインスタンス化してログインページを表示する
    path('login/',
         #ログイン用のテンプレートフォームをレンダリング
         auth_views.LoginView.as_view(template_name='login.html'),
         name='login'
         ),
    # ログアウトを実行
    # https://<ホスト名>/logout/へのアクセスに対して、django.contrib.auth.views.logoutViewをインスタンス化してログアウトさせる
    path('logout/',
         auth_views.LogoutView.as_view(template_name='logout.html'),
         name='logout'
         ),
]