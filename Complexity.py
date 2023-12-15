import requests
import argparse
import json
import re
import nltk
import spacy
from nltk.tokenize import sent_tokenize, word_tokenize
requests.packages.urllib3.disable_warnings()


class ComplexityEval:
    def __init__(self, text):
        self.text = text

    def clean(self):
        cleansed_words = re.sub(r'[^\w\s]', '', self.text)
        return cleansed_words

    def tokenize(self):
        cleansed_words = self.clean()
        tokens = word_tokenize(cleansed_words)
        return tokens

    def tokenizeSent(self):
        cleansed_sent = sent_tokenize(self.text)
        return cleansed_sent

    def ASL(self):
        sentences = re.split('[.!?]', self.text)
        sentences = [sentence for sentence in sentences if sentence.strip()]
        words = self.tokenize()
        word_count = len(words)
        sentences_count = len(sentences)
        asl = word_count / sentences_count
        return round(asl, 2)

    def replace_hyphens(self, data):
        return data.replace('<span class="hyphen">•</span>', '-')

    def syllableize(self, wordList):
        session = requests.Session()
        syllablesList = []
        response = session.get('https://www.ushuaia.pl/hyphen', verify=False)
        cookie = session.cookies.get_dict()
        if response.status_code == 200:
            if response:
                print(f'Pieslēgts cookie auth: ', cookie['hyphen'])
            else:
                print(f"Cookie auth error: {response.status_code}")
        for word in wordList:
            url = f"https://www.ushuaia.pl/hyphen/hyphenate.php?word={word}&lang=lv_LV"
            response = requests.get(url, cookies=cookie, verify=False)
            if response.status_code == 200:
                data = response.text
                cleanedData = self.replace_hyphens(data)
                syllablesList.append(cleanedData)
            else:
                print(f"Cookie auth error: {response.status_code}")
        return syllablesList

    def ASW(self, syllables):
        hyphen_counts = [syllable.count('-') + 1 for syllable in syllables]
        print(hyphen_counts)
        asw = sum(hyphen_counts) / len(hyphen_counts) if len(hyphen_counts) > 0 else 0
        return round(asw, 2)

    def flesch_reading_ease(self, asl, asw):
        print("Vidēji zilbes: ", asw)
        print("Videji teikuma garums: ", asl)
        metric_result = 206.835 - (1.015 * asl) - (84.6 * asw)
        return round(metric_result, 2)
    
    def flesch_reading_grade(self, flesch_reading_ease):
        grade_meaning = ""
        if flesch_reading_ease >= 90:
            grade_meaning = "Ļoti viegli lasāms. Vecuma līmenis: Pirmsskolas +"
        elif flesch_reading_ease >= 80:
            grade_meaning = "Viegli lasāms. Vecuma līmenis: 9 gadi +"
        elif flesch_reading_ease >= 70:
            grade_meaning = "Diezgan viegli lasāms. Vecuma līmenis: 10 gadi +"
        elif flesch_reading_ease >= 60:
            grade_meaning = "Vienkārši lasāms. Vecuma līmenis: 11 gadi +"
        elif flesch_reading_ease >= 50:
            grade_meaning = "Vidēji grūti lasāms. Vecuma līmenis: 13 gadi +"
        elif flesch_reading_ease >= 30:
            grade_meaning = "Grūti lasāms. Līmenis: koledžas, 18 gadi +"
        elif flesch_reading_ease >= 10:
            grade_meaning = "Ļoti grūti lasāms. Līmenis: koledžas absolvents, 21 gadi +"
        elif flesch_reading_ease >= 0:
            grade_meaning = "Ārkārtīgi grūti lasāms. Līmenis: profesionāla, 23 gadi +"
        else:
            grade_meaning = "Nevar noteikt. Samaziniet teikuma garumu."

        return grade_meaning
    
    def complex_words(self, syllables):
        words_to_remove = []
        for word in syllables:
            hyphen_count = word.count('-') + 1
            hyphen_count = hyphen_count
            if hyphen_count < 3:
                words_to_remove.append(word)

        for word_to_remove in words_to_remove:
            syllables.remove(word_to_remove)
        cleaned_complex_words = [syllable.replace('-', '') for syllable in syllables]
        return cleaned_complex_words

    def CWS(self, words, complex_words):
        cws = len(complex_words)/len(words)
        return cws

    def gunning_fog_index(self, asl, cws):
        metric_result = 0.4 * ((asl) + cws * 100)
        return round (metric_result, 2)

    def gunning_fog_grade(self, gunning_fog_grade):
        grade_meaning = "Līmenis: "
        if gunning_fog_grade >= 20:
            grade_meaning += "Universitātes"
        elif gunning_fog_grade >= 17:
            grade_meaning += "Vidusskolas absolventa"
        elif gunning_fog_grade >= 16:
            grade_meaning += "12. klases"
        elif gunning_fog_grade >= 13:
            grade_meaning += "10. - 11. klases"
        elif gunning_fog_grade >= 11:
            grade_meaning += "9. klases"
        elif gunning_fog_grade >= 10:
            grade_meaning += "8. klases"
        elif gunning_fog_grade >= 9:
            grade_meaning += "5. - 7. klases"
        elif gunning_fog_grade < 9:
            grade_meaning += "Sākumskolas un zem"
        else:
            grade_meaning += "Nevar noteikt. Samaziniet teikuma garumu."

        return grade_meaning

    def sentence_type(self, json_data):
        results = {}
        for key, value in json_data.items():
            sentences = value.get('sentences', [])
            text = value.get('text', '')

            sentence_results = []
            for sentence in sentences:
                tags = {'cs': False, 'cc': False, 'zc': False}
                for token in sentence.get('tokens', []):
                    if token['tag'] == 'cs':
                        tags['cs'] = True
                    if token['tag'] == 'cc':
                        tags['cc'] = True
                    if token['tag'] == 'zc':
                        tags['zc'] = True
                
                if tags['cs'] and tags['cc'] and tags['zc']:
                    sentence_results.append({'teikums': text, 'uzbuve': 'Salikts jaukts'})
                elif tags['cs'] and tags['zc'] and not tags['cc']:
                    sentence_results.append({'teikums': text, 'uzbuve': 'Salikts pakārtots'})
                elif tags['cc'] and tags['zc'] and not tags['cs']:
                    sentence_results.append({'teikums': text, 'uzbuve': 'Salikts sakārtots'})
                else:
                    sentence_results.append({'teikums': text, 'uzbuve': 'Vienkāršs'})
            
            results[key] = sentence_results
        return json.dumps(results, indent=2, ensure_ascii=False)

    def average_comma_count(self):
        sentences = self.text.split('.')
        sentencesCount = len(sentences)-1
        commaCount = 0
        for sentence in sentences:
            commaCount += sentence.count(',')
        if sentencesCount > 0:
            average = commaCount / sentencesCount
            return round(average, 2)
        else:
            return 0
    
    def NERCounter(self, analysisList):
        ner_count = 0
        for teikums in analysisList.values():
            for sentence in teikums['sentences']:
                ner_count += len(sentence['ner'])

        return ner_count
    
    def getLemma(self, analysisList):
        lemmas = []
        symbolPattern = re.compile(r'[^\w\s]')

        for teikums_key, teikums_value in analysisList.items():
            sentences = teikums_value.get('sentences', [])
            for sentence in sentences:
                tokens = sentence.get('tokens', [])
                for token in tokens:
                    lemma = token.get('lemma')
                    if lemma:
                        cleanLemma = symbolPattern.sub('', lemma)
                        if cleanLemma:
                            lemmas.append(cleanLemma)

        return lemmas
    
    def directSpeech(self, analysisList, sentencesTotal):
        directSpeechCount = 0
        for teikums_key, teikums_value in analysisList.items():
            sentences = teikums_value.get('sentences', [])
            for sentence in sentences:
                tokens = sentence.get('tokens', [])
                for i in range(len(tokens) - 1):
                    if tokens[i].get('lemma') == ':' and tokens[i + 1].get('lemma') == '"':
                        directSpeechCount += 1
        
        return round(directSpeechCount / len(sentencesTotal), 2)
    
    def simpleSentence(self, sentenceType, sentencesTotal):
        data = json.loads(sentenceType)
        simpleSentenceCount = sum(1 for teikums_list in data.values() for teikums_dict in teikums_list if teikums_dict.get('uzbuve') == 'Vienkāršs')
        return round(simpleSentenceCount / len(sentencesTotal), 2)

    def LVNLPAnalysis(self, sentencesSplit):
        api_url = 'https://nlp.ailab.lv/api/nlp'
        results = {}
        
        steps = None or ['tokenizer', 'morpho', 'parser', 'ner']

        for i, sentence in enumerate(sentencesSplit, start=1):
            payload = {'data': {'text': sentence}, 'steps': steps}
            r = requests.post(api_url, json=payload)
            
            if r.status_code == 200:
                data = r.json().get('data')
                results[f"Teikums #{i}"] = data
            else:
                results[f"Teikums #{i}"] = f"Error: {r.status_code}"
        
        return json.dumps(results, indent=2, ensure_ascii=False)

    def evaluate(self):

        print("----------------TEKSTA SAREŽĢĪTĪBA------------------------\n\n")

        print("----------------Lasāmības atribūtika------------------------\n")

        asl_result = self.ASL()
        
        words = self.tokenize()

        syllables = self.syllableize(words)
        print("Zilbju saraksts:\n", syllables, '\n')

        asw = self.ASW(syllables)

        flesch_reading_ease_result = self.flesch_reading_ease(asl_result, asw)
        print(f"Fleša lasīšanas viegluma aprēķins: ", flesch_reading_ease_result)

        flesch_reading_grade_result = self.flesch_reading_grade(flesch_reading_ease_result)
        print(f"Fleša – Kinkeida lasīšanas viegluma klase: ", flesch_reading_grade_result, '\n')

        complex_words = self.complex_words(syllables)
        cws_result = self.CWS(words, complex_words)
        gunning_fog_index_result = self.gunning_fog_index(asl_result, cws_result)

        print(f"Gunning fog indekss: ",gunning_fog_index_result)

        gunning_fog_index_grade = self.gunning_fog_grade(gunning_fog_index_result)

        print(f"Gunning fog klase: ", gunning_fog_index_grade)

        sentences = self.tokenizeSent()

        print("\n\n----------------Morfoloģiskā analīze------------------------\n")

        lvnlpanalysisData = self.LVNLPAnalysis(sentences)
        print("LV NLP analīze: ", lvnlpanalysisData)

        parsedAnalysisData = json.loads(lvnlpanalysisData)

        NERCount = self.NERCounter(parsedAnalysisData)
        print("Nosaukto entitāšu daudzums tekstā: ", NERCount)

        print("\n\n----------------Sintaktiskā analīze------------------------\n")
        
        sentenceType = self.sentence_type(parsedAnalysisData)
        print("Teikumu uzbūve: ", sentenceType)

        avgCommas = self.average_comma_count()
        print("Vidējo komatu skaits teikumā: ", avgCommas)
        
        directSpeechProportion = self.directSpeech(parsedAnalysisData, sentences)
        print("Tiešo runu īpatsvars: ", directSpeechProportion)

        simpleSentenceProportion = self.simpleSentence(sentenceType, sentences)
        print("Vienkāršo teikumu īpatsvars: ", simpleSentenceProportion)

        lemmas = self.getLemma(parsedAnalysisData)
        print("Lemmas:", lemmas)

def main(fileName):
    with open(fileName, 'r', encoding='utf-8') as file:
        text = file.read()
        if text:
            evaluator = ComplexityEval(text)
            evaluator.evaluate()
        else:
            print("Datnes saturs nesatur tekstu.") 
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process text from a file')
    parser.add_argument('-i', '--input', help='Input file name using -i', required=True)
    args = parser.parse_args()
    main(args.input)