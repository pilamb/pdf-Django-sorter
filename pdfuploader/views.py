# -*- coding: utf-8 -*-

import chardet
import hashlib
from datetime import datetime
from time import mktime, strptime

import pdfminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic.edit import DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy
# from django.core.files.storage import FileSystemStorage
from django.db.utils import IntegrityError

from .upload_form import UploadFileForm
from .models import Archive


def md5_forge_from_file(filename):
    """
    Prepares file to be hashed as a byte_string.
    """
    with open(filename, 'rb') as destination:
        data = destination.read()
    return md5_forge_from_string(data)


def md5_forge_from_string(InString):
    """
    request[File] is a IOBuffer and cant be hashed on the fly.
    It needs to be extracted as string, and then hashed separately.
    @params: str
    @Return: result as a md5 hash or Exception.
    """
    result = ''
    md = hashlib.md5()
    md.update(InString)
    try:
        result = md.hexdigest()
    except Exception as e:
        return HttpResponse("Bad forging md5, {} error...try again.", e)
    return result


def data_organizer(data):
    """
    Receives the data from scrap_data and makes a normalization with the model
    fields. Only wanted metadata is taken.
    @Return: organized_data:
        A dictionary with the normalized data, otherwise is empty.
    """
    labels = ['Title', 'Author', 'Creator', 'Producer', 'CreationDate',
              'ModDate', 'Tagged', 'Pages', 'Encrypted', 'Page size',
              'File size', 'Optimized', 'PDF version', 'Keywords']
    organized_data = {}
    for element in data:
        for label in labels:
            if label in element:
                if label == "CreationDate" or label == "ModDate":
                    if len(data[element]) > 17:  # I know...this is unpythonic xD
                        organized_data[label] = \
                                      datetime.fromtimestamp(mktime(strptime(data[element][2:-7], "%Y%m%d%H%M%S")))
                    else:
                        organized_data[label] = \
                                      datetime.fromtimestamp(mktime(strptime(data[element][2:-2], "%Y%m%d%H%M%S")))
                else:
                    organized_data[label] = data[element]

    if "hash_data" in data:
        organized_data['hash_data'] = data['hash_data']
    if "Size" in data:
        organized_data['Size'] = data['Size']
    return organized_data


def scrap_data(f):
    """
    PDF metadata is extracted here. Note that not all pdfs has metadata.
    The parser will output a dic inside a list. Data must be iterated to order
    and clasify it.
    @params: f: request['FILES']
    @Return: A dictionary with the metadata extracted, otherwise is empty.
    """
    return_data = {}
    parser = PDFParser(f)
    doc = PDFDocument(parser)
    if doc.info != "":
        for i in doc.info:
            for j, k in i.iteritems():  # TODO: no py3!
                if j != '' and k != '':
                    if j == "Trapped":  # PDF parser uses a strange type kind
                        if isinstance(k, pdfminer.psparser.PSLiteral):
                            k = str(k)
                    else:
                        if isinstance(k, str):
                            encoding = chardet.detect(k)['encoding']
                            return_data[j] = k.decode(encoding, 'replace')
    else:
        return_data = None
    return_data["hash_data"] = md5_forge_from_string(f.read())
    return_data["Size"] = f.size
    # if "Title" not in return_data: somepdfs have not title, even if visible
    return_data["Title"] = str(f).strip(".pdf")  # TODO: chardet here
    return return_data


