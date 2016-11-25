from LanguageAnalysis.pre_processing import data_integration as di
import LanguageAnalysis.filepath as fp
from pandas import DataFrame as df, Series
from LanguageAnalysis.data_processing.keyphrases import Keyphrase



def lang_integrated(create_data = False):
    if create_data is True:
        di.integrate_language_posts(file_read=fp.posts_file_xml, file_write=fp.post_integrated)

    keyphrase_gen = Keyphrase(integrate_data=False)
    keyphrase_gen.create_keyphrases(save_model=False, file_integrated = fp.post_integrated)
    language_keyphrase_map = keyphrase_gen.get_keyphrases()
    keyphrase_gen.save_keyphrases(language_keyphrase_map, fp.language_keyphrases, topn=30)



if __name__ == '__main__':
    lang_integrated(True)
    pass
