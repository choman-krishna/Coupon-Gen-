import qrcode

def gen_qr(data, otp):

    data_str = ','.join(data)


    

    split_data = data_str.split(',')

    

    gen_img = qrcode.make(data_str)

    img_path = 'static/QR/' + otp +'.png'

    gen_img.save(img_path)
    
    return img_path