def uploadpdf(request):
    """ View controlling update of files. It is also responsible for
    calling methods to extract the pdf metadata and to call the normalizing
    functions that make the normalization of the model fields.
    """
    archive = None

    archive_model_fields = [
        'hash_data', 'isbn', 'pages', 'size', 'keywords', 'url', 'uploader', 'locked',
        'producer', 'author', 'creationdate', 'title', 'creator']  # count: 12
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                scrapped_data = scrap_data(request.FILES['file'])
            except pdfminer.pdftypes.PDFException:
                return HttpResponse(
                    "Ciphered metadata. Sorry but can't be extracted. Try with another or clean the metadata.")
            if scrapped_data is not None:
                data_normalized = data_organizer(scrapped_data)
            else:
                data_normalized = None
            archive = form.save(commit=False)
            for key, value in data_normalized.iteritems():
                if key.lower() in archive_model_fields:
                    main_key = key.lower()
                    # there are kws in the pdf metadata, lets put them as tags
                    if main_key == 'keywords':
                        if ";" in data_normalized[key]:  # lets chop it
                            extracted_tags = data_normalized[key].split(";")
                        elif "-" in data_normalized[key]:
                            extracted_tags = data_normalized[key].split("-")
                        elif "," in data_normalized[key]:
                            extracted_tags = data_normalized[key].split(",")
                        else:
                            extracted_tags = data_normalized[key].split()
                        extracted_tags2 = list()
                        if len(extracted_tags) > 1:
                            for elem in extracted_tags:
                                if len(elem.split()) > 1:
                                    extracted_tags2.append(elem.strip().replace(" ", "-"))
                                else:
                                    extracted_tags2.append(elem.strip())
                        archive.__setattr__('tags', extracted_tags2[:5])
                        # only 5 tags are allowed
                    else:
                        archive.__setattr__(main_key, data_normalized[key])
            try:
                archive.save()
            except IntegrityError as e:
                return HttpResponse("Error: file already in the database (same hash), or {}".format(e))
            document = request.FILES
        else:
            data_normalized = {}
            document = {}
    else:
        archive = None
        document = {}
        scrapped_data = {}
        data_normalized = {}
        form = UploadFileForm()
    return render(request, 'pdfuploader/upload.html', {'form':
                                                       form,
                                                       'document':
                                                       document,
                                                       'archive':
                                                       archive,
                                                       'data_normalized':
                                                       data_normalized})


def listArchives(request):
    """
    View for listing archives.
    """
    try:
        archives = Archive.objects.all().order_by('-upload_date')
    except Archive.DoesNotExist:
        raise Http404("There are no files.")
    return render(request, 'pdfuploader/list.html', {'archives': archives})


def stats(request):
    """
    Show stats about the number of pdf uploaded, sizes, etc.
    """
    total_size = 0.0  # total size, Mb.
    cont_tags = 0
    stats_dict = {'total_archs': 0}
    try:
        archives = Archive.objects.all()
    except Archive.DoesNotExist:
        raise Http404("There are no files.")
    try:
        tags = Archive.tags.tag_model.objects.all()
        for i in Archive.tags.tag_model.objects.all():
            cont_tags += i.count
        stats_dict['tags'] = cont_tags
    except:
        pass
    stats_dict['total_archs'] = len(archives)
    for arch in archives:
        total_size += arch.size
    stats_dict['total_size'] = total_size
    return render(request, 'pdfuploader/stats.html', {'stats_dict': stats_dict})


def tags(request):
    """
    Shows tags and its use counter,
    and the archives with those tags.
    """
    etiquetas = Archive.tags.tag_model.objects.all()
    tagged_archives = {}
    for element in etiquetas:
        tagged_archives[element] = Archive.objects.filter(tags=element)
    return render(request, 'pdfuploader/tags.html', {
        'etiquetas': etiquetas,
        'ficheros': tagged_archives})


def tag_detail(request, slug):
    """
    A view where the archives related to a tag are shown through a tag slug.
    """
    try:
        found_tags = Archive.tags.tag_model.objects.filter(slug=slug.lower())
        archives = Archive.objects.filter(tags=found_tags)
    except Archive.DoesNotExist:
        archives = None
        found_tags = None
    return render(request, 'pdfuploader/tag_detail.html', {
                                                    'archives': archives,
                                                    'slug': slug,
                                                    })


class ArchiveDelete(DeleteView):
    """
    Delete view
    """
    model = Archive
    success_url = reverse_lazy('list_uploads')


class ArchiveUpdate(UpdateView):
    """
    View for editing.
    """
    model = Archive
    fields = ['title', 'url', 'tags', 'locked', 'produced_by',
              'author', 'producer', 'creator']
    exclude = ('file', 'hash', 'creationdate', )
    template_name = 'pdfuploader/edit_archive.html'
    success_url = reverse_lazy('list_uploads')
