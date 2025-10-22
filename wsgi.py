from apps.app import create_app

# 本番用の設定キー（例："production"）を指定
app = create_app("production")

if __name__ == "__main__":
    app.run()
