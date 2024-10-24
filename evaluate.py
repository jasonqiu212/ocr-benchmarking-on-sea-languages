"""This file provides operations to evaluate OCR performance."""

from torchmetrics.text import CharErrorRate

cer = CharErrorRate()
