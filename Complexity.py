import requests
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

    # ASL jeb Average Sentence Length noskaidro, cik vidēji garš teikums ir.
    # ASL metrika = Kopējais vārdu skaits starp visiem teikumiem / Kopējais teikumu skaits
    def ASL(self):
        # Definē, kas ir teikums (Teksta vienība atdalīta ar beigu simbolu)
        sentences = re.split('[.!?]', self.text)
        # Noņem empty string sentences (tikai, ja eksistē teikums)
        sentences = [sentence for sentence in sentences if sentence.strip()]
        # Izveido sarakstu ar visiem vārdiem. Viens saraksta elements = viens vārds.
        # Ar len() metodi noskaidro saraksta garumu.
        words = self.tokenize()
        word_count = len(words)
        # Ar len() metodi noskaidro cik teikumi ir tekstā.
        sentences_count = len(sentences)
        # Aprēķina vidējo garumu teikumam.
        asl = word_count / sentences_count
        return asl

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
        return asw

    def flesch_reading_ease(self, asl, asw):
        metric_result = 206.835 - (1.015 * asl) - (84.6 * asw)
        return metric_result
    
    def flesch_reading_grade(self, flesch_reading_ease):
        grade_meaning = ""
        if flesch_reading_ease >= 90:
            grade_meaning = "Very easy to read. Vecuma līmenis: 9 gadi un zemāk"
        elif flesch_reading_ease >= 80:
            grade_meaning = "Easy to read. Vecuma līmenis: 9 gadi un zemāk"
        elif flesch_reading_ease >= 70:
            grade_meaning = "Fairly easy to read. Vecuma līmenis: 10 gadi"
        elif flesch_reading_ease >= 60:
            grade_meaning = "Plain English. Vecuma līmenis: 11 - 13 gadi"
        elif flesch_reading_ease >= 50:
            grade_meaning = "Fairly difficult to read. Vecuma līmenis: 13-15 gadi"
        elif flesch_reading_ease >= 30:
            grade_meaning = "Difficult to read. Līmenis: koledžas"
        elif flesch_reading_ease >= 10:
            grade_meaning = "Very difficult to read. Līmenis: koledžas absolvents"
        elif flesch_reading_ease >= 0:
            grade_meaning = "Extremely difficult to read. Līmenis: profesionāla"
        else:
            grade_meaning = "Nesekmīgi"

        return grade_meaning
    
    def complex_words(self, syllables):
        words_to_remove = []
        for word in syllables:
            hyphen_count = word.count('-')
            hyphen_count = hyphen_count + 1
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
        return metric_result

    def gunning_fog_grade(self, gunning_fog_grade):
        grade_meaning = ""
        if gunning_fog_grade >= 20:
            grade_meaning = "Post-graduate +"
        elif gunning_fog_grade >= 17:
            grade_meaning = "Post-graduate"
        elif gunning_fog_grade >= 16:
            grade_meaning = "College senior"
        elif gunning_fog_grade >= 13:
            grade_meaning = "College junior"
        elif gunning_fog_grade >= 11:
            grade_meaning = "High school senior"
        elif gunning_fog_grade >= 10:
            grade_meaning = "High school sophomore"
        elif gunning_fog_grade >= 9:
            grade_meaning = "High school freshman"
        elif gunning_fog_grade < 9:
            grade_meaning = "Middle school and below"
        else:
            grade_meaning = "Nesekmīgi"

        return grade_meaning

    def sentence_type(self, json_data):
        results = {}
        for key, value in json_data.items():
            sentences = value.get('sentences', [])
            text = value.get('text', '')

            sentence_results = []
            for sentence in sentences:
                tags = {'cs': False, 'cc': False}
                for token in sentence.get('tokens', []):
                    if token['tag'] == 'cs':
                        tags['cs'] = True
                    if token['tag'] == 'cc':
                        tags['cc'] = True
                
                if tags['cs'] and tags['cc']:
                    sentence_results.append({'teikums': text, 'uzbuve': 'Salikts jaukts'})
                elif tags['cs']:
                    sentence_results.append({'teikums': text, 'uzbuve': 'Salikts pakārtots'})
                elif tags['cc']:
                    sentence_results.append({'teikums': text, 'uzbuve': 'Salikts sakārtots'})
                else:
                    sentence_results.append({'teikums': text, 'uzbuve': 'Nevaru noteikt'})
            
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
            print(commaCount, sentencesCount)
            return average
        else:
            return 0
        
    def getWordAnalysis(self, words):
        analysisList = []
        for word in words:
            url = f"http://api.tezaurs.lv:8182/analyze/{word}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    analysisList.append(data)
                else:
                    print("Nav atrasti dati vārdam:", word)
            else:
                return f"Error: {response.status_code}"

        fields = []
        for items in analysisList:
            for item in items:
                field_dict = {
                    "Vārds": item.get("Vārds"),
                    "Mija": item.get("Mija"),
                }
                if "Izteiksme" in item:
                    field_dict["Izteiksme"] = item.get("Izteiksme")
                if "Pakāpe" in item:
                    field_dict["Pakāpe"] = item.get("Pakāpe")
                if "Kārta" in item:
                    field_dict["Kārta"] = item.get("Kārta")
                fields.append(field_dict)
        return fields

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
        # print(f"Sarežģītie vārdi: ", complex_words)
        cws_result = self.CWS(words, complex_words)
        gunning_fog_index_result = self.gunning_fog_index(asl_result, cws_result)

        print(f"Gunning fog indekss: ",gunning_fog_index_result)

        gunning_fog_index_grade = self.gunning_fog_grade(gunning_fog_index_result)

        print(f"Gunning fog klase: ", gunning_fog_index_grade)

        print("\n\n----------------Teikuma uzbūve------------------------\n")

        print(f"Vidējais zilbju daudzums vārdā (ASW): {asw}")
        print(f"Vidējais teikuma garums (ASL): {asl_result}\n")

        sentences = self.tokenizeSent()

        print("\n\n----------------Vārdu analīze------------------------\n")

        analysedWords = self.getWordAnalysis(words)
        formattedAnalysedWords = json.dumps(analysedWords, indent=4, ensure_ascii=False)
        analysedWords = [dict(t) for t in set(tuple(d.items()) for d in analysedWords if isinstance(d, dict))]
        formattedAnalysedWords = json.dumps(analysedWords, indent=4, ensure_ascii=False)
        print("Vārdu analīze:", formattedAnalysedWords)

        print("\n\n----------------Morfoloģiskā analīze------------------------\n")

        lvnlpanalysisData = self.LVNLPAnalysis(sentences)
        print("LV NLP analīze: ", lvnlpanalysisData)

        print("\n\n----------------Sintaktiskā analīze------------------------\n")
        
        parsedAnalysisData = json.loads(lvnlpanalysisData)
        sentenceType = self.sentence_type(parsedAnalysisData)
        print("Teikumu uzbūve: ", sentenceType)

        avgCommas = self.average_comma_count()
        print("Vidējo komatu skaits teikumā: ", avgCommas)

def main():
    text = '''Dzīvnieks lido, lai varētu dzīvot, bet nevis dzert. Lai šādu dzīvesstilu uzturētu vajag ūdeni. Es neesmu zaļš, bet nevajag mani apcelt. Viņš sacīja: "Nav jau man grūti to izdarīt, ja vien būtu palīgs"'''
    evaluator = ComplexityEval(text)
    evaluator.evaluate()

if __name__ == "__main__":
    main()