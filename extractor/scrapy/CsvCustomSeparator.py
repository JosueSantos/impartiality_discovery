# coding: utf-8

from scrapy.exporters import CsvItemExporter


class CsvCustomSeparator(CsvItemExporter):
    """
    Customização do arquivo CSV gerado, trocando o delimitador de vírgula por ponto e vírgula
    """
    
    def __init__(self, *args, **kwargs):
        kwargs['encoding'] = 'utf-8'
        kwargs['delimiter'] = ';'
        super(CsvCustomSeparator, self).__init__(*args, **kwargs)
