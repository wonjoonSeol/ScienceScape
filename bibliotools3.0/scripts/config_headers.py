# Headers in files exported from WOS are mapped to their meanings below:

def gen(headers):
    HEADERS = {
      'accession_number' : headers[0], #'UT'
      'authors' : headers[1], #'AU'
      'author_keywords' : headers[2], #'DE'
      'keywords_plus' : headers[3], #'ID'
      'document_title' : headers[4], #'TI'
      'wos_categories' : headers[5], #'WC'
      'cited_references' : headers[6], #'CR'
      'author_address' : headers[7], #'C1'
      'year_published' : headers[8], #'PY'
      'twenty_nine_character_source_abbreviation' : headers[9], #'J9'
      'volume' : headers[10], #'VL'
      'beginning_page' : headers[11], #'BP'
      'doi' : headers[12], #'DI'
      'publication_type' : headers[13], #'PT'
      'document_type' : headers[14], #'DT'
      'wos_core_collection_times_cited' : headers[15], #'TC'
    }

    return HEADERS
