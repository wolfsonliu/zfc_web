import io


def make_job_script(top_n_sgrna=None, top_n_gene=None):
    parameter = dict()
    parameter['input'] = '-i zfc_raw_count.txt'
    parameter['output'] = '-o zfc'
    if top_n_sgrna is None:
        parameter['top_n_sgrna'] = ''
    else:
        parameter['top_n_sgrna'] = '--top-n-sgrna {0}'.format(top_n_sgrna)

    if top_n_gene is None:
        parameter['top_n_gene'] = ''
    else:
        parameter['top_n_gene'] = '--top-n-sgrna {0}'.format(top_n_sgrna)
    script = 'zfc --plot {0} {1} {2} {3}'.format(
        parameter['input'], parameter['output'],
        parameter['top_n_sgrna'], parameter['top_n_gene']
    )
    return io.StringIO(
        '\n'.join([script, 'zip zfc_out.zip *.{pdf,txt,png}'])
    )
