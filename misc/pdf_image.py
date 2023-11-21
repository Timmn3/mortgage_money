import fitz  # PyMuPDF
from PIL import Image


async def pdf_to_images(pdf_path):
    # Открываем PDF-файл
    pdf_document = fitz.open(pdf_path)

    # Проходим по страницам PDF и преобразуем их в изображения
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        image = page.get_pixmap()
        image_pil = Image.frombytes("RGB", [image.width, image.height], image.samples)

        # Сохраняем изображение
        image_pil.save(f"page_{page_number + 1}.png")

    # Закрываем PDF-документ
    pdf_document.close()

# Пример использования
pdf_file_path = "example.pdf"

pdf_to_images(pdf_file_path)
