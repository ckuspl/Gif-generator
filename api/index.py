@app.route("/", methods=['GET', 'POST'])
def upload():
    gif_ready = False
    error_message = ""
    content = ""

    if request.method == 'POST':
        files = request.files.getlist("images")
        if not files or all(f.filename == '' for f in files):
            error_message = "請選擇至少一張圖片。"
        else:
            images = []
            for file in files:
                if allowed_file(file.filename):
                    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                    file.save(filepath)
                    try:
                        with Image.open(filepath) as img:
                            img = img.convert("RGB").resize((512, 512))
                            images.append(img)
                    except Exception as e:
                        print(f"圖片讀取錯誤: {e}")
            if len(images) > 0:
                try:
                    images[0].save(
                        OUTPUT_GIF,
                        save_all=True,
                        append_images=images[1:],
                        duration=200,
                        loop=0
                    )
                    gif_ready = True
                except Exception as e:
                    error_message = f"GIF 生成錯誤: {e}"
            else:
                error_message = "無法處理上傳的圖片，請檢查檔案格式與內容。"

    if gif_ready:
        content = f'''<h3>動畫預覽：</h3>
        <img src="/{OUTPUT_GIF}"><br><br>
        <a href="/{OUTPUT_GIF}" download class="btn">下載動畫 GIF</a>'''
    elif error_message:
        content = f'<p style="color: red;">{error_message}</p>'

    return Response(HTML_PAGE.format(content=content), content_type='text/html')
