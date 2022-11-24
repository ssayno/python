#!/usr/bin/env python3
from pdf2image import convert_from_path
ages = convert_from_path("eng.pdf", 50, size=(1389, 1965))
pages[0].save("OutImage.jpg", "JPEG")
