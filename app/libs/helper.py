from io import BytesIO
import qrcode

def createQrcodeWithurl(url):
    qr = qrcode.QRCode(version=1 ,  # 二维码大小 1～40
                       error_correction=qrcode.constants.ERROR_CORRECT_L ,  # 二维码错误纠正功能
                       box_size=10 ,  # 二维码 每个格子的像素数
                       border=4)  # 二维码与图片边界的距离

    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    byte_io = BytesIO()
    img.save(byte_io , 'PNG')
    byte_io.seek(0)
    return byte_io