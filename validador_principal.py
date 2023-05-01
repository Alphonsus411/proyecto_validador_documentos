import sys
import os
import hashlib
import qrcode
import datetime
import PyPDF2
import io
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.documento = None
        self.nombre_documento = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Validador de Documentos")
        self.setGeometry(100, 100, 800, 500)

        self.boton_cargar = QPushButton("Cargar Documento", self)
        self.boton_cargar.move(50, 50)
        self.boton_cargar.clicked.connect(self.cargar_documento)

        self.label_documento = QLabel(self)
        self.label_documento.setGeometry(50, 100, 500, 200)

        self.boton_validar = QPushButton("Validar Documento", self)
        self.boton_validar.move(50, 320)
        self.boton_validar.clicked.connect(self.validar_documento)

        self.label_qr = QLabel(self)
        self.label_qr.setGeometry(400, 100, 150, 150)

    def cargar_documento(self):
        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        nombre_documento, _ = QFileDialog.getOpenFileName(self, "Cargar Documento", "",
                                                          "All Files (*);;PDF Files (*.pdf)", options=opciones)
        if nombre_documento:
            self.nombre_documento = nombre_documento
            self.documento = open(nombre_documento, "rb").read()
            pixmap = QPixmap("documento.png")
            self.label_documento.setPixmap(pixmap.scaled(500, 200, Qt.KeepAspectRatio))

    def generar_firma(self):
        if self.documento:
            # Obtener la fecha y hora actual
            fecha_actual = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

            # Obtener los metadatos del documento
            reader = PyPDF2.PdfFileReader(io.BytesIO(self.documento))
            info = reader.getDocumentInfo()

            # Generar el valor de hash SHA256 del contenido del documento, la fecha y hora actual y los metadatos
            hash_sha256 = hashlib.sha256(
                self.documento + str(fecha_actual).encode('utf-8') + str(info).encode('utf-8')).hexdigest()

            # Crear el código QR a partir del valor de hash SHA256
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(hash_sha256)
            qr.make(fit=True)
            imagen = qr.make_image(fill_color="black", back_color="white")
            imagen.save("codigo_qr.png")
            pixmap = QPixmap("codigo_qr.png")
            self.label_qr.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))

            # Escribir la fecha y hora actual y los metadatos en el documento
            writer = PyPDF2.PdfFileWriter()
            reader = PyPDF2.PdfFileReader(io.BytesIO(self.documento))
            writer.addPage(reader.getPage(0))
            page = writer.getPage(0)
            page.mergePage(PyPDF2.PdfFileReader(io.BytesIO(imagen.tobytes())).getPage(0))
            page.compressContentStreams()
            page.addMetadata({
                '/Fecha': PyPDF2.generic.createStringObject(fecha_actual),
                '/Metadatos': PyPDF2.generic.create})

            # Añadir metadatos a la página del documento
            page.addMetadata({
            "/CreationDate": fecha_actual,
            "/Title": "Documento sellado",
            "/Author": "Validador de Documentos"
            })

            # Crear el objeto QR que incluirá el hash y los metadatos
            qr_data = {
            "hash": hash_md5,
            "fecha": fecha_actual,
            "metadatos": page.getMetadata(),
            }

            # Convertir el objeto QR a una cadena JSON y calcular su hash
            qr_json = json.dumps(qr_data, sort_keys=True)
            qr_hash = hashlib.md5(qr_json.encode("utf-8")).hexdigest()

            # Crear el objeto QR y añadir la información al mismo
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_json)
            qr.make(fit=True)
            img_qr = qr.make_image(fill_color="black", back_color="white")

            # Crear un objeto PDFWriter y agregar el documento original y el código QR al nuevo archivo PDF
            writer = PyPDF2.PdfFileWriter()
            writer.addPage(page)
            buffer = io.BytesIO()
            img_qr.save(buffer, format="PNG")
            img_qr_data = buffer.getvalue()
            img_qr_io = io.BytesIO(img_qr_data)
            img_qr_pdf = PyPDF2.PdfFileReader(img_qr_io)
            writer.addPage(img_qr_pdf.getPage(0))

            # Escribir el nuevo archivo PDF en disco
            nombre_archivo, _ = os.path.splitext(self.nombre_documento)
            nombre_archivo_sellado = f"{nombre_archivo}_sellado.pdf"
            destino, _ = QFileDialog.getSaveFileName(self, "Guardar documento sellado", nombre_archivo_sellado, "Archivos PDF (*.pdf)")
            if destino:
                with open(destino, "wb") as f:
                    writer.write(f)

            # Escribir la información del documento sellado en un archivo de texto
            nombre_archivo_sellado, _ = os.path.splitext(os.path.basename(destino))
            ruta_archivo_info = os.path.join(os.path.dirname(destino), f"{nombre_archivo_sellado}_info.txt")
            with open(ruta_archivo_info, "w") as f:
                f.write(f"Nombre del archivo sellado: {nombre_archivo_sellado}\n")
                f.write(f"Fecha de sellado: {fecha_actual}\n")
                f.write(f"Hash del QR: {qr_hash}\n")
                f.write(f"Metadatos:\n")
                for clave, valor in page.getMetadata().items():
                    f.write(f"\t{clave}: {valor}\n")

            # Mostrar mensaje de éxito
            QMessageBox.information(self, "Documento sellado", "El documento ha sido sellado correctamente.")

            # mostrar mensaje de texto con información del documento sellado
            QMessageBox.information(self, "Documento sellado", f"El documento ha sido sellado correctamente.\nHash: {hash_md5}\nFecha de sellado: {fecha_sello}\nMetadatos: {metadatos}\nTrazabilidad: {trazabilidad}")

            # guardar el documento sellado
            documento_sellado = io.BytesIO()
            pdf_writer.write(documento_sellado)
            documento_sellado.seek(0)

            # mostrar el documento sellado en la interfaz
            pixmap = QPixmap("documento.png")
            self.label_documento.setPixmap(pixmap.scaled(500, 200, Qt.KeepAspectRatio))

            # generar la firma QR del documento sellado
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(hash_md5)
            qr.make(fit=True)
            qr.make_image(fill_color="black", back_color="white").save("codigo_qr.png")
            pixmap = QPixmap("codigo_qr.png")
            self.label_qr.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))

            # guardar el documento sellado en un archivo
            opciones = QFileDialog.Options()
            opciones |= QFileDialog.DontUseNativeDialog
            nombre_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar documento sellado", "", "Archivos PDF (*.pdf)", options=opciones)
            if nombre_archivo:
                with open(nombre_archivo, "wb") as f:
                     f.write(documento_sellado.getbuffer())

            QMessageBox.information(self, "Documento guardado", f"El documento sellado ha sido guardado correctamente en {nombre_archivo}.")
