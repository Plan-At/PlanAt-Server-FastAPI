from captcha.image import ImageCaptcha

image = ImageCaptcha()

captcha_text = '1234'

data = image.generate(captcha_text)
print(data.read())

image.write(captcha_text, 'CAPTCHA.png')  # create file in current directory
