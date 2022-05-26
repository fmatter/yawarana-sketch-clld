from clld.web.adapters.download import Download

def includeme(config):
    pass



class PdfDownload(Download):
    ext = 'pdf'
    description = "PDF version"
    name = "pdf"